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
This module implements base classes for scales
"""

from __future__ import annotations

from warnings import warn
from abc import ABC
from abc import abstractmethod
from collections.abc import Sequence
from typing import overload
from typing import Optional
from typing import Iterable
from typing import TypeVar
from typing import List
from typing import Self
from typing import Tuple
from types import EllipsisType
from .interval import Interval
from .freq_repr import FreqRepr
from .protocols import PeriodicPitchLike
from .masks import mask_select
from ..exc import IncompatibleOriginContexts

FreqReprT = TypeVar('FreqReprT', bound=FreqRepr)


class Scale(Sequence[FreqReprT], ABC):
    """
    Scale is the abstract base class for all scale types. The class
    implements iteration, the 'in' operator, the == operator, item
    retrieval with [] and set operations.

    Subclasses must implement at least the transpose function

    :param origin_context: An origin context (like a tuning or a notation)
    :param elements: A list of frequency representations
    """

    def __init__(
        self, origin_context, elements: Optional[Iterable[FreqReprT]] = None
    ):

        self._origin_context = origin_context

        if elements is None:
            _elements: Iterable[FreqReprT] = []
        else:
            _elements = elements

        unique_elements: List[FreqReprT] = []
        element_set = set()

        for element in _elements:
            if element.origin_context is not self.origin_context:
                raise IncompatibleOriginContexts(
                    f'The element {element} does not originate from context '
                    f'{origin_context}. Cannot construct scale.'
                )
            if element not in element_set:
                element_set.add(element)
                unique_elements.append(element)

        self._sorted_elements = sorted(unique_elements)

    @property
    def origin_context(self):
        """
        The origin context from which this scale was built
        """
        return self._origin_context

    def __iter__(self):
        return self._sorted_elements.__iter__()

    def __len__(self) -> int:
        return len(self._sorted_elements)

    def __contains__(self, o: object) -> bool:

        if isinstance(o, FreqRepr):
            return o in self._sorted_elements

        if isinstance(o, Interval):
            for element_a in self._sorted_elements:
                for element_b in self._sorted_elements:
                    interval_u = element_a.interval(element_b)
                    if interval_u == o:
                        return True
                    interval_d = element_b.interval(element_a)
                    if interval_d == o:
                        return True

        return False

    @overload
    def __getitem__(self, index_or_slice: int) -> FreqReprT: ...

    @overload
    def __getitem__(self, index_or_slice: slice) -> Self: ...

    def __getitem__(self, index_or_slice: int | slice) -> FreqReprT | Self:

        if type(index_or_slice) is slice:
            partial = self._sorted_elements[index_or_slice]
            return self.origin_context.scale(partial)

        return self._sorted_elements[index_or_slice]

    def __eq__(self, other: object):
        if not isinstance(other, Scale):
            return False
        if len(self) != len(other):
            return False
        for a, b in zip(self, other):
            if a != b:
                return False
        return True

    def with_element(self, element: FreqReprT) -> Self[FreqRepr]:
        """
        Returns a new scale containing all elements from this scale
        and the additional one given as a parameter.

        :param element: The new element to be added to the result

        :raises IncompatibleOriginContexts: If element has a different
            origin context than this scale
        """

        if element.origin_context is not self.origin_context:
            raise IncompatibleOriginContexts(
                'Scale and new element have a different origin context'
            )

        elements = list(self)
        elements.append(element)
        return self.origin_context.scale(elements)

    def partial(self, mask_expr: int | Tuple[int | EllipsisType, ...]) -> Self:
        """
        Returns a new scale consisting of a selection of indices
        of this scale. The selection is defined by an index mask
        expression.

        An index mask can be defined as a tuple of consecutive
        indices, e.g. (1, 2, 5) gives a scale including the
        second, third and sixth element of this one.

        An ellipsis between two indices indicates that all
        indices between them should be selected as well, e.g.
        (1, ..., 5, 9) is equivalent to (1, 2, 3, 4, 5, 9).

        If a mask begins with an ellipsis all indices from
        0 to the next index are added to the selection, e.g.
        (..., 3, 5) is equivalent to (0, 1, 2, 3, 5).

        A mask without a last index is called right-open and will
        select all indices from the last index to the end of the
        scale, for example (2, ...) will select all elements of
        the scale except the first two.

        If only one element should be selected a simple integer
        can be used

        :param mask_expr: An index mask expression which defines
            the selection of indices from this scale.
        """

        elements = []
        for selected, element in mask_select(mask_expr, self):
            if selected:
                elements.append(element)
        return self.origin_context.scale(elements)

    def partial_not(
        self, mask_expr: int | Tuple[int | EllipsisType, ...]
    ) -> Self:
        """
        Returns a new scale consisting of a selection of indices
        of this scale. The selection will be determined by an
        index mask and will hold all elements whose index is
        NOT covered by the mask.

        An index mask can be defined as a tuple of consecutive
        indices, e.g. (1, 2, 5) gives a scale including the
        second, third and sixth element of this one.

        An ellipsis between two indices indicates that all
        indices between them should be selected as well, e.g.
        (1, ..., 5, 9) is equivalent to (1, 2, 3, 4, 5, 9).

        If a mask begins with an ellipsis all indices from
        0 to the next index are added to the selection, e.g.
        (..., 3, 5) is equivalent to (0, 1, 2, 3, 5).

        A mask without a last index is called right-open and will
        select all indices from the last index to the end of the
        scale, for example (2, ...) will select all elements of
        the scale except the first two.

        If only one element should be selected a simple integer
        can be used

        :param mask_expr: An index mask expression which defines
            the selection of indices from this scale.
        """

        elements = []
        for selected, element in mask_select(mask_expr, self):
            if not selected:
                elements.append(element)
        return self.origin_context.scale(elements)

    def partition(
        self, mask_expr: int | Tuple[int | EllipsisType, ...]
    ) -> Tuple[Self, Self]:
        """
        Partitions the scale into two parts using an index mask.
        The function will return a tuple of two scales with the
        first scale including all indices that are covered by
        the index mask and the second one including all indices
        that are not.

        An index mask can be defined as a tuple of consecutive
        indices, e.g. (1, 2, 5) gives a scale including the
        second, third and sixth element of this one.

        An ellipsis between two indices indicates that all
        indices between them should be selected as well, e.g.
        (1, ..., 5, 9) is equivalent to (1, 2, 3, 4, 5, 9).

        If a mask begins with an ellipsis all indices from
        0 to the next index are added to the selection, e.g.
        (..., 3, 5) is equivalent to (0, 1, 2, 3, 5).

        A mask without a last index is called right-open and will
        select all indices from the last index to the end of the
        scale, for example (2, ...) will select all elements of
        the scale except the first two.

        If only one element should be selected a simple integer
        can be used

        :param mask_expr: An index mask expression which defines
            the selection of indices from this scale.
        """

        elements_a = []
        elements_b = []
        for selected, element in mask_select(mask_expr, self):
            if selected:
                elements_a.append(element)
            else:
                elements_b.append(element)
        scale_a = self.origin_context.scale(elements_a)
        scale_b = self.origin_context.scale(elements_b)
        return scale_a, scale_b

    @abstractmethod
    def transpose(self, diff) -> Self:
        """
        Transposes the scale by the given difference
        (must be overwritten by subclass)

        :param diff: An interval or interval-like object
        """
        # argument diff is not type annotated because it can differ
        # greatly for scales containing single dimensional elements
        # and scales containing multi-dimensional elements

    def reflection(self, axis: Optional[FreqReprT] = None) -> Self:
        """
        A reflection of each pitch/note across a pitch/note axis.
        In technical terms the method calculates the interval from
        each element to the axis and then applies that interval to
        to the axis.

        :param axis: The element across which this object is
            reflected (optional, defaults to the zero element
            of the origin context)

        If scale is reflected across the zero element, reflection
        is equivalent to inversion of the pitch class set
        """

        elements = [element.reflection(axis) for element in self]
        return self.origin_context.scale(elements)

    def zero_normalized(self) -> Self:
        """
        Returns the scale transposed in a way so the root has pitch
        index 0. In notations with enharmonic ambiguity a designated
        zero note is used (in western-like notations typically C0)
        """

        if len(self) == 0:
            raise ValueError('zero_normalized is not defined on empty scale')

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

    @property
    def frequencies(self):
        """
        An ordered list of frequencies present in this scale
        """
        return [element.frequency for element in self]

    def to_interval_seq(self):
        """
        Returns this scale represented as an interval sequence
        """

        intervals = []
        for i in range(0, len(self) - 1):
            intervals.append(self[i].interval(self[i + 1]))
        return self.origin_context.interval_seq(intervals)

    def spec_interval(self, source_index, target_index):
        """
        Returns the specific interval for a generic interval.
        For example in the 12-EDO C major scale the generic
        interval defined by (0, 2) is the specific interval
        major 3.

        :param source_index: Source index for the interval
        :param target_index: Target index for the interval
        """

        return self[source_index].interval(self[target_index])

    def to_intervals(self) -> List[Interval[FreqReprT]]:
        """
        Returns this scale represented as a list of intervals
        """
        warn(
            f'{self.__class__.__name__}.to_interval is deprecated and '
            f'will be removed in 1.0.0. Please use '
            f'{self.__class__.__name__}.to_interval_seq instead.',
            DeprecationWarning,
            stacklevel=2,
        )

        intervals = []
        for i in range(0, len(self) - 1):
            intervals.append(self[i].interval(self[i + 1]))
        return intervals

    # set operations

    def union(self, other: Self) -> Self:
        """
        Returns a new scale including all elements from
        this scale as well as the other

        :param other: Another scale of the same origin context

        :raises IncompatibleOriginContexts: If the other scale has a
            different origin context
        """

        if self.origin_context is not other.origin_context:
            raise IncompatibleOriginContexts(
                'Scales do not originate from the same context'
            )

        elements = list(self) + list(other)
        return self.origin_context.scale(elements)

    def __or__(self, other: Self) -> Self:
        """
        operator shortcut for union method
        """
        return self.union(other)

    def intersection(self, other: Self) -> Self:
        """
        Returns a new scale including all elements that are
        included in both scales.

        :param other: Another scale of the same origin context

        :raises IncompatibleOriginContexts: If the other scale has a
            different origin context
        """

        if self.origin_context is not other.origin_context:
            raise IncompatibleOriginContexts(
                'Scales do not originate from the same context'
            )

        elements = []

        for element_a in self:
            for element_b in other:
                if element_a == element_b:
                    elements.append(element_a)

        return self.origin_context.scale(elements)

    def __and__(self, other: Self) -> Self:
        """
        operator shortcut for intersection method
        """
        return self.intersection(other)

    def difference(self, other: Self) -> Self:
        """
        Returns a scale containing only elements from this
        scale that are NOT present in the other scale

        :param other: Another scale of the same origin context

        :raises IncompatibleOriginContexts: If the other scale has a
            different origin context
        """

        if self.origin_context is not other.origin_context:
            raise IncompatibleOriginContexts(
                'Scales do not originate from the same context'
            )

        elements = []

        for element_a in self:
            for element_b in other:
                if element_a == element_b:
                    break
            else:
                elements.append(element_a)

        return self.origin_context.scale(elements)

    def __sub__(self, other: Self) -> Self:
        """
        operator shortcut for difference method
        """
        return self.difference(other)

    def symmetric_difference(self, other: Self) -> Self:
        """
        Returns a scale that includes all the elements from both
        scales that exist in either of them but NOT BOTH. This
        is the complement operation of the intersection.

        :param other: Another scale of the same origin context

        :raises IncompatibleOriginContexts: If the other scale has a
            different origin context
        """

        if self.origin_context is not other.origin_context:
            raise IncompatibleOriginContexts(
                'Scales do not originate from the same context'
            )

        diff_a = self.difference(other)
        diff_b = other.difference(self)
        return diff_a.union(diff_b)

    def __xor__(self, other: Self) -> Self:
        """
        operator shortcut for symmetric difference method
        """
        return self.symmetric_difference(other)

    def is_disjoint(self, other: Self) -> bool:
        """
        Determines if this scale has any common elements
        with another scale of the same origin context.

        :param other: Another scale of the same origin context

        :raises IncompatibleOriginContexts: If the other scale has a
            different origin context
        """

        intersection = self.intersection(other)

        return len(intersection) == 0

    def is_subset(self, other: Self, proper: bool = False) -> bool:
        """
        Determines if all elements in this scale also exist
        in the other scale.

        :param other: Another scale of the same origin context
        :param proper: (Optional, default False) When set
            to True method will return False if the two
            sets are identical

        :raises IncompatibleOriginContexts: If the other scale has a
            different origin context
        """

        intersection = self.intersection(other)

        is_subset = self == intersection

        if not proper:
            return is_subset

        return is_subset and not (self == other)

    def is_superset(self, other: Self, proper: bool = False) -> bool:
        """
        Determines if all elements in the other scale also exist
        in this scale.

        :param other: Another scale of the same origin context
        :param proper: (Optional, default False) When set
            to True method will return False if the two
            sets are identical

        :raises IncompatibleOriginContexts: If the other scale has a
            different origin context
        """

        intersection = self.intersection(other)

        is_superset = other == intersection

        if not proper:
            return is_superset

        return is_superset and not (self == other)


PeriodicFreqReprT = TypeVar('PeriodicFreqReprT', bound=PeriodicPitchLike)


class PeriodicScale(Scale[PeriodicFreqReprT]):
    """
    PeriodicScale is the abstract base class for scales that contain
    frequency representations of periodic tunings / notations. It
    overwrites the set operations to allow for the ignore_bi_index
    flag.

    It implements the following additional methods:
        * pcs_normalized
        * pcs_intersection
        * is_equivalent
        * rotated_up
        * rotated_down
        * rotation

    Subclasses must implement at least the transpose function

    :param origin_context: An origin context (like a tuning or a notation)
    :param elements: A list of frequency representations
    """

    def transpose_bi_index(self, bi_diff: int) -> Self:
        """
        Returns a scale with the same pitch class indices
        and symbols, but with a transposed base interval

        :param bi_diff: The difference in base interval
            between this scale and the resulting one
        """

        elements = []
        for element in self:
            elements.append(element.transpose_bi_index(bi_diff))
        return self.origin_context.scale(elements)

    def pcs_normalized(self) -> Self:
        """
        Returns a normalized version of this scale where
        all the elements of the scale are put into the first
        base interval of the tuning

        Note: If the original scale has equivalent element pairs
        the normalized scale will be smaller in cardinality.
        """

        if self.is_pcs_normalized:
            return self

        elements = []

        for element in self._sorted_elements:
            n_element = element.pcs_normalized()
            elements.append(n_element)

        return self.origin_context.scale(elements)

    @property
    def is_pcs_normalized(self) -> bool:
        """
        Returns bool if this scale is pcs normalized. A pcs
        normalized scale only contains elements with base
        interval index 0.
        """

        if len(self) == 0:
            return True

        return self[0].bi_index == 0 and self[-1].bi_index == 0

    def period_normalized(self) -> Self:
        """
        Returns a version of the scale in which each element that
        is above the root element will be transposed to the
        interval between the root element and its equivalent
        in the next base interval. For example the scale of the
        Fm7/11 chord with notes (F0, Ab0, C1, Eb1, Bb1) will
        become the scale (F0, Ab0, Bb0, C1, Eb1)
        """

        if len(self) == 0:
            raise ValueError('period_normalized is not defined on empty scale')

        if self.is_period_normalized:
            return self

        root = self[0]
        elements = [root]

        for subseq_element in self[1:]:
            bi_diff = root.bi_index - subseq_element.bi_index
            element = subseq_element.transpose_bi_index(bi_diff)
            if element == root:
                continue
            if element < root:
                element = element.transpose_bi_index(1)
            elements.append(element)

        return self.origin_context.scale(elements)

    @property
    def is_period_normalized(self) -> bool:
        """
        Returns bool if this scale is period normalized. A period
        normalized scale only contains elements smaller than the
        equivalent of the root note, meaning if the scale starts
        with F3, all subsequent notes are smaller than F4.
        """

        if len(self) == 0:
            raise ValueError(
                'is_period_normalized is not defined on empty scale'
            )

        return self[-1] < self[0].transpose_bi_index(1)

    def plusone_normalized(self) -> Self:
        """
        Returns a period normalized version of the scale with
        an additional transposed root at the end, e.g.
        (F0, G0, A0, B0, C1, D1, E1, F1)
        """

        if len(self) == 0:
            raise ValueError(
                'plusone_normalized is not defined on empty scale'
            )

        scale = self.period_normalized()
        return scale.with_element(scale[0].transpose_bi_index(1))

    @property
    def is_plusone_normalized(self) -> bool:
        """
        Returns a period normalized version of the scale with
        an additional transposed root at the end, e.g.
        (F0, G0, A0, B0, C1, D1, E1, F1)
        """

        if len(self) == 0:
            raise ValueError(
                'is_plusone_normalized is not defined on empty scale'
            )

        root = self[0]
        last = self[-1]

        return (
            root.is_equivalent(last) and
            (last.bi_index - root.bi_index) == 1
        )

    def zp_normalized(self) -> Self:
        """
        Returns the scale transposed in a way so the root has pitch
        index 0 and all elements reside in the first base interval.
        In notations with enharmonic ambiguity a designated
        zero note is used (in western-like notations typically C0)

        The function is equivalent to successively invoking
        zero_normalized + period_normalized or (which is the
        same) zero_normalized + pcs_normalized
        """

        if len(self) == 0:
            raise ValueError('zp_normalized is not defined on empty scale')

        if self.is_zp_normalized:
            return self

        # use pcs_normalized since it can be calculated faster
        return self.zero_normalized().pcs_normalized()

    @property
    def is_zp_normalized(self) -> bool:
        """
        Returns bool if the first element is the zero element of
        the origin context (pitch 0 in tunings, in western-like
        notations typically C0) and all elements reside in the
        first base interval.
        """

        if len(self) == 0:
            raise ValueError('is_zp_normalized is not defined on empty scale')

        return self.is_zero_normalized and self.is_pcs_normalized

    def rotated_up(self) -> Self:
        """
        Create a new scale by transposing the base interval of the
        lowest element upwards until it is above the highest element
        """

        elements = list(self[1:])

        bi_diff = self[-1].bi_index - self[0].bi_index
        element = self[0].transpose_bi_index(bi_diff)

        if element <= elements[-1]:
            element = element.transpose_bi_index(1)

        elements.append(element)
        return self.origin_context.scale(elements)

    def rotated_down(self) -> Self:
        """
        Create a new scale by transposing the base interval of the
        highest element downwards until it is below the lowest element
        """

        elements = list(self[:-1])

        bi_diff = self[0].bi_index - self[-1].bi_index
        element = self[-1].transpose_bi_index(bi_diff)

        if element >= elements[0]:
            element = element.transpose_bi_index(-1)

        elements.append(element)
        return self.origin_context.scale(elements)

    def rotation(self, order: int) -> Self:
        """
        Returns the n-th rotation of this scale.

        :param order: The number of times the scale is
            rotated. If a negative number is given the
            scale will be rotated downwards. On 0 the
            scale will return itself
        """

        if order == 0:
            return self

        scale = self

        if order > 0:
            for _ in range(0, order):
                scale = scale.rotated_up()

        if order < 0:
            for _ in range(0, abs(order)):
                scale = scale.rotated_down()

        return scale

    def is_equivalent(self, other: PeriodicScale) -> bool:
        """
        .. deprecated:: 0.3.0
           Use :py:meth:`is_set_equivalent` instead.

        Returns True if two scales are set equivalent, i.e. every
        element in this scale has an equivalent element somewhere(!)
        in the other scale (and vice versa).

        Periodic scales of different origin contexts can be
        compared if their origin contexts have the same
        equivalency interval. Set equivalency between scales
        of different contexts is defined as "equality after
        pitch class set normalization"

        :raises IncompatibleOriginContexts: If the other scale
            has a different equivalency interval definition

        :param other: Another periodic scale
        """
        warn(
            f'{self.__class__.__name__}.is_equivalent is deprecated '
            f'and will be removed in 1.0.0. Please use '
            f'{self.__class__.__name__}.is_set_equivalent instead.',
            DeprecationWarning,
            stacklevel=2,
        )

        return self.is_set_equivalent(other)

    def is_seq_equivalent(self, other: PeriodicScale) -> bool:
        """
        Returns True if two scales are sequentially equivalent, i.e.
        every element in this scale corresponds to another one in
        the other scale at the same scale index.

        Periodic scales of different origin contexts can be
        compared if their origin contexts have the same
        equivalency interval. Sequential equivalency between
        scales of different contexts is defined as "equality
        after base interval alignment"

        :raises IncompatibleOriginContexts: If the other scale has a
            different equivalency interval definition

        :param other: Another periodic scale
        """

        if self.tuning is other.tuning:
            return self.pc_indices == other.pc_indices

        if self.tuning.eq_ratio == other.tuning.eq_ratio:
            bi_diff = self[0].bi_index - other[0].bi_index
            t_other = other.transpose_bi_index(bi_diff)
            return self == t_other

        raise IncompatibleOriginContexts(
            'Equivalency can only be tested for scales from tunings '
            'with the same equivalency interval'
        )

    def is_set_equivalent(self, other: PeriodicScale) -> bool:
        """
        Returns True if two scales are set equivalent, i.e. every
        element in this scale has an equivalent element somewhere(!)
        in the other scale (and vice versa).

        Periodic scales of different origin contexts can be
        compared if their origin contexts have the same
        equivalency interval. Set equivalency between scales
        of different contexts is defined as "equality after
        pitch class set normalization"

        :raises IncompatibleOriginContexts: If the other scale
            has a different equivalency interval definition

        :param other: Another periodic scale
        """

        if self.tuning is other.tuning:
            return set(self.pc_indices) == set(other.pc_indices)

        if self.tuning.eq_ratio == other.tuning.eq_ratio:
            n_self = self.pcs_normalized()
            n_other = other.pcs_normalized()
            return n_self == n_other

        raise IncompatibleOriginContexts(
            'Equivalency can only be tested for scales from tunings '
            'with the same equivalency interval'
        )

    def pcs_intersection(self, other: Self) -> Self:
        """
        Returns a scale including all elements whose pitch class
        resides in both of the scales, normalized to the first
        base interval.

        :param other: The other scale
        """

        n_self = self.pcs_normalized()
        n_other = other.pcs_normalized()

        return n_self.intersection(n_other)

    # some variations on the set operations
    # of the parent class

    def intersection(self, other: Self, ignore_bi_index: bool = False) -> Self:
        """
        Returns a new scale including all elements that are included
        in both scales.

        :param other: Another scale of the same origin context
        :param ignore_bi_index: (Optional, default False)
            When set to True elements of the same pitch class
            will be treated the same. For example, if the
            intersection of two scales including C-0 and
            C-1 respectively is calculated, both elements
            will be added to the result

        :raises IncompatibleOriginContexts: If the other scale has a
            different origin context
        """

        if self.origin_context is not other.origin_context:
            raise IncompatibleOriginContexts(
                'Scales do not originate from the same context'
            )

        if not ignore_bi_index:
            return super().intersection(other)

        elements = []

        for element_a in self:
            for element_b in other:
                if element_a.is_equivalent(element_b):
                    elements.append(element_a)
                    elements.append(element_b)

        return self.origin_context.scale(elements)

    def difference(self, other: Self, ignore_bi_index: bool = False) -> Self:
        """
        Returns a scale containing only elements from this
        scale that are NOT present in the other scale

        :param other: Another scale of the same origin context
        :param ignore_bi_index: (Optional, default False)
            When set to True elements of the same pitch class
            will be treated the same. For example, if the
            difference of two scales including C-0 and C-1
            respectively is calculated, C-0 will not be
            inserted into the new scale

        :raises IncompatibleOriginContexts: If the other scale has a
            different origin context
        """

        if self.origin_context is not other.origin_context:
            raise IncompatibleOriginContexts(
                'Scales do not originate from the same context'
            )

        if not ignore_bi_index:
            return super().difference(other)

        elements = []

        for element_a in self:
            for element_b in other:
                if element_a.is_equivalent(element_b):
                    break
            else:
                elements.append(element_a)

        return self.origin_context.scale(elements)

    def symmetric_difference(
        self, other: Self, ignore_bi_index: bool = False
    ) -> Self:
        """
        Returns a scale that includes all the elements
        from both scales that exist in either of them
        but NOT BOTH. This is the complement operation
        of the intersection.

        :param other: Another scale of the same origin context
        :param ignore_bi_index: (Optional, default False)
            When set to True elements of the same pitch class
            will be treated the same. For example, if the
            difference of two scales including C-0 and C-1
            respectively is calculated, C-0 will not be
            inserted into the new scale

        :raises IncompatibleOriginContexts: If the other scale has a
            different origin context
        """

        if self.origin_context is not other.origin_context:
            raise IncompatibleOriginContexts(
                'Scales do not originate from the same context'
            )

        if not ignore_bi_index:
            return super().symmetric_difference(other)

        diff_a = self.difference(other, ignore_bi_index=True)
        diff_b = other.difference(self, ignore_bi_index=True)
        return diff_a.union(diff_b)

    def is_disjoint(self, other: Self, ignore_bi_index: bool = False) -> bool:
        """
        Determines if this scale has any common elements
        with another scale of the same origin context

        :param other: Another scale of the same origin context
        :param ignore_bi_index: (Optional, default False)
            When set to True elements of the same pitch class
            will be treated the same. For example, if one
            scale includes C-0 and another C-1 the scales
            will not be considered disjoint

        :raises IncompatibleOriginContexts: If the other scale originates
            from a different origin context
        """

        intersection = self.intersection(
            other, ignore_bi_index=ignore_bi_index
        )

        return len(intersection) == 0

    def is_subset(
        self, other: Self, proper: bool = False, ignore_bi_index: bool = False
    ) -> bool:
        """
        Determines if all elements in this scale also exist
        in the other scale.

        :param other: Another scale of the same origin context
        :param proper: (Optional, default False) When set
            to True method will return False if the two
            sets are identical
        :param ignore_bi_index: (Optional, default False)
            When set to True elements of the same pitch class
            will be treated the same.

        :raises IncompatibleOriginContexts: If the other scale originates
            from a different origin context
        """

        if not ignore_bi_index:
            return super().is_subset(other, proper=proper)

        intersection = self.intersection(other, ignore_bi_index=True)

        is_subset = self.is_set_equivalent(intersection)

        if not proper:
            return is_subset

        return is_subset and not self.is_set_equivalent(other)

    def is_superset(
        self, other: Self, proper: bool = False, ignore_bi_index: bool = False
    ) -> bool:
        """
        Determines if all elements in the other scale also exist
        in this scale.

        :param other: Another scale of the same origin context
        :param proper: (Optional, default False) When set
            to True method will return False if the two
            sets are identical
        :param ignore_bi_index: (Optional, default False)
            When set to True elements of the same pitch class
            will be treated the same.

        :raises IncompatibleOriginContexts: If the other scale originates
            from a different origin context
        """

        if not ignore_bi_index:
            return super().is_superset(other, proper=proper)

        intersection = self.intersection(other, ignore_bi_index=True)

        is_superset = other.is_set_equivalent(intersection)

        if not proper:
            return is_superset

        return is_superset and not self.is_set_equivalent(other)
