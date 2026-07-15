Pitch/Note Sequences
=================================================

A sequence is a structure representing a succession of pitches or notes.
Sequences don't hold any rhythmic information. They are conceptualized
as a data structure representing purely the "harmonic flow" of a melody.

.. testcode::

   from xenharmlib import WesternNotation

   western = WesternNotation()

   # harmonic flow of the first two measures from the vocals of
   # Schubert's Wiegenlied ("Schlafe Schlafe, holder, süßer Knabe"),
   # rearranged into the key of F major
   schlafe_schlafe = western.seq(
       western.note(pcs, 4) for pcs in
       ['A', 'C', 'G', 'A', 'Bb', 'A', 'A', 'G', 'F', 'E', 'F', 'G', 'C']
   )

In the context of serial music the sequence type is used to analyze segments.
Sequences allow inspection of pitch indices and pitch class indices of their
content:

.. testcode::

   print(schlafe_schlafe.pitch_indices)
   print(schlafe_schlafe.pc_indices)

.. testoutput::

   [57, 48, 55, 57, 58, 57, 57, 55, 53, 52, 53, 55, 48]
   [9, 0, 7, 9, 10, 9, 9, 7, 5, 4, 5, 7, 0]

Sequences act similar to standard python list or tuple types in terms
of their interface, but implement a couple of additional methods specific
to music theory.
In contrast to scales there is no restriction in regards to uniqueness
or order, so sequences can also be used to analyze scale-like data for
which the scale primitive is too restricted, e.g. for "descending scales",
in which pitches and notes are not in ascending, but descending order:

.. testcode::

   from xenharmlib import WesternNotation

   western = WesternNotation()
   scale = western.pc_scale('CDEFGABC', 4)
   descending = western.seq(scale).retrograde()

   print(descending)

.. testoutput::

   WesternNoteSeq([C5, B4, A4, G4, F4, E4, D4, C4])


Deriving sequences from pitches/notes
--------------------------------------

Sequences can easily be constructed from Lists (or any Iterable) of notes
or pitches. This method of construction is preferable when writing utilities
because it works the same on all origin contexts:

.. tabs::

   .. tab:: EDO

      .. testcode:: EDOTuning

         from xenharmlib import EDOTuning
         edo31 = EDOTuning(31)

         C0 = edo31.pitch(0)
         D0 = edo31.pitch(5)
         E0 = edo31.pitch(10)

         seq = edo31.seq([C0, D0, E0, C0, E0])
         print(seq)

      .. testoutput:: EDOTuning

         EDOPitchSeq([0, 5, 10, 0, 10], 31-EDO)

   .. tab:: Prime Limit

      .. testcode:: PrimeLimitTuning

         from xenharmlib import PrimeLimitTuning
         limit5 = PrimeLimitTuning(5)

         C0 = limit5.rs_pitch('1/1')
         D0 = limit5.rs_pitch('9/8')
         E0 = limit5.rs_pitch('5/4')

         seq = limit5.seq([C0, D0, E0, C0, E0])
         print(seq)

      .. testoutput:: PrimeLimitTuning

         PrimeLimitPitchSeq([1, 9/8, 5/4, 1, 5/4], 5-Limit)

   .. tab:: Western

      .. testcode:: WesternNotation

         from xenharmlib import WesternNotation
         western = WesternNotation()

         C4 = western.note('C', 4)
         D4 = western.note('D', 4)
         E4 = western.note('E', 4)

         seq = western.seq([C4, D4, E4, C4, E4])
         print(seq)

      .. testoutput:: WesternNotation

         WesternNoteSeq([C4, D4, E4, C4, E4])

Element-wise Construction
-------------------------------------------------------

Sequences can be constructed element-wise. In line with xenharmlib's
immutable object design, this is not done with an append method like
in standard python, but with a method that returns a sequence with
an additional element:

.. tabs::

   .. tab:: EDO

      .. testcode:: EDOTuning

         from xenharmlib import EDOTuning
         edo31 = EDOTuning(31)

         C0 = edo31.pitch(0)
         D0 = edo31.pitch(5)
         E0 = edo31.pitch(10)

         # start with empty sequence
         seq = edo31.seq()

         for e in [C0, D0, E0, C0, E0]:
             seq = seq.with_element(e)
             print(seq)

      .. testoutput:: EDOTuning

         EDOPitchSeq([0], 31-EDO)
         EDOPitchSeq([0, 5], 31-EDO)
         EDOPitchSeq([0, 5, 10], 31-EDO)
         EDOPitchSeq([0, 5, 10, 0], 31-EDO)
         EDOPitchSeq([0, 5, 10, 0, 10], 31-EDO)

   .. tab:: Prime Limit

      .. testcode:: PrimeLimitTuning

         from xenharmlib import PrimeLimitTuning
         limit5 = PrimeLimitTuning(5)

         C0 = limit5.vec_pitch((0, 0, 0))
         D0 = limit5.vec_pitch((-3, 2, 0))
         E0 = limit5.vec_pitch((-2, 0, 1))

         # start with empty sequence
         seq = limit5.seq()

         for e in [C0, D0, E0, C0, E0]:
             seq = seq.with_element(e)
             print(seq)

      .. testoutput:: PrimeLimitTuning

         PrimeLimitPitchSeq([1], 5-Limit)
         PrimeLimitPitchSeq([1, 9/8], 5-Limit)
         PrimeLimitPitchSeq([1, 9/8, 5/4], 5-Limit)
         PrimeLimitPitchSeq([1, 9/8, 5/4, 1], 5-Limit)
         PrimeLimitPitchSeq([1, 9/8, 5/4, 1, 5/4], 5-Limit)

   .. tab:: Western

      .. testcode:: WesternNotation

         from xenharmlib import WesternNotation
         western = WesternNotation()

         C4 = western.note('C', 4)
         D4 = western.note('D', 4)
         E4 = western.note('E', 4)

         # start with empty sequence
         seq = western.seq()

         for e in [C4, D4, E4, C4, E4]:
             seq = seq.with_element(e)
             print(seq)

      .. testoutput:: WesternNotation

         WesternNoteSeq([C4])
         WesternNoteSeq([C4, D4])
         WesternNoteSeq([C4, D4, E4])
         WesternNoteSeq([C4, D4, E4, C4])
         WesternNoteSeq([C4, D4, E4, C4, E4])

Given an additional positional parameter, new elements can appear at a
place of the user's free choosing in the new sequence. The parameter works
exactly like the equivalent parameter in the insert method of python's
builtin List type, meaning the given value will be the index in which
the new element will be found in the new sequence:

.. tabs::

   .. tab:: EDO

      .. testcode:: EDOTuning

         from xenharmlib import EDOTuning
         edo31 = EDOTuning(31)

         C0 = edo31.pitch(0)
         D0 = edo31.pitch(5)
         E0 = edo31.pitch(10)

         # start with empty sequence
         seq = edo31.seq()

         for e in [C0, D0, E0, C0, E0]:
             seq = seq.with_element(e, 0)
             print(seq)

      .. testoutput:: EDOTuning

         EDOPitchSeq([0], 31-EDO)
         EDOPitchSeq([5, 0], 31-EDO)
         EDOPitchSeq([10, 5, 0], 31-EDO)
         EDOPitchSeq([0, 10, 5, 0], 31-EDO)
         EDOPitchSeq([10, 0, 10, 5, 0], 31-EDO)

   .. tab:: Prime Limit

      .. testcode:: PrimeLimitTuning

         from xenharmlib import PrimeLimitTuning
         limit5 = PrimeLimitTuning(5)

         C0 = limit5.vec_pitch((0, 0, 0))
         D0 = limit5.vec_pitch((-3, 2, 0))
         E0 = limit5.vec_pitch((-2, 0, 1))

         # start with empty sequence
         seq = limit5.seq()

         for e in [C0, D0, E0, C0, E0]:
             seq = seq.with_element(e, 0)
             print(seq)

      .. testoutput:: PrimeLimitTuning

         PrimeLimitPitchSeq([1], 5-Limit)
         PrimeLimitPitchSeq([9/8, 1], 5-Limit)
         PrimeLimitPitchSeq([5/4, 9/8, 1], 5-Limit)
         PrimeLimitPitchSeq([1, 5/4, 9/8, 1], 5-Limit)
         PrimeLimitPitchSeq([5/4, 1, 5/4, 9/8, 1], 5-Limit)

   .. tab:: Western

      .. testcode:: WesternNotation

         from xenharmlib import WesternNotation
         western = WesternNotation()

         C4 = western.note('C', 4)
         D4 = western.note('D', 4)
         E4 = western.note('E', 4)

         # start with empty sequence
         seq = western.seq()

         for e in [C4, D4, E4, C4, E4]:
             seq = seq.with_element(e, 0)
             print(seq)

      .. testoutput:: WesternNotation

         WesternNoteSeq([C4])
         WesternNoteSeq([D4, C4])
         WesternNoteSeq([E4, D4, C4])
         WesternNoteSeq([C4, E4, D4, C4])
         WesternNoteSeq([E4, C4, E4, D4, C4])

Index-based Construction
-------------------------------------------------------

Sequences can also conveniently constructed by providing a list of indices,
which - depending on origin context - can be integers or lattice points.
This type of construction also works on the notation layer by employing
the notation's enharmonic strategy.

.. tabs::

   .. tab:: EDO

      .. testcode:: EDOTuning

         from xenharmlib import EDOTuning
         edo31 = EDOTuning(31)

         seq = edo31.index_seq([0, 5, 10, 0, 5])
         print(seq)

      .. testoutput:: EDOTuning

         EDOPitchSeq([0, 5, 10, 0, 5], 31-EDO)

   .. tab:: Prime Limit

      .. testcode:: PrimeLimitTuning

         from xenharmlib import PrimeLimitTuning
         limit5 = PrimeLimitTuning(5)

         seq = limit5.index_seq(
             [
                 limit5.lattice.point((0, 0, 0)),
                 limit5.lattice.point((-3, 2, 0)),
                 limit5.lattice.point((-2, 0, 1))
             ]
         )
         print(seq)

      .. testoutput:: PrimeLimitTuning

         PrimeLimitPitchSeq([1, 9/8, 5/4], 5-Limit)

   .. tab:: Western

      .. testcode:: WesternNotation

         from xenharmlib import WesternNotation
         western = WesternNotation()

         seq = western.index_seq([0, 2, 4, 0, 2])
         print(seq)

      .. testoutput:: WesternNotation

         WesternNoteSeq([C0, D0, E0, C0, D0])

Index-based construction can be especially useful for dealing with
segments in 12-tone music. The following snippet e.g. creates a
random 12-tone segment and prints the result as a note sequence:

.. code-block:: python

   from random import shuffle
   from xenharmlib import WesternNotation

   western = WesternNotation()
   pc_indices = list(range(0, 12))
   shuffle(pc_indices)

   segment = western.index_seq(pc_indices)

   print(segment)

Construction Based on Closest Frequency
-----------------------------------------------------

Sequences can be constructed by finding pitches or notes closest to an
iterable of frequencies. This can be useful if you have extracted data
on fundamental frequencies of a melody from an audio sample and want to
know the notes played in the recording. The
`Essentia <https://essentia.upf.edu/tutorial_pitch_melody.html>`_
library e.g. allows raw frequency extraction from melodies, however
its note conversion feature only supports 12 equal temperament.
Augmented with xenharmlib you can extend your analysis to non-Western
harmonic system (e.g. 53-EDO Turkish Makam)

.. tabs::

   .. tab:: EDO

      .. testcode:: EDOTuning

         from xenharmlib import EDOTuning
         from xenharmlib import Frequency

         edo31 = EDOTuning(31)

         # melody frequencies extracted by another library
         frequencies = [
             Frequency(f) for f in [230, 410, 230, 670, 600]
         ]

         seq = edo31.closest_seq(frequencies)
         print(seq)

      .. testoutput:: EDOTuning

         EDOPitchSeq([118, 144, 118, 166, 161], 31-EDO)

   .. tab:: Western

      .. testcode:: WesternNotation

         from xenharmlib import WesternNotation
         from xenharmlib import Frequency

         western = WesternNotation()

         # melody frequencies extracted by another library
         frequencies = [
             Frequency(f) for f in [230, 410, 230, 670, 600]
         ]

         seq = western.closest_seq(frequencies)
         print(seq)

      .. testoutput:: WesternNotation

         WesternNoteSeq([A#3, G#4, A#3, E5, D5])

   .. tab:: UpDown

      .. testcode:: UpDownNotation

         from xenharmlib import EDOTuning
         from xenharmlib import UpDownNotation
         from xenharmlib import Frequency

         edo31 = EDOTuning(31)
         n_edo31 = UpDownNotation(edo31)

         # melody frequencies extracted by another library
         frequencies = [
             Frequency(f) for f in [230, 410, 230, 670, 600]
         ]

         seq = n_edo31.closest_seq(frequencies)
         print(seq)

      .. testoutput:: UpDownNotation

         UpDownNoteSeq([A#3, G#4, A#3, Fb5, Ebb5], 31-EDO)


Relation to Interval Sequences
-------------------------------------------------------

Sequences and Interval Sequences are closely related. While a sequence
stores the information "what succession of sounds should be played" an
interval sequence stores the information "given a arbitrary start point,
what relative movements should be made". 
Sequences can be transformed into interval sequences by the
:meth:`~xenharmlib.core.freq_repr_seq.FreqReprSeq.to_interval_seq` method:

.. tabs::

   .. tab:: EDO

      .. testcode:: EDOTuning

         from xenharmlib import EDOTuning
         edo31 = EDOTuning(31)

         C0 = edo31.pitch(0)
         D0 = edo31.pitch(5)
         E0 = edo31.pitch(10)

         seq = edo31.seq([C0, D0, E0, C0, E0])
         iseq = seq.to_interval_seq()
         print(iseq)

      .. testoutput:: EDOTuning

         EDOPitchIntervalSeq([5, 5, -10, 10], 31-EDO)

   .. tab:: Prime Limit

      .. testcode:: PrimeLimitTuning

         from xenharmlib import PrimeLimitTuning
         limit5 = PrimeLimitTuning(5)

         C0 = limit5.vec_pitch((0, 0, 0))
         D0 = limit5.vec_pitch((-3, 2, 0))
         E0 = limit5.vec_pitch((-2, 0, 1))

         seq = limit5.seq([C0, D0, E0, C0, E0])
         iseq = seq.to_interval_seq()
         print(iseq)

      .. testoutput:: PrimeLimitTuning

         PrimeLimitPitchIntervalSeq([9/8, 10/9, 4/5, 5/4], 5-Limit)

   .. tab:: Western

      .. testcode:: WesternNotation

         from xenharmlib import WesternNotation
         western = WesternNotation()

         C4 = western.note('C', 4)
         D4 = western.note('D', 4)
         E4 = western.note('E', 4)

         seq = western.seq([C4, D4, E4, C4, E4])
         iseq = seq.to_interval_seq()
         print(iseq)

      .. testoutput:: WesternNotation

         WesternNoteIntervalSeq([M2, M2, M-3, M3])


Vice versa interval sequences can be transformed into a pitch/note
sequences by providing a root note:

.. tabs::

   .. tab:: EDO

      .. testcode:: EDOTuning

         from xenharmlib import EDOTuning
         edo31 = EDOTuning(31)

         iseq = edo31.diff_interval_seq([5, 5, 2, 5, 2])
         seq = edo31.pitch(18).seq(iseq)
         print(seq)

      .. testoutput:: EDOTuning

         EDOPitchSeq([18, 23, 28, 30, 35, 37], 31-EDO)

   .. tab:: Prime Limit

      .. testcode:: PrimeLimitTuning

         from xenharmlib import PrimeLimitTuning
         limit5 = PrimeLimitTuning(5)

         iseq = limit5.vec_interval_seq(
             [(-3, 2, 0), (-3, 2, 0), (-2, 0, 1)]
         )
         seq = limit5.vec_pitch((-1, 1, 0)).seq(iseq)
         print(seq)

      .. testoutput:: PrimeLimitTuning

         PrimeLimitPitchSeq([3/2, 27/16, 243/128, 1215/512], 5-Limit)

   .. tab:: Western

      .. testcode:: WesternNotation

         from xenharmlib import WesternNotation
         western = WesternNotation()
        
         iseq = western.interval_seq(
             [ 
                 western.shorthand_interval('m', 2),
                 western.shorthand_interval('M', 2),
                 western.shorthand_interval('m', 2),
             ]
         )

         seq = western.note('D', 4).seq(iseq)
         print(seq)

      .. testoutput:: WesternNotation

         WesternNoteSeq([D4, Eb4, F4, Gb4])


Relation to Interval Fans
-------------------------------------------------------

While sequences define a melody flow in concrete terms (for example:
The melody flow of "Marry Had a Little Lamb" in C major), interval fans
abstract away the tonic center (the melodic flow of "Marry Had a Little
Lamb" in *some* key). This abstraction can be calculated using the
:meth:`~xenharmlib.core.freq_repr_seq.FreqReprSeq.to_interval_fan`
method, which expects the pitch or note defining the tonic of the
key as a parameter:

.. tabs::

   .. tab:: EDO

      .. testcode:: EDOTuning

         from xenharmlib import EDOTuning
         edo31 = EDOTuning(31)

         C0 = edo31.pitch(0)
         D0 = edo31.pitch(5)
         E0 = edo31.pitch(10)

         # melodic flow of marry had a little lamb
         seq = edo31.seq([E0, D0, C0, D0, E0, E0, E0])

         # calculate interval fan by using the information that
         # it is written in reference to the tonal center of C
         ifan = seq.to_interval_fan(C0)
         print(ifan)

      .. testoutput:: EDOTuning

         EDOPitchIntervalFan([10, 5, 0, 5, 10, 10, 10], 31-EDO)

   .. tab:: Prime Limit

      .. testcode:: PrimeLimitTuning

         from xenharmlib import PrimeLimitTuning
         limit5 = PrimeLimitTuning(5)

         C0 = limit5.vec_pitch((0, 0, 0))
         D0 = limit5.vec_pitch((-3, 2, 0))
         E0 = limit5.vec_pitch((-2, 0, 1))

         # melodic flow of marry had a little lamb
         seq = limit5.seq([E0, D0, C0, D0, E0, E0, E0])

         # calculate interval fan by using the information that
         # it is written in reference to the tonal center of C
         ifan = seq.to_interval_fan(C0)
         print(ifan)

      .. testoutput:: PrimeLimitTuning

         PrimeLimitPitchIntervalFan([5/4, 9/8, 1, 9/8, 5/4, 5/4, 5/4], 5-Limit)

   .. tab:: Western

      .. testcode:: WesternNotation

         from xenharmlib import WesternNotation
         western = WesternNotation()

         C4 = western.note('C', 4)
         D4 = western.note('D', 4)
         E4 = western.note('E', 4)

         # melodic series of marry had a little lamb
         seq = western.seq([E4, D4, C4, D4, E4, E4, E4])

         # calculate interval fan by using the information that
         # it is written in reference to the tonal center of C
         ifan = seq.to_interval_fan(C4)
         print(ifan)

      .. testoutput:: WesternNotation

         WesternNoteIntervalFan([M3, M2, P1, M2, M3, M3, M3])

The reverse is also possible: Start with an interval fan defining an abstract
sequence in relation to an unspecified tonic, add a tonic and receive the
melodic flow:

.. tabs::

   .. tab:: EDO

      .. testcode:: EDOTuning

         from xenharmlib import EDOTuning
         edo31 = EDOTuning(31)

         # abstract form of "marry had a little lamb"
         # relating to an unspecified tonic note/pitch
         ifan = edo31.diff_interval_fan([10, 5, 0, 5, 10, 10, 10])

         # make an instance with the tonic G0
         in_g = edo31.pitch(18).seq(ifan)

         # make an instance with the tonic F0
         in_f = edo31.pitch(13).seq(ifan)

         print(in_g)
         print(in_f)

      .. testoutput:: EDOTuning

         EDOPitchSeq([28, 23, 18, 23, 28, 28, 28], 31-EDO)
         EDOPitchSeq([23, 18, 13, 18, 23, 23, 23], 31-EDO)

   .. tab:: Prime Limit

      .. testcode:: PrimeLimitTuning

         from xenharmlib import PrimeLimitTuning
         limit5 = PrimeLimitTuning(5)

         # abstract form of "marry had a little lamb"
         # relating to an unspecified tonic note/pitch
         ifan = limit5.rs_interval_fan(
             ['5/4', '9/8', '1', '9/8', '5/4', '5/4', '5/4']
         )

         # make an instance with the tonic G0
         in_g = limit5.rs_pitch('3/2').seq(ifan)

         # make an instance with the tonic F0
         in_f = limit5.rs_pitch('4/3').seq(ifan)

         print(in_g)
         print(in_f)

      .. testoutput:: PrimeLimitTuning

         PrimeLimitPitchSeq([15/8, 27/16, 3/2, 27/16, 15/8, 15/8, 15/8], 5-Limit)
         PrimeLimitPitchSeq([5/3, 3/2, 4/3, 3/2, 5/3, 5/3, 5/3], 5-Limit)

   .. tab:: Western

      .. testcode:: WesternNotation

         from xenharmlib import WesternNotation
         western = WesternNotation()
        
         P1 = western.shorthand_interval('P', 1)
         M2 = western.shorthand_interval('M', 2)
         M3 = western.shorthand_interval('M', 3)
        
         # abstract form of "marry had a little lamb"
         # relating to an unspecified tonic note/pitch
         ifan = western.interval_fan(
             [M3, M2, P1, M2, M3, M3, M3]
         )

         # make an instance with the tonic G4
         in_g = western.note('G', 4).seq(ifan)

         # make an instance with the tonic F4
         in_f = western.note('F', 4).seq(ifan)

         print(in_g)
         print(in_f)

      .. testoutput:: WesternNotation

         WesternNoteSeq([B4, A4, G4, A4, B4, B4, B4])
         WesternNoteSeq([A4, G4, F4, G4, A4, A4, A4])


Identity and Equivalency
--------------------------------------

Two sequences are considered identical if the series of frequencies of
one sequence is identical to the series of frequencies of another.
This means that sequences can be compared across different origin
contexts:

.. testcode::

   from xenharmlib import EDOTuning
   from xenharmlib import UpDownNotation
   from xenharmlib import WesternNotation

   edo24 = EDOTuning(24)
   n_edo24 = UpDownNotation(edo24)
   western = WesternNotation()

   Cm_1 = edo24.index_seq([0, 8, 14, 8, 8, 0, 14])
   Cm_2 = n_edo24.seq([n_edo24.note(pcs, 0) for pcs in 'CEGEECG'])
   Cm_3 = western.seq([western.note(pcs, 0) for pcs in 'CEGEECG'])

   print(Cm_1 == Cm_2 == Cm_3)

.. testoutput::

   True

Keep in mind that even if two sequences might have the same symbolic string
representation in a notation, they are not necessarily equal. A G4 in 31-EDO
has for example a different frequency than a G4 in 12-EDO:

.. testcode::

   from xenharmlib import EDOTuning
   from xenharmlib import UpDownNotation

   edo12 = EDOTuning(12)
   n_edo12 = UpDownNotation(edo12)

   edo31 = EDOTuning(31)
   n_edo31 = UpDownNotation(edo31)

   Cm_1 = n_edo12.seq([n_edo12.note(pcs, 4) for pcs in 'CEGEECG'])
   Cm_2 = n_edo31.seq([n_edo31.note(pcs, 4) for pcs in 'CEGEECG'])
   print(Cm_1)
   print(Cm_2)

   print(Cm_1 == Cm_2)

.. testoutput::

   UpDownNoteSeq([C4, E4, G4, E4, E4, C4, G4], 12-EDO)
   UpDownNoteSeq([C4, E4, G4, E4, E4, C4, G4], 31-EDO)
   False

Identity transfers to object hashes, so two sequences that are equal are also
considered the same object when put into a python set:

.. testcode::

   from xenharmlib import EDOTuning
   from xenharmlib import WesternNotation

   edo24 = EDOTuning(24)
   western = WesternNotation()

   Cm_1 = edo24.index_seq([0, 8, 14, 8, 8, 0, 14])
   Cm_2 = western.seq([western.note(pcs, 0) for pcs in 'CEGEECG'])

   print({Cm_1, Cm_2})

.. testoutput::

   {EDOPitchSeq([0, 8, 14, 8, 8, 0, 14], 24-EDO)}

Sequences can also be tested for equivalency. This means that not frequencies
are compared, but frequencies normalized to the first base interval, making
e.g. "C4 and C5" the same. Like equality this can also be tested across
origin contexts as long as they have the same equivalency interval
ratio:

.. testcode::

   from xenharmlib import EDOTuning
   from xenharmlib import UpDownNotation

   edo12 = EDOTuning(12)
   n_edo12 = UpDownNotation(edo12)

   edo24 = EDOTuning(24)
   n_edo24 = UpDownNotation(edo24)

   Cm_1 = n_edo12.seq([n_edo12.note(pcs, 4) for pcs in 'CEGEECG'])
   Cm_2 = n_edo24.seq([n_edo24.note(pcs, 3) for pcs in 'CEGEECG'])

   print(Cm_1)
   print(Cm_2)
   print(Cm_1.is_equivalent(Cm_2))

.. testoutput::

   UpDownNoteSeq([C4, E4, G4, E4, E4, C4, G4], 12-EDO)
   UpDownNoteSeq([C3, E3, G3, E3, E3, C3, G3], 24-EDO)
   True

The base interval difference does not need to be uniform across
between the two sequences for them to be considered equivalent,
as you can see from the following examples:

.. tabs::

   .. tab:: EDO

      .. testcode:: EDOTuning

         from xenharmlib import EDOTuning
         edo31 = EDOTuning(31)

         seq_a = edo31.index_seq([0, 10, 49, 10, 0])
         seq_b = edo31.index_seq([31, 10, 49, 41, 62])
         seq_c = edo31.index_seq([10, 0, 49, 41, 62])

         print(seq_a.is_equivalent(seq_b))
         print(seq_a.is_equivalent(seq_c))

      .. testoutput:: EDOTuning

         True
         False

   .. tab:: Prime Limit

      .. testcode:: PrimeLimitTuning

         from xenharmlib import PrimeLimitTuning
         limit5 = PrimeLimitTuning(5)

         seq_a = limit5.rs_seq(['3/2', '2/1', '5/2', '1/1'])
         seq_b = limit5.rs_seq(['3/1', '4/1', '5/1', '2/1'])
         seq_c = limit5.rs_seq(['3/1', '4/1', '2/1', '5/2'])

         print(seq_a.is_equivalent(seq_b))
         print(seq_a.is_equivalent(seq_c))

      .. testoutput:: PrimeLimitTuning

         True
         False

   .. tab:: Western

      .. testcode:: WesternNotation

         from xenharmlib import WesternNotation
         western = WesternNotation()

         E3 = western.note('E', 3)
         E4 = western.note('E', 4)
         G4 = western.note('G', 4)
         C5 = western.note('C', 5)
         E5 = western.note('E', 5)
         G5 = western.note('G', 5)

         seq_a = western.seq([G4, C5, E5, E4])
         seq_b = western.seq([G5, C5, E3, E4])
         seq_c = western.seq([C5, G5, E3, E4])

         print(seq_a.is_equivalent(seq_b))
         print(seq_a.is_equivalent(seq_c))

      .. testoutput:: WesternNotation

         True
         False

Iteration
--------------------------------------------

Like other sequence types pitch/note sequences support iteration:

.. tabs::

   .. tab:: EDO

      .. testcode:: EDOTuning

         from xenharmlib import EDOTuning
         edo31 = EDOTuning(31)

         seq = edo31.index_seq([10, 8, 7, 10])

         for pitch in seq:
             print('-->', pitch)

      .. testoutput:: EDOTuning

         --> EDOPitch(10, 31-EDO)
         --> EDOPitch(8, 31-EDO)
         --> EDOPitch(7, 31-EDO)
         --> EDOPitch(10, 31-EDO)

   .. tab:: Prime Limit

      .. testcode:: PrimeLimitTuning

         from xenharmlib import PrimeLimitTuning
         limit5 = PrimeLimitTuning(5)

         seq = limit5.rs_seq(['5/4', '6/5', '5/4', '10/9'])

         for pitch in seq:
             print('-->', pitch)

      .. testoutput:: PrimeLimitTuning

         --> PrimeLimitPitch(5/4, 5-Limit)
         --> PrimeLimitPitch(6/5, 5-Limit)
         --> PrimeLimitPitch(5/4, 5-Limit)
         --> PrimeLimitPitch(10/9, 5-Limit)

   .. tab:: Western

      .. testcode:: WesternNotation

         from xenharmlib import WesternNotation
         western = WesternNotation()

         seq = western.index_seq([0, 4, 2, 5, 7])

         for note in seq:
             print('-->', note)

      .. testoutput:: WesternNotation

         --> WesternNote(C, 0)
         --> WesternNote(E, 0)
         --> WesternNote(D, 0)
         --> WesternNote(F, 0)
         --> WesternNote(G, 0)

   .. tab:: UpDown

      .. testcode:: UpDownNotation

         from xenharmlib import EDOTuning
         from xenharmlib import UpDownNotation

         edo31 = EDOTuning(31)
         n_edo31 = UpDownNotation(edo31)

         seq = n_edo31.index_seq([0, 10, 8, 5, 18])

         for note in seq:
             print('-->', note)

      .. testoutput:: UpDownNotation

         --> UpDownNote(C, 0, 31-EDO)
         --> UpDownNote(E, 0, 31-EDO)
         --> UpDownNote(Eb, 0, 31-EDO)
         --> UpDownNote(D, 0, 31-EDO)
         --> UpDownNote(G, 0, 31-EDO)

Element Containment
--------------------------------------------

If you want to know if a specific note or pitch is contained inside of a
sequence you can use the :code:`in` operator:

.. tabs::

   .. tab:: EDO

      .. testcode:: EDOTuning

         from xenharmlib import EDOTuning
         edo31 = EDOTuning(31)

         seq = edo31.index_seq([10, 8, 7, 10])
         pitch_a = edo31.pitch(7)
         pitch_b = edo31.pitch(9)

         print(pitch_a in seq)
         print(pitch_b in seq)

      .. testoutput:: EDOTuning

         True
         False

   .. tab:: Prime Limit

      .. testcode:: PrimeLimitTuning

         from xenharmlib import PrimeLimitTuning
         limit5 = PrimeLimitTuning(5)

         seq = limit5.rs_seq(['5/4', '6/5', '5/4', '10/9'])
         pitch_a = limit5.rs_pitch('6/5')
         pitch_b = limit5.rs_pitch('3/2')

         print(pitch_a in seq)
         print(pitch_b in seq)

      .. testoutput:: PrimeLimitTuning

         True
         False

   .. tab:: Western

      .. testcode:: WesternNotation

         from xenharmlib import WesternNotation
         western = WesternNotation()

         seq = western.index_seq([3, 5, 5, 3, 5])
         pitch_a = western.note('F', 0)
         pitch_b = western.note('G', 0)

         print(pitch_a in seq)
         print(pitch_b in seq)

      .. testoutput:: WesternNotation

         True
         False

   .. tab:: UpDown

      .. testcode:: UpDownNotation

         from xenharmlib import EDOTuning
         from xenharmlib import UpDownNotation

         edo31 = EDOTuning(31)
         n_edo31 = UpDownNotation(edo31)

         seq = n_edo31.index_seq([10, 11, 10, 10, 18])
         pitch_a = n_edo31.note('E', 0)
         pitch_b = n_edo31.note('vE', 0)

         print(pitch_a in seq)
         print(pitch_b in seq)

      .. testoutput:: UpDownNotation

         True
         False


Item Retrieval and Slicing
------------------------------

Single elements from the sequence can be obtained by their index.
You can also use slices (including step size) to extract portions
of a sequence:

.. tabs::

   .. tab:: EDO

      .. testcode:: EDOTuning

         from xenharmlib import EDOTuning
         edo31 = EDOTuning(31)

         seq = edo31.index_seq([10, 8, 7, 10])

         print(seq[2])
         print(seq[1:3])
         print(seq[::2])

      .. testoutput:: EDOTuning

         EDOPitch(7, 31-EDO)
         EDOPitchSeq([8, 7], 31-EDO)
         EDOPitchSeq([10, 7], 31-EDO)

   .. tab:: Prime Limit

      .. testcode:: PrimeLimitTuning

         from xenharmlib import PrimeLimitTuning
         limit5 = PrimeLimitTuning(5)

         seq = limit5.rs_seq(['5/4', '6/5', '5/4', '10/9'])

         print(seq[2])
         print(seq[1:3])
         print(seq[::2])

      .. testoutput:: PrimeLimitTuning

         PrimeLimitPitch(5/4, 5-Limit)
         PrimeLimitPitchSeq([6/5, 5/4], 5-Limit)
         PrimeLimitPitchSeq([5/4, 5/4], 5-Limit)

   .. tab:: Western

      .. testcode:: WesternNotation

         from xenharmlib import WesternNotation
         western = WesternNotation()

         seq = western.index_seq([3, 5, 5, 3, 5])

         print(seq[2])
         print(seq[1:4])
         print(seq[::2])

      .. testoutput:: WesternNotation

         WesternNote(F, 0)
         WesternNoteSeq([F0, F0, D#0])
         WesternNoteSeq([D#0, F0, F0])

   .. tab:: UpDown

      .. testcode:: UpDownNotation

         from xenharmlib import EDOTuning
         from xenharmlib import UpDownNotation

         edo31 = EDOTuning(31)
         n_edo31 = UpDownNotation(edo31)

         seq = n_edo31.index_seq([10, 11, 10, 10, 18])

         print(seq[1])
         print(seq[1:4])
         print(seq[::2])

      .. testoutput:: UpDownNotation

         UpDownNote(Fb, 0, 31-EDO)
         UpDownNoteSeq([Fb0, E0, E0], 31-EDO)
         UpDownNoteSeq([E0, E0, G0], 31-EDO)

Element Search
------------------

The :meth:`~xenharmlib.core.freq_repr_seq.FreqReprSeq.index` method returns
the first index position where a pitch or note was found (or raises
:code:`ValueError` if the desired element does not exist in the sequence). 

.. tabs::

   .. tab:: EDO

      .. testcode:: EDOTuning

         from xenharmlib import EDOTuning
         edo31 = EDOTuning(31)

         seq = edo31.index_seq([10, 8, 7, 10])
         pitch = edo31.pitch(7)

         print(seq.index(pitch))

      .. testoutput:: EDOTuning

         2

   .. tab:: Prime Limit

      .. testcode:: PrimeLimitTuning

         from xenharmlib import PrimeLimitTuning
         limit5 = PrimeLimitTuning(5)

         seq = limit5.rs_seq(['5/4', '6/5', '5/4', '10/9'])
         pitch = limit5.rs_pitch('6/5')

         print(seq.index(pitch))

      .. testoutput:: PrimeLimitTuning

         1

   .. tab:: Western

      .. testcode:: WesternNotation

         from xenharmlib import WesternNotation
         western = WesternNotation()

         seq = western.index_seq([3, 5, 5, 3, 5])
         note = western.note('F', 0)

         print(seq.index(note))

      .. testoutput:: WesternNotation

         1

   .. tab:: UpDown

      .. testcode:: UpDownNotation

         from xenharmlib import EDOTuning
         from xenharmlib import UpDownNotation

         edo31 = EDOTuning(31)
         n_edo31 = UpDownNotation(edo31)

         seq = n_edo31.index_seq([10, 11, 10, 10, 18])
         note = n_edo31.note('E', 0)

         print(seq.index(note))

      .. testoutput:: UpDownNotation

         0

Counting
------------------

For statistical analysis xenharmlib can calculate the number of times a
specific pitch or note occurs in a sequence:

.. tabs::

   .. tab:: EDO

      .. testcode:: EDOTuning

         from xenharmlib import EDOTuning
         edo31 = EDOTuning(31)

         seq = edo31.index_seq([10, 8, 7, 10])
         pitch = edo31.pitch(7)

         print(seq.count(pitch))

      .. testoutput:: EDOTuning

         1

   .. tab:: Prime Limit

      .. testcode:: PrimeLimitTuning

         from xenharmlib import PrimeLimitTuning
         limit5 = PrimeLimitTuning(5)

         seq = limit5.rs_seq(['5/4', '6/5', '5/4', '10/9'])
         pitch = limit5.rs_pitch('5/4')

         print(seq.count(pitch))

      .. testoutput:: PrimeLimitTuning

         2

   .. tab:: Western

      .. testcode:: WesternNotation

         from xenharmlib import WesternNotation
         western = WesternNotation()

         seq = western.index_seq([3, 5, 5, 3, 5])
         note = western.note('F', 0)

         print(seq.count(note))

      .. testoutput:: WesternNotation

         3

   .. tab:: UpDown

      .. testcode:: UpDownNotation

         from xenharmlib import EDOTuning
         from xenharmlib import UpDownNotation

         edo31 = EDOTuning(31)
         n_edo31 = UpDownNotation(edo31)

         seq = n_edo31.index_seq([10, 11, 10, 10, 18])
         note = n_edo31.note('G', 0)

         print(seq.count(note))

      .. testoutput:: UpDownNotation

         1

Index Masks and Partial Sequences
----------------------------------------------

You can extract (continuous or non-continous) parts from a sequence
with the
:meth:`~xenharmlib.core.freq_repr_seq.FreqReprSeq.partial` method that
expects an index mask expression, i.e. a tuple with indices pointing
to sequence elements that should be extracted.

The mask :code:`(1, 3, 4)` for example extracts the second, fourth and
fifth element of the sequence (like with item retrieval indices in an a
mask expression start with 0):

.. tabs::

   .. tab:: EDO

      .. testcode:: EDOTuning

         from xenharmlib import EDOTuning
         edo31 = EDOTuning(31)

         seq = edo31.index_seq([10, 8, 10, 9, 10, 8])
         print(seq.partial((1, 3, 4)))

      .. testoutput:: EDOTuning

         EDOPitchSeq([8, 9, 10], 31-EDO)

   .. tab:: Prime Limit

      .. testcode:: PrimeLimitTuning

         from xenharmlib import PrimeLimitTuning
         limit5 = PrimeLimitTuning(5)

         seq = limit5.rs_seq(['5/4', '6/5', '9/8', '6/5', '10/9'])
         print(seq.partial((1, 3, 4)))

      .. testoutput:: PrimeLimitTuning

         PrimeLimitPitchSeq([6/5, 6/5, 10/9], 5-Limit)

   .. tab:: Western

      .. testcode:: WesternNotation

         from xenharmlib import WesternNotation
         western = WesternNotation()

         E0 = western.note('E', 0)
         Eb0 = western.note('Eb', 0)
         Csharp0 = western.note('C#', 0)

         seq = western.seq([E0, Eb0, Csharp0, Csharp0, E0, Eb0])
         print(seq.partial((1, 3, 4)))

      .. testoutput:: WesternNotation

         WesternNoteSeq([Eb0, C#0, E0])

Mask expressions targeted at longer continuous spans inside the
sequence can be written as a "shortform" with the ellipsis symbol
(:code:`...`):

.. tabs::

   .. tab:: EDO

      .. testcode:: EDOTuning

         from xenharmlib import EDOTuning
         edo31 = EDOTuning(31)

         seq = edo31.index_seq([10, 8, 10, 9, 10, 8])

         # an ellipsis as a prefix matches all elements from
         # the start of the sequence until and including (!)
         # the first mask index
         print(seq.partial((..., 3, 4)))

         # an ellipsis between two indices matches the two indices
         # in the sequence and all elements between them
         print(seq.partial((1, ..., 4)))

         # an ellipsis at the end matches all remaining indices
         # in the sequence after the last mask index
         print(seq.partial((0, 3, ...)))

      .. testoutput:: EDOTuning

         EDOPitchSeq([10, 8, 10, 9, 10], 31-EDO)
         EDOPitchSeq([8, 10, 9, 10], 31-EDO)
         EDOPitchSeq([10, 9, 10, 8], 31-EDO)

   .. tab:: Prime Limit

      .. testcode:: PrimeLimitTuning

         from xenharmlib import PrimeLimitTuning
         limit5 = PrimeLimitTuning(5)

         seq = limit5.rs_seq(['5/4', '6/5', '9/8', '6/5', '10/9'])

         # an ellipsis as a prefix matches all elements from
         # the start of the sequence until and including (!)
         # the first mask index
         print(seq.partial((..., 3, 4)))

         # an ellipsis between two indices matches the two indices
         # in the sequence and all elements between them
         print(seq.partial((1, ..., 4)))

         # an ellipsis at the end matches all remaining indices
         # in the sequence after the last mask index
         print(seq.partial((0, 3, ...)))

      .. testoutput:: PrimeLimitTuning

         PrimeLimitPitchSeq([5/4, 6/5, 9/8, 6/5, 10/9], 5-Limit)
         PrimeLimitPitchSeq([6/5, 9/8, 6/5, 10/9], 5-Limit)
         PrimeLimitPitchSeq([5/4, 6/5, 10/9], 5-Limit)

   .. tab:: Western

      .. testcode:: WesternNotation

         from xenharmlib import WesternNotation
         western = WesternNotation()

         E0 = western.note('E', 0)
         Eb0 = western.note('Eb', 0)
         Csharp0 = western.note('C#', 0)

         seq = western.seq([E0, Eb0, Csharp0, Csharp0, E0, Eb0])

         # an ellipsis as a prefix matches all elements from
         # the start of the sequence until and including (!)
         # the first mask index
         print(seq.partial((..., 3, 4)))

         # an ellipsis between two indices matches the two indices
         # in the sequence and all elements between them
         print(seq.partial((1, ..., 4)))

         # an ellipsis at the end matches all remaining indices
         # in the sequence after the last mask index
         print(seq.partial((0, 3, ...)))

      .. testoutput:: WesternNotation

         WesternNoteSeq([E0, Eb0, C#0, C#0, E0])
         WesternNoteSeq([Eb0, C#0, C#0, E0])
         WesternNoteSeq([E0, C#0, E0, Eb0])

Selection can also be inverted with the
:meth:`~xenharmlib.core.freq_repr_seq.FreqReprSeq.partial_not` method that
returns all elements *not* covered by the mask expression:

.. tabs::

   .. tab:: EDO

      .. testcode:: EDOTuning

         from xenharmlib import EDOTuning
         edo31 = EDOTuning(31)

         seq = edo31.index_seq([10, 8, 10, 9, 10, 8])
         print(seq.partial_not((1, 3, 4)))

      .. testoutput:: EDOTuning

         EDOPitchSeq([10, 10, 8], 31-EDO)

   .. tab:: Prime Limit

      .. testcode:: PrimeLimitTuning

         from xenharmlib import PrimeLimitTuning
         limit5 = PrimeLimitTuning(5)

         seq = limit5.rs_seq(['5/4', '6/5', '9/8', '6/5', '10/9'])
         print(seq.partial_not((1, 3, 4)))

      .. testoutput:: PrimeLimitTuning

         PrimeLimitPitchSeq([5/4, 9/8], 5-Limit)

   .. tab:: Western

      .. testcode:: WesternNotation

         from xenharmlib import WesternNotation
         western = WesternNotation()

         E0 = western.note('E', 0)
         Eb0 = western.note('Eb', 0)
         Csharp0 = western.note('C#', 0)

         seq = western.seq([E0, Eb0, Csharp0, Csharp0, E0, Eb0])
         print(seq.partial_not((1, 3, 4)))

      .. testoutput:: WesternNotation

         WesternNoteSeq([E0, C#0, Eb0])

To get both the substructure indicated by the mask *and* its complement as
a tuple, you can use the
:meth:`~xenharmlib.core.freq_repr_seq.FreqReprSeq.partition` method:

.. tabs::

   .. tab:: EDO

      .. testcode:: EDOTuning

         from xenharmlib import EDOTuning
         edo31 = EDOTuning(31)

         seq = edo31.index_seq([10, 8, 10, 9, 10, 8])
         a, b = seq.partition((1, 3, 4))
         print(a)
         print(b)

      .. testoutput:: EDOTuning

         EDOPitchSeq([8, 9, 10], 31-EDO)
         EDOPitchSeq([10, 10, 8], 31-EDO)

   .. tab:: Prime Limit

      .. testcode:: PrimeLimitTuning

         from xenharmlib import PrimeLimitTuning
         limit5 = PrimeLimitTuning(5)

         seq = limit5.rs_seq(['5/4', '6/5', '9/8', '6/5', '10/9'])
         a, b = seq.partition((1, 3, 4))
         print(a)
         print(b)

      .. testoutput:: PrimeLimitTuning

         PrimeLimitPitchSeq([6/5, 6/5, 10/9], 5-Limit)
         PrimeLimitPitchSeq([5/4, 9/8], 5-Limit)

   .. tab:: Western

      .. testcode:: WesternNotation

         from xenharmlib import WesternNotation
         western = WesternNotation()

         E0 = western.note('E', 0)
         Eb0 = western.note('Eb', 0)
         Csharp0 = western.note('C#', 0)

         seq = western.seq([E0, Eb0, Csharp0, Csharp0, E0, Eb0])
         a, b = seq.partition((1, 3, 4))
         print(a)
         print(b)

      .. testoutput:: WesternNotation

         WesternNoteSeq([Eb0, C#0, E0])
         WesternNoteSeq([E0, C#0, Eb0])


Concatenation and Repetition
--------------------------------------

Like python's builtin list and tuple types xenharmlib's sequence primitive
allows concatenation of two objects and multiplication with scalars with
the meaning "repeat x times":

.. tabs::

   .. tab:: EDO

      .. testcode:: EDOTuning

         from xenharmlib import EDOTuning
         edo31 = EDOTuning(31)

         seq_a = edo31.index_seq([0, 5, 10, 5])
         seq_b = edo31.index_seq([10, 5, 5, 10])
         print(seq_a + seq_b)
         print(3 * seq_a)

      .. testoutput:: EDOTuning

         EDOPitchSeq([0, 5, 10, 5, 10, 5, 5, 10], 31-EDO)
         EDOPitchSeq([0, 5, 10, 5, 0, 5, 10, 5, 0, 5, 10, 5], 31-EDO)

   .. tab:: Prime Limit

      .. testcode:: PrimeLimitTuning

         from xenharmlib import PrimeLimitTuning
         limit5 = PrimeLimitTuning(5)

         seq_a = limit5.rs_seq(['1/1', '5/4', '9/8', '5/4'])
         seq_b = limit5.rs_seq(['9/8', '1/1', '5/4', '5/4'])
         print(seq_a + seq_b)
         print(3 * seq_a)

      .. testoutput:: PrimeLimitTuning

         PrimeLimitPitchSeq([1, 5/4, 9/8, 5/4, 9/8, 1, 5/4, 5/4], 5-Limit)
         PrimeLimitPitchSeq([1, 5/4, 9/8, 5/4, 1, 5/4, 9/8, 5/4, 1, 5/4, 9/8, 5/4], 5-Limit)

   .. tab:: Western

      .. testcode:: WesternNotation

         from xenharmlib import WesternNotation
         western = WesternNotation()

         C4 = western.note('C', 4)
         D4 = western.note('D', 4)
         E4 = western.note('E', 4)

         seq_a = western.seq([C4, D4, E4, C4])
         seq_b = western.seq([E4, C4, D4, C4])
         print(seq_a + seq_b)
         print(3 * seq_a)

      .. testoutput:: WesternNotation

         WesternNoteSeq([C4, D4, E4, C4, E4, C4, D4, C4])
         WesternNoteSeq([C4, D4, E4, C4, C4, D4, E4, C4, C4, D4, E4, C4])

Transposition
--------------------------------------

Sequences can be transposed with the
:meth:`~xenharmlib.core.freq_repr_seq.FreqReprSeq.transpose`
method. This is typically done by providing an
:doc:`interval object <prim_interval>` of the same origin context:

.. tabs::

   .. tab:: EDO

      .. testcode:: EDOTuning

         from xenharmlib import EDOTuning
         edo31 = EDOTuning(31)

         seq = edo31.index_seq([3, 10, 19, 10])
         interval = edo31.diff_interval(8)
         print(seq.transpose(interval))

      .. testoutput:: EDOTuning

         EDOPitchSeq([11, 18, 27, 18], 31-EDO)

   .. tab:: Prime Limit

      .. testcode:: PrimeLimitTuning

         from xenharmlib import PrimeLimitTuning
         limit5 = PrimeLimitTuning(5)

         seq = limit5.rs_seq(['1/1', '5/4', '3/2', '5/4'])
         interval = limit5.rs_interval('9/8')
         print(seq.transpose(interval))

      .. testoutput:: PrimeLimitTuning

         PrimeLimitPitchSeq([9/8, 45/32, 27/16, 45/32], 5-Limit)

   .. tab:: Western

      .. testcode:: WesternNotation

         from xenharmlib import WesternNotation
         western = WesternNotation()

         seq = western.seq([western.note(pcs, 4) for pcs in 'CDFEGAA'])
         interval = western.shorthand_interval('A', 3)
         print(seq.transpose(interval))

      .. testoutput:: WesternNotation

         WesternNoteSeq([E#4, Fx4, A#4, Gx4, B#4, Cx5, Cx5])

   .. tab:: UpDown

      .. testcode:: UpDownNotation

         from xenharmlib import EDOTuning
         from xenharmlib import UpDownNotation

         edo31 = EDOTuning(31)
         n_edo31 = UpDownNotation(edo31)

         Gb4 = n_edo31.note('Gb', 4)
         Aup4 = n_edo31.note('^A', 4)
         Bb4 = n_edo31.note('Bb', 4)

         seq = n_edo31.seq([Gb4, Aup4, Bb4, Aup4])
         interval = n_edo31.shorthand_interval('^m', 2)
         print(seq.transpose(interval))

      .. testoutput:: UpDownNotation

         UpDownNoteSeq([^Abb4, ^^Bb4, ^Cb5, ^^Bb4], 31-EDO)

The :meth:`~xenharmlib.core.freq_repr_seq.FreqReprSeq.transpose` method
also accepts a **pitch difference**. A pitch difference is an integer or
lattice point that defines the numeric distance between two frequency
representations. In the case of notations with enharmonic ambiguity
xenharmlib makes a guess which note should be picked.

.. tabs::

   .. tab:: EDO

      .. testcode:: EDOTuning

         from xenharmlib import EDOTuning
         edo31 = EDOTuning(31)

         seq = edo31.index_seq([3, 10, 19, 10])
         print(seq.transpose(8))

      .. testoutput:: EDOTuning

         EDOPitchSeq([11, 18, 27, 18], 31-EDO)

   .. tab:: Prime Limit

      .. testcode:: PrimeLimitTuning

         from xenharmlib import PrimeLimitTuning
         limit5 = PrimeLimitTuning(5)

         seq = limit5.rs_seq(['1/1', '5/4', '3/2', '5/4'])
         pitch_diff = limit5.lattice.point((-1, 0, 1))
         print(seq.transpose(pitch_diff))

      .. testoutput:: PrimeLimitTuning

         PrimeLimitPitchSeq([5/2, 25/8, 15/4, 25/8], 5-Limit)

   .. tab:: Western

      .. testcode:: WesternNotation

         from xenharmlib import WesternNotation
         western = WesternNotation()

         seq = western.seq([western.note(pcs, 4) for pcs in 'CDFGABE'])
         print(seq.transpose(2))

      .. testoutput:: WesternNotation

         WesternNoteSeq([D4, E4, G4, A4, B4, C#5, F#4])

   .. tab:: UpDown

      .. testcode:: UpDownNotation

         from xenharmlib import EDOTuning
         from xenharmlib import UpDownNotation

         edo31 = EDOTuning(31)
         n_edo31 = UpDownNotation(edo31)

         Gb4 = n_edo31.note('Gb', 4)
         Aup4 = n_edo31.note('^A', 4)
         Bb4 = n_edo31.note('Bb', 4)

         seq = n_edo31.seq([Gb4, Aup4, Bb4, Aup4])
         print(seq.transpose(18))

      .. testoutput:: UpDownNotation

         UpDownNoteSeq([Db5, Fb5, F5, Fb5], 31-EDO)


Retrograde and Inversion
--------------------------------------

Sequences provide the
:meth:`~xenharmlib.core.freq_repr_seq.FreqReprSeq.retrograde` and
:meth:`~xenharmlib.core.freq_repr_seq.FreqReprSeq.inversion` method,
which return a horizontally mirrored and vertically mirrored
sequence respectively: Retrograde reads the sequence from end-to-start
while Inversion flips the direction of every interval in the sequence:

.. tabs::

   .. tab:: EDO

      .. testcode:: EDOTuning

         from xenharmlib import EDOTuning
         edo31 = EDOTuning(31)

         seq = edo31.index_seq([0, 10, 49, 13, 18])
         print(seq.retrograde())
         print(seq.inversion())

      .. testoutput:: EDOTuning

         EDOPitchSeq([18, 13, 49, 10, 0], 31-EDO)
         EDOPitchSeq([0, -10, -49, -13, -18], 31-EDO)

   .. tab:: Prime Limit

      .. testcode:: PrimeLimitTuning

         from xenharmlib import PrimeLimitTuning
         limit5 = PrimeLimitTuning(5)

         seq = limit5.rs_seq(['3/2', '1/1', '2/1', '5/2', '1/1'])
         print(seq.retrograde())
         print(seq.inversion())

      .. testoutput:: PrimeLimitTuning

         PrimeLimitPitchSeq([1, 5/2, 2, 1, 3/2], 5-Limit)
         PrimeLimitPitchSeq([3/2, 9/4, 9/8, 9/10, 9/4], 5-Limit)

   .. tab:: Western

      .. testcode:: WesternNotation

         from xenharmlib import WesternNotation
         western = WesternNotation()

         E4 = western.note('E', 4)
         G4 = western.note('G', 4)
         C5 = western.note('C', 5)
         E5 = western.note('E', 5)

         seq = western.seq([G4, C5, E5, E4])

         print(seq.retrograde())
         print(seq.inversion())

      .. testoutput:: WesternNotation

         WesternNoteSeq([E4, E5, C5, G4])
         WesternNoteSeq([G4, D4, Bb3, Bb4])


Subsequence Containment
--------------------------------------

If you have two sequences you can test whether one sequence is a subsequence
of the other with the
:meth:`~xenharmlib.core.freq_repr_seq.FreqReprSeq.is_subseq` method:


.. tabs::

   .. tab:: EDO

      .. testcode:: EDOTuning

         from xenharmlib import EDOTuning
         edo31 = EDOTuning(31)

         seq_a = edo31.index_seq([9, 9, 10])
         seq_b = edo31.index_seq([9, 7, 10])
         seq_c = edo31.index_seq([10, 8, 7, 10, 9, 9, 10, 8])

         print(seq_a.is_subseq(seq_c))
         print(seq_b.is_subseq(seq_c))

      .. testoutput:: EDOTuning

         True
         False

   .. tab:: Prime Limit

      .. testcode:: PrimeLimitTuning

         from xenharmlib import PrimeLimitTuning
         limit5 = PrimeLimitTuning(5)

         seq_a = limit5.rs_seq(['6/5', '5/4', '10/9'])
         seq_b = limit5.rs_seq(['1/1', '5/4', '10/9'])
         seq_c = limit5.rs_seq(['5/4', '6/5', '5/4', '10/9', '5/4', '3/2'])

         print(seq_a.is_subseq(seq_c))
         print(seq_b.is_subseq(seq_c))

      .. testoutput:: PrimeLimitTuning

         True
         False

   .. tab:: Western

      .. testcode:: WesternNotation

         from xenharmlib import WesternNotation
         western = WesternNotation()

         seq_a = western.index_seq([3, 5, 3, 3, 7])
         seq_b = western.index_seq([6, 2, 1])
         seq_c = western.index_seq([3, 5, 5, 3, 5, 3, 3, 7, 2, 1])

         print(seq_a.is_subseq(seq_c))
         print(seq_b.is_subseq(seq_c))

      .. testoutput:: WesternNotation

         True
         False

   .. tab:: UpDown

      .. testcode:: UpDownNotation

         from xenharmlib import EDOTuning
         from xenharmlib import UpDownNotation

         edo31 = EDOTuning(31)
         n_edo31 = UpDownNotation(edo31)

         seq_a = n_edo31.index_seq([10, 10, 18, 11])
         seq_b = n_edo31.index_seq([8, 11, 18])
         seq_c = n_edo31.index_seq([10, 11, 10, 10, 18, 11, 18])

         print(seq_a.is_subseq(seq_c))
         print(seq_b.is_subseq(seq_c))

      .. testoutput:: UpDownNotation

         True
         False

Subsequence Search
--------------------------------------

To find the position where a subsequence begins you can call the
:meth:`~xenharmlib.core.freq_repr_seq.FreqReprSeq.subseq_index` method
on the (possible) supersequence:

.. tabs::

   .. tab:: EDO

      .. testcode:: EDOTuning

         from xenharmlib import EDOTuning
         edo31 = EDOTuning(31)

         seq_a = edo31.index_seq([10, 8, 7, 10, 9, 9, 10, 8])
         seq_b = edo31.index_seq([9, 9, 10])

         print(seq_a.subseq_index(seq_b))

      .. testoutput:: EDOTuning

         4

   .. tab:: Prime Limit

      .. testcode:: PrimeLimitTuning

         from xenharmlib import PrimeLimitTuning
         limit5 = PrimeLimitTuning(5)

         seq_a = limit5.rs_seq(['5/4', '6/5', '5/4', '10/9', '5/4', '3/2'])
         seq_b = limit5.rs_seq(['6/5', '5/4', '10/9'])

         print(seq_a.subseq_index(seq_b))

      .. testoutput:: PrimeLimitTuning

         1

   .. tab:: Western

      .. testcode:: WesternNotation

         from xenharmlib import WesternNotation
         western = WesternNotation()

         seq_a = western.index_seq([3, 5, 5, 3, 5, 3, 3, 7, 2, 1])
         seq_b = western.index_seq([3, 5, 3, 3, 7])

         print(seq_a.subseq_index(seq_b))

      .. testoutput:: WesternNotation

         3

   .. tab:: UpDown

      .. testcode:: UpDownNotation

         from xenharmlib import EDOTuning
         from xenharmlib import UpDownNotation

         edo31 = EDOTuning(31)
         n_edo31 = UpDownNotation(edo31)

         seq_a = n_edo31.index_seq([10, 11, 10, 10, 18, 11, 18])
         seq_b = n_edo31.index_seq([10, 10, 18, 11])

         print(seq_a.subseq_index(seq_b))

      .. testoutput:: UpDownNotation

         2
