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
A tuning is the middle piece between the continuous world of frequencies
and the discrete world of pitch.

In this module, you will find a collection of tuning classes, each with
a certain set of assumptions built into them. Some tuning classes can
be used as they are to create tuning objects, some are abstract classes
that need a couple of methods implemented by a subclass.
"""

from __future__ import annotations
import os
from abc import abstractmethod
from fractions import Fraction
from typing import TypeVar
from typing import List
from typing import Optional
from warnings import warn

import sympy as sp

from .pitch import Pitch
from .pitch import PitchInterval
from .pitch_scale import PitchScale

from .pitch import PeriodicPitch
from .pitch import PeriodicPitchInterval
from .pitch_scale import PeriodicPitchScale

from .pitch import EDPitch
from .pitch import EDOPitch
from .pitch import EDPitchInterval
from .pitch import EDOPitchInterval
from .pitch_scale import EDPitchScale
from .pitch_scale import EDOPitchScale
from .pitch_interval_seq import PitchIntervalSeq
from .pitch_interval_seq import PeriodicPitchIntervalSeq
from .pitch_interval_seq import EDPitchIntervalSeq
from .pitch_interval_seq import EDOPitchIntervalSeq
from .frequencies import Frequency
from .frequencies import FrequencyRatio
from .origin_context import OriginContext
from ..exc import IncompatibleOriginContexts
from ..exc import InvalidPitchClassIndex

PitchT = TypeVar('PitchT', bound=Pitch)
IntervalT = TypeVar('IntervalT', bound=PitchInterval)
IntervalSeqT = TypeVar('IntervalSeqT', bound=PitchIntervalSeq)
ScaleT = TypeVar('ScaleT', bound=PitchScale)


class TuningABC(OriginContext[PitchT, IntervalT, ScaleT, IntervalSeqT]):
    """
    The most abstract tuning class and the base class for all
    other tunings. AbstractTuning makes next to no assumptions
    about the tuning, only that it has a reference frequency
    to 'center' the tuning and python classes that define the
    type of pitch, pitch interval, and pitch scale adjacent to
    this tuning.

    A simple tuning can be derived from this simply by
    overwriting the method :meth:`~.AbstractTuning.get_frequency`
    and setting appropriate constructor arguments.

    The constructor arguments are:

    :param pitch_cls: The python class for the pitch that is
        used to generate a pitch object in the
        :meth:`~.AbstractTuning.pitch` method.
        (Not to be confused with the 'pitch class' of pitches
        in periodic tunings)
    :param pitch_interval_cls: The python class for the pitch
        interval that is used to generate a pitch interval object
        in the :meth:`~AbstractTuning.pitch_interval` method.
    :param pitch_scale_cls: The python class for the pitch
        scale that is used to generate a pitch scale object
        in the :meth:`~AbstractTuning.pitch_scale` method.
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


PeriodicPitchT = TypeVar('PeriodicPitchT', bound=PeriodicPitch)
PeriodicIntervalT = TypeVar('PeriodicIntervalT', bound=PeriodicPitchInterval)
PeriodicScaleT = TypeVar('PeriodicScaleT', bound=PeriodicPitchScale)
PeriodicIntervalSeqT = TypeVar(
    'PeriodicIntervalSeqT',
    bound=PeriodicPitchIntervalSeq
)


class PeriodicTuning(
    TuningABC[
        PeriodicPitchT,
        PeriodicIntervalT,
        PeriodicScaleT,
        PeriodicIntervalSeqT
    ]
):
    """
    This abstract class makes the assumption that the tuning has
    a period (a fixed distance between two pitches that declares
    the two pitches as 'equivalent'). This can be the octave in
    EDO tunings or a tritave in ED3 tunings.

    Periodic tunings implement the len() function that returns
    the period length:

    >>> from xenharmlib import EDOTuning
    >>> edo12 = EDOTuning(12)
    >>> len(edo12)
    12

    The constructor arguments are:

    :param period_length: The number of pitches that constitute
        a period (for example 12 in 12EDO)
    :param eq_ratio: A frequency ratio that defines the
        equivalency interval
    :param pitch_cls: The python class for the pitch that is
        used to generate a pitch object in the pitch method.
        (Not to be confused with the 'pitch class' of pitches
        in periodic tunings)
    :param pitch_interval_cls: The python class for the pitch
        interval that is used to generate a pitch interval
        object in the pitch interval method.
    :param pitch_scale_cls: The python class for the pitch
        scale that is used to generate a pitch scale object
        in the pitch scale method.
    :param ref_frequency: A reference frequency on which this
        tuning is build.
    """

    def __init__(
        self,
        period_length: int,
        eq_ratio: FrequencyRatio,
        pitch_cls: type[PeriodicPitchT],
        pitch_interval_cls: type[PeriodicIntervalT],
        pitch_scale_cls: type[PeriodicScaleT],
        pitch_interval_seq_cls: type[PeriodicIntervalSeqT],
        ref_frequency: Frequency,
    ):

        super().__init__(
            pitch_cls=pitch_cls,
            pitch_interval_cls=pitch_interval_cls,
            pitch_scale_cls=pitch_scale_cls,
            pitch_interval_seq_cls=pitch_interval_seq_cls,
            ref_frequency=ref_frequency,
        )

        self._eq_ratio = eq_ratio
        self._period_length = period_length

    def __len__(self):
        return self._period_length

    @property
    def eq_ratio(self) -> FrequencyRatio:
        """
        The frequency ratio defining the equivalency interval
        """
        return self._eq_ratio

    def pc_scale(
        self, pc_indices: Optional[List[int]] = None, root_bi_index: int = 0
    ) -> ScaleT:
        """
        Constructs a pitch scale from a list of pitch class indices.
        The pitch class indices are assumed to be in the order they
        appear in the scale meaning that e.g. in 12-EDO the provided
        argument [7, 3, 4] will result in a scale with pitch indices
        [7, 15, 16]. The base interval of the first provided pc index
        will always assumed to be 0.

        :raises InvalidPitchClassIndex: If one of the indices in the
            list is not a valid pitch class index in this tuning

        :param pc_indices: A list of pitch class indices.
        :param root_bi_index: Base interval index of the root
            (optional, defaults to 0)
        """

        pitches = []
        current_bi_index = root_bi_index
        tuning_len = len(self)

        if not pc_indices:
            return self.scale()

        head = pc_indices[0]
        if head >= tuning_len:
            raise InvalidPitchClassIndex(
                f'Pitch class index must be between 0 and {tuning_len}'
                f'(exclusive). {head} did not meet that boundary.'
            )

        pitch_index = head + (tuning_len * current_bi_index)
        pitches.append(self.pitch(pitch_index))

        for prev_pci, current_pci in zip(pc_indices, pc_indices[1:]):
            if current_pci >= tuning_len:
                raise InvalidPitchClassIndex(
                    f'Pitch class index must be between 0 and {tuning_len}'
                    f'(exclusive). {current_pci} did not meet that boundary.'
                )
            if current_pci <= prev_pci:
                current_bi_index += 1
            pitch_index = current_pci + (tuning_len * current_bi_index)
            pitches.append(self.pitch(pitch_index))

        return self.scale(pitches)

    def get_ring_number(self, pitch: PeriodicPitchT) -> int:
        """
        Returns the greatest common divisor of a pitch and the
        period length of the tuning.

        :param pitch: A pitch of this tuning.
        """

        p = len(self)
        q = pitch.pc_index

        while q != 0:
            p, q = q, p % q

        return p

    @property
    def generator_pitches(self) -> List[PeriodicPitchT]:
        """
        Returns a list of pitch objects that can be used
        to generate the complete set of pitches in this
        tuning by subsequent interval additions with
        themselves.

        A typical generator pitch in 12-EDO for example is
        the pitch with index 7 which generates the circle
        of fifths.
        """

        generators = []

        for index in range(1, len(self) + 1):

            p = len(self)
            q = index

            while q != 0:
                p, q = q, p % q

            if p == 1:  # numbers are co-prime
                generators.append(self.pitch(index))

        return generators


# hack for RTD (see doc/conf.py for more info)
if 'READTHEDOCS' in os.environ:
    Hz440C0 = Frequency(55 / 2 ** Fraction(7, 4))
else:
    Hz440C0 = Frequency(sp.Integer(55) / sp.Integer(2) ** sp.Rational(7, 4))


class EDTuning(
    PeriodicTuning[
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
