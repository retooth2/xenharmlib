.. _whats_new_0_3_0:

What's new in xenharmlib 0.3.0?
======================================

The development of version 0.3.0 focused on further development of
posttonal analysis tools, the introduction of interval sequences
and utilities for extensions of periodic scales.
For an in-detail view of all the changes, see the
:ref:`Changelog<changelog_0_3_0>`

.. contents:: Table of Contents
   :depth: 1
   :local:
   :backlinks: none
 
Posttonal analysis
--------------------------------------

With 0.3.0 xenharmlib implements normal form and prime form calculation
of scales (both Forte and Rahn algorithm) for all tunings:

.. testcode::

   from xenharmlib import EDOTuning
   from xenharmlib.setc import primeform_forte
   
   edo31 = EDOTuning(31)
   scale = edo31.index_scale([2, 5, 9, 13, 16, 18, 24, 29])

   print(primeform_forte(scale).pc_indices)

.. testoutput::

   [0, 2, 5, 9, 13, 16, 20, 25]

See :ref:`Posttonal Basics<posttonal_nf_pf>` chapter for more information.

Western Notation
--------------------------------

Contemporary Western notation is now introduced as its own notation class.
(This makes it less confusing for newcomers or western-only researchers):

.. testcode::

   from xenharmlib import EDOTuning
   from xenharmlib import WesternNotation

   n = WesternNotation()

   c_maj = n.pc_scale(['C', 'D', 'E', 'F', 'G', 'A', 'B'], 4)
   print(c_maj)

   interval = c_maj[1].interval(c_maj[4])
   print(interval)

.. testoutput::

   WesternNoteScale([C4, D4, E4, F4, G4, A4, B4])
   WesternNoteInterval(P, 4)

Interval sequences
--------------------------------

Already in 0.2.x scales could be transformed to lists of intervals:

.. testsetup::

   from xenharmlib import EDOTuning
   from xenharmlib import UpDownNotation
   
   edo12 = EDOTuning(12)
   n_edo12 = UpDownNotation(edo12)
   edo31 = EDOTuning(31)
   n_edo31 = UpDownNotation(edo31)

.. testcode::

   c_maj = n_edo12.pc_scale(['C', 'D', 'E', 'F', 'G', 'A', 'B'])
   intervals = c_maj.to_intervals()

With 0.3.0 intervals sequences become first class citizens of the library,
right next to scales, intervals and notes:

.. testcode::

   c_maj = n_edo12.pc_scale(['C', 'D', 'E', 'F', 'G', 'A', 'B'])
   maj = c_maj.to_interval_seq()
   print(maj)

.. testoutput::

   UpDownNoteIntervalSeq([M2, M2, m2, M2, M2, M2], 12-EDO)

Interval sequences allow to define abstractions of scales, for example
defining an abstract major scale *as such*. These abstractions can then
be used for templating or as scale classifiers or search patterns.
Read more about it in the :ref:`chapter about interval sequences<interval_seq>`

Periodic Scale Extension Tools
--------------------------------

Version 0.3.0 features the :code:`periodic` package, a collection of
useful tools for periodic extension of scales, including structure
discovery, scalar transposition, modulation suggestions and triad
extraction. See the :ref:`package documentation<periodic_ext>`
for a full feature description.
