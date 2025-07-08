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

from .notes import NoteIntervalABC
from .notes import NatAccNoteInterval
from .interval_seq import IntervalSeq
from typing import Optional
from typing import TypeVar
from typing import List

NoteIntervalT = TypeVar('NoteIntervalT', bound=NoteIntervalABC)


class NoteIntervalSeq(IntervalSeq[NoteIntervalT]):
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


NatAccNoteIntervalT = TypeVar('NatAccNoteIntervalT', bound=NatAccNoteInterval)


class NatAccNoteIntervalSeq(NoteIntervalSeq[NatAccNoteIntervalT]):
    """
    Base class for natural/accidental notation interval sequences

    :param notation: The notation this interval sequences originates from
    :param intervals: A list of intervals from the same notation
    """
    pass
