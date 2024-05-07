Quickstart
======================================

Installation
------------------------

Xenharmlib works with python 3.11 and beyond. We recommend using xenharmlib
in a `virtual environment <https://docs.python.org/3/library/venv.html>`_.
Xenharmlib can be installed with pip:

.. code-block:: console

   (.venv) $ pip install xenharmlib


Tunings and Pitches
------------------------

Xenharmlib offers a few basic components that serve as the building
blocks for deriving common tunings. One of the most widespread are
tunings with equal divisions of the octave
(:class:`~xenharmlib.core.tunings.EDOTuning`), which includes the
standard contemporary Western tuning.

.. testcode::

   from xenharmlib import EDOTuning

   edo12 = EDOTuning(12)

EDO tunings are constructed by the number of divisions that exist in one
octave. A modern arabic scale can for example be constructed like this:

.. testcode::

   edo24 = EDOTuning(24)

If you want a different interval than the octave for the equivalency
interval, for example a tritave, you can use the more general "equal
division tuning" :class:`~xenharmlib.core.tunings.EDTuning` (sans 'O').
There you can define the frequency ratio of the equivalency interval
yourself:

.. testcode::

   from xenharmlib import EDTuning
   from xenharmlib import Frequency

   bohlen_pierce = EDTuning(13, Frequency(3))

Xenharmlib is designed in a way that you can use different levels of
abstractions for individual tuning sounds. Some prefer the customary
world of notes (like D, F#) while others want to look at tunings in a
more mathematical way, exploring pitches and pitch classes as integers
without the burdens of enharmonic ambigouity.

In the first part of this tutorial we want to look at this lower
conceptual level of individual sounds, the pitch:

.. testcode::

   edo12 = EDOTuning(12)
   edo31 = EDOTuning(31)

   edo12_g0 = edo12.pitch(7)
   edo31_g0 = edo31.pitch(18)

A pitch is firstmost defined by its pitch index. The pitch index defines
the number of steps from the base pitch, which is given the pitch
index 0. To visualize pitch indices, best think of a piano: The pitch
index is the number of successive key presses needed to reach a tone
starting from the lowest C:

.. image:: _static/images/piano-pitch-indices.png
  :width: 100%
  :alt: An image of a piano with pitch index labels

.. testcode::

   c0 = edo12.pitch(0)
   g0 = edo12.pitch(7)
   g1 = edo12.pitch(19)
   gsharp1 = edo12.pitch(20)

Pitches can be compared based on their frequency:

.. testcode::

   print(edo31.pitch(1) < edo12.pitch(1))
   print(edo31.pitch(1) > edo12.pitch(1))
   print(edo24.pitch(2) == edo12.pitch(1))

.. testoutput::

   True
   False
   True

This also means that pitches are sortable, even across different
tunings:

.. testcode::

    p1 = edo24.pitch(4)
    p2 = edo31.pitch(2)
    p3 = edo12.pitch(3)

    print(sorted([p1, p2, p3]))

.. testoutput::

    [EDOPitch(2, 31-EDO), EDOPitch(4, 24-EDO), EDOPitch(3, 12-EDO)]

To retrieve the frequency of a pitch directly use the frequency
property:

.. testcode::

    print(edo24.pitch(3).frequency)

.. testoutput::

    Frequency(55*2**(3/8)/4)

You might be wondering why you are not seeing a simple number but an
expression. This is because pitches in equal division tunings have
irrational frequencies. Xxenharmlib does not round them to floats
but keeps them in a symbolic format to achieve perfect precision
results when doing mathematical operations. The above frequency
is equal to this expression:

.. math::

   55\frac{2^{\frac{3}{8}}}{4}

If you are fine with less precision you can always convert a frequency
to a float. (Just keep in mind that errors add up when doing floating
point math)

.. testcode::

    print(float(edo24.pitch(3).frequency))

.. testoutput::

    17.831543876451384

Speaking of math: Pitches also allow addition, substraction and scalar
multiplication:

.. testcode::

    print(edo24.pitch(3) + edo24.pitch(3))
    print(edo24.pitch(10) - edo24.pitch(2))
    print(5 * edo24.pitch(2))

.. testoutput::

    EDOPitch(6, 24-EDO)
    EDOPitch(8, 24-EDO)
    EDOPitch(10, 24-EDO)

As an alternative for addition and substraction you can also use the
:meth:`~xenharmlib.core.pitch.Pitch.transpose` method for transposition,
which expects a positive or negative integer. The following snippets
defines a function that transposes the pitch n octaves up regardless of
tuning:

.. testcode::

    def octaves_up(pitch, n):
        return pitch.transpose(
            n * len(pitch.tuning)
        )

    a0 = edo12.pitch(9)
    print(octaves_up(a0, 2))

.. testoutput::

    EDOPitch(33, 12-EDO)

Pitches of periodic tunings (for example the various equal temperaments)
form pitch classes (or in mathematical terms: equivalency classes in a
finite group). As a musician you are already familiar with this in the
standard western notation, since pitches of the same class get assigned
the same letter. For pitches of periodic tunings the property
:attr:`~xenharmlib.core.pitch.PeriodicPitch.pc_index` can be used to
retrieve the pitch class, while the property
:attr:`~xenharmlib.core.pitch.PeriodicPitch.bi_index` returns the index
of the base interval.

.. image:: _static/images/piano-pc-indices.png
  :width: 100%
  :alt: An image of a piano with pitch index labels

.. testcode::

    g0 = edo12.pitch(7)
    g1 = edo12.pitch(19)
    
    print(g0.pc_index)
    print(g0.bi_index)

    print(g1.pc_index)
    print(g1.bi_index)

.. testoutput::

    7
    0
    7
    1

Pitches are bound to their tuning, but you can easily map pitches of
one tuning to another by the :meth:`~xenharmlib.core.pitch.Pitch.retune`
method. This takes the frequency of the pitch and finds the pitch with
the closest frequency in another tuning. For example if you are
accustomed to a standard western tuning and just started your journey
into micronality you might be interested in finding the 12 pitches of a
western octave that you are already familiar with:

.. testcode::

    def western_pitches(tuning):
        pitches = []
        for i in range(0, 12):
            pitches.append(
                edo12.pitch(i).retune(tuning)
            )
        return pitches

    pitches = western_pitches(edo31)
    for pitch in pitches:
        print(pitch)

.. testoutput::

    EDOPitch(0, 31-EDO)
    EDOPitch(3, 31-EDO)
    EDOPitch(5, 31-EDO)
    EDOPitch(8, 31-EDO)
    EDOPitch(10, 31-EDO)
    EDOPitch(13, 31-EDO)
    EDOPitch(15, 31-EDO)
    EDOPitch(18, 31-EDO)
    EDOPitch(21, 31-EDO)
    EDOPitch(23, 31-EDO)
    EDOPitch(26, 31-EDO)
    EDOPitch(28, 31-EDO)

Tunings also allow pitch approximations directly from frequencies
with the :meth:`~xenharmlib.core.tunings.TuningABC.get_approx_pitch`
method.

For example if you want the pitch class that best approximates the
perfect fifth in a tuning you can do something like this:

.. testcode::

    from fractions import Fraction

    def get_fifth_pc_index(tuning):
        zero_freq = tuning.pitch(0).frequency
        perfect_fifth_freq = zero_freq * Frequency(Fraction(3, 2))
        fifth = tuning.get_approx_pitch(
            perfect_fifth_freq
        )
        return fifth.pc_index

    print(get_fifth_pc_index(edo12))
    print(get_fifth_pc_index(edo31))

.. testoutput::

    7
    18

Pitch Intervals
------------------------

Two pitches can form an interval. Pitch intervals can be either
created with the
:meth:`~xenharmlib.core.tunings.TuningABC.pitch_interval` method of a
tuning or with the interval method of a pitch:

.. testcode::

    pitch_a = edo31.pitch(3)
    pitch_b = edo31.pitch(9)
    interval = edo31.pitch_interval(pitch_a, pitch_b)

    assert interval == pitch_a.interval(pitch_b)
    print(interval.pitch_diff)

.. testoutput::

    6

Intervals are considered **directional** in xenharmlib, which means
that the order of the pitches from which they are created is important.

.. testcode::

    pitch_a = edo31.pitch(3)
    pitch_b = edo31.pitch(9)
    interval = pitch_b.interval(pitch_a)

    print(interval.pitch_diff)

.. testoutput::

    -6

The direction of intervals can be normalized with the :code:`abs()`
function:

.. testcode::

    pitch_a = edo31.pitch(3)
    pitch_b = edo31.pitch(9)
    interval_u = pitch_a.interval(pitch_b)
    interval_d = pitch_b.interval(pitch_a)

    assert interval_u.pitch_diff != interval_d.pitch_diff
    assert abs(interval_u).pitch_diff == abs(interval_d).pitch_diff

.. testoutput::
    :hide:


Similar to pitches intervals are comparable and sortable, also across
different tunings. Intervals with a smaller frequency ratio are
considered smaller, and vice versa. For example the fifth interval of
31edo is a bit smaller than the fifth interval of 12edo:

.. testcode::

    interval_fifth_edo12 = edo12.pitch(0).interval(
        edo12.pitch(7)
    )
    interval_fifth_edo31 = edo31.pitch(0).interval(
        edo31.pitch(18)
    )

    assert interval_fifth_edo31 < interval_fifth_edo12

.. testoutput::
    :hide:

You can also directly get the frequency ratio and the corresponding
cents value:

.. testcode::

    interval_fifth_edo31.frequency_ratio
    interval_fifth_edo31.cents

.. testoutput::
    :hide:

There is a bit of a caveat when handling negative / downward intervals:
The :code:`<` operator does compare frequency ratios, *not* absolute
sizes, so - maybe surprising to some - the following holds true:

.. testcode::

    fifth_d = edo12.pitch(7).interval(
        edo12.pitch(0)
    )
    second_d = edo12.pitch(2).interval(
        edo12.pitch(0)
    )
    assert fifth_d < second_d

If you want to compare absolute sizes you have to use the :code:`abs()`
function.

.. testcode::

    assert abs(fifth_d) > abs(second_d)

For periodic tunings you can calculate the generator distance, which is
the minimum number of steps from one pitch to the other when iteratively
adding a generator pitch. A typical example is the minimum distance on
the circle of fifths. If you e.g. want to sort intervals according to
the closeness of their pitches on the circle of fifths you can do
something like this:

.. testcode::

    def co5_closeness(interval):
        return interval.get_generator_distance(
            interval.tuning.best_fifth
        )

    tuning = edo31

    intervals = []
    for i in range(0, len(tuning)):
        zero = tuning.pitch(0)
        target = tuning.pitch(i)
        intervals.append(
            zero.interval(target)
        )

    sorted_by_closeness = sorted(
        intervals, key=co5_closeness
    )

    for interval in sorted_by_closeness:
        print(interval)

.. testoutput::
    :hide:
    
    EDOPitchInterval(0, 31-EDO)
    EDOPitchInterval(13, 31-EDO)
    EDOPitchInterval(18, 31-EDO)
    EDOPitchInterval(5, 31-EDO)
    EDOPitchInterval(26, 31-EDO)
    EDOPitchInterval(8, 31-EDO)
    EDOPitchInterval(23, 31-EDO)
    EDOPitchInterval(10, 31-EDO)
    EDOPitchInterval(21, 31-EDO)
    EDOPitchInterval(3, 31-EDO)
    EDOPitchInterval(28, 31-EDO)
    EDOPitchInterval(15, 31-EDO)
    EDOPitchInterval(16, 31-EDO)
    EDOPitchInterval(2, 31-EDO)
    EDOPitchInterval(29, 31-EDO)
    EDOPitchInterval(11, 31-EDO)
    EDOPitchInterval(20, 31-EDO)
    EDOPitchInterval(7, 31-EDO)
    EDOPitchInterval(24, 31-EDO)
    EDOPitchInterval(6, 31-EDO)
    EDOPitchInterval(25, 31-EDO)
    EDOPitchInterval(12, 31-EDO)
    EDOPitchInterval(19, 31-EDO)
    EDOPitchInterval(1, 31-EDO)
    EDOPitchInterval(30, 31-EDO)
    EDOPitchInterval(14, 31-EDO)
    EDOPitchInterval(17, 31-EDO)
    EDOPitchInterval(4, 31-EDO)
    EDOPitchInterval(27, 31-EDO)
    EDOPitchInterval(9, 31-EDO)
    EDOPitchInterval(22, 31-EDO)

Pitch Scales
------------------------

Pitch scales are sorted lists of unique pitches. Like pitches they
can be constructed through a builder method in the tuning object.

.. testcode::

    scale = edo31.pitch_scale(
        [edo31.pitch(9), edo31.pitch(0), edo31.pitch(4), edo31.pitch(5)]
    )

Xenharmlib will sort the pitches automatically when constructing a
scale, so the original order is not important. The uniqueness property
means that duplicate pitches in the list will be only added once.
Please note that the uniqueness property refers to pitch and not pitch
class, so scales including 'C-0' and 'C-1' are possible.

Pitch scale objects support most of the typical list operations, e.g.
they are iterable:

.. testcode::

    for pitch in scale:
        print(pitch)

.. testoutput::

    EDOPitch(0, 31-EDO)
    EDOPitch(4, 31-EDO)
    EDOPitch(5, 31-EDO)
    EDOPitch(9, 31-EDO)

They also support item selection and slicing:

.. testcode::

    print(scale[1])
    print(scale[1:-1])

.. testoutput::

    EDOPitch(4, 31-EDO)
    EDOPitchScale([4, 5], 31-EDO)

The 'in' operator accepts both pitches and pitch intervals. If an
interval is given xenharmlib checks if *any* two pairs of notes
(both in upwards and downwards direction) form the interval.

.. testcode::
   
    scale = edo31.pitch_scale(
        [edo31.pitch(0), edo31.pitch(5), edo31.pitch(9)]
    )

    p = edo31.pitch(0)
    assert p in scale
    assert p.interval(edo31.pitch(9)) in scale

.. testoutput::
    :hide:

The in operator is even more broad: It generally accepts every object
that has a :attr:`frequency` or a :attr:`frequency_ratio` attribute,
meaning that pitch and interval containment can be tested across
tunings:

.. testcode::

    edo12_scale = edo12.pitch_scale(edo12.pitch_range(0, 12))
    edo24_scale = edo24.pitch_scale(edo24.pitch_range(0, 24))

    assert all([pitch in edo24_scale for pitch in edo12_scale])

    edo12_fifth = edo12.pitch(0).interval(
        edo12.pitch(7)
    )
    assert edo12_fifth in edo24_scale

.. testoutput::
    :hide:

In general all the operations that are possible on single pitches are
also possible on scales, for example you can transpose a scale the
same way you can transpose pitches:

.. testcode::
   
    scale = edo31.pitch_scale(
        [edo31.pitch(0), edo31.pitch(5), edo31.pitch(9)]
    )
    transposed = scale.transpose(2)
    print(transposed)

.. testoutput::

    EDOPitchScale([2, 7, 11], 31-EDO)

You can also use the retune method to approximate a scale in a different
tuning:

.. testcode::

    scale = edo12.pitch_scale(
        [edo12.pitch(0), edo12.pitch(1), edo12.pitch(2)]
    )
    retuned = scale.retune(edo24)
    print(retuned)

.. testoutput::

    EDOPitchScale([0, 2, 4], 24-EDO)

Scales in periodic tunings can be rotated upwards and downwards. On
upwards rotation the lowest pitch will get transposed by the tuning's
equivalency interval until it surpasses the highest pitch of the scale.
On downwards rotation vice versa: The highest pitch is transposed
downwards until it is below the lowest pitch.

In the context of chords this is called *inversion*. In the context
of scales this is also known as *mode*. Since both terms have very
contextual meanings we decided for the more neutral *rotation* as
a name.

Let's look at it in the context of triads:

.. testcode::

    c0 = edo12.pitch(0)
    e0 = edo12.pitch(4)
    g0 = edo12.pitch(7)

    c_triad = edo12.pitch_scale([c0, e0, g0])

We can use the :meth:`rotated_up` method to recieve the first inversion
of the triad:

.. testcode::

    c_first_inversion = c_triad.rotated_up()
    print(c_first_inversion)

.. testoutput::

    EDOPitchScale([4, 7, 12], 12-EDO)

while :meth:`rotated_down` on the other hand can be used to do the
opposite, making us return to where we started:

.. testcode::

    assert c_first_inversion.rotated_down() == c_triad

There is also the more general method :meth:`rotation` to your disposal,
which can be used as a shortcut if you want more than one upwards or
downward rotation:

.. testcode::

    second_inversion = c_triad.rotation(2)
    print(second_inversion)

.. testoutput::

    EDOPitchScale([7, 12, 16], 12-EDO)

Pitch scales also support most of the typical set operations that
you are familiar with from the builtin python sets (with slightly
different names):

* :meth:`~xenharmlib.core.pitch_scale.PeriodicPitchScale.intersection`
* :meth:`~xenharmlib.core.pitch_scale.PeriodicPitchScale.union`
* :meth:`~xenharmlib.core.pitch_scale.PeriodicPitchScale.difference`
* :meth:`~xenharmlib.core.pitch_scale.PeriodicPitchScale.symmetric_difference`
* :meth:`~xenharmlib.core.pitch_scale.PeriodicPitchScale.is_subset`
* :meth:`~xenharmlib.core.pitch_scale.PeriodicPitchScale.is_superset`
* :meth:`~xenharmlib.core.pitch_scale.PeriodicPitchScale.is_disjoint`

As an illustration for the usefulness of set operations we calculate
pitches safe for improvisation according to the 'avoid notes' concept in
jazz for 12-EDO. There are various approaches (and a lot of dispute) to
this, but one rule-of-thumb is that for any chord and a selected scale,
pitches in the scale that are one degree over a chord pitch should be
avoided:

.. testcode::

    def get_safe_for_chord(scale, chord):

        # get a scale consisting of the bad pitches
        avoid_scale = chord.transpose(1)

        # get the original scale without the bad pitches
        # (the ignore_bi_index=True tells the operation
        # to also remove equivalent pitches that just
        # differ in base interval)
        return scale.difference(avoid_scale, ignore_bi_index=True)

    c_maj = edo12.pitch_scale(
        [edo12.pitch(i) for i in [0, 2, 4, 5, 7, 9, 11]]
    )
    C7 = edo12.pitch_scale(
        [edo12.pitch(i) for i in [0, 4, 7, 10]]
    )

    print(get_safe_for_chord(c_maj, C7))

.. testoutput::

    EDOPitchScale([0, 2, 4, 7, 9], 12-EDO)

As an example for the intersection method we calculate how the Revati
scale from India's Carnatic music and the Japanese Hirajōshi scale (as
interpreted by Sachs and Slonimsky) overlap when being translated into
the Western equal-tempered 12-tone system:

.. testcode::

    revati = edo12.pitch_scale(
        [edo12.pitch(i) for i in [0, 1, 5, 7, 10]]
    )
    hirajoshi = edo12.pitch_scale(
        [edo12.pitch(i) for i in [0, 1, 5, 6, 10]]
    )

    print(revati.intersection(hirajoshi))

.. testoutput::

    EDOPitchScale([0, 1, 5, 10], 12-EDO)

Often the interest lies not in the overlapping of specific pitches, but
rather in the shared pitch classes. This becomes particularly relevant
when choosing notes for a melody during key modulation.
To aid in this task, scales of periodic tunings can be normalized to
the first base interval. As a result, pitch indices and pitch class
indices become the same, simplifying the analysis for a variety of
purposes.

.. testcode::

    a_minor = edo12.pitch_scale(
        [edo12.pitch(i) for i in [9, 11, 12, 14, 16, 17, 19]]
    )
    print(a_minor.pcs_normalized())

.. testoutput::

    EDOPitchScale([0, 2, 4, 5, 7, 9, 11], 12-EDO)

(Please note that this method does not maintain the original order of
the scale. As illustrated in the example, both A minor and C major
possess the exact same base interval normal form.)

After scales are converted into their basic interval normal form, they
can be treated like sets of pitch classes. To address our original
question about which notes to use when modulating from one key to
another, we can now combine basic interval normalization with the
intersection method to achieve our goal:

.. testcode::

    a_minor = edo12.pitch_scale(
        [edo12.pitch(i) for i in [9, 11, 12, 14, 16, 17, 19]]
    )
    g_major = edo12.pitch_scale(
        [edo12.pitch(i) for i in [7, 9, 11, 12, 14, 16, 18]]
    )

    shared = a_minor.pcs_normalized().intersection(
        g_major.pcs_normalized()
    )
    print(shared)

.. testoutput::

    EDOPitchScale([0, 2, 4, 7, 9, 11], 12-EDO)

Given the frequent need of this operation, a convenient shortcut is also
available:

.. testcode::

    shared = a_minor.pcs_intersection(g_major)
    print(shared)

.. testoutput::
    :hide:

    EDOPitchScale([0, 2, 4, 7, 9, 11], 12-EDO)

Pitch scale objects have many features, too many to list them all in the
quickstart. If you want to know more about scale features head over to
the API documentation on the :mod:`~xenharmlib.core.pitch_scale` module.

Notation
---------------------------------

Notation can be a murky thing, especially when it comes to tunings that
are more novel and don't come with an established cultural tradition.
Not every notation system makes sense for every tuning. Some systems
produce very counter-intuitive results when combined with unfitting
tunings (for example in standard western notation 'E' and 'F' are the
same note in 5-EDO). In this quickstart we will focus on a notation
called "up/down notation" which is a superset of the standard western
notation. Apart from a couple of outliers (like 5-EDO) the system works
pretty well on a large number of periodic tunings that rely on division
of the octave.

Let's create our first notation with it:

.. testcode::

    from xenharmlib import EDOTuning
    from xenharmlib.notation import UpDownNotation

    edo31 = EDOTuning(31)
    n_edo31 = UpDownNotation(edo31)

The notation layer 'wraps' the low level classes and provides a more
human-friendly interface to them, making connections between
pitches of different tunings visible that are sometimes hard to see
when only represented as integers.

Like the tuning object on the lower level, the notation object provides
us with builder methods to create notes, intervals and scales.

Individual notes can be created by using the note method which expects
a pitch class symbol and the base interval index (the octave number in
EDOs) as arguments:

.. testcode::

    c = n_edo31.note('C', 0)
    e_neutral = n_edo31.note('vE', 0)
    g_flat = n_edo31.note('Gb', 0)

You can combine two notes to form a note interval:

.. testcode::

    neutral_3 = n_edo31.note_interval(
        c, e_neutral
    )
    diminished_5 = n_edo31.note_interval(
        c, g_flat
    )

A list of notes can be used to create a note scale:

.. testcode::

    triad = n_edo31.note_scale(
        [c, e_neutral, g_flat]
    )

Please note that other notations might use different builder arguments
to create these objects, however the above combination are the most
common practice.

All notational objects are bound to their lower level equivalent.
Given a notational object you can always retrieve their lower level
counter-part:

.. testcode::

    print(c.pitch)
    print(neutral_3.pitch_interval)
    print(triad.pitch_scale)

.. testoutput::

    EDOPitch(0, 31-EDO)
    EDOPitchInterval(9, 31-EDO)
    EDOPitchScale([0, 9, 16], 31-EDO)

Notes
-----------------------------------

The type of notes in a notation is heavily dependend on the attributes
of the tuning it encloses. Tunings with many divisions of the octave
need more notes than tunings with less divisions. In certain notations
'C#' and 'Db' refer to the same pitch, in others the pitches are
distinct.

UpDownNotation is a natural/accidental notation. It first approximates
the naturals (C, D, E, F, G, A, B), mapping C to the zero pitch and
generating the other naturals by stacking fifths. After that it
approximates sharp and flat accidentals and fills the gaps with
multiples of sharps and flats or up and down arrows. The note object
created by UpDownNotation consists of a natural (like 'C') and an
accidental (like '#'). The more pitches exist in between two natural
pitches the more accidentals are needed.

In xenharmlib's implementation of UpDownNotation, enharmonic equivalents
are theoretically infinite due to its comprehensive accidental
arithmetic. Though rarely utilized practically, this feature allows for
the creation of notes with any number of accidentals:

.. testcode::

    weird_aug_c0 = n_edo31.note('^^^^Cx#xx', 0)
    weird_dim_c1 = n_edo31.note('vvvCbbbbb', 1)
    print(weird_aug_c0 == weird_dim_c1)

.. testoutput::

    True

It is even possible to mix flat/sharp and up/down accidentals:

.. testcode::

    weird_note = n_edo31.note('vvvvv^^^^Cxx#xxbbx', 0)

In the following table we display an overview of the different
accidentals that are used by UpDownNotation in their ASCII form together
with the matching symbols in the Standard Music Layout Font.

If a certain accidental is available depends on the underlying tuning.
For 12-EDO e.g. the 'bv' accidental is not available, however for 31-EDO
it is. In general there exists exactly one accidental symbol for each
accidental value (hence 'v' does not exist in 12-EDO because it would be
the same as 'b')

.. role:: smufl

.. list-table::
   :widths: 25 25 25 25
   :header-rows: 1

   * - unicode sharp
     - ascii sharp
     - unicode flat
     - ascii flat
   * - C |acc_^|
     - C^
     - C |acc_v|
     - Cv
   * - C |acc_^^|
     - C^^
     - C |acc_vv|
     - Cvv
   * - C |acc_^^^|
     - C^^^
     - C |acc_vvv|
     - Cvvv
   * - C |acc_#vvv|
     - C#vvv
     - C |acc_b^^^|
     - Cb^^^
   * - C |acc_#vv|
     - C#vv
     - C |acc_b^^|
     - Cb^^
   * - C |acc_#v|
     - C#v
     - C |acc_b^|
     - Cb^
   * - C |acc_#|
     - C#
     - C |acc_b|
     - Cb
   * - C |acc_#^|
     - C#^
     - C |acc_bv|
     - Cbv
   * - C |acc_#^^|
     - C#^^
     - C |acc_bvv|
     - Cbvv
   * - C |acc_#^^^|
     - C#^^^
     - C |acc_bvvv|
     - Cbvvv
   * - C |acc_xvvv|
     - Cxvvv
     - C |acc_bb^^^|
     - Cbb^^^
   * - C |acc_xvv|
     - Cxvv
     - C |acc_bb^^|
     - Cbb^^
   * - C |acc_xv|
     - Cxv
     - C |acc_bb^|
     - Cbb^
   * - C |acc_x|
     - Cx
     - C |acc_bb|
     - Cbb
   * - C |acc_x^|
     - Cx^
     - C |acc_bbv|
     - Cbbv
   * - C |acc_x^^|
     - Cx^^
     - C |acc_bbvv|
     - Cbbvv
   * - C |acc_x^^^|
     - Cx^^^
     - C |acc_bbvvv|
     - Cbbvvv

.. |acc_^| replace:: :smufl:``
.. |acc_^^| replace:: :smufl:``
.. |acc_^^^| replace:: :smufl:``
.. |acc_t| replace:: :smufl:``
.. |acc_#vvv| replace:: :smufl:``
.. |acc_#vv| replace:: :smufl:``
.. |acc_#v| replace:: :smufl:``
.. |acc_#| replace:: :smufl:``
.. |acc_#^| replace:: :smufl:``
.. |acc_#^^| replace:: :smufl:``
.. |acc_#^^^| replace:: :smufl:``
.. |acc_#t| replace:: :smufl:``
.. |acc_xvvv| replace:: :smufl:``
.. |acc_xvv| replace:: :smufl:``
.. |acc_xv| replace:: :smufl:``
.. |acc_x| replace:: :smufl:``
.. |acc_x^| replace:: :smufl:``
.. |acc_x^^| replace:: :smufl:``
.. |acc_x^^^| replace:: :smufl:``

.. |acc_v| replace:: :smufl:``
.. |acc_vv| replace:: :smufl:``
.. |acc_vvv| replace:: :smufl:``
.. |acc_d| replace:: :smufl:``
.. |acc_b^^^| replace:: :smufl:``
.. |acc_b^^| replace:: :smufl:``
.. |acc_b^| replace:: :smufl:``
.. |acc_b| replace:: :smufl:``
.. |acc_bv| replace:: :smufl:``
.. |acc_bvv| replace:: :smufl:``
.. |acc_bvvv| replace:: :smufl:``
.. |acc_db| replace:: :smufl:``
.. |acc_bb^^^| replace:: :smufl:``
.. |acc_bb^^| replace:: :smufl:``
.. |acc_bb^| replace:: :smufl:``
.. |acc_bb| replace:: :smufl:``
.. |acc_bbv| replace:: :smufl:``
.. |acc_bbvv| replace:: :smufl:``
.. |acc_bbvvv| replace:: :smufl:``

Since notes are wrappers around pitches, you can operate on notes mostly
the same way you operated on pitches with the difference that the
methods returning pitches now return notes. We will quickly go through
the similarities.

Notes are sortable and comparable by frequencies the same way as
pitches:

.. testcode::

    edo31 = EDOTuning(31)
    n_edo31 = UpDownNotation(edo31)

    assert n_edo31.note('^G', 0) < n_edo31.note('G#', 0)
    assert n_edo31.note('Dx', 0) > n_edo31.note('D#', 0)
    assert n_edo31.note('G', 0) == n_edo31.note('G', 0)

    edo12 = EDOTuning(12)
    n_edo12 = UpDownNotation(edo12)

    assert n_edo12.note('G', 0) != n_edo31.note('G', 0)
    assert n_edo12.note('G', 0) > n_edo31.note('G', 0)

.. testoutput::
    :hide:

Notes and pitches can also be compared:

.. testcode::

    assert n_edo31.note('vG', 0) < edo31.pitch(18)
    assert n_edo31.note('G', 0) == edo31.pitch(18)

.. testoutput::
    :hide:

The reason for this is that notes and pitches implement a common
interface. Notes have convenient 'proxies' to the properties of the
underlying pitch. This way pitch objects can be substituted for notes
in all analytical utils of the library.

Here is a selection of the shared interface between periodic pitches
and periodic notes:

.. testcode::

    gsharp1 = n_edo31.note('G#', 1)
    assert gsharp1.frequency == gsharp1.pitch.frequency
    assert gsharp1.pitch_index == gsharp1.pitch.pitch_index
    assert gsharp1.pc_index == gsharp1.pitch.pc_index
    assert gsharp1.bi_index == gsharp1.pitch.bi_index

.. testoutput::
    :hide:

Because the equality sign tests on frequency it does *not* care for
enharmonic differences. If you want to be stricter and only consider
two notes equal if they are functionally equal you can use the
:meth:`~xenharmlib.core.note.NoteABC.is_notated_same` method:

.. testcode::

    assert n_edo12.note('D#', 0) == n_edo12.note('Eb', 0)

    assert not n_edo12.note('D#', 0).is_notated_same(
        n_edo12.note('Eb', 0)
    )

Notes have an interval method returning a note interval:

.. testcode::

    csharp1 = n_edo31.note('C#', 1)
    gsharp1 = n_edo31.note('G#', 1)
    gsharp1.interval(gsharp1)

.. testoutput::
    :hide:

Notes in UpDownNotation do **not** define addition, multiplication and
scalar multiplication, because the result is not well defined in
notation systems that have enharmonic ambigouity. (Other notations
without this problem might implement them). Notes can be transposed
through the transpose method by giving a note interval of the same
notation:

.. testcode::

    c0 = n_edo12.note('C', 0)
    g0 = n_edo12.note('G', 0)
    P5 = n_edo12.shorthand_interval('P', 5)

    assert g0 == c0.transpose(c0.interval(g0))
    assert g0 == c0.transpose(P5)

.. testoutput::
    :hide:

Notes of UpDownNotation have additional properties which they share
with all Notes from natural/accidental notations that pertain to
their 'split' definition. For example each note can be inspected in
regards to its natural and accidental fragments.

For example observe the difference in using the
:attr:`~xenharmlib.core.notes.PeriodicNoteABC.pc_index`
property and the
:attr:`~xenharmlib.core.notes.NatAccNote.nat_pc_index`
("natural pitch class index") property:

.. testcode::

    edo12_bsharp = n_edo12.note('B#', 0)
    print(edo12_bsharp.pc_index)
    print(edo12_bsharp.nat_pc_index)

.. testoutput::

    0
    11

The pitch class index of the note is 0, because the note refers to the
pitch index 12, which has pitch class 0 (the pitch class of 'C').
In the notation context however it is seen as a 'B' with an accidental
and 'B' has pitch class 11. You can use this to lump notes together
that are based on the same natural but have different accidentals

.. testcode::

    edo31_gsharp = n_edo31.note('G#', 2)
    edo31_gflat = n_edo31.note('Gb', 3)

    assert edo31_gsharp.nat_pc_index == edo31_gflat.nat_pc_index
 
.. testoutput::
    :hide:

You can see a similar effect when looking at the base interval index.
On natural/accidental notes it too comes in two flavors: One for the
actual pitch and one for the pitch of the natural:

.. testcode::

    edo12_bsharp = n_edo12.note('B#', 0)
    print(edo12_bsharp.bi_index)
    print(edo12_bsharp.nat_bi_index)

.. testoutput::

    1
    0

If you were paying close attention, you might have noticed that we
used 0 instead of 1 as the base interval when defining our note.
This convention of using the base interval index of the natural pitch,
rather than the actual pitch, is quite common, as seen in scientific
pitch notation, which forms the basis of xenharmlib's implementation.
You've probably grown so accustomed to it that you didn't even realize
until now.

Let's look at the accidentals: In general they signify a deviation
from a natural pitch, in UpDownNotation they signify a deviation
*in steps* from the natural pitch. You are probably familiar with
this from the traditional western system:

.. testcode::

    d_sharp = n_edo12.note('D#', 0)
    d_flat = n_edo12.note('Db', 0)

    print(d_sharp.acc_value)
    print(d_flat.acc_value)

.. testoutput::

    1
    -1

As expected the '#' symbol raises the note by one step, while the
'b' symbol flattens it by one step. Let's look at this in another
tuning:

.. testcode::

    d_sharp = n_edo31.note('D#', 0)
    d_flat = n_edo31.note('Db', 0)

    print(d_sharp.acc_value)
    print(d_flat.acc_value)

.. testoutput::

    2
    -2

What happened here? In 31-EDO, a step is much smaller compared to the
traditional 12-EDO Western tuning. If we were to map sharps and flats
to just one step in 31-EDO, it would deviate from the expected sound
too much, making it difficult to maintain a (somewhat) consistent
meaning for flats and sharps across different microtonal tunings.
The measure of the size of sharps and flats in EDO tunings is known as
"sharpness," and while 12-EDO has a sharpness of 1, 31-EDO has a
sharpness of 2. To move to the next pitch (upwards or downwards) in
31-EDO, one must use different accidentals:

.. testcode::

    d_up = n_edo31.note('^D', 0)
    d_down = n_edo31.note('vD', 0)

    print(d_up.acc_value)
    print(d_down.acc_value)

.. testoutput::

    1
    -1

Sometimes you also want to examine notes in regards to their symbols.
For this purpose natural/accidental notations like UpDownNotation have
three properties: One for the pitch class symbol, one for the natural
class symbol and one for the accidental:

.. testcode::

    print(n_edo31.note('^B#', 0).pc_symbol)
    print(n_edo31.note('^B#', 0).natc_symbol)
    print(n_edo31.note('^B#', 0).acc_symbol)

.. testoutput::

    ^B#
    B 
    ^#

Naturals have their own index system that is closely related
to the 'roman numeral system' but starting from 0 instead of 1.
In western piano terms: The natural index of a note is the number
of successive *white* key presses from the first natural to the
note while ignoring the accidental of the note:

.. testcode::

    print(n_edo31.note('D', 0).nat_index)
    print(n_edo31.note('D#', 1).nat_index)

.. testoutput::

    1
    8

You can see the relation to the roman numeral system easily when
you think of the way one traditionally calls the intervals from
C-0 to each note in the western system: The interval to the first note
in the example is called a major *second* while the interval to the
second one is called an augmented *ninth*.

Similar to pitch class indices there are also natural class indices.
The natural class index is a measure for when you want to ignore
base intervals and just look at the equivalency of naturals:

.. testcode::

    print(n_edo31.note('D', 0).natc_index)
    print(n_edo31.note('D#', 1).natc_index)
    print(n_edo31.note('vG', 1).natc_index)

.. testoutput::

    1
    1
    4

It follows from definition that notes with the same natural symbol
also have the same natural class index (as you can see with D-0, D#-1)
Natural class indices are especially useful when you are examining
compound intervals since they characterize the remainder in terms
of natural indices: An augmented *ninth* is only an augmented
*second* transposed one octave. 

Note Intervals
-----------------------------------

Today's common western interval notation is shaped by pretty old ideas
and has been handed down as a tradition for centuries without impactful
revisitation from a modern eye. Even though every new generation of
musicians struggles to understand the minute differences of perfect and
imperfect intervals the system is so deeply ingrained in western
harmonic analysis and composition that it is likely to stay for the
foreseeable future.

Fortunately xenharmlib's implementation of UpDownNotation takes a lot of
work from you when it comes to interval naming while also trying to
provide an interface that is more consistent in terms of mathematical
definitions.

When creating a note interval UpDownNotation automatically generates the
appropriate shorthand interval name:

.. testcode::

    edo31 = EDOTuning(31)
    n_edo31 = UpDownNotation(edo31)

    interval = n_edo31.note_interval(
        n_edo31.note('C', 0),
        n_edo31.note('G#', 0)
    )

    print(interval.shorthand_name)

.. testoutput::

    ('A', 5)


As an alternative to the notation builder method you can also use the
interval method of the Note object:

.. testcode::

    interval = n_edo31.note('C', 0).interval(
        n_edo31.note('^Ab', 0)
    )
    print(interval.shorthand_name) 

.. testoutput::

    ('^m', 6)

UpDownNotation also provides a builder method to create intervals
directly from their shorthand name:

.. testcode::

    P5 = n_edo12.shorthand_interval('P', 5)
    b0 = n_edo12.note('B', 0)
    print(b0.transpose(P5))

.. testoutput::

    UpDownNote(F#, 1, 12-EDO)

Note intervals are comparable and sortable by their frequency ratio:

.. testcode::

    edo12 = EDOTuning(12)
    n_edo12 = UpDownNotation(edo12)

    P4 = n_edo12.shorthand_interval('P', 4)
    A5 = n_edo12.shorthand_interval('A', 5)
    m6 = n_edo12.shorthand_interval('m', 6)

    assert P4 < A5
    assert A5 == m6

    edo31 = EDOTuning(31)
    n_edo31 = UpDownNotation(edo31)

    P5_12 = n_edo12.shorthand_interval('P', 5)
    P5_31 = n_edo31.shorthand_interval('P', 5)
    
    assert P5_31 < P5_12

.. testoutput::
    :hide:

Interval sortability can come in handy, for example if you want to sort
different EDOs according to the width of their fifth:

.. testcode::

    edos = [EDOTuning(n) for n in [12, 24, 31, 53]]
    n_edos = [UpDownNotation(e) for e in edos]

    sorted_n_edos = sorted(
        n_edos,
        key=lambda n_edo: n_edo.shorthand_interval('P', 5)
    )

    for n_edo in sorted_n_edos:
        print(n_edo, n_edo.shorthand_interval('P', 5).cents)

.. testoutput::

    UpDownNotation(31-EDO) 696.774193548401
    UpDownNotation(12-EDO) 700.0
    UpDownNotation(24-EDO) 700.0
    UpDownNotation(53-EDO) 701.8867924528022

You can also compare note intervals and pitch intervals:

.. testcode::

    P5_31 = n_edo31.shorthand_interval('P', 5)
    
    assert P5_31 < edo12.pitch_interval(
        edo12.pitch(0), edo12.pitch(7)
    )

.. testoutput::
    :hide:

Note intervals and pitch intervals expose the same basic properties,
so the object types can be used interchangeably in many cases. Here
is a short overview:

.. testcode::

    m3 = n_edo31.shorthand_interval('m', 3)
    assert m3.frequency_ratio == m3.pitch_interval.frequency_ratio
    assert m3.cents == m3.pitch_interval.cents
    assert m3.pitch_diff == m3.pitch_interval.pitch_diff

.. testoutput::
    :hide:

Like pitch intervals xenharmlib's implementation of intervals in
UpDownNotation have *directions*. This is necessary so the transpose
method of the Note object is well defined:

.. testcode::

    a = n_edo31.note('A', 1)
    c = n_edo31.note('C', 1)
    interval = a.interval(c)
    assert a.transpose(interval) == c

.. testoutput::
    :hide:

If intervals have downwards direction their naming changes accordingly.
The constructed interval above is a downward major 6:

.. testcode::

    print(interval.shorthand_name)
    
.. testoutput::

    ('M', -6)

Please note that this is something entirely different than inverting the
interval:

.. testcode::

    a = n_edo31.note('A', 0)
    c = n_edo31.note('C', 1)
    interval = a.interval(c)
    print(interval.shorthand_name)
    
.. testoutput::

    ('m', 3)

Note intervals also implement the :func:`abs` function, so downwards
intervals can be transformed into their upwards counterpart:

.. testcode::

    g0 = n_edo31.note('G', 0)
    c1 = n_edo31.note('C', 1)
    interval = c1.interval(g0)

    print(interval.shorthand_name)
    print(abs(interval).shorthand_name)
    
.. testoutput::

    ('P', -4)
    ('P', 4)

Note Scales
-----------------------------------

A set of unique, ordered notes is called a note scale. Note scales
work similar to pitch scales, however there are special considerations
necessary in light of enharmonic ambigouity. We will address these in
a subsection below. But first, let's create our first note scale:

.. testcode::

    Cm7 = n_edo12.note_scale(
        [n_edo12.note(s, 0) for s in ['C', 'Eb', 'G', 'Bb']]
    )
    
.. testoutput::
    :hide:

In terms of list operations note scales provide the same functionality
as pitch scales. Single notes and slices can be retrieved as if the
scale object was a python builtin list. The in operator works likewise
both with pitches, pitch intervals, notes and note intervals.

.. testcode::

    print(Cm7[1])
    print(Cm7[0:3])

    assert n_edo12.note('C', 0) in Cm7
    assert n_edo12.shorthand_interval('m', 3) in Cm7
    assert edo12.pitch(3) in Cm7
    assert edo12.pitch(1).interval(edo12.pitch(11)) in Cm7
    
.. testoutput::

    UpDownNote(Eb, 0, 12-EDO)
    UpDownNoteScale([C0, Eb0, G0], 12-EDO)

Scale comparisons work on the basis of note frequencies, so using the
equal sign will ignore enharmonic notation differences:

.. testcode::

    Cm = n_edo12.note_scale(
        [n_edo12.note(s, 0) for s in ['C', 'Eb', 'G']]
    )
    Cm_weird = n_edo12.note_scale(
        [n_edo12.note(s, 0) for s in ['C', 'D#', 'Abb']]
    )

    assert Cm == Cm_weird
    
.. testoutput::
    :hide:

If you want to test on equality *on the notation level* (ignoring
enharmonic equivalencies) you have to use the
:meth:`~xenharmlib.core.note_scale.NoteScale.is_notated_same`
method:

.. testcode::

    assert Cm.is_notated_same(Cm)
    assert not Cm.is_notated_same(Cm_weird)

.. testoutput::
    :hide:

You may be familiar with the method from the Note section. In fact a
lot of operations on single notes work on scales as well. This is
especially powerful when you want to transpose scales:

.. testcode::

    M7 = n_edo12.shorthand_interval('M', 7)
    Bm7 = Cm7.transpose(M7)
    print(Bm7)

.. testoutput::

    UpDownNoteScale([B0, D1, F#1, A1], 12-EDO)

Scales support rotation which can be useful if you want to explore
different ways to play a chord or alter the mode of a scale.

.. testcode::

    Cm7_G = Cm7.rotation(2)
    print(Cm7_G)

.. testoutput::

    UpDownNoteScale([G0, Bb0, C1, Eb1], 12-EDO)

In the context of natural/accidental notations you can use the
:meth:`~xenharmlib.core.notation.NatAccNotation.natural_scale` method
to generate a scale consisting of only the naturals in a base interval.
(In UpDownNotation this is simply the C-Major Scale). Together with the
:meth:`~xenharmlib.core.note_scale.PeriodicNoteScale.rotation` method
you can then generate the gregorian modes:

.. testcode::

    c_maj = n_edo12.natural_scale()

    print('ionian    ', c_maj)
    print('dorian    ', c_maj.rotation(1))
    print('phrygian  ', c_maj.rotation(2))
    print('lydian    ', c_maj.rotation(3))
    print('mixolydian', c_maj.rotation(4))
    print('aeolian   ', c_maj.rotation(5))

.. testoutput::

    ionian     UpDownNoteScale([C0, D0, E0, F0, G0, A0, B0], 12-EDO)
    dorian     UpDownNoteScale([D0, E0, F0, G0, A0, B0, C1], 12-EDO)
    phrygian   UpDownNoteScale([E0, F0, G0, A0, B0, C1, D1], 12-EDO)
    lydian     UpDownNoteScale([F0, G0, A0, B0, C1, D1, E1], 12-EDO)
    mixolydian UpDownNoteScale([G0, A0, B0, C1, D1, E1, F1], 12-EDO)
    aeolian    UpDownNoteScale([A0, B0, C1, D1, E1, F1, G1], 12-EDO)

Scales can be normalized to the first base interval which makes it
possible to compare scales on the level of tonal equivalencies:

.. testcode::

    c_maj = n_edo12.natural_scale(bi_index=1)
    a_min = c_maj.rotation(-2)

    norm_c_maj = c_maj.pcs_normalized()
    norm_a_min = a_min.pcs_normalized()
    assert norm_c_maj == norm_a_min

.. testoutput::
    :hide:

Note scales can be treated as sets. They support union, intersection,
difference and symmetric difference operations as well as subset,
superset and is_disjoint relationship tests.

As an illustration for set operations we want to make a deep dive into
John Coltrane's *Giant Steps* and find out why it is regarded as one
of the most difficult jazz work for improvisation.

Coltrane's composition is based on fast harmonic changes between the
scales B major (on chords B7, F#7, C#m7), G major (on chords G7, D7,
Am7) and Eb major (on chords Eb7, Bb7, Fm7). We want to know the notes
playable for improvisation in each of the three sections.

Initially, we'll construct the three major scales. To do this, we'll
start from a C major scale, which has the appropriate structure but the
incorrect key. Then, we'll transpose it to generate each of our desired
three scales. (Though we could define every scale explicitly, noting all
the notes, this approach is simpler and more elegant.)

.. testcode::

    C_maj = n_edo12.natural_scale()

    # make a shortcut for interval builder
    # method so we have less visual noise
    sh = n_edo12.shorthand_interval

    B_maj = C_maj.transpose(sh('M', 7))
    G_maj = C_maj.transpose(sh('P', 5))
    Eb_maj = C_maj.transpose(sh('m', 3))

We'll create the chords in a similar manner. There are just two types:
major dominant 7 and minor dominant 7. We'll define each type in C, then
transpose to obtain each chord.

.. testcode::

    C7 = n_edo12.note_scale(
        [n_edo12.note(s, 0) for s in ['C', 'E', 'G', 'Bb']]
    )
    Cm7 = n_edo12.note_scale(
        [n_edo12.note(s, 0) for s in ['C', 'Eb', 'G', 'Bb']]
    )

    # to be played with B major
    B7 = C7.transpose(sh('M', 7))
    Fsharp_7 = C7.transpose(sh('A', 4))
    Csharp_m7 = Cm7.transpose(sh('A', 1))

    # to be played with G major
    G7 = C7.transpose(sh('P', 5))
    D7 = C7.transpose(sh('M', 2))
    Am7 = Cm7.transpose(sh('M', 6))

    # to be played with Eb major
    Eb7 = C7.transpose(sh('m', 3))
    Bb7 = C7.transpose(sh('m', 7))
    Fm7 = Cm7.transpose(sh('P', 4))

We're going to follow a common practice for improvising over chords with
scales: we avoid using scale notes that clash with the chord tones by a
minor second. To do this, we'll use the scale's
:meth:`~xenharmlib.core.note_scale.PeriodicNoteScale.difference`
operation to filter them out.

.. testcode::

    def remove_avoid_notes(scale, chords):
        for chord in chords:
            avoid_scale = chord.transpose(sh('m',2))
            scale = scale.difference(
                avoid_scale, 
                ignore_bi_index=True
            )
        return scale

    # these three scales should be safe to play
    # on each of the respective chord sections

    B_maj_safe = remove_avoid_notes(B_maj, [B7, Fsharp_7, Csharp_m7])
    G_maj_safe = remove_avoid_notes(G_maj, [G7, D7, Am7])
    Eb_maj_safe = remove_avoid_notes(Eb_maj, [Eb7, Bb7, Fm7])

    print(B_maj_safe)
    print(G_maj_safe)
    print(Eb_maj_safe)

.. testoutput::

    UpDownNoteScale([C#1, D#1, F#1, G#1], 12-EDO)
    UpDownNoteScale([A0, B0, D1, E1], 12-EDO)
    UpDownNoteScale([F0, G0, Bb0, C1], 12-EDO)

We aim to determine if the improvisation scales have any notes in
common, indicating if there are notes we can play safely across two
consecutive sections. To test this, we're utilizing the
:meth:`~xenharmlib.core.note_scale.PeriodicNoteScale.is_disjoint`
method with the :code:`ignore_bi_index` flag set to True, treating notes
that differ only by base interval as the same:

.. testcode::

    print(B_maj_safe.is_disjoint(G_maj_safe, ignore_bi_index=True))
    print(B_maj_safe.is_disjoint(Eb_maj_safe, ignore_bi_index=True))
    print(Eb_maj_safe.is_disjoint(G_maj_safe, ignore_bi_index=True))

.. testoutput::

    True
    True
    True

As it turns out *none* of the improvisation scales have common notes
with any of the others, meaning the player has to change to a completely
different set of tones on each scale change.  

The mathematical beauty of Coltrane's composition becomes even more
apparent when we toss all the notes from the improvisation scales
together by utilizing the
:meth:`~xenharmlib.core.note_scale.NoteScale.union`
operator.

.. testcode::

    all_notes = B_maj_safe.union(G_maj_safe).union(Eb_maj_safe)
    norm = all_notes.pcs_normalized()
    print(norm)
    print(len(norm))

.. testoutput::

    UpDownNoteScale([C0, C#0, D0, D#0, E0, F0, F#0, G0, G#0, A0, Bb0, B0], 12-EDO)
    12

The set of improvisation notes over all sections is simply the full
chromatic scale, meaning that the three improvisation scales cut the
chromatic scale in 3 disjoint sets, each with 4 notes.

Enharmonic ambigouity and set operations
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

When we speak of enharmonic equivalence we mean that two notes refer
to the same pitch, but are notated differently, that is: we
differentiate between the sound of a note and its function.
The question if Eb and D# are *the same* can only be answered if
we further specify: Same in regards to what?

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

Xenharmlib tries to go a middle way. In regards to the uniqueness
restriction of the scale it refers to the :code:`==` equivalency,
while for some set operations it allows switching the equivalency
relation to :code:`is_notated_same`.

The reason for choosing the :code:`==` equivalency as the base for
the uniqueness property is to provide consistency with the underlying
pitch scale object:

.. testcode::

    e_flat = n_edo12.note('Eb', 0)
    d_sharp = n_edo12.note('D#', 0)

    scale_a = n_edo12.note_scale([e_flat])
    scale_b = n_edo12.note_scale([d_sharp])

    note_union = scale_a.union(scale_b)
    pitch_union = scale_a.pitch_scale.union(
        scale_b.pitch_scale
    )

    # among others, these would break if we would
    # treat Eb and D# distinct in note scales
    assert note_union.frequencies == pitch_union.frequencies
    assert len(note_union) == len(pitch_union)
    pitch_intervals = [
        i.pitch_interval for i in note_union.to_note_intervals()
    ]
    assert pitch_intervals == pitch_union.to_pitch_intervals()

.. testoutput::
    :hide:


This choice also allows to implement the scale's :code:`==` operator
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

    scale = n_edo12.note_scale(
        [
            n_edo12.note('D#', 0),
            n_edo12.note('Eb', 0),
        ]
    )
    assert len(scale) == 1
    assert scale[0].pc_symbol == 'D#'

.. testoutput::
    :hide:

When using set operations xenharmlib always prefers the representation
of the scale that executed the operation:

.. testcode::

    c = n_edo12.note('C', 0)
    g = n_edo12.note('G', 0)
    e_flat = n_edo12.note('Eb', 0)
    d_sharp = n_edo12.note('D#', 0)

    scale_a = n_edo12.note_scale([c, e_flat])
    scale_b = n_edo12.note_scale([d_sharp, g])

    # A v B / A ^ B

    union_a_b = scale_a.union(scale_b)
    assert union_a_b.is_notated_same(
        n_edo12.note_scale([c, e_flat, g])
    )

    intersection_a_b = scale_a.intersection(scale_b)
    assert intersection_a_b.is_notated_same(
        n_edo12.note_scale([e_flat])
    )

    # B v A / B ^ A

    union_b_a = scale_b.union(scale_a)
    assert union_b_a.is_notated_same(
        n_edo12.note_scale([c, d_sharp, g])
    )

    intersection_b_a = scale_b.intersection(scale_a)
    assert intersection_b_a.is_notated_same(
        n_edo12.note_scale([d_sharp])
    )

.. testoutput::
    :hide:

Using the :code:`==` operator we see that even though the results
are different in terms of representation, commutativity in regards
to union and intersection is still preserved:

.. testcode::

    assert union_a_b == union_b_a
    assert intersection_a_b == intersection_b_a

.. testoutput::
    :hide:

In contrast using the :code:`is_notated_same` equivalency relation
on the two result pairs does *not* preserve commutativity:

.. testcode::

    assert not union_a_b.is_notated_same(union_b_a)
    assert not intersection_a_b.is_notated_same(intersection_b_a)

.. testoutput::
    :hide:

Since we chose the :code:`==` operator as a basis for scale uniqueness,
there is no way to define a closed set algebra for the 
:code:`is_notated_same` relation at the same time, because the union
operation would not be well defined.

However on *certain* set operations we can define the option to use
the :code:`is_notated_same` relation. For :code:`intersection` we
can define that same-sounding, but differently notated notes should
not be part of the intersection. For :code:`difference` we can define
that such notes will not be removed from the first scale. In the
same way we can define the relationships :code:`is_disjoint`,
:code:`is_subset` and :code:`is_superset`.

The way this works is through the method flag :code:`is_notated_same`:

.. testcode::

    c = n_edo12.note('C', 0)
    g = n_edo12.note('G', 0)
    e_flat = n_edo12.note('Eb', 0)
    d_sharp = n_edo12.note('D#', 0)

    scale_a = n_edo12.note_scale([c, e_flat])
    scale_b = n_edo12.note_scale([d_sharp, g])

    intersection_a_b = scale_a.intersection(
        scale_b, is_notated_same=True
    )
    assert len(intersection_a_b) == 0

    diff_a_b = scale_a.difference(
        scale_b, is_notated_same=True
    )
    assert len(diff_a_b) == 2

.. testoutput::
    :hide:

In combination with the :code:`ignore_bi_index` flag we can for
example build a function that returns the pitch class symbols of
the common notes of two scales while being aware of the key:

.. testcode::

    def common_notes_key_aware(scale_a, scale_b):
        scale_i = scale_a.intersection(
            scale_b,
            is_notated_same=True,
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

Playing and Exporting
-----------------------------------

Sound synthesis and score composition are out of xenharmlib's scope,
however there are ways of hearing the things that you are building. 

You can export xenharmlib objects into various formats and even play
a sinewave audio from the console to get a feeling for the sound of
scales, chords and single notes. Sinewave sounds can be played on Mac,
Linux and Windows using the :func:`~xenharmlib.play.play` function:

.. testcode::

    from xenharmlib import EDOTuning
    from xenharmlib.play import play

    edo31 = EDOTuning(31)
    mothra_6 = edo31.pitch_scale(
        edo31.pitch_range(0, 31, 6)
    )

    # transpose into a mid frequency range
    mothra_6 = mothra_6.transpose(4*31)

    play(mothra_6)

.. raw:: html

   <audio controls="controls">
         <source src="_static/sounds/edo31_mothra_6.wav" type="audio/wav">
         Your browser does not support the <code>audio</code> element. 
   </audio>

The play function generally accepts every playable object (which are:
frequencies, pitches, notes, lists of the aforementioned and scales)
You can also change the duration a pitch is played and play scales
as a chord:

.. testcode::

    from xenharmlib import EDOTuning
    from xenharmlib.notation import UpDownNotation
    from xenharmlib.play import play

    edo12 = EDOTuning(12)
    edo31 = EDOTuning(31)

    n_edo12 = UpDownNotation(edo12)
    n_edo31 = UpDownNotation(edo31)

    edo12_chord = n_edo12.note_scale(
        [n_edo12.note(s, 4) for s in ['C', 'E', 'G', 'Bb']]
    )

    edo31_chord = n_edo31.note_scale(
        [n_edo31.note(s, 4) for s in ['C', 'E', 'G', 'vBb']]
    )

    # vBb approximates the harmonic series better than
    # Bb, so the second chord should sound a bit more
    # resonant

    play(edo12_chord, duration=2, play_as_chord=True)
    play(edo31_chord, duration=2, play_as_chord=True)

.. raw:: html

   <audio controls="controls">
         <source src="_static/sounds/edo12_C-E-G-Bb.wav" type="audio/wav">
         Your browser does not support the <code>audio</code> element. 
   </audio>

.. raw:: html

   <audio controls="controls">
         <source src="_static/sounds/edo31_C-E-G-vBb.wav" type="audio/wav">
         Your browser does not support the <code>audio</code> element. 
   </audio>

Sinewave audio can also be exported as a wav file with the
:func:`~xenharmlib.export.audio.export_wav` function, which supports
the same arguments as the play function:

.. code-block:: python

   from xenharmlib.export.audio import export_wav

   export_wav(
       'edo31_chord.wav',
       edo31_chord,
       duration=2,
       play_as_chord=True
   )


Scala Scale Format (.scl)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Xenharmlib also export to `Scala <https://www.huygens-fokker.org/scala/>`_'s
.scl format with :func:`~xenharmlib.export.scl.export_scl`. SCL files are
supported by a lot of audio synthesis software (e.g. Ableton Live's Microtuner
plugin)

.. code-block:: python

    from xenharmlib import EDOTuning
    from xenharmlib.export.scl import export_scl

    edo31 = EDOTuning(31)
    scale = edo31.pitch_scale(
        edo31.pitch_range(0, 31)
    )

    export_scl('./edo31.scl', scale, '31-EDO', ensure_period=True)

The third parameter gives a title to the SCL file. The :code:`ensure_period`
flag will make sure that the scale ends with a pitch equivalent to the first
pitch. (SCL works by iteratively stacking the scale definition on the last
pitch, so having a scale not ending with an equivalent pitch would cause the
last pitch being declared as the new 0 for the second iteration and make the
scale "move around").
