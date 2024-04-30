# This file is part of xenharmlib.
#
# xenharmlib is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# xenharmlib is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with xenharmlib. If not, see <https://www.gnu.org/licenses/>.

"""
The notation core module includes primitives to build notation systems.
A notation in xenharmlib is defined as a wrapper around a specific
tuning that provides a human-friendly string interface to all the
lower level objects (pitch, pitch interval, pitch scale)
"""

from typing import *
from abc import ABC
from abc import abstractmethod
from ..exc import UnknownNoteSymbol
from .notes import NatAccNote
from .notes import NatAccNoteInterval
from .note_scale import NatAccNoteScale
from .symbols import SymbolCode
from .symbols import SymbolValueNotMapped
from .symbols import UnknownSymbolString
from ..exc import IncompatibleNotations
from ..exc import InvalidPitchIndex
from ..exc import InvalidPitchClassIndex
from ..exc import InvalidNaturalIndex
from ..exc import InvalidAccidentalValue
from ..exc import InvalidNaturalDiffClassIndex
from .symbols import AmbiguousSymbol

NoteT = TypeVar('NoteT')
IntervalT = TypeVar('IntervalT')
ScaleT = TypeVar('ScaleT')


class NotationABC(ABC, Generic[NoteT, IntervalT, ScaleT]):
    """
    Abstract base class for all notations. A notation can be
    understood as a wrapper around the tuning, providing a
    string interface to the underlying integer system.

    Notations in the core package are defined as generics
    with three type variables: One for the note class,
    one for the interval class and one for the scale class.

    :param tuning: The tuning for which the notation should
        be constructed
    :param note_cls: The python class that is used to generate
        the note object in the note method.
    :param note_interval_cls: The python class that is used to
        generate a note interval object in the note_interval
        method.
    :param note_scale_cls: The python class that is used to
        generate a note scale object in the note_scale method.
    """

    def __init__(self,
                 tuning,
                 note_cls: type[NoteT],
                 note_interval_cls: type[IntervalT],
                 note_scale_cls: type[ScaleT]):

        self._tuning = tuning
        self._note_cls = note_cls
        self._note_interval_cls = note_interval_cls
        self._note_scale_cls = note_scale_cls

    def __eq__(self, other) -> bool:
        if not isinstance(other, self.__class__):
            return False
        return (
            self.tuning == other.tuning and \
            self._note_cls == other._note_cls and \
            self._note_interval_cls == other._note_interval_cls and \
            self._note_scale_cls == other._note_scale_cls
        )

    @property
    def tuning(self):
        """
        Returns the tuning this notation was built for
        """
        return self._tuning

    @abstractmethod
    def note(self, *args, **kwargs) -> NoteT:
        """
        (Must be overwritten by subclasses)
        Returns a note object of the note type this notation
        was initialized with
        """

    @abstractmethod
    def note_interval(self, note_a: NoteT, note_b: NoteT) -> IntervalT:
        """
        Returns a note interval of the note interval type this
        notation was initialized with

        :param note_a: The source note
        :param note_b: The target note
        """

    @abstractmethod
    def note_scale(self, notes: Optional[List[NoteT]] = None) -> ScaleT:
        """
        Returns a note scale of the note scale type this
        notation was initialized with

        :param notes: A list of notes
        """


class IncompleteNotation(Exception):
    """
    Gets raised when a notation was not initialized correctly
    """


class NatAccNotation(NotationABC[NatAccNote, NatAccNoteInterval, NatAccNoteScale]):
    """
    NatAccNotation is a notation for periodic tunings that select a
    subset of pitch classes called naturals to form a basic symbol
    set (typically letters) and adds special symbols called accidentals,
    which signify step deviations from the natural pitch classes.
    
    The standard western notation for example is a such a notation,
    defining 7 naturals (C, D, E, G, A, B) and 2 accidentals (#, b)
    that signify a step deviation of +1 and -1 respectively.

    The class assumes that there is exactly one symbol for each natural
    and exactly one symbol for each accidental value, meaning a pitch
    class symbol is uniquely defined through the combination of the
    natural's index and the accidental value, e.g. in 12-EDO (0, 1)
    will always map to 'C#' and (1, -1) will always map to 'Db'.
    Consequently the class is unfit to model notations that map
    different naturals to the same pitch class (for example the
    mapping of 12-EDO naturals to 5-EDO which conflates E and F)

    It further assumes that intervals are uniquely defined by the
    difference of natural indices and the difference in pitch and
    are notated as a tuple (symbol, number). The class implements
    the 1-based ordinal notation for numbers by default (e.g. the
    number 1 for a unison, the number 2 for a second, etc), however
    this behavior get be changed by subclassing and overwriting
    the method :meth:`nat_diff_to_interval_number` and its
    counterpart :meth:`interval_number_to_nat_diff`

    :param tuning: The tuning this notation refers to
    :param note_cls: Note class used in the :meth:`note` builder
        method (optional, defaults to the class NatAccNote)
    :param note_interval_cls: Note interval class used in the
        :meth:`note_interval` builder method (optional, defaults
        to the class NatAccNoteInterval)
    :param note_scale_cls: Note scale class used in the
        :meth:`note_scale` builder method (optional, defaults
        to the class NatAccNoteScale)
    """

    def __init__(self, 
        tuning, 
        note_cls: type[NatAccNote] = NatAccNote,
        note_interval_cls: type[NatAccNoteInterval] = NatAccNoteInterval,
        note_scale_cls: type[NatAccNoteScale] = NatAccNoteScale,
    ):

        super().__init__(
            tuning,
            note_cls,
            note_interval_cls,
            note_scale_cls
        )

        # the naturals list will include tuples with two elements.
        # a tuple (symbol, natc_pitch_index) at position k in the
        # list will mean the following: The natural with natc_index
        # k is notated by <symbol> and points to the pitch index
        # <natc_pitch_index>

        # the reason it is natc_pitch_index and not natc_pc_index
        # is that in some tunings naturals like B can refer to
        # pitches outside of the first base interval, for example
        # in notations of pentatonic EDOs where m2 = M2 the note
        # (B, 0) and (C, 1) refer to the same pitch

        self._naturals: List[Tuple[str, int]] = []

        self._acc_symbol_code: Optional[SymbolCode] = None
        self._interval_symbol_codes: Dict[int, SymbolCode] = {}

    # first we define the builder methods

    def note(self, pc_symbol: str, nat_bi_index: int) -> NatAccNote:
        """
        Creates a note in line with this notation

        :param pc_symbol: A symbol denoting the pitch class
            (typically someting like 'C#', 'Ab', 'F', etc)
        :param nat_bi_index: The base interval index of the
            natural (for example a B#-0 in 12-EDO has the natural base
            interval index of 0, even though the pitch is in base
            interval 1)
        """

        natc_symbol, acc_symbol, natc_index, acc_value = self.parse_pc_symbol(pc_symbol)
        nat_index = natc_index + (nat_bi_index * self.nat_count)

        chosen_note = self._note_cls(
            self,
            nat_index=nat_index,
            acc_value=acc_value,
            pc_symbol=pc_symbol,
            natc_symbol=natc_symbol,
            acc_symbol=acc_symbol
        )

        return chosen_note

    def note_interval(self, note_a: NatAccNote, note_b: NatAccNote) -> NatAccNoteInterval:
        """
        Creates a note interval between two notes created by
        this notation

        :raises IncompatibleNotations: If one of the notes has
            a different notation than this one

        :param note_a: The source note
        :param note_b: The target note
        """

        if note_a.notation is not self or note_b.notation is not self:
            raise IncompatibleNotations(
                'At least one of the given notes does not '
                'originate from this notation'
            )

        return self._note_interval_cls.from_notes(
            note_a,
            note_b
        )

    def note_scale(self, notes: Optional[List[NatAccNote]] = None) -> NatAccNoteScale:
        """
        Creates a note scale from a list of notes

        :raises IncompatibleNotations: If one of the notes has
            a different notation than this one

        :param notes: A list of notes created by this
            notation
        """

        if notes is None:
            notes = []

        for note in notes:
            if note.notation is not self:
                raise IncompatibleNotations(
                    'At least one of the given notes does not '
                    'originate from this notation'
                )

        return self._note_scale_cls(self, notes)

    def shorthand_interval(
        self,
        symbol: str,
        number: int
    ) -> NatAccNoteInterval:
        """
        Creates an interval without specifying two notes

        :param symbol: An interval symbol of this notation
            (for example P, A, M, m)
        :param number: An interval number indicating the interval
            step width according to the convention layed out by
            this notation
        """

        nat_diff = self.interval_number_to_nat_diff(number)
        abs_diff = abs(nat_diff)
        nat_diffc = abs_diff % self.nat_count
        pitch_diff_norm = self.nat_index_to_pitch_index(abs_diff)
        symbol_code = self._interval_symbol_codes[nat_diffc]

        norm_diff = symbol_code.get_value(symbol)
        abs_pitch_diff = pitch_diff_norm + norm_diff

        # pitch difference of the notes must be treated differently
        # if the interval direction is upwards or downwards.

        if nat_diff < 0:
            pitch_diff = - abs_pitch_diff
        else:
            pitch_diff = abs_pitch_diff

        # since this is an interval without any note information we
        # construct an arbitrary reference note with the restriction
        # that the interval from this reference note does not go over
        # the zero pitch threshold

        safe_bi = pitch_diff // len(self.tuning) + 1
        first_natc_symbol = self.get_natc_symbol(0)
        ref_note = self.note(first_natc_symbol, safe_bi)

        return self._note_interval_cls(
            self,
            ref_note,
            pitch_diff,
            nat_diff,
            symbol,
            number
        )

    def natural_scale(self, bi_index: int = 0) -> NatAccNoteScale:
        """
        Creates a scale with all the naturals in this notation
        in a specific base interval (in western notations this
        is typically the C major scale)

        :param bi_index: (optional, defaults to 0). The
            index of the base interval the notes should
            reside in
        """

        scale = self.note_scale()
        for natc_symbol, _ in self._naturals:
            note = self.note(natc_symbol, bi_index)
            scale.add_note(note)
        return scale

    # methods for mapping of natural indices / natural class
    # indices to pitch indices / pitch class indices

    def nat_index_to_pitch_index(self, nat_index: int) -> int:
        """
        Returns the pitch index a natural index refers to

        :param nat_index: A natural index
        """

        nat_bi_index, natc_index = divmod(nat_index, self.nat_count)
        natc_pitch_index = self.natc_pitch_indices[natc_index]
        return natc_pitch_index + len(self.tuning) * nat_bi_index

    def nat_index_to_pc_index(self, nat_index: int) -> int:
        """
        Returns the pitch class index a natural index refers to

        :raises InvalidNaturalIndex: If natural index is
            smaller than 0

        :param nat_index: A natural index
        """

        pitch_index = self.nat_index_to_pitch_index(nat_index)
        return pitch_index % len(self.tuning)

    def is_natural(self, pitch_index: int) -> bool:
        """
        Returns True if the given pitch index refers to
        a natural in this notation, False otherwise

        :param pitch_index: The pitch index to consider
        """

        pc_index = pitch_index % len(self.tuning)
        return pc_index in self.natc_pc_indices

    @property
    def nat_count(self) -> int:
        """
        Returns the number of registered natural symbols
        for this notation (typically 7 for western-style
        notations)
        """
        return len(self._naturals)

    @property
    def natc_pitch_indices(self) -> List[int]:
        """
        A sorted list of natural class pitch indices
        that are present in this notation
        """
        return [t[1] for t in self._naturals]

    @property
    def natc_pc_indices(self) -> List[int]:
        """
        A sorted list of natural class pitch class indices
        that are present in this notation
        """

        return [
            natc_pitch_index % len(self.tuning) \
                for natc_pitch_index in self.natc_pitch_indices
        ]

    # natural symbol processing

    def append_natural(self, natc_symbol: str, natc_pitch_index: int):
        """
        Appends a new natural to this notation. The order in which
        naturals are added determines their natural class index,
        so the first added natural will get natural class index 0,
        the second 1 and so forth.

        :raises AmbiguousSymbol: If given natural symbol already
            denotes a previously appended natural index

        :param natc_symbol: A string denoting the natural (typically
            a single letter)
        :param natc_pitch_index: The pitch index of the natural class
            that is added. For most tunings this pitch index is equal
            to the pitch class index, because for most tunings there
            exists no note tuple (natc_symbol, 0) that is not in the
            first base interval. However there are outliers like
            5-EDO in which (B, 0) = (C, 1) and (B, 0) has a pitch
            index in the second base interval
        """

        added_symbols = {t[0] for t in self._naturals}

        if natc_symbol in added_symbols:
            raise AmbiguousSymbol(
                f'Symbol {natc_symbol} is already used by a '
                f'previous natural class index'
            )

        self._naturals.append(
            (natc_symbol, natc_pitch_index)
        )

    def get_natc_symbol(self, nat_index: int) -> str:
        """
        Returns a string symbol for a natural index like
        0 -> 'C' or 8 -> 'D' in 12-EDO

        :raises InvalidNaturalIndex: If natural index is
            smaller than 0

        :param nat_index: A natural index of this notation
        """

        natc_index = nat_index % self.nat_count
        natc_symbol, _ = self._naturals[natc_index]
        return natc_symbol

    # accidental symbol code processing

    @property
    def acc_symbol_code(self) -> SymbolCode:
        """
        The symbol code for the accidentals. Must be set
        be the subclass constructor
        """
        if self._acc_symbol_code is None:
            raise IncompleteNotation(
                'No symbol code for accidentals was set'
            )
        return self._acc_symbol_code

    @acc_symbol_code.setter
    def acc_symbol_code(self, symbol_code: SymbolCode):
        self._acc_symbol_code = symbol_code

    def get_acc_symbol(self, acc_value: int) -> str:
        """
        Returns a symbol string for an accidental value,
        like 1 -> '#' or -1 -> 'b'

        :raises InvalidAccidentalValue: If the accidental symbol
            code of this notation does not have a symbol or
            symbol combination that maps to this value

        :param acc_value: An integer denoting the step deviation
            from the natural pitch class
        """

        try:
            return self.acc_symbol_code.get_symbol_str(
                acc_value
            )
        except SymbolValueNotMapped:
            raise InvalidAccidentalValue(
                f'Accidental value {acc_value} can not be '
                f'represented by this notation'
            )

    # interval symbol processing

    def set_interval_symbol_code(self,
                                 nat_diffc: int,
                                 symbol_code: SymbolCode):
        """
        Sets an interval class symbol for a natural index difference
        class. The natural index difference class is a number between
        0 and the number of naturals in the notation (exclusive), so
        e.g. [0, ..., 6] in a traditional western systems that has 7
        naturals. It is calculated by taking the absolute distance
        of two natural indices modulo the number of naturals in the
        notation, so e.g. 2 for intervals (C0, E#0), (C0, E1) and
        (E#2, C0).

        The natural index difference class is closely related to the
        roman numeral index of intervals, for example a difference of
        2 is the same as III, a difference of 0 the same as I, etc.

        Associating a natural index difference class with a specific
        symbol code allows setting different interval naming schemes
        for different interval numbers, e.g. making a difference
        between perfect and imperfect interval naming schemes. In
        the western system differences 0 (unison), 3 (fourth) and 4
        (fifth) use the P/A/d interval symbols while for differences
        1 (second), 2 (third), 5 (sixth), 6 (sevenths) the system
        M/m/A/d is used.

        :raises InvalidNaturalDiffClassIndex: If natural diff class
            index is out of bounds

        :param nat_diffc: The difference of the natural indices
            forming the interval modulo the naturals count
        :param symbol_code: A symbol code defining how the center and
            the deviations from it should be represented as strings.
        """

        if nat_diffc >= self.nat_count:
            raise InvalidNaturalDiffClassIndex(
                f'{nat_diffc} is not a valid natural diff class '
                f'index for this notation and tuning. Allowed '
                f'range is 0 to {self.nat_count - 1}'
            )

        self._interval_symbol_codes[nat_diffc] = symbol_code

    def get_interval_symbol(self, nat_diff, pitch_diff) -> str:
        """
        Returns the interval symbol for a natural/accidental note
        interval. Interval symbols depend on the natural index
        difference class of the two notes (e.g. if the interval
        is a unison, a third, a fifth, etc) and the deviation
        from a pitch difference norm (In 12-EDO this norm would
        e.g. be 7 for a fifth, 4 for a third, etc)

        :raises IncompleteNotation: If no symbol code was
            registered for the given parameters

        :param nat_diff: The difference in natural indices
        :param pitch_diff: The difference in pitch indices
        """

        # the natural index difference is an indicator whether
        # this is a upwards or downwards interval. intervals
        # can have a negative pitch difference but still be
        # considered upwards, if the natural index difference
        # is > 0, for example (C-0, Dbbb-0)

        # for the selection of the symbol code interval directions
        # do not matter, e.g. both (C-0, D#-0) and (D#-0, C-0) are
        # considered 'm' with roman numerals 2 and -2 respectively

        abs_diff = abs(nat_diff)
        nat_diffc = abs_diff % self.nat_count
        symbol_code = self._interval_symbol_codes.get(nat_diffc)
        pitch_diff_norm = self.nat_index_to_pitch_index(abs_diff)

        if symbol_code is None:
            raise IncompleteNotation(
                f'No interval symbol code for natural difference '
                f'class index {nat_diffc} was registered in '
                f'this notation'
            )

        # pitch difference of the notes must be treated differently
        # if the interval direction is upwards or downwards.

        if nat_diff < 0:
            pitch_diff = - pitch_diff
        else:
            pitch_diff = pitch_diff

        norm_diff = pitch_diff - pitch_diff_norm

        return symbol_code.get_symbol_str(norm_diff)

    def nat_diff_to_interval_number(self, nat_diff: int) -> int:
        """
        Returns an interval number for a natural index
        difference. By default it returns a 1-based ordinal number.
        Subclasses can change this behavior by overwriting this
        method.

        :param nat_diff: The natural index difference
            that characterizes the interval
        """
        if nat_diff >= 0:
            number = nat_diff + 1
        else:
            number = nat_diff - 1
        return number

    def interval_number_to_nat_diff(self, interval_number: int) -> int:
        """
        Returns a natural index difference for a interval number.
        By default it assumes that the interval number is given
        in 1-based ordinal notation. Subclasses can change this
        behavior by overwriting this method.

        :param interval_number: An interval number
        """
        if interval_number > 0:
            return interval_number - 1
        elif interval_number < 0:
            return interval_number + 1
        else:
            raise Exception('Invalid interval number') # TODO

    def parse_pc_symbol(self, pc_symbol: str) -> Tuple[str, str, int, int]:
        """
        Parses a pitch class symbol into its natural class symbol
        part and its accidental symbol part. Returns a 4-tuple
        (natc_symbol, acc_symbol, natc_index, acc_value) with
        the parsing result.
        """

        best_natc_symbol = ''
        best_natc_index = None

        for natc_index, (natc_symbol, _) in enumerate(self._naturals):

            if pc_symbol.startswith(natc_symbol):
                if len(natc_symbol) > len(best_natc_symbol):
                    best_natc_symbol = natc_symbol
                    best_natc_index = natc_index

        if best_natc_index is None:
            raise UnknownNoteSymbol(
                f'Could not find a natural that would '
                f'fit to {pc_symbol}.'
            )

        acc_tail = pc_symbol[len(best_natc_symbol):]

        try:
            acc_value = self.acc_symbol_code.get_value(acc_tail)
        except UnknownSymbolString:
            raise UnknownNoteSymbol(
                'Could not find a meaning for the accidentals'
            )

        return (best_natc_symbol, acc_tail, best_natc_index, acc_value)

    def gen_pc_symbol(self, natc_index: int, acc_value: int) -> Tuple[str, str, str]:
        """
        Creates a pitch class symbol from a natural class index and an
        accidental value. This defaults to calculating the first natural
        symbol found for natc_index and concatenating it with the minimal
        accidental symbol configuration for the value.

        The method will return a tuple of 3 with the following semantics:
        * First element will be the pitch class symbol
        * Second element will be the natural class symbol
        * Third element will be the accidental symbol string

        (Subclasses can overwrite this method if they e.g wish to generate
        pc_symbols that have post-fix or in-fix naturals)

        :param natc_index: A natural class index of a note
        :param acc_value: An accidental value
        """

        natc_symbol = self.get_natc_symbol(natc_index)
        acc_symbol = self.get_acc_symbol(acc_value)

        return (
            natc_symbol + acc_symbol,
            natc_symbol,
            acc_symbol
        )
