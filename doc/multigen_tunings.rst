Custom Multi-Generator Tunings
================================================

Overview
-------------------------------

Multi-Generator Tunings are a generalization of Prime Limit Tunings.
While harmonic primitives in Prime Limit Tuning are characterized by 
instances of prime generators like

:math:`\frac{n}{d} = p_1^{x_1} \cdot p_2^{x_2} \cdot ... \cdot p_k^{x_k}`

Multi-generator tunings relax the requirement for generators, so they can
be any frequency ratio, even irrational ones e.g.

:math:`2^{x_1} \cdot (3 \cdot (\frac{80}{81})^{\frac{1}{4}})^{x_2}`

Multi-Generator Tunings are created by providing the generator frequency
ratios and a period vector that represents a lattice point defining the
period, so another way to create a 3-Limit Tuning is this:

.. testcode::

   from xenharmlib import MultiGenTuning
   from xenharmlib import FrequencyRatio

   limit3 = MultiGenTuning(
       generators=(FrequencyRatio(2), FrequencyRatio(3)),
       eq_diff_vec=(1, 0) # equivalency interval ratio 2
   )

Irrational frequency ratios (like the one in the introductory example)
can be created using frequency ratio arithmetics, for example the
following code example creates a multi-generator quarter-comma-meantone
tuning:

.. testcode::

   from fractions import Fraction
   from xenharmlib import MultiGenTuning
   from xenharmlib import FrequencyRatio

   g3 = FrequencyRatio(3) * FrequencyRatio(80, 81) ** Fraction(1, 4)
   tuning = MultiGenTuning(
       (FrequencyRatio(2), g3),
       eq_diff_vec=(1, 0)
   )

Even EDO tunings can be constructed by custom multi-generator tunings,
e.g. a unnecessarily complicated way to construct 31-EDO is this:

.. testcode::
   
   edo31 = MultiGenTuning(
       (FrequencyRatio(2) ** Fraction(1, 31),),
       eq_diff_vec=(31,)
   )

Like in Prime-Limit-Tunings pitch indices and pitch differences in
Multi-Generator Tunings are lattice points:

.. tabs::

   .. tab:: Pitch

      .. testcode::

         from fractions import Fraction
         from xenharmlib import MultiGenTuning
         from xenharmlib import FrequencyRatio

         g3 = FrequencyRatio(3) * FrequencyRatio(80, 81) ** Fraction(1, 4)
         qcm = MultiGenTuning(
             (FrequencyRatio(2), g3),
             eq_diff_vec=(1, 0)
         )
         G0 = qcm.pitch(qcm.lattice.point((-1, 1)))

         print(G0)

      .. testoutput::

         MultiGenPitch((-1, 1), G=(2, 2*5**(1/4)))

   .. tab:: Interval

      .. testcode::

         from fractions import Fraction
         from xenharmlib import MultiGenTuning
         from xenharmlib import FrequencyRatio

         g3 = FrequencyRatio(3) * FrequencyRatio(80, 81) ** Fraction(1, 4)
         qcm = MultiGenTuning(
             (FrequencyRatio(2), g3),
             eq_diff_vec=(1, 0)
         )
         P5 = qcm.diff_interval(qcm.lattice.point((-1, 1)))

         print(P5)

      .. testoutput::

         MultiGenPitchInterval((-1, 1), G=(2, 2*5**(1/4)))

   .. tab:: Scale

      .. testcode::

         from fractions import Fraction
         from xenharmlib import MultiGenTuning
         from xenharmlib import FrequencyRatio

         g3 = FrequencyRatio(3) * FrequencyRatio(80, 81) ** Fraction(1, 4)
         qcm = MultiGenTuning(
             (FrequencyRatio(2), g3),
             eq_diff_vec=(1, 0)
         )
         harmonic_series = qcm.index_scale(
             [
                 qcm.lattice.point((0, 0)),
                 qcm.lattice.point((1, 0)),
                 qcm.lattice.point((0, 1)),
             ]
         )

         scale = harmonic_series.period_normalized()
         print(scale)

      .. testoutput::

         MultiGenPitchScale([(0, 0), (-1, 1)], G=(2, 2*5**(1/4)))

   .. tab:: Interval Sequence

      .. testcode::

         from fractions import Fraction
         from xenharmlib import MultiGenTuning
         from xenharmlib import FrequencyRatio

         g3 = FrequencyRatio(3) * FrequencyRatio(80, 81) ** Fraction(1, 4)
         qcm = MultiGenTuning(
             (FrequencyRatio(2), g3),
             eq_diff_vec=(1, 0)
         )
         major_triad = qcm.diff_interval_seq(
             [
                 qcm.lattice.point((-6, 4)),
                 qcm.lattice.point((3, -3)),
             ]
         )

         print(major_triad)

      .. testoutput::

         MultiGenPitchIntervalSeq([(-6, 4), (3, -3)], G=(2, 2*5**(1/4)))

   .. tab:: Interval Fan

      .. testcode::

         from fractions import Fraction
         from xenharmlib import MultiGenTuning
         from xenharmlib import FrequencyRatio

         g3 = FrequencyRatio(3) * FrequencyRatio(80, 81) ** Fraction(1, 4)
         qcm = MultiGenTuning(
             (FrequencyRatio(2), g3),
             eq_diff_vec=(1, 0)
         )
         harmonic_series = qcm.diff_interval_fan(
             [
                 qcm.lattice.point((0, 0)),
                 qcm.lattice.point((1, 0)),
                 qcm.lattice.point((0, 1)),
             ]
         )

         print(harmonic_series)

      .. testoutput::

         MultiGenPitchIntervalFan([(0, 0), (1, 0), (0, 1)], G=(2, 2*5**(1/4)))

   .. tab:: Pitch Sequence

      .. testcode::

         from fractions import Fraction
         from xenharmlib import MultiGenTuning
         from xenharmlib import FrequencyRatio

         g3 = FrequencyRatio(3) * FrequencyRatio(80, 81) ** Fraction(1, 4)
         qcm = MultiGenTuning(
             (FrequencyRatio(2), g3),
             eq_diff_vec=(1, 0)
         )
         harmonic_series = qcm.index_seq(
             [
                 qcm.lattice.point((0, 0)),
                 qcm.lattice.point((1, 0)),
                 qcm.lattice.point((0, 1)),
                 qcm.lattice.point((0, 0)),
             ]
         )

         print(harmonic_series)

      .. testoutput::

         MultiGenPitchSeq([(0, 0), (1, 0), (0, 1), (0, 0)], G=(2, 2*5**(1/4)))

As a shortform multi-generator tunings also support builder methods that
only demand the vector tuple instead of the full lattice point object:

.. tabs::

   .. tab:: Pitch

      .. testcode::

         from xenharmlib import MultiGenTuning

         g3 = FrequencyRatio(3) * FrequencyRatio(80, 81) ** Fraction(1, 4)
         qcm = MultiGenTuning(
             (FrequencyRatio(2), g3),
             eq_diff_vec=(1, 0)
         )
         G0 = qcm.vec_pitch((-1, 1))

         print(G0)

      .. testoutput::

         MultiGenPitch((-1, 1), G=(2, 2*5**(1/4)))

   .. tab:: Interval

      .. testcode::

         from xenharmlib import MultiGenTuning
         from xenharmlib import FrequencyRatio

         g3 = FrequencyRatio(3) * FrequencyRatio(80, 81) ** Fraction(1, 4)
         qcm = MultiGenTuning(
             (FrequencyRatio(2), g3),
             eq_diff_vec=(1, 0)
         )
         P5 = qcm.vec_interval((-1, 1))

         print(P5)

      .. testoutput::

         MultiGenPitchInterval((-1, 1), G=(2, 2*5**(1/4)))

   .. tab:: Scale

      .. testcode::

         from xenharmlib import MultiGenTuning

         g3 = FrequencyRatio(3) * FrequencyRatio(80, 81) ** Fraction(1, 4)
         qcm = MultiGenTuning(
             (FrequencyRatio(2), g3),
             eq_diff_vec=(1, 0)
         )
         harmonic_series = qcm.vec_scale(
             [(0, 0), (1, 0), (0, 1)]
         )

         scale = harmonic_series.period_normalized()
         print(scale)

      .. testoutput::

         MultiGenPitchScale([(0, 0), (-1, 1)], G=(2, 2*5**(1/4)))

   .. tab:: Interval Sequence

      .. testcode::

         from xenharmlib import MultiGenTuning

         g3 = FrequencyRatio(3) * FrequencyRatio(80, 81) ** Fraction(1, 4)
         qcm = MultiGenTuning(
             (FrequencyRatio(2), g3),
             eq_diff_vec=(1, 0)
         )
         major_triad = qcm.vec_interval_seq(
             [(-6, 4), (3, -3)]
         )

         print(major_triad)

      .. testoutput::

         MultiGenPitchIntervalSeq([(-6, 4), (3, -3)], G=(2, 2*5**(1/4)))

   .. tab:: Interval Fan

      .. testcode::

         from xenharmlib import MultiGenTuning

         g3 = FrequencyRatio(3) * FrequencyRatio(80, 81) ** Fraction(1, 4)
         qcm = MultiGenTuning(
             (FrequencyRatio(2), g3),
             eq_diff_vec=(1, 0)
         )
         harmonic_series = qcm.vec_interval_fan(
             [(0, 0), (1, 0), (0, 1)]
         )

         print(harmonic_series)

      .. testoutput::

         MultiGenPitchIntervalFan([(0, 0), (1, 0), (0, 1)], G=(2, 2*5**(1/4)))

   .. tab:: Pitch Sequence

      .. testcode::

         from xenharmlib import MultiGenTuning

         g3 = FrequencyRatio(3) * FrequencyRatio(80, 81) ** Fraction(1, 4)
         qcm = MultiGenTuning(
             (FrequencyRatio(2), g3),
             eq_diff_vec=(1, 0)
         )
         harmonic_series = qcm.vec_seq(
             [(0, 0), (1, 0), (0, 1)]
         )

         print(harmonic_series)

      .. testoutput::

         MultiGenPitchSeq([(0, 0), (1, 0), (0, 1)], G=(2, 2*5**(1/4)))


Prime-Limit Isomorphism
--------------------------

You might have noticed that for our quarter-comma meantone example we
used slightly similar generators then we would use if we would create
a 3-Limit tuning. The difference in the second generator is only
marginal:

.. testcode::

   g3 = FrequencyRatio(3) * FrequencyRatio(80, 81) ** Fraction(1, 4)
   print((FrequencyRatio(3) / g3).cents)

.. testoutput::

   5.3765723992

What did we do here? We took the original frequency ratio of 3 and changed
it slightly to get a different harmonic profile. This construction is
called tempering: You take a Prime Limit Tuning and change various
generators slightly to produce a new harmonic system:

Keeping the *structure* of the lattice points the same (both 3-Limit
tuning and our quarter-comma-meantone tuning are indexed by lattice
points having two dimensions), we can easily create tempered versions
of prime limit pre-images:

.. testcode::

   from xenharmlib import PrimeLimitTuning
   from xenharmlib import MultiGenTuning
   from xenharmlib import play

   limit3 = PrimeLimitTuning(3)

   g3 = FrequencyRatio(3) * FrequencyRatio(80, 81) ** Fraction(1, 4)
   qcm = MultiGenTuning(
       (FrequencyRatio(2), g3),
       eq_diff_vec=(1, 0)
   )

   l3_minor_triad = limit3.rs_scale(['1/1', '81/64', '3/2'])

   # the tempered triad
   qcm_minor_triad = qcm.vec_scale(
       l3_minor_triad.monzos
   )
