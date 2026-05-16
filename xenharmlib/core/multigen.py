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
This module implements tunings and musical objects relating to
multi-generator tunings.

A multi-generator tuning describes the frequency space as a lattice
in which each integer vector :math:`(x_1, ..., x_n)` represents the
exponents in the expression `g_1^{x_1} \\cdot ... \\cdot g_n^{x_n}`
built from a generator vector :math:`(g_1, ..., g_n)`

Multi-generator tunings are an abstraction of JI prime limit tuning
classes, that can hold arbitrary generators. Because of this they
have multiple applications in temperament theory.
"""

from typing import Tuple
from typing import Optional
from typing import Iterable
from typing import TypeVar
from .frequencies import Hz440C0
from .frequencies import Frequency
from .frequencies import FrequencyRatio
from .tunings import PeriodicTuning
from .lattice import Lattice
from .lattice import LatticePoint
from .pitch import PeriodicPitch
from .pitch import PeriodicPitchInterval
from .pitch_scale import PeriodicPitchScale
from .pitch_interval_seq import PeriodicPitchIntervalSeq


class MultiGenPitch(PeriodicPitch[LatticePoint]):

    @property
    def short_repr(self) -> str:
        return self.pitch_index.short_repr

    @property
    def pc_short_repr(self) -> str:
        return self.pc_index.short_repr

    def __repr__(self) -> str:
        base_strings = [ratio.short_repr for ratio in self.pitch_index.base]
        base_string = ', '.join(base_strings)
        return (
            f'{self.__class__.__name__}({self.pitch_index.vector}, '
            f'G=({base_string}))'
        )


class MultiGenPitchInterval(
    PeriodicPitchInterval[LatticePoint, MultiGenPitch]
):

    @property
    def short_repr(self) -> str:
        return self.pitch_diff.short_repr

    def __repr__(self) -> str:
        base_strings = [ratio.short_repr for ratio in self.pitch_diff.base]
        base_string = ', '.join(base_strings)
        return (
            f'{self.__class__.__name__}({self.pitch_diff.vector}, '
            f'G=({base_string}))'
        )


class MultiGenPitchScale(PeriodicPitchScale[LatticePoint, MultiGenPitch]):

    def __repr__(self) -> str:
        base_strings = [ratio.short_repr for ratio in self.tuning.lattice.base]
        base_string = ', '.join(base_strings)
        vec_strings = [
            pitch.pitch_index.short_repr for pitch in self
        ]
        vec_string = ', '.join(vec_strings)
        return (
            f'{self.__class__.__name__}([{vec_string}], '
            f'G=({base_string}))'
        )


class MultiGenPitchIntervalSeq(
    PeriodicPitchIntervalSeq[LatticePoint, MultiGenPitchInterval]
):

    def __repr__(self) -> str:
        base_strings = [ratio.short_repr for ratio in self.tuning.lattice.base]
        base_string = ', '.join(base_strings)
        vec_strings = [
            interval.pitch_diff.short_repr for interval in self
        ]
        vec_string = ', '.join(vec_strings)
        return (
            f'{self.__class__.__name__}([{vec_string}], '
            f'G=({base_string}))'
        )


MultiGenPitchT = TypeVar('MultiGenPitchT', bound=MultiGenPitch)
MultiGenIntervalT = TypeVar('MultiGenIntervalT', bound=MultiGenPitchInterval)
MultiGenScaleT = TypeVar('MultiGenScaleT', bound=MultiGenPitchScale)
MultiGenIntervalSeqT = TypeVar(
    'MultiGenIntervalSeqT', bound=MultiGenPitchIntervalSeq
)


class MultiGenTuning(
    PeriodicTuning[
        LatticePoint,
        MultiGenPitchT,
        MultiGenIntervalT,
        MultiGenScaleT,
        MultiGenIntervalSeqT,
    ]
):
    """
    Base class for multi-generator tunings. A multi-generator tuning
    describes the frequency space as a lattice in which each integer
    vector :math:`(x_1, ..., x_n)` represents the exponents in the
    expression `g_1^{x_1} \\cdot ... \\cdot g_n^{x_n}` built from a
    generator vector :math:`(g_1, ..., g_n)`

    :param generators: A tuple of frequency ratios that constitutes
        the generator vector of this tuning
    :param period_vec: A vector of integers that defines the pitch
        difference of the interval that should be considered the
        equivalence interval, so for example in a pythagorean
        tuning with generators 2 and 3, this should be (1, 0)
        for the octave.
    :param ref_frequence: A reference frequency for the zero index
        (optional, defaults to the frequency for C0 in EDO tunings
        for A4 = 440 Hz (about 16.35 Hz))
    """

    def __init__(
        self,
        generators: Tuple[FrequencyRatio, ...],
        period_vec: Tuple[int, ...],
        ref_frequency: Frequency = Hz440C0,
        pitch_cls: type[MultiGenPitchT] = MultiGenPitch,
        pitch_interval_cls: type[MultiGenIntervalT] = MultiGenPitchInterval,
        pitch_scale_cls: type[MultiGenScaleT] = MultiGenPitchScale,
        pitch_interval_seq_cls: type[
            MultiGenIntervalSeqT
        ] = MultiGenPitchIntervalSeq,
    ):

        self._lattice = Lattice(generators)

        if len(generators) != len(period_vec):
            raise ValueError(
                'Period vector must have the same dimensions '
                'as the generator vector'
            )

        period_length = self._lattice.point(period_vec)

        super().__init__(
            period_length,
            period_length.frequency_ratio,
            pitch_cls,
            pitch_interval_cls,
            pitch_scale_cls,
            pitch_interval_seq_cls,
            ref_frequency,
        )

    @property
    def lattice(self) -> Lattice:
        """
        The lattice on which this tuning is based upon
        """
        return self._lattice

    @property
    def zero_index(self) -> LatticePoint:
        """
        The lattice point representing the zero index
        """
        return self.lattice.zero

    # we overwrite diff-interval builder methods to provide for
    # nicer error messages in case a wrong parameter is given

    def diff_interval(
        self,
        pitch_diff: LatticePoint
    ) -> MultiGenIntervalT:
        """
        Returns an interval the size of a given pitch index difference.

        :param pitch_diff: The pitch index difference
        """

        if not self.lattice.contains_point(pitch_diff):
            raise ValueError(
                'Pitch difference must be a lattice point from the '
                'same lattice as this tuning was configured with.'
            )

        return super().diff_interval(pitch_diff)

    def get_frequency_for_index(self, pitch_index: LatticePoint) -> Frequency:
        """
        Returns the frequency for a given pitch index
        """

        if not self.lattice.contains_point(pitch_index):
            raise ValueError(
                'Pitch index must be a lattice point from the '
                'same lattice as this tuning was configured with.'
            )

        return self.ref_frequency * pitch_index.frequency_ratio

    @property
    def name(self) -> str:
        ratios = ', '.join([ratio.short_repr for ratio in self.lattice.base])
        return f'MultiGenTuning({ratios})'

    def __repr__(self) -> str:
        ratios = ', '.join([ratio.short_repr for ratio in self.lattice.base])
        return f'MultiGenTuning({ratios})'

    def vec_pitch(self, vector: Tuple[int, ...]) -> MultiGenPitchT:
        """
        Convenience function to create a pitch from an integer vector
        defining the exponents of the generators of this tuning, so
        for example in a pythagorean tuning with generators 2 and
        3 input parameter (-1, 1) produces the pitch equivalent to
        the note G0

        :param vector: An integer tuple
        """

        lattice_point = self.lattice.point(vector)
        return self.pitch(lattice_point)

    def vec_interval(self, vector: Tuple[int, ...]) -> MultiGenIntervalT:
        """
        Convenience function to create an interval from an integer
        vector defining the exponents of the generators of this
        tuning, so for example in a pythagorean tuning with
        generators 2 and 3 input parameter (-1, 1) produces
        the perfect fifth interval

        :param vector: An integer tuple
        """

        lattice_point = self.lattice.point(vector)
        return self.diff_interval(lattice_point)

    def vec_scale(
        self, vectors: Optional[Iterable[Tuple[int, ...]]]
    ) -> MultiGenScaleT:
        """
        Convenience function to create a scale from an iterable
        of integer vectors defining all the exponents of the
        generators of each respective pitch in the scale, so
        for example in a pythagorean tuning with generators
        2 and 3 the value [(0, 0), (-7, 4), (-1, 1)] produces
        the C0 major triad.

        :param vectors: An iterable of integer tuples
        """

        _vectors = [] if vectors is None else vectors
        return self.index_scale([self.lattice.point(v) for v in _vectors])

    def vec_interval_seq(
        self, vectors: Optional[Iterable[Tuple[int, ...]]]
    ) -> MultiGenIntervalSeqT:
        """
        Convenience function to create an interval sequence from
        an iterable of integer vectors defining all the exponents
        of the generators of each respective interval in the
        sequence, so for example in a pythagorean tuning with
        generators 2 and 3 the value [(0, 0), (-7, 4), (-1, 1)]
        produces the interval sequence of the major triad.

        :param vectors: An iterable of integer tuples
        """
        _vectors = [] if vectors is None else vectors
        return self.diff_interval_seq(
            [self.lattice.point(v) for v in _vectors]
        )
