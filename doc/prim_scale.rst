Scales
==================

A scale in xenharmlib is a set of unique frequency representations, sorted
in ascending order, from lowest frequency to highest frequency. The scale
primitive allows *equivalent* frequency representations to coexist inside
its structure, but not identical ones. On creation xenharmlib will sort
the frequency representations and remove duplicate items:

.. testcode:: WesternNotation

   from xenharmlib import WesternNotation
   western = WesternNotation()

   C4 = western.note('C', 4)
   E4 = western.note('E', 4)
   G4 = western.note('G', 4)
   C5 = western.note('C', 5)

   # E4 will only appear once in scale, however
   # C4 and C5 are allowed to coexist
   scale = western.scale([E4, G4, E4, C4, C5])
   print(scale)

.. testoutput:: WesternNotation

   WesternNoteScale([C4, E4, G4, C5])

Scales in xenharmlib are not restricted to the span of the equivalency
interval (e.g. the octave), meaning the scale primitive can also be used
to analyze polychords and related structures:

.. testcode:: WesternNotation

   C4 = western.note('C', 4)
   E4 = western.note('E', 4)
   G4 = western.note('G', 4)
   B4 = western.note('B', 4)
   D5 = western.note('D', 5)

   polychord = western.scale([C4, E4, G4, B4, D5])
   print(polychord)

.. testoutput:: WesternNotation

   WesternNoteScale([C4, E4, G4, B4, D5])

Scales can be built from any iterable object that includes pitches or notes
of the same origin context. This includes e.g. python's lists, tuples, sets,
generators and xenharmlib's sequence primitive.

.. testcode:: WesternNotation

   C4 = western.note('C', 4)
   E4 = western.note('E', 4)
   G4 = western.note('G', 4)

   # from list, set, tuple and generator
   scale_a = western.scale([C4, E4, G4])
   scale_b = western.scale({C4, E4, G4})
   scale_c = western.scale((C4, E4, G4))
   scale_d = western.scale(western.note(pcs, 4) for pcs in 'CEG')

   # from xenharmlib's sequence primitive
   seq = western.seq([C4, G4, E4, E4, C4])
   scale_e = western.scale(seq)

   print(scale_a == scale_b == scale_c == scale_d == scale_e)

.. testoutput:: WesternNotation

   True

For post-tonal theory the scale primitive can be used as a pitch set
or pitch class set. Since xenharmlib implements a more general framework
of music theory double-digit pitch class indices are not abbreviated
with 'T' for ten or 'E' for eleven, but returned in their numerical form.

Xenharmlib's support for multi-generator tunings and notations also
means that pitch or pitch class indices are not necessarily represented
by integers, but can also be lattice points:

.. tabs::

   .. tab:: EDO

      .. testcode:: EDOTuning

         from xenharmlib import EDOTuning
         edo31 = EDOTuning(31)

         p41 = edo31.pitch(41)
         p49 = edo31.pitch(49)
         p62 = edo31.pitch(62)

         scale = edo31.scale([p41, p49, p62])
         print(scale.pitch_indices)
         print(scale.pc_indices)

      .. testoutput:: EDOTuning

         [41, 49, 62]
         [10, 18, 0]

   .. tab:: Prime Limit

      .. testcode:: PrimeLimitTuning

         from xenharmlib import PrimeLimitTuning
         limit5 = PrimeLimitTuning(5)

         E0 = limit5.rs_pitch('5/4')
         G0 = limit5.rs_pitch('3/2')
         C1 = limit5.rs_pitch('2/1')

         scale = limit5.scale([E0, G0, C1])
         print(scale.pitch_indices)
         print(scale.pc_indices)

      .. testoutput:: PrimeLimitTuning

         [LatticePoint(-2, 0, 1), LatticePoint(-1, 1, 0), LatticePoint(1, 0, 0)]
         [LatticePoint(-2, 0, 1), LatticePoint(-1, 1, 0), LatticePoint(0, 0, 0)]

   .. tab:: Western

      .. testcode:: WesternNotation

         from xenharmlib import WesternNotation
         western = WesternNotation()

         E4 = western.note('E', 4)
         G4 = western.note('G', 4)
         C5 = western.note('C', 5)

         scale = western.scale([E4, G4, C5])
         print(scale.pitch_indices)
         print(scale.pc_indices)

      .. testoutput:: WesternNotation

         [52, 55, 60]
         [4, 7, 0]

   .. tab:: UpDown

      .. testcode:: UpDownNotation

         from xenharmlib import EDOTuning
         from xenharmlib import UpDownNotation

         edo31 = EDOTuning(31)
         n_edo31 = UpDownNotation(edo31)

         E4 = n_edo31.note('E', 4)
         Gup4 = n_edo31.note('^G', 4)
         C5 = n_edo31.note('C', 5)

         scale = n_edo31.scale([E4, Gup4, C5])
         print(scale.pitch_indices)
         print(scale.pc_indices)

      .. testoutput:: UpDownNotation

         [134, 143, 155]
         [10, 19, 0]

Deriving Scales
-------------------------------------------------------

The builder method most agnostic to the origin context is the
:meth:`~xenharmlib.core.origin_context.OriginContext.scale` method,
that takes a list of frequency representations originating from the
the same context and creates a scale primitive:

.. tabs::

   .. tab:: EDO

      .. testcode:: EDOTuning

         from xenharmlib import EDOTuning
         edo31 = EDOTuning(31)

         p0 = edo31.pitch(0)
         p10 = edo31.pitch(10)
         p18 = edo31.pitch(18)

         scale = edo31.scale([p0, p10, p18])
         print(scale)

      .. testoutput:: EDOTuning

         EDOPitchScale([0, 10, 18], 31-EDO)

   .. tab:: Prime Limit

      .. testcode:: PrimeLimitTuning

         from xenharmlib import PrimeLimitTuning
         limit5 = PrimeLimitTuning(5)

         C0 = limit5.rs_pitch('1/1')
         E0 = limit5.rs_pitch('5/4')
         G0 = limit5.rs_pitch('3/2')

         scale = limit5.scale([C0, E0, G0])
         print(scale)

      .. testoutput:: PrimeLimitTuning

         PrimeLimitPitchScale([1, 5/4, 3/2], 5-Limit)

   .. tab:: Western

      .. testcode:: WesternNotation

         from xenharmlib import WesternNotation
         western = WesternNotation()

         C4 = western.note('C', 4)
         E4 = western.note('E', 4)
         G4 = western.note('G', 4)

         scale = western.scale([C4, E4, G4])
         print(scale)

      .. testoutput:: WesternNotation

         WesternNoteScale([C4, E4, G4])

   .. tab:: UpDown

      .. testcode:: UpDownNotation

         from xenharmlib import EDOTuning
         from xenharmlib import UpDownNotation

         edo31 = EDOTuning(31)
         n_edo31 = UpDownNotation(edo31)

         E4 = n_edo31.note('E', 4)
         Gup4 = n_edo31.note('^G', 4)
         C5 = n_edo31.note('C', 5)

         scale = n_edo31.scale([E4, Gup4, C5])
         print(scale)

      .. testoutput:: UpDownNotation

         UpDownNoteScale([E4, ^G4, C5], 31-EDO)

Element-wise Construction
-------------------------------------------------------

Scales can be constructed element-wise. In line with xenharmlib's
immutable object design, this is not done with an append method like
in standard python, but with a method that returns a scale with
an additional element:

.. tabs::

   .. tab:: EDO

      .. testcode:: EDOTuning

         from xenharmlib import EDOTuning
         edo31 = EDOTuning(31)

         C0 = edo31.pitch(0)
         D0 = edo31.pitch(5)
         E0 = edo31.pitch(10)

         # start with empty scale
         scale = edo31.scale()

         for e in [C0, D0, E0]:
             scale = scale.with_element(e)
             print(scale)

      .. testoutput:: EDOTuning

         EDOPitchScale([0], 31-EDO)
         EDOPitchScale([0, 5], 31-EDO)
         EDOPitchScale([0, 5, 10], 31-EDO)

   .. tab:: Prime Limit

      .. testcode:: PrimeLimitTuning

         from xenharmlib import PrimeLimitTuning
         limit5 = PrimeLimitTuning(5)

         C0 = limit5.rs_pitch('1/1')
         D0 = limit5.rs_pitch('9/8')
         E0 = limit5.rs_pitch('5/4')

         # start with empty scale
         scale = limit5.scale()

         for e in [C0, D0, E0]:
             scale = scale.with_element(e)
             print(scale)

      .. testoutput:: PrimeLimitTuning

         PrimeLimitPitchScale([1], 5-Limit)
         PrimeLimitPitchScale([1, 9/8], 5-Limit)
         PrimeLimitPitchScale([1, 9/8, 5/4], 5-Limit)

   .. tab:: Western

      .. testcode:: WesternNotation

         from xenharmlib import WesternNotation
         western = WesternNotation()

         C4 = western.note('C', 4)
         D4 = western.note('D', 4)
         E4 = western.note('E', 4)

         # start with empty scale
         scale = western.scale()

         for e in [C4, D4, E4]:
             scale = scale.with_element(e)
             print(scale)

      .. testoutput:: WesternNotation

         WesternNoteScale([C4])
         WesternNoteScale([C4, D4])
         WesternNoteScale([C4, D4, E4])

   .. tab:: UpDown

      .. testcode:: UpDownNotation

         from xenharmlib import EDOTuning
         from xenharmlib import UpDownNotation

         edo31 = EDOTuning(31)
         n_edo31 = UpDownNotation(edo31)

         E4 = n_edo31.note('E', 4)
         Gup4 = n_edo31.note('^G', 4)
         C5 = n_edo31.note('C', 5)

         # start with empty scale
         scale = n_edo31.scale()

         for e in [E4, Gup4, C5]:
             scale = scale.with_element(e)
             print(scale)

      .. testoutput:: UpDownNotation

         UpDownNoteScale([E4], 31-EDO)
         UpDownNoteScale([E4, ^G4], 31-EDO)
         UpDownNoteScale([E4, ^G4, C5], 31-EDO)

Index-based Construction
-------------------------------------------------------

Scales can also conveniently be constructed by providing a list of indices,
which - depending on origin context - can be integers or lattice points.
This type of construction also works on the notation layer by employing
the notation's enharmonic strategy.

.. tabs::

   .. tab:: EDO

      .. testcode:: EDOTuning

         from xenharmlib import EDOTuning
         edo31 = EDOTuning(31)

         scale = edo31.index_scale([0, 10, 18])
         print(scale)

      .. testoutput:: EDOTuning

         EDOPitchScale([0, 10, 18], 31-EDO)

   .. tab:: Prime Limit

      .. testcode:: PrimeLimitTuning

         from xenharmlib import PrimeLimitTuning
         limit5 = PrimeLimitTuning(5)

         scale = limit5.index_scale(
             [
                 limit5.lattice.point((0, 0, 0)),
                 limit5.lattice.point((-3, 2, 0)),
                 limit5.lattice.point((-2, 0, 1)),
             ]
         )
         print(scale)

      .. testoutput:: PrimeLimitTuning

         PrimeLimitPitchScale([1, 9/8, 5/4], 5-Limit)

   .. tab:: Western

      .. testcode:: WesternNotation

         from xenharmlib import WesternNotation
         western = WesternNotation()

         scale = western.index_scale([0, 5, 7])
         print(scale)

      .. testoutput:: WesternNotation

         WesternNoteScale([C0, F0, G0])

   .. tab:: UpDown

      .. testcode:: UpDownNotation

         from xenharmlib import EDOTuning
         from xenharmlib import UpDownNotation

         edo31 = EDOTuning(31)
         n_edo31 = UpDownNotation(edo31)

         scale = n_edo31.index_scale([1, 10, 17])
         print(scale)

      .. testoutput:: UpDownNotation

         UpDownNoteScale([Dbb0, E0, Fx0], 31-EDO)

Tunings with lattice point indices provide the convenience builder method
:meth:`~xenharmlib.core.multigen.MultiGenTuning.vec_scale` that expects a
tuple instead of a lattice point object, making the the construction less
verbose:

.. tabs::

   .. tab:: Prime Limit

      .. testcode:: PrimeLimitTuning

         from xenharmlib import PrimeLimitTuning
         limit5 = PrimeLimitTuning(5)

         scale = limit5.vec_scale(
             [(1, 0, 0), (-1, 0, 1), (0, 1, 0)]
         )
         print(scale)

      .. testoutput:: PrimeLimitTuning

         PrimeLimitPitchScale([2, 5/2, 3], 5-Limit)

   .. tab:: 2.3.7 Subgroup

      .. testcode:: MultiGenTuning

         from xenharmlib import MultiGenTuning
         from xenharmlib import FrequencyRatio

         sg237 = MultiGenTuning(
             [FrequencyRatio(p) for p in [2, 3, 7]],
             eq_diff_vec=(1, 0, 0)
         )

         scale = sg237.vec_scale(
             [(0, 0, 0), (-1, -1, 1), (-1, 1, 0)]
         )
         print(scale)

      .. testoutput:: MultiGenTuning

         MultiGenPitchScale([(0, 0, 0), (-1, -1, 1), (-1, 1, 0)], G=(2, 3, 7))


PC Shortform Construction
-------------------------------------------------------

A common shortform to define scales is to simply define a succession of
pitch classes or pitch class symbols with the silent assumption that each
pitch class or symbol points to the next highest pitch of that class in
relation to its precedessor pitch.

If for example we spell the C major scale as :math:`C, D, E, F, G, A, B`
we assume an equivalency interval section for the first element (e.g.
we assume :math:`C` to stand for :math:`C0`) and then move upwards to
find the next D, resulting in :math:`D0`, from there moving upwards
to find the next `E`, finding :math:`E0` and so forth)

The same structure applies if we have a pitch class set from a textbook
given in the form :code:`[8, 11, 0, 3, 4]`: We assume a base interval
for the first pitch and then successively move upwards until we find
a pitch with the respective class and continue to do so, until we
have a scale whose :code:`.pc_indices` property is exactly like our
input values:

.. tabs::

   .. tab:: EDO

      .. testcode:: EDOTuning

         from xenharmlib import EDOTuning
         edo31 = EDOTuning(31)

         scale = edo31.pc_scale([18, 0, 10])
         print(scale)

      .. testoutput:: EDOTuning

         EDOPitchScale([18, 31, 41], 31-EDO)

   .. tab:: Prime Limit

      .. testcode:: PrimeLimitTuning

         from xenharmlib import PrimeLimitTuning
         limit5 = PrimeLimitTuning(5)

         scale = limit5.rs_pc_scale(
             ['3/2', '1/1', '5/4']
         )
         print(scale)

      .. testoutput:: PrimeLimitTuning

         PrimeLimitPitchScale([3/2, 2, 5/2], 5-Limit)

   .. tab:: Western

      .. testcode:: WesternNotation

         from xenharmlib import WesternNotation
         western = WesternNotation()

         scale = western.pc_scale(['C', 'D', 'E', 'F', 'G#', 'A', 'B'])
         print(scale)

      .. testoutput:: WesternNotation

         WesternNoteScale([C0, D0, E0, F0, G#0, A0, B0])

   .. tab:: UpDown

      .. testcode:: UpDownNotation

         from xenharmlib import EDOTuning
         from xenharmlib import UpDownNotation

         edo31 = EDOTuning(31)
         n_edo31 = UpDownNotation(edo31)

         scale = n_edo31.pc_scale(['^E', 'G', 'Ab', 'D#'])
         print(scale)

      .. testoutput:: UpDownNotation

         UpDownNoteScale([^E0, G0, Ab0, D#1], 31-EDO)


Construction Based on Closest Frequency
-----------------------------------------------------

In origin contexts based on integer indices you can build a scale from
a list of frequencies with the
:meth:`~xenharmlib.core.origin_context.OriginContext.closest_scale`
method that finds the closest representation for each frequency
and constructs a scale from it.

The frequency approximation feature can be especially useful for
spectralist composition techniques, where the composer takes a
sound and extracts the most prominent overtone frequencies to
emulate them with chords of another instrument. 

.. tabs::

   .. tab:: EDO

      .. testcode:: EDOTuning

         from xenharmlib import EDOTuning
         from xenharmlib import Frequency

         edo31 = EDOTuning(31)

         # overtone frequencies measured e.g. by
         # a spectrogramm plugin or librosa
         frequencies = [
             Frequency(f) for f in [230, 410, 460, 500, 690]
         ]

         scale = edo31.closest_scale(frequencies)
         print(scale)

      .. testoutput:: EDOTuning

         EDOPitchScale([118, 144, 149, 153, 167], 31-EDO)

   .. tab:: ED

      .. testcode:: EDTuning

         from xenharmlib import EDTuning
         from xenharmlib import Frequency
         from xenharmlib import FrequencyRatio

         bohlen_pierce = EDTuning(13, FrequencyRatio(3))

         # overtone frequencies measured e.g. by
         # a spectrogramm plugin or librosa
         frequencies = [
             Frequency(f) for f in [230, 410, 460, 500, 690]
         ]

         scale = bohlen_pierce.closest_scale(frequencies)
         print(scale)

      .. testoutput:: EDTuning

         EDPitchScale([31, 38, 39, 40, 44], 13ed3)

   .. tab:: Western

      .. testcode:: WesternNotation

         from xenharmlib import WesternNotation
         from xenharmlib import Frequency

         western = WesternNotation()

         # overtone frequencies measured e.g. by
         # a spectrogramm plugin or librosa
         frequencies = [
             Frequency(f) for f in [230, 410, 460, 500, 690]
         ]

         scale = western.closest_scale(frequencies)
         print(scale)

      .. testoutput:: WesternNotation

         WesternNoteScale([A#3, G#4, A#4, B4, F5])

   .. tab:: UpDown

      .. testcode:: UpDownNotation

         from xenharmlib import EDOTuning
         from xenharmlib import UpDownNotation
         from xenharmlib import Frequency

         edo31 = EDOTuning(31)
         n_edo31 = UpDownNotation(edo31)

         # overtone frequencies measured e.g. by
         # a spectrogramm plugin or librosa
         frequencies = [
             Frequency(f) for f in [230, 410, 460, 500, 690]
         ]

         scale = n_edo31.closest_scale(frequencies)
         print(scale)

      .. testoutput:: UpDownNotation

         UpDownNoteScale([A#3, G#4, A#4, Cb5, E#5], 31-EDO)

Relation to Other Primitives
-------------------------------------------------------

Scales can be transformed into three other harmonic primitives:
:doc:`Sequences <prim_seq>`,
:doc:`Interval Sequences <prim_interval_seq>` and
:doc:`Interval Fans <prim_interval_fan>`:

.. tabs::

   .. tab:: EDO

      .. testcode:: EDOTuning

         from xenharmlib import EDOTuning
         edo31 = EDOTuning(31)

         scale = edo31.index_scale([2, 4, 5])

         print(scale.to_seq())
         print(scale.to_interval_seq())
         print(scale.to_interval_fan())

      .. testoutput:: EDOTuning

         EDOPitchSeq([2, 4, 5], 31-EDO)
         EDOPitchIntervalSeq([2, 1], 31-EDO)
         EDOPitchIntervalFan([0, 2, 3], 31-EDO)

   .. tab:: Prime Limit

      .. testcode:: PrimeLimitTuning

         from xenharmlib import PrimeLimitTuning
         limit5 = PrimeLimitTuning(5)

         scale = limit5.rs_scale(
             ['3/2', '15/8', '9/4']
         )

         print(scale.to_seq())
         print(scale.to_interval_seq())
         print(scale.to_interval_fan())

      .. testoutput:: PrimeLimitTuning

         PrimeLimitPitchSeq([3/2, 15/8, 9/4], 5-Limit)
         PrimeLimitPitchIntervalSeq([5/4, 6/5], 5-Limit)
         PrimeLimitPitchIntervalFan([1, 5/4, 3/2], 5-Limit)

   .. tab:: Western

      .. testcode:: WesternNotation

         from xenharmlib import WesternNotation
         western = WesternNotation()

         scale = western.scale(
             [western.note(pcs, 0) for pcs in 'CEG']
         )

         print(scale.to_seq())
         print(scale.to_interval_seq())
         print(scale.to_interval_fan())

      .. testoutput:: WesternNotation

         WesternNoteSeq([C0, E0, G0])
         WesternNoteIntervalSeq([M3, m3])
         WesternNoteIntervalFan([P1, M3, P5])

   .. tab:: UpDown

      .. testcode:: UpDownNotation

         from xenharmlib import EDOTuning
         from xenharmlib import UpDownNotation

         edo31 = EDOTuning(31)
         n_edo31 = UpDownNotation(edo31)

         scale = n_edo31.pc_scale(['^E', 'G', 'Ab'])

         print(scale.to_seq())
         print(scale.to_interval_seq())
         print(scale.to_interval_fan())

      .. testoutput:: UpDownNotation

         UpDownNoteSeq([^E0, G0, Ab0], 31-EDO)
         UpDownNoteIntervalSeq([vm3, m2], 31-EDO)
         UpDownNoteIntervalFan([P1, vm3, vd4], 31-EDO)

It is also possible to create a scale *from* any of the other primitives.
While sequences can just be given to the scale constructor, interval
sequences and interval fans need a pitch or note as a reference point:

.. tabs::

   .. tab:: EDO

      .. testcode:: EDOTuning

         from xenharmlib import EDOTuning
         edo31 = EDOTuning(31)

         seq = edo31.index_seq([3, 5, 10, 18, 15, 10, 0])
         print(edo31.scale(seq))

         iseq = edo31.diff_interval_seq([5, 8, 5, 5, 5, 8])
         print(edo31.pitch(5).scale(iseq))

         ifan = edo31.diff_interval_fan([0, 5, 10, 11, 15])
         print(edo31.pitch(5).scale(ifan))

      .. testoutput:: EDOTuning

         EDOPitchScale([0, 3, 5, 10, 15, 18], 31-EDO)
         EDOPitchScale([5, 10, 18, 23, 28, 33, 41], 31-EDO)
         EDOPitchScale([5, 10, 15, 16, 20], 31-EDO)

   .. tab:: Prime Limit

      .. testcode:: PrimeLimitTuning

         from xenharmlib import PrimeLimitTuning
         limit5 = PrimeLimitTuning(5)

         seq = limit5.rs_seq(['3/2', '15/8', '9/4', '1/1', '15/8'])
         print(limit5.scale(seq))

         iseq = limit5.rs_interval_seq(['9/4', '9/4', '15/4', '9/4'])
         print(limit5.scale(iseq))

         ifan = limit5.rs_interval_fan(['1/1', '15/8', '3/2'])
         print(limit5.scale(ifan))

      .. testoutput:: PrimeLimitTuning

         PrimeLimitPitchScale([1, 3/2, 15/8, 9/4], 5-Limit)
         PrimeLimitPitchScale([9/4, 15/4], 5-Limit)
         PrimeLimitPitchScale([1, 3/2, 15/8], 5-Limit)

   .. tab:: Western

      .. testcode:: WesternNotation

         from xenharmlib import WesternNotation
         western = WesternNotation()

         seq = western.seq([western.note(pcs, 4) for pcs in 'CEGDEFE'])
         print(western.scale(seq))

         m2 = western.shorthand_interval('m', 2)
         M2 = western.shorthand_interval('M', 2)

         iseq = western.interval_seq([m2, m2, M2, m2, M2, m2, m2])
         print(western.note('D#', 3).scale(iseq))

         P1 = western.unison_interval
         m3 = western.shorthand_interval('m', 3)
         P5 = western.shorthand_interval('P', 5)

         ifan = western.interval_seq([P1, m3, P5])
         print(western.note('D#', 3).scale(ifan))

      .. testoutput:: WesternNotation

         WesternNoteScale([C4, D4, E4, F4, G4])
         WesternNoteScale([D#3, E3, F3, G3, Ab3, Bb3, Cb4, Dbb4])
         WesternNoteScale([D#3, F#3, C#4])

   .. tab:: UpDown

      .. testcode:: UpDownNotation

         from xenharmlib import EDOTuning
         from xenharmlib import UpDownNotation

         edo31 = EDOTuning(31)
         n_edo31 = UpDownNotation(edo31)

         seq = n_edo31.seq([n_edo31.note(pcs, 4) for pcs in 'CEGDEFE'])
         print(n_edo31.scale(seq))

         up_m2 = n_edo31.shorthand_interval('^m', 2)
         down_M2 = n_edo31.shorthand_interval('vM', 2)

         iseq = n_edo31.interval_seq(
             [up_m2, up_m2, down_M2, up_m2, down_M2, up_m2, down_M2]
         )
         print(n_edo31.note('D#', 3).scale(iseq))

         P1 = n_edo31.unison_interval
         m3 = n_edo31.shorthand_interval('m', 3)
         P5 = n_edo31.shorthand_interval('P', 5)

         ifan = n_edo31.interval_seq([P1, m3, P5])
         print(n_edo31.note('D#', 3).scale(ifan))

      .. testoutput:: UpDownNotation

         UpDownNoteScale([C4, D4, E4, F4, G4], 31-EDO)
         UpDownNoteScale([D#3, ^E3, ^^F3, ^G3, ^^Ab3, ^Bb3, ^^Cb4, ^Db4], 31-EDO)
         UpDownNoteScale([D#3, F#3, C#4], 31-EDO)

Identity and Equivalency
-------------------------------------------------------

Two scales are considered identical if each element in one scale has a
matching element in the other scale with exactly the same frequency.
This relation works across origin contexts, for example 12-EDO and
24-EDO scales, or Western Note Scales can be identical:

.. testcode::

   from xenharmlib import EDOTuning
   from xenharmlib import UpDownNotation
   from xenharmlib import WesternNotation

   edo24 = EDOTuning(24)
   n_edo24 = UpDownNotation(edo24)
   western = WesternNotation()

   Cm_1 = edo24.index_scale([0, 8, 14])
   Cm_2 = n_edo24.pc_scale('CEG')
   Cm_3 = western.pc_scale('CEG')

   print(Cm_1 == Cm_2 == Cm_3)

.. testoutput::

   True

Keep in mind that even if two scales might have the same symbolic string
representation in a notation, they are not necessarily equal. A G4 in 31-EDO
has for example a different Frequency than a G4 in 12-EDO:

.. testcode::

   from xenharmlib import EDOTuning
   from xenharmlib import UpDownNotation

   edo31 = EDOTuning(31)
   n_edo31 = UpDownNotation(edo31)

   edo12 = EDOTuning(12)
   n_edo12 = UpDownNotation(edo12)

   Cm_1 = n_edo31.pc_scale('CEG', 4)
   Cm_2 = n_edo12.pc_scale('CEG', 4)

   print(Cm_1)
   print(Cm_2)

   print(Cm_1 == Cm_2)

.. testoutput::

   UpDownNoteScale([C4, E4, G4], 31-EDO)
   UpDownNoteScale([C4, E4, G4], 12-EDO)
   False

As long as two origin contexts have the same equivalency interval scales
can also be compared on the criterion of equivalency instead of equality.
Scales provide two definitions of equivalency: **Set equivalency** which
implies that each scale element has an equivalent element in the other
scale (and vice versa) and the (stronger) **sequential equivalency**
which also demands that equivalent elements are *at the same position*
in the scale. To get an intuition for the difference consider the
following example:

.. tabs::

   .. tab:: EDO

      .. testcode:: EDOTuning

         from xenharmlib import EDOTuning
         edo31 = EDOTuning(31)

         scale_a = edo31.index_scale([0, 10, 49])
         scale_b = edo31.index_scale([18, 31, 41])
         scale_c = edo31.index_scale([31, 41, 49])

         print(scale_a.is_set_equivalent(scale_b))
         print(scale_a.is_seq_equivalent(scale_b))
         print(scale_a.is_seq_equivalent(scale_c))

      .. testoutput:: EDOTuning

         True
         False
         True

   .. tab:: Prime Limit

      .. testcode:: PrimeLimitTuning

         from xenharmlib import PrimeLimitTuning
         limit5 = PrimeLimitTuning(5)

         scale_a = limit5.rs_scale(['3/2', '2/1', '5/2'])
         scale_b = limit5.rs_scale(['5/4', '3/2', '2/1'])
         scale_c = limit5.rs_scale(['3/1', '4/1', '5/1'])

         print(scale_a.is_set_equivalent(scale_b))
         print(scale_a.is_seq_equivalent(scale_b))
         print(scale_a.is_seq_equivalent(scale_c))

      .. testoutput:: PrimeLimitTuning

         True
         False
         True

   .. tab:: Western

      .. testcode:: WesternNotation

         from xenharmlib import WesternNotation
         western = WesternNotation()

         E4 = western.note('E', 4)
         G4 = western.note('G', 4)
         C5 = western.note('C', 5)
         E5 = western.note('E', 5)
         G5 = western.note('G', 5)

         scale_a = western.scale([G4, C5, E5])
         scale_b = western.scale([E4, C5, G5])
         scale_c = western.scale([G4, C5, E5])

         print(scale_a.is_set_equivalent(scale_b))
         print(scale_a.is_seq_equivalent(scale_b))
         print(scale_a.is_seq_equivalent(scale_c))

      .. testoutput:: WesternNotation

         True
         False
         True

   .. tab:: UpDown

      .. testcode:: UpDownNotation

         from xenharmlib import EDOTuning
         from xenharmlib import UpDownNotation

         edo31 = EDOTuning(31)
         n_edo31 = UpDownNotation(edo31)

         E4 = n_edo31.note('E', 4)
         Gup4 = n_edo31.note('^G', 4)
         C5 = n_edo31.note('C', 5)
         E5 = n_edo31.note('E', 5)
         Gup5 = n_edo31.note('^G', 5)

         scale_a = n_edo31.scale([Gup4, C5, E5])
         scale_b = n_edo31.scale([E4, C5, Gup5])
         scale_c = n_edo31.scale([Gup4, C5, E5])

         print(scale_a.is_set_equivalent(scale_b))
         print(scale_a.is_seq_equivalent(scale_b))
         print(scale_a.is_seq_equivalent(scale_c))

      .. testoutput:: UpDownNotation

         True
         False
         True

Transposition
-------------------------------------------------------

Scales can be transposed with the
:meth:`~xenharmlib.core.scale.Scale.transpose`
method. This is typically done by providing an
:doc:`interval object <prim_interval>` of the same origin context:

.. tabs::

   .. tab:: EDO

      .. testcode:: EDOTuning

         from xenharmlib import EDOTuning
         edo31 = EDOTuning(31)

         scale = edo31.index_scale([3, 10, 19])
         interval = edo31.diff_interval(8)
         print(scale.transpose(interval))

      .. testoutput:: EDOTuning

         EDOPitchScale([11, 18, 27], 31-EDO)

   .. tab:: Prime Limit

      .. testcode:: PrimeLimitTuning

         from xenharmlib import PrimeLimitTuning
         limit5 = PrimeLimitTuning(5)

         scale = limit5.rs_scale(['1/1', '5/4', '3/2'])
         interval = limit5.rs_interval('9/8')
         print(scale.transpose(interval))

      .. testoutput:: PrimeLimitTuning

         PrimeLimitPitchScale([9/8, 45/32, 27/16], 5-Limit)

   .. tab:: Western

      .. testcode:: WesternNotation

         from xenharmlib import WesternNotation
         western = WesternNotation()

         scale = western.scale([western.note(pcs, 4) for pcs in 'CDEFGAB'])
         interval = western.shorthand_interval('A', 3)
         print(scale.transpose(interval))

      .. testoutput:: WesternNotation

         WesternNoteScale([E#4, Fx4, Gx4, A#4, B#4, Cx5, Dx5])

   .. tab:: UpDown

      .. testcode:: UpDownNotation

         from xenharmlib import EDOTuning
         from xenharmlib import UpDownNotation

         edo31 = EDOTuning(31)
         n_edo31 = UpDownNotation(edo31)

         Gb4 = n_edo31.note('Gb', 4)
         Aup4 = n_edo31.note('^A', 4)
         Bb4 = n_edo31.note('Bb', 4)

         scale = n_edo31.scale([Gb4, Aup4, Bb4])
         interval = n_edo31.shorthand_interval('^m', 2)
         print(scale.transpose(interval))

      .. testoutput:: UpDownNotation

         UpDownNoteScale([^Abb4, ^^Bb4, ^Cb5], 31-EDO)

The :meth:`~xenharmlib.core.scale.Scale.transpose` method also 
accepts a **pitch difference**. A pitch difference is an integer or
lattice point that defines the numeric distance between two frequency
representations. In the case of notations with enharmonic ambiguity
xenharmlib makes a guess which note should be picked.

.. tabs::

   .. tab:: EDO

      .. testcode:: EDOTuning

         from xenharmlib import EDOTuning
         edo31 = EDOTuning(31)

         scale = edo31.index_scale([3, 10, 19])
         print(scale.transpose(8))

      .. testoutput:: EDOTuning

         EDOPitchScale([11, 18, 27], 31-EDO)

   .. tab:: Prime Limit

      .. testcode:: PrimeLimitTuning

         from xenharmlib import PrimeLimitTuning
         limit5 = PrimeLimitTuning(5)

         scale = limit5.rs_scale(['1/1', '5/4', '3/2'])
         pitch_diff = limit5.lattice.point((-1, 0, 1))
         print(scale.transpose(pitch_diff))

      .. testoutput:: PrimeLimitTuning

         PrimeLimitPitchScale([5/2, 25/8, 15/4], 5-Limit)

   .. tab:: Western

      .. testcode:: WesternNotation

         from xenharmlib import WesternNotation
         western = WesternNotation()

         scale = western.scale([western.note(pcs, 4) for pcs in 'CDEFGAB'])
         print(scale.transpose(2))

      .. testoutput:: WesternNotation

         WesternNoteScale([D4, E4, F#4, G4, A4, B4, C#5])

   .. tab:: UpDown

      .. testcode:: UpDownNotation

         from xenharmlib import EDOTuning
         from xenharmlib import UpDownNotation

         edo31 = EDOTuning(31)
         n_edo31 = UpDownNotation(edo31)

         Gb4 = n_edo31.note('Gb', 4)
         Aup4 = n_edo31.note('^A', 4)
         Bb4 = n_edo31.note('Bb', 4)

         scale = n_edo31.scale([Gb4, Aup4, Bb4])
         print(scale.transpose(18))

      .. testoutput:: UpDownNotation

         UpDownNoteScale([Db5, Fb5, F5], 31-EDO)


Rotation
-------------------------------------------------------

Scale objects can be rotated upwards and downwards. On upwards rotation
the first element is transposed upwards by the equivalency interval until
it is bigger than the last element. On downwards rotation the last element
is transposed downwards by the equivalency interval until is smaller than
the first element.

Rotation is also sometimes called the *mode* of a scale (for example the
"Dorian Mode" is the first upwards rotation of the C major scale). In
the context of chords rotation is called *inversion*.

Rotation is done using the rotation method of scales, which takes an
integer parameter: A positive integer :math:`k` will rotate the scale
*upwards* :math:`k` times, a negative integer :math:`-k` will rotate the
scale *downwards* :math:`k` times.

.. tabs::

   .. tab:: EDO

      .. testcode:: EDOTuning

         from xenharmlib import EDOTuning
         edo31 = EDOTuning(31)

         scale = edo31.index_scale([3, 10, 18, 24, 29])
         print(scale.rotation(3))

      .. testoutput:: EDOTuning

         EDOPitchScale([24, 29, 34, 41, 49], 31-EDO)

   .. tab:: Prime Limit

      .. testcode:: PrimeLimitTuning

         from xenharmlib import PrimeLimitTuning
         limit5 = PrimeLimitTuning(5)

         scale = limit5.rs_scale(['1/1', '5/4', '3/2'])
         print(scale.rotation(-1))

      .. testoutput:: PrimeLimitTuning

         PrimeLimitPitchScale([3/4, 1, 5/4], 5-Limit)

   .. tab:: Western

      .. testcode:: WesternNotation

         from xenharmlib import WesternNotation
         western = WesternNotation()

         scale = western.scale([western.note(pcs, 4) for pcs in 'CEGB'])
         print(scale.rotation(2))

      .. testoutput:: WesternNotation

         WesternNoteScale([G4, B4, C5, E5])

   .. tab:: UpDown

      .. testcode:: UpDownNotation

         from xenharmlib import EDOTuning
         from xenharmlib import UpDownNotation

         edo31 = EDOTuning(31)
         n_edo31 = UpDownNotation(edo31)

         Gb4 = n_edo31.note('Gb', 4)
         Aup4 = n_edo31.note('^A', 4)
         Bb4 = n_edo31.note('Bb', 4)

         scale = n_edo31.scale([Gb4, Aup4, Bb4])
         print(scale.rotation(-1))

      .. testoutput:: UpDownNotation

         UpDownNoteScale([Bb3, Gb4, ^A4], 31-EDO)


Sequential Properties
-------------------------------------------------------

Scales implement the typical properties of python's lists und tuples.
Containment can be tested with the :code:`in` operator, item and
slice retrieval can be achieved with the :code:`[]` operator.
Also, of course, iteration is supported:

.. tabs::

   .. tab:: EDO

      .. testcode:: EDOTuning

         from xenharmlib import EDOTuning
         edo31 = EDOTuning(31)

         scale = edo31.index_scale([3, 10, 18, 24, 29])

         print(edo31.pitch(10) in scale)
         print(scale[2])
         print(scale[1:4])

         for pitch in scale:
             print('-->', pitch)

      .. testoutput:: EDOTuning

         True
         EDOPitch(18, 31-EDO)
         EDOPitchScale([10, 18, 24], 31-EDO)
         --> EDOPitch(3, 31-EDO)
         --> EDOPitch(10, 31-EDO)
         --> EDOPitch(18, 31-EDO)
         --> EDOPitch(24, 31-EDO)
         --> EDOPitch(29, 31-EDO)

   .. tab:: Prime Limit

      .. testcode:: PrimeLimitTuning

         from xenharmlib import PrimeLimitTuning
         limit5 = PrimeLimitTuning(5)

         scale = limit5.rs_scale(['1/1', '5/4', '3/2', '25/16'])

         print(limit5.rs_pitch('5/4') in scale)
         print(scale[2])
         print(scale[1:4])

         for pitch in scale:
             print('-->', pitch)

      .. testoutput:: PrimeLimitTuning

         True
         PrimeLimitPitch(3/2, 5-Limit)
         PrimeLimitPitchScale([5/4, 3/2, 25/16], 5-Limit)
         --> PrimeLimitPitch(1, 5-Limit)
         --> PrimeLimitPitch(5/4, 5-Limit)
         --> PrimeLimitPitch(3/2, 5-Limit)
         --> PrimeLimitPitch(25/16, 5-Limit)

   .. tab:: Western

      .. testcode:: WesternNotation

         from xenharmlib import WesternNotation
         western = WesternNotation()

         scale = western.scale([western.note(pcs, 4) for pcs in 'CEGB'])

         print(western.note('E', 4) in scale)
         print(scale[2])
         print(scale[1:])

         for note in scale:
             print('-->', note)

      .. testoutput:: WesternNotation

         True
         WesternNote(G, 4)
         WesternNoteScale([E4, G4, B4])
         --> WesternNote(C, 4)
         --> WesternNote(E, 4)
         --> WesternNote(G, 4)
         --> WesternNote(B, 4)

   .. tab:: UpDown

      .. testcode:: UpDownNotation

         from xenharmlib import EDOTuning
         from xenharmlib import UpDownNotation

         edo31 = EDOTuning(31)
         n_edo31 = UpDownNotation(edo31)

         Gb4 = n_edo31.note('Gb', 4)
         Aup4 = n_edo31.note('^A', 4)
         Bb4 = n_edo31.note('Bb', 4)

         scale = n_edo31.scale([Gb4, Aup4, Bb4])

         print(n_edo31.note('^A', 4) in scale)
         print(scale[1])
         print(scale[:2])

         for note in scale:
             print('-->', note)

      .. testoutput:: UpDownNotation

         True
         UpDownNote(^A, 4, 31-EDO)
         UpDownNoteScale([Gb4, ^A4], 31-EDO)
         --> UpDownNote(Gb, 4, 31-EDO)
         --> UpDownNote(^A, 4, 31-EDO)
         --> UpDownNote(Bb, 4, 31-EDO)

.. _index_masks_and_partial_scales:

Index Masks and Partial Scales
--------------------------------------

When examining a scale you are often interested in focusing only on fragments
of it. In many cases the :code:`[]`-operator is sufficient to extract the
desired partial scale from the original, e.g. if you want the major septimal
chord scale from a major scale:

.. tabs::

   .. tab:: EDO

      .. testcode:: EDOTuning

         from xenharmlib import EDOTuning

         edo31 = EDOTuning(31)

         # stack 7 fifths. since 0 is C, start with -18 (F)
         c_maj_scale = edo31.index_scale(
             k * 18 for k in range(-1, 6)
         ).pcs_normalized()

         c7chord = c_maj_scale[::2]
         print(c7chord)

      .. testoutput:: EDOTuning

         EDOPitchScale([0, 10, 18, 28], 31-EDO)

   .. tab:: Prime Limit

      .. testcode:: PrimeLimitTuning

         from xenharmlib import PrimeLimitTuning
         from xenharmlib import FrequencyRatio

         limit3 = PrimeLimitTuning(3)

         # stack 7 pure fifths. since 1/1 is C start with 2/3 (F)
         c_maj_scale = limit3.ratio_scale(
             (FrequencyRatio(3, 2) ** k) for k in range(-1, 6)
         ).pcs_normalized()

         c7chord = c_maj_scale[::2]
         print(c7chord)

      .. testoutput:: PrimeLimitTuning

         PrimeLimitPitchScale([1, 81/64, 3/2, 243/128], 3-Limit)

   .. tab:: Western

      .. testcode:: WesternNotation

         from xenharmlib import WesternNotation
         
         western = WesternNotation()
         c_maj_scale = western.pc_scale('CDEFGAB')

         c7chord = c_maj_scale[::2]
         print(c7chord)

      .. testoutput:: WesternNotation

         WesternNoteScale([C0, E0, G0, B0])

   .. tab:: UpDown

      .. testcode:: UpDownNotation

         from xenharmlib import EDOTuning
         from xenharmlib import UpDownNotation
         
         edo12 = EDOTuning(12)
         n_edo12 = UpDownNotation(edo12)
         c_maj_scale = n_edo12.pc_scale('CDEFGAB')

         c7chord = c_maj_scale[::2]
         print(c7chord)

      .. testoutput:: UpDownNotation

         UpDownNoteScale([C0, E0, G0, B0], 12-EDO)

In other cases the :code:`[]`-operator will not take you far. What if instead
of the major septimal chord scale you want to generate the sus4 chord scale?
The appropriate indices :code:`(0, 3, 4)` don't have a uniform distance, so
they can not be represented by a single slice expression. For reason of this
limitation xenharmlib implements a generalization of a slice called index
mask and the scale method :meth:`~xenharmlib.core.scale.Scale.partial` that
expects an index mask as its parameter:

.. tabs::

   .. tab:: EDO

      .. testcode:: EDOTuning

         from xenharmlib import EDOTuning

         edo31 = EDOTuning(31)

         # stack 7 fifths. since 0 is C, start with -18 (F)
         c_maj_scale = edo31.index_scale(
             k * 18 for k in range(-1, 6)
         ).pcs_normalized()

         c_sus4_chord = c_maj_scale.partial((0, 3, 4))
         print(c_sus4_chord)

      .. testoutput:: EDOTuning

         EDOPitchScale([0, 13, 18], 31-EDO)

   .. tab:: Prime Limit

      .. testcode:: PrimeLimitTuning

         from xenharmlib import PrimeLimitTuning
         from xenharmlib import FrequencyRatio

         limit3 = PrimeLimitTuning(3)

         # stack 7 pure fifths. since 1/1 is C start with 2/3 (F)
         c_maj_scale = limit3.ratio_scale(
             (FrequencyRatio(3, 2) ** k) for k in range(-1, 6)
         ).pcs_normalized()

         c_sus4_chord = c_maj_scale.partial((0, 3, 4))
         print(c_sus4_chord)

      .. testoutput:: PrimeLimitTuning

         PrimeLimitPitchScale([1, 4/3, 3/2], 3-Limit)

   .. tab:: Western

      .. testcode:: WesternNotation

         from xenharmlib import WesternNotation
         
         western = WesternNotation()
         c_maj_scale = western.pc_scale('CDEFGAB')

         c_sus4_chord = c_maj_scale.partial((0, 3, 4))
         print(c_sus4_chord)

      .. testoutput:: WesternNotation

         WesternNoteScale([C0, F0, G0])

   .. tab:: UpDown

      .. testcode:: UpDownNotation

         from xenharmlib import EDOTuning
         from xenharmlib import UpDownNotation
         
         edo12 = EDOTuning(12)
         n_edo12 = UpDownNotation(edo12)
         c_maj_scale = n_edo12.pc_scale('CDEFGAB')

         c_sus4_chord = c_maj_scale.partial((0, 3, 4))
         print(c_sus4_chord)

      .. testoutput:: UpDownNotation

         UpDownNoteScale([C0, F0, G0], 12-EDO)

An index mask can be defined in multiple ways. In the above snippet, it is
simply expressed as a tuple of consecutive integers. For big connected
*blocks* of integers this can be tedious, so xenharmlib offers a short
variant with Python's ellipsis symbol (:code:`...`). An ellipsis indicates
that all indices between two values should be part of the mask as well:

.. tabs::

   .. tab:: EDO

      .. testcode:: EDOTuning

         from xenharmlib import EDOTuning

         edo31 = EDOTuning(31)

         # stack 7 fifths. since 0 is C, start with -18 (F)
         c_maj_scale = edo31.index_scale(
             k * 18 for k in range(-1, 6)
         ).pcs_normalized()

         partial = c_maj_scale.partial((1, ..., 4, 6))
         print(partial)

      .. testoutput:: EDOTuning

         EDOPitchScale([5, 10, 13, 18, 28], 31-EDO)

   .. tab:: Prime Limit

      .. testcode:: PrimeLimitTuning

         from xenharmlib import PrimeLimitTuning
         from xenharmlib import FrequencyRatio

         limit3 = PrimeLimitTuning(3)

         # stack 7 pure fifths. since 1/1 is C start with 2/3 (F)
         c_maj_scale = limit3.ratio_scale(
             (FrequencyRatio(3, 2) ** k) for k in range(-1, 6)
         ).pcs_normalized()

         partial = c_maj_scale.partial((1, ..., 4, 6))
         print(partial)

      .. testoutput:: PrimeLimitTuning

         PrimeLimitPitchScale([9/8, 81/64, 4/3, 3/2, 243/128], 3-Limit)

   .. tab:: Western

      .. testcode:: WesternNotation

         from xenharmlib import WesternNotation
         
         western = WesternNotation()
         c_maj_scale = western.pc_scale('CDEFGAB')

         partial = c_maj_scale.partial((1, ..., 4, 6))
         print(partial)

      .. testoutput:: WesternNotation

         WesternNoteScale([D0, E0, F0, G0, B0])

   .. tab:: UpDown

      .. testcode:: UpDownNotation

         from xenharmlib import EDOTuning
         from xenharmlib import UpDownNotation
         
         edo12 = EDOTuning(12)
         n_edo12 = UpDownNotation(edo12)
         c_maj_scale = n_edo12.pc_scale('CDEFGAB')

         partial = c_maj_scale.partial((1, ..., 4, 6))
         print(partial)

      .. testoutput:: UpDownNotation

         UpDownNoteScale([D0, E0, F0, G0, B0], 12-EDO)

Similar to Python's slices the first value and the last value of mask
definitions can be omitted entailing the familiar behavior: If a mask
begins with an ellipsis the first value is implicitly 0. If a mask
ends with an ellipsis the last value is the last index of the scale
the mask is applied to:

.. tabs::

   .. tab:: EDO

      .. testcode:: EDOTuning

         from xenharmlib import EDOTuning

         edo31 = EDOTuning(31)

         # stack 7 fifths. since 0 is C, start with -18 (F)
         c_maj_scale = edo31.index_scale(
             k * 18 for k in range(-1, 6)
         ).pcs_normalized()

         partial1 = c_maj_scale.partial((..., 3, 6))
         partial2 = c_maj_scale.partial((3, ...))
      
         print(partial1)
         print(partial2)

      .. testoutput:: EDOTuning

         EDOPitchScale([0, 5, 10, 13, 28], 31-EDO)
         EDOPitchScale([13, 18, 23, 28], 31-EDO)

   .. tab:: Prime Limit

      .. testcode:: PrimeLimitTuning

         from xenharmlib import PrimeLimitTuning
         from xenharmlib import FrequencyRatio

         limit3 = PrimeLimitTuning(3)

         # stack 7 pure fifths. since 1/1 is C start with 2/3 (F)
         c_maj_scale = limit3.ratio_scale(
             (FrequencyRatio(3, 2) ** k) for k in range(-1, 6)
         ).pcs_normalized()

         partial1 = c_maj_scale.partial((..., 3, 6))
         partial2 = c_maj_scale.partial((3, ...))
      
         print(partial1)
         print(partial2)

      .. testoutput:: PrimeLimitTuning

         PrimeLimitPitchScale([1, 9/8, 81/64, 4/3, 243/128], 3-Limit)
         PrimeLimitPitchScale([4/3, 3/2, 27/16, 243/128], 3-Limit)

   .. tab:: Western

      .. testcode:: WesternNotation

         from xenharmlib import WesternNotation
         
         western = WesternNotation()
         c_maj_scale = western.pc_scale('CDEFGAB')

         partial1 = c_maj_scale.partial((..., 3, 6))
         partial2 = c_maj_scale.partial((3, ...))
      
         print(partial1)
         print(partial2)

      .. testoutput:: WesternNotation

         WesternNoteScale([C0, D0, E0, F0, B0])
         WesternNoteScale([F0, G0, A0, B0])

   .. tab:: UpDown

      .. testcode:: UpDownNotation

         from xenharmlib import EDOTuning
         from xenharmlib import UpDownNotation
         
         edo12 = EDOTuning(12)
         n_edo12 = UpDownNotation(edo12)
         c_maj_scale = n_edo12.pc_scale('CDEFGAB')

         partial1 = c_maj_scale.partial((..., 3, 6))
         partial2 = c_maj_scale.partial((3, ...))
      
         print(partial1)
         print(partial2)

      .. testoutput:: UpDownNotation

         UpDownNoteScale([C0, D0, E0, F0, B0], 12-EDO)
         UpDownNoteScale([F0, G0, A0, B0], 12-EDO)

Please note that, in contrast to slices, the index after an ellipsis is
**included** in the mask:

.. tabs::

   .. tab:: EDO

      .. testcode:: EDOTuning

         from xenharmlib import EDOTuning

         edo31 = EDOTuning(31)

         # stack 7 fifths. since 0 is C, start with -18 (F)
         c_maj_scale = edo31.index_scale(
             k * 18 for k in range(-1, 6)
         ).pcs_normalized()

         partial_scale = c_maj_scale.partial((1, ..., 3))
         scale_slice = c_maj_scale[1:3]
      
         print(partial_scale)
         print(scale_slice)

      .. testoutput:: EDOTuning

         EDOPitchScale([5, 10, 13], 31-EDO)
         EDOPitchScale([5, 10], 31-EDO)

   .. tab:: Prime Limit

      .. testcode:: PrimeLimitTuning

         from xenharmlib import PrimeLimitTuning
         from xenharmlib import FrequencyRatio

         limit3 = PrimeLimitTuning(3)

         # stack 7 pure fifths. since 1/1 is C start with 2/3 (F)
         c_maj_scale = limit3.ratio_scale(
             (FrequencyRatio(3, 2) ** k) for k in range(-1, 6)
         ).pcs_normalized()

         partial_scale = c_maj_scale.partial((1, ..., 3))
         scale_slice = c_maj_scale[1:3]
      
         print(partial_scale)
         print(scale_slice)

      .. testoutput:: PrimeLimitTuning

         PrimeLimitPitchScale([9/8, 81/64, 4/3], 3-Limit)
         PrimeLimitPitchScale([9/8, 81/64], 3-Limit)

   .. tab:: Western

      .. testcode:: WesternNotation

         from xenharmlib import WesternNotation
         
         western = WesternNotation()
         c_maj_scale = western.pc_scale('CDEFGAB')

         partial_scale = c_maj_scale.partial((1, ..., 3))
         scale_slice = c_maj_scale[1:3]
      
         print(partial_scale)
         print(scale_slice)

      .. testoutput:: WesternNotation

         WesternNoteScale([D0, E0, F0])
         WesternNoteScale([D0, E0])

   .. tab:: UpDown

      .. testcode:: UpDownNotation

         from xenharmlib import EDOTuning
         from xenharmlib import UpDownNotation
         
         edo12 = EDOTuning(12)
         n_edo12 = UpDownNotation(edo12)
         c_maj_scale = n_edo12.pc_scale('CDEFGAB')

         partial_scale = c_maj_scale.partial((1, ..., 3))
         scale_slice = c_maj_scale[1:3]
      
         print(partial_scale)
         print(scale_slice)

      .. testoutput:: UpDownNotation

         UpDownNoteScale([D0, E0, F0], 12-EDO)
         UpDownNoteScale([D0, E0], 12-EDO)

For convenience reasons, one-element mask expressions can also be given
without being wrapped by the tuple constructor:

.. tabs::

   .. tab:: EDO

      .. testcode:: EDOTuning

         from xenharmlib import EDOTuning

         edo31 = EDOTuning(31)

         # stack 7 fifths. since 0 is C, start with -18 (F)
         c_maj_scale = edo31.index_scale(
             k * 18 for k in range(-1, 6)
         ).pcs_normalized()

         partial_scale = c_maj_scale.partial((1, ..., 3))
         scale_slice = c_maj_scale[1:3]
      
         partial = c_maj_scale.partial(1)
         print(partial)

      .. testoutput:: EDOTuning

         EDOPitchScale([5], 31-EDO)

   .. tab:: Prime Limit

      .. testcode:: PrimeLimitTuning

         from xenharmlib import PrimeLimitTuning
         from xenharmlib import FrequencyRatio

         limit3 = PrimeLimitTuning(3)

         # stack 7 pure fifths. since 1/1 is C start with 2/3 (F)
         c_maj_scale = limit3.ratio_scale(
             (FrequencyRatio(3, 2) ** k) for k in range(-1, 6)
         ).pcs_normalized()

         partial = c_maj_scale.partial(1)
         print(partial)

      .. testoutput:: PrimeLimitTuning

         PrimeLimitPitchScale([9/8], 3-Limit)

   .. tab:: Western

      .. testcode:: WesternNotation

         from xenharmlib import WesternNotation
         
         western = WesternNotation()
         c_maj_scale = western.pc_scale('CDEFGAB')

         partial = c_maj_scale.partial(1)
         print(partial)

      .. testoutput:: WesternNotation

         WesternNoteScale([D0])

   .. tab:: UpDown

      .. testcode:: UpDownNotation

         from xenharmlib import EDOTuning
         from xenharmlib import UpDownNotation
         
         edo12 = EDOTuning(12)
         n_edo12 = UpDownNotation(edo12)
         c_maj_scale = n_edo12.pc_scale('CDEFGAB')

         partial = c_maj_scale.partial(1)
         print(partial)

      .. testoutput:: UpDownNotation

         UpDownNoteScale([D0], 12-EDO)

If you want to receive the *complement* of a mask you can resort to the
:meth:`~xenharmlib.core.scale.Scale.partial_not` method:

.. tabs::

   .. tab:: EDO

      .. testcode:: EDOTuning

         from xenharmlib import EDOTuning

         edo31 = EDOTuning(31)

         # stack 7 fifths. since 0 is C, start with -18 (F)
         c_maj_scale = edo31.index_scale(
             k * 18 for k in range(-1, 6)
         ).pcs_normalized()

         scale = c_maj_scale.partial_not((0, 1, 2, 6, ...))
         print(scale)

      .. testoutput:: EDOTuning

         EDOPitchScale([13, 18, 23], 31-EDO)

   .. tab:: Prime Limit

      .. testcode:: PrimeLimitTuning

         from xenharmlib import PrimeLimitTuning
         from xenharmlib import FrequencyRatio

         limit3 = PrimeLimitTuning(3)

         # stack 7 pure fifths. since 1/1 is C start with 2/3 (F)
         c_maj_scale = limit3.ratio_scale(
             (FrequencyRatio(3, 2) ** k) for k in range(-1, 6)
         ).pcs_normalized()

         scale = c_maj_scale.partial_not((0, 1, 2, 6, ...))
         print(scale)

      .. testoutput:: PrimeLimitTuning

         PrimeLimitPitchScale([4/3, 3/2, 27/16], 3-Limit)

   .. tab:: Western

      .. testcode:: WesternNotation

         from xenharmlib import WesternNotation
         
         western = WesternNotation()
         c_maj_scale = western.pc_scale('CDEFGAB')

         scale = c_maj_scale.partial_not((0, 1, 2, 6, ...))
         print(scale)

      .. testoutput:: WesternNotation

         WesternNoteScale([F0, G0, A0])

   .. tab:: UpDown

      .. testcode:: UpDownNotation

         from xenharmlib import EDOTuning
         from xenharmlib import UpDownNotation
         
         edo12 = EDOTuning(12)
         n_edo12 = UpDownNotation(edo12)
         c_maj_scale = n_edo12.pc_scale('CDEFGAB')

         scale = c_maj_scale.partial_not((0, 1, 2, 6, ...))
         print(scale)

      .. testoutput:: UpDownNotation

         UpDownNoteScale([F0, G0, A0], 12-EDO)

If you want to receive *both* use the
:meth:`~xenharmlib.core.scale.Scale.partition` method:

.. tabs::

   .. tab:: EDO

      .. testcode:: EDOTuning

         from xenharmlib import EDOTuning

         edo31 = EDOTuning(31)

         # stack 7 fifths. since 0 is C, start with -18 (F)
         c_maj_scale = edo31.index_scale(
             k * 18 for k in range(-1, 6)
         ).pcs_normalized()

         c_sus4, leftover = c_maj_scale.partition((0, 3, 4))
  
         print(c_sus4)
         print(leftover)

      .. testoutput:: EDOTuning

         EDOPitchScale([0, 13, 18], 31-EDO)
         EDOPitchScale([5, 10, 23, 28], 31-EDO)

   .. tab:: Prime Limit

      .. testcode:: PrimeLimitTuning

         from xenharmlib import PrimeLimitTuning
         from xenharmlib import FrequencyRatio

         limit3 = PrimeLimitTuning(3)

         # stack 7 pure fifths. since 1/1 is C start with 2/3 (F)
         c_maj_scale = limit3.ratio_scale(
             (FrequencyRatio(3, 2) ** k) for k in range(-1, 6)
         ).pcs_normalized()

         c_sus4, leftover = c_maj_scale.partition((0, 3, 4))
  
         print(c_sus4)
         print(leftover)

      .. testoutput:: PrimeLimitTuning

         PrimeLimitPitchScale([1, 4/3, 3/2], 3-Limit)
         PrimeLimitPitchScale([9/8, 81/64, 27/16, 243/128], 3-Limit)

   .. tab:: Western

      .. testcode:: WesternNotation

         from xenharmlib import WesternNotation
         
         western = WesternNotation()
         c_maj_scale = western.pc_scale('CDEFGAB')

         c_sus4, leftover = c_maj_scale.partition((0, 3, 4))
  
         print(c_sus4)
         print(leftover)

      .. testoutput:: WesternNotation

         WesternNoteScale([C0, F0, G0])
         WesternNoteScale([D0, E0, A0, B0])

   .. tab:: UpDown

      .. testcode:: UpDownNotation

         from xenharmlib import EDOTuning
         from xenharmlib import UpDownNotation
         
         edo12 = EDOTuning(12)
         n_edo12 = UpDownNotation(edo12)
         c_maj_scale = n_edo12.pc_scale('CDEFGAB')

         c_sus4, leftover = c_maj_scale.partition((0, 3, 4))
  
         print(c_sus4)
         print(leftover)

      .. testoutput:: UpDownNotation

         UpDownNoteScale([C0, F0, G0], 12-EDO)
         UpDownNoteScale([D0, E0, A0, B0], 12-EDO)

.. _scale_normalizations:

Normalizations
--------------------------------------

Scales can be normalized in various ways. From the quickstart you already
know the :meth:`~xenharmlib.core.scale.PeriodicScale.pcs_normalized` method
which transposes all elements of the scale to the first base interval.
However, there are other methods of normalization that can be useful depending
on what you want to do.

One downside of pitch class set normalization is that the scale does not
necessarily retain its original root note. Often you want to reduce a scale
to one base interval, but keep the root note. For this xenharmlib offers the
:meth:`~xenharmlib.core.scale.PeriodicScale.period_normalized`
method:

.. tabs::

   .. tab:: EDO

      .. testcode:: EDOTuning

         from xenharmlib import EDOTuning

         edo31 = EDOTuning(31)
         scale = edo31.index_scale([2, 8, 10, 19, 24, 29, 31, 35])
         print(scale)

         pn_scale = scale.period_normalized()
         print(pn_scale)

      .. testoutput:: EDOTuning

         EDOPitchScale([2, 8, 10, 19, 24, 29, 31, 35], 31-EDO)
         EDOPitchScale([2, 4, 8, 10, 19, 24, 29, 31], 31-EDO)

   .. tab:: Prime Limit

      .. testcode:: PrimeLimitTuning

         from xenharmlib import PrimeLimitTuning
         from xenharmlib import FrequencyRatio

         limit11 = PrimeLimitTuning(11)
         scale = limit11.ratio_scale(
             FrequencyRatio(2*k) for k in range(1, 12)
         )
         print(scale)

         pn_scale = scale.period_normalized()
         print(pn_scale)

      .. testoutput:: PrimeLimitTuning
   
         PrimeLimitPitchScale([2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22], 11-Limit)
         PrimeLimitPitchScale([2, 9/4, 5/2, 11/4, 3, 7/2], 11-Limit)

   .. tab:: Western

      .. testcode:: WesternNotation

         from xenharmlib import WesternNotation

         western = WesternNotation()
         scale = western.pc_scale('CEGBDF', 4)
         print(scale)

         pn_scale = scale.period_normalized()
         print(pn_scale)

      .. testoutput:: WesternNotation

         WesternNoteScale([C4, E4, G4, B4, D5, F5])
         WesternNoteScale([C4, D4, E4, F4, G4, B4])

   .. tab:: UpDown

      .. testcode:: UpDownNotation

         from xenharmlib import EDOTuning
         from xenharmlib import UpDownNotation
         
         edo12 = EDOTuning(12)
         n_edo12 = UpDownNotation(edo12)

         scale = n_edo12.pc_scale(
             ['F', 'G#', 'C', 'F#', 'G']
         )
         print(scale)

         pn_scale = scale.period_normalized()
         print(pn_scale)

      .. testoutput:: UpDownNotation

         UpDownNoteScale([F0, G#0, C1, F#1, G1], 12-EDO)
         UpDownNoteScale([F0, F#0, G0, G#0, C1], 12-EDO)

Sometimes you want to compare the structure of different scales without
considering the root note, for example, you want to know if a scale is
a major scale by comparing it with the definition of the C major scale.
Here the method
:meth:`~xenharmlib.core.scale.Scale.zero_normalized`
can help that will transpose the scale so the root note is the zero element
(C0 in UpDownNotation, the pitch with index 0 on the pitch layer):

.. testcode::

   from xenharmlib import EDOTuning
   from xenharmlib import UpDownNotation
   
   edo12 = EDOTuning(12)
   n_edo12 = UpDownNotation(edo12)
   c_maj_scale = n_edo12.natural_scale()

   scale = n_edo12.pc_scale(
       ['A', 'B', 'C#', 'D', 'E', 'F#', 'G#']
   )

   zn_scale = scale.zero_normalized()
   print(zn_scale)
   print(zn_scale.is_notated_same(c_maj_scale))

.. testoutput::

   UpDownNoteScale([C0, D0, E0, F0, G0, A0, B0], 12-EDO)
   True

Note, that zero normalization does *not* guarantee that the elements of the
resulting scale are contained in one base interval:

.. testcode::

   polychord_Db_G = n_edo12.pc_scale(
       ['G', 'B', 'D', 'F', 'Ab', 'C#']
   )

   zn_scale = polychord_Db_G.zero_normalized()
   print(zn_scale)

.. testoutput::

   UpDownNoteScale([C0, E0, G0, Bb0, Db1, F#1], 12-EDO)

Often in textbooks scales are described in a form where the root note is
C0 and the scale elements all reside in the first base interval. This form
is equivalent to the combined application of zero normalization and
period normalization:

.. testcode::

   norm = polychord_Db_G.period_normalized().zero_normalized()
   print(norm)

.. testoutput::

   UpDownNoteScale([C0, Db0, E0, F#0, G0, Bb0], 12-EDO)

For this type of normalization, there is a convenient shortcut available,
the method :meth:`~xenharmlib.core.scale.PeriodicScale.zp_normalized`
("zero-period normalized"):

.. testcode::

   norm = polychord_Db_G.zp_normalized()
   print(norm)

.. testoutput::

   UpDownNoteScale([C0, Db0, E0, F#0, G0, Bb0], 12-EDO)

Another common normal form is depicting the scale as a series inbetween two
equivalent notes (for example depicting the notes of F major inbetween F4
and F5). This form can be calculated using the method
:meth:`~xenharmlib.core.scale.PeriodicScale.plusone_normalized`:

.. testcode::

   edo12 = EDOTuning(12)
   n_edo12 = UpDownNotation(edo12)

   scale = n_edo12.pc_scale(
       ['F', 'G#', 'C', 'F#', 'G']
   )
   print(scale)

   pn_scale = scale.plusone_normalized()
   print(pn_scale)

.. testoutput::

   UpDownNoteScale([F0, G#0, C1, F#1, G1], 12-EDO)
   UpDownNoteScale([F0, F#0, G0, G#0, C1, F1], 12-EDO)

Reflection
--------------------------------------

Reflection is a generalization of the post-tonal inversion operation on
pitch class sets. A reflection is defined as calculating the interval from
each scale element to a designated axis note/pitch and applying the 
resulting interval on the axis to get the target note/pitch.

Without an argument the :meth:`~xenharmlib.core.scale.Scale.reflection`
method assumes the axis to be the zero element of the origin context.

.. testcode::

   c_hypodorian = n_edo12.pc_scale(
       ['B', 'C', 'D', 'E', 'F', 'G', 'A']
   )
   refl = c_hypodorian.reflection()
   print(refl)

.. testoutput::

   UpDownNoteScale([Eb-2, F-2, G-2, Ab-2, Bb-2, C-1, Db-1], 12-EDO)

Observe how reflection across the zero element is equivalent to applying
the pitch class set inversion operation:

.. testcode::

   print(c_hypodorian.pc_indices)
   print(refl.pc_indices)

.. testoutput::

    [11, 0, 2, 4, 5, 7, 9]
    [3, 5, 7, 8, 10, 0, 1]

A scale can also be reflected using a different axis:

.. testcode::

   c_hypodorian = n_edo12.pc_scale(
       ['B', 'C', 'D', 'E', 'F', 'G', 'A']
   )
   axis = n_edo12.note('B', 0)
   refl = c_hypodorian.reflection(axis)
   print(refl)

.. testoutput::

   UpDownNoteScale([C#0, D#0, E#0, F#0, G#0, A#0, B0], 12-EDO)


Retuning by Closest Correspondence
--------------------------------------

In the beginning we talked about the possibility to constructs scales from
a list of frequencies.
The :meth:`~xenharmlib.core.scale.Scale.retune_closest` provides an extra
level of convenience: With it you can take a scale from one origin context
and transform it into a scale from a different origin context:

.. testcode::

   from xenharmlib import EDOTuning
   from xenharmlib import WesternNotation
   from xenharmlib import UpDownNotation

   edo31 = EDOTuning(31)
   n_edo31 = UpDownNotation(edo31)
   western = WesternNotation()

   scale = n_edo31.pc_scale(['C', 'D#', 'E', 'G'], 4)
   print(scale)

   retuned = scale.retune_closest(western)
   print(retuned)

.. testoutput::

   UpDownNoteScale([C4, D#4, E4, G4], 31-EDO)
   WesternNoteScale([C4, D#4, E4, G4])

Please note, that retuning by closest frequency is not necessarily a one
to one correspondence. If we try to reverse the retuning result, we will
*not* receive the scale we started with:

.. testcode::

   retuned_back = retuned.retune_closest(n_edo31)
   print(retuned_back)
   print(scale == retuned_back)

.. testoutput::

   UpDownNoteScale([C4, Eb4, E4, G4], 31-EDO)
   False

This is because in the Western equal tempered system "D#" and "Eb"
represent the same frequency, however in a 31-EDO system they
are distinct:

.. testcode::

   print(western.note('D#', 4) == western.note('Eb', 4))
   print(n_edo31.note('D#', 4) == n_edo31.note('Eb', 4))

.. testoutput::

   True
   False

Retuning from 31-EDO to a Western system is like lowering the resolution
in an image. Once you have done it the more "fine-grained" data is lost.
Since distinct notes or pitches in one system can "collapse" into one
in a system with less granularity, retuning scales can also have the
effect that the resulting scale is shorter than the original one:

.. testcode::

   scale = n_edo31.pc_scale(['C', 'D#', 'Eb', 'E', 'G'], 4)
   print(scale)

   retuned = scale.retune_closest(western)
   print(retuned)

.. testoutput::

   UpDownNoteScale([C4, D#4, Eb4, E4, G4], 31-EDO)
   WesternNoteScale([C4, D#4, E4, G4])


Set operations
-----------------------------------------

Scales support most of the typical set operations that you are familiar
with from the builtin python sets (with slightly different names):

* :meth:`~xenharmlib.core.scale.PeriodicScale.intersection`
* :meth:`~xenharmlib.core.scale.Scale.union`
* :meth:`~xenharmlib.core.scale.PeriodicScale.difference`
* :meth:`~xenharmlib.core.scale.PeriodicScale.symmetric_difference`
* :meth:`~xenharmlib.core.scale.PeriodicScale.is_subset`
* :meth:`~xenharmlib.core.scale.PeriodicScale.is_superset`
* :meth:`~xenharmlib.core.scale.PeriodicScale.is_disjoint`

Please note that set operations without additional parameters
test for *equality* and not *equivalency*, so if one scale 
includes C0 and the second scale includes C1, they are not
considered as the same element in regards to intersection,
difference or symmetric difference.

Union (:math:`A \cup B`)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The :meth:`~xenharmlib.core.scale.Scale.union` operation (also possible to
use with the infix operator :code:`|`) returns a new scale with all elements
from both scales.

.. tabs::

   .. tab:: EDO

      .. testcode:: EDOTuning

         from xenharmlib import EDOTuning
         edo31 = EDOTuning(31)

         scale_a = edo31.index_scale([3, 10, 18, 24, 29])
         scale_b = edo31.index_scale([4, 10, 18, 24])

         print(scale_a.union(scale_b))
         print(scale_a | scale_b)

      .. testoutput:: EDOTuning

         EDOPitchScale([3, 4, 10, 18, 24, 29], 31-EDO)
         EDOPitchScale([3, 4, 10, 18, 24, 29], 31-EDO)

   .. tab:: Prime Limit

      .. testcode:: PrimeLimitTuning

         from xenharmlib import PrimeLimitTuning
         limit5 = PrimeLimitTuning(5)

         scale_a = limit5.rs_scale(['1/1', '5/4', '3/2', '25/16'])
         scale_b = limit5.rs_scale(['3/2', '25/16', '15/8', '9/4'])

         print(scale_a.union(scale_b))
         print(scale_a | scale_b)

      .. testoutput:: PrimeLimitTuning

         PrimeLimitPitchScale([1, 5/4, 3/2, 25/16, 15/8, 9/4], 5-Limit)
         PrimeLimitPitchScale([1, 5/4, 3/2, 25/16, 15/8, 9/4], 5-Limit)

   .. tab:: Western

      .. testcode:: WesternNotation

         from xenharmlib import WesternNotation
         western = WesternNotation()

         scale_a = western.pc_scale('CDEGB')
         scale_b = western.pc_scale('DEGBCD')

         print(scale_a.union(scale_b))
         print(scale_a | scale_b)

      .. testoutput:: WesternNotation

         WesternNoteScale([C0, D0, E0, G0, B0, C1, D1])
         WesternNoteScale([C0, D0, E0, G0, B0, C1, D1])

   .. tab:: UpDown

      .. testcode:: UpDownNotation

         from xenharmlib import EDOTuning
         from xenharmlib import UpDownNotation

         edo31 = EDOTuning(31)
         n_edo31 = UpDownNotation(edo31)

         C4 = n_edo31.note('C', 4)
         E4 = n_edo31.note('E', 4)
         Gb4 = n_edo31.note('Gb', 4)
         Aup4 = n_edo31.note('^A', 4)
         Bb4 = n_edo31.note('Bb', 4)

         scale_a = n_edo31.scale([E4, Gb4, Aup4, Bb4])
         scale_b = n_edo31.scale([C4, Gb4, Aup4, Bb4])

         print(scale_a.union(scale_b))
         print(scale_a | scale_b)

      .. testoutput:: UpDownNotation

         UpDownNoteScale([C4, E4, Gb4, ^A4, Bb4], 31-EDO)
         UpDownNoteScale([C4, E4, Gb4, ^A4, Bb4], 31-EDO)

Intersection (:math:`A \cap B`)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The :meth:`~xenharmlib.core.scale.Scale.intersection` operation (also
possible to use with the infix operator :code:`&`) returns a new scale
with contatining only elements that exist in both scales.

.. tabs::

   .. tab:: EDO

      .. testcode:: EDOTuning

         from xenharmlib import EDOTuning
         edo31 = EDOTuning(31)

         scale_a = edo31.index_scale([3, 10, 18, 24, 29])
         scale_b = edo31.index_scale([4, 10, 18, 24])

         print(scale_a.intersection(scale_b))
         print(scale_a & scale_b)

      .. testoutput:: EDOTuning

         EDOPitchScale([10, 18, 24], 31-EDO)
         EDOPitchScale([10, 18, 24], 31-EDO)

   .. tab:: Prime Limit

      .. testcode:: PrimeLimitTuning

         from xenharmlib import PrimeLimitTuning
         limit5 = PrimeLimitTuning(5)

         scale_a = limit5.rs_scale(['1/1', '5/4', '3/2', '25/16'])
         scale_b = limit5.rs_scale(['3/2', '25/16', '15/8', '9/4'])

         print(scale_a.intersection(scale_b))
         print(scale_a & scale_b)

      .. testoutput:: PrimeLimitTuning

         PrimeLimitPitchScale([3/2, 25/16], 5-Limit)
         PrimeLimitPitchScale([3/2, 25/16], 5-Limit)

   .. tab:: Western

      .. testcode:: WesternNotation

         from xenharmlib import WesternNotation
         western = WesternNotation()

         scale_a = western.pc_scale('CDEGB')
         scale_b = western.pc_scale('DEGBCD')

         print(scale_a.intersection(scale_b))
         print(scale_a & scale_b)

      .. testoutput:: WesternNotation

         WesternNoteScale([D0, E0, G0, B0])
         WesternNoteScale([D0, E0, G0, B0])

   .. tab:: UpDown

      .. testcode:: UpDownNotation

         from xenharmlib import EDOTuning
         from xenharmlib import UpDownNotation

         edo31 = EDOTuning(31)
         n_edo31 = UpDownNotation(edo31)

         C4 = n_edo31.note('C', 4)
         E4 = n_edo31.note('E', 4)
         Gb4 = n_edo31.note('Gb', 4)
         Aup4 = n_edo31.note('^A', 4)
         Bb4 = n_edo31.note('Bb', 4)

         scale_a = n_edo31.scale([E4, Gb4, Aup4, Bb4])
         scale_b = n_edo31.scale([C4, Gb4, Aup4, Bb4])

         print(scale_a.intersection(scale_b))
         print(scale_a & scale_b)

      .. testoutput:: UpDownNotation

         UpDownNoteScale([Gb4, ^A4, Bb4], 31-EDO)
         UpDownNoteScale([Gb4, ^A4, Bb4], 31-EDO)

It is possible to modify the intersection operation, so that equivalent
pitches (e.g. C4 and C5) are considered equal. This approach is especially
useful if you want to find common pitch classes that bridge one scale
to the other.

.. tabs::

   .. tab:: EDO

      .. testcode:: EDOTuning

         from xenharmlib import EDOTuning
         edo31 = EDOTuning(31)

         scale_a = edo31.index_scale([0, 4, 18, 24])
         scale_b = edo31.index_scale([20, 24, 31, 35])

         print(scale_a.intersection(scale_b, ignore_bi_index=True))

      .. testoutput:: EDOTuning

         EDOPitchScale([0, 4, 24, 31, 35], 31-EDO)

   .. tab:: Prime Limit

      .. testcode:: PrimeLimitTuning

         from xenharmlib import PrimeLimitTuning
         limit5 = PrimeLimitTuning(5)

         scale_a = limit5.rs_scale(['1/1', '5/4', '3/2', '15/8'])
         scale_b = limit5.rs_scale(['6/5', '15/8', '2/1', '5/2'])

         print(scale_a.intersection(scale_b, ignore_bi_index=True))

      .. testoutput:: PrimeLimitTuning

         PrimeLimitPitchScale([1, 5/4, 15/8, 2, 5/2], 5-Limit)

   .. tab:: Western

      .. testcode:: WesternNotation

         from xenharmlib import WesternNotation
         western = WesternNotation()

         C4 = western.note('C', 4)
         E4 = western.note('E', 4)
         Eb4 = western.note('Eb', 4)
         G4 = western.note('G', 4)
         B4 = western.note('B', 4)
         C5 = western.note('C', 5)
         E5 = western.note('E', 5)

         scale_a = western.scale([C4, E4, G4, B4])
         scale_b = western.scale([Eb4, B4, C5, E5])

         print(scale_a.intersection(scale_b, ignore_bi_index=True))

      .. testoutput:: WesternNotation

         WesternNoteScale([C4, E4, B4, C5, E5])

   .. tab:: UpDown

      .. testcode:: UpDownNotation

         from xenharmlib import EDOTuning
         from xenharmlib import UpDownNotation

         edo31 = EDOTuning(31)
         n_edo31 = UpDownNotation(edo31)

         Cb4 = n_edo31.note('Cb', 4)
         Eup4 = n_edo31.note('^E', 4)
         Eb4 = n_edo31.note('Eb', 4)
         G4 = n_edo31.note('G', 4)
         B4 = n_edo31.note('B', 4)
         Cb5 = n_edo31.note('Cb', 5)
         Eup5 = n_edo31.note('^E', 5)

         scale_a = n_edo31.scale([Cb4, Eup4, G4, B4])
         scale_b = n_edo31.scale([Eb4, B4, Cb5, Eup5])

         print(scale_a.intersection(scale_b, ignore_bi_index=True))

      .. testoutput:: UpDownNotation

         UpDownNoteScale([Cb4, ^E4, B4, Cb5, ^E5], 31-EDO)

Difference (:math:`A \setminus B`)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The :meth:`~xenharmlib.core.scale.Scale.difference` operation (also
possible to use with the infix operator :code:`-`) returns a new scale
contatining only elements that exist in the first scale, but not in
the second one.

.. tabs::

   .. tab:: EDO

      .. testcode:: EDOTuning

         from xenharmlib import EDOTuning
         edo31 = EDOTuning(31)

         scale_a = edo31.index_scale([3, 10, 18, 24, 29])
         scale_b = edo31.index_scale([4, 10, 18, 24])

         print(scale_a.difference(scale_b))
         print(scale_a - scale_b)

      .. testoutput:: EDOTuning

         EDOPitchScale([3, 29], 31-EDO)
         EDOPitchScale([3, 29], 31-EDO)

   .. tab:: Prime Limit

      .. testcode:: PrimeLimitTuning

         from xenharmlib import PrimeLimitTuning
         limit5 = PrimeLimitTuning(5)

         scale_a = limit5.rs_scale(['1/1', '5/4', '3/2', '25/16'])
         scale_b = limit5.rs_scale(['3/2', '25/16', '15/8', '9/4'])

         print(scale_a.difference(scale_b))
         print(scale_a - scale_b)

      .. testoutput:: PrimeLimitTuning

         PrimeLimitPitchScale([1, 5/4], 5-Limit)
         PrimeLimitPitchScale([1, 5/4], 5-Limit)

   .. tab:: Western

      .. testcode:: WesternNotation

         from xenharmlib import WesternNotation
         western = WesternNotation()

         scale_a = western.pc_scale('CDEGB')
         scale_b = western.pc_scale('DEGBCD')

         print(scale_a.difference(scale_b))
         print(scale_a - scale_b)

      .. testoutput:: WesternNotation

         WesternNoteScale([C0])
         WesternNoteScale([C0])

   .. tab:: UpDown

      .. testcode:: UpDownNotation

         from xenharmlib import EDOTuning
         from xenharmlib import UpDownNotation

         edo31 = EDOTuning(31)
         n_edo31 = UpDownNotation(edo31)

         C4 = n_edo31.note('C', 4)
         E4 = n_edo31.note('E', 4)
         Gb4 = n_edo31.note('Gb', 4)
         Aup4 = n_edo31.note('^A', 4)
         Bb4 = n_edo31.note('Bb', 4)

         scale_a = n_edo31.scale([E4, Gb4, Aup4, Bb4])
         scale_b = n_edo31.scale([C4, Gb4, Aup4, Bb4])

         print(scale_a.difference(scale_b))
         print(scale_a - scale_b)

      .. testoutput:: UpDownNotation

         UpDownNoteScale([E4], 31-EDO)
         UpDownNoteScale([E4], 31-EDO)

It is possible to modify the difference operation, so that equivalent
pitches (e.g. C4 and C5) are considered equal.

.. tabs::

   .. tab:: EDO

      .. testcode:: EDOTuning

         from xenharmlib import EDOTuning
         edo31 = EDOTuning(31)

         scale_a = edo31.index_scale([0, 4, 18, 24])
         scale_b = edo31.index_scale([20, 24, 31, 35])

         print(scale_a.difference(scale_b, ignore_bi_index=True))

      .. testoutput:: EDOTuning

         EDOPitchScale([18], 31-EDO)

   .. tab:: Prime Limit

      .. testcode:: PrimeLimitTuning

         from xenharmlib import PrimeLimitTuning
         limit5 = PrimeLimitTuning(5)

         scale_a = limit5.rs_scale(['1/1', '5/4', '3/2', '15/8'])
         scale_b = limit5.rs_scale(['6/5', '15/8', '2/1', '5/2'])

         print(scale_a.difference(scale_b, ignore_bi_index=True))

      .. testoutput:: PrimeLimitTuning

         PrimeLimitPitchScale([3/2], 5-Limit)

   .. tab:: Western

      .. testcode:: WesternNotation

         from xenharmlib import WesternNotation
         western = WesternNotation()

         C4 = western.note('C', 4)
         E4 = western.note('E', 4)
         Eb4 = western.note('Eb', 4)
         G4 = western.note('G', 4)
         B4 = western.note('B', 4)
         C5 = western.note('C', 5)
         E5 = western.note('E', 5)

         scale_a = western.scale([C4, E4, G4, B4])
         scale_b = western.scale([Eb4, B4, C5, E5])

         print(scale_a.difference(scale_b, ignore_bi_index=True))

      .. testoutput:: WesternNotation

         WesternNoteScale([G4])

   .. tab:: UpDown

      .. testcode:: UpDownNotation

         from xenharmlib import EDOTuning
         from xenharmlib import UpDownNotation

         edo31 = EDOTuning(31)
         n_edo31 = UpDownNotation(edo31)

         Cb4 = n_edo31.note('Cb', 4)
         Eup4 = n_edo31.note('^E', 4)
         Eb4 = n_edo31.note('Eb', 4)
         G4 = n_edo31.note('G', 4)
         B4 = n_edo31.note('B', 4)
         Cb5 = n_edo31.note('Cb', 5)
         Eup5 = n_edo31.note('^E', 5)

         scale_a = n_edo31.scale([Cb4, Eup4, G4, B4])
         scale_b = n_edo31.scale([Eb4, B4, Cb5, Eup5])

         print(scale_a.difference(scale_b, ignore_bi_index=True))

      .. testoutput:: UpDownNotation

         UpDownNoteScale([G4], 31-EDO)


Symmetric Difference (:math:`A \triangle B`)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The :meth:`~xenharmlib.core.scale.Scale.symmetric_difference` operation
(also possible to use with the infix operator :code:`^`) returns a new
scale contatining only elements that exist in the first scale, but not
in the second one combined with elements that exist in the second scale
but not in the first one.

.. tabs::

   .. tab:: EDO

      .. testcode:: EDOTuning

         from xenharmlib import EDOTuning
         edo31 = EDOTuning(31)

         scale_a = edo31.index_scale([3, 10, 18, 24, 29])
         scale_b = edo31.index_scale([4, 10, 18, 24])

         print(scale_a.symmetric_difference(scale_b))
         print(scale_a ^ scale_b)

      .. testoutput:: EDOTuning

         EDOPitchScale([3, 4, 29], 31-EDO)
         EDOPitchScale([3, 4, 29], 31-EDO)

   .. tab:: Prime Limit

      .. testcode:: PrimeLimitTuning

         from xenharmlib import PrimeLimitTuning
         limit5 = PrimeLimitTuning(5)

         scale_a = limit5.rs_scale(['1/1', '5/4', '3/2', '25/16'])
         scale_b = limit5.rs_scale(['3/2', '25/16', '15/8', '9/4'])

         print(scale_a.symmetric_difference(scale_b))
         print(scale_a ^ scale_b)

      .. testoutput:: PrimeLimitTuning

         PrimeLimitPitchScale([1, 5/4, 15/8, 9/4], 5-Limit)
         PrimeLimitPitchScale([1, 5/4, 15/8, 9/4], 5-Limit)

   .. tab:: Western

      .. testcode:: WesternNotation

         from xenharmlib import WesternNotation
         western = WesternNotation()

         scale_a = western.pc_scale('CDEGB')
         scale_b = western.pc_scale('DEGBCD')

         print(scale_a.symmetric_difference(scale_b))
         print(scale_a ^ scale_b)

      .. testoutput:: WesternNotation

         WesternNoteScale([C0, C1, D1])
         WesternNoteScale([C0, C1, D1])

   .. tab:: UpDown

      .. testcode:: UpDownNotation

         from xenharmlib import EDOTuning
         from xenharmlib import UpDownNotation

         edo31 = EDOTuning(31)
         n_edo31 = UpDownNotation(edo31)

         C4 = n_edo31.note('C', 4)
         E4 = n_edo31.note('E', 4)
         Gb4 = n_edo31.note('Gb', 4)
         Aup4 = n_edo31.note('^A', 4)
         Bb4 = n_edo31.note('Bb', 4)

         scale_a = n_edo31.scale([E4, Gb4, Aup4, Bb4])
         scale_b = n_edo31.scale([C4, Gb4, Aup4, Bb4])

         print(scale_a.symmetric_difference(scale_b))
         print(scale_a ^ scale_b)

      .. testoutput:: UpDownNotation

         UpDownNoteScale([C4, E4], 31-EDO)
         UpDownNoteScale([C4, E4], 31-EDO)

It is possible to modify the symmetric difference operation, so that
equivalent pitches (e.g. C4 and C5) are considered equal.

.. tabs::

   .. tab:: EDO

      .. testcode:: EDOTuning

         from xenharmlib import EDOTuning
         edo31 = EDOTuning(31)

         scale_a = edo31.index_scale([0, 4, 18, 24])
         scale_b = edo31.index_scale([20, 24, 31, 35])

         print(scale_a.symmetric_difference(scale_b, ignore_bi_index=True))

      .. testoutput:: EDOTuning

         EDOPitchScale([18, 20], 31-EDO)

   .. tab:: Prime Limit

      .. testcode:: PrimeLimitTuning

         from xenharmlib import PrimeLimitTuning
         limit5 = PrimeLimitTuning(5)

         scale_a = limit5.rs_scale(['1/1', '5/4', '3/2', '15/8'])
         scale_b = limit5.rs_scale(['6/5', '15/8', '2/1', '5/2'])

         print(scale_a.symmetric_difference(scale_b, ignore_bi_index=True))

      .. testoutput:: PrimeLimitTuning

         PrimeLimitPitchScale([6/5, 3/2], 5-Limit)

   .. tab:: Western

      .. testcode:: WesternNotation

         from xenharmlib import WesternNotation
         western = WesternNotation()

         C4 = western.note('C', 4)
         E4 = western.note('E', 4)
         Eb4 = western.note('Eb', 4)
         G4 = western.note('G', 4)
         B4 = western.note('B', 4)
         C5 = western.note('C', 5)
         E5 = western.note('E', 5)

         scale_a = western.scale([C4, E4, G4, B4])
         scale_b = western.scale([Eb4, B4, C5, E5])

         print(scale_a.symmetric_difference(scale_b, ignore_bi_index=True))

      .. testoutput:: WesternNotation

         WesternNoteScale([Eb4, G4])

   .. tab:: UpDown

      .. testcode:: UpDownNotation

         from xenharmlib import EDOTuning
         from xenharmlib import UpDownNotation

         edo31 = EDOTuning(31)
         n_edo31 = UpDownNotation(edo31)

         Cb4 = n_edo31.note('Cb', 4)
         Eup4 = n_edo31.note('^E', 4)
         Eb4 = n_edo31.note('Eb', 4)
         G4 = n_edo31.note('G', 4)
         B4 = n_edo31.note('B', 4)
         Cb5 = n_edo31.note('Cb', 5)
         Eup5 = n_edo31.note('^E', 5)

         scale_a = n_edo31.scale([Cb4, Eup4, G4, B4])
         scale_b = n_edo31.scale([Eb4, B4, Cb5, Eup5])

         print(scale_a.symmetric_difference(scale_b, ignore_bi_index=True))

      .. testoutput:: UpDownNotation

         UpDownNoteScale([Eb4, G4], 31-EDO)

Subset Relations (:math:`A \subset B`, :math:`A \subseteq B`)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The :meth:`~xenharmlib.core.scale.Scale.is_subset` operation (also possible
to use with the infix operator :code:`<=` for "subset or equal" and
:code:`<` for "proper subset") returns True if all the elements in
one scale exist in the other.

.. tabs::

   .. tab:: EDO

      .. testcode:: EDOTuning

         from xenharmlib import EDOTuning
         edo31 = EDOTuning(31)

         scale_a = edo31.index_scale([3, 10, 18, 24, 29])
         scale_b = edo31.index_scale([3, 10, 18, 24])

         print(scale_b.is_subset(scale_a))
         print(scale_a.is_subset(scale_a, proper=True))

         print(scale_b <= scale_a)
         print(scale_a < scale_a)

      .. testoutput:: EDOTuning

         True
         False
         True
         False

   .. tab:: Prime Limit

      .. testcode:: PrimeLimitTuning

         from xenharmlib import PrimeLimitTuning
         limit5 = PrimeLimitTuning(5)

         scale_a = limit5.rs_scale(['1/1', '5/4', '3/2', '25/16'])
         scale_b = limit5.rs_scale(['5/4', '3/2', '25/16'])

         print(scale_b.is_subset(scale_a))
         print(scale_a.is_subset(scale_a, proper=True))

         print(scale_b <= scale_a)
         print(scale_a < scale_a)

      .. testoutput:: PrimeLimitTuning

         True
         False
         True
         False

   .. tab:: Western

      .. testcode:: WesternNotation

         from xenharmlib import WesternNotation
         western = WesternNotation()

         scale_a = western.pc_scale('CDEGB')
         scale_b = western.pc_scale('CDEG')

         print(scale_b.is_subset(scale_a))
         print(scale_a.is_subset(scale_a, proper=True))

         print(scale_b <= scale_a)
         print(scale_a < scale_a)

      .. testoutput:: WesternNotation

         True
         False
         True
         False

   .. tab:: UpDown

      .. testcode:: UpDownNotation

         from xenharmlib import EDOTuning
         from xenharmlib import UpDownNotation

         edo31 = EDOTuning(31)
         n_edo31 = UpDownNotation(edo31)

         E4 = n_edo31.note('E', 4)
         Gb4 = n_edo31.note('Gb', 4)
         Aup4 = n_edo31.note('^A', 4)
         Bb4 = n_edo31.note('Bb', 4)

         scale_a = n_edo31.scale([E4, Gb4, Aup4, Bb4])
         scale_b = n_edo31.scale([Gb4, Aup4, Bb4])

         print(scale_b.is_subset(scale_a))
         print(scale_a.is_subset(scale_a, proper=True))

         print(scale_b <= scale_a)
         print(scale_a < scale_a)

      .. testoutput:: UpDownNotation

         True
         False
         True
         False

It is possible to modify the subset operation, so that equivalent pitches
(e.g. C4 and C5) are considered equal.

.. tabs::

   .. tab:: EDO

      .. testcode:: EDOTuning

         from xenharmlib import EDOTuning
         edo31 = EDOTuning(31)

         scale_a = edo31.index_scale([0, 4, 18])
         scale_b = edo31.index_scale([31, 35, 49])

         print(scale_b.is_subset(scale_a, ignore_bi_index=True))
         print(scale_b.is_subset(scale_a, proper=True, ignore_bi_index=True))

      .. testoutput:: EDOTuning

         True
         False

   .. tab:: Prime Limit

      .. testcode:: PrimeLimitTuning

         from xenharmlib import PrimeLimitTuning
         limit5 = PrimeLimitTuning(5)

         scale_a = limit5.rs_scale(['1/1', '5/4', '3/2'])
         scale_b = limit5.rs_scale(['2/1', '5/2', '3/1'])

         print(scale_b.is_subset(scale_a, ignore_bi_index=True))
         print(scale_b.is_subset(scale_a, proper=True, ignore_bi_index=True))

      .. testoutput:: PrimeLimitTuning

         True
         False

   .. tab:: Western

      .. testcode:: WesternNotation

         from xenharmlib import WesternNotation
         western = WesternNotation()

         C4 = western.note('C', 4)
         E4 = western.note('E', 4)
         G4 = western.note('G', 4)
         C5 = western.note('C', 5)
         E5 = western.note('E', 5)
         G5 = western.note('G', 5)

         scale_a = western.scale([C4, E4, G4])
         scale_b = western.scale([C5, E5, G5])

         print(scale_b.is_subset(scale_a, ignore_bi_index=True))
         print(scale_b.is_subset(scale_a, proper=True, ignore_bi_index=True))

      .. testoutput:: WesternNotation

         True
         False

   .. tab:: UpDown

      .. testcode:: UpDownNotation

         from xenharmlib import EDOTuning
         from xenharmlib import UpDownNotation

         edo31 = EDOTuning(31)
         n_edo31 = UpDownNotation(edo31)

         Cb4 = n_edo31.note('Cb', 4)
         Eup4 = n_edo31.note('^E', 4)
         G4 = n_edo31.note('G', 4)
         Cb5 = n_edo31.note('Cb', 5)
         Eup5 = n_edo31.note('^E', 5)
         G5 = n_edo31.note('G', 5)

         scale_a = n_edo31.scale([Cb4, Eup4, G4])
         scale_b = n_edo31.scale([Cb5, Eup5, G5])

         print(scale_b.is_subset(scale_a, ignore_bi_index=True))
         print(scale_b.is_subset(scale_a, proper=True, ignore_bi_index=True))

      .. testoutput:: UpDownNotation

         True
         False

Disjoint Sets (:math:`A \cap B = \emptyset`)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Two scales can be tested if they don not contain any common elements 
(are disjoint) by the :meth:`~xenharmlib.core.scale.Scale.is_disjoint`
operation.

.. tabs::

   .. tab:: EDO

      .. testcode:: EDOTuning

         from xenharmlib import EDOTuning
         edo31 = EDOTuning(31)

         scale_a = edo31.index_scale([3, 10, 18, 24, 29])
         scale_b = edo31.index_scale([4, 10, 18, 24])
         scale_c = edo31.index_scale([4, 11, 19, 25])

         print(scale_a.is_disjoint(scale_b))
         print(scale_a.is_disjoint(scale_c))

      .. testoutput:: EDOTuning

         False
         True

   .. tab:: Prime Limit

      .. testcode:: PrimeLimitTuning

         from xenharmlib import PrimeLimitTuning
         limit5 = PrimeLimitTuning(5)

         scale_a = limit5.rs_scale(['1/1', '5/4', '3/2', '25/16'])
         scale_b = limit5.rs_scale(['3/2', '25/16', '15/8', '9/4'])
         scale_c = limit5.rs_scale(['15/2', '125/16', '75/8', '45/4'])

         print(scale_a.is_disjoint(scale_b))
         print(scale_a.is_disjoint(scale_c))

      .. testoutput:: PrimeLimitTuning

         False
         True

   .. tab:: Western

      .. testcode:: WesternNotation

         from xenharmlib import WesternNotation
         western = WesternNotation()

         scale_a = western.pc_scale('CDEGB')
         scale_b = western.pc_scale('DEGBCD')
         scale_c = western.pc_scale('FA')

         print(scale_a.is_disjoint(scale_b))
         print(scale_a.is_disjoint(scale_c))

      .. testoutput:: WesternNotation

         False
         True

   .. tab:: UpDown

      .. testcode:: UpDownNotation

         from xenharmlib import EDOTuning
         from xenharmlib import UpDownNotation

         edo31 = EDOTuning(31)
         n_edo31 = UpDownNotation(edo31)

         C4 = n_edo31.note('C', 4)
         E4 = n_edo31.note('E', 4)
         Eb4 = n_edo31.note('Eb', 4)
         Gb4 = n_edo31.note('Gb', 4)
         Aup4 = n_edo31.note('^A', 4)
         Bb4 = n_edo31.note('Bb', 4)

         scale_a = n_edo31.scale([Eb4, Gb4, Bb4])
         scale_b = n_edo31.scale([Gb4, Aup4, Bb4])
         scale_c = n_edo31.scale([C4, E4])

         print(scale_a.is_disjoint(scale_b))
         print(scale_a.is_disjoint(scale_c))

      .. testoutput:: UpDownNotation

         False
         True

It is possible to modify the disjoint test, so that equivalent pitches
(e.g. C4 and C5) are considered equal.

.. tabs::

   .. tab:: EDO

      .. testcode:: EDOTuning

         from xenharmlib import EDOTuning
         edo31 = EDOTuning(31)

         scale_a = edo31.index_scale([0, 4, 18])
         scale_b = edo31.index_scale([31, 35, 49])

         print(scale_a.is_disjoint(scale_b, ignore_bi_index=True))

      .. testoutput:: EDOTuning

         False

   .. tab:: Prime Limit

      .. testcode:: PrimeLimitTuning

         from xenharmlib import PrimeLimitTuning
         limit5 = PrimeLimitTuning(5)

         scale_a = limit5.rs_scale(['1/1', '5/4', '3/2'])
         scale_b = limit5.rs_scale(['2/1', '5/2', '3/1'])

         print(scale_a.is_disjoint(scale_b, ignore_bi_index=True))

      .. testoutput:: PrimeLimitTuning

         False

   .. tab:: Western

      .. testcode:: WesternNotation

         from xenharmlib import WesternNotation
         western = WesternNotation()

         C4 = western.note('C', 4)
         E4 = western.note('E', 4)
         G4 = western.note('G', 4)
         C5 = western.note('C', 5)
         E5 = western.note('E', 5)
         G5 = western.note('G', 5)

         scale_a = western.scale([C4, E4, G4])
         scale_b = western.scale([C5, E5, G5])

         print(scale_a.is_disjoint(scale_b, ignore_bi_index=True))

      .. testoutput:: WesternNotation

         False

   .. tab:: UpDown

      .. testcode:: UpDownNotation

         from xenharmlib import EDOTuning
         from xenharmlib import UpDownNotation

         edo31 = EDOTuning(31)
         n_edo31 = UpDownNotation(edo31)

         Cb4 = n_edo31.note('Cb', 4)
         Eup4 = n_edo31.note('^E', 4)
         G4 = n_edo31.note('G', 4)
         Cb5 = n_edo31.note('Cb', 5)
         Eup5 = n_edo31.note('^E', 5)
         G5 = n_edo31.note('G', 5)

         scale_a = n_edo31.scale([Cb4, Eup4, G4])
         scale_b = n_edo31.scale([Cb5, Eup5, G5])

         print(scale_a.is_disjoint(scale_b, ignore_bi_index=True))

      .. testoutput:: UpDownNotation

         False

Enharmonic ambiguity and set operations
-----------------------------------------

When we speak of enharmonic equivalence we mean that two notes refer
to the same pitch, but are notated differently, that is: we
differentiate between the sound of a note and its function.
The question if Eb and D# in 12-EDO are *the same* can only be
answered if we further specify: Same in regards to what?

In regards to notation Eb and D# are distinct, however in regards
to sound they are the same. Spoken in mathematical terms:
Notation systems in which there is enharmonic equivalence
define two equivalency relations on the space of notes. We already came
across to both of them in the chapter about notes: The :code:`==`
operator considers notes as equal if their frequency is the same
while the method :code:`is_notated_same` checks for notation
equality.

The existence of two different equivalency relations on the space
of notes poses a problem for us when we want to define scales and
operations on them:
Note scales are defined as 'an ordered set of *unique* notes',
meaning that no two notes in a scale are the same. Now should
this refer to notation or sound? After all in cases where we
are interested in the functional relationship of scales, we
would want to treat D# and Eb as distinct, while in other cases
we want them to be considered equal.

Xenharmlib defines the uniqueness restriction of the scale as "unique in
*pitch*", meaning that no two notes :code:`e_flat` and :code:`d_sharp` with
:code:`e_flat == d_sharp` can exist in the scale at the same time. However,
it provides special variants for some set operations that honor notational
differences (More on that later).

The reason for choosing the :code:`==` equivalency as the base for the
uniqueness property is to provide consistency with the underlying pitch
scale object:

.. testcode::

    e_flat = n_edo12.note('Eb', 0)
    d_sharp = n_edo12.note('D#', 0)

    scale_a = n_edo12.scale([e_flat])
    scale_b = n_edo12.scale([d_sharp])

    note_union = scale_a.union(scale_b)
    pitch_union = scale_a.pitch_scale.union(
        scale_b.pitch_scale
    )

    # among others, these would break if we would
    # treat Eb and D# distinct in note scales
    assert note_union.frequencies == pitch_union.frequencies
    assert len(note_union) == len(pitch_union)
    pitch_intervals = [
        i.pitch_interval for i in note_union.to_intervals()
    ]
    assert pitch_intervals == pitch_union.to_intervals()

This choice also allows implementing the scale's :code:`==` operator
as a consistent logical extension of the note's :code:`==` operator,
creating a closed set algebra for scales under :code:`==` with all
basic set operations. Think of it this way: Notes are variable names
holding the pitch as their value with some variables being equal:

.. math::

   A = \{a, b\}\\
   B = \{c, d\}\\
   \\
   b = c \rightarrow\\
   A \cap B = \{b\} = \{c\}\\
   A \cup B = \{a, b, d\} == \{a, c, d\}\\

How does xenharmlib then choose the note representation of a pitch when
more than one enharmonically equivalent note is present? During
construction of a note scale it chooses on the principle of first
encounter:

.. testcode::

    scale = n_edo12.scale(
        [
            n_edo12.note('D#', 0),
            n_edo12.note('Eb', 0),
        ]
    )
    assert len(scale) == 1
    assert scale[0].pc_symbol == 'D#'

When using set operations xenharmlib always prefers the representation
of the scale that executed the operation:

.. testcode::

    c = n_edo12.note('C', 0)
    g = n_edo12.note('G', 0)
    e_flat = n_edo12.note('Eb', 0)
    d_sharp = n_edo12.note('D#', 0)

    scale_a = n_edo12.scale([c, e_flat])
    scale_b = n_edo12.scale([d_sharp, g])

    # A v B / A ^ B

    union_a_b = scale_a.union(scale_b)
    assert union_a_b.is_notated_same(
        n_edo12.scale([c, e_flat, g])
    )

    intersection_a_b = scale_a.intersection(scale_b)
    assert intersection_a_b.is_notated_same(
        n_edo12.scale([e_flat])
    )

    # B v A / B ^ A

    union_b_a = scale_b.union(scale_a)
    assert union_b_a.is_notated_same(
        n_edo12.scale([c, d_sharp, g])
    )

    intersection_b_a = scale_b.intersection(scale_a)
    assert intersection_b_a.is_notated_same(
        n_edo12.scale([d_sharp])
    )

Using the :code:`==` operator we see that even though the results
are different in terms of representation, commutativity in regards
to union and intersection is still preserved:

.. testcode::

    assert union_a_b == union_b_a
    assert intersection_a_b == intersection_b_a

In contrast using the :code:`is_notated_same` equivalency relation
on the two result pairs does *not* preserve commutativity:

.. testcode::

    assert not union_a_b.is_notated_same(union_b_a)
    assert not intersection_a_b.is_notated_same(intersection_b_a)

Since we chose the :code:`==` operator as a basis for scale uniqueness,
there is no way to define a closed set algebra for the :code:`is_notated_same`
relation at the same time, because the union operation would not be well
defined.

However, on *certain* set operations, we can define the option to use
the :code:`is_notated_same` relation. For :code:`intersection`, we
can define that same-sounding, but differently notated notes should
not be part of the intersection. For :code:`difference` we can define
that such notes will not be removed from the first scale. In the
same way, we can define the relationships :code:`is_disjoint`,
:code:`is_subset`, and :code:`is_superset`.

These stricter variants of the set operations are called:

* :meth:`~xenharmlib.core.note_scale.NoteScale.note_intersection`
* :meth:`~xenharmlib.core.note_scale.NoteScale.note_difference`
* :meth:`~xenharmlib.core.note_scale.NoteScale.is_note_subset`
* :meth:`~xenharmlib.core.note_scale.NoteScale.is_note_superset`
* :meth:`~xenharmlib.core.note_scale.NoteScale.is_notated_disjoint`

.. testcode::

    c = n_edo12.note('C', 0)
    g = n_edo12.note('G', 0)
    e_flat = n_edo12.note('Eb', 0)
    d_sharp = n_edo12.note('D#', 0)

    scale_a = n_edo12.scale([c, e_flat])
    scale_b = n_edo12.scale([d_sharp, g])

    intersection_a_b = scale_a.note_intersection(scale_b)
    assert len(intersection_a_b) == 0

    diff_a_b = scale_a.note_difference(scale_b)
    assert len(diff_a_b) == 2

In combination with the :code:`ignore_bi_index` flag, we can for
example build a function that returns the pitch class symbols of
the common notes of two scales while being aware of the key:

.. testcode::

    def common_notes_key_aware(scale_a, scale_b):
        scale_i = scale_a.note_intersection(
            scale_b,
            ignore_bi_index=True
        ).pcs_normalized()
        return scale_i

    # F# major and Gb major have exactly the same
    # pitches, however they are notated differently
    f_sharp_maj = n_edo12.natural_scale().transpose(
        n_edo12.shorthand_interval('A', 4)
    )
    g_flat_maj = n_edo12.natural_scale().transpose(
        n_edo12.shorthand_interval('d', 5)
    )

    # D# minor is the relative key to F# major
    d_sharp_min = f_sharp_maj.rotation(5)

    print(common_notes_key_aware(f_sharp_maj, g_flat_maj))
    print(common_notes_key_aware(g_flat_maj, d_sharp_min))
    print(common_notes_key_aware(f_sharp_maj, d_sharp_min))

.. testoutput::

    UpDownNoteScale([], 12-EDO)
    UpDownNoteScale([], 12-EDO)
    UpDownNoteScale([C#0, D#0, E#0, F#0, G#0, A#0, B0], 12-EDO)
