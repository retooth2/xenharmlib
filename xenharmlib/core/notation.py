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
lower-level objects (pitch, pitch interval, pitch scale)
"""

import operator
from functools import reduce
from typing import Tuple
from typing import Dict
from typing import Optional
from typing import TypeVar
from typing import List
from warnings import warn
from abc import abstractmethod

from ..exc import UnknownNoteSymbol
from .notes import NoteABC
from .notes import NoteIntervalABC
from .notes import NatAccNote
from .notes import NatAccNoteInterval
from .note_interval_seq import NoteIntervalSeq
from .note_interval_seq import NatAccNoteIntervalSeq
from .note_scale import NoteScale
from .note_scale import NatAccNoteScale
from .symbols import SymbolCode
from .symbols import SymbolValueNotMapped
from .symbols import UnknownSymbolString
from .origin_context import OriginContext
from ..exc import IncompatibleOriginContexts
from ..exc import InvalidIntervalNumber
from ..exc import InvalidAccidentalValue
from ..exc import InvalidNaturalDiffClassIndex
from .protocols import Index
from .protocols import PeriodicIndex
from .symbols import AmbiguousSymbol
from .utils import scalar_op

NoteT = TypeVar('NoteT', bound=NoteABC)
IntervalT = TypeVar('IntervalT', bound=NoteIntervalABC)
ScaleT = TypeVar('ScaleT', bound=NoteScale)
IntervalSeqT = TypeVar('IntervalSeqT', bound=NoteIntervalSeq)
IndexT = TypeVar('IndexT', bound=Index)


class NotationABC(
    OriginContext[IndexT, NoteT, IntervalT, ScaleT, IntervalSeqT]
):
    """
    Abstract base class for all notations. A notation can be
    understood as a wrapper around the tuning, providing a
    string interface to the underlying integer system.

    Notations in the core package are defined as generics
    with three type variables: One for the note class,
    one for the interval class, and one for the scale class.

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

    def __init__(
        self,
        tuning,
        note_cls: type[NoteT],
        note_interval_cls: type[IntervalT],
        note_scale_cls: type[ScaleT],
        note_interval_seq_cls: type[IntervalSeqT]
    ):
        super().__init__(
            note_cls,
            note_interval_cls,
            note_scale_cls,
            note_interval_seq_cls
        )
        self._tuning = tuning
        self._enharm_strategy = None

    @property
    def tuning(self):
        """
        Returns the tuning this notation was built for
        """
        return self._tuning

    @property
    def enharm_strategy(self):
        """
        The enharmonic strategy of this notation. Enharmonic strategies
        define different ways to map pitch layer objects to notation layer
        objects.
        """
        if self._enharm_strategy is None:
            raise IncompleteNotation(
                'Notation did not define an enharmonic strategy. Without '
                'it the result of this operation is not well-defined'
            )
        return self._enharm_strategy

    @enharm_strategy.setter
    def enharm_strategy(self, enharm_strategy):
        self._enharm_strategy = enharm_strategy

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

    def guess_note(self, pitch) -> NoteT:
        """
        Guesses a note from a pitch using the preferred enharmonic
        strategy of this notation

        :pitch: A pitch object originating from the underlying tuning
        """

        if pitch.tuning is not self.tuning:
            raise IncompatibleOriginContexts(
                'Pitch must originate from the tuning that this '
                'notation is build upon'
            )

        return self.enharm_strategy.guess_note(self, pitch)

    def guess_note_interval(self, pitch_interval) -> NoteT:
        """
        Guesses a note interval from a pitch interval using the preferred
        enharmonic strategy of this notation

        :pitch_interval: A pitch interval object originating
            from the underlying tuning
        """

        if pitch_interval.tuning is not self.tuning:
            raise IncompatibleOriginContexts(
                'Pitch interval must originate from the tuning '
                'that this notation is build upon'
            )

        return self.enharm_strategy.guess_note_interval(self, pitch_interval)

    def guess_note_scale(self, pitch_scale) -> NoteT:
        """
        Guesses a note scale from a pitch scale using the preferred
        enharmonic strategy of this notation

        :pitch_scale: A pitch scale object originating
            from the underlying tuning
        """

        if pitch_scale.tuning is not self.tuning:
            raise IncompatibleOriginContexts(
                'Pitch scale must originate from the tuning '
                'that this notation is build upon'
            )

        return self.enharm_strategy.guess_note_scale(self, pitch_scale)


class IncompleteNotation(Exception):
    """
    Gets raised when a notation is not initialized correctly
    """


# We will give a formal definition of a natural/accidental notation in here.
# We will first define the structure of notes and intervals, then define the
# transposition and interval determination operations.
#
# We first define two terms:
#
#   * A "pitch index" (subsequently denoted P) is any type of index that
#     denotes a specific frequency ratio. Typical pitch indices in sparse
#     tunings are integers (e.g. C0 = 0, C#0 = 1, etc), however a pitch
#     index can also be something else that implements the necessary
#     arithmetic protocol, e.g. a lattice point in a multi-dimensional
#     tuning
#
#   * An "accidental sum vector" (subsequently denoted 'A') is a vector that
#     counts value sums of different accidental sets. An accidental set
#     is a set of accidentals (e.g. {#, b, x}) where each element has
#     a specific value (e.g. # = 1, b = -1, x = 2) and opposite values
#     cancel each other out. In the standard western notation there
#     exists only one accidental set, so the note Cbb corresponds
#     to vector (-2,), C# to (1,), Cxx# to (5,) and both C and Cb# to
#     (0,). UpDownNotation on the other hand has two different accidental
#     sets, the aforementioned flat/sharp set and the independent up/down
#     set ({v, ^}). A note ^Cbb in UpDownNotation has for example the
#     corresponding vector A = (-2, 1) meaning "two flats, 1 up"
#
# A natural accidental notation is a structure (p, q, w, h) with the
# following definition of its elements:
#
#   * p(n): Z -> P
#     This function returns the equivalent pitch index for a natural index.
#     A natural index is a whole number indicating the index of the natural
#     part of a note. For example in Western notation C0 has natural index
#     0, D0 natural index 1, C1 has natural index 7, B(-1) has natural
#     index -1, A(-1) and A#(-1) have natural index -2.
#
#   * q(m): Z -> P
#     This function returns the equivalent pitch diff for a natural diff.
#     A natural diff is a whole number indicating the diff of the natural
#     part of an interval. For example in Western notation M3 has natural
#     diff 2, P1 natural diff 0, P5 has natural diff 4, P(-5) has natural
#     diff -4, P(-4) has natural diff -3, etc.
#     For reasons we will explain later it is defined as follows:
#         p(m)    for positive m
#       - p(|m|)  for negative m
#
#   * w(A): Z^n -> P^n
#     A linear weighting function that multiplies an accidental sum
#     vector component-wise with a fixed weight vector, more formally
#     for a fixed weight vector (w_1, w_2, ..., w_n) in P^n the function
#     w(A) is defined as w(A) = (w_1 * a_1, w_2 * a_2, ...w_n * a_n).
#     The resulting vector is called "accidental diff vector"
#
#   * h(p): P -> Z^n
#     A balancing function returning an accidental vector for a specific
#     pitch index deviation (more on that later)
#
# Notes in natural accidental notations are defined as a structure (n, A)
# with n being the natural index and A being the accidental sum vector.
#
# Let's give some simple examples for the UpDownNotation system that
# has two accidental sets: sharp/flats and ups/downs:
#
#   C0      ^=  (0, (0, 0))
#   C#0     ^=  (0, (1, 0))
#   vD0     ^=  (1, (0, -1))
#   ^^Gb0   ^=  (4, (-1, 2))
#   C(-1)x  ^=  (-7, (2, 0))
#
# The (n, A) structure can be understood as: from C0 go n naturals up (n > 0)
# or down (n < 0) and then alter the result according to accidentals in A.
#
# We define the total pitch index of a note (n, A) as:
#
#       total((n, A)) := p(n) + sum(w(A))
#
# (the pitch index of the natural + the weighted pitch alterations of
# all sets of accidentals)

# In an analogue fashion we can also define intervals I = (m, A) with m
# being the difference(!) in natural index and A being the difference in
# accidentals.
#
# Please note that the (m, A) structure CAN NOT in general be understood
# as "move m naturals and alter with A". The problem with intervals
# in natural/accidental notations is that naturals are not uniformly
# distributed, meaning that the (m, A) structure is dependent on an
# implicit starting point. If we e.g. want to define a minor second
# we will notice that starting from E0 it is "one natural up", while
# starting from D0 it is "one natural up, 1 pitch down". Same goes
# for interval direction: On C0 a minor second upwards would mean
# "1 natural up, 1 pitch down". The downward minor second from C0
# would however be "1 natural down"
#
# Following the path it is defined in common interval naming systems
# we implicitely assume that an interval starts at the natural that
# is also the zero element (C0) and points upwards, so for example
# in the UpDownNotation system we have the following equivalencies:
#
#   P1 (unison)                     ^=   (0, (0, 0))
#   M2 (major second)               ^=   (1, (0, 0))
#   A3 (augmented third)            ^=   (2, (1, 0))
#   P5 (perfect fifth)              ^=   (4, (0, 0))
#   ^dim5 (up-diminished fifth)     ^=   (4, (-1, 1))
#   M(-2) (inverted major second)   ^=   (-1, (0, 0))
#
# This "implicit upward semantics" is the reason of why the q function
# aligns with p on positive natural diffs, but is "flipped" on negative
# natural diffs.
#
# The total pitch difference of an interval (m, A) is consequently defined
# as:
#
#       total_diff((m, A)) := q(m) + sum(w(A))

# Without knowing about the aforementioned problem of non-uniformity we
# could naively assume that transposition would mean to just add the natural
# index diff to the natural index and add the two accidental vectors together.
# However this would give us an incorrect result.
#
# As example: If we want to transpose B0 in a Western notation by a perfect
# fifth the correct result IS NOT (6 + 4, (0,) + (0,)) = F1, but F#1. We
# need to "balance" the result first.
#
# The question for transposition is: Find A' so that
#
#     total((n + m, A1 + A2 + A') = total((n, A1)) + total_diff((m, A2))
#
# We fill in the definition:
#
#     p(n + m) + sum(w(A1)) + sum(w(A2)) + sum(w(A')) =
#     p(n) + sum(w(A1)) + q(m) + sum(w(A2))
#
# And simplify:
#
#     p(n + m) + sum(w(A')) = p(n) + q(m)
#     sum(w(A')) = p(n) + q(m) - p(n + m)
#
# So every natural/accidental notation needs to define a function
# h(p): P -> Z^n that receives the right side of this equation
# and returns a suitable A' vector satisfying the equation.
#
# Transposition T: Notes x Intervals -> Notes is therefore defined as:
#
#     T((n, A1), (m, A2)) := (n + m, A1 + A2 + h(p(n) + q(m) - p(n + m)))
#
# For interval determination between two notes (n1, A1) and (n2, A2) we
# need to find a A' such that
#
#     total_diff((n2 - n1, A2 - A1 + A') = total((n2, A2)) - total((n1, A_1))
#
# We fill in the definition
#
#     q(n2 - n1) + sum(w(A2)) - sum(w(A1)) + sum(w(A')) =
#     p(n2) + sum(w(A2)) - p(n1) - sum(w(A1))
#
# And simplify:
#
#     q(n2 - n1) + sum(w(A')) = p(n2) - p(n1)
#     sum(w(A')) = p(n2) - p(n1) - q(n2 - n1)
#
# Interval determination I: Notes x Notes -> Interval is therefore defined as:
#
#     I((n1, A1), (n2, A2)) :=
#           (n2 - n1, A2 - A1 + h(p(n2) - p(n1) - q(n2 - n1)))
#
# As for the definition of h: For typical sharp/flat accidental systems we
# would just balance with flats or sharps. However depending on notation it
# is possible that other strategies must be applied.

PeriodicIndexT = TypeVar('PeriodicIndexT', bound=PeriodicIndex)


class NatAccNotation(
    NotationABC[
        PeriodicIndexT,
        NatAccNote,
        NatAccNoteInterval,
        NatAccNoteScale,
        NatAccNoteIntervalSeq
    ]
):
    """
    NatAccNotation is a notation for periodic tunings that select a
    subset of pitches called naturals to form a basic symbol set (typically
    letters) and adds special symbols called accidentals, which signify
    step deviations from the natural pitch classes.

    The standard Western notation for example is a such a notation,
    defining 7 naturals (C, D, E, G, A, B) and 2 accidentals (#, b)
    that signify a step deviation of +1 and -1 respectively.

    The class supports different 'categories' of accidentals that do not
    interact with one another, for example, a category for sharps/flats
    and one category for ups/downs. Consequently, accidental values are
    given in the form of a vector.

    It assumes that intervals are uniquely defined by their
    difference in natural index + the difference of the accidental
    vectors of their source notes. It further assumes that intervals
    are notated as a tuple (symbol, number). The class implements
    the 1-based ordinal notation for numbers by default (e.g. the
    number 1 for a unison, the number 2 for a second, etc), however
    this behavior get be changed by subclassing and overwriting
    the method :meth:`nat_diff_to_interval_number` and its
    counterpart :meth:`interval_number_to_nat_diff`

    :param tuning: The tuning this notation refers to
    :param acc_weight: A vector defining a mapping between the
        (unweighted) accidental sum vector and the (weighted)
        accidental diff vector
    :param note_cls: Note class used in the :meth:`note` builder
        method (optional, defaults to the class NatAccNote)
    :param note_interval_cls: Note interval class used in the
        :meth:`note_interval` builder method (optional, defaults
        to the class NatAccNoteInterval)
    :param note_scale_cls: Note scale class used in the
        :meth:`note_scale` builder method (optional, defaults
        to the class NatAccNoteScale)
    """

    def __init__(
        self,
        tuning,
        acc_weights: Tuple[PeriodicIndexT, ...],
        note_cls: type[NatAccNote] = NatAccNote,
        note_interval_cls: type[NatAccNoteInterval] = NatAccNoteInterval,
        note_scale_cls: type[NatAccNoteScale] = NatAccNoteScale,
        note_interval_seq_cls: type[NatAccNoteIntervalSeq] = NatAccNoteIntervalSeq,
    ):

        super().__init__(
            tuning,
            note_cls,
            note_interval_cls,
            note_scale_cls,
            note_interval_seq_cls
        )

        self._acc_weights = acc_weights

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

        self._naturals: List[Tuple[str, PeriodicIndexT]] = []

        self._acc_symbol_code: Optional[SymbolCode] = None
        self._interval_symbol_codes: Dict[int, SymbolCode] = {}

    @property
    def acc_weights(self) -> Tuple[PeriodicIndexT, ...]:
        """
        The weight vector that transforms the accidental sum vector
        into the accidental diff vector
        """
        return self._acc_weights

    @property
    def zero_element(self) -> NatAccNote:
        """
        The 'standard note' with pitch_index 0
        """

        natc_symbol = self._naturals[0][0]
        note = self.note(natc_symbol, 0)

        if note.pitch_index != 0:
            raise IncompleteNotation(
                'First defined natural did not point to pitch index 0.'
                'Please overwrite the zero_element property to return '
                'a correct result'
            )

        return note

    # we define the function w(A) from the definition and (for
    # implementation detail reasons) also the inverse function

    def acc_sum_vector_to_acc_diff_vector(
        self, acc_sum_vector: Tuple[int, ...]
    ) -> Tuple[PeriodicIndexT, ...]:
        """
        Transforms an (unweighted) accidental sum vector into a
        (weighted) accidental diff vector.

        :raises ValueError: If dimensions of accidental sum vector
            do not match the weighting vector dimensions of this
            notation

        :param acc_sum_vector: The accidental sum vector
        """

        dimensions = len(self.acc_weights)

        if len(acc_sum_vector) != dimensions:
            raise ValueError(
                f'accidental sum vector does not have the '
                f'correct dimensions (should be {dimensions})'
            )

        result: Tuple[PeriodicIndexT, ...] = tuple()

        for i, component in enumerate(acc_sum_vector):
            result += (component * self.acc_weights[i],)

        return result

    def acc_diff_vector_to_acc_sum_vector(
        self, acc_diff_vector: Tuple[PeriodicIndexT, ...]
    ) -> Tuple[int, ...]:
        """
        Transforms a (weighted) accidental diff vector into a
        (unweighted) accidental sum vector.

        :raises ValueError: If dimensions of accidental diff vector
            do not match the weighting vector dimensions of this
            notation

        :raises ValueError: If accidental diff vector is not in
            the image of the accidental weight mapping of this
            notation

        :param acc_diff_vector: The accidental diff vector
        """

        dimensions = len(self.acc_weights)

        if len(acc_diff_vector) != dimensions:
            raise ValueError(
                f'accidental diff vector does not have the '
                f'correct dimensions (should be {dimensions})'
            )

        result: Tuple[int, ...] = tuple()

        for i, component in enumerate(acc_diff_vector):
            q, r = divmod(component, self.acc_weights[i])
            if r != 0:
                raise ValueError(
                    'accidental diff vector is not in the image '
                    'of the accidental weight mapping'
                )
            result += (q,)

        return result

    # we define the h(p) function from the definition

    def get_acc_sum_balance_vector(
        self, delta: PeriodicIndexT
    ) -> Tuple[int, ...]:
        """
        Returns an accidental sum balance vector for a pitch difference
        delta. By default this function assumes that pitch difference
        deltas introduced on transposition or interval determination
        can be counter-balanced by changing the first dimension of
        the accidental sum vector (e.g. B0 + P5 = F#1). If your
        subclassed notation does this differently you need to
        change this behavior by overwriting the method in
        your class.

        :param delta: The delta in pitch difference
        """

        q, r = divmod(delta, self.acc_weights[0])

        if r != self.zero_index:
            raise ValueError(
                f'heuristic for balancing accidental sum vector failed: '
                f'pitch deviation {delta} can not be represented by '
                f'the first accidental set. please replace the '
                f'get_acc_sum_balance_vector method with a suitable '
                f'strategy in your notation subclass'
            )

        return (q,) + (0,) * (len(self.acc_weights) - 1)

    # we define the p(n) function from the definition

    def nat_index_to_pitch_index(self, nat_index: int) -> PeriodicIndexT:
        """
        Returns the pitch index a natural index refers to
        (e.g. in 12-EDO: 0 -> 0, 1 -> 2, 3 -> 4, 4 -> 5)

        :param nat_index: A natural index
        """

        nat_bi_index, natc_index = divmod(nat_index, self.nat_count)
        natc_pitch_index = self.natc_pitch_indices[natc_index]
        return natc_pitch_index + len(self.tuning) * nat_bi_index

    # we define the q(m) function from the definition

    def std_pitch_diff(self, nat_diff: int) -> PeriodicIndexT:
        """
        Returns the standardized pitch difference for a
        natural index difference (e.g. in 12-EDO: 0 -> 0,
        1 -> 2, 4 -> 7, (-1) -> (-2), (-4) -> (-7), etc)

        :param nat_diff: A natural index difference
        """

        abs_nat_bi_diff, abs_natc_diff = divmod(abs(nat_diff), self.nat_count)
        abs_natc_pitch_diff = self.natc_pitch_indices[abs_natc_diff]
        abs_pitch_diff = (
            abs_natc_pitch_diff + len(self.tuning) * abs_nat_bi_diff
        )

        if nat_diff >= 0:
            return abs_pitch_diff

        return (-1) * abs_pitch_diff

    # after having implemented the formally defined functions we now
    # implement builder and parsing methods and various properties.

    def note(self, pc_symbol: str, nat_bi_index: int) -> NatAccNote:
        """
        Creates a note in line with this notation

        :param pc_symbol: A symbol denoting the pitch class
            (typically something like 'C#', 'Ab', 'F', etc)
        :param nat_bi_index: The base interval index of the
            natural (for example a B#-0 in 12-EDO has the natural base
            interval index of 0, even though the pitch is in base
            interval 1)
        """

        natc_symbol, acc_symbol, natc_index, acc_sum_vector = self.parse_pc_symbol(
            pc_symbol
        )
        nat_index = natc_index + (nat_bi_index * self.nat_count)
        natc_pitch_index = self.nat_index_to_pitch_index(natc_index)
        acc_diff_vector = self.acc_sum_vector_to_acc_diff_vector(
            acc_sum_vector
        )
        acc_value = reduce(operator.add, acc_diff_vector)

        tuning = self.tuning
        pitch_index = (
            natc_pitch_index + len(tuning) * nat_bi_index
        ) + acc_value
        frequency = tuning.get_frequency_for_index(pitch_index)

        chosen_note = self._freq_repr_cls(
            self,
            frequency,
            pitch_index,
            nat_index=nat_index,
            acc_sum_vector=acc_sum_vector,
            acc_diff_vector=acc_diff_vector,
            pc_symbol=pc_symbol,
            natc_symbol=natc_symbol,
            acc_symbol=acc_symbol,
        )

        return chosen_note

    def note_by_numdef(
        self, nat_index: int, acc_sum_vector: Tuple[int, ...]
    ) -> NatAccNote:
        """
        Creates a natural/accidental note by its numerical definition.
        Autogenerates appropriate symbols

        :param nat_index: The natural index of the note
        :param acc_sum_vector: The (unweighted) accidental sum vector
            of the note
        """

        acc_diff_vector = self.acc_sum_vector_to_acc_diff_vector(
            acc_sum_vector
        )
        acc_value = reduce(operator.add, acc_diff_vector)
        nat_pitch_index = self.nat_index_to_pitch_index(nat_index)
        pitch_index = nat_pitch_index + acc_value
        frequency = self.tuning.get_frequency_for_index(pitch_index)
        result = self.gen_pc_symbol(nat_index, acc_sum_vector)

        pc_symbol = result[0]
        natc_symbol = result[1]
        acc_symbol = result[2]

        chosen_note = self._freq_repr_cls(
            self,
            frequency,
            pitch_index,
            nat_index,
            acc_sum_vector,
            acc_diff_vector,
            pc_symbol,
            natc_symbol,
            acc_symbol,
        )

        return chosen_note

    def note_interval(
        self, note_a: NatAccNote, note_b: NatAccNote
    ) -> NatAccNoteInterval:
        """
        .. deprecated:: 0.2.0
           Use :py:meth:`interval` instead.

        Creates a note interval between two notes created by
        this notation

        :raises IncompatibleOriginContexts: If one of the notes has
            a different notation than this one

        :param note_a: The source note
        :param note_b: The target note
        """
        warn(
            f'{self.__class__.__name__}.note_interval is deprecated and '
            f'will be removed in 1.0.0. Please use '
            f'{self.__class__.__name__}.interval instead.',
            DeprecationWarning,
            stacklevel=2,
        )
        return self.interval(note_a, note_b)

    def note_scale(
        self, notes: Optional[List[NatAccNote]] = None
    ) -> NatAccNoteScale:
        """
        .. deprecated:: 0.2.0
           Use :py:meth:`scale` instead.

        Creates a note scale from a list of notes

        :raises IncompatibleOriginContexts: If one of the notes has
            a different notation than this one

        :param notes: A list of notes created by this
            notation
        """
        warn(
            f'{self.__class__.__name__}.note_scale is deprecated and '
            f'will be removed in 1.0.0. Please use '
            f'{self.__class__.__name__}.scale instead.',
            DeprecationWarning,
            stacklevel=2,
        )
        return self.scale(notes)

    def shorthand_interval(
        self, symbol: str, number: int
    ) -> NatAccNoteInterval:
        """
        Creates an interval without specifying two notes.

        A caveat for tunings that are not equal-step: Intervals can have
        irregular sizes, even if they are notated the same. This method
        will automatically add some reference note to the interval to be
        able to calculate ANY size of the interval, so the result of this
        method might differ in size from a result that you obtained by
        forming an interval through the note_interval method.

        :param symbol: An interval symbol of this notation
            (for example P, A, M, m)
        :param number: An interval number indicating the interval
            step width according to the convention laid out by
            this notation
        """

        nat_diff = self.interval_number_to_nat_diff(number)
        nat_diffc = abs(nat_diff) % self.nat_count

        symbol_code = self._interval_symbol_codes[nat_diffc]
        acc_sum_vector = symbol_code.get_vector(symbol)

        # interval symbol codes are defined for positive natural
        # differences, so e.g. a ^d will result in an accidental
        # vector of (1, -2). if however the natural difference
        # is a negative one ^d will actually point to (-1, 2)
        # (we could have also defined additional symbol codes
        # for negative naturals, but this way is less complicated
        # to write albeit more difficult to comprehend)

        if nat_diff < 0:
            acc_sum_vector = scalar_op(operator.mul, acc_sum_vector, -1)

        first_natc_symbol = self.get_natc_symbol(0)
        ref_note = self.note(first_natc_symbol, 0)

        nat_pitch_diff = self.std_pitch_diff(nat_diff)

        acc_diff_vector = self.acc_sum_vector_to_acc_diff_vector(
            acc_sum_vector
        )
        pitch_diff_zero = reduce(
            operator.add, acc_diff_vector
        ) + nat_pitch_diff
        pitch_diff = pitch_diff_zero - ref_note.pitch_index

        tuning = self.tuning
        frequency_ratio = ref_note.pitch.interval(
            tuning.pitch(pitch_diff_zero)
        ).frequency_ratio

        return self._interval_cls(
            self,
            frequency_ratio,
            pitch_diff,
            ref_note,
            nat_diff,
            acc_sum_vector,
            acc_diff_vector,
            symbol,
            number,
        )

    def natural_scale(self, bi_index: int = 0) -> NatAccNoteScale:
        """
        Creates a scale with all the naturals in this notation
        in a specific base interval (in Western notations this
        is typically the C major scale)

        :param bi_index: (optional, defaults to 0). The
            index of the base interval the notes should
            reside in
        """

        notes = []
        for natc_symbol, _ in self._naturals:
            note = self.note(natc_symbol, bi_index)
            notes.append(note)

        return self.scale(notes)

    def pc_scale(
        self,
        pc_symbols: Optional[List[str]] = None,
        root_nat_bi_index: int = 0
    ) -> NatAccNoteScale:
        """
        Constructs a note scale from a list of pitch class symbols.
        The pitch class symbols are assumed to be in the order they
        appear in the scale meaning that e.g. in 12-EDO the provided
        argument ['G', 'D', 'E'] will result in a scale with notes
        G0, D1, E1. The base interval of the natural of the first
        provided pc symbol will always assumed to be 0.

        :raises UnknownNoteSymbol: If one of the pc symbols is not
            valid in the definition of this notation

        :param pc_symbols: A list of pitch class symbols.
        :param root_nat_bi_index: (optional, defaults to 0) The base
            interval index of the natural of the root (for example a
            B#-2 in 12-EDO has the natural base interval index of 2,
            even though the pitch is in base interval 3).
        """

        notes = []
        current_nat_bi_index = root_nat_bi_index

        if not pc_symbols:
            return self.scale()

        notes.append(self.note(pc_symbols[0], root_nat_bi_index))

        for pc_symbol in pc_symbols[1:]:
            note = self.note(pc_symbol, current_nat_bi_index)
            if note <= notes[-1]:
                current_nat_bi_index += 1
                note = note.transpose_bi_index(1)
            notes.append(note)

        return self.scale(notes)

    # methods for mapping of natural indices / natural class
    # indices to pitch indices / pitch class indices

    def nat_index_to_pc_index(self, nat_index: int) -> PeriodicIndexT:
        """
        Returns the pitch class index a natural index refers to

        :param nat_index: A natural index
        """

        pitch_index = self.nat_index_to_pitch_index(nat_index)
        return pitch_index % len(self.tuning)

    def is_natural(self, pitch_index: PeriodicIndexT) -> bool:
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
        for this notation (typically 7 for Western-style
        notations)
        """
        return len(self._naturals)

    @property
    def natc_pitch_indices(self) -> List[PeriodicIndexT]:
        """
        A sorted list of natural class pitch indices
        that are present in this notation
        """
        return [t[1] for t in self._naturals]

    @property
    def natc_pc_indices(self) -> List[PeriodicIndexT]:
        """
        A sorted list of natural class pitch class indices
        that are present in this notation
        """

        return [
            natc_pitch_index % len(self.tuning)
            for natc_pitch_index in self.natc_pitch_indices
        ]

    # natural symbol processing

    def append_natural(
        self, natc_symbol: str, natc_pitch_index: PeriodicIndexT
    ):
        """
        Appends a new natural to this notation. The order in which
        naturals are added determines their natural class index,
        so the first added natural will get natural class index 0,
        the second 1, and so forth.

        :raises AmbiguousSymbol: If the given natural symbol already
            denotes a previously appended natural index

        :param natc_symbol: A string denoting the natural (typically
            a single letter)
        :param natc_pitch_index: The pitch index of the natural class
            that is added. For most tunings, this pitch index is equal
            to the pitch class index because for most tunings there
            exists no note tuple (natc_symbol, 0) that is not in the
            first base interval. However, there are outliers like
            5-EDO in which (B, 0) = (C, 1) and (B, 0) has a pitch
            index in the second base interval
        """

        added_symbols = {t[0] for t in self._naturals}

        if natc_symbol in added_symbols:
            raise AmbiguousSymbol(
                f'Symbol {natc_symbol} is already used by a '
                f'previous natural class index'
            )

        self._naturals.append((natc_symbol, natc_pitch_index))

    def get_natc_symbol(self, nat_index: int) -> str:
        """
        Returns a string symbol for a natural index like
        0 -> 'C' or 8 -> 'D' in 12-EDO

        :raises InvalidNaturalIndex: If the natural index is
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
        by the subclass constructor
        """
        if self._acc_symbol_code is None:
            raise IncompleteNotation('No symbol code for accidentals was set')
        return self._acc_symbol_code

    @acc_symbol_code.setter
    def acc_symbol_code(self, symbol_code: SymbolCode):
        self._acc_symbol_code = symbol_code

    def get_acc_symbol(self, acc_sum_vector: Tuple[int, ...]) -> str:
        """
        Returns a symbol string for an accidental vector,
        like (1, 0) -> '#' or (-1, 1) -> '^b'

        :raises InvalidAccidentalValue: If the accidental symbol
            code of this notation does not have a symbol or
            symbol combination that maps to this value

        :param acc_sum_vector: The (unweighted) accidental sum vector
        """

        try:
            return self.acc_symbol_code.get_symbol_str(acc_sum_vector)
        except SymbolValueNotMapped:
            raise InvalidAccidentalValue(
                f'Accidental vector {acc_sum_vector} can '
                f'not be represented by this notation'
            )

    # interval symbol processing

    def set_interval_symbol_code(
        self, nat_diffc: int, symbol_code: SymbolCode
    ):
        """
        Sets an interval class symbol for a natural index difference
        class. The natural index difference class is a number between
        0 and the number of naturals in the notation (exclusive), so
        e.g. [0, ..., 6] in a traditional Western system that has 7
        naturals. It is calculated by taking the absolute distance
        of two natural indices modulo the number of naturals in the
        notation, so e.g. 2 for intervals (C0, E#0), (C0, E1) and
        (E#2, C0).

        The natural index difference class is closely related to the
        Roman numeral index of intervals, for example, a difference of
        2 is the same as III, a difference of 0 is the same as I, etc.

        Associating a natural index difference class with a specific
        symbol code allows setting different interval naming schemes
        for different interval numbers, e.g. making a difference
        between perfect and imperfect interval naming schemes. In
        the Western system differences 0 (unison), 3 (fourth) and 4
        (fifth) use the P/A/d interval symbols while for differences
        1 (second), 2 (third), 5 (sixth), 6 (sevenths) the system
        M/m/A/d is used.

        :raises InvalidNaturalDiffClassIndex: If the natural diff class
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

    def get_interval_symbol(
        self, nat_diff: int, acc_sum_vector: Tuple[int]
    ) -> str:
        """
        Returns the interval symbol for a natural/accidental note
        interval. Interval symbols depend on the natural index
        difference class of the two notes (e.g. if the interval
        is a unison, a third, a fifth, etc) and the deviation
        from the standard pitch difference of a natural difference
        (In 12-EDO this standard pitch difference would e.g. be 7
        for a fifth, 4 for a third, etc)

        :raises IncompleteNotation: If no symbol code was
            registered for the given parameters

        :param nat_diff: The difference in natural indices
        :param acc_sum_vector: The (unweighted) accidental sum
            vector of the interval
        """

        # the natural index difference is an indicator whether
        # this is a upwards or downwards interval. intervals
        # can have a negative pitch difference but still be
        # considered upwards, if the natural index difference
        # is > 0, for example (C-0, Dbbb-0)

        # for the selection of the symbol code interval directions
        # do not matter, e.g. both (C-0, D#-0) and (D#-0, C-0) are
        # considered 'm' with roman numerals 2 and -2 respectively

        nat_diffc = abs(nat_diff) % self.nat_count
        symbol_code = self._interval_symbol_codes.get(nat_diffc)

        if symbol_code is None:
            raise IncompleteNotation(
                f'No interval symbol code for natural difference '
                f'class index {nat_diffc} was registered in '
                f'this notation'
            )

        # interval symbol codes are defined for positive natural
        # differences, so e.g. a (1, -2) accidental vector
        # will result in ^d. if however the natural difference
        # is a negative one (1, -2) will actually point to vA
        # so we need to sign-invert on negative natural diff.
        # (we could have also defined additional symbol codes
        # for negative natural diffs, but this way is less
        # complicated to write albeit more difficult to
        # comprehend)

        if nat_diff < 0:
            acc_sum_vector = scalar_op(operator.mul, acc_sum_vector, -1)

        symbol = symbol_code.get_symbol_str(acc_sum_vector)
        return symbol

    def nat_diff_to_interval_number(self, nat_diff: int) -> int:
        """
        Returns an interval number for a natural index
        difference. By default, it returns a 1-based ordinal number.
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
        Returns a natural index difference for an interval number.
        By default, it assumes that the interval number is given
        in 1-based ordinal notation. Subclasses can change this
        behavior by overwriting this method.

        :param interval_number: An interval number
        """
        if interval_number > 0:
            return interval_number - 1
        if interval_number < 0:
            return interval_number + 1

        raise InvalidIntervalNumber(
            "Interval number must be strictly positive or negative"
        )

    def parse_pc_symbol(
        self, pc_symbol: str
    ) -> Tuple[str, str, int, Tuple[int, ...]]:
        """
        Parses a pitch class symbol into its natural class symbol
        part and its accidental symbol part. Returns a 4-tuple
        (natc_symbol, acc_symbol, natc_index, acc_sum_vector) with
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
                f'Could not find a natural that would fit to {pc_symbol}.'
            )

        acc_tail = pc_symbol[len(best_natc_symbol):]

        try:
            acc_sum_vector = self.acc_symbol_code.get_vector(acc_tail)
        except UnknownSymbolString:
            raise UnknownNoteSymbol(
                'Could not find a meaning for the accidentals'
            )

        return (best_natc_symbol, acc_tail, best_natc_index, acc_sum_vector)

    def gen_pc_symbol(
        self, natc_index: int, acc_sum_vector: Tuple[int, ...]
    ) -> Tuple[str, str, str]:
        """
        Creates a pitch class symbol from a natural class index and an
        accidental vector. This defaults to calculating the first natural
        symbol found for natc_index and concatenating it with the minimal
        accidental symbol configuration for the vector.

        The method will return a tuple of 3 with the following semantics:
            * The first element will be the pitch class symbol
            * The second element will be the natural class symbol
            * The third element will be the accidental symbol string

        (Subclasses can overwrite this method if they e.g wish to generate
        pc_symbols that have post-fix or in-fix naturals)

        :param natc_index: A natural class index of a note
        :param acc_sum_vector: An (unweighted) accidental sum vector
        """

        natc_symbol = self.get_natc_symbol(natc_index)
        acc_symbol = self.get_acc_symbol(acc_sum_vector)

        return (natc_symbol + acc_symbol, natc_symbol, acc_symbol)
