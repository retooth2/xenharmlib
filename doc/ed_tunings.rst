Equal Division Tunings
==================================

Equal division tunings divide an equivalency interval into a finite number
of steps, with each pitch having the same interval ratio to its successor.
The most well-known equal division tuning is 12-EDO, the standard
contemporary Western system that divides an octave into 12 equal
steps.

In general, equal division tunings can be created by defining the
number of divisions and the equivalency interval in the constructor
of the :class:`~xenharmlib.core.tunings.EDTuning` class:

.. testcode::

   from xenharmlib import FrequencyRatio
   from xenharmlib import EDTuning

   # create a tuning that divides the frequency ratio of 3
   # (a tritave) into 13 equal steps (this tuning is also
   # known as the "Bohlen-Pierce Tuning")
   ed13_3 = EDTuning(13, FrequencyRatio(3))

Equal division tunings that slice up the octave (having frequency ratio 2)
are also called "Equal Division of the Octave Tunings" (or EDO for short):

.. testcode::

   from xenharmlib import FrequencyRatio
   from xenharmlib import EDTuning

   # create the modern Western tuning
   ed12_2 = EDTuning(12, FrequencyRatio(2))

As a short form, EDOs can also be created by the
:class:`~xenharmlib.core.tunings.EDOTuning` class, which sets the frequency
ratio of the equivalency interval implicitly:

.. testcode::

   from xenharmlib import EDOTuning

   # this tuning is equivalent to the above ed12_2
   edo12 = EDOTuning(12)

By default, xenharmlib sets the frequency of the 0-pitch of equal division
tunings to about 16.35 Hz, which is the default frequency for C0 in an
equally tempered Western system. You can change the frequency of the
0-pitch with the :code:`ref_frequency` parameter:

.. testcode::

   from xenharmlib import Frequency
   from xenharmlib import FrequencyRatio
   from xenharmlib import EDTuning
   from xenharmlib import EDOTuning

   new_ref = Frequency(20)

   ed13_3 = EDTuning(13, FrequencyRatio(3), ref_frequency=new_ref)
   print(ed13_3.pitch(0).frequency.to_float())

   edo24 = EDOTuning(24)
   print(ed24.pitch(0).frequency.to_float())

.. testoutput::

   20.0
   20.0
