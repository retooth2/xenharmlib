Interval Sequences
======================================

Interval sequences provide an abstract way to represent musical structures
by storing the relative distances between notes, rather than their absolute
pitches. This allows for the definition of abstract scale and chord types - 
for example, representing the major scale *as such*, rather than as specific
instances like C major or E major.

Creating sequences
-------------------------------

One method for generating an interval sequence is to begin with a scale and
call its :meth:`~xenharmlib.core.scale.Scale.to_interval_seq` method.
Xenharmlib will then calculate the intervals between successive notes
and return the resulting sequence:

.. testcode::

   from xenharmlib import EDOTuning
   from xenharmlib import UpDownNotation
   
   edo12 = EDOTuning(12)
   n_edo12 = UpDownNotation(edo12)
   c_major_scale = n_edo12.pc_scale(
       ['C', 'D', 'E', 'F', 'G', 'A', 'B']
   )
   major_seq = c_major_scale.to_interval_seq()
   print(major_seq)

.. testoutput::

   UpDownNoteIntervalSeq([M2, M2, m2, M2, M2, M2], 12-EDO)

As you can see you obtained a sequence of major and minor seconds in the
order that they occur in the scale. The resulting interval sequence is only
one possible representation of the major scale. Another representation that
is more common in textbooks is derived from a form of the scale where the
series is bookended by two equivalent notes. This scale form can be obtained
by the method :meth:`~xenharmlib.core.scale.PeriodicScale.plusone_normalized`:

.. testcode::

   alt_c_major = c_major_scale.plusone_normalized()
   alt_major_seq = alt_c_major.to_interval_seq()

   print(alt_c_major)
   print(alt_major_seq)

.. testoutput::

   UpDownNoteScale([C0, D0, E0, F0, G0, A0, B0, C1], 12-EDO)
   UpDownNoteIntervalSeq([M2, M2, m2, M2, M2, M2, m2], 12-EDO)

Both methods to define the major scale have their valid usecases. It is
upon you to decide which form fits your task.

Alternatively you can define an interval sequence explicitely by calling
the builder method
:meth:`~xenharmlib.core.origin_context.OriginContext.interval_seq` of
the origin context that takes an iterable of intervals as its argument.

.. testcode::

   m2 = n_edo12.shorthand_interval('m', 2)
   M2 = n_edo12.shorthand_interval('M', 2)
   
   minor_seq = n_edo12.interval_seq(
       [M2, m2, M2, M2, m2, M2]
   )
   print(minor_seq)

.. testoutput::

   UpDownNoteIntervalSeq([M2, m2, M2, M2, m2, M2], 12-EDO)

Interval sequences can also be defined without choosing a notation
by calling :meth:`~xenharmlib.core.origin_context.OriginContext.interval_seq`
directly on the tuning layer with an iterable of pitch intervals
as parameter:

.. testcode::

   major_seq = edo12.interval_seq(
       [
           edo12.diff_interval(2),
           edo12.diff_interval(1),
           edo12.diff_interval(2),
           edo12.diff_interval(2),
           edo12.diff_interval(1),
           edo12.diff_interval(2),
       ]
   )
   print(major_seq)

.. testoutput::

   EDOPitchIntervalSeq([2, 1, 2, 2, 1, 2], 12-EDO)

The same result can also be achieved more concisely through the
:meth:`~xenharmlib.core.origin_context.OriginContext.diff_interval_seq` method:

.. testcode::
   
   major_seq = edo12.diff_interval_seq([2, 1, 2, 2, 1, 2])
   print(major_seq)

.. testoutput::

   EDOPitchIntervalSeq([2, 1, 2, 2, 1, 2], 12-EDO)

Templating and categorization
-------------------------------

The most obvious usage of interval sequences is templating. You can for
example define minor and major chords as interval sequences and then
derive specific chords from it:

.. testcode::

   m3 = n_edo12.shorthand_interval('m', 3)
   M3 = n_edo12.shorthand_interval('M', 3)
   
   minor = n_edo12.interval_seq([M3, m3])
   major = n_edo12.interval_seq([m3, M3])

   D = n_edo12.note('D', 0).scale(major)
   G = n_edo12.note('G', 0).scale(major)
   Am = n_edo12.note('A', 0).scale(minor)
   Em = n_edo12.note('E', 0).scale(minor)

Vice versa, interval sequences can also be used to categorize scale
objects. In the next snippet we devise three functions that generate
abstract definitions of the three types of minor scales for a given
context and an additional identifier function that takes a scale and
returns the type of minor scale.

.. testcode::

   def natural_minor(context):
       return context.pc_scale(
           ['A', 'B', 'C', 'D', 'E', 'F', 'G']
       ).to_interval_seq()

   def harmonic_minor(context):
       return context.pc_scale(
           ['A', 'B', 'C', 'D', 'E', 'F', 'G#']
       ).to_interval_seq()

   def melodic_minor(context):
       return context.pc_scale(
           ['A', 'B', 'C', 'D', 'E', 'F#', 'G#']
       ).to_interval_seq()

   def which_minor(scale):
       seq = scale.to_interval_seq()
       context = scale.origin_context
       if seq == natural_minor(context): return 'natural'
       if seq == harmonic_minor(context): return 'harmonic'
       if seq == melodic_minor(context): return 'melodic'
       raise ValueError('Scale is not minor')

The generic approach allows us to reuse the functions for various
tunings wrapped with UpDownNotation:

.. testcode::

   # 12 EDO
   edo12 = EDOTuning(12)
   n_edo12 = UpDownNotation(edo12)
   what_am_i_12 = n_edo12.pc_scale(
       ['C', 'D', 'Eb', 'F', 'G', 'Ab', 'Bb'] 
   )
   print(which_minor(what_am_i_12))

   # 31 EDO
   edo31 = EDOTuning(31)
   n_edo31 = UpDownNotation(edo31)
   what_am_i_31 = n_edo31.pc_scale(
       ['C', 'D', 'Eb', 'F', 'G', 'Ab', 'B'] 
   )
   print(which_minor(what_am_i_31))

.. testoutput::

   natural
   harmonic

Pattern matching
-------------------------------

Interval sequences can be used to match interval patterns in scales
with the :func:`~xenharmlib.periodic.find_iseq` function from the periodic
extension package.

The following snippet finds all minor triads that can be derived from the
C major scale:

.. testcode::

   from xenharmlib import periodic

   c_major_scale = n_edo12.pc_scale(
       ['C', 'D', 'E', 'F', 'G', 'A', 'B']
   )
   minor_chord = n_edo12.pc_scale(['C', 'Eb', 'G']).to_interval_seq()

   masks = periodic.find_iseq(c_major_scale, minor_chord)

   for mask in masks:
       print(periodic.partial(c_major_scale, mask))

.. testoutput::

   UpDownNoteScale([D0, F0, A0], 12-EDO)
   UpDownNoteScale([E0, G0, B0], 12-EDO)
   UpDownNoteScale([A0, C1, E1], 12-EDO)
