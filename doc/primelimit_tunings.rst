Prime Limit Tunings
================================================

Introduction
------------------------------

A Prime Limit Tuning is a type of tuning in which each pitch and interval is
characterized by a fraction of two positive integers :math:`\frac{n}{d}`
with the restriction that in their prime factorizations

:math:`n = p_1^{x_1} \cdot p_2^{x_2} \cdot ... \cdot p_k^{x_k}`

:math:`d = p_1^{x_1} \cdot p_2^{x_2} \cdot ... \cdot p_k^{x_k}`

There is no prime :math:`p_{k+1}` bigger than a fixed prime :math:`p_{k}`
(the "prime limit"). In a 5-Limit tuning, for example, every pitch
and interval can be characterized like this:

:math:`\frac{n}{d} = 2^{x_1} \cdot 3^{x_2} \cdot 5^{x_3}`

A Prime Limit tuning can be created in xenharmlib by importing the
:class:`~xenharmlib.core.primelimit.PrimeLimitTuning` class and
making an instance with a specific limit:

.. testcode::

   from xenharmlib import PrimeLimitTuning

   limit7 = PrimeLimitTuning(7)
   E0 = limit7.rs_pitch('5/4')

   print(E0)

.. testoutput::

   PrimeLimitPitch(5/4, 7-Limit)

Xenharmlib will raise an error if the prime factorization of the given
fraction includes a prime that is above the limit:

.. testcode::

   try:
       pitch = limit7.rs_pitch('11/8')
   except Exception as exc:
       print(exc)

.. testoutput::

   Frequency ratio 11/8 surpasses prime limit of 7


Special Builder Methods
--------------------------------

The :meth:`~xenharmlib.core.primelimit.PrimeLimitTuning.rs_pitch` function
is a convenience function specific to prime limit tunings. "RS" stands for
"ratio string", signifying that the data is given as a string expression
that represents a frequency ratio. The tuning class offers equivalent
builder methods for all other harmonic primitives:

.. tabs::

   .. tab:: Pitch

      .. testcode::

         from xenharmlib import PrimeLimitTuning

         limit7 = PrimeLimitTuning(7)
         pitch = limit7.rs_pitch('7/5')

         print(pitch)

      .. testoutput::

         PrimeLimitPitch(7/5, 7-Limit)

   .. tab:: Interval

      .. testcode::

         from xenharmlib import PrimeLimitTuning

         limit7 = PrimeLimitTuning(7)
         just_M3 = limit7.rs_interval('5/4')

         print(just_M3)

      .. testoutput::

         PrimeLimitPitchInterval(5/4, 7-Limit)

   .. tab:: Scale

      .. testcode::

         from xenharmlib import PrimeLimitTuning

         limit7 = PrimeLimitTuning(7)
         G_just_major_triad = limit7.rs_scale(
             ['3/2', '15/8', '9/4']
         )

         print(G_just_major_triad)

      .. testoutput::

         PrimeLimitPitchScale([3/2, 15/8, 9/4], 7-Limit)

   .. tab:: Interval Sequence

      .. testcode::

         from xenharmlib import PrimeLimitTuning

         limit7 = PrimeLimitTuning(7)
         just_major_triad = limit7.rs_interval_seq(
             ['5/4', '6/5']
         )

         print(just_major_triad)

      .. testoutput::

         PrimeLimitPitchIntervalSeq([5/4, 6/5], 7-Limit)

   .. tab:: Interval Fan

      .. testcode::

         from xenharmlib import PrimeLimitTuning

         limit7 = PrimeLimitTuning(7)
         just_major_triad = limit7.rs_interval_fan(
             ['1/1', '5/4', '3/2']
         )

         print(just_major_triad)

      .. testoutput::

         PrimeLimitPitchIntervalFan([1, 5/4, 3/2], 7-Limit)

   .. tab:: Pitch Sequence

      .. testcode::

         from xenharmlib import PrimeLimitTuning

         limit7 = PrimeLimitTuning(7)
         C_just_major_triad = limit7.rs_seq(
             ['1/1', '5/4', '3/2']
         )

         print(C_just_major_triad)

      .. testoutput::

         PrimeLimitPitchSeq([1, 5/4, 3/2], 7-Limit)


As a more structured approach, Prime Limit Tunings also offer builder
methods to create harmonic primitives from
:class:`~xenharmlib.core.frequencies.FrequencyRatio` objects:

.. tabs::

   .. tab:: Pitch

      .. testcode::

         from xenharmlib import PrimeLimitTuning
         from xenharmlib import FrequencyRatio

         limit11 = PrimeLimitTuning(11)

         G0 = limit11.ratio_pitch(
             FrequencyRatio(3, 2)
         )

         print(G0)

      .. testoutput::

         PrimeLimitPitch(3/2, 11-Limit)

   .. tab:: Interval

      .. testcode::

         from xenharmlib import PrimeLimitTuning
         from xenharmlib import FrequencyRatio

         limit11 = PrimeLimitTuning(11)

         P5 = limit11.ratio_interval(
             FrequencyRatio(3, 2)
         )

         print(P5)

      .. testoutput::

         PrimeLimitPitchInterval(3/2, 11-Limit)

   .. tab:: Scale

      .. testcode::

         from xenharmlib import PrimeLimitTuning
         from xenharmlib import FrequencyRatio

         limit11 = PrimeLimitTuning(11)
         harmonic_series = limit11.ratio_scale(
             [FrequencyRatio(n) for n in range(1, 12)]
         )

         scale = harmonic_series.period_normalized()
         print(scale)

      .. testoutput::

         PrimeLimitPitchScale([1, 9/8, 5/4, 11/8, 3/2, 7/4], 11-Limit)

   .. tab:: Interval Sequence

      .. testcode::

         from xenharmlib import PrimeLimitTuning
         from xenharmlib import FrequencyRatio

         limit11 = PrimeLimitTuning(11)
         just_major_triad = limit11.ratio_interval_seq(
             [FrequencyRatio(5, 4), FrequencyRatio(6, 5)]
         )

         print(just_major_triad)

      .. testoutput::

         PrimeLimitPitchIntervalSeq([5/4, 6/5], 11-Limit)

   .. tab:: Interval Fan

      .. testcode::

         from xenharmlib import PrimeLimitTuning
         from xenharmlib import FrequencyRatio

         limit11 = PrimeLimitTuning(11)
         harmonic_series = limit11.ratio_interval_fan(
             [FrequencyRatio(n) for n in range(1, 12)]
         )

         print(harmonic_series)

      .. testoutput::

         PrimeLimitPitchIntervalFan([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11], 11-Limit)

   .. tab:: Pitch Sequence

      .. testcode::

         from xenharmlib import PrimeLimitTuning
         from xenharmlib import FrequencyRatio

         limit11 = PrimeLimitTuning(11)
         harmonic_series = limit11.ratio_seq(
             [FrequencyRatio(n) for n in range(1, 12)]
         )

         print(harmonic_series)

      .. testoutput::

         PrimeLimitPitchSeq([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11], 11-Limit)


In most theoretical writings on Just Intonation, scales are given in the form
of xenharmlib's interval fan primitive, e.g. a just major triad is given
as 1/1, 5/4, 3/2 with the unison 1/1 sometimes being omitted and made
implicit (e.g. in the SCL file format). A convenient way to define a
scale or sequence obtained from a theoretical text is therefore
to create an interval fan first and then create a scale or sequence
from a root pitch and the fan:

.. testcode::

   from xenharmlib import PrimeLimitTuning

   limit11 = PrimeLimitTuning(11)

   major_triad = limit11.rs_interval_fan(['1/1', '5/4', '3/2'])
   G4 = limit11.rs_pitch('3/2').transpose_bi_index(4)

   scale = G4.scale(major_triad)
   seq = G4.seq(major_triad)

   print(scale)
   print(seq)

.. testoutput::

   PrimeLimitPitchScale([24, 30, 36], 11-Limit)
   PrimeLimitPitchSeq([24, 30, 36], 11-Limit)

Vice versa, scales and sequences can easily be transformed into the
interval fan form to compare them with theoretical writings:

.. testcode::

   from xenharmlib import PrimeLimitTuning
   from xenharmlib import FrequencyRatio

   limit11 = PrimeLimitTuning(11)

   scale = limit11.ratio_scale([FrequencyRatio(r) for r in range(1, 12)])
   scale = scale.period_normalized()

   seq = limit11.ratio_seq([FrequencyRatio(r) for r in range(1, 5)])

   ifan1 = scale.to_interval_fan()
   ifan2 = seq.to_interval_fan()

   print(ifan1)
   print(ifan2)

.. testoutput::

   PrimeLimitPitchIntervalFan([1, 9/8, 5/4, 11/8, 3/2, 7/4], 11-Limit)
   PrimeLimitPitchIntervalFan([1, 2, 3, 4], 11-Limit)

Prime-Limits also support the creation of interval fans from "enumerated
chord expressions", and vice versa, the transformation of an interval fan
into the expression:

.. testcode::

   from xenharmlib import PrimeLimitTuning

   limit11 = PrimeLimitTuning(11)

   major_triad = limit11.ec_interval_fan('4:5:6')
   print(major_triad)

   minor_triad = limit11.rs_interval_fan(
       ['1/1', '6/5', '3/2']
   )
   expr = minor_triad.to_ec_expr()
   print(expr)

.. testoutput::

   PrimeLimitPitchIntervalFan([1, 5/4, 3/2], 11-Limit)
   10:12:15

Pitch Indices
-------------------------------------------------------------

In the introduction, we have defined intervals and pitches in prime limit
tunings for a limit :math:`p_k` as characterized by the expression:

:math:`\frac{n}{d} = p_1^{x_1} \cdot p_2^{x_2} \cdot ... \cdot p_k^{x_k}`

In turn, this means every pitch and every interval can be characterized
by an integer vector of prime number exponents:

:math:`\vec{X} = (x_1, x_2, ...., x_k)`

This prime exponent vector is called a *Lattice Point* . In the special
case of Prime Limit Tunings, it is also colloquially known as a *Monzo*,
named after composer and theorist Joe Monzo.

Other than in equal temperaments where pitch indices are integers, because
every pitch can be understood in a linear line, pitch indices in Prime
Limit Tunings (and in all multi-generator tunings for that matter) are
lattice points:

.. testcode::

   from xenharmlib import PrimeLimitTuning

   limit5 = PrimeLimitTuning(5)
   E0 = limit5.rs_pitch('5/4')

   print(E0.pitch_index)

.. testoutput::

   LatticePoint(-2, 0, 1)

So far we have talked about builder methods special to prime limit tunings;
however, prime limit tunings also provide the standard index-based builder
methods of every tuning, with the difference that in prime limit tunings
all indices and pitch difference values are lattice points.

Lattice point objects can be created from the tuning object like this:

.. testcode::

   from xenharmlib import PrimeLimitTuning

   limit5 = PrimeLimitTuning(5)
   lp = limit5.lattice.point((-2, 0, 1))
   print(lp)

.. testoutput::

   LatticePoint(-2, 0, 1)

Lattice point objects can be used exactly like integers in the default
builder methods of the tuning:

.. tabs::

   .. tab:: Pitch

      .. testcode::

         from xenharmlib import PrimeLimitTuning

         limit5 = PrimeLimitTuning(5)
         G0 = limit5.pitch(limit5.lattice.point((-1, 1, 0)))

         print(G0)

      .. testoutput::

         PrimeLimitPitch(3/2, 5-Limit)

   .. tab:: Interval

      .. testcode::

         from xenharmlib import PrimeLimitTuning
         from xenharmlib import FrequencyRatio

         limit5 = PrimeLimitTuning(5)
         P5 = limit5.diff_interval(limit5.lattice.point((-1, 1, 0)))

         print(P5)

      .. testoutput::

         PrimeLimitPitchInterval(3/2, 5-Limit)

   .. tab:: Scale

      .. testcode::

         from xenharmlib import PrimeLimitTuning

         limit5 = PrimeLimitTuning(5)
         harmonic_series = limit5.index_scale(
             [
                 limit5.lattice.point((0, 0, 0)),
                 limit5.lattice.point((1, 0, 0)),
                 limit5.lattice.point((0, 1, 0)),
                 limit5.lattice.point((0, 0, 1)),
             ]
         )

         scale = harmonic_series.period_normalized()
         print(scale)

      .. testoutput::

         PrimeLimitPitchScale([1, 5/4, 3/2], 5-Limit)

   .. tab:: Interval Sequence

      .. testcode::

         from xenharmlib import PrimeLimitTuning

         limit5 = PrimeLimitTuning(5)
         just_major_triad = limit5.diff_interval_seq(
             [
                 limit5.lattice.point((-2, 0, 1)),
                 limit5.lattice.point((1, 1, -1)),
             ]
         )

         print(just_major_triad)

      .. testoutput::

         PrimeLimitPitchIntervalSeq([5/4, 6/5], 5-Limit)

   .. tab:: Interval Fan

      .. testcode::

         from xenharmlib import PrimeLimitTuning

         limit5 = PrimeLimitTuning(5)
         harmonic_series = limit5.diff_interval_fan(
             [
                 limit5.lattice.point((0, 0, 0)),
                 limit5.lattice.point((1, 0, 0)),
                 limit5.lattice.point((0, 1, 0)),
                 limit5.lattice.point((0, 0, 1)),
             ]
         )

         print(harmonic_series)

      .. testoutput::

         PrimeLimitPitchIntervalFan([1, 2, 3, 5], 5-Limit)

   .. tab:: Pitch Sequence

      .. testcode::

         from xenharmlib import PrimeLimitTuning

         limit5 = PrimeLimitTuning(5)
         harmonic_series = limit5.index_seq(
             [
                 limit5.lattice.point((0, 0, 0)),
                 limit5.lattice.point((1, 0, 0)),
                 limit5.lattice.point((0, 1, 0)),
                 limit5.lattice.point((0, 0, 1)),
             ]
         )

         print(harmonic_series)

      .. testoutput::

         PrimeLimitPitchSeq([1, 2, 3, 5], 5-Limit)

Lattice points implement a full arithmetic and can be used like integers
are used in one-dimensional tunings. Here is a comparison between adding
pitch differences in an integer-based tuning and in a prime limit tuning.
You will notice that they are structurally the same:

.. testcode::

   from xenharmlib import EDOTuning

   edo31 = EDOTuning(31)

   i1 = edo31.diff_interval(4)
   i2 = edo31.diff_interval(3)
   i3 = edo31.diff_interval(4 + 3)

   print((i1 + i2).pitch_diff == i3.pitch_diff)

.. testoutput::

   True

.. testcode::

   from xenharmlib import PrimeLimitTuning

   limit5 = PrimeLimitTuning(5)

   lp_a = limit5.lattice.point((-2, 0, 1))
   lp_b = limit5.lattice.point((-1, 1, 0))

   i1 = limit5.diff_interval(lp_a)
   i2 = limit5.diff_interval(lp_b)
   i3 = limit5.diff_interval(lp_a + lp_b)

   print((i1 + i2).pitch_diff == i3.pitch_diff)

.. testoutput::

   True

To get a full overview of lattice point arithmetic, take a look at the
dedicated chapter on Lattice Points.

Like every multi-generator tuning, Prime Limit Tunings also implements
shortform builder methods that take tuples instead of lattice point
objects as parameter. The equivalent of the above, more verbose but
more structured approach is this:

.. tabs::

   .. tab:: Pitch

      .. testcode::

         from xenharmlib import PrimeLimitTuning

         limit5 = PrimeLimitTuning(5)
         G0 = limit5.vec_pitch((-1, 1, 0))

         print(G0)

      .. testoutput::

         PrimeLimitPitch(3/2, 5-Limit)

   .. tab:: Interval

      .. testcode::

         from xenharmlib import PrimeLimitTuning
         from xenharmlib import FrequencyRatio

         limit5 = PrimeLimitTuning(5)
         P5 = limit5.vec_interval((-1, 1, 0))

         print(P5)

      .. testoutput::

         PrimeLimitPitchInterval(3/2, 5-Limit)

   .. tab:: Scale

      .. testcode::

         from xenharmlib import PrimeLimitTuning

         limit5 = PrimeLimitTuning(5)
         harmonic_series = limit5.vec_scale(
             [
                 (0, 0, 0),
                 (1, 0, 0),
                 (0, 1, 0),
                 (0, 0, 1),
             ]
         )

         scale = harmonic_series.period_normalized()
         print(scale)

      .. testoutput::

         PrimeLimitPitchScale([1, 5/4, 3/2], 5-Limit)

   .. tab:: Interval Sequence

      .. testcode::

         from xenharmlib import PrimeLimitTuning

         limit5 = PrimeLimitTuning(5)
         just_major_triad = limit5.vec_interval_seq(
             [(-2, 0, 1), (1, 1, -1)]
         )

         print(just_major_triad)

      .. testoutput::

         PrimeLimitPitchIntervalSeq([5/4, 6/5], 5-Limit)

   .. tab:: Interval Fan

      .. testcode::

         from xenharmlib import PrimeLimitTuning

         limit5 = PrimeLimitTuning(5)
         harmonic_series = limit5.vec_interval_fan(
             [
                 (0, 0, 0),
                 (1, 0, 0),
                 (0, 1, 0),
                 (0, 0, 1),
             ]
         )

         print(harmonic_series)

      .. testoutput::

         PrimeLimitPitchIntervalFan([1, 2, 3, 5], 5-Limit)

   .. tab:: Pitch Sequence

      .. testcode::

         from xenharmlib import PrimeLimitTuning

         limit5 = PrimeLimitTuning(5)
         harmonic_series = limit5.vec_seq(
             [
                 (0, 0, 0),
                 (1, 0, 0),
                 (0, 1, 0),
                 (0, 0, 1),
             ]
         )

         print(harmonic_series)

      .. testoutput::

         PrimeLimitPitchSeq([1, 2, 3, 5], 5-Limit)

Special Considerations regarding Tools
--------------------------------------------

Prime Limit Tunings are a model of a subset of the rational numbers. This
means that the number of pitches between every two pitches is infinite.
Consequently, this means that tools that make the assumption that there
is a *finite* number of pitches inside, say, an octave are not applicable
to Prime Limit Tunings. The interval class vector from post-tonal theory,
e.g., assumes that the tuning has a finite number of interval classes,
which is not the case in Prime Limit Tunings:

.. testcode::

   from xenharmlib import PrimeLimitTuning
   from xenharmlib.setc import ic_vector

   limit5 = PrimeLimitTuning(5)
   scale = limit5.rs_scale(['1/1', '5/4', '3/2'])

   try:
       ic_vector(scale)
   except Exception as exc:
       print(exc)

.. testoutput::

   ic_vector only supports one-dimensional tunings

Xenharmlib implements tools as general as possible, so if the definition
of an analytical object does not collide with the assumption of infinity,
it will work. For example, it is possible to calculate the normal form
or prime form of a prime limit tuning scale with the particularity that
the pitch class indices are not integers, but lattice points:

.. testcode::

   from xenharmlib import PrimeLimitTuning
   from xenharmlib.setc import primeform_forte

   limit5 = PrimeLimitTuning(5)
   scale = limit5.rs_scale(['1/1', '5/4', '3/2'])

   p_scale = primeform_forte(scale)
   print(p_scale.pc_indices)

.. testoutput::

   [LatticePoint(0, 0, 0), LatticePoint(1, 1, -1), LatticePoint(-1, 1, 0)]
