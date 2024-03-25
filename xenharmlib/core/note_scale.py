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

from abc import ABC
from abc import abstractmethod
from typing import *
from bisect import insort
from collections import defaultdict
from .notes import NoteABC
from .notes import NatAccNote
from .notes import NoteIntervalABC
from ..exc import IncompatibleNotations

NoteT = TypeVar('NoteT', bound=NoteABC)

class NoteScale(ABC, Generic[NoteT]):
    """
    Abstract base class for all note scales. Implements list and
    set operations, transposition, etc

    Note scales are implemented as generic types with the
    inner type being a note class.

    Subclasses must implement at least the :meth:`from_notes`
    method.

    :param notation: The notation this scale refers to
    :param notes: (optional) A list of notes from the notation.
        If parameter is omitted an empty scale will be
        initialized
    """

    def __init__(self, notation, notes=None):
        self.notation = notation
        if notes is None:
            self._sorted_notes = []
        else:
            for note in notes:
                self.add_note(note)

    @property
    def tuning(self):
        return self.notation.tuning

    def add_note(self, note: NoteT):
        """
        Inserts a new note into to the scale at the right
        position. If the note already exists in the scale
        the method will do nothing.

        :raises IncompatibleNotations: If note has a different 
            notation than this scale.
        
        :param note: The new note
        """

        if note.notation != self.notation:
            raise IncompatibleNotations(
                'The provided note has a different '
                'notation than the scale'
            )

        if note not in self._sorted_notes:
            insort(self._sorted_notes, note)

    def __eq__(self, other: object):
        if not isinstance(other, NoteScale):
            return False
        return list(self) == list(other)

    def is_notated_same(self, other: Self) -> bool:
        """
        Returns True if this scale has the exact same notes
        as the other scale while ignoring possible enharmonic
        equivalence.
        """

        if len(self) != len(other):
            return False

        intersection = self.intersection(
            other,
            is_notated_same=True
        )
        return len(intersection) == len(self)

    # in this section we implement all the magic methods
    # so the scale behaves similar to a list

    def __len__(self):
        return len(self._sorted_notes)

    def __iter__(self):
        return self._sorted_notes.__iter__()

    def __getitem__(self, index_or_slice: Union[int, slice]):

        if type(index_or_slice) is slice:
            return self.notation.note_scale(
                self._sorted_notes[index_or_slice]
            )

        return self._sorted_notes[index_or_slice]

    def __contains__(self, object: object) -> bool:

        if isinstance(object, NoteIntervalABC):
            # FIXME: should negative intervals also be
            # considered?
            for note_a in self._sorted_notes:
                for note_b in self._sorted_notes:
                    interval = note_a.interval(note_b)
                    if interval == object:
                        return True

        return object in self._sorted_pitches

    # the obligatory __repr__

    def __repr__(self):
        return (
            f'{self.__class__.__name__}('
            f'{self._sorted_notes}, '
            f'{self.notation.name})'
        )

    # operations that are possible on single notes
    # that can also be applied to collections of
    # notes

    @property
    def frequencies(self):
        """
        An ordered list of frequencies present in this scale
        """
        return [notes.frequency for notes in self]

    @property
    def pitch_indices(self) -> List[int]:
        """
        An ordered list of pitch indices present in this scale
        """
        return [
            notes.pitch_index for notes in self._sorted_notes
        ]

    def to_note_intervals(self) -> List[NoteIntervalABC]:
        """
        Returns this scale represented as a list of note intervals
        """

        intervals = []
        for i in range(0, len(self) - 1):
            intervals.append(
                self[i].interval(self[i+1])
            )
        return intervals

    def transpose(self, interval: NoteIntervalABC) -> Self:
        """
        Transposes the scale by the given interval

        :param interval: A note interval
        """

        transposed = []
        for notes in self._sorted_notes:
            transposed.append(
                notes.transpose(interval)
            )
        
        return self.tuning.notes_scale(
            transposed
        )
    
    # set operations

    def union(self, other: Self) -> Self:
        """
        Returns a new scale including all notes from
        this scale as well as the other

        :param other: Another note of the same notation

        :raises IncompatibleNotations: If other scale has a
            different notation
        """

        if self.notation != other.notation:
            raise IncompatibleNotations(
                'Scales have different notations'
            )

        scale = self.notation.note_scale()

        for note in self:
            scale.add_note(note)

        for note in other:
            scale.add_note(note)

        return scale

    def intersection(self,
                     other: Self,
                     is_notated_same: bool = False) -> Self:
        """
        Returns a new scale including all notes that are
        included in both scales.

        :param other: Another scale of the same notation
        :param is_notated_same: (optional, default False).
            If set to True notes will only be considered
            shared notes of the sets if they are notated
            the same and excluded otherwise, even if they
            are enharmonically equivalent

        :raises IncompatibleNotations: If other scale has a
            different notation
        """

        if self.notation != other.notation:
            raise IncompatibleNotations(
                'Scales have different notations'
            )

        if is_notated_same:
            intersection = set()
            for note_a in self:
                for note_b in other:
                    if note_a.is_notated_same(note_b):
                        intersection.add(note_a)

        else:
            a = set(self)
            b = set(other)
            intersection = a.intersection(b)

        return self.notation.note_scale(
            intersection
        )

    def difference(self,
                   other: Self,
                   is_notated_same: bool = False) -> Self:
        """
        Returns a scale containing only notes from this
        scale that are NOT present in the other scale

        :param other: Another scale of the same notation
        :param is_notated_same: (optional, default False).
            If set to True notes will only be considered
            shared notes of the sets if they are notated
            the same. If a note is in the second set that
            is enharmonically equivalent to a note in this
            set, but notated in a different way, the latter
            will be included in the result set.

        :raises IncompatibleNotations: If other scale has a
            different notation
        """

        if self.notation != other.notation:
            raise IncompatibleNotations(
                'Scales have different notations'
            )

        if is_notated_same:
            difference = set(self)
            for note_a in self:
                for note_b in other:
                    if note_a.is_notated_same(note_b):
                        difference.remove(note_a)

        else:
            a = set(self)
            b = set(other)
            difference = a.difference(b)

        return self.notation.note_scale(
            difference
        )

    def symmetric_difference(self,
                             other: Self) -> Self:
        """
        Returns a scale that includes all the notes from both
        scales that exist in either of them but NOT BOTH. This
        is the complement operation of the intersection.

        :param other: Another scale of the same notation

        :raises IncompatibleNotations: If other scale has a
            different notation
        """

        if self.notation != other.notation:
            raise IncompatibleNotations(
                'Scales have different notations'
            )

        a = set(self)
        b = set(other)
        difference = a.symmetric_difference(b)

        return self.notation.note_scale(
            difference
        )

    def is_disjoint(self,
                    other: Self,
                    is_notated_same: bool = False) -> bool:
        """
        Determines if this scale has any common notes
        with another scale of the same notation
        
        :param other: Another scale of the same tuning
        :param is_notated_same: (optional, default False).
            If set to True enharmonically equivalent but
            differently notated notes will be treated as
            distinct

        :raises IncompatibleNotations: If other scale has a
            different notation
        """

        intersection = self.intersection(
            other,
            is_notated_same=is_notated_same
        )

        return len(intersection) == 0

    def is_subset(self,
                  other: Self,
                  proper: bool = False,
                  is_notated_same: bool = False) -> bool:
        """
        Determines if all notes in this scale also exist
        in the other scale.

        :param other: Another scale of the same tuning
        :param proper: (Optional, default False) When set
            to True method will return False if the two
            sets are identical
        :param is_notated_same: (optional, default False).
            If set to True enharmonically equivalent but
            differently notated notes will be treated as
            distinct

        :raises IncompatibleNotations: If other scale has a
            different tuning
        """

        intersection = self.intersection(
            other,
            is_notated_same=is_notated_same
        )

        is_subset = (self == intersection)

        if not proper:
            return is_subset

        return is_subset and not (self == other)

    def is_superset(self,
                    other: Self,
                    proper: bool = False,
                    is_notated_same: bool = False) -> bool:
        """
        Determines if all pitches in the other scale also exist
        in this scale.

        :param other: Another scale of the same tuning
        :param proper: (Optional, default False) When set
            to True method will return False if the two
            sets are identical
        :param is_notated_same: (optional, default False).
            If set to True enharmonically equivalent but
            differently notated notes will be treated as
            distinct

        :raises IncompatibleNotations: If other scale has a
            different tuning
        """

        intersection = self.intersection(
            other,
            is_notated_same=is_notated_same
        )

        is_superset = (other == intersection)

        if not proper:
            return is_superset

        return is_superset and not (self == other)

    @classmethod
    @abstractmethod
    def from_notes(cls, notes: List[NoteT]) -> Self:
        pass


class PeriodicNoteScale(NoteScale):
    """
    Note scale class for periodic notations. Implements
    customized set operations (for when you want to treat
    equivalent notes the same as equal notes).
    """

    # TODO: implement normalization + inversion

    @property
    def pc_indices(self) -> List[int]:
        """
        Returns a list of pitch class indices in
        the order they appear in this scale. This can
        include duplicate items if the list has two
        pitches of the same pitch class
        """
        return [
            note.pc_index for note in self
        ]

    def get_bi_normalized(self) -> Self:
        """
        Returns a normalized version of this scale where
        all the notes of the scale are put into the first
        base interval of the tuning

        Note: If the original scale has equivalent note pairs
        the normalized scale will be smaller in cardinality.
        """

        n_scale = self.notation.note_scale()

        for note in self._sorted_notes:
            n_note = note.get_bi_normalized()
            n_scale.add_pitch(n_note)

        return n_scale

    def inverted_up(self) -> Self:
        """
        Create a new scale by transposing the base interval of the
        lowest note upwards until it is above the highest note
        """

        inverted_scale = self.notation.note_scale(
            self[1:]
        )

        bi_diff = self[-1].bi_index - self[0].bi_index
        note = self[0].transpose_bi_index(bi_diff)

        if note < inverted_scale[-1]:
            note = note.transpose_bi_index(1)

        inverted_scale.add_pitch(note)
        return inverted_scale

    def inverted_down(self) -> Self:
        """
        Create a new scale by transposing the base interval of the
        highest pitch downwards until it is below the lowest pitch
        """

        inverted_scale = self.tuning.pitch_scale(
            self[:-1]
        )

        bi_diff = self[0].bi_index - self[-1].bi_index
        note = self[-1].transpose_bi_index(bi_diff)

        if note > inverted_scale[0]:
            note = note.transpose_bi_index(-1)

        inverted_scale.add_pitch(note)
        return inverted_scale

    def inversion(self, order: int) -> Self:
        """
        Returns the inversion of the n-th order of this scale.

        :param order: The number of times the scale is
            inverted. If a negative number is given the
            scale will be inverted downwards. On 0 the
            scale will return itself
        """

        if order == 0:
            return self

        scale = self

        if order > 0:
            for _ in range(0, order):
                scale = scale.inverted_up()

        if order < 0:
            for _ in range(0, abs(order)):
                scale = scale.inverted_down()

        return scale

    # some variations on the set operations
    # of the parent class

    def intersection(self,
                     other: Self,
                     is_notated_same: bool = False,
                     ignore_bi_index: bool = False) -> Self:
        """
        Returns a new scale including all notes that are included
        in both scales.

        :param other: Another scale of the same notation
        :param is_notated_same: (Optional, default False)
            When set to True the intersection will include
            only notes, that are notated the same and
            exclude those which are enharmonically equal,
            but notated differently.
        :param ignore_bi_index: (Optional, default False)
            When set to True notes of the same pitch class
            will be treated the same. For example if the
            intersection of two scales including C-0 and
            C-1 respectively is calculated, both pitches
            will be added to the result

        Please be aware that if both ignore_bi_index and
        is_notated_same are set, the former is evaluated
        before the latter, meaning that C-0 and C-1 will
        be considered equal, however C-0 and Dbb-1 will
        be considered distinct.

        :raises IncompatibleNotations: If other scale has a
            different notation
        """

        if self.notation != other.notation:
            raise IncompatibleNotations(
                'Scales have different notations'
            )

        if not ignore_bi_index:
            return super().intersection(
                other,
                is_notated_same=is_notated_same
            )

        a_map = defaultdict(set)
        b_map = defaultdict(set)

        for note in self:
            n_note = note.get_bi_normalized()
            a_map[n_note].add(note)

        for note in other:
            n_note = note.get_bi_normalized()
            b_map[n_note].add(note)

        if is_notated_same:
            intersection = set()
            for n_note_a in a_map:
                for n_note_b in b_map:
                    if n_note_a.is_notated_same(n_note_b):
                        intersection.add(n_note_a)
        
        else:
            a_set = set(a_map.keys())
            b_set = set(b_map.keys())
            intersection = a_set.intersection(b_set)

        scale = self.notation.note_scale()

        for n_note in intersection:
            for note in a_map[n_note]:
                scale.add_note(note)
            for note in b_map[n_note]:
                scale.add_note(note)

        return scale

    def difference(self,
                   other: Self,
                   is_notated_same: bool = False,
                   ignore_bi_index: bool = False) -> Self:
        """
        Returns a scale containing only notes from this
        scale that are NOT present in the other scale

        :param other: Another scale of the same notation
        :param is_notated_same: (Optional, default False)
            When set to True the operation will only
            remove notes, when they are notated the same,
            not when they are just enharmonically equivalent
        :param ignore_bi_index: (Optional, default False)
            When set to True notes of the same pitch class
            will be treated the same. For example if the
            difference of two scales including C-0 and C-1
            respectively is calculated, C-0 will not be
            inserted into the new scale

        Please be aware that if both ignore_bi_index and
        is_notated_same are set, the former is evaluated
        before the latter, meaning that C-0 and C-1 will
        be considered equal, however C-0 and Dbb-1 will
        be considered distinct.

        :raises IncompatibleNotations: If other scale has a
            different notation
        """

        if self.notation != other.notation:
            raise IncompatibleNotations(
                'Scales have different notations'
            )

        if not ignore_bi_index:
            return super().difference(
                other,
                is_notated_same=is_notated_same
            )

        a_map = defaultdict(set)
        b_map = defaultdict(set)

        for note in self:
            n_note = note.get_bi_normalized()
            a_map[n_note].add(note)

        for note in other:
            n_note = note.get_bi_normalized()
            b_map[n_note].add(note)

        if is_notated_same:
            difference = a_map.keys()
            for n_note_a in a_map:
                for n_note_b in b_map:
                    if n_note_a.is_notated_same(n_note_b):
                        difference.remove(n_note_a)
        
        else:
            a_set = set(a_map.keys())
            b_set = set(b_map.keys())
            difference = a_set.difference(b_set)

        scale = self.notation.note_scale()

        for n_note in difference:
            for note in a_map[n_note]:
                scale.add_note(note)

        return scale

    def symmetric_difference(self,
                             other: Self,
                             ignore_bi_index: bool = False) -> Self:
        """
        Returns a scale that includes all the notes
        from both scales that exist in either of them
        but NOT BOTH. This is the complement operation
        of the intersection.

        :param other: Another scale of the same notation
        :param ignore_bi_index: (Optional, default False)
            When set to True notes of the same pitch class
            will be treated the same. For example if the
            difference of two scales including C-0 and C-1
            respectively is calculated, C-0 will not be
            inserted into the new scale

        :raises IncompatibleNotations: If other scale has a
            different notation
        """

        if self.notation != other.notation:
            raise IncompatibleNotations(
                'Scales have different notations'
            )

        if not ignore_bi_index:
            return super().symmetric_difference(
                other
            )

        a_map = defaultdict(set)
        b_map = defaultdict(set)

        for note in self:
            n_note = note.get_bi_normalized()
            a_map[n_note].add(note)

        for note in other:
            n_note = note.get_bi_normalized()
            b_map[n_note].add(note)

        a_set = set(a_map.keys())
        b_set = set(b_map.keys())

        difference = a_set.symmetric_difference(b_set)

        scale = self.notation.note_scale()

        for n_note in difference:
            for note in a_map[n_note]:
                scale.add_note(note)
            for note in b_map[n_note]:
                scale.add_note(note)

        return scale

class NatAccNoteScale(PeriodicNoteScale):
    pass