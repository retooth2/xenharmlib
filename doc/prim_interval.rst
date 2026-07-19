Intervals
============================================

Intervals describe the difference between two frequency representations,
for example the difference between C4 and E4 (a major third interval).
The main purpose of the interval primitive is to define the span and
harmonic function of a transposition.

Xenharmlib distinguishes between intervals that are enharmonically
equal to preserve their harmonic function, so an augmented second
and a minor third in Western notation produce different results in
regards to transposition, even though they describe the same
difference in pitch:

.. testcode:: WesternNotation

   from xenharmlib import WesternNotation
   western = WesternNotation()

   A2 = western.shorthand_interval('A', 2)
   m3 = western.shorthand_interval('m', 3)

   result_a = western.note('D', 4).transpose(A2)
   result_b = western.note('D', 4).transpose(m3)

   print(result_a)
   print(result_b)
   print(result_a == result_b)

.. testoutput:: WesternNotation

   WesternNote(E#, 4)
   WesternNote(F, 4)
   True

The interval primitive also supports various arithmetic operators and
transformation functions (for example inversion, compound-to-simple-mapping, 
intervals class normalization, etc). The following chapter will look at
intervals more in-depth and give examples on various origin contexts.

Deriving Intervals
-------------------------------------------------------

There are two way to derive an interval from two frequency representations:
One is the :meth:`~xenharmlib.core.origin_context.OriginContext.interval`
method of the origin context, the other is the
:meth:`~xenharmlib.core.freq_repr.FreqRepr.interval` method found directly
on the pitch or note:

.. tabs::

   .. tab:: EDO

      .. testcode:: EDOTuning

         from xenharmlib import EDOTuning
         edo31 = EDOTuning(31)

         p10 = edo31.pitch(10)
         p18 = edo31.pitch(18)

         interval_1 = edo31.interval(p10, p18)
         interval_2 = p10.interval(p18)

         print(interval_1)
         print(interval_2)

      .. testoutput:: EDOTuning

         EDOPitchInterval(8, 31-EDO)
         EDOPitchInterval(8, 31-EDO)

   .. tab:: Prime Limit

      .. testcode:: PrimeLimitTuning

         from xenharmlib import PrimeLimitTuning
         limit5 = PrimeLimitTuning(5)

         C0 = limit5.pitch(limit5.lattice.point((0, 0, 0)))
         G0 = limit5.pitch(limit5.lattice.point((-1, 1, 0)))

         interval_1 = limit5.interval(C0, G0)
         interval_2 = C0.interval(G0)

         print(interval_1)
         print(interval_2)

      .. testoutput:: PrimeLimitTuning

         PrimeLimitPitchInterval(3/2, 5-Limit)
         PrimeLimitPitchInterval(3/2, 5-Limit)

   .. tab:: Western

      .. testcode:: WesternNotation

         from xenharmlib import WesternNotation
         western = WesternNotation()

         C4 = western.note('C', 4)
         E4 = western.note('E', 4)

         interval_1 = western.interval(C4, E4)
         interval_2 = C4.interval(E4)

         print(interval_1)
         print(interval_2)

      .. testoutput:: WesternNotation

         WesternNoteInterval(M, 3)
         WesternNoteInterval(M, 3)

   .. tab:: UpDown

      .. testcode:: UpDownNotation

         from xenharmlib import EDOTuning
         from xenharmlib import UpDownNotation

         edo31 = EDOTuning(31)
         n_edo31 = UpDownNotation(edo31)

         C4 = n_edo31.note('C', 4)
         Eup4 = n_edo31.note('^E', 4)

         interval_1 = n_edo31.interval(C4, Eup4)
         interval_2 = C4.interval(Eup4)

         print(interval_1)
         print(interval_2)

      .. testoutput:: UpDownNotation

         UpDownNoteInterval(^M, 3, 31-EDO)
         UpDownNoteInterval(^M, 3, 31-EDO)

Depending on tuning and notation there are other *direct* builder methods
available to create intervals. While in every origin context intervals
can be derived from two frequency representations direct methods are
highly dependend on context.


Difference-based Construction
-------------------------------------------------------

You can create intervals by providing the pitch difference using the
:meth:`~xenharmlib.core.origin_context.OriginContext.diff_interval`
method. Depending on the index scheme, this pitch difference can
be an integer or a :class:`~xenharmlib.core.lattice.LatticePoint` object:

.. tabs::

   .. tab:: EDO

      .. testcode:: EDOTuning

         from xenharmlib import EDOTuning
         edo31 = EDOTuning(31)

         P5 = edo31.diff_interval(18)
         print(P5)

      .. testoutput:: EDOTuning

         EDOPitchInterval(18, 31-EDO)

   .. tab:: Prime Limit

      .. testcode:: PrimeLimitTuning

         from xenharmlib import PrimeLimitTuning
         limit5 = PrimeLimitTuning(5)

         P5 = limit5.diff_interval(limit5.lattice.point((-1, 1, 0)))
         print(P5)

      .. testoutput:: PrimeLimitTuning

         PrimeLimitPitchInterval(3/2, 5-Limit)

   .. tab:: Western

      .. testcode:: WesternNotation

         from xenharmlib import WesternNotation
         western = WesternNotation()

         P5 = western.diff_interval(7)
         print(P5)

      .. testoutput:: WesternNotation

         WesternNoteInterval(P, 5)

   .. tab:: UpDown

      .. testcode:: UpDownNotation

         from xenharmlib import EDOTuning
         from xenharmlib import UpDownNotation

         edo31 = EDOTuning(31)
         n_edo31 = UpDownNotation(edo31)

         P5 = n_edo31.diff_interval(18)
         print(P5)

      .. testoutput:: UpDownNotation

         UpDownNoteInterval(P, 5, 31-EDO)

In notations where there is enharmonic ambiguity (e.g. the western notation)
the result can vary depending on the configured enharmonic strategy of the
notation, i.e. a pitch difference of 4 can be interpreted as a m3 interval
or an A2 interval. Since there is no way of knowing the harmonic function
of an interval given in absolute pitch difference, xenharmlib makes a guess.

For tunings and notations whose pitch differences are represented by lattice
points xenharmlib provides also the more concise
:meth:`~xenharmlib.core.multigen.MultiGenTuning.vec_interval` method:

.. testcode:: PrimeLimitTuning

     from xenharmlib import PrimeLimitTuning
     limit5 = PrimeLimitTuning(5)

     # these two expressions create the same object
     P5 = limit5.diff_interval(limit5.lattice.point((-1, 1, 0)))
     P5_alt = limit5.vec_interval((-1, 1, 0))

Name-based Construction
-------------------------------------------------------

On the notation layer intervals can also be created by their shorthand
name. In fact every notation in xenharmlib comes with an interval naming
scheme, so - like notes - every interval has a distinct name from which
it can be uniquely identified. Details about the interval naming scheme
can be obtained from the relevant notation chapter of this documentation.

.. tabs::

   .. tab:: Western

      .. testcode:: WesternNotation

         from xenharmlib import WesternNotation
         western = WesternNotation()

         P5 = western.shorthand_interval('P', 5)
         print(P5)

      .. testoutput:: WesternNotation

         WesternNoteInterval(P, 5)

   .. tab:: UpDown

      .. testcode:: UpDownNotation

         from xenharmlib import EDOTuning
         from xenharmlib import UpDownNotation

         edo31 = EDOTuning(31)
         n_edo31 = UpDownNotation(edo31)

         supermajor3 = n_edo31.shorthand_interval('^M', 3)
         print(supermajor3)

      .. testoutput:: UpDownNotation

         UpDownNoteInterval(^M, 3, 31-EDO)

Construction Based on Closest Frequency Ratio
-----------------------------------------------------

Origin contexts based on integer indices allow construction based on the
approximation of frequency ratios. Given an arbitrary frequency ratio the
:meth:`~xenharmlib.core.origin_context.OriginContext.closest_interval`
method returns the interval of an origin context that is closest to it:

.. tabs::

   .. tab:: EDO

      .. testcode:: EDOTuning

         from xenharmlib import EDOTuning
         from xenharmlib import FrequencyRatio

         edo31 = EDOTuning(31)
         interval = edo31.closest_interval(FrequencyRatio(7, 4))
         print(interval)

      .. testoutput:: EDOTuning

         EDOPitchInterval(25, 31-EDO)

   .. tab:: Western

      .. testcode:: WesternNotation

         from xenharmlib import WesternNotation
         from xenharmlib import FrequencyRatio

         western = WesternNotation()
         interval = western.closest_interval(FrequencyRatio(3, 2))
         print(interval)

      .. testoutput:: WesternNotation

         WesternNoteInterval(P, 5)

   .. tab:: UpDown

      .. testcode:: UpDownNotation

         from xenharmlib import EDOTuning
         from xenharmlib import UpDownNotation
         from xenharmlib import FrequencyRatio

         edo31 = EDOTuning(31)
         n_edo31 = UpDownNotation(edo31)
         interval = n_edo31.closest_interval(FrequencyRatio(5, 4))
         print(interval)

      .. testoutput:: UpDownNotation

         UpDownNoteInterval(M, 3, 31-EDO)

Simple and Compound
-----------------------------------------------------------

In relation to an equivalency interval intervals can be categorized into
"simple intervals" (smaller or equal to the equivalency interval) or
"compound intervals" (bigger than the equivalency interval). In the
western system for example M2 is a simple interval while M9 is a
compound interval.

.. tabs::

   .. tab:: EDO

      .. testcode:: EDOTuning

         from xenharmlib import EDOTuning
         edo31 = EDOTuning(31)

         interval = edo31.diff_interval(33)

         print(interval.is_simple)
         print(interval.is_compound)

      .. testoutput:: EDOTuning

         False
         True

   .. tab:: Prime Limit

      .. testcode:: PrimeLimitTuning

         from xenharmlib import PrimeLimitTuning
         limit5 = PrimeLimitTuning(5)

         interval = limit5.diff_interval(limit5.lattice.point((0, 1, 0)))

         print(interval.is_simple)
         print(interval.is_compound)

      .. testoutput:: PrimeLimitTuning

         False
         True

   .. tab:: Western

      .. testcode:: WesternNotation

         from xenharmlib import WesternNotation
         western = WesternNotation()

         interval = western.shorthand_interval('M', 9)
         print(interval.is_simple)
         print(interval.is_compound)

      .. testoutput:: WesternNotation

         False
         True

   .. tab:: UpDown

      .. testcode:: UpDownNotation

         from xenharmlib import EDOTuning
         from xenharmlib import UpDownNotation

         edo31 = EDOTuning(31)
         n_edo31 = UpDownNotation(edo31)

         interval = n_edo31.shorthand_interval('^M', 9)
         print(interval.is_simple)
         print(interval.is_compound)

      .. testoutput:: UpDownNotation

         False
         True

Compound intervals can be reduced to their simple equivalent easily.
For example in the western system M9 has the simple interval equivalent
of M2:

.. tabs::

   .. tab:: EDO

      .. testcode:: EDOTuning

         from xenharmlib import EDOTuning
         edo31 = EDOTuning(31)

         interval = edo31.diff_interval(33)
         simple = interval.to_simple()

         print(simple)

      .. testoutput:: EDOTuning

         EDOPitchInterval(2, 31-EDO)

   .. tab:: Prime Limit

      .. testcode:: PrimeLimitTuning

         from xenharmlib import PrimeLimitTuning
         limit5 = PrimeLimitTuning(5)

         interval = limit5.diff_interval(limit5.lattice.point((0, 1, 0)))
         simple = interval.to_simple()

         print(simple)

      .. testoutput:: PrimeLimitTuning

         PrimeLimitPitchInterval(3/2, 5-Limit)

   .. tab:: Western

      .. testcode:: WesternNotation

         from xenharmlib import WesternNotation
         western = WesternNotation()

         interval = western.shorthand_interval('M', 9)
         simple = interval.to_simple()

         print(simple)

      .. testoutput:: WesternNotation

         WesternNoteInterval(M, 2)

   .. tab:: UpDown

      .. testcode:: UpDownNotation

         from xenharmlib import EDOTuning
         from xenharmlib import UpDownNotation

         edo31 = EDOTuning(31)
         n_edo31 = UpDownNotation(edo31)

         interval = n_edo31.shorthand_interval('^M', 9)
         simple = interval.to_simple()

         print(simple)

      .. testoutput:: UpDownNotation

         UpDownNoteInterval(^M, 2, 31-EDO)


Direction, Inversion & Absolute
-----------------------------------------------------------

Intervals in xenharmlib are *directional* meaning there is a difference
between ascending and descending intervals. Each ascending interval has
its descending counterpart and vice versa. Whether you receive an ascending
or descending interval depends on the order of the notes from which
an interval is constructed. If the first note is lower than the second,
you will receive an ascending interval. If the first note is higher than
the second you will receive a descending interval:

.. tabs::

   .. tab:: EDO

      .. testcode:: EDOTuning

         from xenharmlib import EDOTuning
         edo31 = EDOTuning(31)

         p10 = edo31.pitch(10)
         p18 = edo31.pitch(18)

         ascending = p10.interval(p18)
         descending = p18.interval(p10)

         print(ascending)
         print(descending)

      .. testoutput:: EDOTuning

         EDOPitchInterval(8, 31-EDO)
         EDOPitchInterval(-8, 31-EDO)

   .. tab:: Prime Limit

      .. testcode:: PrimeLimitTuning

         from xenharmlib import PrimeLimitTuning
         limit5 = PrimeLimitTuning(5)

         C0 = limit5.pitch(limit5.lattice.point((0, 0, 0)))
         G0 = limit5.pitch(limit5.lattice.point((-1, 1, 0)))

         ascending = C0.interval(G0)
         descending = G0.interval(C0)

         print(ascending)
         print(descending)

      .. testoutput:: PrimeLimitTuning

         PrimeLimitPitchInterval(3/2, 5-Limit)
         PrimeLimitPitchInterval(2/3, 5-Limit)

   .. tab:: Western

      .. testcode:: WesternNotation

         from xenharmlib import WesternNotation
         western = WesternNotation()

         C4 = western.note('C', 4)
         E4 = western.note('E', 4)

         ascending = C4.interval(E4)
         descending = E4.interval(C4)

         print(ascending)
         print(descending)

      .. testoutput:: WesternNotation

         WesternNoteInterval(M, 3)
         WesternNoteInterval(M, -3)

   .. tab:: UpDown

      .. testcode:: UpDownNotation

         from xenharmlib import EDOTuning
         from xenharmlib import UpDownNotation

         edo31 = EDOTuning(31)
         n_edo31 = UpDownNotation(edo31)

         C4 = n_edo31.note('C', 4)
         Eup4 = n_edo31.note('^E', 4)

         ascending = C4.interval(Eup4)
         descending = Eup4.interval(C4)

         print(ascending)
         print(descending)

      .. testoutput:: UpDownNotation

         UpDownNoteInterval(^M, 3, 31-EDO)
         UpDownNoteInterval(^M, -3, 31-EDO)

An ascending interval can be transformed into a descending interval 
(and vice versa) by prefixing the interval object with a minus
(:code:`-`) sign. For an interval :code:`X` we call the object
:code:`-X` the *negation* of :code:`X`, with :code:`X + (-X)`
always resulting in the unison interval:

.. tabs::

   .. tab:: EDO

      .. testcode:: EDOTuning

         from xenharmlib import EDOTuning
         edo31 = EDOTuning(31)

         p10 = edo31.pitch(10)
         p18 = edo31.pitch(18)

         ascending = p10.interval(p18)
         descending = -ascending

         print(ascending)
         print(descending)
         print(ascending + descending)

      .. testoutput:: EDOTuning

         EDOPitchInterval(8, 31-EDO)
         EDOPitchInterval(-8, 31-EDO)
         EDOPitchInterval(0, 31-EDO)

   .. tab:: Prime Limit

      .. testcode:: PrimeLimitTuning

         from xenharmlib import PrimeLimitTuning
         limit5 = PrimeLimitTuning(5)

         C0 = limit5.pitch(limit5.lattice.point((0, 0, 0)))
         G0 = limit5.pitch(limit5.lattice.point((-1, 1, 0)))

         ascending = C0.interval(G0)
         descending = -ascending

         print(ascending)
         print(descending)
         print(ascending + descending)

      .. testoutput:: PrimeLimitTuning

         PrimeLimitPitchInterval(3/2, 5-Limit)
         PrimeLimitPitchInterval(2/3, 5-Limit)
         PrimeLimitPitchInterval(1, 5-Limit)

   .. tab:: Western

      .. testcode:: WesternNotation

         from xenharmlib import WesternNotation
         western = WesternNotation()

         C4 = western.note('C', 4)
         E4 = western.note('E', 4)

         ascending = C4.interval(E4)
         descending = -ascending

         print(ascending)
         print(descending)
         print(ascending + descending)

      .. testoutput:: WesternNotation

         WesternNoteInterval(M, 3)
         WesternNoteInterval(M, -3)
         WesternNoteInterval(P, 1)

   .. tab:: UpDown

      .. testcode:: UpDownNotation

         from xenharmlib import EDOTuning
         from xenharmlib import UpDownNotation

         edo31 = EDOTuning(31)
         n_edo31 = UpDownNotation(edo31)

         C4 = n_edo31.note('C', 4)
         Eup4 = n_edo31.note('^E', 4)

         ascending = C4.interval(Eup4)
         descending = -ascending

         print(ascending)
         print(descending)
         print(ascending + descending)

      .. testoutput:: UpDownNotation

         UpDownNoteInterval(^M, 3, 31-EDO)
         UpDownNoteInterval(^M, -3, 31-EDO)
         UpDownNoteInterval(P, 1, 31-EDO)

Interval objects provide the :attr:`~xenharmlib.core.intervals.Interval.sign`
property to inspect the direction of an interval, returning 1 for an
ascending interval, -1 for a descending interval and 0 for the unison
interval.

.. tabs::

   .. tab:: EDO

      .. testcode:: EDOTuning

         from xenharmlib import EDOTuning
         edo31 = EDOTuning(31)

         p10 = edo31.pitch(10)
         p18 = edo31.pitch(18)

         ascending = p10.interval(p18)
         descending = -ascending
         unison = p10.interval(p10)

         print(ascending.sign)
         print(descending.sign)
         print(unison.sign)

      .. testoutput:: EDOTuning

         1
         -1
         0

   .. tab:: Prime Limit

      .. testcode:: PrimeLimitTuning

         from xenharmlib import PrimeLimitTuning
         limit5 = PrimeLimitTuning(5)

         C0 = limit5.pitch(limit5.lattice.point((0, 0, 0)))
         G0 = limit5.pitch(limit5.lattice.point((-1, 1, 0)))

         ascending = C0.interval(G0)
         descending = -ascending
         unison = C0.interval(C0)

         print(ascending.sign)
         print(descending.sign)
         print(unison.sign)


      .. testoutput:: PrimeLimitTuning

         1
         -1
         0

   .. tab:: Western

      .. testcode:: WesternNotation

         from xenharmlib import WesternNotation
         western = WesternNotation()

         C4 = western.note('C', 4)
         E4 = western.note('E', 4)

         ascending = C4.interval(E4)
         descending = -ascending
         unison = C4.interval(C4)

         print(ascending.sign)
         print(descending.sign)
         print(unison.sign)

      .. testoutput:: WesternNotation

         1
         -1
         0

   .. tab:: UpDown

      .. testcode:: UpDownNotation

         from xenharmlib import EDOTuning
         from xenharmlib import UpDownNotation

         edo31 = EDOTuning(31)
         n_edo31 = UpDownNotation(edo31)

         C4 = n_edo31.note('C', 4)
         Eup4 = n_edo31.note('^E', 4)

         ascending = C4.interval(Eup4)
         descending = -ascending
         unison = C4.interval(C4)

         print(ascending.sign)
         print(descending.sign)
         print(unison.sign)

      .. testoutput:: UpDownNotation

         1
         -1
         0

Intervals support the :code:`abs()` function that returns the corresponding
ascending interval for a descending interval (or the interval itself if
it is already ascending or unison)

.. tabs::

   .. tab:: EDO

      .. testcode:: EDOTuning

         from xenharmlib import EDOTuning
         edo31 = EDOTuning(31)

         p10 = edo31.pitch(10)
         p18 = edo31.pitch(18)

         descending = p18.interval(p10)
         ascending = abs(descending)

         print(descending)
         print(ascending)

      .. testoutput:: EDOTuning

         EDOPitchInterval(-8, 31-EDO)
         EDOPitchInterval(8, 31-EDO)

   .. tab:: Prime Limit

      .. testcode:: PrimeLimitTuning

         from xenharmlib import PrimeLimitTuning
         limit5 = PrimeLimitTuning(5)

         C0 = limit5.pitch(limit5.lattice.point((0, 0, 0)))
         G0 = limit5.pitch(limit5.lattice.point((-1, 1, 0)))

         descending = G0.interval(C0)
         ascending = abs(descending)

         print(descending)
         print(ascending)

      .. testoutput:: PrimeLimitTuning

         PrimeLimitPitchInterval(2/3, 5-Limit)
         PrimeLimitPitchInterval(3/2, 5-Limit)

   .. tab:: Western

      .. testcode:: WesternNotation

         from xenharmlib import WesternNotation
         western = WesternNotation()

         C4 = western.note('C', 4)
         E4 = western.note('E', 4)

         descending = E4.interval(C4)
         ascending = abs(descending)

         print(descending)
         print(ascending)

      .. testoutput:: WesternNotation

         WesternNoteInterval(M, -3)
         WesternNoteInterval(M, 3)

   .. tab:: UpDown

      .. testcode:: UpDownNotation

         from xenharmlib import EDOTuning
         from xenharmlib import UpDownNotation

         edo31 = EDOTuning(31)
         n_edo31 = UpDownNotation(edo31)

         C4 = n_edo31.note('C', 4)
         Eup4 = n_edo31.note('^E', 4)

         descending = Eup4.interval(C4)
         ascending = abs(descending)

         print(descending)
         print(ascending)

      .. testoutput:: UpDownNotation

         UpDownNoteInterval(^M, -3, 31-EDO)
         UpDownNoteInterval(^M, 3, 31-EDO)

In contrast inversion of an interval :code:`X` is defined as the interval
:code:`Y`, so that :code:`X + Y` equals the *equivalency interval* [#f1]_.

.. tabs::

   .. tab:: EDO

      .. testcode:: EDOTuning

         from xenharmlib import EDOTuning
         edo31 = EDOTuning(31)

         p10 = edo31.pitch(10)
         p18 = edo31.pitch(18)

         interval = p10.interval(p18)
         inv_interval = interval.inversion()

         print(interval)
         print(inv_interval)
         print(interval + inv_interval)

      .. testoutput:: EDOTuning

         EDOPitchInterval(8, 31-EDO)
         EDOPitchInterval(23, 31-EDO)
         EDOPitchInterval(31, 31-EDO)

   .. tab:: Prime Limit

      .. testcode:: PrimeLimitTuning

         from xenharmlib import PrimeLimitTuning
         limit5 = PrimeLimitTuning(5)

         C0 = limit5.pitch(limit5.lattice.point((0, 0, 0)))
         G0 = limit5.pitch(limit5.lattice.point((-1, 1, 0)))

         interval = C0.interval(G0)
         inv_interval = interval.inversion()

         print(interval)
         print(inv_interval)
         print(interval + inv_interval)

      .. testoutput:: PrimeLimitTuning

         PrimeLimitPitchInterval(3/2, 5-Limit)
         PrimeLimitPitchInterval(4/3, 5-Limit)
         PrimeLimitPitchInterval(2, 5-Limit)

   .. tab:: Western

      .. testcode:: WesternNotation

         from xenharmlib import WesternNotation
         western = WesternNotation()

         C4 = western.note('C', 4)
         E4 = western.note('E', 4)

         interval = C4.interval(E4)
         inv_interval = interval.inversion()

         print(interval)
         print(inv_interval)
         print(interval + inv_interval)

      .. testoutput:: WesternNotation

         WesternNoteInterval(M, 3)
         WesternNoteInterval(m, 6)
         WesternNoteInterval(P, 8)

   .. tab:: UpDown

      .. testcode:: UpDownNotation

         from xenharmlib import EDOTuning
         from xenharmlib import UpDownNotation

         edo31 = EDOTuning(31)
         n_edo31 = UpDownNotation(edo31)

         C4 = n_edo31.note('C', 4)
         Eup4 = n_edo31.note('^E', 4)

         interval = C4.interval(Eup4)
         inv_interval = interval.inversion()

         print(interval)
         print(inv_interval)
         print(interval + inv_interval)

      .. testoutput:: UpDownNotation

         UpDownNoteInterval(^M, 3, 31-EDO)
         UpDownNoteInterval(vm, 6, 31-EDO)
         UpDownNoteInterval(P, 8, 31-EDO)

Identity and Comparison
-----------------------------------------------------------

While pitch and note objects are representations of frequencies,
intervals are representations of frequency ratios. Similar to
pitches and notes, two intervals are considered equal if their
:attr:`~xenharmlib.core.interval.Interval.frequency_ratio` property
is equal. This equality relation works across different origin
contexts:

.. tabs::

   .. tab:: EDO

      .. testcode:: EDOTuning

         from xenharmlib import EDOTuning
         edo12 = EDOTuning(12)
         edo24 = EDOTuning(24)

         P5_12 = edo12.diff_interval(7)
         P5_24 = edo24.diff_interval(14)

         print(P5_12.frequency_ratio)
         print(P5_24.frequency_ratio)
         print(P5_12 == P5_24)

      .. testoutput:: EDOTuning

         FrequencyRatio(2**(7/12))
         FrequencyRatio(2**(7/12))
         True

   .. tab:: Prime Limit

      .. testcode:: PrimeLimitTuning

         from xenharmlib import PrimeLimitTuning
         limit3 = PrimeLimitTuning(3)
         limit5 = PrimeLimitTuning(5)

         P5_l3 = limit3.vec_interval((-1, 1))
         P5_l5 = limit5.vec_interval((-1, 1, 0))

         print(P5_l3.frequency_ratio)
         print(P5_l5.frequency_ratio)
         print(P5_l3 == P5_l5)

      .. testoutput:: PrimeLimitTuning

         FrequencyRatio(3/2)
         FrequencyRatio(3/2)
         True

   .. tab:: UpDown

      .. testcode:: UpDownNotation

         from xenharmlib import EDOTuning
         from xenharmlib import UpDownNotation

         edo24 = EDOTuning(24)
         edo48 = EDOTuning(48)
         n_edo24 = UpDownNotation(edo24)
         n_edo48 = UpDownNotation(edo48)

         interval_24 = n_edo24.shorthand_interval('^M', 3)
         interval_48 = n_edo48.shorthand_interval('^^M', 3)

         print(interval_24.frequency_ratio)
         print(interval_48.frequency_ratio)
         print(interval_24 == interval_48)

      .. testoutput:: UpDownNotation

         FrequencyRatio(2**(3/8))
         FrequencyRatio(2**(3/8))
         True

Likewise comparison operators work by comparing frequency ratios:

.. tabs::

   .. tab:: EDO

      .. testcode:: EDOTuning

         from xenharmlib import EDOTuning
         edo12 = EDOTuning(12)

         P5 = edo12.diff_interval(7)
         M3 = edo12.diff_interval(4)

         print(M3 < P5)
         print(M3 > P5)

      .. testoutput:: EDOTuning

         True
         False

   .. tab:: Prime Limit

      .. testcode:: PrimeLimitTuning

         from xenharmlib import PrimeLimitTuning
         limit3 = PrimeLimitTuning(3)
         limit5 = PrimeLimitTuning(5)

         P5 = limit5.vec_interval((-1, 1, 0))
         M3pure = limit5.vec_interval((-2, 0, 1))

         print(M3pure < P5)
         print(M3pure > P5)

      .. testoutput:: PrimeLimitTuning

         True
         False

   .. tab:: UpDown

      .. testcode:: UpDownNotation

         from xenharmlib import EDOTuning
         from xenharmlib import UpDownNotation

         edo31 = EDOTuning(31)
         n_edo31 = UpDownNotation(edo31)

         P5 = n_edo31.shorthand_interval('P', 5)
         M3 = n_edo31.shorthand_interval('M', 3)

         print(M3 < P5)
         print(M3 > P5)

      .. testoutput:: UpDownNotation

         True
         False

Since descending intervals are inverting the frequency ratio of their
ascending counterpart (e.g. negating a ascending pure fifth with ratio
:math:`\frac{3}{2}` we will receive a descending pure fifth with
ratio :math:`\frac{2}{3}`) descending frequencies are always
considered smaller than the unison interval, even if they might
be bigger in *absolute* size:

.. tabs::

   .. tab:: EDO

      .. testcode:: EDOTuning

         from xenharmlib import EDOTuning
         edo12 = EDOTuning(12)

         desc_P5 = edo12.diff_interval(-7)
         P1 = edo12.diff_interval(0)

         print(desc_P5 < P1)

      .. testoutput:: EDOTuning

         True

   .. tab:: Prime Limit

      .. testcode:: PrimeLimitTuning

         from xenharmlib import PrimeLimitTuning
         limit5 = PrimeLimitTuning(5)

         desc_P5 = limit5.vec_interval((1, -1, 0))
         P1 = limit5.vec_interval((0, 0, 0))

         print(desc_P5 < P1)

      .. testoutput:: PrimeLimitTuning

         True

   .. tab:: UpDown

      .. testcode:: UpDownNotation

         from xenharmlib import EDOTuning
         from xenharmlib import UpDownNotation

         edo31 = EDOTuning(31)
         n_edo31 = UpDownNotation(edo31)

         desc_P5 = n_edo31.shorthand_interval('P', -5)
         P1 = n_edo31.shorthand_interval('P', 1)

         print(desc_P5 < P1)

      .. testoutput:: UpDownNotation

         True

Subtraction and Addition
-----------------------------------------------------------

Intervals support addition and subtraction. The plus (:code:`+`) operator
stacks two intervals on top of one another, meaning that transposing by the
sum of two intervals is the same as transposing first by the first interval
and then by the second. The minus (:code:`-`) operator is defined as the
addition of the negation of the second interval, i.e. transposing by
:math:`X-Y` is equal to transposing by :math:`X` first and then
transposing by :math:`-Y`

.. tabs::

   .. tab:: EDO

      .. testcode:: EDOTuning

         from xenharmlib import EDOTuning
         edo31 = EDOTuning(31)

         interval_a = edo31.diff_interval(9)
         interval_b = edo31.diff_interval(7)

         print(interval_a + interval_b)
         print(interval_a - interval_b)

      .. testoutput:: EDOTuning

         EDOPitchInterval(16, 31-EDO)
         EDOPitchInterval(2, 31-EDO)

   .. tab:: Prime Limit

      .. testcode:: PrimeLimitTuning

         from xenharmlib import PrimeLimitTuning
         limit5 = PrimeLimitTuning(5)

         P5 = limit5.diff_interval(limit5.lattice.point((-1, 1, 0)))
         M3_pure = limit5.diff_interval(limit5.lattice.point((-2, 0, 1)))

         print(P5 + M3_pure)
         print(P5 - M3_pure)

      .. testoutput:: PrimeLimitTuning

         PrimeLimitPitchInterval(15/8, 5-Limit)
         PrimeLimitPitchInterval(6/5, 5-Limit)

   .. tab:: Western

      .. testcode:: WesternNotation

         from xenharmlib import WesternNotation
         western = WesternNotation()

         m3 = western.shorthand_interval('m', 3)
         M3 = western.shorthand_interval('M', 3)

         print(M3 + m3)
         print(M3 - m3)

      .. testoutput:: WesternNotation

         WesternNoteInterval(P, 5)
         WesternNoteInterval(A, 1)

   .. tab:: UpDown

      .. testcode:: UpDownNotation

         from xenharmlib import EDOTuning
         from xenharmlib import UpDownNotation

         edo31 = EDOTuning(31)
         n_edo31 = UpDownNotation(edo31)

         up_M3 = n_edo31.shorthand_interval('^M', 3)
         down_m3 = n_edo31.shorthand_interval('vm', 3)

         print(up_M3 + down_m3)
         print(up_M3 - down_m3)

      .. testoutput:: UpDownNotation

         UpDownNoteInterval(P, 5, 31-EDO)
         UpDownNoteInterval(^^A, 1, 31-EDO)


Continued Stacking / Multiplication
-----------------------------------------------------------

Intervals can be multiplied by an integer, which is the same as stacking
an interval upon itself a number of times. Continued stacking of the same
interval has many applications for example in the circle of fifths or
the generation of scales:

.. tabs::

   .. tab:: EDO

      .. testcode:: EDOTuning

         from xenharmlib import EDOTuning
         edo31 = EDOTuning(31)

         P5 = edo31.diff_interval(18)

         print(3 * P5)

      .. testoutput:: EDOTuning

         EDOPitchInterval(54, 31-EDO)

   .. tab:: Prime Limit

      .. testcode:: PrimeLimitTuning

         from xenharmlib import PrimeLimitTuning
         limit5 = PrimeLimitTuning(5)

         P5 = limit5.diff_interval(limit5.lattice.point((-1, 1, 0)))

         print(3 * P5)

      .. testoutput:: PrimeLimitTuning

         PrimeLimitPitchInterval(27/8, 5-Limit)

   .. tab:: Western

      .. testcode:: WesternNotation

         from xenharmlib import WesternNotation
         western = WesternNotation()

         P5 = western.shorthand_interval('P', 5)

         print(3 * P5)

      .. testoutput:: WesternNotation

         WesternNoteInterval(M, 13)

   .. tab:: UpDown

      .. testcode:: UpDownNotation

         from xenharmlib import EDOTuning
         from xenharmlib import UpDownNotation

         edo31 = EDOTuning(31)
         n_edo31 = UpDownNotation(edo31)

         up_M3 = n_edo31.shorthand_interval('^M', 3)

         print(3 * up_M3)

      .. testoutput:: UpDownNotation

         UpDownNoteInterval(^^^A, 7, 31-EDO)


Interval Class Calculation
-----------------------------------------------------------

Similar to pitch classes that represent sets of equivalent pitches,
intervals can be sorted into interval classes that represent intervals
of the same "intervallic content" or "color". This equivalency is
defined as follows:

* Two intervals that only differ in direction belong inside the
  same class (C1 to G1 has the same color as G1 to C1)
* If one interval is the simplified version of another compound
  interval they belong inside the same class (C1 to G1 has the
  same color as C1 to G2 or C1 to G5)
* If one interval is the inversion of another they belong into
  the same class (C1 to G1 has the same color as G1 to C2)

Each interval class has a normalized representative that is
calculated from an interval of the same class as follows:

1. Calculate the absolute of the interval
2. Transform the result into a simple interval
3. Compare the result and its inversion and choose whichever is smaller

.. tabs::

   .. tab:: EDO

      .. testcode:: EDOTuning

         from xenharmlib import EDOTuning
         edo31 = EDOTuning(31)

         interval = edo31.diff_interval(-18)
         ic = interval.ic_normalized()
         print(ic)

      .. testoutput:: EDOTuning

         EDOPitchInterval(13, 31-EDO)

   .. tab:: Prime Limit

      .. testcode:: PrimeLimitTuning

         from xenharmlib import PrimeLimitTuning
         limit5 = PrimeLimitTuning(5)

         interval = limit5.diff_interval(limit5.lattice.point((0, 1, 0)))
         ic = interval.ic_normalized()
         print(ic)

      .. testoutput:: PrimeLimitTuning

         PrimeLimitPitchInterval(4/3, 5-Limit)

   .. tab:: Western

      .. testcode:: WesternNotation

         from xenharmlib import WesternNotation
         western = WesternNotation()

         interval = western.shorthand_interval('P', 5)
         ic = interval.ic_normalized()
         print(ic)

      .. testoutput:: WesternNotation

         WesternNoteInterval(P, 4)

   .. tab:: UpDown

      .. testcode:: UpDownNotation

         from xenharmlib import EDOTuning
         from xenharmlib import UpDownNotation

         edo31 = EDOTuning(31)
         n_edo31 = UpDownNotation(edo31)

         interval = n_edo31.shorthand_interval('^M', 9)
         ic = interval.ic_normalized()
         print(ic)

      .. testoutput:: UpDownNotation

         UpDownNoteInterval(^M, 2, 31-EDO)

Instead of receiving an interval object you can also get the interval class
index (which is the numeric representation used in most posttonal theory
textbooks):

.. tabs::

   .. tab:: EDO

      .. testcode:: EDOTuning

         from xenharmlib import EDOTuning
         edo31 = EDOTuning(31)

         interval = edo31.diff_interval(-18)
         print(interval.ic_index)

      .. testoutput:: EDOTuning

         13

   .. tab:: Prime Limit

      .. testcode:: PrimeLimitTuning

         from xenharmlib import PrimeLimitTuning
         limit5 = PrimeLimitTuning(5)

         interval = limit5.diff_interval(limit5.lattice.point((0, 1, 0)))
         print(interval.ic_index)

      .. testoutput:: PrimeLimitTuning

         LatticePoint(2, -1, 0)

   .. tab:: Western

      .. testcode:: WesternNotation

         from xenharmlib import WesternNotation
         western = WesternNotation()

         interval = western.shorthand_interval('P', 5)
         print(interval.ic_index)

      .. testoutput:: WesternNotation

         5

   .. tab:: UpDown

      .. testcode:: UpDownNotation

         from xenharmlib import EDOTuning
         from xenharmlib import UpDownNotation

         edo31 = EDOTuning(31)
         n_edo31 = UpDownNotation(edo31)

         interval = n_edo31.shorthand_interval('^M', 9)
         print(interval.ic_index)

      .. testoutput:: UpDownNotation

         6

.. rubric:: Footnotes

.. [#f1] The term *inversion* of an interval in music theory is often 
   confusing for mathematicians who know the term from group theory.
   There the inversion of an element is actually the element that
   combined with the original element results in the neutral element
   (in our case: the unison interval), meaning inversion in group theory
   is actually what we earlier called *negation*. Though it might be
   regrettable, that different things are named the same and same
   things are named differently, we have to accept these types of
   idiosyncracies and choose the meaning the word has in the domain
   of music theory.
