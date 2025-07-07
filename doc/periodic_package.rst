.. _periodic_ext:

The :code:`periodic` Package
===============================

The :code:`periodic` package implements utilities for periodic extensions
of scales. A periodic extension treats the scale object as a representation
of a periodically repeating series, meaning that

   :math:`D_4\ \  E_4\ \  F_4\ \  G_4\ \  A_4\ \  B_4\ \  C_5`

represents the infinitely repeating series

   :math:`...\ \  G_3\ \  A_3\ \  B_3\ \  C_4\ \  \mathbfit{D_4\ \  E_4\ \  F_4\ \  G_4\ \  A_4\ \  B_4\ \  C_5}\ \  D_5\ \  E_5\ \  F_5\ \  ...`

Scale objects must be period normalized to be elligible for the package,
meaning the included elements must inhabit a single base interval.
If a scale is not period normalized (for example if it was generated to
represent a chord with compound intervals), it can be transformed easily:

.. testcode::

   from xenharmlib import EDOTuning
   from xenharmlib import UpDownNotation

   edo12 = EDOTuning(12)
   n_edo12 = UpDownNotation(edo12)

   c_maj9 = n_edo12.pc_scale(
       ['C', 'E', 'G', 'B', 'D']
   )
   print(c_maj9)

   normalized = c_maj9.period_normalized()
   print(normalized)

.. testoutput::

   UpDownNoteScale([C0, E0, G0, B0, D1], 12-EDO)
   UpDownNoteScale([C0, D0, E0, G0, B0], 12-EDO)

.. note::

   Examples in this documentation are given for the notation
   layer however the functions in periodic also work for the
   tuning/pitch layer


Periodic Indexing
----------------------------------------------------------------------

From the scale object itself you are already familiar with the :code:`[]`
operator which returns a scale element at the desired position:

.. testcode::

   from xenharmlib import EDOTuning
   from xenharmlib import UpDownNotation
   from xenharmlib import periodic

   edo12 = EDOTuning(12)
   n_edo12 = UpDownNotation(edo12)

   c_maj = n_edo12.pc_scale(
       ['C', 'D', 'E', 'F', 'G', 'A', 'B']
   )

   print(c_maj[0])
   print(c_maj[2])

.. testoutput::

   UpDownNote(C, 0, 12-EDO)
   UpDownNote(E, 0, 12-EDO)

However the :code:`[]` operator only retrieves direct elements of the scale
object, so "overshooting" the index will result in an error:

.. testcode::

   from xenharmlib import EDOTuning
   from xenharmlib import UpDownNotation

   edo12 = EDOTuning(12)
   n_edo12 = UpDownNotation(edo12)

   c_maj = n_edo12.pc_scale(
       ['C', 'D', 'E', 'F', 'G', 'A', 'B']
   )

   try:
       note = c_maj[7]
   except Exception as exc:
       print(exc)

.. testoutput::

   list index out of range

Since in :code:`periodic` the scale only represents a section of an infinite
series, indices and index-based parameters have a different semantic. Because
we are talking about an infinite series, each element in the series must
be attributed to a single integer index. Consequently indices in the
package do not have lower or upper bounds.

The equivalent function of the :code:`[]` operator is the package function
:func:`~xenharmlib.periodic.scale_element`. Because here the index points to an
element in an infinite series, "overshooting" is not possible. If an index
greater than the last scale index is provided, the function will simply
"walk along" the infinite series until it reaches the index and then return
the associated element:

.. testcode::

   from xenharmlib import periodic

   for i in range(0, 9):
       note = periodic.scale_element(c_maj, i)
       print(note)

.. testoutput::

   UpDownNote(C, 0, 12-EDO)
   UpDownNote(D, 0, 12-EDO)
   UpDownNote(E, 0, 12-EDO)
   UpDownNote(F, 0, 12-EDO)
   UpDownNote(G, 0, 12-EDO)
   UpDownNote(A, 0, 12-EDO)
   UpDownNote(B, 0, 12-EDO)
   UpDownNote(C, 1, 12-EDO)
   UpDownNote(D, 1, 12-EDO)

The periodic index is centered, so the 0 indices of both scale index and
periodic index align, meaning that for indices :code:`0, ..., len(scale) - 1`
the :code:`[]` operator and :func:`~xenharmlib.periodic.scale_element` will
result in the same elements:

.. testcode::

   from xenharmlib import periodic

   for i in range(0, len(c_maj)):
       note_a = c_maj[i]
       note_b = periodic.scale_element(c_maj, i)
       assert note_a == note_b

Please note the subtle difference in the result for negative indices.
While the :code:`[]` operator acts on a negative index in the standard
python way (counting from the right of the finite sequence), the
:func:`~xenharmlib.periodic.scale_element` function retrieves an element
from the section of the infinite series that is *left* to the scale:

.. testcode::

   from xenharmlib import periodic

   note = c_maj[-1]
   print(note)

   note = periodic.scale_element(c_maj, -1)
   print(note)

.. testoutput::

   UpDownNote(B, 0, 12-EDO)
   UpDownNote(B, -1, 12-EDO)

The counterpart of :func:`~xenharmlib.periodic.scale_element` (expecting
an index, returning a note) is :func:`~xenharmlib.periodic.index` expecting
a note and returning the index the note was found at in the infinite series:

.. testcode::

   from xenharmlib import periodic

   c2 = n_edo12.note('C', 2)
   index = periodic.index(c_maj, c2)
   print(index)

.. testoutput::

   14

If the element does not exist in the infinite series, a ValueError is thrown
(a behavior familiar from the index method of python's List type):

.. testcode::

   c_sharp = n_edo12.note('C#', 4)

   try:
       partial_scale = periodic.index(c_maj, c_sharp)
   except Exception as exc:
       print(exc)

.. testoutput::

   UpDownNote(C#, 4, 12-EDO) was not found in periodic extension of the scale

Periodic Index Masks
----------------------------------------------------------------------

With :func:`~xenharmlib.periodic.partial` the package allows partial
scale extraction, similar to the
:ref:`native scale method<index_masks_and_partial_scales>`.
Because indices do not relate to a finite scale, but to the infinite
periodic extension, index masks given to :func:`~xenharmlib.periodic.partial`
have a couple of differences to their finite counterpart. One key difference
is that indices in the mask don't have upper or lower bounds. They only need
to be consecutive:

.. testcode::

   from xenharmlib import periodic

   partial_scale = periodic.partial(c_maj, (5, ..., 8))
   print(partial_scale)

.. testoutput::

   UpDownNoteScale([A0, B0, C1, D1], 12-EDO)

In contrast to index masks used in the native scale methods periodic index
masks can therefor also include negative numbers:

.. testcode::

   from xenharmlib import periodic

   partial_scale = periodic.partial(c_maj, (-2, -1, 8))
   print(partial_scale)

.. testoutput::

   UpDownNoteScale([A-1, B-1, D1], 12-EDO)

Because the mask is operating on an infinite series with the purpose
of extracting a finite scale, ellipsis symbols (:code:`...`) are not
allowed on the first or last position of an infinite series index mask:

.. testcode::

   try:
       partial_scale = periodic.partial(c_maj, (..., 8))
   except Exception as exc:
       print(exc)

.. testoutput::

   Ellipsis is not allowed on edges of infinite series mask

For the same reason the package does **not** implement variants of
:func:`~xenharmlib.core.scale.PeriodicScale.partial_not` or
:func:`~xenharmlib.core.scale.PeriodicScale.partition`. It does
however implement :func:`~xenharmlib.periodic.index_mask` which
takes a partial scale and returns the periodic index mask:

.. testcode::

   from xenharmlib import periodic

   Bdim = n_edo12.pc_scale(['B', 'D', 'F'])
   mask = periodic.index_mask(c_maj, Bdim)
   print(mask)

.. testoutput::

   (6, 8, 10)

Periodic Cutouts
-----------------------------------------------------------------

When composing, you often want to identify which chords of a particular
structure can be derived from a scale. For instance, the following I-III-V
chords can be formed from the C major scale:

.. list-table::
   :widths: 50 50
   :header-rows: 1

   * - Notes
     - Chord name
   * - :math:`C-E-G`
     - C major
   * - :math:`D-F-A`
     - D minor
   * - :math:`E-G-B`
     - E minor
   * - :math:`F-A-C`
     - F major
   * - :math:`G-B-D`
     - G major
   * - :math:`A-C-E`
     - A minor
   * - :math:`B-D-F`
     - B diminished

The :func:`~xenharmlib.periodic.cutouts` generator takes a periodic index
mask and a scale, sliding the mask from left to right and yielding all
partials until it reaches a partial equivalent to the first.

.. testcode::

   from xenharmlib import EDOTuning
   from xenharmlib import UpDownNotation
   from xenharmlib import periodic

   edo12 = EDOTuning(12)
   n_edo12 = UpDownNotation(edo12)

   c_maj = n_edo12.pc_scale(
       ['C', 'D', 'E', 'F', 'G', 'A', 'B']
   )
   
   for tetrad_scale in periodic.cutouts(c_maj, (0, 2, 4)):
       print(tetrad_scale)

.. testoutput::

   UpDownNoteScale([C0, E0, G0], 12-EDO)
   UpDownNoteScale([D0, F0, A0], 12-EDO)
   UpDownNoteScale([E0, G0, B0], 12-EDO)
   UpDownNoteScale([F0, A0, C1], 12-EDO)
   UpDownNoteScale([G0, B0, D1], 12-EDO)
   UpDownNoteScale([A0, C1, E1], 12-EDO)
   UpDownNoteScale([B0, D1, F1], 12-EDO)

If you want the seven chords (I-III-V-VII) you choose the :code:`(0, 2, 4, 6)`
index mask:

.. testcode::
   
   for tetrad_scale in periodic.cutouts(c_maj, (0, 2, 4, 6)):
       print(tetrad_scale)

.. testoutput::

   UpDownNoteScale([C0, E0, G0, B0], 12-EDO)
   UpDownNoteScale([D0, F0, A0, C1], 12-EDO)
   UpDownNoteScale([E0, G0, B0, D1], 12-EDO)
   UpDownNoteScale([F0, A0, C1, E1], 12-EDO)
   UpDownNoteScale([G0, B0, D1, F1], 12-EDO)
   UpDownNoteScale([A0, C1, E1, G1], 12-EDO)
   UpDownNoteScale([B0, D1, F1, A1], 12-EDO)

You can also choose chords with a structure bigger than the scale itself
for example chords with a ninth:

.. testcode::
   
   for tetrad_scale in periodic.cutouts(c_maj, (0, 2, 4, 6, 8)):
       print(tetrad_scale)

.. testoutput::

   UpDownNoteScale([C0, E0, G0, B0, D1], 12-EDO)
   UpDownNoteScale([D0, F0, A0, C1, E1], 12-EDO)
   UpDownNoteScale([E0, G0, B0, D1, F1], 12-EDO)
   UpDownNoteScale([F0, A0, C1, E1, G1], 12-EDO)
   UpDownNoteScale([G0, B0, D1, F1, A1], 12-EDO)
   UpDownNoteScale([A0, C1, E1, G1, B1], 12-EDO)
   UpDownNoteScale([B0, D1, F1, A1, C2], 12-EDO)

You can also use :func:`~xenharmlib.periodic.cutouts` for applying a gapless
sliding window over the periodic extension, so a possible way to write a
function generating all modes of a scale is this:

.. testcode::

   def gen_modes(scale):
       yield from periodic.cutouts(scale, (0, ..., len(scale) - 1))

   for mode in gen_modes(c_maj):
       print(mode)

.. testoutput::

   UpDownNoteScale([C0, D0, E0, F0, G0, A0, B0], 12-EDO)
   UpDownNoteScale([D0, E0, F0, G0, A0, B0, C1], 12-EDO)
   UpDownNoteScale([E0, F0, G0, A0, B0, C1, D1], 12-EDO)
   UpDownNoteScale([F0, G0, A0, B0, C1, D1, E1], 12-EDO)
   UpDownNoteScale([G0, A0, B0, C1, D1, E1, F1], 12-EDO)
   UpDownNoteScale([A0, B0, C1, D1, E1, F1, G1], 12-EDO)
   UpDownNoteScale([B0, C1, D1, E1, F1, G1, A1], 12-EDO)


Modulation Connectors
-----------------------------------------------------------------

If you are composing a chord progression in a specific key and want to
modulate to another key you typically want to find chords that are shared
between the two different keys so they be used as pivot from one key to
another. The :func:`~xenharmlib.periodic.mod_connectors` function makes
this task a piece of cake. It expects two scales as parameters and a
cutouts structure and finds equivalent partial scales between the two
scales:

.. testcode::

   from xenharmlib import periodic

   c_maj = n_edo12.pc_scale(
       ['C', 'D', 'E', 'F', 'G', 'A', 'B']
   )

   g_min = n_edo12.pc_scale(
       ['G', 'A', 'Bb', 'C', 'D', 'Eb', 'F']
   )

   connectors = periodic.mod_connectors(c_maj, g_min, (0, 2, 4))

   for connector in connectors:
       print(connector)

.. testoutput::

   UpDownNoteScale([D0, F0, A0], 12-EDO)
   UpDownNoteScale([F0, A0, C1], 12-EDO)


Scalar Transposition
-----------------------------------------------------------------

The function :func:`~xenharmlib.periodic.scalar_transpose` transposes
a note or a scale *along* the infinite periodic series, meaning if a
note is transposed by 3 it is moved 3 steps upwards *on the scale*:

.. testcode::

   from xenharmlib import periodic

   c_maj = n_edo12.pc_scale(
       ['C', 'D', 'E', 'F', 'G', 'A', 'B']
   )
   B2 = n_edo12.note('B', 2)

   transposed = periodic.scalar_transpose(c_maj, B2, 3)
   print(transposed)

.. testoutput::

   UpDownNote(E, 3, 12-EDO)

Likewise if a scale is provided and the step difference is 5 each note
of the scale will be transposed 5 scale steps in the resulting scale:

.. testcode::

   from xenharmlib import periodic

   c_triad = n_edo12.pc_scale(['C', 'E', 'G'])
   transposed = periodic.scalar_transpose(c_maj, c_triad, 5)
   print(transposed)

.. testoutput::

   UpDownNoteScale([A0, C1, E1], 12-EDO)


Pair Iteration
-----------------------------------------------------------------

The :func:`~xenharmlib.periodic.pairs` function iterates over all pairs
of scale elements until a pair equivalent to the first pair is reached.
By default the function will iterate over successive elements, however
a custom distance can be given as second parameter.

.. testcode::

   from xenharmlib import periodic
   
   for note_a, note_b in periodic.pairs(c_maj):
       print(note_a, '---->', note_b)

.. testoutput::

   UpDownNote(C, 0, 12-EDO) ----> UpDownNote(D, 0, 12-EDO)
   UpDownNote(D, 0, 12-EDO) ----> UpDownNote(E, 0, 12-EDO)
   UpDownNote(E, 0, 12-EDO) ----> UpDownNote(F, 0, 12-EDO)
   UpDownNote(F, 0, 12-EDO) ----> UpDownNote(G, 0, 12-EDO)
   UpDownNote(G, 0, 12-EDO) ----> UpDownNote(A, 0, 12-EDO)
   UpDownNote(A, 0, 12-EDO) ----> UpDownNote(B, 0, 12-EDO)
   UpDownNote(B, 0, 12-EDO) ----> UpDownNote(C, 1, 12-EDO)


Deriving Specific From Generic Intervals
-----------------------------------------------------------------

A *generic interval* in regards to a scale is defined by two scale
indices, for example 0 and 3. In regards to the western C4 major
scale the generic interval (0, 3) is the interval between C4
(scale index 0) and F4 (scale index 3). The related *specific
interval* is defined by the absolute pitch indices, in our
example 48 for C4 and 53 for F4.

The :func:`~xenharmlib.periodic.spec_interval` function expects
two scale index parameters (source and target index) and returns
the related specific interval. The scale indices refer to the
periodic extension of the scale and behave like outlined in
the :ref:`Periodic Indexing` section.

.. testcode::

   from xenharmlib import periodic
   
   interval = periodic.spec_interval(c_maj, 6, 7)
   print(interval)

.. testoutput::

   UpDownNoteInterval(m, 2, 12-EDO)


Interval Sequence Pattern Matching
-----------------------------------------------------------------

The function :func:`~xenharmlib.periodic.find_iseq` provides
a way to find interval sequences in the periodic extension of the
scale. Given an interval sequence it returns all occurences of the
sequence as a list of infinite series index masks.

Let's suppose you want to find all minor chords in a scale. With
interval sequence pattern matching you can define a suitable
function like this:

.. testcode::

   def find_minor_chords(scale):
       notation = scale.notation
       seq = notation.interval_seq(
           [
              notation.shorthand_interval('m', 3),
              notation.shorthand_interval('M', 3),
           ]
       )
       return periodic.find_iseq(scale, seq)

   masks = find_minor_chords(c_maj)

   for mask in masks:
       print(mask)
       print(periodic.partial(c_maj, mask))

.. testoutput::

   (1, 3, 5)
   UpDownNoteScale([D0, F0, A0], 12-EDO)
   (2, 4, 6)
   UpDownNoteScale([E0, G0, B0], 12-EDO)
   (5, 7, 9)
   UpDownNoteScale([A0, C1, E1], 12-EDO)


