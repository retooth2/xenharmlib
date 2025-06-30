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

from .updown import UpDownNotation
from .updown import UpDownNote
from .updown import UpDownNoteInterval
from .updown import UpDownNoteScale
from .updown import UpDownNoteIntervalSeq
from .updown import DownwardsEnharmStrategy
from .updown import UpwardsEnharmStrategy
from ..core.tunings import EDOTuning


class FlatEnharmStrategy(DownwardsEnharmStrategy):
    pass


class SharpEnharmStrategy(UpwardsEnharmStrategy):
    pass


class WesternNote(UpDownNote):

    def __repr__(self):
        return (
            f'{self.__class__.__name__}('
            f'{self.pc_symbol}, '
            f'{self.nat_bi_index})'
        )


class WesternNoteInterval(UpDownNoteInterval):

    def __repr__(self) -> str:
        return (
            f'{self.__class__.__name__}('
            f'{self.symbol}, {self.number})'
        )


class WesternNoteScale(UpDownNoteScale):

    def __repr__(self):
        note_symbols = []
        for note in self:
            note_symbols.append(note.short_repr)
        note_symbols = ', '.join(note_symbols)
        note_symbols = '[' + note_symbols + ']'
        return (
            f'{self.__class__.__name__}('
            f'{note_symbols})'
        )


class WesternNoteIntervalSeq(UpDownNoteIntervalSeq):

    def __repr__(self):
        interval_symbols = []
        for interval in self:
            interval_symbols.append(interval.short_repr)
        interval_symbols = ', '.join(interval_symbols)
        interval_symbols = '[' + interval_symbols + ']'
        return (
            f'{self.__class__.__name__}('
            f'{interval_symbols})'
        )


class WesternNotation(UpDownNotation):
    """
    WesternNotation is an implementation of the contemporary
    western notation (12 notes per octave, equally tempered,
    A4 set to 440Hz, interval system with perfect and
    imperfect interval qualities, etc)
    """

    def __init__(
        self,
        note_cls=WesternNote,
        note_interval_cls=WesternNoteInterval,
        note_scale_cls=WesternNoteScale,
        note_interval_seq_cls=WesternNoteIntervalSeq,
    ):

        tuning = EDOTuning(12)

        super().__init__(
            tuning,
            note_cls,
            note_interval_cls,
            note_scale_cls,
            note_interval_seq_cls
        )

        # initialize default enharmonic strategy
        self.enharm_strategy = SharpEnharmStrategy(self)

    @property
    def name(self):
        return f'{self.__class__.__name__}'

    def __repr__(self):
        return f'{self.__class__.__name__}(A4=440Hz)'
