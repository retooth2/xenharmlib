from __future__ import annotations
from typing import TypeVar
from typing import List
from typing import Optional


from .sd_context import SDTuning
from .psd_objects import PeriodicSDPitch
from .psd_objects import PeriodicSDPitchInterval
from .psd_objects import PeriodicSDPitchScale
from .psd_objects import PeriodicSDPitchIntervalSeq

from ..frequencies import Frequency
from ..frequencies import FrequencyRatio
from ...exc import InvalidPitchClassIndex


PitchT = TypeVar('PitchT', bound=PeriodicSDPitch)
IntervalT = TypeVar('IntervalT', bound=PeriodicSDPitchInterval)
ScaleT = TypeVar('ScaleT', bound=PeriodicSDPitchScale)
IntervalSeqT = TypeVar(
    'IntervalSeqT',
    bound=PeriodicSDPitchIntervalSeq
)


class PeriodicSDTuning(
    SDTuning[
        PitchT,
        IntervalT,
        ScaleT,
        IntervalSeqT
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
        pitch_cls: type[PitchT],
        pitch_interval_cls: type[IntervalT],
        pitch_scale_cls: type[ScaleT],
        pitch_interval_seq_cls: type[IntervalSeqT],
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

    def get_ring_number(self, pitch: PitchT) -> int:
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
    def generator_pitches(self) -> List[PitchT]:
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
