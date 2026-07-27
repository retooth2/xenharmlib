Pitches & Notes
==============================

As outlined in the introduction, frequency representations are the smallest
building unit in the realm of harmonic primitives in xenharmlib. Other than
second-order or third-order primitives, their method of construction is
highly dependent on the context they originate from. We try to give a
general overview of them here, but be sure to also check the specifics
in the respective sections on tunings and notations.

We can roughly divide frequency representations into two classes:
**Pitches** and **notes**. Pitches (which originate from *tunings*)
are *numeric* representations of frequencies, while notes
(originating from *notations*) are *symbolic string*
representations of frequencies. 

Numeric Representation
--------------------------------

Depending on tuning, frequencies can be represented numerically either
through an integer or a lattice point. This parameter is called **pitch
index** in xenharmlib. The unified standard builder method to create
a frequency representation from a pitch index in a tuning is called
:meth:`~xenharmlib.core.tunings.TuningABC.pitch`:

.. tabs::

   .. tab:: EDO

      .. testcode:: EDOTuning

         from xenharmlib import EDOTuning
         edo31 = EDOTuning(31)

         p10 = edo31.pitch(10)
         print(p10.frequency.to_float())

      .. testoutput:: EDOTuning

         20.448744438412696

   .. tab:: Prime Limit

      .. testcode:: PrimeLimitTuning

         from xenharmlib import PrimeLimitTuning
         limit5 = PrimeLimitTuning(5)

         pitch = limit5.pitch(limit5.lattice.point((-1, 1, 0)))
         print(pitch.frequency.to_float())

      .. testoutput:: PrimeLimitTuning

         24.52739674693112

One purpose of the different tuning objects is to define the *mapping*
of pitch indices to frequencies, so the same numerical value can represent
a completely different frequency when tuning contexts are switched.
Observe how the above integer index :code:`10` and the integer
vector :code:`(-1, 1, 1)` are mapped to different frequencies
when applied to other tuning contexts:

.. tabs::

   .. tab:: EDO31 vs EDO24

      .. testcode:: EDOTuning

         from xenharmlib import EDOTuning

         edo24 = EDOTuning(24)
         edo31 = EDOTuning(31)

         pitch_a = edo24.pitch(10)
         pitch_b = edo24.pitch(31)

         print(pitch_a.frequency.to_float())
         print(pitch_b.frequency.to_float())

      .. testoutput:: EDOTuning

         21.826764464562743
         40.03046252816015

   .. tab:: 5-Limit vs 2.3.7 Subgroup

      .. testcode:: PrimeLimitTuning

         from xenharmlib import PrimeLimitTuning
         from xenharmlib import MultiGenTuning
         from xenharmlib import FrequencyRatio

         limit5 = PrimeLimitTuning(5)

         sg237 = MultiGenTuning(
             [FrequencyRatio(p) for p in [2, 3, 7]],
             eq_diff_vec=(1, 0, 0)
         )

         pitch_a = limit5.pitch(limit5.lattice.point((-1, 1, 1)))
         pitch_b = sg237.pitch(sg237.lattice.point((-1, 1, 1)))

         print(pitch_a.frequency.to_float())
         print(pitch_b.frequency.to_float())

      .. testoutput:: PrimeLimitTuning

         122.63698373465562
         171.69177722851785

Pitches provide the pitch index from which they were created as a property
for later inspection. In addition, pitches also provide a *pitch class index*
that denotes the (integer or lattice point) equivalency class of the pitch
index with regard to the equivalency interval (e.g., the octave) of the
tuning:

.. tabs::

   .. tab:: EDO

      .. testcode:: EDOTuning

         from xenharmlib import EDOTuning
         edo31 = EDOTuning(31)

         pitch = edo31.pitch(33)
         print(pitch.pitch_index)
         print(pitch.pc_index)

      .. testoutput:: EDOTuning

         33
         2

   .. tab:: Prime Limit

      .. testcode:: PrimeLimitTuning

         from xenharmlib import PrimeLimitTuning
         limit5 = PrimeLimitTuning(5)

         pitch = limit5.pitch(limit5.lattice.point((0, 1, 0)))
         print(pitch.pitch_index)
         print(pitch.pc_index)

      .. testoutput:: PrimeLimitTuning

         LatticePoint(0, 1, 0)
         LatticePoint(-1, 1, 0)

Tunings with lattice point indices provide a convenience builder method
that does not expect a proper lattice point object, but a tuple from
which then the tuning creates the lattice point object "under the hood":

.. tabs::

   .. tab:: Prime Limit

      .. testcode:: PrimeLimitTuning

         from xenharmlib import PrimeLimitTuning
         limit5 = PrimeLimitTuning(5)

         pitch = limit5.vec_pitch((0, 1, 0))
         print(pitch.pitch_index)
         print(pitch.pc_index)

      .. testoutput:: PrimeLimitTuning

         LatticePoint(0, 1, 0)
         LatticePoint(-1, 1, 0)

   .. tab:: 2.3.7 Subgroup

      .. testcode:: MultiGenTuning

         from xenharmlib import MultiGenTuning
         from xenharmlib import FrequencyRatio

         sg237 = MultiGenTuning(
             [FrequencyRatio(p) for p in [2, 3, 7]],
             eq_diff_vec=(1, 0, 0)
         )

         pitch = sg237.vec_pitch((0, 1, 0))
         print(pitch.pitch_index)
         print(pitch.pc_index)

      .. testoutput:: MultiGenTuning

         LatticePoint(0, 1, 0)
         LatticePoint(-1, 1, 0)

Symbolic Representation
--------------------------------

If frequencies are represented by strings (or combinations of strings and
numbers) we speak of these symbolic representations as **notes**.
Notes are created by the :meth:`~xenharmlib.core.notation.NotationABC.note`
method of notations. The specific creation parameters depend on the type
of notation that is employed:

.. tabs::

   .. tab:: Western

      .. testcode:: WesternNotation

         from xenharmlib import WesternNotation
         western = WesternNotation()

         A4 = western.note('A', 4)
         print(A4.frequency.to_float())

      .. testoutput:: WesternNotation

         440.0

   .. tab:: UpDown

      .. testcode:: UpDownNotation

         from xenharmlib import EDOTuning
         from xenharmlib import UpDownNotation

         edo31 = EDOTuning(31)
         n_edo31 = UpDownNotation(edo31)

         Aup4 = n_edo31.note('^A', 4)
         print(Aup4.frequency.to_float())

      .. testoutput:: UpDownNotation

         447.44087978031575

In the same way notations are wrappers around tunings, notes are wrappers
around pitches. Every note object can be transformed into the corresponding
pitch object:

.. tabs::

   .. tab:: Western

      .. testcode:: WesternNotation

         from xenharmlib import WesternNotation
         western = WesternNotation()

         A4 = western.note('A', 4)
         print(A4.pitch)

      .. testoutput:: WesternNotation

         EDOPitch(57, 12-EDO)

   .. tab:: UpDown

      .. testcode:: UpDownNotation

         from xenharmlib import EDOTuning
         from xenharmlib import UpDownNotation

         edo31 = EDOTuning(31)

         n_edo31 = UpDownNotation(edo31)

         Aup4 = n_edo31.note('^A', 4)
         print(Aup4.pitch)

      .. testoutput:: UpDownNotation

         EDOPitch(148, 31-EDO)

Pitches can also be transformed into a corresponding note object; however,
because of enharmonic equivalence, this transformation is not necessarily
unique. In the Western system, for example, there can be infinite corresponding
note objects to a single pitch object (think of G#4, Ab4, Bbbb4, Cbbbb5 all
referring to the same key on a piano), so xenharmlib makes a guess:

.. tabs::

   .. tab:: Western

      .. testcode:: WesternNotation

         from xenharmlib import WesternNotation

         western = WesternNotation()
         tuning = western.tuning

         pitch = tuning.pitch(8)
         note = western.guess_note(pitch)

         print(note)

      .. testoutput:: WesternNotation

         WesternNote(G#, 0)

   .. tab:: UpDown

      .. testcode:: UpDownNotation

         from xenharmlib import EDOTuning
         from xenharmlib import UpDownNotation

         edo31 = EDOTuning(31)
         n_edo31 = UpDownNotation(edo31)

         pitch = edo31.pitch(19)
         note = n_edo31.guess_note(pitch)

         print(note)

      .. testoutput:: UpDownNotation

         UpDownNote(Abb, 0, 31-EDO)

Most of the time it is not necessary to convert pitches and notes into one
another, because they expose the same interface with regard to methods and
properties; e.g., each note can be inspected with regard to its pitch index
and pitch class index:

.. tabs::

   .. tab:: Western

      .. testcode:: WesternNotation

         from xenharmlib import WesternNotation
         western = WesternNotation()

         A4 = western.note('A', 4)
         print(A4.pitch_index)
         print(A4.pc_index)

      .. testoutput:: WesternNotation

         57
         9


   .. tab:: UpDown

      .. testcode:: UpDownNotation

         from xenharmlib import EDOTuning
         from xenharmlib import UpDownNotation

         edo31 = EDOTuning(31)
         n_edo31 = UpDownNotation(edo31)

         Aup4 = n_edo31.note('^A', 4)
         print(Aup4.pitch_index)
         print(Aup4.pc_index)

      .. testoutput:: UpDownNotation

         148
         24

Construction Based on Closest Frequency
-----------------------------------------------------

Origin contexts based on integer indices allow construction based on the
approximation of frequencies. Given an arbitrary frequency, the
:meth:`~xenharmlib.core.origin_context.OriginContext.closest_freq_repr`
method returns the pitch or note of an origin context that is closest
to it:

.. tabs::

   .. tab:: EDO

      .. testcode:: EDOTuning

         from xenharmlib import EDOTuning
         from xenharmlib import Frequency

         edo31 = EDOTuning(31)
         pitch = edo31.closest_freq_repr(Frequency(500))
         print(pitch)
         print(pitch.frequency.to_float())

      .. testoutput:: EDOTuning

         EDOPitch(153, 31-EDO)
         500.367260159388

   .. tab:: Western

      .. testcode:: WesternNotation

         from xenharmlib import WesternNotation
         from xenharmlib import Frequency

         western = WesternNotation()
         note = western.closest_freq_repr(Frequency(450))
         print(note)
         print(note.frequency.to_float())

      .. testoutput:: WesternNotation

         WesternNote(A, 4)
         440.0

   .. tab:: UpDown

      .. testcode:: UpDownNotation

         from xenharmlib import EDOTuning
         from xenharmlib import UpDownNotation
         from xenharmlib import Frequency

         edo31 = EDOTuning(31)
         n_edo31 = UpDownNotation(edo31)
         note = n_edo31.closest_freq_repr(Frequency(500))
         print(note)
         print(note.frequency.to_float())

      .. testoutput:: UpDownNotation

         UpDownNote(Cb, 5, 31-EDO)
         500.367260159388

We mentioned that only tunings and notations based on integer pitch indices
support "closest approximation". This is because in multi-generator tunings
like prime limit tunings there are infinite representations between every
two representations, meaning that a single "closest" pitch can not be found:

.. testcode::

   from xenharmlib import WesternNotation
   from xenharmlib import PrimeLimitTuning

   western = WesternNotation()
   limit7 = PrimeLimitTuning(7)

   try:
       western.note('F#', 4).retune_closest(limit7)
   except Exception as exc:
       print(exc)

.. testoutput::

   Not possible to find a closest representation to the given frequency, either because in this harmonic context frequencies can be approximated arbitrarily close (so there is no closest representation) or the way in which this harmonic context is defined is not restricted enough to mathematically deduce a method of approximation.


Identity, Comparison and Equivalency
--------------------------------------

All frequency representations can be compared to one another and tested
for equality, regardless of the tuning or notation they originate from.
This is because at the core they are, well, representations of frequencies,
and frequencies can be compared to one another (which frequency is bigger?)
or tested for equality (are these two frequencies the same?)


.. testcode::

   from xenharmlib import EDOTuning
   from xenharmlib import UpDownNotation
   from xenharmlib import WesternNotation

   edo24 = EDOTuning(24)
   edo31 = EDOTuning(31)
   n_edo31 = UpDownNotation(edo31)
   western = WesternNotation()

   print(western.note('Gb', 4) == western.note('F#', 4))
   print(edo24.pitch(14) == western.note('G', 0))
   print(n_edo31.note('G', 4) < western.note('G', 4))
   print(edo31.pitch(19) <= western.note('G', 0))
   print(n_edo31.note('G', 4) == western.note('G', 4))

.. testoutput::

   True
   True
   True
   False
   False

Equality/Identity also translates to Python's built-in set type. If two
frequency representations are considered equal, combining them in a
Python set will result in a one-element set:

.. testcode::

   from xenharmlib import EDOTuning
   from xenharmlib import WesternNotation

   edo24 = EDOTuning(24)
   western = WesternNotation()

   pitch_a = edo24.pitch(14)
   pitch_b = western.note('G', 0)

   # since the second element is equal to the first 
   # only the first element will be added to the set
   print({pitch_a, pitch_b})

.. testoutput::

   {EDOPitch(14, 24-EDO)}

If the origin contexts have the same equivalency interval constant,
frequency representations can also be tested across contexts with regard
to their equivalency:

.. testcode::

   from xenharmlib import EDOTuning
   from xenharmlib import UpDownNotation
   from xenharmlib import WesternNotation

   edo24 = EDOTuning(24)
   edo31 = EDOTuning(31)
   n_edo31 = UpDownNotation(edo31)
   western = WesternNotation()

   print(edo24.pitch(14).is_equivalent(western.note('G', 5)))
   print(n_edo31.note('G', 4).is_equivalent(western.note('G', 5)))

.. testoutput::

   True
   False

If, however, origin contexts have a different equivalency interval constant,
testing for equivalency will fail, because the operation is undefined:

.. testcode::

   from xenharmlib import EDTuning
   from xenharmlib import FrequencyRatio
   from xenharmlib import WesternNotation

   bohlen_pierce = EDTuning(13, FrequencyRatio(3))
   western = WesternNotation()

   print(bohlen_pierce.eq_interval.frequency_ratio)
   print(western.eq_interval.frequency_ratio)

   try:
       western.note('C', 4).is_equivalent(bohlen_pierce.pitch(4))
   except Exception as exc:
       print(exc)

.. testoutput::

   FrequencyRatio(3)
   FrequencyRatio(2)
   Equivalency can only be tested for notes from tunings with the same equivalency interval


Indices, Pitch Classes and Base Intervals
-------------------------------------------

As we have outlined in the earlier part of this page, every frequency
representation has a "pitch index" that denotes the distance from the
"zero element" of an origin context. Depending on the origin context this
distance can take the form of an integer or a lattice point.

To get an intuition for the concept of the pitch index, we can imagine
the 12-EDO / Western Notation case: Here the zero element is simply
the C0 key, and the pitch index is the number of successive key presses
necessary to reach the pitch in question:

.. image:: _static/images/piano-pitch-indices.png
  :width: 100%
  :alt: An image of a piano with pitch index labels

.. tabs::

   .. tab:: EDO

      .. testcode:: EDOTuning

         from xenharmlib import EDOTuning
         edo31 = EDOTuning(31)

         pitch = edo31.pitch(8)
         print(pitch.pitch_index)

      .. testoutput:: EDOTuning

         8

   .. tab:: Prime Limit

      .. testcode:: PrimeLimitTuning

         from xenharmlib import PrimeLimitTuning

         limit5 = PrimeLimitTuning(5)

         pitch = limit5.vec_pitch((0, 1, 0))
         print(pitch.pitch_index)

      .. testoutput:: PrimeLimitTuning

         LatticePoint(0, 1, 0)

   .. tab:: Western

      .. testcode:: WesternNotation

         from xenharmlib import WesternNotation
         western = WesternNotation()

         A4 = western.note('A', 4)
         print(A4.pitch_index)

      .. testoutput:: WesternNotation

         57

   .. tab:: UpDown

      .. testcode:: UpDownNotation

         from xenharmlib import EDOTuning
         from xenharmlib import UpDownNotation

         edo31 = EDOTuning(31)
         n_edo31 = UpDownNotation(edo31)

         Aup4 = n_edo31.note('^A', 4)
         print(Aup4.pitch_index)

      .. testoutput:: UpDownNotation

         148

Pitch indices can be "sorted into bins" by equivalency. In the above graphic,
you can see that pitch indices 0, 12 and 24 are all Cs. The unified
representative for that bin is called "pitch class index" and is
defined as the lowest positive representative (in case of C: 0). If we
divide the piano by the equivalency interval (in the Western system
the octave), we can describe each key by two parameters: The pitch
class and the base interval index:

.. image:: _static/images/piano-pc-indices.png
  :width: 100%
  :alt: An image of a piano with pitch index labels

.. tabs::

   .. tab:: EDO

      .. testcode:: EDOTuning

         from xenharmlib import EDOTuning
         edo31 = EDOTuning(31)

         pitch = edo31.pitch(39)
         print(pitch.pc_index)
         print(pitch.bi_index)

      .. testoutput:: EDOTuning

         8
         1

   .. tab:: Prime Limit

      .. testcode:: PrimeLimitTuning

         from xenharmlib import PrimeLimitTuning

         limit5 = PrimeLimitTuning(5)

         pitch = limit5.vec_pitch((0, 1, 0))
         print(pitch.pc_index)
         print(pitch.bi_index)

      .. testoutput:: PrimeLimitTuning

         LatticePoint(-1, 1, 0)
         1

   .. tab:: Western

      .. testcode:: WesternNotation

         from xenharmlib import WesternNotation
         western = WesternNotation()

         A4 = western.note('A', 4)
         print(A4.pc_index)
         print(A4.bi_index)

      .. testoutput:: WesternNotation

         9
         4

   .. tab:: UpDown

      .. testcode:: UpDownNotation

         from xenharmlib import EDOTuning
         from xenharmlib import UpDownNotation

         edo31 = EDOTuning(31)
         n_edo31 = UpDownNotation(edo31)

         Aup4 = n_edo31.note('^A', 4)
         print(Aup4.pc_index)
         print(Aup4.bi_index)

      .. testoutput:: UpDownNotation

         24
         4

Transposition
---------------------------------

Frequency representations can be transposed. This is typically done
by providing an :doc:`interval object <prim_interval>` of the same
origin context. One way to create an interval is to use the
:meth:`~xenharmlib.core.freq_repr.FreqRepr.interval` method
of the frequency representation:

.. tabs::

   .. tab:: EDO

      .. testcode:: EDOTuning

         from xenharmlib import EDOTuning
         edo31 = EDOTuning(31)

         p3 = edo31.pitch(3)
         p10 = edo31.pitch(10)
         p18 = edo31.pitch(18)

         interval = p10.interval(p18)
         print(p3.transpose(interval))

      .. testoutput:: EDOTuning

         EDOPitch(11, 31-EDO)

   .. tab:: Prime Limit

      .. testcode:: PrimeLimitTuning

         from xenharmlib import PrimeLimitTuning
         limit5 = PrimeLimitTuning(5)

         pitch_a = limit5.vec_pitch((0, 0, 0))
         pitch_b = limit5.vec_pitch((-2, 0, 1))
         pitch_c = limit5.vec_pitch((-1, 1, 0))

         interval = pitch_a.interval(pitch_b)
         print(pitch_b.transpose(interval))

      .. testoutput:: PrimeLimitTuning

         PrimeLimitPitch(25/16, 5-Limit)

   .. tab:: Western

      .. testcode:: WesternNotation

         from xenharmlib import WesternNotation
         western = WesternNotation()

         D4 = western.note('D', 4)
         Gb4 = western.note('Gb', 4)
         A4 = western.note('A', 4)

         interval = Gb4.interval(A4)
         print(D4.transpose(interval))

      .. testoutput:: WesternNotation

         WesternNote(E#, 4)

   .. tab:: UpDown

      .. testcode:: UpDownNotation

         from xenharmlib import EDOTuning
         from xenharmlib import UpDownNotation

         edo31 = EDOTuning(31)
         n_edo31 = UpDownNotation(edo31)

         Gb4 = n_edo31.note('Gb', 4)
         Aup4 = n_edo31.note('^A', 4)
         Bb4 = n_edo31.note('Bb', 4)

         interval = Gb4.interval(Aup4)
         print(Gb4.transpose(interval))

      .. testoutput:: UpDownNotation

         UpDownNote(^A, 4, 31-EDO)

The :meth:`~xenharmlib.core.freq_repr.FreqRepr.transpose` method also 
accepts a **pitch difference**. A pitch difference is an integer or
lattice point that defines the numeric distance between two frequency
representations. In the case of notations with enharmonic ambiguity,
xenharmlib makes a guess which note should be picked.

.. tabs::

   .. tab:: EDO

      .. testcode:: EDOTuning

         from xenharmlib import EDOTuning
         edo31 = EDOTuning(31)

         p3 = edo31.pitch(3)
         print(p3.transpose(11))

      .. testoutput:: EDOTuning

         EDOPitch(14, 31-EDO)

   .. tab:: Prime Limit

      .. testcode:: PrimeLimitTuning

         from xenharmlib import PrimeLimitTuning
         limit5 = PrimeLimitTuning(5)

         pitch = limit5.pitch(limit5.lattice.point((-2, 0, 1)))
         transposed = pitch.transpose(limit5.lattice.point((-1, 1, 0)))
         print(transposed)

      .. testoutput:: PrimeLimitTuning

         PrimeLimitPitch(15/8, 5-Limit)

   .. tab:: Western

      .. testcode:: WesternNotation

         from xenharmlib import WesternNotation
         western = WesternNotation()

         D4 = western.note('D', 4)
         print(D4.transpose(2))

      .. testoutput:: WesternNotation

         WesternNote(E, 4)

   .. tab:: UpDown

      .. testcode:: UpDownNotation

         from xenharmlib import EDOTuning
         from xenharmlib import UpDownNotation

         edo31 = EDOTuning(31)
         n_edo31 = UpDownNotation(edo31)

         Aup4 = n_edo31.note('^A', 4)
         print(Aup4.transpose(-1))

      .. testoutput:: UpDownNotation

         UpDownNote(A, 4, 31-EDO)

Retuning by Closest Correspondence
--------------------------------------

In the beginning we talked briefly about a family of "bridge functions"
that make a symbolic representation into a numeric one (and vice versa).
We have also shown how to find the closest representative in a tuning or
notation for a given frequency.

If a target context allows approximation to a closest frequency, we can
also directly map a frequency representation of one tuning to another:

.. testcode::

   from xenharmlib import EDOTuning
   from xenharmlib import WesternNotation
   from xenharmlib import UpDownNotation

   edo31 = EDOTuning(31)
   n_edo31 = UpDownNotation(edo31)
   western = WesternNotation()

   retuned_a = western.note('F#', 4).retune_closest(edo31)
   retuned_b = western.note('F#', 4).retune_closest(n_edo31)
   retuned_c = edo31.pitch(18).retune_closest(western)

   print(retuned_a)
   print(retuned_b)
   print(retuned_c)

.. testoutput::

   EDOPitch(139, 31-EDO)
   UpDownNote(F#, 4, 31-EDO)
   WesternNote(G, 0)
