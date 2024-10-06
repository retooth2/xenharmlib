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
from typing import List
from typing import Self
from typing import Optional
from warnings import warn
from .pitch import Pitch
from .pitch import PeriodicPitch
from .pitch import EDPitch
from .pitch import PitchInterval
from .interval import Interval
from .scale import Scale
from .scale import PeriodicScale
from ..exc import IncompatibleOriginContexts

PitchT = TypeVar('PitchT', bound=Pitch)


class PitchScale(Scale[PitchT]):
    """
    The base class of all pitch scales. Implements list and set
    operations, transposition, retuning, etc.

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

    def transpose(self, diff: int | PitchInterval[PitchT]) -> Self:
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

        pitches = []

        for pitch in self:
            retuned_pitch = pitch.retune(tuning)
            pitches.append(retuned_pitch)

        return tuning.scale(pitches)


PeriodicPitchT = TypeVar('PeriodicPitchT', bound=PeriodicPitch)


class PeriodicPitchScale(
    PitchScale[PeriodicPitchT], PeriodicScale[PeriodicPitchT]
):
    """
    Pitch scale class for periodic tunings. Implements
    operations like rotation and customized set operations
    (for when you want to treat equivalent pitches the same
    as equal pitches). It also implements normalization methods.
    """

    # normalization methods

    def pcs_complement(self) -> Self:
        """
        Normalizes this scale to the first base interval
        and returns the complement (that is: a scale of
        all pitches NOT in this scale) as a normalized
        scale
        """

        n_scale = self.pcs_normalized()
        complement = []

        full_scale = self.tuning.scale(
            self.tuning.pitch_range(len(self.tuning))
        )

        for pitch in full_scale:
            if pitch not in n_scale:
                complement.append(pitch)

        return self.tuning.scale(complement)

    @property
    def pc_indices(self) -> List[int]:
        """
        Returns a list of pitch class indices in
        the order they appear in this scale. This can
        include duplicate items if the list has two
        pitches of the same pitch class
        """
        return [pitch.pc_index for pitch in self]


class EDPitchScale(PeriodicPitchScale[EDPitch]):
    """Pitch scale class for equal division tunings"""


class EDOPitchScale(EDPitchScale):
    """Pitch scale class for 'equal division of the octave' tunings"""
