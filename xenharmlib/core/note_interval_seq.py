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

from ..exc import IncompatibleOriginContexts
from .notes import NoteIntervalABC
from .notes import NatAccNoteInterval
from .interval_seq import IntervalSeq
from .protocols import Index
from .protocols import PeriodicIndex
from typing import Optional
from typing import TypeVar
from typing import List

NoteIntervalT = TypeVar('NoteIntervalT', bound=NoteIntervalABC)
IndexT = TypeVar('IndexT', bound=Index)


class NoteIntervalSeq(IntervalSeq[IndexT, NoteIntervalT]):
    """
    Base class for note interval sequences

    :param notation: The notation this interval sequences originates from
    :param intervals: A list of intervals from the same notation
    """

    def __init__(
        self,
        notation,
        intervals: Optional[List[NoteIntervalT]] = None
    ):
        super().__init__(notation, intervals)
        self.notation = notation

    @property
    def tuning(self):
        """
        The tuning associated with this note interval sequence
        """
        return self.notation.tuning

    @property
    def pitch_interval_seq(self):
        """
        Returns the underlying pitch interval sequence
        """
        return self.tuning.interval_seq(
            [interval.pitch_interval for interval in self]
        )

    def __repr__(self):
        interval_symbols = []
        for interval in self:
            interval_symbols.append(interval.short_repr)
        interval_symbols = ', '.join(interval_symbols)
        interval_symbols = '[' + interval_symbols + ']'
        return (
            f'{self.__class__.__name__}('
            f'{interval_symbols}, '
            f'{self.tuning.name})'
        )

    def is_notated_same(self, other) -> bool:
        """
        Returns True, if this interval sequence is notated the same
        way as the other sequence, False otherwise

        :param other: Another interval sequence to compare
        """

        if len(self) != len(other):
            return False

        if other.notation is not self.notation:
            raise IncompatibleOriginContexts(
                'Interval sequences must originate from the same '
                'notation context'
            )

        for a, b in zip(self, other):
            if not a.is_notated_same(b):
                return False

        return True


NatAccNoteIntervalT = TypeVar('NatAccNoteIntervalT', bound=NatAccNoteInterval)
PeriodicIndexT = TypeVar('PeriodicIndexT', bound=PeriodicIndex)


class NatAccNoteIntervalSeq(
    NoteIntervalSeq[PeriodicIndexT, NatAccNoteIntervalT]
):
    """
    Base class for natural/accidental notation interval sequences

    :param notation: The notation this interval sequences originates from
    :param intervals: A list of intervals from the same notation
    """
    pass
