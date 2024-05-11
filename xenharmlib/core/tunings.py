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
import sympy as sp
from abc import ABC
from abc import abstractmethod
from fractions import Fraction
from typing import TypeVar
from typing import Generic
from typing import List
from typing import Optional

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
from .frequencies import Frequency
from ..exc import IncompatibleTunings

PitchT = TypeVar('PitchT', bound=Pitch)
IntervalT = TypeVar('IntervalT', bound=PitchInterval)
ScaleT = TypeVar('ScaleT', bound=PitchScale)


class TuningABC(ABC, Generic[PitchT, IntervalT, ScaleT]):
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
        ref_frequency: Frequency,
    ):

        self.ref_frequency = ref_frequency
        self._pitch_cls = pitch_cls
        self._pitch_interval_cls = pitch_interval_cls
        self._pitch_scale_cls = pitch_scale_cls

    def pitch(self, pitch_index: int) -> PitchT:
        """
        Returns a pitch having the pitch type this tuning
        was configured with

        :param pitch_index: An integer denoting the
            number of steps from the zero pitch.
        """
        return self._pitch_cls(self, pitch_index)

    def pitch_interval(self, pitch_a: PitchT, pitch_b: PitchT) -> IntervalT:
        """
        Returns a pitch interval having the pitch intervals type
        this tuning was configured with

        :param pitch_a: The starting pitch
        :param pitch_b: The target pitch
        """
        return self._pitch_interval_cls.from_pitches(pitch_a, pitch_b)

    def pitch_scale(self, pitches: Optional[List[PitchT]] = None) -> ScaleT:
        """
        Returns a pitch scale having the pitch scale type
        this tuning was configured with

        :param pitches: A list of pitches
        """
        return self._pitch_scale_cls(self, pitches)

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

    def __repr__(self):
        return f'{self.__class__.__name__}({self.name})'


PeriodicPitchT = TypeVar('PeriodicPitchT', bound=PeriodicPitch)
PeriodicIntervalT = TypeVar('PeriodicIntervalT', bound=PeriodicPitchInterval)
PeriodicScaleT = TypeVar('PeriodicScaleT', bound=PeriodicPitchScale)


class PeriodicTuning(
    TuningABC[PeriodicPitchT, PeriodicIntervalT, PeriodicScaleT]
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
        pitch_cls: type[PeriodicPitchT],
        pitch_interval_cls: type[PeriodicIntervalT],
        pitch_scale_cls: type[PeriodicScaleT],
        ref_frequency: Frequency,
    ):

        super().__init__(
            pitch_cls=pitch_cls,
            pitch_interval_cls=pitch_interval_cls,
            pitch_scale_cls=pitch_scale_cls,
            ref_frequency=ref_frequency,
        )

        self._period_length = period_length

    def __len__(self):
        return self._period_length

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


Hz440C0 = Frequency(sp.Integer(55) / sp.Integer(2) ** sp.Rational(7, 4))


class EDTuning(PeriodicTuning[EDPitch, EDPitchInterval, EDPitchScale]):
    """
    EDTuning ("equal division tuning") takes a base interval
    given as a frequency ratio and divides this base interval
    into pitches equally spaced from one another.

    For example, the Bohlen-Pierce tuning can be created
    like this:

    >>> from xenharmlib import EDTuning
    >>> from xenharmlib import Frequency
    >>> BP = EDTuning(
    ...     divisions=13,
    ...     eq_ratio=Frequency(3)
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
        eq_ratio: Frequency,
        pitch_cls: type[EDPitch] = EDPitch,
        pitch_interval_cls: type[EDPitchInterval] = EDPitchInterval,
        pitch_scale_cls: type[EDPitchScale] = EDPitchScale,
        ref_frequency: Frequency = Hz440C0,
    ):

        super().__init__(
            period_length=divisions,
            pitch_cls=pitch_cls,
            pitch_interval_cls=pitch_interval_cls,
            pitch_scale_cls=pitch_scale_cls,
            ref_frequency=ref_frequency,
        )
        self.divisions = divisions
        self.eq_ratio = eq_ratio

    @property
    def name(self) -> str:
        expr = f'{self.eq_ratio.sp_expr}'
        return f'{self.divisions}ed{expr}'

    def get_frequency(self, pitch: EDPitch) -> Frequency:
        """
        Returns the frequency of a given note

        :param note: A note from this tuning
        :raises IncompatibleTunings: If note is from a different
            tuning
        """

        if pitch.tuning is not self:
            raise IncompatibleTunings('Given pitch has a different tuning')

        scale_size = len(self)
        index = pitch.pitch_index
        exp = sp.Rational(1, scale_size)
        return Frequency(self.ref_frequency * (self.eq_ratio**exp) ** index)


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
        ref_frequency: Frequency = Hz440C0,
    ):

        super().__init__(
            divisions=divisions,
            eq_ratio=Frequency(2),
            pitch_cls=pitch_cls,
            pitch_interval_cls=pitch_interval_cls,
            pitch_scale_cls=pitch_scale_cls,
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
        return self.get_approx_pitch(
            self.ref_frequency * Frequency(Fraction(3, 2))
        )

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
