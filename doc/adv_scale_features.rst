Advanced Scale Features
======================================

This section talks about pitch scale / note scale features that have not
been covered in the quickstart. The following features work on both note
scales and pitch scales. For the sake of brevity, we will only give
one example instead of one for each domain.

.. _index_masks_and_partial_scales:

Index Masks and Partial Scales
--------------------------------------

When examining a scale you are often interested in focusing only on fragments
of it. In many cases the :code:`[]`-operator is sufficient to extract the
desired partial scale from the original, e.g. if you want the major septimal
chord scale from a major scale:

.. testcode::

   from xenharmlib import EDOTuning
   from xenharmlib import UpDownNotation
   
   edo12 = EDOTuning(12)
   n_edo12 = UpDownNotation(edo12)
   c_maj_scale = n_edo12.natural_scale()
   c7chord = c_maj_scale[::2]
   print(c7chord)

.. testoutput::

   UpDownNoteScale([C0, E0, G0, B0], 12-EDO)

In other cases the :code:`[]`-operator will not take you far. What if instead
of the major septimal chord scale you want to generate the sus4 chord scale?
The appropriate indices :code:`(0, 3, 4)` don't have a uniform distance, so
they can not be represented by a single slice expression. For reason of this
limitation xenharmlib implements a generalization of a slice called index
mask and the scale method :meth:`~xenharmlib.core.scale.Scale.partial` that
expects an index mask as its parameter:

.. testcode::

   c_sus4_chord = c_maj_scale.partial((0, 3, 4))
   print(c_sus4_chord)

.. testoutput::

   UpDownNoteScale([C0, F0, G0], 12-EDO)

An index mask can be defined in multiple ways. In the above snippet, it is
simply expressed as a tuple of consecutive integers. For big connected
*blocks* of integers this can be tedious, so xenharmlib offers a short
variant with Python's ellipsis symbol (:code:`...`). An ellipsis indicates
that all indices between two values should be part of the mask as well:

.. testcode::

   partial = c_maj_scale.partial((1, ..., 4, 6))

   print(partial)

.. testoutput::

   UpDownNoteScale([D0, E0, F0, G0, B0], 12-EDO)

Similar to Python's slices the first value and the last value of mask
definitions can be omitted entailing the familiar behavior: If a mask
begins with an ellipsis the first value is implicitly 0. If a mask
ends with an ellipsis the last value is the last index of the scale
the mask is applied to:

.. testcode::

   partial1 = c_maj_scale.partial((..., 3, 6))
   partial2 = c_maj_scale.partial((3, ...))

   print(partial1)
   print(partial2)

.. testoutput::

   UpDownNoteScale([C0, D0, E0, F0, B0], 12-EDO)
   UpDownNoteScale([F0, G0, A0, B0], 12-EDO)

Please note that, in contrast to slices, the index after an ellipsis is
**included** in the mask:

.. testcode::

   partial_scale = c_maj_scale.partial((1, ..., 3))
   scale_slice = c_maj_scale[1:3]

   print(partial_scale)
   print(scale_slice)

.. testoutput::

   UpDownNoteScale([D0, E0, F0], 12-EDO)
   UpDownNoteScale([D0, E0], 12-EDO)

For convenience reasons, one-element mask expressions can also be given
without being wrapped by the tuple constructor:

.. testcode::

   partial = c_maj_scale.partial(1)
   print(partial)

.. testoutput::

   UpDownNoteScale([D0], 12-EDO)

If you want to receive the *complement* of a mask you can resort to the
:meth:`~xenharmlib.core.scale.Scale.partial_not` method:

.. testcode::

   scale = c_maj_scale.partial_not((0, 1, 2, 6, ...))
   print(scale)

.. testoutput::

   UpDownNoteScale([F0, G0, A0], 12-EDO)

If you want to receive *both* use the
:meth:`~xenharmlib.core.scale.Scale.partition` method:

.. testcode::

   c_sus4, leftover = c_maj_scale.partition((0, 3, 4))

   print(c_sus4)
   print(leftover)

.. testoutput::

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

.. testcode::

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

.. testoutput::

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

