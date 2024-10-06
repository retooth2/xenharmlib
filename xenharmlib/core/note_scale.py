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
The note scale core module implements basic classes for different
types of scale notation systems.
"""

from typing import Self
from typing import TypeVar
from typing import List
from warnings import warn
from bisect import insort
from .notes import NoteABC
from .notes import PeriodicNoteABC
from .notes import NoteIntervalABC
from .scale import Scale
from .scale import PeriodicScale
from ..exc import IncompatibleOriginContexts

NoteT = TypeVar('NoteT', bound=NoteABC)


class NoteScale(Scale[NoteT]):
    """
    Base class for all note scales. Implements list and
    set operations, transposition, etc

    Note scales are implemented as generic types with the
    inner type being a note class.

    :param notation: The notation this scale refers to
    :param notes: (optional) A list of notes from the notation.
        If the parameter is omitted an empty scale will be
        initialized
    """

    def __init__(self, notation, notes=None):
        super().__init__(notation, notes)
        self.notation = notation

    @property
    def tuning(self):
        """
        The tuning the origin notation of this scale relies upon
        """
        return self.notation.tuning

    @property
    def is_zero_normalized(self) -> bool:
        """
        Returns True if this function is zero normalized, meaning
        that the first element of the scale is notated the same
        as the zero element of the origin context (typically C0
        in western-like notations)
        """

        if len(self) == 0:
            raise ValueError(
                'is_zero_normalized is not defined on empty scale'
            )

        return self[0].is_notated_same(self.origin_context.zero_element)

    @property
    def enharm_strategy(self):
        """
        A proxy property to the enharmonic strategy of the notation
        """
        return self.notation.enharm_strategy

    @property
    def pitch_scale(self):
        """
        Returns the equivalent pitch scale for this object
        """
        return self.tuning.scale([note.pitch for note in self])

    def add_note(self, note: NoteT):
        """
        .. deprecated:: 0.2.0
           objects in xenharmlib are supposed to be immutable

        Inserts a new note into to the scale at the right
        position. If the note already exists in the scale
        the method will do nothing.

        :raises IncompatibleOriginContexts: If the note has a different
            notation than this scale.

        :param note: The new note
        """
        warn(
            f'{self.__class__.__name__}.add_note is deprecated and '
            f'will be removed in 1.0.0. As per design philosophy '
            f'scales should be immutable. To gradually construct '
            f'a scale by single elements use .with_element',
            DeprecationWarning,
            stacklevel=2,
        )

        if note.notation is not self.notation:
            raise IncompatibleOriginContexts(
                'The provided note originates from a different '
                'notation than the scale'
            )

        if note not in self._sorted_elements:
            insort(self._sorted_elements, note)

    def is_notated_same(self, other: Self) -> bool:
        """
        Returns True if this scale has the exact same notes
        as the other scale while ignoring possible enharmonic
        equivalence.
        """

        if len(self) != len(other):
            return False

        for i, note in enumerate(self):
            if not other[i].is_notated_same(note):
                return False

        return True

    # the obligatory __repr__

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

    # operations that are possible on single notes
    # that can also be applied to collections of
    # notes

    @property
    def pitch_indices(self) -> List[int]:
        """
        An ordered list of pitch indices present in this scale
        """
        return [notes.pitch_index for notes in self]

    def to_note_intervals(self) -> List[NoteIntervalABC]:
        """
        .. deprecated:: 0.2.0
           Use :py:meth:`to_intervals` instead.

        Returns this scale represented as a list of note intervals
        """
        warn(
            f'{self.__class__.__name__}.to_note_intervals is deprecated and '
            f'will be removed in 1.0.0. Please use '
            f'{self.__class__.__name__}.to_intervals instead.',
            DeprecationWarning,
            stacklevel=2,
        )
        return self.to_intervals()

    def transpose(self, diff: int | NoteIntervalABC) -> Self:
        """
        Transposes the scale by the given interval

        :param diff: A note interval or pitch difference given
            as an integer
        """

        if isinstance(diff, int):
            return self.enharm_strategy.note_scale_transpose(self, diff)

        interval = diff
        transposed = []
        for notes in self:
            transposed.append(notes.transpose(interval))

        return self.notation.scale(transposed)

    def note_intersection(self, other: Self) -> Self:
        """
        Returns a new scale including all notes that are
        included in both scales. In contrast to the intersection
        method notes will only be considered shared notes of the
        sets if they are notated the same and excluded otherwise,
        even if they are enharmonically equivalent

        :raises IncompatibleOriginContexts: If the other scale has a
            different notation
        """

        if self.notation is not other.notation:
            raise IncompatibleOriginContexts(
                'Scales do not originate from the same notation'
            )

        notes = []

        for note_a in self:
            for note_b in other:
                if note_a.is_notated_same(note_b):
                    notes.append(note_a)

        return self.notation.scale(notes)

    def note_difference(self, other: Self) -> Self:
        """
        Returns a new scale containing only notes from this scale
        that are NOT present in the other scale. In contrast to
        the difference method notes will only be considered
        shared notes of the sets if they are notated the same.
        If a note is in the second set that is enharmonically
        equivalent to a note in this set but notated in a
        different way, the latter will stay in the result set.

        :raises IncompatibleOriginContexts: If the other scale has a
            different notation
        """

        if self.notation is not other.notation:
            raise IncompatibleOriginContexts(
                'Scales do not originate from the same notation'
            )

        notes = []

        for note_a in self:
            for note_b in other:
                if note_a.is_notated_same(note_b):
                    break
            else:
                notes.append(note_a)

        return self.notation.scale(notes)

    def is_notated_disjoint(self, other: Self) -> bool:
        """
        Determines if this scale has any common notes with another
        scale of the same notation. In contrast to is_disjoint
        enharmonically equivalent but differently notated notes
        will be treated as distinct

        :raises IncompatibleOriginContexts: If the other scale has a
            different notation
        """

        intersection = self.note_intersection(other)

        return len(intersection) == 0

    def is_note_subset(self, other: Self, proper: bool = False) -> bool:
        """
        Determines if all notes in this scale also exist in the
        other scale. In contrast to is_subset enharmonically
        equivalent but differently notated notes will be treated
        as distinct

        :param other: Another scale of the same notation
        :param proper: (Optional, default False) When set
            to True method will return False if the two
            sets are identical

        :raises IncompatibleOriginContexts: If the other scale has a
            different notation
        """

        intersection = self.note_intersection(other)

        is_subset = self.is_notated_same(intersection)

        if not proper:
            return is_subset

        return is_subset and not self.is_notated_same(other)

    def is_note_superset(self, other: Self, proper: bool = False) -> bool:
        """
        Determines if all notes in the other scale also exist
        in this scale. In contrast to is_superset enharmonically
        equivalent but differently notated notes will be treated
        as distinct

        :param other: Another scale of the same notation
        :param proper: (Optional, default False) When set
            to True method will return False if the two
            sets are identical

        :raises IncompatibleOriginContexts: If the other scale has a
            different notation
        """

        intersection = self.note_intersection(other)

        is_superset = other.is_notated_same(intersection)

        if not proper:
            return is_superset

        return is_superset and not self.is_notated_same(other)


PeriodicNoteT = TypeVar('PeriodicNoteT', bound=PeriodicNoteABC)


class PeriodicNoteScale(
    NoteScale[PeriodicNoteT], PeriodicScale[PeriodicNoteT]
):
    """
    Note scale class for periodic notations. Implements
    customized set operations (for when you want to treat
    equivalent notes the same as equal notes).
    """

    @property
    def pc_indices(self) -> List[int]:
        """
        Returns a list of pitch class indices in
        the order they appear in this scale. This can
        include duplicate items if the scale has two
        notes of the same pitch class
        """
        return [note.pc_index for note in self]

    def pcs_complement(self) -> Self:
        """
        Returns a complement version of this scale that includes
        all the notes in the first base interval that are not part
        of this scale
        """

        return self.enharm_strategy.note_scale_pcs_complement(self)

    def is_notated_equivalent(self, other: Self) -> bool:
        """
        Returns True if this scale has, apart from the base
        interval, the exact same notes as the other while
        ignoring possible enharmonic equivalence.
        """

        n_self = self.pcs_normalized()
        n_other = other.pcs_normalized()

        return n_self.is_notated_same(n_other)

    def note_intersection(
        self, other: Self, ignore_bi_index: bool = False
    ) -> Self:
        """
        Returns a new scale including all notes that are
        included in both scales. In contrast to the intersection
        method notes will only be considered shared notes of the
        sets if they are notated the same and excluded otherwise,
        even if they are enharmonically equivalent

        :param ignore_bi_index: (Optional, default False)
            When set to True notes of the same pitch class
            will be treated the same. For example, if the
            intersection of two scales including C-0 and
            C-1 respectively is calculated, both notes
            will be added to the result

        :raises IncompatibleOriginContexts: If the other scale has a
            different notation
        """

        if self.notation is not other.notation:
            raise IncompatibleOriginContexts(
                'Scales do not originate from the same notation'
            )

        if not ignore_bi_index:
            return super().note_intersection(other)

        notes = []

        for note_a in self:
            for note_b in other:
                if note_a.is_notated_equivalent(note_b):
                    notes.append(note_a)
                    notes.append(note_b)

        return self.notation.scale(notes)

    def note_difference(
        self, other: Self, ignore_bi_index: bool = False
    ) -> Self:
        """
        Returns a new scale containing only notes from this scale
        that are NOT present in the other scale. In contrast to
        the difference method notes will only be considered
        shared notes of the sets if they are notated the same.
        If a note is in the second set that is enharmonically
        equivalent to a note in this set, but notated in a
        different way, the latter will stay in the result set.

        :param other: Another scale of the same notation
        :param ignore_bi_index: (Optional, default False)
            When set to True notes of the same pitch class
            will be treated the same. For example, if the
            difference of two scales including C-0 and C-1
            respectively is calculated, C-0 will not be
            inserted into the new scale

        :raises IncompatibleOriginContexts: If the other scale has a
            different notation
        """

        if self.notation is not other.notation:
            raise IncompatibleOriginContexts(
                'Scales do not originate from the same notation'
            )

        if not ignore_bi_index:
            return super().note_difference(other)

        notes = []

        for note_a in self:
            for note_b in other:
                if note_a.is_notated_equivalent(note_b):
                    break
            else:
                notes.append(note_a)

        return self.notation.scale(notes)

    def is_notated_disjoint(
        self, other: Self, ignore_bi_index: bool = False
    ) -> bool:
        """
        Determines if this scale has any common notes with another
        scale of the same notation. In contrast to is_disjoint
        enharmonically equivalent but differently notated notes
        will be treated as distinct

        :param other: Another scale of the same notation
        :param ignore_bi_index: (Optional, default False)
            When set to True notes of the same pitch class
            will be treated the same. For example, if one
            scale includes C-0 and another C-1 the scales
            will not be considered disjoint

        :raises IncompatibleOriginContexts: If the other scale originates
            from a different notation
        """

        intersection = self.note_intersection(
            other, ignore_bi_index=ignore_bi_index
        )

        return len(intersection) == 0

    def is_note_subset(
        self, other: Self, proper: bool = False, ignore_bi_index: bool = False
    ) -> bool:
        """
        Determines if all notes in this scale also exist in the
        other scale. In contrast to is_subset enharmonically
        equivalent but differently notated notes will be treated
        as distinct

        :param other: Another scale of the same notation
        :param proper: (Optional, default False) When set
            to True method will return False if the two
            sets are identical
        :param ignore_bi_index: (Optional, default False)
            When set to True notes of the same pitch class
            will be treated the same.

        :raises IncompatibleOriginContexts: If the other scale originates
            from a different notation
        """

        if not ignore_bi_index:
            return super().is_note_subset(other, proper=proper)

        intersection = self.note_intersection(other, ignore_bi_index=True)

        is_subset = self.is_notated_equivalent(intersection)

        if not proper:
            return is_subset

        return is_subset and not self.is_notated_equivalent(other)

    def is_note_superset(
        self, other: Self, proper: bool = False, ignore_bi_index: bool = False
    ) -> bool:
        """
        Determines if all notes in the other scale also exist
        in this scale. In contrast to is_superset enharmonically
        equivalent but differently notated notes will be treated
        as distinct

        :param other: Another scale of the same notation
        :param proper: (Optional, default False) When set
            to True method will return False if the two
            sets are identical
        :param ignore_bi_index: (Optional, default False)
            When set to True notes of the same pitch class
            will be treated the same.

        :raises IncompatibleOriginContexts: If the other scale originates
            from a different notation
        """

        if not ignore_bi_index:
            return super().is_note_superset(other, proper=proper)

        intersection = self.note_intersection(other, ignore_bi_index=True)

        is_superset = other.is_notated_equivalent(intersection)

        if not proper:
            return is_superset

        return is_superset and not self.is_notated_equivalent(other)


class NatAccNoteScale(PeriodicNoteScale):
    """
    Basic note scale class for natural/accidental notations.
    Implements the scale equivalents of properties special to
    natural/accidental notes.
    """

    # properties on single natural/accidental notes that
    # should also apply to collections

    @property
    def nat_indices(self) -> List[int]:
        """
        A list of the natural indices of notes in this scale

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
        A list of natural class indices of notes in this scale.

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
        scale. The natural base interval is the base interval index
        of the natural part of the note, so e.g. 0 for B#-0
        """
        indices = []
        for note in self:
            indices.append(note.nat_bi_index)
        return indices

    @property
    def acc_vectors(self) -> List[int]:
        """
        A list of accidental vectors for each note in the scale
        """
        vectors = []
        for note in self:
            vectors.append(note.acc_vector)
        return vectors

    @property
    def acc_values(self) -> List[int]:
        """
        A list of accidental values for each note in the scale
        """
        values = []
        for note in self:
            values.append(note.acc_value)
        return values

    @property
    def nat_pc_indices(self) -> List[int]:
        """
        A list of pitch class indices of the natural part of each note
        in the scale (e.g. in 12-EDO [0, 2, 4] for [C#0, D1, Eb2])
        """
        indices = []
        for note in self:
            indices.append(note.nat_pc_index)
        return indices

    @property
    def nat_pitch_indices(self) -> List[int]:
        """
        A list of pitch indices of the natural part of each note
        in the scale (e.g. in 12-EDO [0, 14, 18] for [C#0, D1, Eb2])
        """
        indices = []
        for note in self:
            indices.append(note.nat_pitch_index)
        return indices

    @property
    def natc_symbols(self) -> List[str]:
        """
        The symbol list for the natural part of each note in the
        scale (e.g. in 12-EDO ['C', 'G', 'B'] for [C#0, Gb1, B4])
        """
        symbols = []
        for note in self:
            symbols.append(note.natc_symbol)
        return symbols

    @property
    def acc_symbols(self) -> List[str]:
        """
        The symbol list for the accidental part of each note in the
        scale (e.g. in 12-EDO ['#', 'b', ''] for [C#0, Gb1, B4])
        """
        symbols = []
        for note in self:
            symbols.append(note.acc_symbol)
        return symbols

    @property
    def pc_symbols(self) -> List[str]:
        """
        The symbol list for the pitch classes represented in the
        scale (e.g. in 12-EDO ['C#', 'Gb', 'B'] for [C#0, Gb1, B4])
        """
        symbols = []
        for note in self:
            symbols.append(note.pc_symbol)
        return symbols

    @property
    def acc_directions(self) -> List[int]:
        """
        The list of accidental directions of notes in the scale
        (0 if the note is a natural, 1 if the note is a sharp note,
        -1 if it is a flat note, so for example in 31-EDO [0, 1, -1]
        for [C0, ^B#2, Cb0])
        """
        directions = []
        for note in self:
            directions.append(note.acc_direction)
        return directions
