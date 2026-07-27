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
The note core module implements primitives to handle sequences of notes
"""

from ..exc import IncompatibleOriginContexts
from .notes import NoteABC
from .notes import PeriodicNoteABC
from .notes import NoteIntervalABC
from .notes import NatAccNote
from .protocols import Index
from .protocols import PeriodicIndex
from .freq_repr_seq import FreqReprSeq
from .freq_repr_seq import PeriodicFreqReprSeq
from typing import Self
from typing import Tuple
from typing import Generic
from typing import Optional
from typing import TypeVar
from typing import List
from typing import Iterable

PitchT = TypeVar('PitchT', bound=NoteABC)
IndexT = TypeVar('IndexT', bound=Index)


class NoteSeq(FreqReprSeq[IndexT, PitchT], Generic[IndexT, PitchT]):
    """
    Base class for all sequences of pitches

    :param tuning: The tuning this pitch sequence originates from
    :param elements: A sequence of pitches
    """

    def __init__(self, notation, elements: Optional[Iterable[PitchT]] = None):
        super().__init__(notation, elements)
        self._notation = notation

    @property
    def is_zero_normalized(self) -> bool:
        """
        Returns True if this function is zero normalized, meaning
        that the first element of the sequence is notated the same
        as the zero element of the origin context (typically C0
        in western-like notations)
        """

        if len(self) == 0:
            raise ValueError(
                'is_zero_normalized is not defined on empty sequence'
            )

        return self[0].is_notated_same(self.origin_context.zero_element)

    @property
    def notation(self):
        """
        The notation associated with this note sequence
        """
        return self._notation

    @property
    def tuning(self):
        """
        The tuning associated with this note sequence
        """
        return self.notation.tuning

    def transpose(self, diff: IndexT | NoteIntervalABC) -> Self:
        """
        Transposes the sequence by the given interval

        :param diff: A note interval or pitch difference
        """

        if not isinstance(diff, NoteIntervalABC):
            return self.enharm_strategy.note_seq_transpose(self, diff)

        interval = diff
        transposed = []
        for notes in self:
            transposed.append(notes.transpose(interval))

        return self.notation.seq(transposed)

    @property
    def enharm_strategy(self):
        """
        A proxy property to the enharmonic strategy of the notation
        """
        return self.notation.enharm_strategy

    @property
    def pitch_seq(self):
        return self.tuning.seq([element.pitch for element in self])

    @property
    def pitch_indices(self) -> List[IndexT]:
        return [element.pitch_index for element in self]

    def is_notated_same(self, other: Self) -> bool:
        """
        Returns True if this sequence has the exact same notes
        as the other sequence while ignoring possible enharmonic
        equivalence.
        """

        if len(self) != len(other):
            return False

        for i, note in enumerate(self):
            if not other[i].is_notated_same(note):
                return False

        return True

    def __repr__(self):
        note_symbols = []
        for note in self:
            note_symbols.append(note.short_repr)
        note_symbols = ', '.join(note_symbols)
        note_symbols = '[' + note_symbols + ']'
        return (
            f'{self.__class__.__name__}('
            f'{note_symbols}, '
            f'{self.tuning.name})'
        )


PeriodicNoteT = TypeVar('PeriodicNoteT', bound=PeriodicNoteABC)
PeriodicIndexT = TypeVar('PeriodicIndexT', bound=PeriodicIndex)


class PeriodicNoteSeq(
    NoteSeq[PeriodicIndexT, PeriodicNoteT], PeriodicFreqReprSeq[PeriodicNoteT]
):
    """
    Note sequence class for periodic notations. Implements
    customized set operations (for when you want to treat
    equivalent notes the same as equal notes).
    """

    @property
    def pc_indices(self) -> List[PeriodicIndexT]:
        """
        Returns a list of pitch class indices in
        the order they appear in this sequence.
        """
        return [note.pc_index for note in self]

    def is_notated_equivalent(self, other: Self) -> bool:
        """
        Returns True if this sequence has, apart from the base
        interval, the exact same notes as the other while
        ignoring possible enharmonic equivalence.
        """

        if self.tuning.eq_ratio != other.tuning.eq_ratio:
            raise IncompatibleOriginContexts(
                'Equivalency can only be tested for sequences from tunings '
                'with the same equivalency interval'
            )

        if len(self) != len(other):
            return False

        for a, b in zip(self, other):
            if not a.is_notated_equivalent(b):
                return False

        return True


NatAccNoteT = TypeVar('NatAccNoteT', bound=NatAccNote)


class NatAccNoteSeq(PeriodicNoteSeq[PeriodicIndexT, NatAccNoteT]):
    """
    Basic note sequence class for natural/accidental notations.
    """

    @property
    def nat_indices(self) -> List[int]:
        """
        A list of the natural indices of notes in this sequence

        The natural index is the number of natural steps needed
        to reach the natural part of this note, so for example in
        a notation with naturals C, D, E, F, G, A, B the
        natural index of C#-0 is 0, D-1 is 8, Eb-3 is 16
        """
        indices = []
        for note in self:
            indices.append(note.nat_index)
        return indices

    @property
    def natc_indices(self) -> List[int]:
        """
        A list of natural class indices of notes in this sequence.

        The natural class index is the equivalency class
        of the natural index, so for example in a notation
        with naturals C, D, E, F, G, A, B the notes C#-3
        and Cb-0 both have natural class index 0 while F#-2
        and Fbb-5 have natural class index 3
        """
        indices = []
        for note in self:
            indices.append(note.natc_index)
        return indices

    @property
    def nat_bi_indices(self) -> List[int]:
        """
        A list of natural base interval indices represented in this
        sequence. The natural base interval is the base interval index
        of the natural part of the note, so e.g. 0 for B#-0
        """
        indices = []
        for note in self:
            indices.append(note.nat_bi_index)
        return indices

    @property
    def acc_sum_vectors(self) -> List[Tuple[int]]:
        """
        A list of (unweighted) accidental sum vectors for
        each note in the sequence
        """
        vectors = []
        for note in self:
            vectors.append(note.acc_sum_vector)
        return vectors

    @property
    def acc_diff_vectors(self) -> List[Tuple[PeriodicIndexT]]:
        """
        A list of (weighted) accidental diff vectors for
        each note in the sequence
        """
        vectors = []
        for note in self:
            vectors.append(note.acc_diff_vector)
        return vectors

    @property
    def acc_values(self) -> List[PeriodicIndexT]:
        """
        A list of accidental values for each note in the sequence
        """
        values = []
        for note in self:
            values.append(note.acc_value)
        return values

    @property
    def nat_pc_indices(self) -> List[PeriodicIndexT]:
        """
        A list of pitch class indices of the natural part of each note
        in the sequence (e.g. in 12-EDO [0, 2, 4] for [C#0, D1, Eb2])
        """
        indices = []
        for note in self:
            indices.append(note.nat_pc_index)
        return indices

    @property
    def nat_pitch_indices(self) -> List[PeriodicIndexT]:
        """
        A list of pitch indices of the natural part of each note
        in the sequence (e.g. in 12-EDO [0, 14, 18] for [C#0, D1, Eb2])
        """
        indices = []
        for note in self:
            indices.append(note.nat_pitch_index)
        return indices

    @property
    def natc_symbols(self) -> List[str]:
        """
        The symbol list for the natural part of each note in the
        sequence (e.g. in 12-EDO ['C', 'G', 'B'] for [C#0, Gb1, B4])
        """
        symbols = []
        for note in self:
            symbols.append(note.natc_symbol)
        return symbols

    @property
    def acc_symbols(self) -> List[str]:
        """
        The symbol list for the accidental part of each note in the
        sequence (e.g. in 12-EDO ['#', 'b', ''] for [C#0, Gb1, B4])
        """
        symbols = []
        for note in self:
            symbols.append(note.acc_symbol)
        return symbols

    @property
    def pc_symbols(self) -> List[str]:
        """
        The symbol list for the pitch classes represented in the
        sequence (e.g. in 12-EDO ['C#', 'Gb', 'B'] for [C#0, Gb1, B4])
        """
        symbols = []
        for note in self:
            symbols.append(note.pc_symbol)
        return symbols

    @property
    def acc_directions(self) -> List[int]:
        """
        The list of accidental directions of notes in the sequence
        (0 if the note is a natural, 1 if the note is a sharp note,
        -1 if it is a flat note, so for example in 31-EDO [0, 1, -1]
        for [C0, ^B#2, Cb0])
        """
        directions = []
        for note in self:
            directions.append(note.acc_direction)
        return directions
