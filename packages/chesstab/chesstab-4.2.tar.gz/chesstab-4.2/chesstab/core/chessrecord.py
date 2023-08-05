# chessrecord.py
# Copyright 2008 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""Record definitions for chess game database.

The ...Game... classes differ in the PGN parser used as a superclass of the
...valueGame... class.  These generate different combinations of the available
data structures from the game score for the various display and update uses.
The ...Update classes allow editing of a, possibly incomplete, game score.

"""
from ast import literal_eval
import re

from solentware_base.core.record import KeyData, Value, ValueText, Record
from solentware_base.core.segmentsize import SegmentSize

from pgn_read.core.constants import (
    SEVEN_TAG_ROSTER,
    START_RAV,
    END_RAV,
    NON_MOVE,
    TAG_OPENING,
    TAG_DATE,
    SPECIAL_TAG_DATE,
    TAG_WHITE,
    TAG_BLACK,
    IFG_TAG_SYMBOL,
    IFG_TAG_STRING_VALUE,
    ERROR_START_COMMENT,
    )
from pgn_read.core.parser import (
    PGNDisplay,
    PGNRepertoireDisplay,
    PGNRepertoireTags,
    PGNRepertoireUpdate,
    PGNTags,
    )

from .pgnupdate import PGNUpdate
from .cqlstatement import CQLStatement
from .filespec import (
    POSITIONS_FIELD_DEF,
    SOURCE_FIELD_DEF,
    PIECESQUAREMOVE_FIELD_DEF,
    PIECEMOVE_FIELD_DEF,
    SQUAREMOVE_FIELD_DEF,
    GAMES_FILE_DEF,
    REPERTOIRE_FILE_DEF,
    OPENING_ERROR_FIELD_DEF,
    PGN_DATE_FIELD_DEF,
    VARIATION_FIELD_DEF,
    ENGINE_FIELD_DEF,
    PARTIALPOSITION_NAME_FIELD_DEF,
    RULE_FIELD_DEF,
    COMMAND_FIELD_DEF,
    )
from .analysis import Analysis
from .querystatement import QueryStatement, re_normalize_player_name
from .engine import Engine

PLAYER_NAME_TAGS = frozenset((TAG_WHITE, TAG_BLACK))


class ChessRecordError(Exception):
    pass


class ChessDBkeyGame(KeyData):
    
    """Primary key of chess game.
    """

    def __eq__(self, other):
        """Return (self == other).  Attributes are compared explicitly."""
        try:
            return self.recno == other.recno
        except:
            return False
    
    def __ne__(self, other):
        """Return (self != other).  Attributes are compared explicitly."""
        try:
            return self.recno != other.recno
        except:
            return True
        

class ChessDBvaluePGN(Value):
    
    """Methods common to all chess PGN data classes.
    """
    
    @staticmethod
    def encode_move_number(key):
        """Return base 256 string for integer with left-end most significant.
        """
        return key.to_bytes(2, byteorder='big')

    def load(self, value):
        """Get game from value."""
        self.get_first_game(literal_eval(value))

    def pack_value(self):
        """Return PGN text for game."""
        return repr(
            ''.join((''.join([''.join(('[',
                                       t.group(IFG_TAG_SYMBOL),
                                       '"',
                                       t.group(IFG_TAG_STRING_VALUE),
                                       '"]'))
                              for t in self.collected_game[0]]),
                     ''.join([t.group() for t in self.collected_game[2]]),
                     ''.join([t for t in self.collected_game[3]]),
                     )))
        

class ChessDBvalueGame(PGNDisplay, ChessDBvaluePGN):
    
    """Chess game data.

    Data is indexed by PGN Seven Tag Roster tags.

    """

    def __init__(self):
        """Extend with game source and move number encoder placeholders."""
        super(ChessDBvalueGame, self).__init__()

    def pack(self):
        """Return PGN text and indexes for game."""
        v = super(ChessDBvalueGame, self).pack()
        index = v[1]
        tags = self.collected_game[1]
        for field in tags:
            if field in PLAYER_NAME_TAGS:

                # PGN specification states colon is used to separate player
                # names in consultation games.
                index[field] = [' '.join(re_normalize_player_name.findall(tf))
                                for tf in tags[field].split(':')]

            elif field in SEVEN_TAG_ROSTER:
                index[field] = [tags[field]]
        if TAG_DATE in tags:
            index[PGN_DATE_FIELD_DEF] = [
                tags[TAG_DATE].replace(*SPECIAL_TAG_DATE)]
        return v


class ChessDBrecordGame(Record):
    
    """Chess game record customised for displaying the game score and tags.
    """

    def __init__(self):
        """Extend with move number encode and decode methods"""
        super(ChessDBrecordGame, self).__init__(
            ChessDBkeyGame,
            ChessDBvalueGame)

    def clone(self):
        """Return copy of ChessDBrecordGame instance.

        The bound method attributes are dealt with explicitly and the rest
        are handled by super(...).clone().  (Hope that DPT CR LF restrictions
        will be removed at which point the bound method attributes will not
        be needed.  Then ChessDBrecordGame.clone() can be deleted.)
        
        """
        # are conditions for deleting this method in place?
        clone = super(ChessDBrecordGame, self).clone()
        return clone

    @staticmethod
    def decode_move_number(skey):
        """Return integer from base 256 string with left-end most significant.
        """
        return int.from_bytes(skey, byteorder='big')
        
    def delete_record(self, database, dbset):
        """Delete record not allowed using ChessDBrecordGame class.

        Process the game using a ChessDBrecordGameUpdate instance

        """
        raise ChessRecordError

    def edit_record(self, database, dbset, dbname, newrecord):
        """Edit record not allowed using ChessDBrecordGame class.

        Process the game using a ChessDBrecordGameUpdate instance

        """
        raise ChessRecordError
        
    def get_keys(self, datasource=None, partial=None):
        """Return list of (key, value) tuples.
        
        The keys for the secondary databases in a ChessDatabase instance are
        embedded in, or derived from, the PGN string for the game.  All
        except the positions are held in self.value.collected_game[1].
        Multiple position keys can arise becuse all repetitions of a
        position are of interest.  The partial argument is used to select
        the relevant keys.  The position is in partial and the keys will
        differ in the move number.
        
        """
        dbname = datasource.dbname
        if dbname != POSITIONS_FIELD_DEF:
            if dbname == GAMES_FILE_DEF:
                return [(self.key.recno, self.srvalue)]
            elif dbname in self.value.collected_game[1]:
                return [(self.value.collected_game[1][dbname], self.key.pack())]
            else:
                return []
        if partial == None:
            return []
        
        moves = self.value.moves
        gamekey = datasource.dbhome.encode_record_number(self.key.pack())
        rav = 0
        ref = 0
        keys = []
        convert_format = datasource.dbhome.db_compatibility_hack

        p = tuple(partial)
        for mt in moves:
            if mt == START_RAV:
                rav += 1
            elif mt == END_RAV:
                rav -= 1
            elif mt == NON_MOVE:
                pass
            else:
                if mt[-1] == p:
                    record = (partial, None)
                    keys.append(convert_format(record, gamekey))
            ref += 1
        return keys
        
    def put_record(self, database, dbset):
        """Put record not allowed using ChessDBrecordGame class.

        Process the game using a ChessDBrecordGameUpdate instance

        """
        raise ChessRecordError


class ChessDBrecordGameText(Record):
    
    """Chess game record customised for processing the game score as text.
    
    Used to export games or repertoires from a database in the 'Import Format',
    see PGN specification 3.1, used to store the games.

    """

    def __init__(self):
        """Extend with move number encode and decode methods"""
        super(ChessDBrecordGameText, self).__init__(
            ChessDBkeyGame,
            ValueText)

    def clone(self):
        """Return copy of ChessDBrecordGameText instance.

        The bound method attributes are dealt with explicitly and the rest
        are handled by super(...).clone().  (Hope that DPT CR LF restrictions
        will be removed at which point the bound method attributes will not
        be needed.  Then ChessDBrecordGameText.clone() can be deleted.)
        
        """
        # are conditions for deleting this method in place?
        clone = super(ChessDBrecordGameText, self).clone()
        return clone

    @staticmethod
    def decode_move_number(skey):
        """Return integer from base 256 string with left-end most significant.
        """
        return int.from_bytes(skey, byteorder='big')
        
    def delete_record(self, database, dbset):
        """Delete record not allowed using ChessDBrecordGamePosition class.

        Process the game using a ChessDBrecordGameUpdate instance

        """
        raise ChessRecordError

    def edit_record(self, database, dbset, dbname, newrecord):
        """Edit record not allowed using ChessDBrecordGamePosition class.

        Process the game using a ChessDBrecordGameUpdate instance

        """
        raise ChessRecordError
        
    def put_record(self, database, dbset):
        """Put record not allowed using ChessDBrecordGamePosition class.

        Process the game using a ChessDBrecordGameUpdate instance

        """
        raise ChessRecordError


class ChessDBvalueGameTags(PGNTags, ChessDBvalueGame):
    
    """Chess game data excluding PGN movetext but including PGN Tags.
    """

    def __init__(self):
        """Extend with game source and move number encoder placeholders."""
        super(ChessDBvalueGameTags, self).__init__()

    def get_field_value(self, fieldname, occurrence=0):
        """Return value of a field occurrence, the first by default.

        Added to support Find and Where classes.

        """
        return self.collected_game[1].get(fieldname, None)

    #def get_field_values(self, fieldname):
    #    """Return tuple of field values for fieldname.

    #    Added to support Find and Where classes.

    #    """
    #    return self.get_field_value(fieldname),


class ChessDBrecordGameTags(Record):
    
    """Chess game record customised for displaying tag information for a game.
    """

    def __init__(self):
        """Extend with move number encode and decode methods"""
        super(ChessDBrecordGameTags, self).__init__(
            ChessDBkeyGame,
            ChessDBvalueGameTags)


class ChessDBrecordGamePosition(Record):
    
    """Chess game record customised for displaying the game score only.
    
    Much of the game structure to be represented in the row display is held
    in the Tkinter.Text object created for display.  Thus the processing of
    the record data is delegated to a PositionScore instance created when
    filling the grid.
    
    """

    def __init__(self):
        """Extend with move number encode and decode methods"""
        super(ChessDBrecordGamePosition, self).__init__(
            ChessDBkeyGame,
            ChessDBvalueGameTags)

    def clone(self):
        """Return copy of ChessDBrecordGamePosition instance.

        The bound method attributes are dealt with explicitly and the rest
        are handled by super(...).clone().  (Hope that DPT CR LF restrictions
        will be removed at which point the bound method attributes will not
        be needed.  Then ChessDBrecordGamePosition.clone() can be deleted.)
        
        """
        # are conditions for deleting this method in place?
        clone = super(ChessDBrecordGamePosition, self).clone()
        return clone

    @staticmethod
    def decode_move_number(skey):
        """Return integer from base 256 string with left-end most significant.
        """
        return int.from_bytes(skey, byteorder='big')
        
    def delete_record(self, database, dbset):
        """Delete record not allowed using ChessDBrecordGamePosition class.

        Process the game using a ChessDBrecordGameUpdate instance

        """
        raise ChessRecordError

    def edit_record(self, database, dbset, dbname, newrecord):
        """Edit record not allowed using ChessDBrecordGamePosition class.

        Process the game using a ChessDBrecordGameUpdate instance

        """
        raise ChessRecordError
        
    def put_record(self, database, dbset):
        """Put record not allowed using ChessDBrecordGamePosition class.

        Process the game using a ChessDBrecordGameUpdate instance

        """
        raise ChessRecordError


class ChessDBvaluePGNUpdate(PGNUpdate, ChessDBvaluePGN):
    
    """Chess game data with position, piece location, and PGN Tag, indexes."""
    
    # Replaces ChessDBvaluePGNUpdate and ChessDBvalueGameImport which had been
    # identical for a considerable time.
    # Decided that PGNUpdate should remain in pgn.core.parser because that code
    # generates data while this code updates a database.
    # ChessDBvalueGameImport had this comment:
    # Implication of original is encode_move_number not supported and load in
    # ChessDBvaluePGN superclass is used.

    def __init__(self):
        """Extend with game source and move number encoder placeholders."""
        super().__init__()
        self.gamesource = None

    def pack(self):
        """Return PGN text and indexes for game."""
        v = super().pack()
        index = v[1]
        cg = self.collected_game
        if self.do_full_indexing():
            tags = cg[1]
            for field in SEVEN_TAG_ROSTER:
                if field in PLAYER_NAME_TAGS:

                    # PGN specification states colon is used to separate player
                    # names in consultation games.
                    index[field
                          ] = [' '.join(re_normalize_player_name.findall(tf))
                               for tf in tags[field].split(':')]

                else:
                    index[field] = [tags[field]]
            index[POSITIONS_FIELD_DEF] = cg[4]
            index[PIECESQUAREMOVE_FIELD_DEF] = cg[5]
            index[PIECEMOVE_FIELD_DEF] = cg[6]
            index[SQUAREMOVE_FIELD_DEF] = cg[7]
            index[PGN_DATE_FIELD_DEF] = [
                tags[TAG_DATE].replace(*SPECIAL_TAG_DATE)]
        else:
            index[SOURCE_FIELD_DEF] = [self.gamesource]
        return v

    def set_game_source(self, source):
        """Set the index value to use if full indexing is not to be done."""
        self.gamesource = source

    def do_full_indexing(self):
        """Return True if full indexing is to be done.

        Detected PGN errors are wrapped in a comment starting 'Error: ' so
        method is_pgn_valid() is not used to decide what indexing to do.
        """
        return self.gamesource is None

    def is_error_comment_present(self):
        """Return True if an {Error: ...} comment is in the PGN text.

        The string attribute of any re.match object for PGN text will do to
        get the answer.
        """
        return ERROR_START_COMMENT in self.collected_game[2][0].string
    

class ChessDBrecordGameUpdate(Record):
    
    """Chess game record customized for editing database records.

    Used to edit or insert a single record by typing in a widget.

    """

    def __init__(self):
        """Extend with move number encode and decode methods"""
        super(ChessDBrecordGameUpdate, self).__init__(
            ChessDBkeyGame,
            ChessDBvaluePGNUpdate)

    def clone(self):
        """Return copy of ChessDBrecordGameUpdate instance.

        The bound method attributes are dealt with explicitly and the rest
        are handled by super(...).clone().  (Hope that DPT CR LF restrictions
        will be removed at which point the bound method attributes will not
        be needed.  Then ChessDBrecordGameUpdate.clone() can be deleted.)
        
        """
        # are conditions for deleting this method in place?
        clone = super(ChessDBrecordGameUpdate, self).clone()
        return clone

    @staticmethod
    def decode_move_number(skey):
        """Return integer from base 256 string with left-end most significant.
        """
        return int.from_bytes(skey, byteorder='big')
        
    def get_keys(self, datasource=None, partial=None):
        """Return list of (key, value) tuples.
        
        The keys for the secondary databases in a ChessDatabase instance are
        embedded in, or derived from, the PGN string for the game.  All
        except the positions are held in self.value.collected_game[1].
        Multiple position keys can arise becuse all repetitions of a
        position are of interest.  The partial argument is used to select
        the relevant keys.  The position is in partial and the keys will
        differ in the move number.
        
        """
        dbname = datasource.dbname
        if dbname != POSITIONS_FIELD_DEF:
            if dbname == GAMES_FILE_DEF:
                return [(self.key.recno, self.srvalue)]
            elif dbname in self.value.collected_game[1]:
                return [(self.value.collected_game[1][dbname], self.key.pack())]
            else:
                return []
        if partial == None:
            return []
        
        moves = self.value.moves
        gamekey = datasource.dbhome.encode_record_number(self.key.pack())
        rav = 0
        ref = 0
        keys = []
        convert_format = datasource.dbhome.db_compatibility_hack

        p = tuple(partial)
        for mt in moves:
            if mt == START_RAV:
                rav += 1
            elif mt == END_RAV:
                rav -= 1
            elif mt == NON_MOVE:
                pass
            else:
                if mt[-1] == p:
                    record = (partial, None)
                    keys.append(convert_format(record, gamekey))
            ref += 1
        return keys
        
    def load_instance(self, database, dbset, dbname, record):
        """Extend to set source for game if necessary."""
        super(ChessDBrecordGameUpdate, self).load_instance(
            database, dbset, dbname, record)
    
        # Never called because attribute is not bound anywhere and no
        # exceptions are seen ever.
        # Until ..tools.chesstab-4-1-1_castling-option-correction written, and
        # following code commented.  I assume the idea made sense once!
        # Might as well let superclass method be used directly.
        #if self.value.callbacktried:
        #    pass
        #elif self.value.callbacktried == None:
        #    pass
        #elif not self.value.callbacktried:
        #    self.value.set_game_source(record[0])
    

class ChessDBrecordGameImport(Record):
    
    """Chess game record customised for importing games from PGN files.

    Used to import multiple records from a PGN file.

    """

    def __init__(self):
        """Customise Record with chess database import key and value classes"""
        super(ChessDBrecordGameImport, self).__init__(
            ChessDBkeyGame,
            ChessDBvaluePGNUpdate)

    def import_pgn(self, database, source, sourcename, reporter=None):
        """Update database with games read from source."""
        self.set_database(database)
        #self.value.set_game_source(sourcename)
        if reporter is not None:
            reporter('Extracting games from ' + sourcename)
        ddup = database.deferred_update_points
        db_segment_size = SegmentSize.db_segment_size
        value = self.value
        count = 0
        for d in value.read_games(
            source,
            housekeepinghook=database.deferred_update_housekeeping):
            value.set_game_source(
                sourcename if not value.is_pgn_valid() else None)
            self.key.recno = None#0
            self.put_record(self.database, GAMES_FILE_DEF)
            if reporter is not None:
                if not count:
                    base = self.key.recno - self.key.recno % db_segment_size
                count += 1
                if self.key.recno % db_segment_size in ddup:
                    reporter(' '.join(('Game',
                                       str(count),
                                       'stored as record',
                                       str(self.key.recno),
                                       'offset',
                                       str(self.key.recno - base))))
        if reporter is not None:
            reporter('Extraction from ' + sourcename + ' done')
            reporter('', timestamp=False)


class ChessDBkeyPartial(KeyData):
    
    """Primary key of partial position record.
    """


class ChessDBvaluePartial(CQLStatement, Value):
    
    """Partial position data.
    """

    def __init__(self):
        super(ChessDBvaluePartial, self).__init__()

    def __eq__(self, other):
        """Return (self == other).  Attributes are compared explicitly."""
        try:
            if (self.get_name_statement_text() !=
                other.get_name_statement_text()):
                return False
            else:
                return True
        except:
            return False

    def __ne__(self, other):
        """Return (self != other).  Attributes are compared explicitly."""
        try:
            if (self.get_name_statement_text() ==
                other.get_name_statement_text()):
                return False
            else:
                return True
        except:
            return True
    
    def load(self, value):
        """Set partial position from value"""
        self.process_statement(literal_eval(value))

    def pack_value(self):
        """Return partial position value"""
        return repr(self.get_name_statement_text())

    def pack(self):
        """Extend, return partial position record and index data."""
        v = super().pack()
        index = v[1]
        index[PARTIALPOSITION_NAME_FIELD_DEF] = [self.get_name_text()]
        return v
        

class ChessDBrecordPartial(Record):
    
    """Partial position record.
    """

    def __init__(self):
        """Extend as a partial position record."""
        super(ChessDBrecordPartial, self).__init__(
            ChessDBkeyPartial,
            ChessDBvaluePartial)
        
    def get_keys(self, datasource=None, partial=None):
        """Return list of (key, value) tuples.
        
        The partial position name is held in an attribute which is not named
        for the field where it exists in the database.
        
        """
        if datasource.dbname == PARTIALPOSITION_NAME_FIELD_DEF:
            return [(self.value.get_name_text(), self.key.pack())]
        else:
            return super().get_keys(datasource=datasource, partial=partial)

    def load_value(self, value):
        """Load self.value from value which is repr(<data>).

        Set database in self.value for query processing then delegate value
        processing to superclass.

        """
        self.value.set_database(self.database)
        self.value.dbset = GAMES_FILE_DEF
        super().load_value(value)
        

# Not quite sure what customization needed yet
class ChessDBvalueRepertoire(PGNRepertoireDisplay, Value):
    
    """Repertoire data using custom non-standard tags in PGN format.
    """

    def __init__(self):
        """Extend with game source and move number encoder placeholders."""
        super(ChessDBvalueRepertoire, self).__init__()

    def load(self, value):
        """Get game from value."""
        self.get_first_game(literal_eval(value))


# Not quite sure what customization needed yet
class ChessDBvalueRepertoireTags(PGNRepertoireTags, ChessDBvalueRepertoire):
    
    """Repertoire data using custom non-standard tags in PGN format.
    """

    def __init__(self):
        """Extend with game source and move number encoder placeholders."""
        super(ChessDBvalueRepertoireTags, self).__init__()

    def load(self, value):
        """Get game from value."""
        self.get_first_game(literal_eval(value))


# Not quite sure what customization needed yet
class ChessDBvalueRepertoireUpdate(PGNRepertoireUpdate, ChessDBvaluePGN):
    
    """Repertoire data using custom non-standard tags in PGN format.
    """

    def __init__(self):
        """Extend with game source and move number encoder placeholders."""
        super(ChessDBvalueRepertoireUpdate, self).__init__()
        self.gamesource = None

    def pack(self):
        """Return PGN text and indexes for game."""
        v = super(ChessDBvalueRepertoireUpdate, self).pack()
        index = v[1]
        tags = self.collected_game[1]
        if self.is_pgn_valid():
            index[TAG_OPENING] = [tags[TAG_OPENING]]
        elif tags[TAG_OPENING]:
            index[TAG_OPENING] = [tags[TAG_OPENING]]
        else:
            index[TAG_OPENING] = [self.gamesource]
        return v

    def set_game_source(self, source):
        """Set game source (the PGN file name or '')"""
        self.gamesource = source


# Not quite sure what customization needed yet
class ChessDBrecordRepertoire(ChessDBrecordGame):
    
    """Repertoire record customised for exporting repertoire information.
    """

    def __init__(self):
        """Extend with move number encode and decode methods"""
        # Skip the immediate superclass __init__ to fix key and value classes
        super(ChessDBrecordGame, self).__init__(
            ChessDBkeyGame,
            ChessDBvalueRepertoire)


# Not quite sure what customization needed yet
class ChessDBrecordRepertoireTags(ChessDBrecordGameTags):
    
    """Repertoire record customised for displaying repertoire tag information.
    """

    def __init__(self):
        """Extend with move number encode and decode methods"""
        # Skip the immediate superclass __init__ to fix key and value classes
        super(ChessDBrecordGameTags, self).__init__(
            ChessDBkeyGame,
            ChessDBvalueRepertoireTags)
    

# Not quite sure what customization needed yet
class ChessDBrecordRepertoireUpdate(ChessDBrecordGameUpdate):
    
    """Repertoire record customized for editing repertoire records.
    """

    def __init__(self):
        """Extend with move number encode and decode methods"""
        # Skip the immediate superclass __init__ to fix key and value classes
        super(ChessDBrecordGameUpdate, self).__init__(
            ChessDBkeyGame,
            ChessDBvalueRepertoireUpdate)
        
    def get_keys(self, datasource=None, partial=None):
        """Return list of (key, value) tuples.
        
        The keys for the secondary databases in a ChessDatabase instance are
        embedded in, or derived from, the PGN string for the game.  All
        except the positions are held in self.value.collected_game[1].
        Multiple position keys can arise becuse all repetitions of a
        position are of interest.  The partial argument is used to select
        the relevant keys.  The position is in partial and the keys will
        differ in the move number.
        
        """
        dbname = datasource.dbname
        if dbname == REPERTOIRE_FILE_DEF:
            return [(self.key.recno, self.srvalue)]
        elif dbname in self.value.collected_game[1]:
            return [(self.value.collected_game[1][dbname], self.key.pack())]
        else:
            return []
        

class ChessDBvalueAnalysis(Analysis, Value):
    
    """Chess engine analysis data for a position.
    """

    def __init__(self):
        """"""
        super().__init__()

    def pack(self):
        """Extend, return analysis record and index data."""
        v = super().pack()
        index = v[1]
        index[VARIATION_FIELD_DEF] = [self.position]
        index[ENGINE_FIELD_DEF] = [k for k in self.scale]
        return v


class ChessDBrecordAnalysis(Record):
    
    """Chess game record customised for chess engine analysis data.

    No index values are derived from PGN move text, so there is no advantage in
    separate classes for display and update.  The PGN FEN tag provides the only
    PGN related index value used.
    
    """

    def __init__(self):
        """Delegate using ChessDBkeyGame and ChessDBvalueAnalysis classes."""
        super().__init__(KeyData, ChessDBvalueAnalysis)


class ChessDBkeyQuery(KeyData):
    
    """Primary key of game selection rule record.
    """


class ChessDBvalueQuery(QueryStatement, Value):
    
    """Game selection rule data.
    """

    def __init__(self):
        super(ChessDBvalueQuery, self).__init__()

    def __eq__(self, other):
        """Return (self == other).  Attributes are compared explicitly."""
        try:
            if (self.get_name_query_statement_text() !=
                other.get_name_query_statement_text()):
                return False
            else:
                return True
        except:
            return False

    def __ne__(self, other):
        """Return (self != other).  Attributes are compared explicitly."""
        try:
            if (self.get_name_query_statement_text() ==
                other.get_name_query_statement_text()):
                return False
            else:
                return True
        except:
            return True
    
    def load(self, value):
        """Set game selection rule from value"""
        self.process_query_statement(literal_eval(value))

    def pack_value(self):
        """Return gameselection rule value"""
        return repr(self.get_name_query_statement_text())

    def pack(self):
        """Extend, return game selection rule record and index data."""
        v = super().pack()
        index = v[1]
        index[RULE_FIELD_DEF] = [self.get_name_text()]
        return v
        

class ChessDBrecordQuery(Record):
    
    """Game selection rule record.
    """

    def __init__(self):
        """Extend as a game selection rule record."""
        super(ChessDBrecordQuery, self).__init__(
            ChessDBkeyQuery,
            ChessDBvalueQuery)
        
    def get_keys(self, datasource=None, partial=None):
        """Return list of (key, value) tuples.
        
        The game selection rule name is held in an attribute which is not named
        for the field where it exists in the database.
        
        """
        if datasource.dbname == RULE_FIELD_DEF:
            return [(self.value.get_name_text(), self.key.pack())]
        else:
            return super().get_keys(datasource=datasource, partial=partial)

    def load_value(self, value):
        """Load self.value from value which is repr(<data>).

        Set database in self.value for query processing then delegate value
        processing to superclass.

        """
        self.value.set_database(self.database)
        self.value.dbset = GAMES_FILE_DEF
        super().load_value(value)


class ChessDBkeyEngine(KeyData):
    
    """Primary key of chess engine record.
    """


class ChessDBvalueEngine(Engine, Value):
    
    """Game selection rule data.
    """

    def __init__(self):
        super(ChessDBvalueEngine, self).__init__()

    def pack(self):
        """Extend, return game selection rule record and index data."""
        v = super().pack()
        index = v[1]
        index[COMMAND_FIELD_DEF] = [self.get_name_text()]
        return v
        

class ChessDBrecordEngine(Record):
    
    """Chess engine record.
    """

    def __init__(self):
        """Extend as a game selection rule record."""
        super(ChessDBrecordEngine, self).__init__(
            ChessDBkeyEngine,
            ChessDBvalueEngine)
