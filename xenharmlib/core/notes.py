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
of notes and note intervals. Notes and note intervals wrap the
integer-based pitch and pitch interval classes.
"""

from __future__ import annotations

from typing import Tuple
from typing import Self
from typing import TypeVar
from warnings import warn
from functools import total_ordering
from abc import ABC
from abc import abstractmethod
import numpy as np
from .protocols import PeriodicPitchLike
from .freq_repr import SDFreqRepr
from .interval import SDInterval
from .pitch import PeriodicPitch
from ..exc import IncompatibleOriginContexts


@total_ordering
class NoteABC(SDFreqRepr):
    """
    Abstract base class for notes. Implements the properties
    :attr:`tuning`, :attr:`frequency` and :attr:`pitch_index`
    as well as the equality and lesser-than relation based on
    the :attr:`frequency` property.

    Subclasses must implement the :attr:`pitch` property, the
    :attr:`is_notated_same` method and the :meth:`transpose`
    method.

    :param notation: The notation object this note belongs to
    :param pitch_index: The pitch index of this note
    :param frequency: The frequency this note represents
    """

    def __init__(self, notation, frequency, pitch_index):
        super().__init__(notation, frequency, pitch_index)
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

    @property
    def enharm_strategy(self):
        """
        Proxy property for the enharmonic strategy of the notation
        """
        return self.notation.enharm_strategy

    @property
    @abstractmethod
    def pitch(self):
        """
        (Must be implemented by subclasses)
        Returns the underlying pitch object
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


class PeriodicNoteABC(NoteABC, PeriodicPitchLike):
    """
    Abstract base class for periodic notes. Implements
    proxy properties :attr:`pc_index` and :attr:`bi_index`
    that refer to the underlying periodic pitch object.

    Subclasses need to implement the :meth:`transpose_bi_index`
    method (in addition to the abstract properties and methods
    of NoteABC)
    """

    def __init__(self, notation, frequency, pitch_index):
        super().__init__(notation, frequency, pitch_index)
        self._pc_index = pitch_index % len(notation.tuning)
        self._bi_index = pitch_index // len(notation.tuning)

    @property
    def pc_index(self) -> int:
        """
        The pitch class index of this note
        """
        return self._pc_index

    @property
    def bi_index(self) -> int:
        """
        The base interval index of this note
        """
        return self._bi_index

    def is_equivalent(self, other: PeriodicPitchLike) -> bool:
        """
        Returns True if this note has the same frequency as the
        other object when normalized to the first base interval

        :param other: Another periodic pitch or note
        """

        if self.tuning is other.tuning:
            return self.pc_index == other.pc_index

        if self.tuning.eq_ratio == other.tuning.eq_ratio:
            bi_diff = self.bi_index - other.bi_index
            t_other = other.transpose_bi_index(bi_diff)
            return self == t_other

        raise IncompatibleOriginContexts(
            'Equivalency can only be tested for notes from tunings '
            'with the same equivalency interval'
        )

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

    def pcs_normalized(self) -> Self:
        """
        Returns the equivalent of this note in the first
        base interval
        """
        return self.transpose_bi_index(-self.bi_index)

    def get_generator_index(self, generator_note: Self):
        """
        Calculates the number of steps needed to reach this note
        when iteratively adding the pitch of the given generator
        note to the zero pitch of this tuning

        :param generator_note: A generator note. Will be normalized
            to the equivalent note in the first base interval if its
            pitch index exceeds the period length of the tuning.

        :raises IncompatibleOriginContexts: If notes come
            from a different notation system

        :raises InvalidGenerator: If the pitch of given generator note is
            not in fact a generator in the underlying tuning
        """

        if generator_note.notation is not self.notation:
            raise IncompatibleOriginContexts(
                'Generator notes must originate from the same notation'
            )

        return self.pitch.get_generator_index(generator_note.pitch)


class NatAccNote(PeriodicNoteABC):
    """
    A base class for notes that are constructed from a natural and
    accidentals (the appropriate base class for notes of notations
    subclassing from :class:`~xenharmlib.core.notation.NatAccNotation`)

    :param notation: The notation object this note belongs to
    :param frequency: The frequency this note represents
    :param pitch_index: The pitch index of this note
    :param nat_index: The natural index of this note, which is an index
        counting the naturals starting with 0 (e.g. in Western notation
        C0 ^= 0, D0 ^= 1, C1 ^=7, etc)
    :param acc_vector: A vector detailing the different deviations in
        steps that were introduced through accidentals
    :param pc_symbol: The chosen symbol for the pitch class
        (in most notations this is equal to natc_symbol + acc_symbol,
        however, there are notations - like UpDownNotation - that put
        some of the accidentals before the natural)
    :param natc_symbol: The chosen symbol for the natural class
        (e.g. 'C' for C#)
    :param acc_symbol: The chosen symbol for the accidental
        (e.g. '#' for C#)
    """

    def __init__(
        self,
        notation,
        frequency,
        pitch_index,
        nat_index: int,
        acc_vector: Tuple[int, ...],
        pc_symbol: str,
        natc_symbol: str,
        acc_symbol: str,
    ):

        super().__init__(notation, frequency, pitch_index)
        self._nat_index = nat_index
        self._natc_index = nat_index % notation.nat_count
        self._nat_bi_index = nat_index // notation.nat_count
        self._acc_vector = acc_vector
        self._pc_symbol = pc_symbol
        self._natc_symbol = natc_symbol
        self._acc_symbol = acc_symbol

    @property
    def pitch(self) -> PeriodicPitch:
        """
        Returns the underlying pitch object
        """
        tuning = self._notation.tuning
        pitch_index = (
            self.natc_pitch_index + len(tuning) * self.nat_bi_index
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
        return self.notation.note(self.pc_symbol, nat_bi_index)

    def is_notated_same(self, other) -> bool:
        """
        Returns True, if this note is notated the same
        way as the other, False otherwise

        :param other: Another note to compare
        """

        if other.notation is not self.notation:
            raise IncompatibleOriginContexts(
                'Notes must originate from the same notation context'
            )

        return (self.pc_symbol == other.pc_symbol) and (
            self.nat_bi_index == other.nat_bi_index
        )

    def is_notated_equivalent(self, other) -> bool:
        """
        Returns True, if this note is notated the same
        way as the other, False otherwise

        :param other: Another note to compare
        """

        if other.notation is not self.notation:
            raise IncompatibleOriginContexts(
                'Notes must originate from the same notation context'
            )

        return self.pc_symbol == other.pc_symbol

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
        return self._nat_index

    @property
    def nat_bi_index(self) -> int:
        """The base interval index of the natural of this note"""
        return self._nat_bi_index

    @property
    def acc_value(self) -> int:
        """
        The accidental value of this note
        (e.g. in 31edo 2 for #, -2 for b, 0 for natural)
        """
        return int(sum(self._acc_vector))

    @property
    def acc_vector(self) -> Tuple[int, ...]:
        """
        The accidental vector of this note
        """
        return self._acc_vector

    # methods for mapping the natural index into
    # a pitch index or pitch class index

    @property
    def nat_pc_index(self) -> int:
        """The pitch class index of the natural of this note"""
        return self._notation.nat_index_to_pc_index(self.natc_index)

    @property
    def nat_pitch_index(self) -> int:
        """The pitch index of the natural of this note"""
        return self._notation.nat_index_to_pitch_index(self.nat_index)

    @property
    def natc_pitch_index(self) -> int:
        """The pitch index of the natural class of this note"""
        return self._notation.nat_index_to_pitch_index(self.natc_index)

    # symbols / symbol fragments of the note

    @property
    def natc_symbol(self) -> str:
        """The symbol for the natural of this note"""
        return self._natc_symbol

    @property
    def acc_symbol(self) -> str:
        """The symbol for the accidental of this note"""
        return self._acc_symbol

    @property
    def pc_symbol(self) -> str:
        """The pitch class symbol of this note"""
        return self._pc_symbol

    @property
    def acc_direction(self) -> int:
        """
        The accidental direction of this note (0 if the note
        is a natural, 1 if the note is a sharp note, -1 if
        it is a flat note)
        """
        if self.acc_value == 0:
            return 0
        return self.acc_value // abs(self.acc_value)

    @property
    def is_notated_natural(self) -> bool:
        """
        Returns True if this note is notated(!) as a natural,
        False otherwise (e.g. the note E# refers to a natural,
        however, it is notated with an accidental, thus the
        property will be False here)
        """
        return self.acc_value == 0

    @property
    def is_enharmonic_natural(self) -> bool:
        """
        Returns True if note refers to a pitch class
        that is a natural
        """
        return self.notation.is_natural(self.nat_pc_index + self.acc_value)

    def __repr__(self):
        return (
            f'{self.__class__.__name__}('
            f'{self.pc_symbol}, '
            f'{self.nat_bi_index}, '
            f'{self._notation.tuning.name})'
        )

    @property
    def short_repr(self):
        """
        A shortened representation of this note
        """
        return f'{self.pc_symbol}{self.nat_bi_index}'

    @property
    def pc_short_repr(self):
        """
        The pitch class symbol of this note
        """
        return f'{self.pc_symbol}'

    def acc_altered(self, acc_diff: Tuple[int, ...]):
        """
        Returns a note with altered accidentals from an accidental
        difference vector, so for example in UpDownNotation for a tuning
        with sharpness 2 altering ^C# by (2, -1) results in the note Cx

        :param acc_diff: The accidental difference vector
        """

        if len(self.acc_vector) != len(acc_diff):
            raise ValueError(
                "The accidental difference vector must have the same "
                "number of dimensions as the accidental vector of the "
                "note it is applied to"
            )

        acc_vector = tuple(np.add(self.acc_vector, acc_diff))
        return self.notation.note_by_numdef(self.nat_index, acc_vector)

    def transpose(self, diff: int | NatAccNoteInterval) -> NatAccNote:
        """
        Transposes the note to another one by a natural/accidental
        note interval.

        :param diff: A natural/accidental note interval object
            or an integer denoting the pitch difference
        """

        if isinstance(diff, int):
            return self.enharm_strategy.note_transpose(self, diff)

        # rename diff to interval so it is clear that
        # we have a proper interval definition
        interval = diff

        if interval.notation is not self.notation:
            raise IncompatibleOriginContexts(
                'Interval must originate from same notation '
                'as the note that should be transposed'
            )

        notation = self.notation
        nat_index = self.nat_index + interval.nat_diff
        nat_pitch_diff = notation.std_pitch_diff(interval.nat_diff)
        unbalanced_nat_pitch_index = self.nat_pitch_index + nat_pitch_diff
        unbalanced_acc_vector = tuple(
            np.add(self.acc_vector, interval.acc_vector)
        )

        notation = self.notation
        acc_vector = notation.balance_note_acc_vector(
            nat_index, unbalanced_nat_pitch_index, unbalanced_acc_vector
        )

        return self.notation.note_by_numdef(nat_index, acc_vector)


NoteT = TypeVar('NoteT', bound=NoteABC)


@total_ordering
class NoteIntervalABC(SDInterval[NoteT], ABC):
    """
    Abstract base class for note intervals. Implements the
    property :attr:`pitch_interval` that constructs the
    equivalent pitch interval

    Note intervals are implemented as generic types with the
    inner type being a note class.

    Subclasses must at least implement the :meth:`from_source_and_target`
    class method.

    :param notation: The notation this interval refers to
    :param frequency_ratio: A frequency ratio object
    :param pitch_diff: The difference in pitch that this
        interval represents
    :param ref_note: A reference note (needed for non-equal
        step tunings)
    """

    def __init__(
        self,
        notation,
        frequency_ratio,
        pitch_diff: int,
        ref_note: NoteT,
    ):
        super().__init__(notation, frequency_ratio, pitch_diff)
        self._notation = notation
        self._ref_note = ref_note

    def __abs__(self) -> Self:
        """
        Returns the absolute of this note interval. On downwards
        interval it returns an upwards interval of the same absolute
        size. On upwards intervals it acts as the identity function.
        """

        if self.pitch_diff >= 0:
            return self

        target_note = self.ref_note.transpose(self)
        return self.notation.interval(target_note, self.ref_note)

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
        return tuning.interval(note_a.pitch, note_b.pitch)


class PeriodicNoteInterval(NoteIntervalABC[NoteT]):
    """
    Abstract base class for intervals referring to notations
    of periodic tunings.

    Implements the method :meth:`get_generator_distance`
    """

    def get_generator_distance(self, generator_note: NoteT) -> int:
        """
        Calculates the minimum number of steps needed to reach
        one note from the other when iteratively adding a
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

        if generator_note.notation is not self.notation:
            raise IncompatibleOriginContexts(
                'Notes must come from the same notation instance'
            )

        generator_pitch = generator_note.pitch
        return self.pitch_interval.get_generator_distance(generator_pitch)


class NatAccNoteInterval(PeriodicNoteInterval[NatAccNote]):
    """
    Note interval class for intervals with natural/accidental notes.
    The class assumes that the interval is value-representable by
    the difference in natural indices and an accidental vector
    signifying step alterations of different categories.
    It is meant as a solid basis for interval notations that are
    similar to the traditional Western interval notation having
    a interval symbol (like 'M') and an interval number (like 2)

    The concrete way an interval symbol and number are chosen is
    dependent on the underlying notation from which a symbol and
    a number are received in the :meth:`from_source_and_target`
    builder method.

    :param notation: The notation this interval refers to
    :param frequency_ratio: A frequency ratio object
    :param pitch_diff: The difference in pitch that this
        interval represents
    :param ref_note: A reference note (needed for non-equal
        step tunings)
    :param nat_diff: The difference of the natural indices
        of the two notes defining the interval
    :param acc_vector: A vector defining the alteration of
        the standard pitch index difference of a natural
        index difference
    :param symbol: An interval symbol (like 'M', 'd', 'P')
    :param number: An interval number
    """

    def __init__(
        self,
        notation,
        frequency_ratio,
        pitch_diff,
        ref_note: NatAccNote,
        nat_diff: int,
        acc_vector: Tuple[int, ...],
        symbol: str,
        number: int,
    ):

        super().__init__(notation, frequency_ratio, pitch_diff, ref_note)

        self._acc_vector = acc_vector
        self._nat_diff = nat_diff
        self._symbol = symbol
        self._number = number

    @property
    def acc_vector(self) -> Tuple[int, ...]:
        """
        The accidental vector of this interval (signifying the different
        pitch deviations from the standard natural pitch difference)
        """
        return self._acc_vector

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
        A symbol classifying this interval in regard
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
        .. deprecated:: 0.2.0
           Use :py:meth:`from_source_and_target` instead.

        Creates a note interval from two notes

        :raises IncompatibleOriginContexts: If notes belong to different
            notations

        :param note_a: The source note
        :param note_b: The target note
        """
        warn(
            f'{cls.__name__}.from_notes is deprecated and will be '
            f'removed in 1.0.0. Please use '
            f'{cls.__name__}.from_source_and_target instead.',
            DeprecationWarning,
            stacklevel=2,
        )
        return cls.from_source_and_target(note_a, note_b)

    @classmethod
    def from_source_and_target(
        cls, source: NatAccNote, target: NatAccNote
    ) -> Self:
        """
        Creates a note interval from two notes

        :raises IncompatibleOriginContexts: If notes belong to different
            notations

        :param source: The source note
        :param target: The target note
        """

        if source.notation is not target.notation:
            raise IncompatibleOriginContexts(
                'Notes do not originate from the same notation'
            )

        notation = source.notation
        nat_diff = target.nat_index - source.nat_index
        unbalanced_nat_pitch_diff = (
            target.nat_pitch_index - source.nat_pitch_index
        )
        unbalanced_acc_vector = tuple(
            np.subtract(target.acc_vector, source.acc_vector)
        )

        acc_vector = notation.balance_interval_acc(
            nat_diff, unbalanced_nat_pitch_diff, unbalanced_acc_vector
        )

        frequency_ratio = target.frequency / source.frequency
        pitch_diff = target.pitch_index - source.pitch_index

        symbol = notation.get_interval_symbol(nat_diff, acc_vector)
        number = notation.nat_diff_to_interval_number(nat_diff)

        return cls(
            notation,
            frequency_ratio,
            pitch_diff,
            source,
            nat_diff,
            acc_vector,
            symbol,
            number,
        )

    def __repr__(self) -> str:
        return (
            f'{self.__class__.__name__}('
            f'{self.symbol}, {self.number}, '
            f'{self.tuning.name})'
        )

    @property
    def short_repr(self) -> str:
        """
        A short representation string of the interval
        (to be shown in collections)
        """
        return f'{self.symbol}{self.number}'

    @property
    def shorthand_name(self) -> Tuple[str, int]:
        """
        A tuple consisting of the interval symbol
        and the interval number
        """
        return (self.symbol, self.number)
