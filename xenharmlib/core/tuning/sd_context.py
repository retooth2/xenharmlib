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
This module implements the origin context class for single-dimensional
tunings. In single-dimensional tuning each pitch can be represented by
a single integer
"""

from __future__ import annotations
from abc import abstractmethod
from typing import TypeVar
from typing import List
from typing import Optional
from warnings import warn

from .sd_objects import SDPitch
from .sd_objects import SDPitchInterval
from .sd_objects import SDPitchScale
from .sd_objects import SDPitchIntervalSeq
from ..frequencies import Frequency
from ..origin_context import OriginContext


PitchT = TypeVar('PitchT', bound=SDPitch)
IntervalT = TypeVar('IntervalT', bound=SDPitchInterval)
IntervalSeqT = TypeVar('IntervalSeqT', bound=SDPitchIntervalSeq)
ScaleT = TypeVar('ScaleT', bound=SDPitchScale)


class SDTuning(OriginContext[PitchT, IntervalT, ScaleT, IntervalSeqT]):
    """
    The abstract base class for single-dimension tunings. The class
    makes next to no assumptions about the tuning, only that it has
    a reference frequency to 'center' the tuning and that frequency
    representions can be created by providing an integer.

    A simple tuning can be derived from this simply by overwriting
    the method :meth:`~.SDTuning.get_frequency_for_index` and
    setting appropriate constructor arguments.

    The constructor arguments are:

    :param pitch_cls: The python class for the pitch that is used
        to generate a pitch object in the :meth:`~.SDTuning.pitch`
        method. (Not to be confused with the 'pitch class' of
        pitches in periodic tunings)
    :param pitch_interval_cls: The python class for the pitch
        interval that is used to generate a pitch interval object
        in the :meth:`~SDTuning.interval` method.
    :param pitch_scale_cls: The python class for the pitch
        scale that is used to generate a pitch scale object
        in the :meth:`~SDTuning.scale` method.
    :param pitch_interval_seq_cls: The python class for the pitch
        interval sequence that is used to generate a pitch interval
        sequence object in the :meth:`~SDTuning.interval_seq` method.
    :param ref_frequency: A reference frequency on which this
        tuning is built.
    """

    def __init__(
        self,
        pitch_cls: type[PitchT],
        pitch_interval_cls: type[IntervalT],
        pitch_scale_cls: type[ScaleT],
        pitch_interval_seq_cls: type[IntervalSeqT],
        ref_frequency: Frequency,
    ):

        super().__init__(
            pitch_cls,
            pitch_interval_cls,
            pitch_scale_cls,
            pitch_interval_seq_cls
        )
        self.ref_frequency = ref_frequency

    @property
    def zero_element(self) -> PitchT:
        return self.pitch(0)

    def pitch(self, pitch_index: int) -> PitchT:
        """
        Returns a pitch having the pitch type this tuning
        was configured with

        :param pitch_index: An integer denoting the
            number of steps from the zero pitch.
        """
        frequency = self.get_frequency_for_index(pitch_index)
        return self._freq_repr_cls(self, frequency, pitch_index)

    def pitch_interval(self, pitch_a: PitchT, pitch_b: PitchT) -> IntervalT:
        """
        .. deprecated:: 0.2.0
           Use :py:meth:`interval` instead.

        Returns a pitch interval having the pitch intervals type
        this tuning was configured with

        :param pitch_a: The starting pitch
        :param pitch_b: The target pitch
        """
        warn(
            f'{self.__class__.__name__}.pitch_interval is deprecated and '
            f'will be removed in 1.0.0. Please use '
            f'{self.__class__.__name__}.interval instead.',
            DeprecationWarning,
            stacklevel=2,
        )
        return self.interval(pitch_a, pitch_b)

    def index_scale(self, pitch_indices: Optional[List[int]] = None) -> ScaleT:
        """
        Constructs a pitch scale from a list of pitch indices.
        According to the definition of a scale indices occuring
        multiple times will only be considered once. The list
        of indices will also be sorted automatically.

        :param pitch_indices: A list of pitch indices
        """

        pitches = []
        for index in pitch_indices:
            pitches.append(self.pitch(index))

        return self.scale(pitches)

    def pitch_scale(self, pitches: Optional[List[PitchT]] = None) -> ScaleT:
        """
        .. deprecated:: 0.2.0
           Use :py:meth:`scale` instead.

        Returns a pitch scale having the pitch scale type
        this tuning was configured with

        :param pitches: A list of pitches
        """
        warn(
            f'{self.__class__.__name__}.pitch_scale is deprecated and '
            f'will be removed in 1.0.0. Please use '
            f'{self.__class__.__name__}.scale instead.',
            DeprecationWarning,
            stacklevel=2,
        )
        return self.scale(pitches)

    def pitch_range(self, start, stop=None, step=1):
        """
        Returns a generator for continuous pitches of this
        tuning similar to pythons range function. The
        method can be called in the familiar ways:

        >>> from xenharmlib import EDOTuning
        >>> edo12 = EDOTuning(12)

        >>> for pitch in edo12.pitch_range(3):
        ...    print(pitch)
        EDOPitch(0, 12-EDO)
        EDOPitch(1, 12-EDO)
        EDOPitch(2, 12-EDO)

        >>> for pitch in edo12.pitch_range(5, 10):
        ...    print(pitch)
        EDOPitch(5, 12-EDO)
        EDOPitch(6, 12-EDO)
        EDOPitch(7, 12-EDO)
        EDOPitch(8, 12-EDO)
        EDOPitch(9, 12-EDO)

        >>> for pitch in edo12.pitch_range(5, 10, 2):
        ...    print(pitch)
        EDOPitch(5, 12-EDO)
        EDOPitch(7, 12-EDO)
        EDOPitch(9, 12-EDO)
        """

        if stop is None:
            stop = start
            start = 0

        for i in range(start, stop, step):
            yield self.pitch(i)

    @abstractmethod
    def get_frequency(self, pitch: PitchT) -> Frequency:
        """
        (Must be overwritten by subclasses)
        Returns the frequency for a given pitch
        """

    @abstractmethod
    def get_frequency_for_index(self, pitch_index: int) -> Frequency:
        """
        (Must be overwritten by subclasses)
        Returns the frequency for a given pitch index
        """

    def get_approx_pitch(self, frequency: Frequency) -> PitchT:
        """
        Returns the closest pitch in the tuning
        to a given frequency.

        :param frequency: The frequency in Hz
        """

        base_pitch = self.pitch(0)

        # first find the appropriate search window

        if frequency >= base_pitch.frequency:
            bottom_pitch = base_pitch
            i = 0
            while True:
                top_pitch = self.pitch(2**i)
                if top_pitch.frequency > frequency:
                    break
                i += 1
        else:
            top_pitch = base_pitch
            i = 0
            while True:
                bottom_pitch = self.pitch(-(2**i))
                if bottom_pitch.frequency < frequency:
                    break
                i += 1

        # then do binary search

        higher_pi = top_pitch.pitch_index
        lower_pi = bottom_pitch.pitch_index

        while (higher_pi - lower_pi) > 1:

            middle_pi = lower_pi + (higher_pi - lower_pi) // 2
            middle_pitch = self.pitch(middle_pi)

            if middle_pitch.frequency == frequency:
                return middle_pitch
            if middle_pitch.frequency < frequency:
                lower_pi = middle_pi
            if middle_pitch.frequency > frequency:
                higher_pi = middle_pi

        higher_pitch = self.pitch(higher_pi)
        lower_pitch = self.pitch(lower_pi)

        if abs(lower_pitch.frequency - frequency) < abs(
            higher_pitch.frequency - frequency
        ):
            return lower_pitch

        return higher_pitch
