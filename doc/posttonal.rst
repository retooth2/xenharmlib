Posttonal Basics
===============================

Pitch Class Sets and Scales
------------------------------------

In textbooks on post-tonal theory, the definition of pitch class sets is often
ambiguous. In *some* applications a pitch class set is considered unordered.
In others (for example in normal form calculation) the order is vital.
To account for both cases pitch class sets in xenharmlib are always
*lists* of unique pitch classes.

Xenharmlib implements pitch class set arithmetic as a byproduct of scale
arithmetic. Every scale object in xenharmlib has a
:attr:`~xenharmlib.core.pitch_scale.PeriodicPitchScale.pc_indices` property
that lists pitch classes in the order they appear in the scale:

.. testcode::

   from xenharmlib import EDOTuning

   edo12 = EDOTuning(12)

   scale = edo12.index_scale(
       [2, 4, 7, 9, 11, 13, 16, 18]
   )
   print(scale.pc_indices)

.. testoutput::

   [2, 4, 7, 9, 11, 1, 4, 6]

However, :attr:`~xenharmlib.core.pitch_scale.PeriodicPitchScale.pc_indices`
does not always return a collection of *unique* elements. For example,
in the list above, pitch class 4 appears twice. This is due to the
flexibility of xenharmlib's scale definition. Unlike many traditional
textbook definitions, the scale object permits multiple equivalent
(albeit not identical) pitches to coexist and also allows pitches
to span multiple octaves. See the following diagram for illustration:

.. image:: _static/images/scale-open-necklace-1.png
  :width: 100%
  :alt: A diagram showing a chain of pitches

One way to ensure that the elements are unique is calling the 
:attr:`~xenharmlib.core.scale.PeriodicScale.pcs_normalized`
method of the scale:

.. testcode::

   pcsn_scale = scale.pcs_normalized()
   print(pcsn_scale.pc_indices)

.. testoutput::

   [1, 2, 4, 6, 7, 9, 11]

The normalization transposes every pitch into the first base interval.
This has two effects: First, it guarantees the uniqueness of the pitch classes
in the list. Secondly, it guarantees that pitch classes occur in a strictly
ascending order.

.. image:: _static/images/scale-open-necklace-pcs-normalized-1.png
  :width: 100%
  :alt: A diagram showing the same chain of pitches after pcs normalization

However, this kind of transformation is not always desirable, as it
eliminates the mode information of a scale (for instance, the C major
and A minor scales result in the same scale when pcs normalized). A
better way to make the list of pitch classes unique is period
normalization which transposes every pitch into the base interval
spanned by the root pitch of the original scale (highlighted in red below):

.. image:: _static/images/scale-open-necklace-relative-bi-1.png
  :width: 100%
  :alt: A diagram showing the same chain of pitches with the relative base interval marked red

This transformation can be executed on the scale like this:

.. testcode::

   pn_scale = scale.period_normalized()
   print(pn_scale.pc_indices)

.. testoutput::

   [2, 4, 6, 7, 9, 11, 1]


.. image:: _static/images/scale-open-necklace-period-normalized-1.png
  :width: 100%
  :alt: A diagram showing the same chain of pitches after period normalization

Period normalization guarantees uniqueness, but not that pitch classes are
in ascending order (as you can see from the jump from 11 to 1). They
guarantee however that at most one such violation of the order occurs.

If visualized as a closed necklace the resulting pitch class set of both
normalizations share the same geometric form, however the starting point
(highlighted in green) is different:

.. image:: _static/images/scale-closed-necklace-pcs-vs-period-1.png
  :width: 100%
  :alt: A diagram showing the difference between pcs and period normal form


Transposition
------------------------------------

Period normalized scales have a nice quality to it: They form a closed
subset of scales in regard to transposition, meaning that every time
you transpose a period-normalized scale your result will be another
period normalized scale:

.. testcode::

   pn_scale_t3 = pn_scale.transpose(3)
   print(pn_scale_t3.pc_indices)

.. testoutput::

   [5, 7, 9, 10, 0, 2, 4]

From the viewpoint of the
:attr:`~xenharmlib.core.pitch_scale.PeriodicPitchScale.pc_indices` property a
transposition is an addition mod period size (mod 12 in our example).
In the closed necklace visualization, it amounts to a rotation of the
necklace:

.. image:: _static/images/scale-closed-necklace-transposed-1.png
  :width: 100%
  :alt: A necklace diagram showing a transposition

To learn more about scale normalization methods read the
:ref:`section on normalization <scale_normalizations>`
in the Advanced Scale Guide.

We now have established how to apply the post-tonal :math:`T_n` operation
on a pitch class set by using scale operations and can now move on to the
:math:`I` (inversion) operation.

Inversion
------------------------------------

Xenharmlib implements a generalization of the :math:`I` operation, called
:meth:`~xenharmlib.core.scale.Scale.reflection`, that reflects the scale
around an arbitrary axis pitch. Without any parameters it reflects around
the zero element of the origin context (pitch 0 in tunings, C0 in
UpDownNotation).

.. testcode::

   scale = edo12.index_scale(
       [1, 2, 4, 5, 6, 7, 9, 11]
   )
   refl = scale.reflection()
   print(refl)

.. testoutput::

   EDOPitchScale([-11, -9, -7, -6, -5, -4, -2, -1], 12-EDO)

Reflection is most easily understood visually. In the graphic below,
the source and target pitches are represented by the same color.
As shown, reflection is accomplished by calculating the interval
from the reflection point (outlined in red) and applying the
negative of that interval back to the reflection point:

.. image:: _static/images/scale-open-necklace-inverted-1.png
  :width: 100%
  :alt: A diagram showing a reflection along the 0-6 axis

From the perspective of the
:attr:`~xenharmlib.core.pitch_scale.PeriodicPitchScale.pc_indices` property
invoking :meth:`~xenharmlib.core.scale.Scale.reflection` without
a parameter applies the :math:`I` operation on the pitch class set.

.. testcode::

   scale = edo12.index_scale(
       [1, 2, 4, 5, 6, 7, 9, 11]
   )
   refl = scale.reflection()
   print(refl.pc_indices)

.. testoutput::

   [1, 3, 5, 6, 7, 8, 10, 11]

On the closed necklace graph of the pitch class set, this operation is
equivalent to flipping the necklace across the horizontal line passing
through 0.

.. image:: _static/images/scale-closed-necklace-inverted-1.png
  :width: 100%
  :alt: A diagram showing a reflection of a necklace along the 0-6 axis

If another pitch should serve as the reflection axis it can be provided
as an argument:

.. testcode::

   scale = edo12.index_scale(
       [1, 2, 4, 5, 6, 7, 9, 11]
   )
   refl = scale.reflection(
       edo12.pitch(6)
   )
   print(refl)

.. testoutput::

   EDOPitchScale([1, 3, 5, 6, 7, 8, 10, 11], 12-EDO)

.. image:: _static/images/scale-open-necklace-inverted-alt-center-1.png
  :width: 100%
  :alt: A diagram showing a reflection with a different axis

.. _posttonal_nf_pf:

Normal Form
------------------------------------

The normal form transforms all scales that are related by rotation 
into a single representative, more formally for two scales :math:`S_1`
:math:`S_2`, rotation function :math:`R` and normal form :math:`N` it
holds that:

.. math::

   \exists i (S_1 = R^i(S_2)) \leftrightarrow N(S_1) = N(S_2)

In more concrete terms this means that all modes of a scale and all
inversions of a chord have the same normal form, e.g. "C Major" and 
"D Dorian" have the same normal form or the "C4-E4-G4" chord has the
same normal form as its inversion "E4-G4-C5".

There are several ways to define the normal form, with the most
well-known being those proposed by Alan Forte and John Rahn.
Both methods seek to identify the rotation in which the scale’s
intervals are most tightly clustered toward the left, though
they differ slightly in their criteria, leading to different
representatives in a few cases.

Xenharmlib provides both variants as part of the set class package:
:func:`~xenharmlib.setc.nf_forte` for Forte's definition and
:func:`~xenharmlib.setc.nf_rahn` for Rahns's definition respectively.

While in textbooks the normal form is often given in a notation like
"[013468T]" (with T representing 10), xenharmlib's normal form
functions do not return a string but a scale object of the same
type as the input:

.. testcode::

   from xenharmlib import EDOTuning
   from xenharmlib.setc import nf_forte

   edo12 = EDOTuning(12)
   scale = edo12.index_scale([1, 4, 6, 7, 9, 11])
   n_scale = nf_forte(scale)

   print(n_scale)

.. testoutput::

   EDOPitchScale([4, 6, 7, 9, 11, 13], 12-EDO)

To retrieve the normal form in its pitch class representation
the scale attribute
:attr:`~xenharmlib.core.pitch_scale.PeriodicPitchScale.pc_indices`
must be used:

.. testcode::

   print(n_scale.pc_indices)

.. testoutput::

   [4, 6, 7, 9, 11, 1]

Prime Form
------------------------------------

The prime form transforms all scales that are related by rotation,
transposition and inversion into a single representative. 

Xenharmlib provides both the Forte and the Rahn variant of the prime
form transformation: :func:`~xenharmlib.setc.primeform_forte` and
:func:`~xenharmlib.setc.primeform_rahn` respectively.

The prime form is calculated as follows:

1. Transform the scale to its normal order.
2. Zero-normalize the scale
3. Generate the inversion of the resulting scale,
   transform it to its normal order and zero-normalize it.
4. Compare scales from step 2 and 3 and choose the one
   with intervals most tightly packed to the left
   (using Forte's or Rahn's algorithm)

An example for 12-EDO:

.. testcode::

   from xenharmlib import EDOTuning
   from xenharmlib.setc import primeform_forte

   edo12 = EDOTuning(12)
   scale = edo12.index_scale([1, 4, 6, 7, 9, 11])
   n_scale = primeform_forte(scale)

   print(n_scale)

.. testoutput::

   EDOPitchScale([0, 2, 3, 5, 7, 9], 12-EDO)

To retrieve the prime form in its pure pitch class representation
use the scale attribute
:attr:`~xenharmlib.core.pitch_scale.PeriodicPitchScale.pc_indices`:

.. testcode::

   print(n_scale.pc_indices)

.. testoutput::

   [0, 2, 3, 5, 7, 9]

Interval Class Vectors
-------------------------------------

For tunings with integer pitch indices xenharmlib can calculate the
interval class vector with the :meth:`~xenharmlib.setc.ic_vector`
function from the set class package. An interval class vector counts
the number of times different interval classes occur in a scale, thus
giving a mathematical expression of the "color" of a scale or chord,
making it possible to compare scales and chords by color
similarity.

Intervals are counted like this:

1. Start from the first scale element and generate intervals to
   all succeeding elements. Transform the intervals to interval
   classes and count the number of occurences of each class
2. Do the same starting from the next scale element: Generate
   all intervals to succeeding elements (this omits already
   counted intervals between the current element and the
   proceeding element(s)), calculate the interval classes
   and update the counter
3. Repeat 2 until the last scale element is reached.

The first vector dimension counts the number of intervals with interval
class 1, the second dimension the number of intervals with interval class
2, etc. This means that the dimensions of the vector depend on the number
of possible interval classes in an origin context.
12-EDO for example has 6 different interval classes, therefor the
vector has 6 dimensions, 31-EDO has 15 different interval classes,
so the length of an interval class vector in 31-EDO is 15, etc.

Some examples for illustration:


.. tabs::

   .. tab:: EDO

      .. testcode:: EDOTuning

         from xenharmlib import EDOTuning
         from xenharmlib.setc import ic_vector

         edo31 = EDOTuning(31)

         scale = edo31.index_scale([0, 5, 11, 15, 17, 21])
         print(ic_vector(scale))

      .. testoutput:: EDOTuning

         (0, 1, 0, 2, 1, 3, 0, 0, 0, 3, 1, 1, 0, 1, 2)

   .. tab:: Western

      .. testcode:: WesternNotation

         from xenharmlib import WesternNotation
         from xenharmlib.setc import ic_vector

         western = WesternNotation()

         E4 = western.note('E', 4)
         G4 = western.note('G', 4)
         C5 = western.note('C', 5)

         scale = western.scale([E4, G4, C5])
         print(ic_vector(scale))

      .. testoutput:: WesternNotation

         (0, 0, 1, 1, 1, 0)

   .. tab:: UpDown

      .. testcode:: UpDownNotation

         from xenharmlib import EDOTuning
         from xenharmlib import UpDownNotation
         from xenharmlib.setc import ic_vector

         edo24 = EDOTuning(24)
         n_edo24 = UpDownNotation(edo24)

         Gb4 = n_edo24.note('Gb', 4)
         Aup4 = n_edo24.note('^A', 4)
         Bb4 = n_edo24.note('Bb', 4)

         scale = n_edo24.scale([Gb4, Aup4, Bb4])
         print(ic_vector(scale))

      .. testoutput:: UpDownNotation

         (1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0)
