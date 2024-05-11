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
"""

from __future__ import annotations

from bisect import insort
from typing import TypeVar
from typing import Generic
from typing import List
from typing import Self
from typing import Union
from typing import Optional
from .pitch import Pitch
from .pitch import PeriodicPitch
from .pitch import EDPitch
from .pitch import PitchInterval
from .frequencies import Frequency
from ..exc import IncompatibleTunings
from .protocols import HasFrequency
from .protocols import HasFrequencyRatio

PitchT = TypeVar('PitchT', bound=Pitch)


class PitchScale(Generic[PitchT]):
    """
    The base class of all pitch scales. Implements list and set
    operations, transposition, retuning, etc.

    PitchScale (or, respectively, its subclasses) are built by
    the tunings pitch_scale builder method:

    >>> from xenharmlib import EDOTuning
    >>> edo31 = EDOTuning(31)
    >>> scale = edo31.pitch_scale(
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
    >>> edo24_scale = edo24.pitch_scale(edo24.pitch_range(24))
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
        self.tuning = tuning
        self._sorted_pitches: List[PitchT] = []
        if pitches is not None:
            for pitch in pitches:
                self.add_pitch(pitch)

    def add_pitch(self, pitch: PitchT):
        """
        Inserts a new pitch into the scale at
        the right position

        :raises IncompatibleTunings: If the pitch has a different
            tuning than this scale.

        :param pitch: The new pitch
        """

        if pitch.tuning is not self.tuning:
            raise IncompatibleTunings(
                'Pitch must originate from the same tuning '
                'context as the scale'
            )

        if pitch not in self._sorted_pitches:
            insort(self._sorted_pitches, pitch)

    def add_pitch_index(self, pitch_index: int):
        """
        Inserts a new pitch into the scale denoted
        by its pitch index

        :param pitch_index: Index of the pitch
        """

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

        scale = cls(tuning=tuning)

        for pitch_index in pitch_indices:
            scale.add_pitch_index(pitch_index)

        return scale

    def __eq__(self, other: object):

        if not isinstance(other, PitchScale):
            return False

        return list(self) == list(other)

    # in this section we implement all the magic methods
    # s so the scale behaves similar to a list

    def __len__(self):
        return len(self._sorted_pitches)

    def __iter__(self):
        return self._sorted_pitches.__iter__()

    def __getitem__(self, index_or_slice: Union[int, slice]):

        if type(index_or_slice) is slice:
            return self.tuning.pitch_scale(
                self._sorted_pitches[index_or_slice]
            )

        return self._sorted_pitches[index_or_slice]

    def __contains__(self, object: object) -> bool:

        if isinstance(object, HasFrequency):
            return object in self._sorted_pitches

        elif isinstance(object, HasFrequencyRatio):
            for pitch_a in self._sorted_pitches:
                for pitch_b in self._sorted_pitches:
                    interval_u = pitch_a.interval(pitch_b)
                    if interval_u == object:
                        return True
                    interval_d = pitch_b.interval(pitch_a)
                    if interval_d == object:
                        return True

        # TODO: should Frequencies and FrequencyRatios also
        # allowed to be checked with in operator?

        return False

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
    def frequencies(self) -> List[Frequency]:
        return [pitch.frequency for pitch in self]

    @property
    def pitch_indices(self) -> List[int]:
        """
        A list of the ordered pitch indices
        present in this scale
        """
        return [pitch.pitch_index for pitch in self._sorted_pitches]

    def to_pitch_intervals(self) -> List[PitchInterval]:
        """
        Returns this scale represented as a list of pitch intervals
        """

        intervals = []
        for i in range(0, len(self) - 1):
            intervals.append(self[i].interval(self[i + 1]))
        return intervals

    def transpose(self, diff: Union[int, PitchInterval]) -> Self:
        """
        Transposes the scale upwards or downwards

        :param diff: The difference from this pitch. Can be
            either an integer (positive for upward movement,
            negative for downward movement) or a pitch
            interval
        """

        transposed = []
        for pitch in self._sorted_pitches:
            transposed.append(pitch.transpose(diff))

        return self.tuning.pitch_scale(transposed)

    def retune(self, tuning) -> PitchScale:
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

        retuned_scale = tuning.pitch_scale()

        for pitch in self:
            retuned_pitch = pitch.retune(tuning)
            retuned_scale.add_pitch(retuned_pitch)

        return retuned_scale

    # set operations

    def union(self, other: Self) -> Self:
        """
        Returns a new scale including all pitches from
        this scale as well as the other

        :param other: Another scale of the same tuning

        :raises IncompatibleTunings: If the other scale has a
            different tuning
        """

        if self.tuning is not other.tuning:
            raise IncompatibleTunings(
                'Scales must originate from the same tuning context'
            )

        scale = self.tuning.pitch_scale()

        for pitch in self:
            scale.add_pitch(pitch)

        for pitch in other:
            scale.add_pitch(pitch)

        return scale

    def intersection(self, other: Self) -> Self:
        """
        Returns a new scale including all pitches
        that are included in both scales.

        :param other: Another scale of the same tuning

        :raises IncompatibleTunings: If the other scale has a
            different tuning
        """

        if self.tuning is not other.tuning:
            raise IncompatibleTunings(
                'Scales must originate from the same tuning context'
            )

        scale = self.tuning.pitch_scale()

        for pitch_a in self:
            for pitch_b in other:
                if pitch_a == pitch_b:
                    scale.add_pitch(pitch_a)

        return scale

    def difference(self, other: Self) -> Self:
        """
        Returns a scale containing only pitches from this
        scale that are NOT present in the other scale

        :param other: Another scale of the same tuning

        :raises IncompatibleTunings: If the other scale has a
            different tuning
        """

        if self.tuning is not other.tuning:
            raise IncompatibleTunings(
                'Scales must originate from the same tuning context'
            )

        scale = self.tuning.pitch_scale()

        for pitch_a in self:
            for pitch_b in other:
                if pitch_a == pitch_b:
                    break
            else:
                scale.add_pitch(pitch_a)

        return scale

    def symmetric_difference(self, other: Self) -> Self:
        """
        Returns a scale that includes all the pitches
        from both scales that exist in either of them
        but NOT BOTH. This is the complement operation
        of the intersection.

        :param other: Another scale of the same tuning

        :raises IncompatibleTunings: If the other scale has a
            different tuning
        """

        if self.tuning is not other.tuning:
            raise IncompatibleTunings(
                'Scales must originate from the same tuning context'
            )

        diff_a = self.difference(other)
        diff_b = other.difference(self)
        return diff_a.union(diff_b)

    def is_disjoint(self, other: Self) -> bool:
        """
        Determines if this scale has any common pitches
        with another scale of the same tuning

        :param other: Another scale of the same tuning

        :raises IncompatibleTunings: If the other scale has a
            different tuning
        """

        intersection = self.intersection(other)

        return len(intersection) == 0

    def is_subset(self, other: Self, proper: Optional[bool] = False) -> bool:
        """
        Determines if all pitches in this scale also exist
        in the other scale.

        :param other: Another scale of the same tuning
        :param proper: (Optional, default False) When set
            to True method will return False if the two
            sets are identical

        :raises IncompatibleTunings: If the other scale has a
            different tuning
        """

        intersection = self.intersection(other)

        is_subset = self == intersection

        if not proper:
            return is_subset

        return is_subset and not (self == other)

    def is_superset(self, other: Self, proper: Optional[bool] = False) -> bool:
        """
        Determines if all pitches in the other scale also exist
        in this scale.

        :param other: Another scale of the same tuning
        :param proper: (Optional, default False) When set
            to True method will return False if the two
            sets are identical

        :raises IncompatibleTunings: If the other scale has a
            different tuning
        """

        intersection = self.intersection(other)

        is_superset = other == intersection

        if not proper:
            return is_superset

        return is_superset and not (self == other)


PeriodicPitchT = TypeVar('PeriodicPitchT', bound=PeriodicPitch)


class PeriodicPitchScale(PitchScale[PeriodicPitchT]):
    """
    Pitch scale class for periodic tunings. Implements
    operations like rotation and customized set operations
    (for when you want to treat equivalent pitches the same
    as equal pitches). It also implements normalization methods.
    """

    # normalization methods

    def pcs_normalized(self) -> Self:
        """
        Returns a normalized version of this scale where
        all the pitches of the scale are put into the first
        base interval of the tuning

        Note: If the original scale has equivalent pitch pairs
        the normalized scale will be smaller in cardinality.
        """

        n_scale = self.tuning.pitch_scale()

        for pitch in self._sorted_pitches:
            n_pitch = self.tuning.pitch(pitch.pc_index)
            n_scale.add_pitch(n_pitch)

        return n_scale

    def pcs_complement(self) -> Self:
        """
        Normalizes this scale to the first base interval
        and returns the complement (that is: a scale of
        all pitches NOT in this scale) as a normalized
        scale
        """

        n_scale = self.pcs_normalized()

        complement = self.tuning.pitch_scale()

        full_scale = self.tuning.pitch_scale(
            self.tuning.pitch_range(len(self.tuning))
        )

        for pitch in full_scale:
            if pitch not in n_scale:
                complement.add_pitch(pitch)

        return complement

    # typical scale operations in music theory

    def rotated_up(self) -> Self:
        """
        Create a new scale by transposing the lowest pitch
        upwards until it is above the highest pitch
        """

        rotated_scale = self.tuning.pitch_scale(self[1:])

        pitch = self.tuning.pitch(
            self[0].pc_index + self[-1].bi_index * len(self.tuning)
        )

        if pitch < rotated_scale[-1]:
            pitch = pitch.transpose_bi_index(1)

        rotated_scale.add_pitch(pitch)
        return rotated_scale

    def rotated_down(self) -> Self:
        """
        Create a new scale by transposing the highest pitch
        downwards until it is below the lowest pitch
        """

        rotated_scale = self.tuning.pitch_scale(self[:-1])

        bi_diff = self[-1].bi_index - self[0].bi_index

        pitch = self.tuning.pitch(
            self[-1].pitch_index - bi_diff * len(self.tuning)
        )

        if pitch > rotated_scale[0]:
            pitch = pitch.transpose_bi_index(-1)

        rotated_scale.add_pitch(pitch)
        return rotated_scale

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

    @property
    def pc_indices(self) -> List[int]:
        """
        Returns a list of pitch class indices in
        the order they appear in this scale. This can
        include duplicate items if the list has two
        pitches of the same pitch class
        """
        return [pitch.pc_index for pitch in self._sorted_pitches]

    def pcs_intersection(self, other: Self) -> Self:
        """
        Returns a scale including all pitches whose pitch class
        resides in both of the scales, normalized to the first
        base interval

        This is a shortcut for calling intersection with the ignore
        base interval flag and subsequent base interval normalization

        :param other: The other scale
        """

        n_self = self.pcs_normalized()
        n_other = other.pcs_normalized()

        return n_self.intersection(n_other)

    # some variations on the set operations
    # of the parent class

    def intersection(
        self, other: Self, ignore_bi_index: Optional[bool] = False
    ) -> Self:
        """
        Returns a new scale including all pitches
        that are included in both scales.

        :param other: Another scale of the same tuning
        :param ignore_bi_index: (Optional, default False)
            When set to True pitches of the same pitch class
            will be treated the same. For example, if the
            intersection of two scales including C-0 and
            C-1 respectively is calculated, both pitches
            will be added to the result

        :raises IncompatibleTunings: If the other scale has a
            different tuning
        """

        if self.tuning is not other.tuning:
            raise IncompatibleTunings(
                'Scales must originate from the same tuning context'
            )

        if not ignore_bi_index:
            return super().intersection(other)

        scale = self.tuning.pitch_scale()

        for pitch_a in self:
            for pitch_b in other:
                if pitch_a.is_equivalent(pitch_b):
                    scale.add_pitch(pitch_a)
                    scale.add_pitch(pitch_b)

        return scale

    def difference(
        self, other: Self, ignore_bi_index: Optional[bool] = False
    ) -> Self:
        """
        Returns a scale containing only pitches from this
        scale that are NOT present in the other scale

        :param other: Another scale of the same tuning
        :param ignore_bi_index: (Optional, default False)
            When set to True pitches of the same pitch class
            will be treated the same. For example, if the
            difference between two scales including C-0 and C-1
            respectively is calculated, C-0 will not be
            inserted into the new scale

        :raises IncompatibleTunings: If the other scale has a
            different tuning
        """

        if self.tuning is not other.tuning:
            raise IncompatibleTunings(
                'Scales must originate from the same tuning context'
            )

        if not ignore_bi_index:
            return super().difference(other)

        scale = self.tuning.pitch_scale()

        for pitch_a in self:
            for pitch_b in other:
                if pitch_a.is_equivalent(pitch_b):
                    break
            else:
                scale.add_pitch(pitch_a)

        return scale

    def symmetric_difference(
        self, other: Self, ignore_bi_index: Optional[bool] = False
    ) -> Self:
        """
        Returns a scale that includes all the pitches
        from both scales that exist in either of them
        but NOT BOTH. This is the complement operation
        of the intersection.

        :param other: Another scale of the same tuning
        :param ignore_bi_index: (Optional, default False)
            When set to True pitches of the same pitch class
            will be treated the same. For example, if the
            difference of two scales including C-0 and C-1
            respectively is calculated, both C-0 and C-1
            will not be inserted into the new scale

        :raises IncompatibleTunings: If the other scale has a
            different tuning
        """

        if self.tuning is not other.tuning:
            raise IncompatibleTunings(
                'Scales must originate from the same tuning context'
            )

        if not ignore_bi_index:
            return super().symmetric_difference(other)

        diff_a = self.difference(other, ignore_bi_index=True)
        diff_b = other.difference(self, ignore_bi_index=True)
        return diff_a.union(diff_b)

    def is_disjoint(
        self, other: Self, ignore_bi_index: Optional[bool] = False
    ) -> bool:
        """
        Determines if this scale has any common pitches
        with another scale of the same tuning

        :param other: Another scale of the same tuning
        :param ignore_bi_index: (Optional, default False)
            When set to True pitches of the same pitch class
            will be treated the same. For example, if one
            scale includes C-0 and the other includes C-1
            the scales will not be considered disjoint

        :raises IncompatibleTunings: If the other scale has a
            different tuning
        """

        intersection = self.intersection(
            other, ignore_bi_index=ignore_bi_index
        )

        return len(intersection) == 0

    def is_equivalent(self, other: Self) -> bool:
        """
        Determines if this scale and another scale have
        exactly the same pitch classes

        :param other: Another scale of the same tuning

        :raises IncompatibleTunings: If the other scale has a
            different tuning
        """

        if self.tuning is not other.tuning:
            raise IncompatibleTunings(
                'Scales must originate from the same tuning context'
            )

        a_set = set()
        b_set = set()

        for pitch_a in self:
            a_set.add(pitch_a.pc_index)

        for pitch_b in other:
            b_set.add(pitch_b.pc_index)

        return a_set == b_set

    def is_subset(
        self,
        other: Self,
        proper: Optional[bool] = False,
        ignore_bi_index: Optional[bool] = False,
    ) -> bool:
        """
        Determines if all pitches in this scale also exist
        in the other scale.

        :param other: Another scale of the same tuning
        :param proper: (Optional, default False) When set
            to True method will return False if the two
            sets are identical
        :param ignore_bi_index: (Optional, default False)
            When set to True pitches of the same pitch class
            will be treated the same.

        :raises IncompatibleTunings: If the other scale has a
            different tuning
        """

        if not ignore_bi_index:
            return super().is_subset(other, proper)

        intersection = self.intersection(other, ignore_bi_index=True)

        is_subset = self.is_equivalent(intersection)

        if not proper:
            return is_subset

        equal = self.is_equivalent(other)

        return is_subset and not equal

    def is_superset(
        self,
        other: Self,
        proper: Optional[bool] = False,
        ignore_bi_index: Optional[bool] = False,
    ) -> bool:
        """
        Determines if all pitches in the other scale also exist
        in this scale.

        :param other: Another scale of the same tuning
        :param proper: (Optional, default False) When set
            to True method will return False if the two
            sets are identical
        :param ignore_bi_index: (Optional, default False)
            When set to True pitches of the same pitch class
            will be treated the same.

        :raises IncompatibleTunings: If the other scale has a
            different tuning
        """

        if not ignore_bi_index:
            return super().is_superset(other, proper)

        intersection = self.intersection(other, ignore_bi_index=True)

        is_superset = other.is_equivalent(intersection)

        if not proper:
            return is_superset

        equal = self.is_equivalent(other)

        return is_superset and not equal


class EDPitchScale(PeriodicPitchScale[EDPitch]):
    """Pitch scale class for equal division tunings"""


class EDOPitchScale(EDPitchScale):
    """Pitch scale class for 'equal division of the octave' tunings"""
