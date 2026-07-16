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

from __future__ import annotations

from abc import ABC
from abc import abstractmethod
from collections.abc import Sequence
from typing import Generic
from typing import Optional
from typing import overload
from typing import Self
from typing import Iterable
from typing import TypeVar
from typing import Tuple
from types import EllipsisType
from .protocols import Index
from .protocols import PeriodicPitchLike
from .masks import mask_select
from ..exc import IncompatibleOriginContexts
from .freq_repr import FreqRepr
from .interval import Interval


FreqReprT = TypeVar('FreqReprT', bound=FreqRepr)
IndexT = TypeVar('IndexT', bound=Index)


class FreqReprSeq(Sequence[FreqReprT], ABC, Generic[IndexT, FreqReprT]):
    """
    FreqReprSeq is the abstract base class for all pitch/note sequence types.

    In line with its Sequence superclass frequency representation sequences
    implement iteration, the 'in' operator, the == operator, item retrieval
    with [], concatenation with +, repeated self-concatenation with \\*,
    searching with index, and len().

    Like scale types sequences also allow partitioning with partial,
    partial_not and partition.

    :param origin_context: An origin context (like a tuning or a notation)
    :param elements: A sequence of elements from the origin context
    """

    def __init__(
        self, origin_context, elements: Optional[Iterable[FreqReprT]] = None
    ):

        self._origin_context = origin_context

        if elements is None:
            _elements: Sequence[FreqReprT] = []
        else:
            _elements = elements

        self._elements = []

        for element in _elements:
            if element.origin_context is not self.origin_context:
                raise IncompatibleOriginContexts(
                    f'The element {element} does not originate from context '
                    f'{origin_context}. Cannot construct sequence.'
                )
            self._elements.append(element)

    @property
    def origin_context(self):
        """
        The origin context from which this sequence was built
        """
        return self._origin_context

    def __hash__(self):
        return hash(('FreqReprSeq', ) + tuple(self.frequencies))

    def __contains__(self, o: object) -> bool:

        if isinstance(o, FreqRepr):
            return o in self._elements

        if isinstance(o, Interval):
            for element_a in self._elements:
                for element_b in self._elements:
                    interval_u = element_a.interval(element_b)
                    if interval_u == o:
                        return True
                    interval_d = element_b.interval(element_a)
                    if interval_d == o:
                        return True
        return False

    def __add__(self, other: Self) -> Self:
        return self.origin_context.seq(list(self) + list(other))

    def __mul__(self, scalar: int) -> Self:
        return self.origin_context.seq(scalar * list(self))

    def __rmul__(self, scalar: int) -> Self:
        return self.origin_context.seq(scalar * list(self))

    @overload
    def __getitem__(self, index_or_slice: int) -> FreqReprT: ...

    @overload
    def __getitem__(self, index_or_slice: slice) -> Self: ...

    def __getitem__(self, index_or_slice: int | slice) -> FreqReprT | Self:

        if type(index_or_slice) is slice:
            partial = self._elements[index_or_slice]
            return self.origin_context.seq(partial)

        return self._elements[index_or_slice]

    def index(self, element, start=0, end=None, /) -> int:
        """
        Return first index of element (similar to the index method
        of python's list)

        :param element: The element to search for
        :param start: If set method ignores occurences before given
            index (optional, defaults to 0)
        :param end: If set method ignores occurences after given
            index (optional, defaults to end of sequence)

        :raises ValueError: If element was not found in sequence
        """

        try:

            if end is None:
                return self._elements.index(element, start)

            if start is not None and end is not None:
                return self._elements.index(element, start, end)

        except ValueError:
            raise ValueError(f'{element} is not in sequence')

    def __len__(self) -> int:
        return len(self._elements)

    def __iter__(self):
        return self._elements.__iter__()

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, FreqReprSeq):
            # FIXME: should scale equality be considered here?
            return False
        if len(self) != len(other):
            return False
        for a, b in zip(self, other):
            if a != b:
                return False
        return True

    def with_element(
        self, element: FreqReprT, insert_pos: Optional[int] = None
    ) -> Self:
        """
        Returns a new sequence containing all elements
        from this sequence and the additional one given as a parameter.
        By default new elements appear at the end of the sequence.

        :param element: The new element to be added to the result
        :param insert_pos: The insertion position of the new element.
            0 will insert the element at the front, 1 will insert the
            element at the second position, etc. (optional, default is
            None which results in the value len(sequence) + 1)

        :raises IncompatibleOriginContexts: If element has a different
            origin context than this sequence
        """

        if element.origin_context is not self.origin_context:
            raise IncompatibleOriginContexts(
                "Sequence and new element have a different origin context"
            )

        if insert_pos is None:
            insert_pos = len(self) + 1

        elements = list(self)
        elements.insert(insert_pos, element)
        return self.origin_context.seq(elements)

    def retune_closest(self, origin_context) -> Self:
        """
        Gets the sequence in a target origin context that is closest
        to the frequency series of this sequence.

        :param origin_context: The target origin context

        :raises TypeError: If the target context does not have a
            proper definition of a closest representation to a
            given frequency
        """

        return origin_context.closest_seq(self.frequencies)

    def is_subseq(self, seq: Self, proper=False):
        """
        Returns True if the given sequence is a subsequence
        of this one, False otherwise.

        :param seq: The (possible) subsequence
        :param proper: (optional, default is False). If set to
            True function will return False if sequences are
            identical
        """

        if seq.origin_context is not self.origin_context:
            raise IncompatibleOriginContexts(
                "Sequences have different origin contexts"
            )

        len_seq = len(seq)
        len_self = len(self)
        len_diff = len_seq - len_self

        if len_diff < 0:
            False

        if proper and len_diff == 0:
            return False

        for i in range(0, len_diff + 1):
            if self == seq[i:i+len_self]:
                return True

        return False

    def is_superseq(self, seq: Self, proper=False):
        """
        Returns True if the given sequence is a supersequence
        of this one, False otherwise.

        :param seq: The (possible) subsequence
        :param proper: (optional, default is False). If set to
            True function will return False if sequences are
            identical
        """
        return seq.is_subseq(self, proper)

    def partial(self, mask_expr: int | Tuple[int | EllipsisType, ...]) -> Self:
        """
        Returns a new sequence consisting of a selection of indices
        of this sequence. The selection is defined by an index mask
        expression.

        An index mask can be defined as a tuple of consecutive
        indices, e.g. (1, 2, 5) gives a sequence including the
        second, third and sixth element of this one.

        An ellipsis between two indices indicates that all
        indices between them should be selected as well, e.g.
        (1, ..., 5, 9) is equivalent to (1, 2, 3, 4, 5, 9).

        If a mask begins with an ellipsis all indices from
        0 to the next index are added to the selection, e.g.
        (..., 3, 5) is equivalent to (0, 1, 2, 3, 5).

        A mask without a last index is called right-open and will
        select all indices from the last index to the end of the
        sequence, for example (2, ...) will select all elements
        of the sequence except the first two.

        If only one element should be selected a simple integer
        can be used

        :param mask_expr: An index mask expression which defines
            the selection of indices from this sequence.
        """

        elements = []
        for selected, element in mask_select(mask_expr, self):
            if selected:
                elements.append(element)
        return self.origin_context.seq(elements)

    def partial_not(
        self, mask_expr: int | Tuple[int | EllipsisType, ...]
    ) -> Self:
        """
        Returns a new sequence consisting of a selection of indices
        of this sequence. The selection will be determined by an
        index mask and will hold all elements whose index is
        NOT covered by the mask.

        An index mask can be defined as a tuple of consecutive
        indices, e.g. (1, 2, 5) gives a sequence including the
        second, third and sixth element of this one.

        An ellipsis between two indices indicates that all
        indices between them should be selected as well, e.g.
        (1, ..., 5, 9) is equivalent to (1, 2, 3, 4, 5, 9).

        If a mask begins with an ellipsis all indices from
        0 to the next index are added to the selection, e.g.
        (..., 3, 5) is equivalent to (0, 1, 2, 3, 5).

        A mask without a last index is called right-open and will
        select all indices from the last index to the end of the
        sequence, for example (2, ...) will select all elements
        of the sequence except the first two.

        If only one element should be selected a simple integer
        can be used

        :param mask_expr: An index mask expression which defines
            the selection of indices from this sequence.
        """

        elements = []
        for selected, element in mask_select(mask_expr, self):
            if not selected:
                elements.append(element)
        return self.origin_context.seq(elements)

    def partition(
        self, mask_expr: int | Tuple[int | EllipsisType, ...]
    ) -> Tuple[Self, Self]:
        """
        Partitions the sequence into two parts using an index mask.
        The function will return a tuple of two sequences with the
        first sequence including all indices that are covered by
        the index mask and the second one including all indices
        that are not.

        An index mask can be defined as a tuple of consecutive
        indices, e.g. (1, 2, 5) defines a sequence including the
        second, third and sixth element of this one.

        An ellipsis between two indices indicates that all
        indices between them should be selected as well, e.g.
        (1, ..., 5, 9) is equivalent to (1, 2, 3, 4, 5, 9).

        If a mask begins with an ellipsis all indices from
        0 to the next index are added to the selection, e.g.
        (..., 3, 5) is equivalent to (0, 1, 2, 3, 5).

        A mask without a last index is called right-open and will
        select all indices from the last index to the end of the
        sequence, for example (2, ...) will select all elements of
        the sequence except the first two.

        If only one element should be selected a simple integer
        can be used

        :param mask_expr: An index mask expression which defines
            the selection of indices from this sequence.
        """

        elements_a = []
        elements_b = []
        for selected, element in mask_select(mask_expr, self):
            if selected:
                elements_a.append(element)
            else:
                elements_b.append(element)
        seq_a = self.origin_context.seq(elements_a)
        seq_b = self.origin_context.seq(elements_b)
        return seq_a, seq_b

    @property
    def frequencies(self):
        """
        An ordered list of frequencies present in this sequence
        """
        return [element.frequency for element in self]

    def transpose(self, diff) -> Self:
        """
        Transposes the sequence by the given difference
        """
        transposed = [element.transpose(diff) for element in self]
        return self.origin_context.seq(transposed)

    def zero_normalized(self) -> Self:
        """
        Returns the sequence transposed in a way so the first element
        has pitch index 0. In notations with enharmonic ambiguity a
        designated zero note is used (in western-like notations
        typically C0)
        """

        if len(self) == 0:
            raise ValueError(
                'zero_normalized is not defined on empty sequence'
            )

        if self.is_zero_normalized:
            return self

        ze = self.origin_context.zero_element
        interval = self[0].interval(ze)
        return self.transpose(interval)

    @property
    @abstractmethod
    def is_zero_normalized(self) -> bool:
        """
        Returns True if this function is zero normalized, meaning
        that the first element of the scale is identical to the
        zero element of the origin context (pitch 0 in tunings,
        typically C0 in western-like notations)

        (must be implemented by subclass, since comparison to the
        the zero note should be done according to notational identity)
        """

    def to_interval_seq(self):
        """
        Returns this sequence represented as an interval sequence
        """

        # FIXME: how is interval seq defined on an empty sequence?
        # currently it is defined as empty, but it already defined
        # as empty on a 1 element scale. should interval seq be
        # undefined on empty scale?

        intervals = []
        for i in range(0, len(self) - 1):
            intervals.append(self[i].interval(self[i + 1]))
        return self.origin_context.interval_seq(intervals)

    def to_interval_fan(self, ref: Optional[Self] = None):
        """
        Returns this sequence represented as an interval fan
        """

        if len(self) == 0:
            return self.origin_context.interval_fan()

        _ref = self[0] if ref is None else ref

        if _ref.origin_context is not self.origin_context:
            raise IncompatibleOriginContexts(
                f'The ref parameter {_ref} does not originate from context '
                f'{self.origin_context}. Cannot construct interval fan.'
            )

        intervals = []
        for element in self:
            intervals.append(_ref.interval(element))
        return self.origin_context.interval_fan(intervals)

    def retrograde(self) -> Self:
        """
        Returns the retrograde of this sequence, which is defined
        as "mirroring" the sequence so the last note becomes the
        first note and vice versa
        """
        return self[::-1]

    def inversion(self) -> Self:
        """
        Returns the inversion of this sequence, which is defined
        as transforming all ascending intervals in the sequence
        into their descending counterpart and vice versa.
        """

        if len(self) == 0:
            return self

        iseq_inversion = self.to_interval_seq().inversion()
        return self[0].seq(iseq_inversion)


PeriodicFreqReprT = TypeVar('PeriodicFreqReprT', bound=PeriodicPitchLike)


class PeriodicFreqReprSeq(FreqReprSeq[PeriodicFreqReprT]):
    """
    PeriodicFreqReprSeq is the abstract base class for frequency
    representation sequences that contain frequency representations of
    periodic tunings / notations.

    It implements the following additional methods:
        * transpose_bi_index
        * is_equivalent

    :param origin_context: An origin context (like a tuning or a notation)
    :param elements: A list of frequency representations
    """

    def transpose_bi_index(self, bi_diff: int) -> Self:
        """
        Returns a sequence with the same pitch class indices
        and symbols, but with a transposed base interval

        :param bi_diff: The difference in base interval
            between this sequence and the resulting one
        """

        elements = []
        for element in self:
            elements.append(element.transpose_bi_index(bi_diff))
        return self.origin_context.seq(elements)

    def is_equivalent(self, other: PeriodicFreqReprSeq) -> bool:
        """
        Returns True if two sequences are equivalent, i.e. every element in
        this sequence corresponds to another one in the other sequence at
        the same index.

        Periodic sequences of different origin contexts can be compared
        if their origin contexts have the same equivalency interval.
        Equivalency between sequences of different contexts is defined
        as "equality after base interval alignment"

        :raises IncompatibleOriginContexts: If the other sequence has a
            different equivalency interval definition

        :param other: Another periodic scale
        """

        if self.tuning.eq_ratio != other.tuning.eq_ratio:
            raise IncompatibleOriginContexts(
                'Equivalency can only be tested for sequences from tunings '
                'with the same equivalency interval'
            )

        if len(self) != len(other):
            return False

        for a, b in zip(self, other):
            if not a.is_equivalent(b):
                return False

        return True
