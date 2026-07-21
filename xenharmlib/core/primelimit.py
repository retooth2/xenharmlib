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
This module implements tunings in which pitches and intervals are
formed by using consecutive prime numbers as generators up until
to a specified prime (the "prime limit").
"""

import math

from typing import TypeVar
from typing import Optional
from typing import Tuple
from typing import List
from typing import Iterable
from .frequencies import Frequency
from .frequencies import FrequencyRatio
from .frequencies import Hz440C0
from .multigen import MultiGenTuning
from .multigen import MultiGenPitch
from .multigen import MultiGenPitchInterval
from .multigen import MultiGenPitchScale
from .multigen import MultiGenPitchIntervalSeq
from .multigen import MultiGenPitchIntervalFan
from .multigen import MultiGenPitchSeq
from .utils import get_primes_until
from .utils import pad_tuple


class PrimeLimitPitch(MultiGenPitch):
    """
    The pitch type for prime limit tunings

    :param tuning: The tuning to which this pitch belongs to
    :param frequency: The frequency this pitch represents
    :param pitch_index: An lattice point denoting the pitch
    """

    @property
    def monzo(self) -> Tuple[int, ...]:
        """
        Returns the monzo of this pitch. A monzo is a tuple
        of exponents for the prime number generator vector,
        e.g. in 5-Limit for 5/4 = 2**(-2) * 3**(0) * 5**(1)
        the monzo is (-2, 0, 1)
        """
        return self.pitch_index.vector

    @property
    def short_repr(self) -> str:
        """
        A shortened representation string of this pitch
        without any type prefix
        """
        ratio = FrequencyRatio.from_monzo(self.monzo)
        return ratio.short_repr

    @property
    def pc_short_repr(self) -> str:
        """
        A shortened representation string of the pitch class
        ratio of this pitch
        """
        pc_ratio = FrequencyRatio.from_monzo(self.pcs_normalized().monzo)
        return pc_ratio.short_repr

    def __repr__(self) -> str:
        return (
            f'{self.__class__.__name__}({self.short_repr}, '
            f'{self.tuning.prime_limit}-Limit)'
        )


class PrimeLimitPitchInterval(MultiGenPitchInterval):
    """
    The pitch interval type for prime limit tunings

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

    @property
    def monzo(self) -> Tuple[int, ...]:
        """
        Returns the monzo of this pitch. A monzo is a tuple
        of exponents for the prime number generator vector,
        e.g. in 5-Limit for 5/4 = 2**(-2) * 3**(0) * 5**(1)
        the monzo is (-2, 0, 1)
        """
        return self.pitch_diff.vector

    @property
    def short_repr(self) -> str:
        """
        A shortened representation string of the frequency
        ratio of this interval
        """
        return self.frequency_ratio.short_repr

    def __repr__(self) -> str:
        return (
            f'{self.__class__.__name__}({self.short_repr}, '
            f'{self.tuning.prime_limit}-Limit)'
        )


class PrimeLimitPitchScale(MultiGenPitchScale):
    """
    The pitch scale type for prime limit tunings
    """

    @property
    def monzos(self) -> List[Tuple[int, ...]]:
        """
        Returns the monzos of the pitches in this scale.
        A monzo is a tuple of exponents for the prime number
        generator vector, e.g. in a 5-Limit tuning scale for
        5/4 = 2**(-2) * 3**(0) * 5**(1) the monzo is (-2, 0, 1)
        """
        return [pitch.pitch_index.vector for pitch in self]

    def __repr__(self) -> str:
        ratios_str = ', '.join([pitch.short_repr for pitch in self])
        return (
            f'{self.__class__.__name__}([{ratios_str}], '
            f'{self.tuning.prime_limit}-Limit)'
        )


class PrimeLimitPitchIntervalSeq(MultiGenPitchIntervalSeq):
    """
    The pitch interval sequence type for prime limit tunings
    """

    @property
    def monzos(self) -> List[Tuple[int, ...]]:
        """
        Returns the monzos of the intervals in this interval sequence.
        A monzo is a tuple of exponents for the prime number generator
        vector, e.g. in a 5-Limit tuning sequence for
        5/4 = 2**(-2) * 3**(0) * 5**(1) the monzo is (-2, 0, 1)
        """
        return [interval.pitch_diff.vector for interval in self]

    def __repr__(self) -> str:
        ratios_str = ', '.join([interval.short_repr for interval in self])
        return (
            f'{self.__class__.__name__}([{ratios_str}], '
            f'{self.tuning.prime_limit}-Limit)'
        )


class PrimeLimitPitchIntervalFan(MultiGenPitchIntervalFan):
    """
    The pitch interval fan type for prime limit tunings
    """

    @property
    def monzos(self) -> List[Tuple[int, ...]]:
        """
        Returns the monzos of the intervals in this interval fan.
        A monzo is a tuple of exponents for the prime number
        generator vector, e.g. in a 5-Limit tuning fan for
        5/4 = 2**(-2) * 3**(0) * 5**(1) the monzo is (-2, 0, 1)
        """
        return [interval.pitch_diff.vector for interval in self]

    def to_ec_expr(self) -> str:
        """
        Transforms this interval fan into an enumerated chord
        expression e.g. [1/1, 5/4, 3/2] into '4:5:6'

        An enumerated chord expression is a short form to notate
        frequency ratios of an interval fan as a sequence of
        integers where each integer is divided by the first
        integer.

        :raises ValueError: If fan includes less than two intervals
        :raises ValueError: If fan does not start with unison interval
        """

        if len(self) < 2:
            raise ValueError(
                'Interval fan must have at least length 2 '
                'to create enumerated chord expression'
            )

        if self[0].frequency_ratio != FrequencyRatio(1):
            raise ValueError(
                'Interval fan must start with 1/1 ratio '
                'to create enumerated chord expression'
            )

        # we calculate the lowest common denominator of all
        # ratio fractions and normalize the ratio numerators
        # to it. the resulting numerators are then the basis
        # for our string expression

        lcm = math.lcm(*[i.frequency_ratio.denominator.to_int() for i in self])

        str_partials = []
        for interval in self:
            factor = lcm / interval.frequency_ratio.denominator.to_int()
            n = (factor * interval.frequency_ratio.numerator).short_repr
            str_partials.append(n)

        return ':'.join(str_partials)

    def __repr__(self) -> str:
        ratios_str = ', '.join([interval.short_repr for interval in self])
        return (
            f'{self.__class__.__name__}([{ratios_str}], '
            f'{self.tuning.prime_limit}-Limit)'
        )


class PrimeLimitPitchSeq(MultiGenPitchSeq):
    """
    The pitch sequence type for prime limit tunings
    """

    @property
    def monzos(self) -> List[Tuple[int, ...]]:
        """
        Returns the monzos of the pitches in this sequence.
        A monzo is a tuple of exponents for the prime number
        generator vector, e.g. in a 5-Limit tuning sequence for
        5/4 = 2**(-2) * 3**(0) * 5**(1) the monzo is (-2, 0, 1)
        """
        return [pitch.pitch_index.vector for pitch in self]

    def __repr__(self) -> str:
        ratios_str = ', '.join([pitch.short_repr for pitch in self])
        return (
            f'{self.__class__.__name__}([{ratios_str}], '
            f'{self.tuning.prime_limit}-Limit)'
        )


PrimeLimitPitchT = TypeVar('PrimeLimitPitchT', bound=PrimeLimitPitch)
PrimeLimitIntervalT = TypeVar(
    'PrimeLimitIntervalT', bound=PrimeLimitPitchInterval
)
PrimeLimitScaleT = TypeVar('PrimeLimitScaleT', bound=PrimeLimitPitchScale)
PrimeLimitIntervalSeqT = TypeVar(
    'PrimeLimitIntervalSeqT', bound=PrimeLimitPitchIntervalSeq
)
PrimeLimitIntervalFanT = TypeVar(
    'PrimeLimitIntervalFanT', bound=PrimeLimitPitchIntervalFan
)
PrimeLimitSeqT = TypeVar(
    'PrimeLimitSeqT', bound=PrimeLimitPitchSeq
)


class PrimeLimitTuning(
    MultiGenTuning[
        PrimeLimitPitchT,
        PrimeLimitIntervalT,
        PrimeLimitScaleT,
        PrimeLimitIntervalSeqT,
        PrimeLimitIntervalFanT,
        PrimeLimitSeqT,
    ]
):
    """
    A prime limit tuning is a multi-generator tuning in which the
    generator vector consists of consecutive primes up to a certain
    point (the prime limit), so for example a 7-Limit tuning spans
    a frequency space with generators (2, 3, 5, 7)

    :param prime_limit: The last prime number in the sequence of
        consecutive prime numbers which form the generator vector

    :param ref_frequency: A reference frequency defining the
        frequency of the zero index (optional, defaults to the
        frequency of C0 for A4=440 in 12-EDO)

    :param period_vec: (optional) A vector of integers that defines
        the pitch difference of the interval that should be considered
        the equivalence interval, so for example in a 5 limit tuning
        with generators (2, 3, 5), this should be (1, 0, 0) for
        the octave, (0, 1, 0) for the tritave, etc. If parameter
        is omitted the octave is assumed to be the equivalence
        interval
    """

    def __init__(
        self,
        prime_limit: int,
        period_vec: Optional[Tuple[int, ...]] = None,
        *,
        ref_frequency: Frequency = Hz440C0,
        pitch_cls: type[PrimeLimitPitchT] = PrimeLimitPitch,
        pitch_interval_cls: type[
            PrimeLimitIntervalT
        ] = PrimeLimitPitchInterval,
        pitch_scale_cls: type[PrimeLimitScaleT] = PrimeLimitPitchScale,
        pitch_interval_seq_cls: type[
            PrimeLimitIntervalSeqT
        ] = PrimeLimitPitchIntervalSeq,
        pitch_interval_fan_cls: type[
            PrimeLimitIntervalFanT
        ] = PrimeLimitPitchIntervalFan,
        pitch_seq_cls: type[
            PrimeLimitSeqT
        ] = PrimeLimitPitchSeq,
    ):

        self._prime_limit = prime_limit

        generators = [FrequencyRatio(p) for p in get_primes_until(prime_limit)]

        if period_vec is None:
            period_vec = pad_tuple((1,), 0, len(generators))

        super().__init__(
            generators,
            ref_frequency=ref_frequency,
            period_vec=period_vec,
            pitch_cls=pitch_cls,
            pitch_interval_cls=pitch_interval_cls,
            pitch_scale_cls=pitch_scale_cls,
            pitch_interval_seq_cls=pitch_interval_seq_cls,
            pitch_interval_fan_cls=pitch_interval_fan_cls,
            pitch_seq_cls=pitch_seq_cls,
        )

    @property
    def name(self) -> str:
        return f'PrimeLimitTuning({self.prime_limit})'

    def __repr__(self) -> str:
        return f'PrimeLimitTuning({self.prime_limit}-Limit)'

    @property
    def prime_limit(self) -> int:
        """
        The highest prime number in the sequence of consecutive
        prime number frequency ratios that forms the generator
        vector
        """
        return self._prime_limit

    def ratio_pitch(self, frequency_ratio: FrequencyRatio) -> PrimeLimitPitchT:
        """
        Convenience function to create a pitch from a frequency ratio
        defining the resulting pitch by the interval from the zero
        element.

        The frequency ratio must be an element of the rational numbers
        and its biggest prime factor must not exceed the prime limit
        of this tuning.

        :param frequency_ratio: A frequency ratio object

        :raises ValueError: If biggest prime factor exceeds the limit
        """

        vector = frequency_ratio.to_monzo()

        len_vector = len(vector)
        len_base = len(self.lattice.base)

        if len_vector > len_base:
            raise ValueError(
                f'Frequency ratio {frequency_ratio.short_repr} surpasses '
                f'prime limit of {self.prime_limit}'
            )

        vector = pad_tuple(vector, 0, len_base)
        return self.vec_pitch(vector)

    def ratio_interval(
        self, frequency_ratio: FrequencyRatio
    ) -> PrimeLimitIntervalT:
        """
        Convenience function to create an interval from a frequency ratio.
        The frequency ratio must be an element of the rational numbers
        and its biggest prime factor must not exceed the prime limit
        of this tuning.

        :param frequency_ratio: A frequency ratio object

        :raises ValueError: If biggest prime factor exceeds the limit
        """

        vector = frequency_ratio.to_monzo()

        len_vector = len(vector)
        len_base = len(self.lattice.base)

        if len_vector > len_base:
            raise ValueError(
                f'Frequency ratio {frequency_ratio.short_repr} surpasses '
                f'prime limit of {self.prime_limit}'
            )

        vector = pad_tuple(vector, 0, len_base)
        return self.vec_interval(vector)

    def ratio_pc_scale(
        self,
        pc_frequency_ratios: Optional[Iterable[FrequencyRatio]] = None,
        root_bi_index: int = 0,
    ) -> PrimeLimitScaleT:
        """
        Constructs a scale from a list of frequency ratios representing
        successive pitch classes (meaning all ratios have to be between
        the unison ratio (1/1) and the equivalency ratio). The pitch
        class ratios are assumed to be in the order they appear in the
        scale, meaning that the following expression will result in
        the G-B-D triad:

        >>> from xenharmlib import PrimeLimitTuning
        >>>
        >>> tuning = PrimeLimitTuning(5)
        >>> scale = tuning.ratio_pc_scale(
        ...    [
        ...        FrequencyRatio(3, 2),
        ...        FrequencyRatio(15, 8),
        ...        FrequencyRatio(10, 9)
        ...    ],
        ... )

        :param ratio_strs: A list of ratio string expressions
        :param root_bi_index: The base interval index of the root pitch
            (optional, defaults to 0)

        :raises ValueError: If one of the frequency ratios is not
            between the unison ratio and the equivalency ratio
        :raises ValueError: If a prime factor of one of the frequency
            ratios exceeds the prime limit of this tuning
        """

        if pc_frequency_ratios is None:
            return self.scale()

        pc_indices = []

        for pc_frequency_ratio in pc_frequency_ratios:

            if not (FrequencyRatio(1) <= pc_frequency_ratio < self.eq_ratio):
                raise ValueError(
                    f'Frequency ratios must all be between 1 and '
                    f'{self.eq_ratio.short_repr}.'
                )

            vector = pc_frequency_ratio.to_monzo()
            len_vector = len(vector)
            len_base = len(self.lattice.base)

            if len_vector > len_base:
                raise ValueError(
                    f'Frequency ratio {pc_frequency_ratio.short_repr} '
                    f'surpasses prime limit of {self.prime_limit}'
                )

            vector = pad_tuple(vector, 0, len_base)
            lattice_point = self.lattice.point(vector)
            pc_indices.append(lattice_point)

        return self.pc_scale(pc_indices, root_bi_index)

    def ratio_scale(
        self, frequency_ratios: Optional[Iterable[FrequencyRatio]] = None
    ) -> PrimeLimitScaleT:
        """
        Convenience function to create a scale from an iterable
        of frequency ratios, all refering to the interval distance
        of the scale pitches to the zero element, e.g. in 5 limit
        tuning, creating a major chord on C1 can be done like this:

        >>> from xenharmlib import PrimeLimitTuning
        >>>
        >>> tuning = PrimeLimitTuning(5)
        >>> scale = tuning.ratio_scale(
        ...    [FrequencyRatio(2, 1), FrequencyRatio(5, 2), FrequencyRatio(3)],
        ... )
        >>> scale
        PrimeLimitPitchScale([2, 5/2, 3], 5-Limit)

        :param frequency_ratios: An iterable of frequency ratio objects

        :raises ValueError: If a prime factor of one of the frequency
            ratios exceeds the prime limit of this tuning
        """

        if frequency_ratios is None:
            return self.scale()

        return self.scale(
            [self.ratio_pitch(ratio) for ratio in frequency_ratios]
        )

    def ratio_interval_seq(
        self, frequency_ratios: Optional[Iterable[FrequencyRatio]] = None
    ) -> PrimeLimitIntervalSeqT:
        """
        Convenience function to create an interval sequence from
        an iterable of frequency ratios. The frequency ratios must
        all be elements of the rational numbers and their biggest
        prime factors must not exceed the prime limit of this tuning.

        :param frequency_ratios: An iterable of frequency ratio objects

        :raises ValueError: If a prime factor of one of the frequency
            ratios exceeds the prime limit of this tuning
        """

        if frequency_ratios is None:
            return self.interval_seq()

        return self.interval_seq(
            [self.ratio_interval(ratio) for ratio in frequency_ratios]
        )

    def ratio_interval_fan(
        self, frequency_ratios: Optional[Iterable[FrequencyRatio]] = None
    ) -> PrimeLimitIntervalFanT:
        """
        Convenience function to create an interval fan from an
        iterable of frequency ratios. The frequency ratios must
        all be elements of the rational numbers and their biggest
        prime factors must not exceed the prime limit of this tuning.

        :param frequency_ratios: An iterable of frequency ratio objects

        :raises ValueError: If a prime factor of one of the frequency
            ratios exceeds the prime limit of this tuning
        """

        if frequency_ratios is None:
            return self.interval_fan()

        return self.interval_fan(
            [self.ratio_interval(ratio) for ratio in frequency_ratios]
        )

    def ratio_seq(
        self, frequency_ratios: Optional[Iterable[FrequencyRatio]] = None
    ) -> PrimeLimitSeqT:
        """
        Convenience function to create a sequence from an iterable
        of frequency ratios, all refering to the interval distance
        of the sequence pitches to the zero element, e.g. in 5 limit
        tuning, creating a major chord sequence on C1 can be done
        like this:

        >>> from xenharmlib import PrimeLimitTuning
        >>>
        >>> tuning = PrimeLimitTuning(5)
        >>> scale = tuning.ratio_seq(
        ...    [FrequencyRatio(2, 1), FrequencyRatio(5, 2), FrequencyRatio(3)],
        ... )
        >>> scale
        PrimeLimitPitchSeq([2, 5/2, 3], 5-Limit)

        :param frequency_ratios: An iterable of frequency ratio objects

        :raises ValueError: If a prime factor of one of the frequency
            ratios exceeds the prime limit of this tuning
        """

        if frequency_ratios is None:
            return self.seq()

        return self.seq(
            [self.ratio_pitch(ratio) for ratio in frequency_ratios]
        )

    def rs_pitch(self, ratio_str: str) -> PrimeLimitPitchT:
        """
        Convenience function to create a pitch from a frequency ratio
        string expression, defining the resulting pitch by the interval
        from the zero element. String expressions can be two natural
        numbers separated by a slash (e.g. '5/4') or a single number
        (e.g. '3', refering to the 3/1 ratio)

        :param ratio_str: The ratio string expression

        :raises ValueError: If a prime factor of the frequency ratio
            exceeds the prime limit of this tuning
        :raises ValueError: If expression was ill-formatted
        """

        if not isinstance(ratio_str, str):
            raise ValueError(
                f'\'{ratio_str}\' is not a valid ratio string expression'
            )

        slash_count = ratio_str.count('/')

        if slash_count == 1:
            n, _, d = ratio_str.partition('/')
            if not (n.isdigit() and d.isdigit()):
                raise ValueError(
                    f'\'{ratio_str}\' is not a valid ratio string expression'
                )
            n, d = int(n), int(d)

        elif slash_count == 0:
            if not (ratio_str.isdigit()):
                raise ValueError(
                    f'\'{ratio_str}\' is not a valid ratio string expression'
                )
            n, d = int(ratio_str), 1

        else:
            raise ValueError(
                f'\'{ratio_str}\' is not a valid ratio string expression'
            )

        ratio = FrequencyRatio(n, d)
        return self.ratio_pitch(ratio)

    def rs_interval(self, ratio_str: str) -> PrimeLimitIntervalT:
        """
        Convenience function to create an interval from a frequency
        ratio string expression. String expressions can be two natural
        numbers separated by a slash (e.g. '5/4') or a single number
        (e.g. '3', refering to the 3/1 ratio)

        :param ratio_str: The ratio string expression

        :raises ValueError: If a prime factor of the frequency ratio
            exceeds the prime limit of this tuning
        :raises ValueError: If expression was ill-formatted
        """

        if not isinstance(ratio_str, str):
            raise ValueError(
                f'\'{ratio_str}\' is not a valid ratio string expression'
            )

        slash_count = ratio_str.count('/')

        if slash_count == 1:
            n, _, d = ratio_str.partition('/')
            if not (n.isdigit() and d.isdigit()):
                raise ValueError(
                    f'\'{ratio_str}\' is not a valid ratio string expression'
                )
            n, d = int(n), int(d)

        elif slash_count == 0:
            if not (ratio_str.isdigit()):
                raise ValueError(
                    f'\'{ratio_str}\' is not a valid ratio string expression'
                )
            n, d = int(ratio_str), 1

        else:
            raise ValueError(
                f'\'{ratio_str}\' is not a valid ratio string expression'
            )

        ratio = FrequencyRatio(n, d)
        return self.ratio_interval(ratio)

    def rs_scale(
        self,
        ratio_strs: Optional[Iterable[str]] = None
    ) -> PrimeLimitScaleT:
        """
        Convenience function to create a scale from an iterable of
        frequency ratio expressions, all refering to the interval
        distance of the scale pitches to the zero element, e.g. in
        5 limit tuning, creating a major chord on C1 can be done
        like this:

        >>> from xenharmlib import PrimeLimitTuning
        >>>
        >>> tuning = PrimeLimitTuning(5)
        >>> tuning.rs_scale(['2', '5/2', '3'])
        PrimeLimitPitchScale([2, 5/2, 3], 5-Limit)

        :param ratio_strs: A list of ratio string expressions

        :raises ValueError: If a prime factor of one of the frequency
            ratios exceeds the prime limit of this tuning
        :raises ValueError: If expression was ill-formatted
        """

        if ratio_strs is None:
            return self.scale()

        pitches = []

        for ratio_str in ratio_strs:
            pitch = self.rs_pitch(ratio_str)
            pitches.append(pitch)

        return self.scale(pitches)

    def rs_pc_scale(
        self,
        ratio_strs: Optional[Iterable[str]] = None,
        root_bi_index: int = 0,
    ) -> PrimeLimitScaleT:
        """
        Constructs a scale from a list of frequency ratios given as strings
        representing successive pitch classes (meaning all ratios have to
        be between the unison ratio (1/1) and the equivalency ratio). The
        pitch class ratios are assumed to be in the order they appear in
        the scale, meaning that the following expression will result in
        the G-B-D triad:

        >>> from xenharmlib import PrimeLimitTuning
        >>>
        >>> tuning = PrimeLimitTuning(5)
        >>> tuning.rs_pc_scale(['3/2', '15/8', '10/9'])
        PrimeLimitPitchScale([3/2, 15/8, 20/9], 5-Limit)

        :param ratio_strs: A list of ratio string expressions
        :param root_bi_index: The base interval index of the root pitch
            (optional, defaults to 0)

        :raises ValueError: If one of the frequency ratios is not
            between the unison ratio and the equivalency ratio
        :raises ValueError: If a prime factor of one of the frequency
            ratios exceeds the prime limit of this tuning
        :raises ValueError: If expression was ill-formatted
        """

        if ratio_strs is None:
            return self.scale()

        ratios = []

        for ratio_str in ratio_strs:

            if not isinstance(ratio_str, str):
                raise ValueError(
                    f'\'{ratio_str}\' is not a valid '
                    f'ratio string expression'
                )

            slash_count = ratio_str.count('/')

            if slash_count == 1:
                n, _, d = ratio_str.partition('/')
                if not (n.isdigit() and d.isdigit()):
                    raise ValueError(
                        f'\'{ratio_str}\' is not a valid '
                        f'ratio string expression'
                    )
                n, d = int(n), int(d)

            elif slash_count == 0:
                if not (ratio_str.isdigit()):
                    raise ValueError(
                        f'\'{ratio_str}\' is not a valid '
                        f'ratio string expression'
                    )
                n, d = int(ratio_str), 1

            else:
                raise ValueError(
                    f'\'{ratio_str}\' is not a valid ratio string expression'
                )

            ratio = FrequencyRatio(n, d)
            ratios.append(ratio)

        return self.ratio_pc_scale(ratios, root_bi_index)

    def rs_interval_seq(
        self,
        ratio_strs: Optional[Iterable[str]] = None
    ) -> PrimeLimitIntervalSeqT:
        """
        Convenience function to create an interval sequence from
        an iterable of frequency ratio string expressions. String
        expressions can be two natural numbers separated by a slash
        (e.g. '5/4') or a single number (e.g. '3', refering to the
        3/1 ratio)

        :param ratio_strs: A list of ratio string expressions

        :raises ValueError: If a prime factor of one of the frequency
            ratios exceeds the prime limit of this tuning
        :raises ValueError: If expression was ill-formatted
        """

        if ratio_strs is None:
            return self.interval_seq()

        intervals = []

        for ratio_str in ratio_strs:
            interval = self.rs_interval(ratio_str)
            intervals.append(interval)

        return self.interval_seq(intervals)

    def rs_interval_fan(
        self, ratio_strs: Optional[Iterable[str]] = None
    ) -> PrimeLimitIntervalFanT:
        """
        Convenience function to create an interval fan from an
        iterable of frequency ratio string expressions. String
        expressions can be two natural numbers separated by a
        slash (e.g. '5/4') or a single number (e.g. '3',
        refering to the 3/1 ratio)

        :param ratio_strs: A list of ratio string expressions

        :raises ValueError: If a prime factor of one of the frequency
            ratios exceeds the prime limit of this tuning
        :raises ValueError: If expression was ill-formatted
        """

        if ratio_strs is None:
            return self.interval_fan()

        intervals = []

        for ratio_str in ratio_strs:
            interval = self.rs_interval(ratio_str)
            intervals.append(interval)

        return self.interval_fan(intervals)

    def rs_seq(
        self,
        ratio_strs: Optional[Iterable[str]] = None
    ) -> PrimeLimitSeqT:
        """
        Convenience function to create a sequence from an iterable of
        frequency ratio expressions, all refering to the interval
        distance of the sequence pitches to the zero element, e.g.
        in 5 limit tuning, creating a major chord sequence on C1
        can be done like this:

        >>> from xenharmlib import PrimeLimitTuning
        >>>
        >>> tuning = PrimeLimitTuning(5)
        >>> tuning.rs_seq(['2', '5/2', '3'])
        PrimeLimitPitchSeq([2, 5/2, 3], 5-Limit)

        :param ratio_strs: A list of ratio string expressions

        :raises ValueError: If a prime factor of one of the frequency
            ratios exceeds the prime limit of this tuning
        :raises ValueError: If expression was ill-formatted
        """

        if ratio_strs is None:
            return self.seq()

        pitches = []

        for ratio_str in ratio_strs:
            pitch = self.rs_pitch(ratio_str)
            pitches.append(pitch)

        return self.seq(pitches)

    def ec_interval_fan(self, expr: str) -> PrimeLimitIntervalFanT:
        """
        Creates an interval fan from an enumerated chord expression,
        e.g. '4:5:6' ^= [4/4, 5/4, 6/4] ^= [1/1, 5/4, 3/2]

        An enumerated chord expression is a short form to notate
        frequency ratios of an interval fan as a sequence of
        integers where each integer is divided by the first
        integer.

        :param expr: An expression of the form '4:5:6'

        :raises ValueError: If expression string is invalid
        :raises ValueError: If expression contains a number
            that violates the prime limit of this tuning
        """

        if expr.count(':') < 1:
            raise ValueError('Invalid expression')

        digit_strs = expr.split(':')
        digits = []

        for digit_str in digit_strs:
            if not digit_str.isdigit():
                raise ValueError('Invalid expression')
            digits.append(int(digit_str))

        intervals = []
        for digit in digits:
            intervals.append(
                self.ratio_interval(FrequencyRatio(digit, digits[0]))
            )

        return self.interval_fan(intervals)
