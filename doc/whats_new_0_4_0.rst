What's new in xenharmlib 0.4.0?
======================================

As far as new features are concerned, version 0.4.0 is not a step
but a leap forward. Xenharmlib's core has been refactored to allow
not only equal-division temperaments but also tunings with multiple
generator intervals. This means that it now supports the entire range
of regular temperaments, including Just Intonation.

With the sole exception of irregular temperaments (such as the
“Werckmeister temperaments”), xenharmlib can finally represent
the entire cosmos of musical traditions in mathematical form.
It can now be used for the accurate analysis of music from the
Byzantine Empire, the European Renaissance, Indian classical
music, the Indonesian gamelan tradition, Arabic Maqam and
20th-century American experimental music (such as the
compositions of Harry Partch or Ben Johnston)

In keeping with its holistic approach, xenharmlib allows the use
of existing analytical tools for all regular temperaments, provided
they are mathematically compatible with them.
For example, Prime Form and Normal Form calculations can also be
performed on (multi-dimensional) regular temperaments.

In addition, the documentation has been completely revamped:
feature examples are organized by tuning and notation, and
comprehensive, dedicated documentation is provided for all
harmonic primitives.
We will give a brief overview of the aforementioned (and other)
features hereinafter. (For the full Changelog see
:ref:`here<changelog_0_4_0>`)

.. contents:: Table of Contents
   :depth: 1
   :local:
   :backlinks: none


Just Intonation / Prime Limit Tunings
--------------------------------------------

Just Intonation refers to tunings that are based on “pure intervals”.
A pure interval is characterized by a fraction of two integers, e.g.
:math:`\frac{3}{2}`. Historically, most tuning systems were based on
Just Intonation. It was not until the 18th and 19th centuries that
equal temperament systems began to gain widespread acceptance in
practice.
Xenharmlib now introduces support for Just Intonation with
the :doc:`Prime Limit Tuning <primelimit_tunings>` construct:

.. testcode::

   from xenharmlib import PrimeLimitTuning

   limit11 = PrimeLimitTuning(11)

A Pythagorean 12-tone chromatic scale can, for example, now be generated
by stacking 5 ascending pure fifths and 6 descending pure fifths from
the root pitch:

.. testcode::

   from xenharmlib import PrimeLimitTuning
   from xenharmlib import periodic

   pythagorean = PrimeLimitTuning(3)

   C0 = pythagorean.rs_pitch('1/1')
   P5 = pythagorean.rs_interval('3/2')

   iseq_a = pythagorean.interval_seq([P5] * 5)
   iseq_b = pythagorean.interval_seq([-P5] * 6)
   chromatic_scale = (
       C0.scale(iseq_a) | C0.scale(iseq_b)
   ).pcs_normalized()
   print(chromatic_scale)

.. testoutput::

   PrimeLimitPitchScale([1, 256/243, 9/8, 32/27, 81/64, 4/3, 1024/729, 3/2, 128/81, 27/16, 16/9, 243/128], 3-Limit)

Most software programs implement functions for Just Intonation not as a
complete arithmetic system, but as a system of scalar transposition.
In the case of a transposition by a fifth, for example, a definition
of the chromatic scale (such as the one mentioned above) is typically
used as a basis, and the transposition is understood as a shift of 7
scale degrees:

.. testcode::

   for i in range(0, 12):
       pitch = chromatic_scale[i]
       result = periodic.scalar_transpose(chromatic_scale, pitch, 7)
       interval = pitch.interval(result)
       print(f'{pitch.short_repr} --> {result.short_repr} ({interval.short_repr})')

.. testoutput::

    1 --> 3/2 (3/2)
    256/243 --> 128/81 (3/2)
    9/8 --> 27/16 (3/2)
    32/27 --> 16/9 (3/2)
    81/64 --> 243/128 (3/2)
    4/3 --> 2 (3/2)
    1024/729 --> 512/243 (3/2)
    3/2 --> 9/4 (3/2)
    128/81 --> 64/27 (3/2)
    27/16 --> 81/32 (3/2)
    16/9 --> 8/3 (3/2)
    243/128 --> 2048/729 (262144/177147)

As you can see with the last pitch of the output (:math:`\frac{243}{128}`),
transposition by scale degree in a Pythagorean chromatic scale does
not always result in an *actual* transposition of the interval in question.
This is a common problem when tuning a keyboard instrument (such as a
piano or harpsichord) that has only a limited number of notes per octave. 
Mathematically speaking, this definition of transposition by a fifth is
irregular: the size of the fifth changes depending on which note is chosen
as the starting point.

Unlike a keyboard instrument, a stringed instrument without frets or the
human voice does not have the problem of limited note selection.
Xenharmlib therefore implements its default transposition *not* as scalar
transposition, but as regular transposition, with the effect that the
result of transposing the last note of the above scale has a pitch
class no longer represented in the scale itself.

.. testcode::

   for i in range(0, 12):

       pitch = chromatic_scale[i]
       result = pitch.transpose(P5)
       interval = pitch.interval(result)

       try:
           scale_degree = periodic.index(chromatic_scale, result)
       except ValueError:
           scale_degree = 'not in scale'

       print(f'{pitch.short_repr} --> {result.short_repr} ', end='')
       print(f'({interval.short_repr}) - degree: {scale_degree}')

.. testoutput::

    1 --> 3/2 (3/2) - degree: 7
    256/243 --> 128/81 (3/2) - degree: 8
    9/8 --> 27/16 (3/2) - degree: 9
    32/27 --> 16/9 (3/2) - degree: 10
    81/64 --> 243/128 (3/2) - degree: 11
    4/3 --> 2 (3/2) - degree: 12
    1024/729 --> 512/243 (3/2) - degree: 13
    3/2 --> 9/4 (3/2) - degree: 14
    128/81 --> 64/27 (3/2) - degree: 15
    27/16 --> 81/32 (3/2) - degree: 16
    16/9 --> 8/3 (3/2) - degree: 17
    243/128 --> 729/256 (3/2) - degree: not in scale

This definition is not only mathematically more sound (since it has a
single, consistent definition of a fifth), but it also allows us to deal
with compositions that use the available tuning space to its full
extent, not just a chromatic selection of pitches.

Custom Regular Temperaments
-----------------------------------------

Custom regular temperaments can now be designed using the newly introduced
:doc:`Multi-Generator Tunings <multigen_tunings>`.
The Quarter-Comma-Meantone Temperament that flattens the tritave by
a quarter of the syntonic comma can, for example, be constructed like this:

.. testcode::

   from fractions import Fraction
   from xenharmlib import MultiGenTuning
   from xenharmlib import FrequencyRatio

   g3 = FrequencyRatio(3) * FrequencyRatio(80, 81) ** Fraction(1, 4)
   qcm = MultiGenTuning(
       (FrequencyRatio(2), g3),
       eq_diff_vec=(1, 0)
   )


Full Interval Arithmetic
-----------------------------------------

A feature necessary for many theoretical applications — one that was long
missing from xenharmlib — is now being introduced in version 0.4.0. We're
talking about interval arithmetic:

.. testcode::

   from xenharmlib import WesternNotation

   western = WesternNotation()

   m3 = western.shorthand_interval('m', 3)
   M3 = western.shorthand_interval('M', 3)

   print(m3 + M3)
   print(M3 - m3)
   print(3 * M3)

.. testoutput::

   WesternNoteInterval(P, 5)
   WesternNoteInterval(A, 1)
   WesternNoteInterval(A, 7)

To learn more, please consult the
:doc:`dedicated page on intervals <prim_interval>`.

Additional Harmonic Primitives
-----------------------------------------

Version 0.4.0 comes with two new harmonic primitives for its analytical
toolbox:

:doc:`Sequences <prim_seq>` allow you to conceptualize a "succession of notes",
for example in segment analysis. Sequences come with typical transformation
methods like retrograde and inversion.

.. testcode::
   
   from xenharmlib import WesternNotation
   western = WesternNotation()
   
   # melodic flow of the beginning of "marry had a little lamb"
   seq = western.seq(western.note(pcs, 4) for pcs in 'EDCDEEE')

   print(seq)
   print(seq.retrograde())
   print(seq.inversion())

.. testoutput::

   WesternNoteSeq([E4, D4, C4, D4, E4, E4, E4])
   WesternNoteSeq([E4, E4, E4, D4, C4, D4, E4])
   WesternNoteSeq([E4, F#4, G#4, F#4, E4, E4, E4])

With :doc:`Interval Fans <prim_interval_fan>`, a new type of abstract
scale object is introduced that describes the relative distances of
the elements of a sequence or scale to a tonal center:

.. testcode::
   
   from xenharmlib import WesternNotation
   western = WesternNotation()
   
   # melodic flow of the beginning of "marry had a little lamb"
   seq = western.seq(western.note(pcs, 4) for pcs in 'EDCDEEE')
   
   # calculate relative distances to the tonic of C4
   tonic = western.note('C', 4)
   ifan = seq.to_interval_fan(tonic)
   print(ifan)

.. testoutput::
   
   WesternNoteIntervalFan([M3, M2, P1, M2, M3, M3, M3])

Interval Class Vectors
-----------------------------------------

As an essential tool for scale analysis, especially in post-tonal analysis,
xenharmlib now supports the calculation of interval class vectors:

.. testcode::
   
   from xenharmlib import EDOTuning
   from xenharmlib.setc import ic_vector
   
   edo31 = EDOTuning(31)
   
   scale = edo31.index_scale([0, 5, 11, 15, 17, 21])
   print(ic_vector(scale))

.. testoutput::

   (0, 1, 0, 2, 1, 3, 0, 0, 0, 3, 1, 1, 0, 1, 2)

Closest Frequency Approximation
-----------------------------------------------------

All harmonic primitives of one-dimensional tunings and notations now
support closest frequency approximation, e.g. scales:

.. testcode::

   from xenharmlib import WesternNotation
   from xenharmlib import Frequency
   
   western = WesternNotation()
   
   # overtone frequencies measured e.g. by
   # a spectrogram plugin or librosa
   frequencies = [
       Frequency(f) for f in [230, 410, 460, 500, 690]
   ]
   
   scale = western.closest_scale(frequencies)
   print(scale)

.. testoutput::

   WesternNoteScale([A#3, G#4, A#4, B4, F5])

