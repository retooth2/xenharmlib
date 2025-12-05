from typing import Self
from typing import List
from typing import TypeVar
from .sd_objects import SDPitch
from .sd_objects import SDPitchInterval
from .sd_objects import SDPitchScale
from .sd_objects import SDPitchIntervalSeq
from ..objects import PeriodicScale
from ..protocols import PeriodicPitchLike
from ...exc import InvalidGenerator
from ...exc import IncompatibleOriginContexts


class PeriodicSDPitch(SDPitch, PeriodicPitchLike):
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

    def __init__(self, tuning, frequency, pitch_index: int):

        super().__init__(tuning, frequency, pitch_index)
        tuning_len = len(tuning)

        self._pc_index = pitch_index % tuning_len
        self._bi_index = pitch_index // tuning_len

    @property
    def pitch_index(self) -> int:
        """
        The index of this pitch as an integer
        """
        return self._pitch_index

    @property
    def pc_index(self):
        """
        The pitch class index of this pitch
        """
        return self._pc_index

    @property
    def bi_index(self):
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

        tuning_len = len(self.tuning)
        bi_index = self._bi_index + bi_diff
        pitch_index = self._pc_index + bi_index * tuning_len
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

    def get_generator_index(self, generator_pitch: Self):
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
            pc_index = (pc_index + gen_pc) % len(self.tuning)

        return g_index


PitchT = TypeVar('PitchT', bound=PeriodicSDPitch)


class PeriodicSDPitchInterval(SDPitchInterval[PitchT]):
    """
    The pitch interval class for periodic tunings.
    """

    def get_generator_distance(self, generator_pitch: PitchT) -> int:
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

        return min(i_diff, len(self.tuning) - i_diff)


class PeriodicSDPitchScale(
    SDPitchScale[PitchT], PeriodicScale[PitchT]
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


PitchIntervalT = TypeVar('PitchIntervalT', bound=PeriodicSDPitchInterval)


class PeriodicSDPitchIntervalSeq(SDPitchIntervalSeq[PitchIntervalT]):
    """
    Pitch interval sequence class for periodic tunings

    :param tuning: The tuning this pitch interval sequence originates from
    :param intervals: A sequence of pitch intervals
    """
    pass
