Lattice Points
===================

While single-generator tunings like the "equal division tuning" family use
integers for pitch indices, pitch class indices and pitch differences,
multi-generator tunings use *vectors* of integers, that are called
*Lattice Points*.

The semantics of a lattice point, i.e. what frequency or frequency ratio
a specific vector represents depends on the tuning, more specifically
on the generator intervals of that tuning. That's why lattice points
are typically created from the tuning context:

.. testcode::

   from xenharmlib import PrimeLimitTuning

   limit5 = PrimeLimitTuning(5)
   lp = limit5.lattice.point((-2, 0, 1))

   print(lp)

.. testoutput::

   LatticePoint(-2, 0, 1)

The generator interval ratios can be inspected like this:

.. testcode::

   print(lp.base)

.. testoutput::

   [FrequencyRatio(2), FrequencyRatio(3), FrequencyRatio(5)]

In this example the lattice point represents the following frequency ratio:

:math:`2^{-2} \cdot 3^{0} \cdot 5^{1} = \frac{5}{4}`

When given as a pitch index, this lattice point represents the pitch
that results from transposing the zero pitch by a ratio of
:math:`\frac{5}{4}`, i.e. a "just E0". When given as a pitch
difference it represents the "just major third interval".

:class:`~xenharmlib.core.lattice.LatticePoint` objects in many aspects
behave like regular integers. They support the following arithmetic
operations:

    * **addition** and **subtraction** fullfill the same purposes as
      in the integer case, for example transposing a pitch upwards or
      downwards by combining its pitch index with a pitch diff:

      .. testcode::

         G0 = limit5.rs_pitch('3/2')
         P4 = limit5.rs_interval('4/3')

         pitch_index = G0.pitch_index + P4.pitch_diff
         C1 = limit5.pitch(pitch_index)

         pitch_index = G0.pitch_index - P4.pitch_diff
         D0 = limit5.pitch(pitch_index)

    * **scalar multiplication** can be used to stack an interval

      .. testcode::

         pitch_index = G0.pitch_index + 2 * P4.pitch_diff
         F1 = limit5.pitch(pitch_index)

    * **floor division** and **modulo** can be used to calculate the
      pitch class index and base interval index of a pitch index:

      .. testcode::

         octave_diff = limit5.lattice.point((1, 0, 0))

         pc_index = F1.pitch_index % octave_diff
         bi_index = F1.pitch_index // octave_diff

         print(pc_index)
         print(bi_index)

      .. testoutput::

         LatticePoint(2, -1, 0)
         1

    * **negation** and **abs()** can be used on pitch difference
      values to change direction of an interval or calculate its
      absolute value:

      .. testcode::

         P4_downwards = limit5.diff_interval(-P4.pitch_diff)
         pitch_index = G0.pitch_index + P4_downwards.pitch_diff
         D0 = limit5.pitch(pitch_index)

         P4 = limit5.diff_interval(abs(P4_downwards.pitch_diff))

Floor division and modulo operations can be defined on lattice
points, because lattice points implement a total ordering
based on the frequency ratios they represent:

.. testcode::

   F0 = limit5.vec_pitch((2, -1, 0))
   F1 = F0.transpose_bi_index(1)
   G0 = limit5.vec_pitch((-1, 1, 0))

   assert G0.pitch_index > F0.pitch_index
   assert G0.pitch_index < F1.pitch_index

:class:`~xenharmlib.core.lattice.LatticePoint` objects are bound to the
generator vector to which they relate to. This acts as a safeguard so
lattice points of different origins can not be mixed:

.. testcode::

   from xenharmlib import MultiGenTuning
   from xenharmlib import FrequencyRatio

   tuning_a = MultiGenTuning(
       (FrequencyRatio(2), FrequencyRatio(3)),
       period_vec=(1, 0)
   )
   tuning_b = MultiGenTuning(
       (FrequencyRatio(2), FrequencyRatio(7)),
       period_vec=(1, 0)
   )

   try:
       tuning_a.lattice.point((1, 2)) + tuning_b.lattice.point((4, 0))
   except TypeError as exc:
       print(exc)

.. testoutput::

   unsupported operator +: lattice points originate from different lattices

