Advanced Scale Methods
======================================

This section talks about pitch scale / note scale methods that have not
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
