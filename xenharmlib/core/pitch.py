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

from typing import Self
from typing import TypeVar
from warnings import warn
from .frequencies import FrequencyRatio
from .protocols import Index
from .protocols import PeriodicIndex
from .protocols import PeriodicPitchLike
from .protocols import SDPeriodicPitchLike
from .protocols import SDPitchIntervalLike
from .protocols import SDTuningLike
from .freq_repr import IndexedFreqRepr
from .interval import IndexedInterval
from ..exc import IncompatibleOriginContexts
from ..exc import InvalidGenerator

IndexT = TypeVar('IndexT', bound=Index)


class Pitch(IndexedFreqRepr[IndexT]):
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

    def __init__(self, tuning, frequency, pitch_index: IndexT):
        super().__init__(tuning, frequency, pitch_index)
        self._tuning = tuning

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

    def transpose(self, diff: IndexT | PitchInterval) -> Pitch:
        """
        Transposes the pitch to a different one

        :param diff: The difference from this pitch. Can be
            either an integer (positive for upward movement,
            negative for downward movement) or a pitch
            interval
        """

        if isinstance(diff, PitchInterval):
            transposed_index = self.pitch_index + diff.pitch_diff
        else:
            transposed_index = self.pitch_index + diff

        return self.tuning.pitch(transposed_index)

    def retune(self, tuning: SDTuningLike) -> Self:
        """
        .. deprecated:: 0.4.0
           Use :py:meth:`retune_closest` instead.

        Gets the frequency representation in a given origin context
        that is closest to the frequency of this object.

        :param origin_context: The target origin context

        :raises NotImplementedError: If the target tuning does not
            have a proper definition of a closest representation
            to a given frequency
        """

        warn(
            f'{self.__class__.__name__}.retune is deprecated and will '
            f'be removed 1.0.0. Please use the .retune_closest method. ',
            DeprecationWarning,
            stacklevel=2,
        )

        return self.retune_closest(tuning)


PeriodicIndexT = TypeVar('PeriodicIndexT', bound=PeriodicIndex)


class PeriodicPitch(Pitch[PeriodicIndexT], PeriodicPitchLike):
    """
    The pitch type for periodic tunings. Depending on the period
    length it will classify the pitch into a 'pitch class index'
    (:attr:`pc_index` attribute) and a 'base interval index'
    (:attr:`bi_index`)

    :param tuning: The tuning to which this pitch belongs
    :param frequency: The frequency this pitch represents
    :param pitch_index: An integer denoting the pitch (with
        0 being the first pitch, 1 being the second, etc)
    """

    def __init__(self, tuning, frequency, pitch_index: PeriodicIndexT):

        super().__init__(tuning, frequency, pitch_index)

        self._pc_index = pitch_index % tuning.eq_diff
        self._bi_index = pitch_index // tuning.eq_diff

    @property
    def pc_index(self) -> PeriodicIndexT:
        """
        The pitch class index of this pitch
        """
        return self._pc_index

    @property
    def bi_index(self) -> int:
        """
        The base interval index of this pitch
        """
        return self._bi_index

    @property
    def pc_short_repr(self) -> str:
        return f'{self.pc_index}'

    def transpose_bi_index(self, bi_diff: int) -> Self:
        """
        Returns a pitch with the same pitch class index
        but a transposed base interval

        :param bi_diff: The difference in base interval
            between this pitch and the resulting one
        """

        bi_index = self._bi_index + bi_diff
        pitch_index = self._pc_index + bi_index * self.tuning.eq_diff
        return self.tuning.pitch(pitch_index)

    def pcs_normalized(self) -> Self:
        """
        Returns the equivalent of this pitch in the first base interval
        """
        return self.tuning.pitch(self.pc_index)

    def is_equivalent(self, other: PeriodicPitchLike) -> bool:
        """
        Returns True if this pitch has the same frequency as the
        other object when normalized to the first base interval

        :param other: Another periodic pitch or note
        """

        if self.tuning is other.tuning:
            return self.pc_index == other.pc_index

        if self.tuning.eq_ratio == other.tuning.eq_ratio:
            bi_diff = self.bi_index - other.bi_index
            t_other = other.transpose_bi_index(bi_diff)
            return self == t_other

        raise IncompatibleOriginContexts(
            'Equivalency can only be tested for pitches from tunings '
            'with the same equivalency interval'
        )


class SDPeriodicPitchMixin:

    def get_generator_index(
        self: SDPeriodicPitchLike, generator_pitch: SDPeriodicPitchLike
    ):
        """
        Calculates the number of steps needed to reach this pitch
        when iteratively adding the given generator to the zero
        pitch of this tuning

        :param generator_pitch: A generator pitch. Will be normalized
            to the equivalent pitch in the first base interval if its
            pitch index exceeds the period length of the tuning.

        :raises IncompatibleOriginContexts: If pitches come
            from different tuning systems

        :raises InvalidGenerator: If the given generator pitch is not in
            fact a generator in the tuning of this pitch
        """

        if generator_pitch.tuning is not self.tuning:
            raise IncompatibleOriginContexts(
                'Pitches must originate from the same tuning context'
            )

        generator_pitch = generator_pitch.pcs_normalized()

        if generator_pitch not in self.tuning.generator_pitches:
            raise InvalidGenerator(
                f'{generator_pitch} is not a valid generator '
                f'in tuning {self.tuning.name}'
            )

        gen_pc = generator_pitch.pitch_index

        pc_index = 0
        g_index = 0

        while True:

            if pc_index == self.pc_index:
                break

            g_index += 1
            pc_index = (pc_index + gen_pc) % self.tuning.eq_diff

        return g_index


class EDPitch(PeriodicPitch[int], SDPeriodicPitchMixin):
    """
    The pitch type for equal division tunings

    :param tuning: The tuning to which this pitch belongs
    :param frequency: The frequency this pitch represents
    :param pitch_index: An integer denoting the pitch (with
        0 being the first pitch, 1 being the second, etc)
    """


class EDOPitch(EDPitch):
    """
    The pitch type for 'equal division of the octave' tunings

    :param tuning: The tuning to which this pitch belongs
    :param frequency: The frequency this pitch represents
    :param pitch_index: An integer denoting the pitch (with
        0 being the first pitch, 1 being the second, etc)
    """


PitchT = TypeVar('PitchT', bound=Pitch)


class PitchInterval(IndexedInterval[IndexT, PitchT]):
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
        are not equal step.
    """

    def __init__(
        self,
        tuning,
        frequency_ratio: FrequencyRatio,
        pitch_diff: IndexT,
        ref_pitch: PitchT,
    ):
        super().__init__(tuning, frequency_ratio, pitch_diff)
        self.ref_pitch = ref_pitch
        self.tuning = tuning

    def __abs__(self) -> Self:
        """
        Returns the absolute of this pitch interval. On downwards
        interval it returns an upwards interval of the same absolute
        size. On upwards intervals it acts as the identity function.
        """

        if self.pitch_diff >= self.tuning.zero_index:
            return self

        target_pitch = self.ref_pitch.transpose(self.pitch_diff)

        return self.tuning.interval(target_pitch, self.ref_pitch)

    def __neg__(self) -> Self:
        """
        Returns the negative of this pitch interval. On downwards
        interval it returns an upwards interval of the same absolute
        size. On upwards intervals it returns the corresponding
        downwards interval
        """

        target_pitch = self.ref_pitch.transpose(self)
        return self.tuning.interval(target_pitch, self.ref_pitch)

    def __add__(self, other) -> Self:
        """
        Returns the combination of two intervals
        """
        if not isinstance(other, PitchInterval):
            raise TypeError(
                f"unsupported operand type(s) for +: "
                f"'{type(self)}' and '{type(other)}'"
            )
        if self.origin_context is not other.origin_context:
            raise IncompatibleOriginContexts(
                'Intervals must originate from the same tuning context'
            )
        target_pitch = self.ref_pitch.transpose(self).transpose(other)
        return self.tuning.interval(self.ref_pitch, target_pitch)

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

    def __repr__(self) -> str:
        return (
            f'{self.__class__.__name__}({self.pitch_diff}, {self.tuning.name})'
        )

    @property
    def short_repr(self) -> str:
        return f'{self.pitch_diff}'


PeriodicPitchT = TypeVar('PeriodicPitchT', bound=PeriodicPitch)


class PeriodicPitchInterval(PitchInterval[PeriodicIndexT, PeriodicPitchT]):
    """
    The pitch interval class for periodic tunings.
    """

    @property
    def is_compound(self) -> bool:
        """
        Returns True if this interval is a compound interval,
        False otherwise. A compound interval is defined as
        an interval whose absolute value is strictly greater
        than the equivalency interval (meaning the equivalency
        interval itself and its negation are not considered
        compound)
        """
        return abs(self) > self.origin_context.eq_interval

    @property
    def is_simple(self) -> bool:
        """
        Returns True if this interval is a simple interval,
        False otherwise. A simple interval is defined as
        an interval whose absolute value is lesser or equal
        than the equivalency interval (meaning the equivalency
        interval itself and its negation are considered a simple
        interval)
        """
        return abs(self) <= self.origin_context.eq_interval

    def to_simple(self) -> Self:
        """
        Returns the corresponding simple interval if this
        is a compound interval (or the interval itself if
        it is already simple)

        The method preserves direction, so if this interval
        is a downward interval, the resulting interval will
        also be a downward interval.
        """

        interval = self
        eq_interval = self.origin_context.eq_interval

        while interval.is_compound:
            # if interval is pointing upward, subtract
            # the equivalency interval successively.
            # if it points downwards, add it.
            interval += (-1) * self.sign * eq_interval

        return interval

    def inversion(self) -> Self:
        """
        Returns the inversion of this interval. The inversion
        is calculated by subtracting this interval from the
        equivalency interval.
        """

        return self.origin_context.eq_interval - self

    def ic_normalized(self) -> Self:
        """
        Returns an interval class normalized version of this
        interval. The interval normalized version is calculated
        by converting (if necessary) this interval into a simple
        interval, normalizing it to a upwards interval and then
        building the minimum from that result and its inversion.
        """
        a = abs(self.to_simple())
        b = a.inversion()
        return min(a, b)

    @property
    def ic_index(self) -> PeriodicIndexT:
        """
        Returns the interval class index of this interval
        (often simply called "interval class" or "ic")
        as known from pitch class set theory.

        The interval class is the shortest distance in pitch
        class space between two unordered pitch classes.

        It is calculated by comparing the absolute value of
        the simple portion of the interval and its inversion,
        returning whatever pitch difference is smaller, so
        e.g. in 12-EDO the ic class for P5 is min(7, 5) = 5
        """
        return self.ic_normalized().pitch_diff


class SDPeriodicPitchIntervalMixin:

    def get_generator_distance(
        self: SDPitchIntervalLike, generator_pitch: PeriodicPitchT
    ) -> int:
        """
        Calculates the minimum number of steps needed to reach
        one pitch from the other when iteratively adding a
        generator pitch.

        A typical application in 12EDO is to calculate the minimum
        distance of the two pitches on the circle of fifths, hence
        the generator distance can be a good measure for consonance
        of an interval given the right generator pitch.

        >>> from xenharmlib import EDOTuning
        >>> edo12 = EDOTuning(12)
        >>> M3 = edo12.pitch(0).interval(edo12.pitch(4))
        >>> M3.get_generator_distance(edo12.pitch(7))
        4

        :param generator_pitch: A generator pitch. Will be normalized
            to the equivalent pitch in the first base interval if its
            pitch index exceeds the period length of the tuning.

        :raises InvalidGenerator: If the pitch is not a generator
            in the tuning attached to the interval
        """

        zero = self.tuning.pitch(0)
        target = self.tuning.pitch(abs(self).pitch_diff)

        i_zero = zero.get_generator_index(generator_pitch)
        i_target = target.get_generator_index(generator_pitch)
        i_diff = i_target - i_zero

        return min(i_diff, self.tuning.eq_diff - i_diff)


class EDPitchInterval(
    PeriodicPitchInterval[int, EDPitch], SDPeriodicPitchIntervalMixin
):
    """
    Pitch interval class for equal division tunings
    """


class EDOPitchInterval(EDPitchInterval):
    """
    Pitch intervals class for 'equal division of the octave'
    pitches
    """
