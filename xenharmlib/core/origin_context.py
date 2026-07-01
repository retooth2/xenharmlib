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
This module implements the OriginContext class which
is the abstract base class for tunings and notations
"""

from typing import Optional
from typing import Iterable
from typing import Sequence
from typing import Generic
from typing import TypeVar
from abc import ABC
from abc import abstractmethod
from ..exc import IncompatibleOriginContexts
from .freq_repr import FreqRepr
from .freq_repr_seq import FreqReprSeq
from .protocols import Index
from .interval import Interval
from .scale import Scale
from .interval_seq import IntervalSeq
from .interval_fan import IntervalFan

IndexT = TypeVar('IndexT', bound=Index)
FreqReprT = TypeVar('FreqReprT', bound=FreqRepr)
IntervalT = TypeVar('IntervalT', bound=Interval)
ScaleT = TypeVar('ScaleT', bound=Scale)
IntervalSeqT = TypeVar('IntervalSeqT', bound=IntervalSeq)
FreqReprSeqT = TypeVar('FreqReprSeqT', bound=FreqReprSeq)
IntervalFanT = TypeVar('IntervalFanT', bound=IntervalFan)


class OriginContext(
    ABC,
    Generic[
        IndexT,
        FreqReprT,
        IntervalT,
        ScaleT,
        IntervalSeqT,
        IntervalFanT,
        FreqReprSeqT,
    ],
):
    """
    OriginContext is the abstract base class for both tunings and notations.
    It defines a unified interface for collection and interval builder
    methods as well as an interface for a defined "zero element" which
    is used as a reference point for other objects.

    OriginContext does not define an interface for the builder method
    of the FreqRepr object (such as pitch or note) as the name and the
    function signature vary greatly from context to context (e.g. one
    dimensional tunings demand an integer as construction argument,
    more-dimensional tunings a vector, notes in periodic tunings
    mostly demand a string symbol and a base interval index, etc)
    """

    def __init__(
        self,
        *,
        freq_repr_cls: type[FreqReprT],
        interval_cls: type[IntervalT],
        scale_cls: type[ScaleT],
        interval_seq_cls: type[IntervalSeqT],
        interval_fan_cls: type[IntervalFanT],
        freq_repr_seq_cls: type[FreqReprSeqT],
    ):

        self._freq_repr_cls = freq_repr_cls
        self._interval_cls = interval_cls
        self._scale_cls = scale_cls
        self._interval_seq_cls = interval_seq_cls
        self._interval_fan_cls = interval_fan_cls
        self._freq_repr_seq_cls = freq_repr_seq_cls

    @property
    @abstractmethod
    def zero_index(self) -> IndexT:
        """
        The zero index is a reference point, in tunings with integer
        indexing this is 0, in tunings with lattice indexing this is
        typically the zero-vector.
        """

    @property
    @abstractmethod
    def zero_element(self) -> FreqReprT:
        """
        The zero element is a reference point, in one-dimensional tunings
        it is the element with index 0, in western notation typically C-0,
        etc
        """

    @property
    def zero_diff(self) -> IndexT:
        """
        The zero diff is a reference point, in tunings with integer
        indexing this is 0, in tunings with lattice indexing this is
        typically the zero-vector.
        """
        return self.interval(self.zero_element, self.zero_element).pitch_diff

    @property
    def unison_interval(self) -> IntervalSeqT:
        """
        The unison interval is a reference point, in one-dimensional tunings
        it is the element with pitch diff 0, in western notation typically
        P1, etc.
        """
        return self.interval(self.zero_element, self.zero_element)

    def interval(self, source: FreqReprT, target: FreqReprT) -> IntervalT:
        """
        Returns an interval having the interval type
        this origin context was configured with

        :raises IncompatibleOriginContexts: If either source or
            target have a different origin context than this one

        :param source: The source of the interval
        :param target: The target of the interval
        """

        # .from_source_and_target can only make sure that
        # the two elements are from the same origin context,
        # not that they are from THIS context. consequently
        # we need to check it here

        for freq_repr in [source, target]:
            if freq_repr.origin_context is not self:
                raise IncompatibleOriginContexts(
                    'At least one in the given interval pair does not '
                    'originate from this origin context'
                )

        return self._interval_cls.from_source_and_target(source, target)

    def diff_interval(self, pitch_diff: IndexT) -> IntervalT:
        """
        Returns an interval the size of a given pitch index difference.

        :param pitch_diff: The pitch index difference
        """

        a = self.zero_element
        b = a.transpose(pitch_diff)
        return a.interval(b)

    # FIXME: scale and interval_seq have Iterable and Sequence requirement
    # respectively, should be uniform

    def scale(self, elements: Optional[Iterable[FreqReprT]] = None) -> ScaleT:
        """
        Returns a scale having the scale type this origin context
        was configured with

        :raises IncompatibleOriginContexts: If at least one given
            element has a different origin context than this one

        :param elements: A list of frequency representations
            originating from this context
        """

        return self._scale_cls(self, elements)

    def interval_seq(
        self, intervals: Optional[Sequence[IntervalT]] = None
    ) -> IntervalSeqT:
        """
        Returns an interval sequence having the interval sequence type
        this origin context was configured with

        :raises IncompatibleOriginContexts: If at least one given
            element has a different origin context than this one

        :param intervals: A list of intervals originating from this
            context
        """

        return self._interval_seq_cls(self, intervals)

    def interval_fan(
        self, intervals: Optional[Sequence[IntervalT]] = None
    ) -> IntervalSeqT:
        """
        Returns an interval fan having the interval fan type
        this origin context was configured with

        :raises IncompatibleOriginContexts: If at least one given
            element has a different origin context than this one

        :param intervals: A list of intervals originating from this
            context
        """

        return self._interval_fan_cls(self, intervals)

    def seq(
        self, elements: Optional[Sequence[FreqReprT]] = None
    ) -> FreqReprSeqT:
        """
        Returns a pitch/note sequence

        :raises IncompatibleOriginContexts: If at least one given
            element has a different origin context than this one

        :param elements: A list of elements originating from this
            context
        """

        return self._freq_repr_seq_cls(self, elements)

    def diff_interval_seq(
        self, pitch_diffs: Optional[Sequence[IndexT]] = None
    ) -> IntervalSeqT:
        """
        Returns an interval sequence from an iterable of pitch index
        differences, for example:

        >>> from xenharmlib import EDOTuning
        >>> edo12 = EDOTuning(12)
        >>> major_chord = edo12.diff_interval_seq([4, 3])
        >>> minor_chord = edo12.diff_interval_seq([3, 4])

        :param pitch_diffs: An iterable containing pitch index
            differences
        """

        if not pitch_diffs:
            return self.interval_seq()

        intervals = [
            self.diff_interval(pitch_diff) for pitch_diff in pitch_diffs
        ]

        return self.interval_seq(intervals)

    def diff_interval_fan(
        self, pitch_diffs: Optional[Sequence[IndexT]] = None
    ) -> IntervalFanT:
        """
        Returns an interval fan from an iterable of pitch index
        differences, for example:

        >>> from xenharmlib import EDOTuning
        >>> edo12 = EDOTuning(12)
        >>> major_chord = edo12.diff_interval_fan([4, 7])
        >>> minor_chord = edo12.diff_interval_fan([3, 7])

        :param pitch_diffs: An iterable containing pitch index
            differences
        """

        if not pitch_diffs:
            return self.interval_fan()

        intervals = [
            self.diff_interval(pitch_diff) for pitch_diff in pitch_diffs
        ]

        return self.interval_fan(intervals)
