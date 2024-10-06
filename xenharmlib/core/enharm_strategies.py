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
This module includes functionality to deal with enharmonic ambiguity
"""

from typing import Sequence
from .notes import PeriodicNoteABC


class EnharmonicStrategy:
    """
    An enharmonic strategy is a drop-in function set to solve the problem
    of enharmonic ambiguity when translating pitches into notes.

    An example: On the pitch/tuning layer the transpose method is
    well-defined if given an integer:

    >>> from xenharmlib import EDOTuning
    >>> edo12 = EDOTuning(12)
    >>> edo12.pitch(0).transpose(1)
    EDOPitch(1, 12-EDO)

    However on the notation layer it is unclear, if "C + 1" should
    result in C# or Db, if "C + 2" should result in "D" or "C##", etc.
    The same problem is encountered on operations like pcs_complement:
    Should the PCS complement of [C, D, E, F, G, A, B] be notated with
    upwards accidentals [C#, D#, F#, G#, A#], downward accidentals
    [Db, Eb, Gb, Ab, Bb] or a mixture of both?

    An enharmonic strategy makes an opinionated(!) choice which pitches
    translate to which notes. Because not every strategy is fit for every
    context and purpose xenharmlib allows choosing a custom strategy
    when initializing a notation.

    This base class implements stubs of all hook functions which get
    called by the notation layer classes. By default these stubs are
    not abstract, but simply raise NotImplementedError, so it is
    possible for EnharmonicStrategy subclasses to not support *all*
    operations that need an enharmonic strategy. This way custom
    enharmonic strategies implemented by the user also keep working
    if the feature set expands on an update.
    """

    def guess_note(self, notation, pitch):
        """
        Notation.guess_note relays to here

        :param notation: The notation object that relayed here
        :param pitch: The pitch object
        """

        raise NotImplementedError(
            f'Enharmonic strategy {self.__class__.__name__} does not '
            f'implement the guess_note method. Creating a note from '
            f'a pitch is therefore not possible'
        )

    def guess_note_interval(self, notation, pitch_interval):
        """
        Notation.guess_note_interval relays to here

        :param notation: The notation object that relayed here
        :param pitch_interval: The pitch interval object
        """

        raise NotImplementedError(
            f'Enharmonic strategy {self.__class__.__name__} does not '
            f'implement the guess_note_interval method. Creating a note '
            f'interval from a pitch interval is therefore not possible'
        )

    def guess_note_scale(self, notation, pitch_scale):
        """
        Notation.guess_note_scale relays to here

        :param notation: The notation object that relayed here
        :param pitch_scale: The pitch scale object
        """

        raise NotImplementedError(
            f'Enharmonic strategy {self.__class__.__name__} does not '
            f'implement the guess_note_scale method. Creating a note '
            f'scale from a pitch scale is therefore not possible'
        )

    def note_transpose(self, note, pitch_diff: int):
        """
        Note.transpose relays to here if the interval argument was
        not given as a suitable NoteInterval object but as an integer.

        :param note: The note on which the transpose method was called
        :param pitch_diff: The pitch difference as an integer
        """

        raise NotImplementedError(
            f'Enharmonic strategy {self.__class__.__name__} does not '
            f'implement the note_transpose method. Transposing a note '
            f'with an integer argument is therefore not possible'
        )

    def note_scale_transpose(self, note_scale, pitch_diff: int):
        """
        NoteScale.transpose relays to here if the interval argument was
        not given as a suitable NoteInterval object but as an integer.

        :param note_scale: The note scale on which the transpose method
            was called
        :param pitch_diff: The pitch difference as an integer
        """

        raise NotImplementedError(
            f'Enharmonic strategy {self.__class__.__name__} does not '
            f'implement the note_scale_transpose method. Transposing a '
            f'note scale with an integer argument is therefore not possible'
        )

    def note_scale_pcs_complement(self, note_scale):
        """
        NoteScale.pcs_complement relays to here

        :param note_scale: The note scale on which the pcs_complement
            method was called
        """

        raise NotImplementedError(
            f'Enharmonic strategy {self.__class__.__name__} does not '
            f'implement the note_scale_transpose method. Transposing a '
            f'note scale with an integer argument is therefore not possible'
        )


class PCBlueprintStrategy(EnharmonicStrategy):
    """
    PCBlueprintStrategy is an enharmonic strategy that defines fixed note
    symbols for each pitch class and translates every pitch to a note by
    matching the pitch class and transposing the base interval.

    :param pc_blueprint: An iterable of notes that together form a pitch
        class blueprint for the whole pitch range

    >>> from xenharmlib import EDOTuning
    >>> from xenharmlib import UpDownNotation
    >>> from xenharmlib.core.enharm_strategies import PCBlueprintStrategy
    >>>
    >>> edo12 = EDOTuning(12)
    >>> n_edo12 = UpDownNotation(edo12)
    >>>
    >>> S = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    >>> strategy = PCBlueprintStrategy(
    ...     [n_edo12.note(symbol, 0) for symbol in S]
    ... )
    >>> n_edo12.enharmonic_strategy = strategy
    >>>
    >>> n_edo12.guess_note(edo12.pitch(13))
    UpDownNote(C#, 1, 12-EDO)
    >>> n_edo12.note('D#', 2).transpose(1)
    UpDownNote(E, 2, 12-EDO)
    """

    def __init__(self, pc_blueprint: Sequence[PeriodicNoteABC]):

        notation = pc_blueprint[0].notation

        # create a pcs normalized scale from the list of notes.
        # the result should be a pcs normalized scale that has
        # exactly as much unique notes in the first base interval
        # as the period length of the tuning

        self.pc_blueprint = notation.scale(pc_blueprint).pcs_normalized()

        if len(self.pc_blueprint) != len(notation.tuning):
            # pick out the missing pitch class representative
            # in the blueprint to get a nicer error message
            for i, note in enumerate(self.pc_blueprint):
                if note.pc_index != i:
                    raise ValueError(
                        f'Pitch class {i} was not represented by a note'
                    )

    def guess_note(self, notation, pitch):
        """
        Notation.guess_note relays to here

        :param notation: The notation object that relayed here
        :param pitch: The pitch object
        """

        blueprint_note = self.pc_blueprint[pitch.pc_index]
        return blueprint_note.transpose_bi_index(pitch.bi_index)

    def guess_note_interval(self, notation, pitch_interval):
        """
        Notation.guess_note_interval relays to here

        :param notation: The notation object that relayed here
        :param pitch: The pitch interval object
        """

        ref_pitch = pitch_interval.ref_pitch
        ref_note = self.guess_note(notation, ref_pitch)
        target_note = self.note_transpose(ref_note, pitch_interval.pitch_diff)
        return ref_note.interval(target_note)

    def guess_note_scale(self, notation, pitch_scale):
        """
        Notation.guess_note_scale relays to here

        :param notation: The notation object that relayed here
        :param pitch_scale: The pitch scale object
        """

        notes = []
        for pitch in pitch_scale:
            note = self.guess_note(notation, pitch)
            notes.append(note)
        return notation.scale(notes)

    def note_transpose(self, note, pitch_diff: int):
        """
        Note.transpose relays to here if the interval argument was
        not given as a suitable NoteInterval object but as an integer.

        :param note: The note on which the transpose method was called
        :param pitch_diff: The pitch difference as an integer
        """

        pitch = note.pitch.transpose(pitch_diff)
        blueprint_note = self.pc_blueprint[pitch.pc_index]
        return blueprint_note.transpose_bi_index(pitch.bi_index)

    def note_scale_transpose(self, note_scale, pitch_diff: int):
        """
        NoteScale.transpose relays to here if the interval argument was
        not given as a suitable NoteInterval object but as an integer.

        :param note_scale: The note scale on which the transpose method
            was called
        :param pitch_diff: The pitch difference as an integer
        """

        notation = note_scale.notation
        notes = []
        for note in note_scale:
            transposed = self.note_transpose(note, pitch_diff)
            notes.append(transposed)
        return notation.scale(notes)

    def note_scale_pcs_complement(self, note_scale):
        """
        NoteScale.pcs_complement relays to here

        :param note_scale: The note scale on which the pcs_complement
            method was called
        """

        note_scale = note_scale.pcs_normalized()
        notation = note_scale.notation

        notes = []
        for note in self.pc_blueprint:
            if note not in note_scale:
                notes.append(note)

        return notation.scale(notes)
