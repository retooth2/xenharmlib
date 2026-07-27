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

from .pitch import Pitch
from .pitch import PeriodicPitch
from .pitch import EDPitch
from .protocols import Index
from .protocols import PeriodicIndex
from .freq_repr_seq import FreqReprSeq
from .freq_repr_seq import PeriodicFreqReprSeq
from typing import Generic
from typing import Optional
from typing import TypeVar
from typing import List
from typing import Iterable

PitchT = TypeVar('PitchT', bound=Pitch)
IndexT = TypeVar('IndexT', bound=Index)


class PitchSeq(FreqReprSeq[IndexT, PitchT], Generic[IndexT, PitchT]):
    """
    Base class for all sequences of pitches

    :param tuning: The tuning this pitch sequence originates from
    :param elements: A sequence of pitches
    """

    def __init__(self, tuning, elements: Optional[Iterable[PitchT]] = None):
        super().__init__(tuning, elements)
        self.tuning = tuning

    @property
    def is_zero_normalized(self) -> bool:

        if len(self) == 0:
            raise ValueError(
                'is_zero_normalized is not defined on empty sequence'
            )

        return self[0] == self.tuning.zero_element

    @property
    def pitch_indices(self) -> List[IndexT]:
        return [element.pitch_index for element in self]

    def __repr__(self):
        return (
            f'{self.__class__.__name__}('
            f'{self.pitch_indices}, '
            f'{self.tuning.name})'
        )


PeriodicPitchT = TypeVar('PeriodicPitchT', bound=PeriodicPitch)
PeriodicIndexT = TypeVar('PeriodicIndexT', bound=PeriodicIndex)


class PeriodicPitchSeq(
    PitchSeq[PeriodicIndexT, PeriodicPitchT],
    PeriodicFreqReprSeq[PeriodicPitchT]
):
    """
    Pitch sequence class for periodic tunings

    :param tuning: The tuning this pitch sequence originates from
    :param elements: A sequence of pitch
    """

    @property
    def pc_indices(self) -> List[IndexT]:
        return [element.pc_index for element in self]


class EDPitchSeq(PeriodicPitchSeq[int, EDPitch]):
    """
    The pitch sequence class for equal division tunings

    :param tuning: The tuning this pitch sequence originates from
    :param elements: A sequence of pitches
    """

    pass


class EDOPitchSeq(EDPitchSeq):
    """
    The pitch sequence class for 'equal division of the octave' tunings

    :param tuning: The tuning this pitch sequence originates from
    :param elements: A sequence of pitches
    """

    pass
