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

from .pitch import PitchInterval
from .pitch import PeriodicPitchInterval
from .pitch import EDPitchInterval
from .interval_seq import IntervalSeq
from typing import Optional
from typing import TypeVar
from typing import List

PitchIntervalT = TypeVar('PitchIntervalT', bound=PitchInterval)


class PitchIntervalSeq(IntervalSeq[PitchIntervalT]):
    """
    Base class for all sequences of pitch intervals.
    Interval sequences can be understood as "abstract scales" (for example
    the minor scale *as such*, instead of C minor). Interval sequences have
    multiple applications from templating to structure discovery.

    In line with its Sequence superclass pitch interval sequences implement
    iteration, the 'in' operator, the == operator, item retrieval with
    [], concatenation with +, repeated self-concatenation with *, searching
    with index, and len().

    Like scale types pitch interval sequences also allow partitioning with
    partial, partial_not and partition.

    :param tuning: The tuning this pitch interval sequence originates from
    :param intervals: A sequence of pitch intervals
    """

    def __init__(
        self,
        tuning,
        intervals: Optional[List[PitchIntervalT]] = None
    ):
        super().__init__(tuning, intervals)
        self.tuning = tuning

    def __repr__(self):
        return (
            f'{self.__class__.__name__}('
            f'{self.pitch_diffs}, '
            f'{self.tuning.name})'
        )


PeriodicPitchIntervalT = TypeVar('PeriodicPitchT', bound=PeriodicPitchInterval)


class PeriodicPitchIntervalSeq(PitchIntervalSeq[PeriodicPitchIntervalT]):
    """
    Pitch interval sequence class for periodic tunings

    :param tuning: The tuning this pitch interval sequence originates from
    :param intervals: A sequence of pitch intervals
    """
    pass


class EDPitchIntervalSeq(PeriodicPitchIntervalSeq[EDPitchInterval]):
    """
    The pitch interval sequence class for equal division tunings

    :param tuning: The tuning this pitch interval sequence originates from
    :param intervals: A sequence of pitch intervals
    """
    pass


class EDOPitchIntervalSeq(EDPitchIntervalSeq):
    """
    The pitch interval sequence class for 'equal division of the octave'
    tunings

    :param tuning: The tuning this pitch interval sequence originates from
    :param intervals: A sequence of pitch intervals
    """
    pass
