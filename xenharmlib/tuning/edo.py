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
import os
from fractions import Fraction
from typing import Optional

import sympy as sp

from ..core.frequencies import Frequency
from ..core.frequencies import FrequencyRatio
from .ed import EDTuning
from .ed import EDPitch
from .ed import EDPitchInterval
from .ed import EDPitchScale
from .ed import EDPitchIntervalSeq


# hack for RTD (see doc/conf.py for more info)
if 'READTHEDOCS' in os.environ:
    Hz440C0 = Frequency(55 / 2 ** Fraction(7, 4))
else:
    Hz440C0 = Frequency(sp.Integer(55) / sp.Integer(2) ** sp.Rational(7, 4))


class EDOPitch(EDPitch):
    """
    The pitch type for 'equal division of the octave' tunings

    :param tuning: The tuning to which this pitch belongs
    :param frequency: The frequency this pitch represents
    :param pitch_index: An integer denoting the pitch (with
        0 being the first pitch, 1 being the second, etc)
    """


class EDOPitchInterval(EDPitchInterval):
    """
    Pitch intervals class for 'equal division of the octave'
    pitches
    """


class EDOPitchScale(EDPitchScale):
    """Pitch scale class for 'equal division of the octave' tunings"""


class EDOPitchIntervalSeq(EDPitchIntervalSeq):
    """
    The pitch interval sequence class for 'equal division of the octave'
    tunings

    :param tuning: The tuning this pitch interval sequence originates from
    :param intervals: A sequence of pitch intervals
    """


class EDOTuning(EDTuning):
    """
    EDOTuning ("equal division of the octave tuning") divides an
    octave into pitches equally spaced from each other.

    :param divisions: The number of divisions of the octave
    :param pitch_cls: (Optional) The python class for the pitch
        that is used to generate a pitch object in the pitch
        method. (Not to be confused with the 'pitch class' of
        pitches in periodic tunings). Defaults to
        :class:`~xenharmlib.core.pitch.EDOPitch`
    :param pitch_interval_cls: (Optional) The python class for
        the pitch interval that is used to generate a pitch
        interval object in the pitch interval method. Defaults
        to :class:`~xenharmlib.core.pitch.EDOPitchInterval`
    :param pitch_scale_cls: (Optional) The python class for
        the pitch scale that is used to generate a pitch scale
        object in the pitch scale method. Defaults to
        :class:`~xenharmlib.core.pitch_scale.EDOPitchScale`
    :param ref_frequency: (Optional) A reference frequency on
        which this tuning is built. For EDOTunings this is the
        lowest pitch (pitch index 0). Defaults to the frequency
        for C0 in EDO tunings for A4 = 440Hz (about 16.35 Hz)
    """

    def __init__(
        self,
        divisions,
        pitch_cls: type[EDOPitch] = EDOPitch,
        pitch_interval_cls: type[EDOPitchInterval] = EDOPitchInterval,
        pitch_scale_cls: type[EDOPitchScale] = EDOPitchScale,
        pitch_interval_seq_cls: type[EDOPitchIntervalSeq] = EDOPitchIntervalSeq,
        ref_frequency: Frequency = Hz440C0,
    ):

        super().__init__(
            divisions=divisions,
            eq_ratio=FrequencyRatio(2),
            pitch_cls=pitch_cls,
            pitch_interval_cls=pitch_interval_cls,
            pitch_scale_cls=pitch_scale_cls,
            pitch_interval_seq_cls=pitch_interval_seq_cls,
            ref_frequency=ref_frequency,
        )

    @property
    def name(self) -> str:
        return f'{self.divisions}-EDO'

    @property
    def best_fifth(self):
        """
        Returns the pitch that best approximates the pure fifth
        (frequency ratio 3/2) in this tuning.
        """
        return self.get_approx_pitch(self.ref_frequency * FrequencyRatio(3, 2))

    @property
    def fifth(self):
        """
        Returns the pitch that represents the fifth of
        this tuning. In the default implementation, this
        is the best fifth, however, subclasses can also
        overwrite this behavior, so e.g. the second-best
        fifth is returned.
        """
        return self.best_fifth

    def get_ring_number(self, pitch: Optional[EDOPitch] = None) -> int:
        """
        Returns the greatest common divisor of a pitch and the
        period length of the tuning.

        :param pitch: A pitch of this tuning. (Optional,
            defaults to the pitch that best approximates
            the perfect fifth)
        """

        if pitch is None:
            pitch = self.best_fifth

        return super().get_ring_number(pitch)

    @property
    def sharpness(self) -> int:
        """
        Sharpness is an indicator of the pitch difference in EDO tunings
        between a natural and their sharp version (for example the steps
        needed to reach C# from C)

        The sharpness of an EDO is defined by 7 times the
        pitch difference between the base pitch and the
        perfect fifth approximation minus 4 times
        the pitch difference in an octave.
        """

        fifth = self.fifth
        return fifth.pitch_index * 7 - self.divisions * 4

    def __repr__(self):
        return f'{self.__class__.__name__}({self.name}, {self.divisions})'
