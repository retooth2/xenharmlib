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

import sympy as sp

from ..core import PeriodicSDTuning
from ..core import PeriodicSDPitch
from ..core import PeriodicSDPitchInterval
from ..core import PeriodicSDPitchScale
from ..core import PeriodicSDPitchIntervalSeq

from ..core.frequencies import Frequency
from ..core.frequencies import FrequencyRatio
from ..exc import IncompatibleOriginContexts


class EDPitch(PeriodicSDPitch):
    """
    The pitch type for equal division tunings

    :param tuning: The tuning to which this pitch belongs
    :param frequency: The frequency this pitch represents
    :param pitch_index: An integer denoting the pitch (with
        0 being the first pitch, 1 being the second, etc)
    """


class EDPitchInterval(PeriodicSDPitchInterval[EDPitch]):
    """
    Pitch interval class for equal division tunings
    """


class EDPitchScale(PeriodicSDPitchScale[EDPitch]):
    """Pitch scale class for equal division tunings"""


class EDPitchIntervalSeq(PeriodicSDPitchIntervalSeq[EDPitchInterval]):
    """
    The pitch interval sequence class for equal division tunings

    :param tuning: The tuning this pitch interval sequence originates from
    :param intervals: A sequence of pitch intervals
    """


# hack for RTD (see doc/conf.py for more info)
if 'READTHEDOCS' in os.environ:
    Hz440C0 = Frequency(55 / 2 ** Fraction(7, 4))
else:
    Hz440C0 = Frequency(sp.Integer(55) / sp.Integer(2) ** sp.Rational(7, 4))


class EDTuning(
    PeriodicSDTuning[
        EDPitch,
        EDPitchInterval,
        EDPitchScale,
        EDPitchIntervalSeq
    ]
):
    """
    EDTuning ("equal division tuning") takes a base interval
    given as a frequency ratio and divides this base interval
    into pitches equally spaced from one another.

    For example, the Bohlen-Pierce tuning can be created
    like this:

    >>> from xenharmlib import EDTuning
    >>> from xenharmlib import FrequencyRatio
    >>> BP = EDTuning(
    ...     divisions=13,
    ...     eq_ratio=FrequencyRatio(3)
    ... )

    :param divisions: The number of divisions of the base
        interval
    :param eq_ratio: The frequency factor defining the base
        interval (e.g. 2 for an octave, 3/2 for a fifth)
    :param pitch_cls: (Optional) The python class for the pitch
        that is used to generate a pitch object in the pitch
        method. (Not to be confused with the 'pitch class' of
        pitches in periodic tunings). Defaults to
        :class:`~xenharmlib.core.pitch.EDPitch`
    :param pitch_interval_cls: (Optional) The python class
        for the pitch interval that is used to generate a
        pitch interval object in the pitch interval method.
        Defaults to :class:`~xenharmlib.core.pitch.EDPitchInterval`
    :param pitch_scale_cls: (Optional) The python class for the pitch
        scale that is used to generate a pitch scale object
        in the pitch scale method. Defaults to
        :class:`~xenharmlib.core.pitch_scale.EDPitchScale`
    :param ref_frequency: (Optional) A reference frequency on
        which this tuning is built. For EDTunings this is the
        lowest pitch (pitch index 0). Defaults to the frequency
        for C0 in EDO tunings for A4 = 440Hz (about 16.35 Hz)
    """

    def __init__(
        self,
        divisions,
        eq_ratio: FrequencyRatio,
        pitch_cls: type[EDPitch] = EDPitch,
        pitch_interval_cls: type[EDPitchInterval] = EDPitchInterval,
        pitch_scale_cls: type[EDPitchScale] = EDPitchScale,
        pitch_interval_seq_cls: type[EDPitchIntervalSeq] = EDPitchIntervalSeq,
        ref_frequency: Frequency = Hz440C0,
    ):

        super().__init__(
            period_length=divisions,
            eq_ratio=eq_ratio,
            pitch_cls=pitch_cls,
            pitch_interval_cls=pitch_interval_cls,
            pitch_scale_cls=pitch_scale_cls,
            pitch_interval_seq_cls=pitch_interval_seq_cls,
            ref_frequency=ref_frequency,
        )

        if not isinstance(eq_ratio, FrequencyRatio):
            raise TypeError('eq_ratio must be a FrequencyRatio')

        self.divisions = divisions

    @property
    def name(self) -> str:
        """
        The name of this tuning
        """
        expr = f'{self.eq_ratio.sp_expr}'
        return f'{self.divisions}ed{expr}'

    def get_frequency(self, pitch: EDPitch) -> Frequency:
        """
        Returns the frequency of a given note

        :param note: A note from this tuning
        :raises IncompatibleOriginContexts: If note is from a different
            tuning
        """

        if pitch.tuning is not self:
            raise IncompatibleOriginContexts(
                'Given pitch has a different tuning'
            )

        index = pitch.pitch_index
        return self.get_frequency_for_index(index)

    def get_frequency_for_index(self, pitch_index: int) -> Frequency:
        """
        Returns the frequency for a given pitch index

        :param pitch_index: A pitch index
        """

        scale_size = len(self)
        exp = sp.Rational(1, scale_size)
        ratio = (self.eq_ratio**exp) ** pitch_index
        return self.ref_frequency * ratio
