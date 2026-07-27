Introduction
===============================================

Harmonic primitives in xenharmlib are objects representing basic harmonic
structures. They are created from and always relate to an **origin context**,
i.e., a musical system that defines the *meaning* of their symbolic expression
(e.g. a G#-4 has a different frequency in the context of 31-EDO than in
the context of 12-EDO)

Origin Contexts
----------------------------

An origin context can take on the form of a **tuning** (a representation
system built on integers or lattice points) or a **notation** representing
musical objects with strings (like Eb-4). Generally speaking, notations
are symbolic *wrappers* around tunings, meaning each primitive
created from a notation can be reduced to an equivalent tuning
primitive. The reverse is also true, however, with some restrictions:
Because most of the time there are multiple symbolic representations
for the same numeric pitch (for example, in Western tuning Eb and D#
represent the pitch index), xenharmlib must make a guess on what symbolic
representation to choose when translating a harmonic primitive from a
tuning to a notation.

Harmonic primitives are built from *builder methods* of the origin context.
These builder methods share (for the most part) an interface across contexts,
making it possible to make analytical tools that are *agnostic* to the
origin context, i.e., allowing to create one function that works on
objects built from an EDO Tuning *as well as* on objects originating
from an UpDownNotation context.

The smallest unit of representation, from which all harmonic primitives can be
derived, is the frequency representation, which in tuning contexts is called
*pitch* and in notation contexts *note*.

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

         G0 = limit5.pitch(limit5.lattice.point((-1, 1, 0)))
         print(G0.frequency.to_float())

      .. testoutput:: PrimeLimitTuning

         24.52739674693112

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

         Abb4 = n_edo31.note('Abb', 4)
         print(Abb4.frequency.to_float())

      .. testoutput:: UpDownNotation

         400.1127908225046

From these "smallest" units other harmonic primitives can be built, which we
call *second-order* harmonic primitives:

* A structure of 2 frequency representations is called an **interval**
* A sorted list of unique frequency representations is called a **scale**
* A succession of multiple frequency representations is called a **sequence**

On top of these we have what we call *third-order* harmonic primitives:

* A structure which represents the intervals between each *successive*
  frequency representation in a scale or sequence is called an
  **interval sequence**.
* A structure which represents intervals relating the elements of a
  scale or sequence to a fixed tonic pitch is called an **interval fan**

Third-order harmonic primitives allow generalizations like "major scale"
(with the root note being left undefined) and play a big role for utilities
dealing with structures in the context of transformation theory.

Every primitive refers to its origin context by the :attr:`origin_context`
property. Together with the unified interface of builder methods, this can
be leveraged to create generalized utilities. Observe, for example, how the
following function can be applied to sequences of all origins:

.. testcode::

   from xenharmlib import periodic

   def steps_and_skips(sequence):

       context = sequence.origin_context
       scale = context.scale(sequence).period_normalized()
       result = []

       for a, b in zip(sequence, sequence[1:]):

           i_a = periodic.index(scale, a)
           i_b = periodic.index(scale, b)

           if abs(i_a - i_b) == 1:
               result.append('step')
           if abs(i_a - i_b) > 1:
               result.append('skip')
           if abs(i_a - i_b) == 0:
               result.append('-')

       return result

The function transforms notes in a sequence into a period-normalized scale
and then uses that scale to calculate scale degrees of movement in the
sequence, allowing us to differentiate between steps and skips in the
sequence, regardless of sequence origin:

.. tabs::

   .. tab:: EDO

      .. testcode::

         from xenharmlib import EDOTuning
         edo31 = EDOTuning(31)

         seq = edo31.index_seq([0, 5, 10, 0, 10])
         result = steps_and_skips(seq)
         print(result)

      .. testoutput::

         ['step', 'step', 'skip', 'skip']

   .. tab:: Prime Limit

      .. testcode::

         from xenharmlib import PrimeLimitTuning
         limit5 = PrimeLimitTuning(5)

         seq = limit5.rs_seq(['1/1', '9/8', '5/4', '1/1', '3/2'])
         result = steps_and_skips(seq)
         print(result)

      .. testoutput::

         ['step', 'step', 'skip', 'skip']

   .. tab:: Western

      .. testcode::

         from xenharmlib import WesternNotation
         western = WesternNotation()

         C4 = western.note('C', 4)
         D4 = western.note('D', 4)
         E4 = western.note('E', 4)

         seq = western.seq([C4, D4, E4, C4, E4])
         result = steps_and_skips(seq)
         print(result)

      .. testoutput::

         ['step', 'step', 'skip', 'skip']

   .. tab:: UpDown

      .. testcode::

         from xenharmlib import EDOTuning
         from xenharmlib import UpDownNotation

         edo31 = EDOTuning(31)
         n_edo31 = UpDownNotation(edo31)

         C4 = n_edo31.note('C', 4)
         Dbb4 = n_edo31.note('Dbb', 4)
         Eup4 = n_edo31.note('^E', 4)

         seq = n_edo31.seq([C4, Dbb4, Eup4, C4, Eup4])
         result = steps_and_skips(seq)
         print(result)

      .. testoutput::

         ['step', 'step', 'skip', 'skip']

Constants
------------------------------------------------

Origin contexts define various constants that give necessary definitions to
the methods of harmonic primitives and utilities. We will start with the
:attr:`~xenharmlib.core.origin_context.OriginContext.eq_interval`
property that returns an interval object defining the equivalency
interval:

.. tabs::

   .. tab:: EDO

      .. testcode::

         from xenharmlib import EDOTuning

         edo31 = EDOTuning(31)
         print(edo31.eq_interval)

      .. testoutput::

         EDOPitchInterval(31, 31-EDO)

   .. tab:: Prime Limit

      .. testcode::

         from xenharmlib import PrimeLimitTuning

         limit5 = PrimeLimitTuning(5)
         print(limit5.eq_interval)

      .. testoutput::

         PrimeLimitPitchInterval(2, 5-Limit)

   .. tab:: Western

      .. testcode:: WesternNotation

         from xenharmlib import WesternNotation

         western = WesternNotation()
         print(western.eq_interval)

      .. testoutput:: WesternNotation

         WesternNoteInterval(P, 8)

   .. tab:: UpDown

      .. testcode:: UpDownNotation

         from xenharmlib import EDOTuning
         from xenharmlib import UpDownNotation

         edo31 = EDOTuning(31)
         n_edo31 = UpDownNotation(edo31)

         print(n_edo31.eq_interval)

      .. testoutput:: UpDownNotation

         UpDownNoteInterval(P, 8, 31-EDO)

Especially in notations where there can be multiple enharmonic ways to
define the equivalency interval, the constant returns the definitive
object necessary to do calculations, so e.g. the method transforming
a compound interval into a simple one does not only return an interval
with the correct frequency ratio, but also with the correct spelling.

In the same way, the
:attr:`~xenharmlib.core.origin_context.OriginContext.unison_interval`
constant provides the "neutral element" of the interval space. The
unison interval is for example the reference point for xenharmlib
to find out if an interval is descending or ascending.

.. tabs::

   .. tab:: EDO

      .. testcode::

         from xenharmlib import EDOTuning

         edo31 = EDOTuning(31)
         print(edo31.unison_interval)

      .. testoutput::

         EDOPitchInterval(0, 31-EDO)

   .. tab:: Prime Limit

      .. testcode::

         from xenharmlib import PrimeLimitTuning

         limit5 = PrimeLimitTuning(5)
         print(limit5.unison_interval)

      .. testoutput::

         PrimeLimitPitchInterval(1, 5-Limit)

   .. tab:: Western

      .. testcode:: WesternNotation

         from xenharmlib import WesternNotation

         western = WesternNotation()
         print(western.unison_interval)

      .. testoutput:: WesternNotation

         WesternNoteInterval(P, 1)

   .. tab:: UpDown

      .. testcode:: UpDownNotation

         from xenharmlib import EDOTuning
         from xenharmlib import UpDownNotation

         edo31 = EDOTuning(31)
         n_edo31 = UpDownNotation(edo31)

         print(n_edo31.unison_interval)

      .. testoutput:: UpDownNotation

         UpDownNoteInterval(P, 1, 31-EDO)


The :attr:`~xenharmlib.core.origin_context.OriginContext.zero_element`
constant defines the frequency representation that is considered
the reference element for transposing harmonic primitives to their
zero-normalized form:

.. tabs::

   .. tab:: EDO

      .. testcode::

         from xenharmlib import EDOTuning

         edo31 = EDOTuning(31)
         print(edo31.zero_element)

      .. testoutput::

         EDOPitch(0, 31-EDO)

   .. tab:: Prime Limit

      .. testcode::

         from xenharmlib import PrimeLimitTuning

         limit5 = PrimeLimitTuning(5)
         print(limit5.zero_element)

      .. testoutput::

         PrimeLimitPitch(1, 5-Limit)

   .. tab:: Western

      .. testcode:: WesternNotation

         from xenharmlib import WesternNotation

         western = WesternNotation()
         print(western.zero_element)

      .. testoutput:: WesternNotation

         WesternNote(C, 0)

   .. tab:: UpDown

      .. testcode:: UpDownNotation

         from xenharmlib import EDOTuning
         from xenharmlib import UpDownNotation

         edo31 = EDOTuning(31)
         n_edo31 = UpDownNotation(edo31)

         print(n_edo31.zero_element)

      .. testoutput:: UpDownNotation

         UpDownNote(C, 0, 31-EDO)

Since xenharmlib supports both integer and lattice point indexing,
reference points for different indexing strategies are also
given as constants, namely
:attr:`~xenharmlib.core.origin_context.OriginContext.zero_index`
(the pitch index of the zero element), and
:attr:`~xenharmlib.core.origin_context.OriginContext.unison_diff`
(the pitch difference of the unison interval), and
:attr:`~xenharmlib.core.origin_context.OriginContext.eq_diff`
(the pitch difference of the equivalency interval)

.. tabs::

   .. tab:: EDO

      .. testcode:: EDOTuning

         from xenharmlib import EDOTuning

         edo31 = EDOTuning(31)
         print(edo31.zero_index)
         print(edo31.unison_diff)
         print(edo31.eq_diff)

      .. testoutput:: EDOTuning

         0
         0
         31

   .. tab:: Prime Limit

      .. testcode:: PrimeLimitTuning

         from xenharmlib import PrimeLimitTuning

         limit5 = PrimeLimitTuning(5)
         print(limit5.zero_index)
         print(limit5.unison_diff)
         print(limit5.eq_diff)

      .. testoutput:: PrimeLimitTuning

         LatticePoint(0, 0, 0)
         LatticePoint(0, 0, 0)
         LatticePoint(1, 0, 0)

   .. tab:: Western

      .. testcode:: WesternNotation

         from xenharmlib import WesternNotation

         western = WesternNotation()
         print(western.zero_index)
         print(western.unison_diff)
         print(western.eq_diff)

      .. testoutput:: WesternNotation

         0
         0
         12

   .. tab:: UpDown

      .. testcode:: UpDownNotation

         from xenharmlib import EDOTuning
         from xenharmlib import UpDownNotation

         edo31 = EDOTuning(31)
         n_edo31 = UpDownNotation(edo31)

         print(n_edo31.zero_index)
         print(n_edo31.unison_diff)
         print(n_edo31.eq_diff)

      .. testoutput:: UpDownNotation

         0
         0
         31
