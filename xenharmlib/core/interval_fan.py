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

from abc import ABC
from collections.abc import Sequence
from typing import Generic
from typing import Optional
from typing import overload
from typing import Self
from typing import List
from typing import TypeVar
from typing import Tuple
from types import EllipsisType
from .interval import Interval
from .protocols import Index
from .masks import mask_select
from ..exc import IncompatibleOriginContexts
from .scale import Scale
from .freq_repr import FreqRepr


IntervalT = TypeVar('IntervalT', bound=Interval)
IndexT = TypeVar('IndexT', bound=Index)


class IntervalFan(Sequence[IntervalT], ABC, Generic[IndexT, IntervalT]):
    """
    IntervalSeq is the abstract base class for all interval fan types.
    An interval fan is a list of intervals that all refer to a single
    reference pitch (e.g. in prime limit tunings (1/1, 5/4, 3/2) is
    the interval fan for a pure major triad, all referencing to a
    common point of origin)

    In line with its Sequence superclass interval fans implement
    iteration, the 'in' operator, the == operator, item retrieval with
    [], concatenation with +, repeated self-concatenation with *, searching
    with index, and len().

    Like scale types interval fans also allow partitioning with partial,
    partial_not and partition.

    :param origin_context: An origin context (like a tuning or a notation)
    :param intervals: A sequence of intervals from the origin context
    """

    def __init__(
        self, origin_context, intervals: Optional[Sequence[IntervalT]] = None
    ):

        self._origin_context = origin_context

        if intervals is None:
            _intervals: Sequence[IntervalT] = []
        else:
            _intervals = intervals

        for element in _intervals:
            if element.origin_context is not self.origin_context:
                raise IncompatibleOriginContexts(
                    f'The element {element} does not originate from context '
                    f'{origin_context}. Cannot construct interval fan.'
                )

        self._intervals = _intervals

    @property
    def origin_context(self):
        """
        The origin context from which this interval fan was built
        """
        return self._origin_context

    def __hash__(self):
        return hash(('IntervalFan', ) + tuple(self.frequency_ratios))

    def __contains__(self, o: object) -> bool:
        if isinstance(o, Interval):
            return o in self._intervals
        return False

    def __add__(self, other: Self) -> Self:
        return self.origin_context.interval_fan(list(self) + list(other))

    def __mul__(self, scalar: int) -> Self:
        return self.origin_context.interval_fan(scalar * list(self))

    def __rmul__(self, scalar: int) -> Self:
        return self.origin_context.interval_fan(scalar * list(self))

    @overload
    def __getitem__(self, index_or_slice: int) -> IntervalT: ...

    @overload
    def __getitem__(self, index_or_slice: slice) -> Self: ...

    def __getitem__(self, index_or_slice: int | slice) -> IntervalT | Self:

        if type(index_or_slice) is slice:
            partial = self._intervals[index_or_slice]
            return self.origin_context.interval_fan(partial)

        return self._intervals[index_or_slice]

    def index(self, interval, start=0, end=None, /) -> int:
        """
        Return first index of interval (similar to the index method
        of python's list)

        :param interval: The interval to search for
        :param start: If set method ignores occurences before given
            index (optional, defaults to 0)
        :param end: If set method ignores occurences after given
            index (optional, defaults to end of fan)

        :raises ValueError: If interval was not found in fan
        """

        try:

            if end is None:
                return self._intervals.index(interval, start)

            if start is not None and end is not None:
                return self._intervals.index(interval, start, end)

        except ValueError:
            raise ValueError(f'{interval} is not in fan')

    def __len__(self) -> int:
        return len(self._intervals)

    def __iter__(self):
        return self._intervals.__iter__()

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, IntervalFan):
            return False
        if len(self) != len(other):
            return False
        for a, b in zip(self, other):
            if a != b:
                return False
        return True

    def with_interval(
        self, interval: IntervalT, insert_pos: Optional[int] = None
    ) -> Self:
        """
        Returns a new interval fan containing all intervals
        from this fan and the additional one given as a parameter.
        By default new intervals appear at the end of the fan.

        :param interval: The new interval to be added to the result
        :param insert_pos: The insertion position of the new interval.
            0 will insert the interval at the front, 1 will insert the
            interval at the second position, etc. (optional, default is
            None which results in the value len(fan) + 1)

        :raises IncompatibleOriginContexts: If interval has a different
            origin context than this fan
        """

        if interval.origin_context is not self.origin_context:
            raise IncompatibleOriginContexts(
                "Interval fan and new interval have a different"
                "origin context"
            )

        if insert_pos is None:
            insert_pos = len(self) + 1

        intervals = list(self)
        intervals.insert(insert_pos, interval)
        return self.origin_context.interval_fan(intervals)

    def partial(self, mask_expr: int | Tuple[int | EllipsisType, ...]) -> Self:
        """
        Returns a new fan consisting of a selection of indices
        of this fan. The selection is defined by an index mask
        expression.

        An index mask can be defined as a tuple of consecutive
        indices, e.g. (1, 2, 5) gives a fan including the
        second, third and sixth interval of this one.

        An ellipsis between two indices indicates that all
        indices between them should be selected as well, e.g.
        (1, ..., 5, 9) is equivalent to (1, 2, 3, 4, 5, 9).

        If a mask begins with an ellipsis all indices from
        0 to the next index are added to the selection, e.g.
        (..., 3, 5) is equivalent to (0, 1, 2, 3, 5).

        A mask without a last index is called right-open and will
        select all indices from the last index to the end of the
        fan, for example (2, ...) will select all intervals
        of the fan except the first two.

        If only one interval should be selected a simple integer
        can be used

        :param mask_expr: An index mask expression which defines
            the selection of indices from this fan.
        """

        intervals = []
        for selected, interval in mask_select(mask_expr, self):
            if selected:
                intervals.append(interval)
        return self.origin_context.interval_fan(intervals)

    def partial_not(
        self, mask_expr: int | Tuple[int | EllipsisType, ...]
    ) -> Self:
        """
        Returns a new fan consisting of a selection of indices
        of this fan. The selection will be determined by an
        index mask and will hold all intervals whose index is
        NOT covered by the mask.

        An index mask can be defined as a tuple of consecutive
        indices, e.g. (1, 2, 5) gives a fan including the
        second, third and sixth interval of this one.

        An ellipsis between two indices indicates that all
        indices between them should be selected as well, e.g.
        (1, ..., 5, 9) is equivalent to (1, 2, 3, 4, 5, 9).

        If a mask begins with an ellipsis all indices from
        0 to the next index are added to the selection, e.g.
        (..., 3, 5) is equivalent to (0, 1, 2, 3, 5).

        A mask without a last index is called right-open and will
        select all indices from the last index to the end of the
        fan, for example (2, ...) will select all intervals
        of the fan except the first two.

        If only one interval should be selected a simple integer
        can be used

        :param mask_expr: An index mask expression which defines
            the selection of indices from this fan.
        """

        intervals = []
        for selected, interval in mask_select(mask_expr, self):
            if not selected:
                intervals.append(interval)
        return self.origin_context.interval_fan(intervals)

    def partition(
        self, mask_expr: int | Tuple[int | EllipsisType, ...]
    ) -> Tuple[Self, Self]:
        """
        Partitions the fan into two parts using an index mask.
        The function will return a tuple of two fans with the
        first fan including all indices that are covered by
        the index mask and the second one including all indices
        that are not.

        An index mask can be defined as a tuple of consecutive
        indices, e.g. (1, 2, 5) defines a fan including the
        second, third and sixth interval of this one.

        An ellipsis between two indices indicates that all
        indices between them should be selected as well, e.g.
        (1, ..., 5, 9) is equivalent to (1, 2, 3, 4, 5, 9).

        If a mask begins with an ellipsis all indices from
        0 to the next index are added to the selection, e.g.
        (..., 3, 5) is equivalent to (0, 1, 2, 3, 5).

        A mask without a last index is called right-open and will
        select all indices from the last index to the end of the
        fan, for example (2, ...) will select all intervals of
        the fan except the first two.

        If only one interval should be selected a simple integer
        can be used

        :param mask_expr: An index mask expression which defines
            the selection of indices from this fan.
        """

        intervals_a = []
        intervals_b = []
        for selected, interval in mask_select(mask_expr, self):
            if selected:
                intervals_a.append(interval)
            else:
                intervals_b.append(interval)
        seq_a = self.origin_context.interval_fan(intervals_a)
        seq_b = self.origin_context.interval_fan(intervals_b)
        return seq_a, seq_b

    def inversion(self) -> Self:
        """
        Returns an interval fan with all ascending intervals flipped
        into descending intervals and vice versa.

        .. warning::

           Inversion has a different meaning on intervals and interval
           fans. This function does **not** call the inversion
           function on every interval in the fan but the negation
           (-) function
        """

        return self.origin_context.interval_fan(
            [-interval for interval in self]
        )

    @property
    def frequency_ratios(self):
        """
        An ordered list of frequency ratios present in this fan
        """
        return [interval.frequency_ratio for interval in self]

    @property
    def cents(self) -> List[float]:
        """
        An ordered list of cent values representing the fan
        """
        return [interval.cents for interval in self]

    @property
    def pitch_diffs(self) -> List[IndexT]:
        """
        An ordered list of pitch differences representing the fan
        """
        return [interval.pitch_diff for interval in self]

    def to_scale(self, reference: FreqRepr) -> Scale:
        """
        Returns a scale that has the interval structure of
        this fan, with the given note/pitch being the pitch
        mapped to the unison

        :param reference: A reference note/pitch of the same
            origin context
        """

        if reference.origin_context is not self.origin_context:
            raise IncompatibleOriginContexts(
                f'The element {reference} does not originate from context '
                f'{self.origin_context}. Cannot construct scale.'
            )

        scale_elements = []
        for interval in self:
            current = reference.transpose(interval)
            scale_elements.append(current)

        return self.origin_context.scale(scale_elements)

    def to_seq(self, reference: FreqRepr) -> Scale:
        """
        Returns a pitch/note fan that has the interval
        structure of this fan, with the given note/pitch
        being the pitch mapped to the unison

        :param reference: A reference note/pitch of the same
            origin context
        """

        if reference.origin_context is not self.origin_context:
            raise IncompatibleOriginContexts(
                f'The element {reference} does not originate from context '
                f'{self.origin_context}. Cannot construct sequence.'
            )

        seq_elements = []
        for interval in self:
            current = reference.transpose(interval)
            seq_elements.append(current)

        return self.origin_context.seq(seq_elements)
