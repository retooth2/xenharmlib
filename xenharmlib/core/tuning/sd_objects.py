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

from bisect import insort
from typing import Self
from typing import Optional
from typing import List
from typing import TypeVar
from warnings import warn
from ..frequencies import Frequency
from ..frequencies import FrequencyRatio
from ..objects import FreqRepr
from ..objects import Scale
from ..objects import Interval
from ..objects import IntervalSeq
from ...exc import IncompatibleOriginContexts


class SDPitch(FreqRepr):
    """
    In its most basic form, a Pitch is a tuple of a pitch index
    (an integer value) and a tuning that interprets this index
    as a frequency.

    Pitch creates a total ordering on all pitches according
    to their frequency. This means you can sort pitches in lists
    (e.g. from lowest frequency to highest frequency). You can
    also compare pitches, even across different tunings:

    >>> from xenharmlib import EDOTuning
    >>> edo12 = EDOTuning(12)
    >>> edo31 = EDOTuning(31)
    >>> edo31.pitch(1) < edo12.pitch(1)
    True
    >>> edo31.pitch(31) == edo12.pitch(12)
    True

    :param tuning: The tuning to which this pitch belongs
    :param frequency: The frequency this pitch represents
    :param pitch_index: An integer denoting the pitch (with
        0 being the first pitch, 1 being the second, etc)
    """

    def __init__(self, tuning, frequency: Frequency, pitch_index: int):
        super().__init__(tuning, frequency)
        self._pitch_index = pitch_index
        self._tuning = tuning

    def __hash__(self):
        return hash(self._pitch_index)

    @property
    def pitch_index(self) -> int:
        """
        The pitch index of this object
        """
        return self._pitch_index

    def __eq__(self, other) -> bool:
        if not isinstance(other, FreqRepr):
            return False
        if (
            isinstance(other, SDPitch)
            and self.origin_context is other.origin_context
        ):
            return self.pitch_index == other.pitch_index
        return self.frequency == other.frequency

    def __lt__(self, other) -> bool:
        if not isinstance(other, FreqRepr):
            return NotImplemented
        if (
            isinstance(other, SDPitch)
            and self.origin_context is other.origin_context
        ):
            return self.pitch_index < other.pitch_index
        return self.frequency < other.frequency

    @property
    def tuning(self):
        """
        The origin tuning of this pitch
        """
        return self._tuning

    # arithmetic

    def __add__(self, other):
        if self.tuning is not other.tuning:
            raise IncompatibleOriginContexts(
                'Pitches must originate from the same tuning context'
            )
        return self.tuning.pitch(self.pitch_index + other.pitch_index)

    def __sub__(self, other):
        if self.tuning is not other.tuning:
            raise IncompatibleOriginContexts(
                'Pitches must originate from the same tuning context'
            )
        return self.tuning.pitch(self.pitch_index - other.pitch_index)

    def __mul__(self, factor: int):
        return self.tuning.pitch(self.pitch_index * factor)

    def __rmul__(self, factor: int):
        return self.tuning.pitch(self.pitch_index * factor)

    def __repr__(self):
        return (
            f'{self.__class__.__name__}('
            f'{self.pitch_index}, '
            f'{self.tuning.name})'
        )

    @property
    def short_repr(self) -> str:
        return f'{self.pitch_index}'

    def transpose(self, diff: int | SDPitchInterval) -> SDPitch:
        """
        Transposes the pitch to a different one

        :param diff: The difference from this pitch. Can be
            either an integer (positive for upward movement,
            negative for downward movement) or a pitch
            interval
        """

        if isinstance(diff, SDPitchInterval):
            transposed_index = self.pitch_index + diff.pitch_diff
        else:
            transposed_index = self.pitch_index + diff

        return self.tuning.pitch(transposed_index)

    def retune(self, tuning) -> SDPitch:
        """
        Approximates this pitch in a different
        tuning
        """

        return tuning.get_approx_pitch(self.frequency)


PitchT = TypeVar('PitchT', bound=SDPitch)


class SDPitchInterval(Interval[PitchT]):
    """
    The most abstract form of an interval of two pitches.
    Implements conversion functions to frequency ratios
    and a total ordering based on the calculated ratios:

    >>> from xenharmlib import EDOTuning
    >>> edo31 = EDOTuning(31)
    >>> pitch_a = edo31.pitch(4)
    >>> pitch_b = edo31.pitch(8)
    >>> pitch_c = edo31.pitch(10)
    >>> i_ab = pitch_a.interval(pitch_b)
    >>> i_ac = pitch_a.interval(pitch_c)
    >>> i_ab < i_ac
    True

    **A caveat**: Intervals are considered directional in xenharmlib
    so the order of pitches from which the interval is created
    is important

    :param tuning: The tuning associated with this
        interval
    :param frequency_ratio: The frequency ratio of this interval
    :param pitch_diff: An integer that defines the
        number of steps this interval encompasses
        (a positive integer means 'upward steps',
        while a negative one means 'downward steps')
    :param ref_pitch: A reference pitch for the pitch
        difference. This is necessary for tunings that
        are not equal step. In just intonation tunings
        frequency ratios may vary depending on the
        original pitches used to construct the interval,
        even if their pitch index difference is the same
    """

    def __init__(
        self,
        tuning,
        frequency_ratio: FrequencyRatio,
        pitch_diff: int,
        ref_pitch: PitchT,
    ):
        super().__init__(tuning, frequency_ratio)
        self._pitch_diff = pitch_diff
        self.ref_pitch = ref_pitch
        self.tuning = tuning

    @property
    def pitch_diff(self) -> int:
        return self._pitch_diff

    def __abs__(self) -> Self:
        """
        Returns the absolute of this pitch interval. On downwards
        interval it returns an upwards interval of the same absolute
        size. On upwards intervals it acts as the identity function.
        """

        if self.pitch_diff >= 0:
            return self

        target_pitch = self.ref_pitch.transpose(self.pitch_diff)

        return self.tuning.interval(target_pitch, self.ref_pitch)

    @classmethod
    def from_pitches(cls, pitch_a: PitchT, pitch_b: PitchT) -> Self:
        """
        .. deprecated:: 0.2.0
           Use :py:meth:`from_source_and_target` instead.

        Constructs an interval out of two pitches of the same tuning.
        If the second pitch is lower than the first pitch the Interval
        will have a negative pitch difference

        :raises IncompatibleOriginContexts: If pitches come
            from different tuning systems

        :param pitch_a: The first (or reference) pitch
        :param pitch_b: The second (or target) pitch
        """
        warn(
            f'{cls.__name__}.from_pitches is deprecated and will be '
            f'removed in 1.0.0. Please use '
            f'{cls.__name__}.from_source_and_target instead.',
            DeprecationWarning,
            stacklevel=2,
        )
        return cls.from_source_and_target(pitch_a, pitch_b)

    @classmethod
    def from_source_and_target(cls, source: PitchT, target: PitchT) -> Self:
        """
        Constructs an interval out of two pitches of the same tuning.
        If the second pitch is lower than the first pitch the Interval
        will have a negative pitch difference

        :raises IncompatibleOriginContexts: If pitches come
            from different tuning systems

        :param source: The starting point of the interval
        :param target: The end point of the interval
        """

        if source.tuning is not target.tuning:
            raise IncompatibleOriginContexts(
                'Pitches must originate from the same tuning context'
            )

        tuning = source.tuning
        pitch_diff = target.pitch_index - source.pitch_index
        frequency_ratio = target.frequency / source.frequency

        return cls(
            tuning,
            frequency_ratio,
            pitch_diff,
            source,
        )

    def __repr__(self):
        return (
            f'{self.__class__.__name__}({self.pitch_diff}, {self.tuning.name})'
        )

    @property
    def short_repr(self) -> str:
        return f'{self.pitch_diff}'


class SDPitchScale(Scale[PitchT]):
    """
    The base class of all pitch scales. Implements list and set
    operations, transposition, retuning, etc.

    A pitch scale is an ordered set of unique pitches in a given tuning.
    The uniqueness property means that there are no duplicate pitches.
    However other than in the popular use of the word 'scale' the pitch
    scale object in xenharmlib is not limited to one base interval in
    periodic tunings. (e.g. C-0 and C-1 are considered distinct)
    This has a couple of advantages, e.g. that the scale object can be
    used more generally.

    Pitch scales have both a list and a set quality to them.
    Similar to lists they have an item order, support iteration,
    positional item retrieval, and slicing. At the same time scales
    support set operations like intersection, union, symmetric
    difference, etc.

    PitchScale (or, respectively, its subclasses) are built by
    the tunings pitch_scale builder method:

    >>> from xenharmlib import EDOTuning
    >>> edo31 = EDOTuning(31)
    >>> scale = edo31.scale(
    ...     [edo31.pitch(4), edo31.pitch(6), edo31.pitch(9)]
    ... )

    Every pitch will be automatically sorted in its place.
    The order of the scale is ascending (First lower pitch, then
    higher pitch)

    PitchScale objects support most of the typical list operations:

    >>> for pitch in scale:
    ...     print(pitch)
    EDOPitch(4, 31-EDO)
    EDOPitch(6, 31-EDO)
    EDOPitch(9, 31-EDO)

    >>> scale[1]
    EDOPitch(6, 31-EDO)

    >>> scale[1:-1]
    EDOPitchScale([6], 31-EDO)

    The 'in' operator accepts both pitches and pitch intervals

    >>> p = edo31.pitch(4)
    >>> p in scale
    True
    >>> p.interval(edo31.pitch(2)) in scale
    True

    In regards to intervals, it even works across tunings

    >>> edo12 = EDOTuning(12)
    >>> edo24 = EDOTuning(24)
    >>> edo12_fifth = edo12.pitch(0).interval(edo12.pitch(7))
    >>> edo24_scale = edo24.scale(edo24.pitch_range(24))
    >>> edo12_fifth in edo24_scale
    True

    In addition similar operations to the native python sets are
    available (with slightly different naming and additional method
    arguments):

    * union
    * intersection
    * difference
    * symmetric_difference
    * is_disjoint
    * is_subset
    * is_superset
    """

    def __init__(self, tuning, pitches: Optional[List[PitchT]] = None):
        super().__init__(tuning, pitches)
        self.tuning = tuning

    @property
    def is_zero_normalized(self) -> bool:
        """
        Returns True if this function is zero normalized, meaning
        that the first element of the scale is identical to the
        pitch with index 0
        """

        if len(self) == 0:
            raise ValueError(
                'is_zero_normalized is not defined on empty scale'
            )

        return self[0] == self.tuning.pitch(0)

    def add_pitch(self, pitch: PitchT):
        """
        .. deprecated:: 0.2.0
           objects in xenharmlib are supposed to be immutable

        Inserts a new pitch into the scale at
        the right position

        :raises IncompatibleOriginContexts: If the pitch has a different
            tuning than this scale.

        :param pitch: The new pitch
        """
        warn(
            f'{self.__class__.__name__}.add_pitch is deprecated and '
            f'will be removed in 1.0.0. As per design philosophy '
            f'scales should be immutable. To gradually construct '
            f'a scale by single elements use .with_element',
            DeprecationWarning,
            stacklevel=2,
        )

        if pitch.tuning is not self.tuning:
            raise IncompatibleOriginContexts(
                'Pitch must originate from the same tuning '
                'context as the scale'
            )

        if pitch not in self._sorted_elements:
            insort(self._sorted_elements, pitch)

    def add_pitch_index(self, pitch_index: int):
        """
        .. deprecated:: 0.2.0
           objects in xenharmlib are supposed to be immutable

        Inserts a new pitch into the scale denoted
        by its pitch index

        :param pitch_index: Index of the pitch
        """
        warn(
            f'{self.__class__.__name__}.add_pitch_index is deprecated and '
            f'will be removed in 1.0.0. As per design philosophy '
            f'scales should be immutable. To gradually construct '
            f'a scale by single elements use .with_element',
            DeprecationWarning,
            stacklevel=2,
        )

        pitch = self.tuning.pitch(pitch_index)
        self.add_pitch(pitch)

    # builder methods

    @classmethod
    def from_pitch_indices(cls, pitch_indices: List[int], tuning) -> Self:
        """
        Creates a scale from a list of pitch
        indices

        :param pitch_indices: A list of pitch indices in
            any order.
        :param tuning: The tuning through which these indices
            should be interpreted
        """
        warn(
            f'{cls.__name__}.from_pitch_indices is deprecated and '
            f'will be removed in 1.0.0. Please use the .index_scale '
            f'method of the tuning',
            DeprecationWarning,
            stacklevel=2,
        )

        pitches = []
        for pitch_index in pitch_indices:
            pitches.append(tuning.pitch(pitch_index))

        return tuning.scale(pitches)

    # the obligatory __repr__

    def __repr__(self):
        return (
            f'{self.__class__.__name__}('
            f'{self.pitch_indices}, '
            f'{self.tuning.name})'
        )

    # operations that are possible on single pitches
    # that can also be applied to collections of
    # pitches

    @property
    def pitch_indices(self) -> List[int]:
        """
        A list of the ordered pitch indices
        present in this scale
        """
        return [pitch.pitch_index for pitch in self]

    def to_pitch_intervals(self) -> List[Interval[PitchT]]:
        """
        .. deprecated:: 0.2.0
           Use :py:meth:`to_intervals` instead.

        Returns this scale represented as a list of pitch intervals
        """
        warn(
            f'{self.__class__.__name__}.to_pitch_intervals is deprecated and '
            f'will be removed in 1.0.0. Please use '
            f'{self.__class__.__name__}.to_intervals instead.',
            DeprecationWarning,
            stacklevel=2,
        )
        return self.to_intervals()

    def transpose(self, diff: int | SDPitchInterval[PitchT]) -> Self:
        """
        Transposes the scale upwards or downwards

        :param diff: The difference from this pitch. Can be
            either an integer (positive for upward movement,
            negative for downward movement) or a pitch
            interval
        """

        transposed = []
        for pitch in self:
            transposed.append(pitch.transpose(diff))

        return self.tuning.scale(transposed)

    def retune(self, tuning) -> SDPitchScale:
        """
        Returns a scale retuned into a different tuning by
        approximating every pitch in the scale with a pitch
        from the target tuning.

        **A caveat**: Since pitch scales are a structure of sorted unique
        pitches this method may produce a scale with a smaller size than
        the original because two pitches in this tuning can be approximated
        to the same pitch in the target tuning.

        :param tuning: The target tuning
        """

        pitches = []

        for pitch in self:
            retuned_pitch = pitch.retune(tuning)
            pitches.append(retuned_pitch)

        return tuning.scale(pitches)


PitchIntervalT = TypeVar('PitchIntervalT', bound=SDPitchInterval)


class SDPitchIntervalSeq(IntervalSeq[PitchIntervalT]):
    """
    Base class for all sequences of pitch intervals.
    Interval sequences can be understood as "abstract scales" (for example
    the minor scale *as such*, instead of C minor). Interval sequences have
    multiple applications from templating to structure discovery.

    In line with its Sequence superclass pitch interval sequences implement
    iteration, the 'in' operator, the == operator, item retrieval with
    [], concatenation with +, repeated self-concatenation with *, searching
    with index, and len().

    Like scale types pitch interval sequences also allow partitioning with
    partial, partial_not and partition.

    :param tuning: The tuning this pitch interval sequence originates from
    :param intervals: A sequence of pitch intervals
    """

    def __init__(
        self,
        tuning,
        intervals: Optional[List[PitchIntervalT]] = None
    ):
        super().__init__(tuning, intervals)
        self.tuning = tuning

    def __repr__(self):
        return (
            f'{self.__class__.__name__}('
            f'{self.pitch_diffs}, '
            f'{self.tuning.name})'
        )
