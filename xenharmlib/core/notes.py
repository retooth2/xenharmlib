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
The note core module implements primitives to handle different types
of notes and note intervals. Notes and note intervals wrap the integer
based pitch and pitch interval classes.
"""

from __future__ import annotations

from typing import *
from functools import total_ordering
from abc import ABC
from abc import abstractmethod
from .protocols import PeriodicPitchLike
from .frequencies import Frequency
from .pitch import PeriodicPitch
from .protocols import HasFrequency
from .protocols import HasFrequencyRatio
from ..exc import IncompatibleNotations
from ..exc import InvalidPitchIndex
from .constants import FREQ_EQUALITY_EPSILON


@total_ordering
class NoteABC(ABC):
    """
    Abstract base class for notes. Implements the properties
    :attr:`tuning`, :attr:`frequency` and :attr:`pitch_index`
    as well as the equality and lesser-than relation based on
    the :attr:`frequency` property.

    Subclasses must implement the :attr:`pitch` property, the
    :attr:`is_notated_same` method and the :meth:`transpose`
    method.

    :param notation: The notation object this note belongs to
    """

    def __init__(self, notation):
        self._notation = notation

    @property
    def notation(self):
        """
        The notation associated with this note
        """
        return self._notation

    @property
    def tuning(self):
        """
        The tuning associated with this note
        """
        return self.notation.tuning

    def interval(self, other: Self) -> NoteIntervalABC[Self]:
        """
        Returns an interval between this note and
        another note of the same notation.

        :param other: The other note (can be higher
            or lower than this note)
        """
        return self.notation.note_interval(
            self, other
        )

    def __eq__(self, other) -> bool:
        if not isinstance(other, HasFrequency):
            return False
        return abs(
            self.frequency - other.frequency
        ) < FREQ_EQUALITY_EPSILON

    def __lt__(self, other: HasFrequency) -> bool:
        return self.frequency < other.frequency

    @property
    def frequency(self) -> Frequency:
        """
        The frequency of this note
        """
        return self.pitch.frequency

    @property
    def pitch_index(self) -> int:
        """
        The pitch index of the underlying pitch
        """
        return self.pitch.pitch_index

    @property
    @abstractmethod
    def pitch(self):
        """
        (Must be implemented by subclasses)
        Returns the underlying pitch object
        """

    @abstractmethod
    def transpose(self, interval) -> Self:
        """
        (Must be implemented by subclasses)
        Transposes the note to a different one

        :param interval: A note interval 
        """

    @abstractmethod
    def is_notated_same(self, other) -> bool:
        """
        (Must be implemented by subclasses)
        Returns True, if this note is notated the same
        way as the other, False otherwise

        :param other: Another note of the same
            notation or class
        """


class PeriodicNoteABC(NoteABC):
    """
    Abstract base class for periodic notes. Implements
    proxy properties :attr:`pc_index` and :attr:`bi_index`
    that refer to the underlying periodic pitch object.

    Subclasses need to implement the :meth:`transpose_bi_index`
    method (in addition to the abstract properties and methods
    of NoteABC)
    """

    @property
    def pc_index(self) -> int:
        """
        The pitch class index of this note
        """
        return self.pitch.pc_index

    @property
    def bi_index(self) -> int:
        """
        The base interval index of this note
        """
        return self.pitch.bi_index

    def is_equivalent(self, other: PeriodicPitchLike) -> bool:
        """
        Returns True if this note has the same frequency as the
        other object when normalized to the first base interval

        :param other: Another periodic pitch or note
        """

        n_self = self.get_bi_normalized()
        n_other = other.get_bi_normalized()

        return n_self == n_other

    @abstractmethod
    def is_notated_equivalent(self, other) -> bool:
        """
        (Must be implemented by subclasses)
        Returns True, if this note is notated the same
        way as the other in regards to its pitch class
        symbol

        :param other: Another note
        """

    @abstractmethod
    def transpose_bi_index(self, bi_diff: int) -> Self:
        """
        Returns a note with the same pitch class index
        and symbol, but with a transposed base interval

        :param bi_diff: The difference in base interval
            between this note and the resulting one
        """

    def get_bi_normalized(self) -> Self:
        """
        Returns the equivalent of this note in the first
        base interval
        """
        return self.transpose_bi_index(
            -self.bi_index
        )

    def get_generator_index(self, generator_note: Self):
        """
        Calculates the number of steps needed to reach this note
        when iteratively adding the pitch of the given generator
        note to the zero pitch of this tuning

        :param generator_note: A generator note. Will be normalized
            to the equivalent note in the first base interval if its
            pitch index exceeds the period length of the tuning.

        :raises IncompatibleNotations: If notes come
            from a different notation system

        :raises InvalidGenerator: If pitch of given generator note is
            not in fact a generator in the underlying tuning
        """

        if generator_note.notation != self.notation:
            raise IncompatibleNotations(
                'Generator notes must come from the same notation'
            )

        return self.pitch.get_generator_index(
            generator_note.pitch
        )


class NatAccNote(PeriodicNoteABC):
    """
    A base class for notes which are constructed from a natural and
    an accidental (the appropriate base class for notes of notations
    subclassing from :class:`~xenharmlib.core.notation.NatAccNotation`)

    :param notation: The notation object this note belongs to
    :param natc_index: The natural class index of this note, which is
        the equivalency class index of the natural index of this note
        (so for example in a notation with naturals C, D, E, F, G, A, B
        the natc_index for C#-0 and Cb-2 is 0, while the natc_index for
        F-2 and F#-4 is 3)
    :param nat_bi_index: The base interval index of the natural of this
        note (e.g. for C#-0 this will be 0, for A#-2 it will be 2, etc)
    :param acc_value: The deviations (positive or negative) in steps
        that was introduced through an accidental (for example in
        12-EDO the accidental value of C#-0 is 1, Eb-2 is -1)
    :param natc_symbol: The chosen symbol for the natural class 
        (e.g. 'C' for C#)
    :param acc_symbol: The chosen symbol for the accidental
        (e.g. '#' for C#)
    """

    def __init__(self,
                 notation,
                 natc_index: int,
                 nat_bi_index: int,
                 acc_value: int,
                 natc_symbol: str,
                 acc_symbol: str):

        super().__init__(notation)
        self._natc_index = natc_index
        self._nat_bi_index = nat_bi_index
        self._acc_value = acc_value
        self._natc_symbol = natc_symbol
        self._acc_symbol = acc_symbol

    @property
    def pitch(self) -> PeriodicPitch:
        """
        Returns the underlying pitch object
        """
        tuning = self._notation.tuning
        pitch_index = (
            self.nat_pc_index + len(tuning) * self.nat_bi_index
        ) + self.acc_value
        return tuning.pitch(pitch_index)

    def transpose_bi_index(self, bi_diff: int) -> Self:
        """
        Returns a note with the same pitch class index
        and symbol, but with a transposed base interval

        :param bi_diff: The difference in base interval
            between this note and the resulting one
        """

        nat_bi_index = self.nat_bi_index + bi_diff
        return self.notation.note(
            self.pc_symbol, nat_bi_index
        )

    def is_notated_same(self, other) -> bool:
        """
        Returns True, if this note is notated the same
        way as the other, False otherwise

        :param other: Another note to compare
        """

        if isinstance(other, NatAccNote):
            return (self.pc_symbol == other.pc_symbol) and \
                (self.nat_bi_index == other.nat_bi_index)

        return False

    def is_notated_equivalent(self, other) -> bool:
        """
        Returns True, if this note is notated the same
        way as the other, False otherwise

        :param other: Another note to compare
        """

        if isinstance(other, NatAccNote):
            return self.pc_symbol == other.pc_symbol

        return False

    # methods pertaining to the split in natural and
    # accidental part

    @property
    def natc_index(self) -> int:
        """
        Returns the natural class index of this note.
        The natural class index is the equivalency class
        of the natural index, so for example in a notation
        with naturals C, D, E, F, G, A, B the notes C#-3
        and Cb-0 both have natural class index 0 while F#-2
        and Fbb-5 have natural class index 3
        """
        return self._natc_index

    @property
    def nat_index(self) -> int:
        """
        Returns the natural index of this note. The natural
        index is the number of steps needed to reach the
        natural part of this note, so for example in a
        notation with naturals C, D, E, F, G, A, B the
        natural index of C#-0 is 0, D-1 is 8, Eb-3 is 16
        """
        return self.natc_index + (
            self.nat_bi_index * self.notation.nat_count
        )

    @property
    def nat_bi_index(self) -> int:
        """ The base interval index of the natural of this note """
        return self._nat_bi_index

    @property
    def acc_value(self) -> int:
        """
        The accidental value of this note
        (e.g. in 31edo 2 for #, -2 for b, 0 for natural)
        """
        return self._acc_value

    # methods for mapping the natural index into
    # a pitch index or pitch class index

    @property
    def nat_pc_index(self) -> int:
        """ The pitch class index of the natural of this note """
        return self._notation.nat_index_to_pitch_index(self.natc_index)

    @property
    def nat_pitch_index(self) -> int:
        """ The pitch index of the natural of this note """
        return self._notation.nat_index_to_pitch_index(
            self.nat_index
        )

    # symbols / symbol fragments of the note

    @property
    def natc_symbol(self) -> str:
        """ The symbol for the natural of this note """
        return self._natc_symbol

    @property
    def acc_symbol(self) -> str:
        """ The symbol for the accidental of this note """
        return self._acc_symbol

    @property
    def pc_symbol(self) -> str:
        """ The combined symbol (natural + accidental) of this note """
        return self.natc_symbol + self.acc_symbol

    @property
    def acc_direction(self) -> int:
        """
        The accidental direction of this note (0 if the note
        is a natural, 1 if the note is a sharp note, -1 if
        it is a flat note)
        """
        if self._acc_value == 0:
            return 0
        return self._acc_value // abs(self._acc_value)

    @property
    def is_notated_natural(self) -> bool:
        """
        Returns True if this note is notated(!) as a natural,
        False otherwise (e.g. the note E# refers to a natural,
        however it is notated with an accidental, thus the
        property will be False here)
        """
        return self._acc_value == 0

    @property
    def is_enharmonic_natural(self) -> bool:
        """
        Returns True if note refers to a pitch class
        that is a natural
        """
        return self.notation.is_natural(
            self.nat_pc_index + self._acc_value
        )

    def __repr__(self):
        return (
            f'{self.__class__.__name__}('
            f'{self.pc_symbol}, '
            f'{self.nat_bi_index}, '
            f'{self._notation.tuning.name})'
        )

    def transpose(self, interval: NatAccNoteInterval) -> NatAccNote:
        """
        Transposes the note to another one by a natural/accidental
        note interval.

        :param interval: A natural/accidental note interval object
        """

        nat_diff = interval.nat_diff
        nat_count = self.notation.nat_count

        target_nat_index = self.nat_index + nat_diff

        source_nat_pitch_index = self.notation.nat_index_to_pitch_index(
            self.nat_index
        )
        target_nat_pitch_index = self.notation.nat_index_to_pitch_index(
            target_nat_index
        )

        target_nat_pitch_diff = (
            target_nat_pitch_index - source_nat_pitch_index
        )

        # the target accidental can be calculated as follows:
        # let N_0 be the pitch diff norm for the natural difference
        # (e.g. in 12-EDO 7 for 4 ^= P5). We now calculate the
        # actual pitch difference N between the two naturals, for
        # example 6 for B-F and receive the numbers of accidentals
        # (N_0 - N) needed to reach the norm (in case of B-F, F
        # needs to become F# so the interval is a P5). In a second
        # step we get the actual pitch difference D denoted by the
        # interval and substract the norm from it so we get the
        # number of 'extra accidentals' that deviate from the
        # norm. at the end we also need to add the accidental
        # deviation D_0 of the source note, so for example an A5
        # of Bb becomes F#. The full formula is:

        # (N_0 - N) + (D - N_0) + D_0
        
        # which is:
        # (D - N) + D_0

        target_acc = (
            interval.pitch_diff - target_nat_pitch_diff + self.acc_value
        )

        target_natc_index = target_nat_index % nat_count
        target_nat_bi_index = target_nat_index // nat_count

        target_natc_symbol = self.notation.get_natc_symbol(target_natc_index)
        target_acc_symbol = self.notation.get_acc_symbol(target_acc)

        return self.__class__(
            self.notation,
            target_natc_index,
            target_nat_bi_index,
            target_acc,
            target_natc_symbol,
            target_acc_symbol
        )

NoteT = TypeVar('NoteT', bound=NoteABC)

@total_ordering
class NoteIntervalABC(Generic[NoteT], ABC):
    """
    Abstract base class for note intervals. Implements the
    properties :attr:`pitch_interval`, :attr:`frequency_ratio`,
    :attr:`cents`, :attr:`pitch_diff` as well as equality and
    lesser-than relations based on frequency ratio.

    Note intervals are implemented as generic types with the
    inner type being a note class.

    Subclasses must at least implement the :meth:`from_notes`
    class method.

    :param notation: The notation this interval refers to
    :param ref_note: A reference note (needed for non-equal
        step tunings)
    :param pitch_diff: The difference in pitch that this
        interval represents
    """

    def __init__(self,
                 notation,
                 ref_note: NoteT,
                 pitch_diff: int):

        self._notation = notation
        self._ref_note = ref_note
        self._pitch_diff = pitch_diff

    # abstract methods

    @classmethod
    @abstractmethod
    def from_notes(cls, note_a: NoteT, note_b: NoteT) -> Self:
        """
        Constructs an interval from two notes
        """

    def __abs__(self) -> Self:
        """
        Returns the absolute of this note interval. On downwards
        interval it returns an upwards interval of the same absolute
        size. On upwards intervals it acts as the identity function.
        """

        if self.pitch_diff >= 0:
            return self

        target_note = self.ref_note.transpose(self)
        return self.notation.note_interval(
            target_note,
            self.ref_note
        )

    # read-only properties

    @property
    def notation(self):
        """
        The notation associated with this note interval
        """
        return self._notation

    @property
    def tuning(self):
        """
        The tuning associated with this note interval
        """
        return self.notation.tuning

    @property
    def ref_note(self) -> NoteT:
        """
        A reference note for the interval. (This is important
        for tunings that are not equal step where the same
        pitch difference does not imply the same frequency
        ratio)
        """
        return self._ref_note

    @property
    def pitch_diff(self) -> int:
        """
        The size of the interval in pitch steps from one
        note to the other
        """
        return self._pitch_diff

    # methods necessary for total ordering

    def __eq__(self, other) -> bool:
        if not isinstance(other, HasFrequencyRatio):
            return False
        return abs(
            self.frequency_ratio - other.frequency_ratio
        ) < FREQ_EQUALITY_EPSILON

    def __lt__(self, other: HasFrequencyRatio) -> bool:
        return self.frequency_ratio < other.frequency_ratio

    # pitch interval calculation and proxy properties

    @property
    def pitch_interval(self):
        """
        Returns the pitch interval equivalent to this
        note interval
        """
        note_a = self.ref_note
        note_b = note_a.transpose(self)
        tuning = self.notation.tuning
        return tuning.pitch_interval(
            note_a.pitch,
            note_b.pitch
        )

    @property
    def frequency_ratio(self) -> Frequency:
        """
        The frequency ratio of this note interval
        """
        return self.pitch_interval.frequency_ratio

    @property
    def cents(self) -> float:
        """
        The frequency ratio of this note interval
        measured in cents
        """
        return self.pitch_interval.cents


class PeriodicNoteInterval(NoteIntervalABC[NoteT]):
    """
    Abstract base class for intervals refering to notations
    of periodic tunings.
    
    Implements the method :meth:`get_generator_distance`
    """

    def get_generator_distance(
        self,
        generator_note: NoteT
    ) -> int:
        """
        Calculates the minimum number of steps needed to reach
        the one note from the other when iteratively adding a
        generator note.

        A typical application in 12EDO is to calculate the minimum
        distance of the two notes on the circle of fifths, hence
        the generator distance can be a good measure for consonance
        of an interval given the right generator note.

        :param generator_note: A generator note. Will be normalized
            to the equivalent pitch in the first base interval if its
            pitch index exceeds the period length of the tuning.

        :raises InvalidGenerator: If the note is not a generator
            in the tuning attached to this interval's notation
        """

        if generator_note.notation != self.notation:
            raise IncompatibleNotations(
                'Notes must come from the same '
                'notation instance'
            )

        generator_pitch = generator_note.pitch
        return self.pitch_interval.get_generator_distance(
            generator_pitch
        )

class NatAccNoteInterval(PeriodicNoteInterval[NatAccNote]):
    """
    Note interval class for intervals with natural/accidental notes.
    The class assumes that the interval is value-representable by
    the difference in natural indices and the difference in pitch.
    It is meant as a solid basis for interval notations that are
    similar to the traditional western interval notation having
    a interval symbol (like 'M') and an interval number (like 2)

    The concrete way an interval symbol and number are chosen is
    dependend on the underlying notation from which a symbol and
    a number is received in the :meth:`from_notes` builder method.

    :param notation: The notation this interval refers to
    :param ref_note: A reference note (needed for non-equal
        step tunings)
    :param pitch_diff: The difference in pitch that this
        interval represents
    :param nat_diff: The difference of the natural indices
        of the two notes defining the interval
    :param symbol: An interval symbol (like 'M', 'd', 'P')
    :param number: An interval number
    """

    def __init__(self,
                 notation,
                 ref_note: NatAccNote,
                 pitch_diff: int,
                 nat_diff: int,
                 symbol: str,
                 number: int):

        super().__init__(
            notation,
            ref_note,
            pitch_diff
        )

        self._nat_diff = nat_diff
        self._symbol = symbol
        self._number = number

    @property
    def nat_diff(self) -> int:
        """
        The difference of the natural indices of the
        two notes forming the interval
        """
        return self._nat_diff

    @property
    def symbol(self) -> str:
        """
        A symbol classifying this interval in regards
        to size and quality
        """
        return self._symbol

    @property
    def number(self) -> int:
        """
        A number signifying the size of the interval
        (closely related to the :attr:`nat_diff`
        property but traditionally implemented as
        1-based index)
        """
        return self._number

    @classmethod
    def from_notes(cls, note_a: NatAccNote, note_b: NatAccNote) -> Self:
        """
        Creates a note interval from two notes

        :raises IncompatibleNotations: If notes belong to different
            notations

        :param note_a: The source note
        :param note_b: The target note
        """

        if note_a.notation != note_b.notation:
            raise IncompatibleNotations(
                'Notes do not originate from the same notation'
            )

        notation = note_a.notation
        nat_diff = note_b.nat_index - note_a.nat_index
        pitch_diff = note_b.pitch_index - note_a.pitch_index

        symbol = notation.get_interval_symbol(
            nat_diff, pitch_diff
        )
        number = notation.nat_diff_to_interval_number(
            nat_diff
        )

        return cls(
            notation,
            note_a,
            pitch_diff,
            nat_diff,
            symbol,
            number
        )

    def __repr__(self) -> str:
        return (
            f'{self.__class__.__name__}('
            f'{self.shorthand_name}'
            f'{self.notation.tuning.name})'
        )

    @property
    def shorthand_name(self) -> Tuple[str, int]:
        """
        A tuple consisting of the interval symbol
        and the interval number
        """
        return (self.symbol, self.number)