.. _interval_seq:

Interval Sequences
=================================

Interval sequences provide an abstract way to represent musical structures
by storing the relative distances between notes, rather than their absolute
pitches. This allows for the definition of abstract scale, sequence and chord
types -  for example, representing the major scale *as such*, rather than as
specific instances like C major or E major.

One method for generating an interval sequence is to begin with a scale 
or sequence of frequency representations and call their
:meth:`~!xenharmlib.core.scale.Scale.to_interval_seq`
method. Xenharmlib will then calculate the intervals between successive
notes and return the resulting interval sequence:

.. tabs::

   .. tab:: EDO

      .. testcode:: EDOTuning

         from xenharmlib import EDOTuning
         edo31 = EDOTuning(31)

         c_maj_scale = edo31.index_scale(
             k * 18 for k in range(-1, 6)
         ).pcs_normalized()

         major_seq = c_maj_scale.to_interval_seq()
         print(major_seq)

      .. testoutput:: EDOTuning

         EDOPitchIntervalSeq([5, 5, 3, 5, 5, 5], 31-EDO)

   .. tab:: Prime Limit

      .. testcode:: PrimeLimitTuning

         from xenharmlib import PrimeLimitTuning
         from xenharmlib import FrequencyRatio
         limit3 = PrimeLimitTuning(3)

         c_maj_scale = limit3.ratio_scale(
             (FrequencyRatio(3, 2) ** k) for k in range(-1, 6)
         ).pcs_normalized()

         major_seq = c_maj_scale.to_interval_seq()
         print(major_seq)

      .. testoutput:: PrimeLimitTuning

         PrimeLimitPitchIntervalSeq([9/8, 9/8, 256/243, 9/8, 9/8, 9/8], 3-Limit)

   .. tab:: Western

      .. testcode:: WesternNotation

         from xenharmlib import WesternNotation
         western = WesternNotation()
         c_maj_scale = western.pc_scale('CDEFGAB')

         major_seq = c_maj_scale.to_interval_seq()
         print(major_seq)

      .. testoutput:: WesternNotation

         WesternNoteIntervalSeq([M2, M2, m2, M2, M2, M2])

   .. tab:: UpDown

      .. testcode:: UpDownNotation

         from xenharmlib import EDOTuning
         from xenharmlib import UpDownNotation
         
         edo12 = EDOTuning(12)
         n_edo12 = UpDownNotation(edo12)
         c_maj_scale = n_edo12.pc_scale('CDEFGAB')

         major_seq = c_maj_scale.to_interval_seq()
         print(major_seq)

      .. testoutput:: UpDownNotation

         UpDownNoteIntervalSeq([M2, M2, m2, M2, M2, M2], 12-EDO)

As you can see you obtained a sequence of major and minor seconds in the
order that they occur in the scale. The resulting interval sequence is only
one possible representation of the major scale. Another representation that
is more common in textbooks is derived from a form of the scale where the
series is bookended by two equivalent notes. This scale form can be obtained
by the method :meth:`~xenharmlib.core.scale.PeriodicScale.plusone_normalized`:

.. tabs::

   .. tab:: EDO

      .. testcode:: EDOTuning

         from xenharmlib import EDOTuning
         edo31 = EDOTuning(31)

         c_maj_scale = edo31.index_scale(
             k * 18 for k in range(-1, 6)
         ).pcs_normalized()

         alt_c_maj = c_maj_scale.plusone_normalized()
         alt_maj_seq = alt_c_maj.to_interval_seq()

         print(alt_c_maj)
         print(alt_maj_seq)

      .. testoutput:: EDOTuning

         EDOPitchScale([0, 5, 10, 13, 18, 23, 28, 31], 31-EDO)
         EDOPitchIntervalSeq([5, 5, 3, 5, 5, 5, 3], 31-EDO)

   .. tab:: Prime Limit

      .. testcode:: PrimeLimitTuning

         from xenharmlib import PrimeLimitTuning
         from xenharmlib import FrequencyRatio
         limit3 = PrimeLimitTuning(3)

         c_maj_scale = limit3.ratio_scale(
             (FrequencyRatio(3, 2) ** k) for k in range(-1, 6)
         ).pcs_normalized()

         alt_c_maj = c_maj_scale.plusone_normalized()
         alt_maj_seq = alt_c_maj.to_interval_seq()

         print(alt_c_maj)
         print(alt_maj_seq)

      .. testoutput:: PrimeLimitTuning

         PrimeLimitPitchScale([1, 9/8, 81/64, 4/3, 3/2, 27/16, 243/128, 2], 3-Limit)
         PrimeLimitPitchIntervalSeq([9/8, 9/8, 256/243, 9/8, 9/8, 9/8, 256/243], 3-Limit)

   .. tab:: Western

      .. testcode:: WesternNotation

         from xenharmlib import WesternNotation
         western = WesternNotation()
         c_maj_scale = western.pc_scale('CDEFGAB')

         alt_c_maj = c_maj_scale.plusone_normalized()
         alt_maj_seq = alt_c_maj.to_interval_seq()

         print(alt_c_maj)
         print(alt_maj_seq)

      .. testoutput:: WesternNotation

         WesternNoteScale([C0, D0, E0, F0, G0, A0, B0, C1])
         WesternNoteIntervalSeq([M2, M2, m2, M2, M2, M2, m2])

   .. tab:: UpDown

      .. testcode:: UpDownNotation

         from xenharmlib import EDOTuning
         from xenharmlib import UpDownNotation
         
         edo12 = EDOTuning(12)
         n_edo12 = UpDownNotation(edo12)
         c_maj_scale = n_edo12.pc_scale('CDEFGAB')

         alt_c_maj = c_maj_scale.plusone_normalized()
         alt_maj_seq = alt_c_maj.to_interval_seq()

         print(alt_c_maj)
         print(alt_maj_seq)

      .. testoutput:: UpDownNotation

         UpDownNoteScale([C0, D0, E0, F0, G0, A0, B0, C1], 12-EDO)
         UpDownNoteIntervalSeq([M2, M2, m2, M2, M2, M2, m2], 12-EDO)

Both methods to define the major scale have their valid usecases. It is
upon you to decide which form fits your task.

Interval sequences implement the complete set of methods from python's
builtin lists and tuples that do not mutatate the object. This means
that interval sequences can be treated *as if* they were lists or
tuples of intervals and used as a drop-in replacement.

Deriving Interval Sequences from Intervals
---------------------------------------------

Like other harmonic "collection primitives" interval sequences can be built
by assembly from the primitives they contain, in this case intervals:

.. tabs::

   .. tab:: EDO

      .. testcode:: EDOTuning

         from xenharmlib import EDOTuning
         edo31 = EDOTuning(31)

         M2 = edo31.diff_interval(5)
         m2 = edo31.diff_interval(3)

         major_seq = edo31.interval_seq([M2, M2, m2, M2, M2, M2])
         print(major_seq)

      .. testoutput:: EDOTuning

         EDOPitchIntervalSeq([5, 5, 3, 5, 5, 5], 31-EDO)

   .. tab:: Prime Limit

      .. testcode:: PrimeLimitTuning

         from xenharmlib import PrimeLimitTuning
         from xenharmlib import FrequencyRatio
         limit3 = PrimeLimitTuning(3)

         M2 = limit3.rs_interval('9/8')
         m2 = limit3.rs_interval('256/243')

         major_seq = limit3.interval_seq([M2, M2, m2, M2, M2, M2])
         print(major_seq)

      .. testoutput:: PrimeLimitTuning

         PrimeLimitPitchIntervalSeq([9/8, 9/8, 256/243, 9/8, 9/8, 9/8], 3-Limit)

   .. tab:: Western

      .. testcode:: WesternNotation

         from xenharmlib import WesternNotation
         western = WesternNotation()

         M2 = western.shorthand_interval('M', 2)
         m2 = western.shorthand_interval('m', 2)

         major_seq = western.interval_seq([M2, M2, m2, M2, M2, M2])
         print(major_seq)

      .. testoutput:: WesternNotation

         WesternNoteIntervalSeq([M2, M2, m2, M2, M2, M2])

   .. tab:: UpDown

      .. testcode:: UpDownNotation

         from xenharmlib import EDOTuning
         from xenharmlib import UpDownNotation
         
         edo12 = EDOTuning(12)
         n_edo12 = UpDownNotation(edo12)

         M2 = n_edo12.shorthand_interval('M', 2)
         m2 = n_edo12.shorthand_interval('m', 2)

         major_seq = n_edo12.interval_seq([M2, M2, m2, M2, M2, M2])
         print(major_seq)

      .. testoutput:: UpDownNotation

         UpDownNoteIntervalSeq([M2, M2, m2, M2, M2, M2], 12-EDO)

Index-based Construction
---------------------------------------------

Interval sequences can also be constructed by providing pitch differences
which (depending on origin context) can be integers or lattice points.
In case of notations xenharmlib uses the notation's enharmonic strategy
to transform differences into full note interval objects.

.. tabs::

   .. tab:: EDO

      .. testcode:: EDOTuning

         from xenharmlib import EDOTuning
         edo31 = EDOTuning(31)

         major_seq = edo31.diff_interval_seq([5, 5, 3, 5, 5, 5])
         print(major_seq)

      .. testoutput:: EDOTuning

         EDOPitchIntervalSeq([5, 5, 3, 5, 5, 5], 31-EDO)

   .. tab:: Prime Limit

      .. testcode:: PrimeLimitTuning

         from xenharmlib import PrimeLimitTuning
         from xenharmlib import FrequencyRatio
         limit3 = PrimeLimitTuning(3)

         major_seq = limit3.diff_interval_seq(
             [
                 limit3.lattice.point((-3, 2)),
                 limit3.lattice.point((-3, 2)),
                 limit3.lattice.point((8, -5)),
                 limit3.lattice.point((-3, 2)),
                 limit3.lattice.point((-3, 2)),
                 limit3.lattice.point((-3, 2)),
             ]
         )
         print(major_seq)

      .. testoutput:: PrimeLimitTuning

         PrimeLimitPitchIntervalSeq([9/8, 9/8, 256/243, 9/8, 9/8, 9/8], 3-Limit)

   .. tab:: Western

      .. testcode:: WesternNotation

         from xenharmlib import WesternNotation
         western = WesternNotation()

         major_seq = western.diff_interval_seq([2, 2, 1, 2, 2, 2])
         print(major_seq)

      .. testoutput:: WesternNotation

         WesternNoteIntervalSeq([M2, M2, A1, M2, M2, M2])

   .. tab:: UpDown

      .. testcode:: UpDownNotation

         from xenharmlib import EDOTuning
         from xenharmlib import UpDownNotation

         edo31 = EDOTuning(31)
         n_edo31 = UpDownNotation(edo31)
         
         major_seq = n_edo31.diff_interval_seq([5, 5, 3, 5, 5, 5])
         print(major_seq)

      .. testoutput:: UpDownNotation

         UpDownNoteIntervalSeq([M2, M2, m2, M2, M2, M2], 31-EDO)

Origin contexts built on lattice point indexing also allow construction
from an iterable of tuples with
:meth:`~xenharmlib.core.multigen.MultiGenTuning.vec_interval_seq`
as an alternative to the more verbose above method which expects
a full :class:`~xenharmlib.core.lattice.LatticePoint` object.

.. tabs::

   .. tab:: Prime Limit

      .. testcode:: PrimeLimitTuning

         from xenharmlib import PrimeLimitTuning
         limit3 = PrimeLimitTuning(3)

         major_seq = limit3.vec_interval_seq(
             [(-3, 2), (-3, 2), (8, -5), (-3, 2), (-3, 2), (-3, 2)]
         )
         print(major_seq)

      .. testoutput:: PrimeLimitTuning

         PrimeLimitPitchIntervalSeq([9/8, 9/8, 256/243, 9/8, 9/8, 9/8], 3-Limit)

   .. tab:: 2.3.7 Subgroup

      .. testcode:: MultiGenTuning

         from xenharmlib import MultiGenTuning
         from xenharmlib import FrequencyRatio

         sg237 = MultiGenTuning(
             [FrequencyRatio(p) for p in [2, 3, 7]],
             period_vec=(1, 0, 0)
         )

         iseq = sg237.vec_interval_seq(
             [(-1, -1, 1), (-2, 1, 1), (-1, -1, 1)]
         )
         print(iseq)

      .. testoutput:: MultiGenTuning

         MultiGenPitchIntervalSeq([(-1, -1, 1), (-2, 1, 1), (-1, -1, 1)], G=(2, 3, 7))


Construction Based on Closest Frequency Ratio
-----------------------------------------------------

Origin contexts based on integer indices allow construction based on the
approximation of frequency ratios. Given an arbitrary iterable of frequency
ratios the 
:meth:`~xenharmlib.core.origin_context.OriginContext.closest_interval_seq`
method returns the interval sequence of an origin context that is closest
to it:

.. tabs::

   .. tab:: EDO

      .. testcode:: EDOTuning

         from xenharmlib import EDOTuning
         from xenharmlib import FrequencyRatio

         edo31 = EDOTuning(31)
         ratios = [
             FrequencyRatio(5, 4),
             FrequencyRatio(6, 5),
         ]

         iseq = edo31.closest_interval_seq(ratios)
         print(iseq)

      .. testoutput:: EDOTuning

         EDOPitchIntervalSeq([10, 8], 31-EDO)

   .. tab:: Western

      .. testcode:: WesternNotation

         from xenharmlib import WesternNotation
         from xenharmlib import FrequencyRatio

         western = WesternNotation()
         ratios = [
             FrequencyRatio(5, 4),
             FrequencyRatio(6, 5),
         ]

         iseq = western.closest_interval_seq(ratios)
         print(iseq)

      .. testoutput:: WesternNotation

         WesternNoteIntervalSeq([M3, A2])

   .. tab:: UpDown

      .. testcode:: UpDownNotation

         from xenharmlib import EDOTuning
         from xenharmlib import UpDownNotation
         from xenharmlib import FrequencyRatio

         edo31 = EDOTuning(31)
         n_edo31 = UpDownNotation(edo31)
         ratios = [
             FrequencyRatio(5, 4),
             FrequencyRatio(6, 5),
         ]

         iseq = n_edo31.closest_interval_seq(ratios)
         print(iseq)

      .. testoutput:: UpDownNotation

         UpDownNoteIntervalSeq([M3, m3], 31-EDO)

Iteration
--------------------------------------------

Like other sequence types interval sequences support iteration:

.. tabs::

   .. tab:: EDO

      .. testcode:: EDOTuning

         from xenharmlib import EDOTuning
         edo31 = EDOTuning(31)

         iseq = edo31.diff_interval_seq([10, 8, 7, 10])

         for interval in iseq:
             print('-->', interval)

      .. testoutput:: EDOTuning

         --> EDOPitchInterval(10, 31-EDO)
         --> EDOPitchInterval(8, 31-EDO)
         --> EDOPitchInterval(7, 31-EDO)
         --> EDOPitchInterval(10, 31-EDO)

   .. tab:: Prime Limit

      .. testcode:: PrimeLimitTuning

         from xenharmlib import PrimeLimitTuning
         limit5 = PrimeLimitTuning(5)

         iseq = limit5.rs_interval_seq(['5/4', '6/5', '5/4', '10/9'])

         for interval in iseq:
             print('-->', interval)

      .. testoutput:: PrimeLimitTuning

         --> PrimeLimitPitchInterval(5/4, 5-Limit)
         --> PrimeLimitPitchInterval(6/5, 5-Limit)
         --> PrimeLimitPitchInterval(5/4, 5-Limit)
         --> PrimeLimitPitchInterval(10/9, 5-Limit)

   .. tab:: Western

      .. testcode:: WesternNotation

         from xenharmlib import WesternNotation
         western = WesternNotation()

         iseq = western.diff_interval_seq([3, 5, 5, 3, 5])

         for interval in iseq:
             print('-->', interval)

      .. testoutput:: WesternNotation

         --> WesternNoteInterval(A, 2)
         --> WesternNoteInterval(P, 4)
         --> WesternNoteInterval(P, 4)
         --> WesternNoteInterval(A, 2)
         --> WesternNoteInterval(P, 4)

   .. tab:: UpDown

      .. testcode:: UpDownNotation

         from xenharmlib import EDOTuning
         from xenharmlib import UpDownNotation

         edo31 = EDOTuning(31)
         n_edo31 = UpDownNotation(edo31)

         iseq = n_edo31.diff_interval_seq([10, 11, 10, 10, 18])

         for interval in iseq:
             print('-->', interval)

      .. testoutput:: UpDownNotation

         --> UpDownNoteInterval(M, 3, 31-EDO)
         --> UpDownNoteInterval(d, 4, 31-EDO)
         --> UpDownNoteInterval(M, 3, 31-EDO)
         --> UpDownNoteInterval(M, 3, 31-EDO)
         --> UpDownNoteInterval(P, 5, 31-EDO)

Containment
--------------------------------------------

If you want to know if a specific interval is contained inside of an
interval sequence you can use the :code:`in` operator:

.. tabs::

   .. tab:: EDO

      .. testcode:: EDOTuning

         from xenharmlib import EDOTuning
         edo31 = EDOTuning(31)

         iseq = edo31.diff_interval_seq([10, 8, 7, 10])
         interval_a = edo31.diff_interval(7)
         interval_b = edo31.diff_interval(9)

         print(interval_a in iseq)
         print(interval_b in iseq)

      .. testoutput:: EDOTuning

         True
         False

   .. tab:: Prime Limit

      .. testcode:: PrimeLimitTuning

         from xenharmlib import PrimeLimitTuning
         limit5 = PrimeLimitTuning(5)

         iseq = limit5.rs_interval_seq(['5/4', '6/5', '5/4', '10/9'])
         interval_a = limit5.rs_interval('6/5')
         interval_b = limit5.rs_interval('3/2')

         print(interval_a in iseq)
         print(interval_b in iseq)

      .. testoutput:: PrimeLimitTuning

         True
         False

   .. tab:: Western

      .. testcode:: WesternNotation

         from xenharmlib import WesternNotation
         western = WesternNotation()

         iseq = western.diff_interval_seq([3, 5, 5, 3, 5])
         interval_a = western.shorthand_interval('P', 4)
         interval_b = western.shorthand_interval('P', 5)

         print(interval_a in iseq)
         print(interval_b in iseq)

      .. testoutput:: WesternNotation

         True
         False

   .. tab:: UpDown

      .. testcode:: UpDownNotation

         from xenharmlib import EDOTuning
         from xenharmlib import UpDownNotation

         edo31 = EDOTuning(31)
         n_edo31 = UpDownNotation(edo31)

         iseq = n_edo31.diff_interval_seq([10, 11, 10, 10, 18])
         interval_a = n_edo31.shorthand_interval('M', 3)
         interval_b = n_edo31.shorthand_interval('vM', 3)

         print(interval_a in iseq)
         print(interval_b in iseq)

      .. testoutput:: UpDownNotation

         True
         False

Identity
-------------------------------------------------------

Two interval sequences are considered identical if each interval in one
interval sequence corresponds to another interval in the other sequence
at the same position.
This relation works across origin contexts, for example 12-EDO and
24-EDO interval sequences, or western note interval sequences can
be identical:

.. testcode::

   from xenharmlib import EDOTuning
   from xenharmlib import UpDownNotation
   from xenharmlib import WesternNotation

   edo24 = EDOTuning(24)
   n_edo24 = UpDownNotation(edo24)
   western = WesternNotation()

   Cm_1 = edo24.diff_interval_seq([8, 6])
   Cm_2 = n_edo24.interval_seq(
       [
           n_edo24.shorthand_interval('M', 3),
           n_edo24.shorthand_interval('m', 3),
       ]
   )
   Cm_3 = western.interval_seq(
       [
           western.shorthand_interval('M', 3),
           western.shorthand_interval('m', 3),
       ]
   )

   print(Cm_1 == Cm_2 == Cm_3)

.. testoutput::

   True

Keep in mind that even if two interval sequences might have the same symbolic
string representation in a notation, they are not necessarily equal. A major
third interval in 31-EDO has for example a different frequency ratio than a
major third interval in 12-EDO:

.. testcode::

   from xenharmlib import EDOTuning
   from xenharmlib import UpDownNotation

   edo31 = EDOTuning(31)
   n_edo31 = UpDownNotation(edo31)

   edo12 = EDOTuning(12)
   n_edo12 = UpDownNotation(edo12)

   Cm_1 = n_edo31.interval_seq(
       [
           n_edo31.shorthand_interval('M', 3),
           n_edo31.shorthand_interval('m', 3),
       ]
   )
   Cm_2 = n_edo12.interval_seq(
       [
           n_edo12.shorthand_interval('M', 3),
           n_edo12.shorthand_interval('m', 3),
       ]
   )

   print(Cm_1)
   print(Cm_2)

   print(Cm_1 == Cm_2)

.. testoutput::

   UpDownNoteIntervalSeq([M3, m3], 31-EDO)
   UpDownNoteIntervalSeq([M3, m3], 12-EDO)
   False

Item Retrieval and Slicing
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Single intervals from the sequence can be obtained by their index.
You can also use slices (including step size) to extract portions
of an interval sequence:

.. tabs::

   .. tab:: EDO

      .. testcode:: EDOTuning

         from xenharmlib import EDOTuning
         edo31 = EDOTuning(31)

         iseq = edo31.diff_interval_seq([10, 8, 7, 10])

         print(iseq[2])
         print(iseq[1:3])
         print(iseq[::2])

      .. testoutput:: EDOTuning

         EDOPitchInterval(7, 31-EDO)
         EDOPitchIntervalSeq([8, 7], 31-EDO)
         EDOPitchIntervalSeq([10, 7], 31-EDO)

   .. tab:: Prime Limit

      .. testcode:: PrimeLimitTuning

         from xenharmlib import PrimeLimitTuning
         limit5 = PrimeLimitTuning(5)

         iseq = limit5.rs_interval_seq(['5/4', '6/5', '5/4', '10/9'])

         print(iseq[2])
         print(iseq[1:3])
         print(iseq[::2])

      .. testoutput:: PrimeLimitTuning

         PrimeLimitPitchInterval(5/4, 5-Limit)
         PrimeLimitPitchIntervalSeq([6/5, 5/4], 5-Limit)
         PrimeLimitPitchIntervalSeq([5/4, 5/4], 5-Limit)

   .. tab:: Western

      .. testcode:: WesternNotation

         from xenharmlib import WesternNotation
         western = WesternNotation()

         iseq = western.diff_interval_seq([3, 5, 5, 3, 5])

         print(iseq[2])
         print(iseq[1:4])
         print(iseq[::2])

      .. testoutput:: WesternNotation

         WesternNoteInterval(P, 4)
         WesternNoteIntervalSeq([P4, P4, A2])
         WesternNoteIntervalSeq([A2, P4, P4])

   .. tab:: UpDown

      .. testcode:: UpDownNotation

         from xenharmlib import EDOTuning
         from xenharmlib import UpDownNotation

         edo31 = EDOTuning(31)
         n_edo31 = UpDownNotation(edo31)

         iseq = n_edo31.diff_interval_seq([10, 11, 10, 10, 18])

         print(iseq[1])
         print(iseq[1:4])
         print(iseq[::2])

      .. testoutput:: UpDownNotation

         UpDownNoteInterval(d, 4, 31-EDO)
         UpDownNoteIntervalSeq([d4, M3, M3], 31-EDO)
         UpDownNoteIntervalSeq([M3, M3, P5], 31-EDO)

Search
------------------

The :meth:`~xenharmlib.core.interval_seq.IntervalSeq.index` method returns
the first index position where an interval was found (or raises
:code:`ValueError` if the interval does not exist in the sequence). 

.. tabs::

   .. tab:: EDO

      .. testcode:: EDOTuning

         from xenharmlib import EDOTuning
         edo31 = EDOTuning(31)

         iseq = edo31.diff_interval_seq([10, 8, 7, 10])
         interval = edo31.diff_interval(7)

         print(iseq.index(interval))

      .. testoutput:: EDOTuning

         2

   .. tab:: Prime Limit

      .. testcode:: PrimeLimitTuning

         from xenharmlib import PrimeLimitTuning
         limit5 = PrimeLimitTuning(5)

         iseq = limit5.rs_interval_seq(['5/4', '6/5', '5/4', '10/9'])
         interval = limit5.rs_interval('6/5')

         print(iseq.index(interval))

      .. testoutput:: PrimeLimitTuning

         1

   .. tab:: Western

      .. testcode:: WesternNotation

         from xenharmlib import WesternNotation
         western = WesternNotation()

         iseq = western.diff_interval_seq([3, 5, 5, 3, 5])
         interval = western.shorthand_interval('P', 4)

         print(iseq.index(interval))

      .. testoutput:: WesternNotation

         1

   .. tab:: UpDown

      .. testcode:: UpDownNotation

         from xenharmlib import EDOTuning
         from xenharmlib import UpDownNotation

         edo31 = EDOTuning(31)
         n_edo31 = UpDownNotation(edo31)

         iseq = n_edo31.diff_interval_seq([10, 11, 10, 10, 18])
         interval = n_edo31.shorthand_interval('M', 3)

         print(iseq.index(interval))

      .. testoutput:: UpDownNotation

         0

Counting
------------------

For statistical analysis xenharmlib can calculate the number of times a
specific interval occurs in an interval sequence:

.. tabs::

   .. tab:: EDO

      .. testcode:: EDOTuning

         from xenharmlib import EDOTuning
         edo31 = EDOTuning(31)

         iseq = edo31.diff_interval_seq([10, 8, 7, 10])
         interval = edo31.diff_interval(7)

         print(iseq.count(interval))

      .. testoutput:: EDOTuning

         1

   .. tab:: Prime Limit

      .. testcode:: PrimeLimitTuning

         from xenharmlib import PrimeLimitTuning
         limit5 = PrimeLimitTuning(5)

         iseq = limit5.rs_interval_seq(['5/4', '6/5', '5/4', '10/9'])
         interval = limit5.rs_interval('5/4')

         print(iseq.count(interval))

      .. testoutput:: PrimeLimitTuning

         2

   .. tab:: Western

      .. testcode:: WesternNotation

         from xenharmlib import WesternNotation
         western = WesternNotation()

         iseq = western.diff_interval_seq([3, 5, 5, 3, 5])
         interval = western.shorthand_interval('P', 4)

         print(iseq.count(interval))

      .. testoutput:: WesternNotation

         3

   .. tab:: UpDown

      .. testcode:: UpDownNotation

         from xenharmlib import EDOTuning
         from xenharmlib import UpDownNotation

         edo31 = EDOTuning(31)
         n_edo31 = UpDownNotation(edo31)

         iseq = n_edo31.diff_interval_seq([10, 11, 10, 10, 18])
         interval = n_edo31.shorthand_interval('P', 5)

         print(iseq.count(interval))

      .. testoutput:: UpDownNotation

         1

Concatenation
------------------

Interval sequences can be "glued together" with the :code:`+` operator.
(In programming known under the term "concatentation")
This can be especially useful when programmatically creating polychords.

Think of defining the major triad and the minor triad as an abstract
sequence, resulting in interval sequences with two intervals each.
Concatenation of the interval sequences then means the following
in the scale space: Take a triad and then, using the highest note
in the chord as a new root, add another triad on top of it. 

Putting a minor on top of a major then gives the abstract sequence
for the "dominant seventh add ninth" polychord. Putting a major
on top of a minor gives the abstract "minor-major ninth chord":

.. tabs::

   .. tab:: EDO

      .. testcode:: EDOTuning

         from xenharmlib import EDOTuning
         edo31 = EDOTuning(31)

         major = edo31.diff_interval_seq([10, 8])
         minor = edo31.diff_interval_seq([8, 10])

         print(major + minor)
         print(minor + major)

      .. testoutput:: EDOTuning

         EDOPitchIntervalSeq([10, 8, 8, 10], 31-EDO)
         EDOPitchIntervalSeq([8, 10, 10, 8], 31-EDO)

   .. tab:: Prime Limit

      .. testcode:: PrimeLimitTuning

         from xenharmlib import PrimeLimitTuning
         limit5 = PrimeLimitTuning(5)

         major = limit5.rs_interval_seq(['5/4', '6/5'])
         minor = limit5.rs_interval_seq(['6/5', '5/4'])

         print(major + minor)
         print(minor + major)

      .. testoutput:: PrimeLimitTuning

         PrimeLimitPitchIntervalSeq([5/4, 6/5, 6/5, 5/4], 5-Limit)
         PrimeLimitPitchIntervalSeq([6/5, 5/4, 5/4, 6/5], 5-Limit)

   .. tab:: Western

      .. testcode:: WesternNotation

         from xenharmlib import WesternNotation
         western = WesternNotation()

         M3 = western.shorthand_interval('M', 3)
         m3 = western.shorthand_interval('m', 3)

         major = western.interval_seq([M3, m3])
         minor = western.interval_seq([m3, M3])

         print(major + minor)
         print(minor + major)

      .. testoutput:: WesternNotation

         WesternNoteIntervalSeq([M3, m3, m3, M3])
         WesternNoteIntervalSeq([m3, M3, M3, m3])

Repetition
------------------

Repetition of an interval sequence can be achieved by multiplying
(:code:`*`) an interval sequence with an integer.

This technique can be useful if you have an interval sequence that first
ascends and then descends without returning to the point of origin. 
Repeating such an interval sequence results in a wave of "upward and 
downword motions" that in its entirety slowly moves upwards:

.. tabs::

   .. tab:: EDO

      .. testcode:: EDOTuning

         from xenharmlib import EDOTuning
         edo31 = EDOTuning(31)

         iseq = edo31.diff_interval_seq([5, 7, 5, -7, -5])
         print(3 * iseq)

      .. testoutput:: EDOTuning

         EDOPitchIntervalSeq([5, 7, 5, -7, -5, 5, 7, 5, -7, -5, 5, 7, 5, -7, -5], 31-EDO)

   .. tab:: Prime Limit

      .. testcode:: PrimeLimitTuning

         from xenharmlib import PrimeLimitTuning
         limit5 = PrimeLimitTuning(5)

         iseq = limit5.rs_interval_seq(['16/15', '9/8', '9/8', '8/9'])
         print(3 * iseq)

      .. testoutput:: PrimeLimitTuning

         PrimeLimitPitchIntervalSeq([16/15, 9/8, 9/8, 8/9, 16/15, 9/8, 9/8, 8/9, 16/15, 9/8, 9/8, 8/9], 5-Limit)

   .. tab:: Western

      .. testcode:: WesternNotation

         from xenharmlib import WesternNotation
         western = WesternNotation()

         M2 = western.shorthand_interval('M', 2)
         M3 = western.shorthand_interval('M', 3)
         m3 = western.shorthand_interval('m', 3)
         M2down = western.shorthand_interval('M', -2)

         iseq = western.interval_seq([M2, M3, m3, M2down, M2down])
         print(3 * iseq)

      .. testoutput:: WesternNotation

         WesternNoteIntervalSeq([M2, M3, m3, M-2, M-2, M2, M3, m3, M-2, M-2, M2, M3, m3, M-2, M-2])


Index Masks and Partial Interval Sequences
----------------------------------------------

Like with scales the interval sequence primitive allows extraction of 
"substructures" with the
:meth:`~xenharmlib.core.interval_seq.IntervalSeq.partial` method, that
expects an index mask expression, i.e. a tuple with indices pointing
to sequence elements that should be extracted.

The mask :code:`(1, 3, 4)` for example extracts the second, fourth and
fifth element of the sequence (like with item retrieval indices in an a
mask expression start with 0):

.. tabs::

   .. tab:: EDO

      .. testcode:: EDOTuning

         from xenharmlib import EDOTuning
         edo31 = EDOTuning(31)

         iseq = edo31.diff_interval_seq([10, 8, 10, 9, 10, 8])
         print(iseq.partial((1, 3, 4)))

      .. testoutput:: EDOTuning

         EDOPitchIntervalSeq([8, 9, 10], 31-EDO)

   .. tab:: Prime Limit

      .. testcode:: PrimeLimitTuning

         from xenharmlib import PrimeLimitTuning
         limit5 = PrimeLimitTuning(5)

         iseq = limit5.rs_interval_seq(['5/4', '6/5', '9/8', '6/5', '10/9'])
         print(iseq.partial((1, 3, 4)))

      .. testoutput:: PrimeLimitTuning

         PrimeLimitPitchIntervalSeq([6/5, 6/5, 10/9], 5-Limit)

   .. tab:: Western

      .. testcode:: WesternNotation

         from xenharmlib import WesternNotation
         western = WesternNotation()

         M3 = western.shorthand_interval('M', 3)
         m3 = western.shorthand_interval('m', 3)
         A1 = western.shorthand_interval('A', 1)

         iseq = western.interval_seq([M3, m3, A1, A1, M3, m3])
         print(iseq.partial((1, 3, 4)))

      .. testoutput:: WesternNotation

         WesternNoteIntervalSeq([m3, A1, M3])

Mask expressions targeted at longer continuous spans inside the interval
sequence can be written as a "shortform" with the ellipsis symbol
(:code:`...`):

.. tabs::

   .. tab:: EDO

      .. testcode:: EDOTuning

         from xenharmlib import EDOTuning
         edo31 = EDOTuning(31)

         iseq = edo31.diff_interval_seq([10, 8, 10, 9, 10, 8])

         # an ellipsis as a prefix matches all elements from
         # the start of the sequence until and including (!)
         # the first mask index
         print(iseq.partial((..., 3, 4)))

         # an ellipsis between two indices matches the two indices
         # in the sequence and all elements between them
         print(iseq.partial((1, ..., 4)))

         # an ellipsis at the end matches all remaining indices
         # in the sequence after the last mask index
         print(iseq.partial((0, 3, ...)))

      .. testoutput:: EDOTuning

         EDOPitchIntervalSeq([10, 8, 10, 9, 10], 31-EDO)
         EDOPitchIntervalSeq([8, 10, 9, 10], 31-EDO)
         EDOPitchIntervalSeq([10, 9, 10, 8], 31-EDO)

   .. tab:: Prime Limit

      .. testcode:: PrimeLimitTuning

         from xenharmlib import PrimeLimitTuning
         limit5 = PrimeLimitTuning(5)

         iseq = limit5.rs_interval_seq(['5/4', '6/5', '9/8', '6/5', '10/9'])

         # an ellipsis as a prefix matches all elements from
         # the start of the sequence until and including (!)
         # the first mask index
         print(iseq.partial((..., 3, 4)))

         # an ellipsis between two indices matches the two indices
         # in the sequence and all elements between them
         print(iseq.partial((1, ..., 4)))

         # an ellipsis at the end matches all remaining indices
         # in the sequence after the last mask index
         print(iseq.partial((0, 3, ...)))

      .. testoutput:: PrimeLimitTuning

         PrimeLimitPitchIntervalSeq([5/4, 6/5, 9/8, 6/5, 10/9], 5-Limit)
         PrimeLimitPitchIntervalSeq([6/5, 9/8, 6/5, 10/9], 5-Limit)
         PrimeLimitPitchIntervalSeq([5/4, 6/5, 10/9], 5-Limit)

   .. tab:: Western

      .. testcode:: WesternNotation

         from xenharmlib import WesternNotation
         western = WesternNotation()

         M3 = western.shorthand_interval('M', 3)
         m3 = western.shorthand_interval('m', 3)
         A1 = western.shorthand_interval('A', 1)

         iseq = western.interval_seq([M3, m3, A1, A1, M3, m3])

         # an ellipsis as a prefix matches all elements from
         # the start of the sequence until and including (!)
         # the first mask index
         print(iseq.partial((..., 3, 4)))

         # an ellipsis between two indices matches the two indices
         # in the sequence and all elements between them
         print(iseq.partial((1, ..., 4)))

         # an ellipsis at the end matches all remaining indices
         # in the sequence after the last mask index
         print(iseq.partial((0, 3, ...)))

      .. testoutput:: WesternNotation

         WesternNoteIntervalSeq([M3, m3, A1, A1, M3])
         WesternNoteIntervalSeq([m3, A1, A1, M3])
         WesternNoteIntervalSeq([M3, A1, M3, m3])

Selection can also be inverted with the
:meth:`~xenharmlib.core.interval_seq.IntervalSeq.partial_not` method that
returns all elements *not* covered by the mask expression:

.. tabs::

   .. tab:: EDO

      .. testcode:: EDOTuning

         from xenharmlib import EDOTuning
         edo31 = EDOTuning(31)

         iseq = edo31.diff_interval_seq([10, 8, 10, 9, 10, 8])
         print(iseq.partial_not((1, 3, 4)))

      .. testoutput:: EDOTuning

         EDOPitchIntervalSeq([10, 10, 8], 31-EDO)

   .. tab:: Prime Limit

      .. testcode:: PrimeLimitTuning

         from xenharmlib import PrimeLimitTuning
         limit5 = PrimeLimitTuning(5)

         iseq = limit5.rs_interval_seq(['5/4', '6/5', '9/8', '6/5', '10/9'])
         print(iseq.partial_not((1, 3, 4)))

      .. testoutput:: PrimeLimitTuning

         PrimeLimitPitchIntervalSeq([5/4, 9/8], 5-Limit)

   .. tab:: Western

      .. testcode:: WesternNotation

         from xenharmlib import WesternNotation
         western = WesternNotation()

         M3 = western.shorthand_interval('M', 3)
         m3 = western.shorthand_interval('m', 3)
         A1 = western.shorthand_interval('A', 1)

         iseq = western.interval_seq([M3, m3, A1, A1, M3, m3])
         print(iseq.partial_not((1, 3, 4)))

      .. testoutput:: WesternNotation

         WesternNoteIntervalSeq([M3, A1, m3])

To get both the substructure indicated by the mask *and* its complement as
a tuple, you can use the
:meth:`~xenharmlib.core.interval_seq.IntervalSeq.partition` method:

.. tabs::

   .. tab:: EDO

      .. testcode:: EDOTuning

         from xenharmlib import EDOTuning
         edo31 = EDOTuning(31)

         iseq = edo31.diff_interval_seq([10, 8, 10, 9, 10, 8])
         a, b = iseq.partition((1, 3, 4))
         print(a)
         print(b)

      .. testoutput:: EDOTuning

         EDOPitchIntervalSeq([8, 9, 10], 31-EDO)
         EDOPitchIntervalSeq([10, 10, 8], 31-EDO)

   .. tab:: Prime Limit

      .. testcode:: PrimeLimitTuning

         from xenharmlib import PrimeLimitTuning
         limit5 = PrimeLimitTuning(5)

         iseq = limit5.rs_interval_seq(['5/4', '6/5', '9/8', '6/5', '10/9'])
         a, b = iseq.partition((1, 3, 4))
         print(a)
         print(b)

      .. testoutput:: PrimeLimitTuning

         PrimeLimitPitchIntervalSeq([6/5, 6/5, 10/9], 5-Limit)
         PrimeLimitPitchIntervalSeq([5/4, 9/8], 5-Limit)

   .. tab:: Western

      .. testcode:: WesternNotation

         from xenharmlib import WesternNotation
         western = WesternNotation()

         M3 = western.shorthand_interval('M', 3)
         m3 = western.shorthand_interval('m', 3)
         A1 = western.shorthand_interval('A', 1)

         iseq = western.interval_seq([M3, m3, A1, A1, M3, m3])
         a, b = iseq.partition((1, 3, 4))
         print(a)
         print(b)

      .. testoutput:: WesternNotation

         WesternNoteIntervalSeq([m3, A1, M3])
         WesternNoteIntervalSeq([M3, A1, m3])

Templating and Categorization
----------------------------------------------

One of the main use cases for interval sequences is templating. You can
for example define abstract scales (like "major scale") and then make
scale instances from it:

.. tabs::

   .. tab:: EDO

      .. testcode:: EDOTuning

         from xenharmlib import EDOTuning
         edo31 = EDOTuning(31)

         M2 = edo31.diff_interval(5)
         m2 = edo31.diff_interval(3)

         major_seq = edo31.interval_seq([M2, M2, m2, M2, M2, M2])
         Emaj_scale = edo31.pitch(10).scale(major_seq)
         print(Emaj_scale)

      .. testoutput:: EDOTuning

         EDOPitchScale([10, 15, 20, 23, 28, 33, 38], 31-EDO)

   .. tab:: Prime Limit

      .. testcode:: PrimeLimitTuning

         from xenharmlib import PrimeLimitTuning
         from xenharmlib import FrequencyRatio
         limit3 = PrimeLimitTuning(3)

         M2 = limit3.rs_interval('9/8')
         m2 = limit3.rs_interval('256/243')

         major_seq = limit3.interval_seq([M2, M2, m2, M2, M2, M2])
         Gmaj_scale = limit3.rs_pitch('3/2').scale(major_seq)
         print(Gmaj_scale)

      .. testoutput:: PrimeLimitTuning

         PrimeLimitPitchScale([3/2, 27/16, 243/128, 2, 9/4, 81/32, 729/256], 3-Limit)

   .. tab:: Western

      .. testcode:: WesternNotation

         from xenharmlib import WesternNotation
         western = WesternNotation()

         M2 = western.shorthand_interval('M', 2)
         m2 = western.shorthand_interval('m', 2)

         major_seq = western.interval_seq([M2, M2, m2, M2, M2, M2])
         Fmaj_scale = western.note('F', 4).scale(major_seq)
         print(Fmaj_scale)

      .. testoutput:: WesternNotation

         WesternNoteScale([F4, G4, A4, Bb4, C5, D5, E5])

   .. tab:: UpDown

      .. testcode:: UpDownNotation

         from xenharmlib import EDOTuning
         from xenharmlib import UpDownNotation
         
         edo12 = EDOTuning(12)
         n_edo12 = UpDownNotation(edo12)

         M2 = n_edo12.shorthand_interval('M', 2)
         m2 = n_edo12.shorthand_interval('m', 2)

         major_seq = n_edo12.interval_seq([M2, M2, m2, M2, M2, M2])
         Emaj_scale = n_edo12.note('E', 4).scale(major_seq)
         print(Emaj_scale)

      .. testoutput:: UpDownNotation

         UpDownNoteScale([E4, F#4, G#4, A4, B4, C#5, D#5], 12-EDO)

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

The generic approach allows us to reuse the functions for all notations
supporting western-style naturals and sharps and flats.

.. tabs::

   .. tab:: Western

      .. testcode::

         from xenharmlib import WesternNotation

         western = WesternNotation()
         scale = western.pc_scale(['C', 'D', 'Eb', 'F', 'G', 'A', 'B'])
         print(which_minor(scale))

      .. testoutput::

         melodic

   .. tab:: UpDown (EDO24)

      .. testcode::

         from xenharmlib import EDOTuning
         from xenharmlib import UpDownNotation

         edo24 = EDOTuning(24)
         n_edo24 = UpDownNotation(edo24)
         scale = n_edo24.pc_scale(['C', 'D', 'Eb', 'F', 'G', 'Ab', 'Bb'])
         print(which_minor(scale))

      .. testoutput::

         natural

   .. tab:: UpDown (EDO31)

      .. testcode::

         from xenharmlib import EDOTuning
         from xenharmlib import UpDownNotation
         from xenharmlib import WesternNotation

         edo31 = EDOTuning(31)
         n_edo31 = UpDownNotation(edo31)
         scale = n_edo31.pc_scale(['C', 'D', 'Eb', 'F', 'G', 'Ab', 'B'])
         print(which_minor(scale))

      .. testoutput::

         harmonic
