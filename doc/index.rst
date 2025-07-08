.. admonition:: New Release

   Xenharmlib 0.3.0 has just been released.
   :doc:`Find out what's new<whats_new_0_3_0>`

Welcome to xenharmlib’s documentation!
=================================================

----

   **Xenharmonic (adj.):** Pertaining to music which sounds unlike
   that composed in the familiar 12 tone equal-tempered scale.

   -- *Ivor Darreg*

Xenharmlib is a generalized music theory library that supports traditional
Western and non-western harmonic systems, unconventional microtonal and
macrotonal tunings, diatonic and posttonal set theory and non-standard
notations.

It is easy to use, extendable, and tries to be intuitive. Have a peek:

.. testcode::

   from xenharmlib import WesternNotation
   from xenharmlib.periodic import mod_connectors

   n = WesternNotation()

   # find out which I-III-V triads can be used
   # to modulate between d minor and g major

   d_minor = n.pc_scale(['D', 'E', 'F', 'G', 'A', 'Bb', 'C'])
   g_major = n.pc_scale(['G', 'A', 'B', 'C', 'D', 'E', 'F#'])

   for c in mod_connectors(d_minor, g_major, (0, 2, 4)):
       print(c)

.. testoutput::

   WesternNoteScale([A0, C1, E1])
   WesternNoteScale([C1, E1, G1])

-----------

.. testcode::

   from xenharmlib import EDOTuning
   from xenharmlib import play
   from xenharmlib import UpDownNotation

   # create a supermajor 7 chord on vD for an
   # equal temperament with 31 notes per octave

   edo31 = EDOTuning(31)
   n_edo31 = UpDownNotation(edo31)

   d_down = n_edo31.note('vD', 4)
   SM3 = n_edo31.shorthand_interval('^M', 3)
   P5 = n_edo31.shorthand_interval('P', 5)
   m7 = n_edo31.shorthand_interval('m', 7)

   chord = n_edo31.scale(
      [
         d_down,
         d_down.transpose(SM3),
         d_down.transpose(P5),
         d_down.transpose(m7),
      ]
   )
   print(chord)

.. testoutput::

   UpDownNoteScale([vD4, F#4, vA4, vC5], 31-EDO)

.. code-block:: python

   play(chord)

.. raw:: html

   <audio controls="controls">
         <source src="_static/sounds/edo31_vD_supermajor7_scale.wav" type="audio/wav">
         Your browser does not support the <code>audio</code> element. 
   </audio>

.. code-block:: python

   play(chord, duration=1, play_as_chord=True)

.. raw:: html

   <audio controls="controls">
         <source src="_static/sounds/edo31_vD_supermajor7_chord.wav" type="audio/wav">
         Your browser does not support the <code>audio</code> element. 
   </audio>

-----------

.. testcode::

   from xenharmlib import EDTuning
   from xenharmlib import FrequencyRatio

   # analyze group theoretical properties of
   # Bohlen-Pierce tunings

   bp = EDTuning(13, FrequencyRatio(3))

   p1 = bp.pitch(4)
   p2 = bp.pitch(18)
   i1 = bp.interval(p1, p2)

   print(p1.pc_index)
   print(p2.pc_index)
   print(i1.frequency_ratio)

   dist = i1.get_generator_distance(
      bp.pitch(7)
   )
   print(dist)

.. testoutput::
   :hide:

   4
   5
   FrequencyRatio(3*3**(1/13))
   2

Audience & Design Philosophy
-----------------------------

Xenharmlib is targeted at composers and researchers who already have
basic knowledge in python programming.

Xenharmlib does **not** aim to be a score composition tool, sequencer,
or synthesizer (however it is possible to build such things on top of
it). Rather it wants to provide a toolset for exploring different
concepts of harmonic relations with a scientific focus.

Xenharmlib is object-oriented but mostly designed around functional
programming principles: Objects are considered immutable and methods
do not alter internal states but return modified versions of the
original object.

Features
---------------

A selection of things supported by xenharmlib:

* Equal division tunings (e.g. Western, Modern Arabic, Turkish Makam,
  Bohlen-Pierce, Wendy Carlos' Gamma Scale)
* Western notation (including interval naming)
* Up/Down notation (a superset of Western notation)
* Analysis of intervals, scales, and their relations to one another
* Group theoretical analysis (integer pitches, pitch classes, etc)
* Interval sequence pattern matching
* Modulation suggestions for arbitrary key changes
* Basic posttonal analysis (normal & prime form calculations, inversion, etc)

Roadmap
-----------------

A list of planned features (not necessarily in chronological order):

* Templates for Western music
* Plugin interface for score rendering backends
* Advanced posttonal analysis (interval vectors, z-Relations, Forte numbers)
* Rothenberg propriety and interval matrices
* MOS scale generation utilities
* Just Intonation and prime limit tunings
* Extended Helmholtz-Ellis JI Pitch Notation
* Odd Limit Tunings
* Arel-Ezgi-Uzdilek notation

License
---------------

Xenharmlib is released under the `GNU Public License v3
<https://www.gnu.org/licenses/gpl-3.0.en.html>`_.

You can find the source code hosted on `Gitlab.com
<https://www.gitlab.com/retooth/xenharmlib>`_

Acknowledgments
---------------

Thanks to `Kite Giedraitis <https://www.tallkite.com/>`_ and
`Lumi Pakkanen <https://lumipakkanen.com/>`_ and everyone else on the
Xenharmonic Alliance Discord who was patient with me when I was
struggling to implement UpDownNotation.

Support and Contact
------------------------

If you want to ask for a new feature or report a bug, take it to the
`Gitlab issue page <https://gitlab.com/retooth/xenharmlib/-/issues>`_.
In case you just wanna chat with the maintainer: I often hang around on
the `Xenharmonic Alliance Discord <https://discord.com/invite/FSF5JFT>`_
under the name :code:`@retooth`

User Guide
-------------

In the following, you will find a guide to most of xenharmlib's
features.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   quickstart
   western_notation
   adv_scale_methods
   adv_notation_features
   interval_seq
   periodic_package
   posttonal
   core_api
   export_api
   notation_api
   periodic_api
   setc_api
   changelog

Contributor Guide
---------------------

You are always welcome to open a pull request, however, there are some
prerequisites for a pull request to be accepted that you should know:

* For formatting your commit messages please use
  `conventional commits <https://www.conventionalcommits.org/>`_
* To format your code please use the
  `black code formatter <https://black.readthedocs.io/en/stable/>`_
  with string normalization turned off and maximum line length 79.
  In regards to strings, xemharmlib follows the principle single quotes
  (') for data, double quotes (") for information meant to be read only
  by humans (like exception descriptions) and triple-double quotes (""")
  for docstrings.
* Your code should come with tests that cover everything you have done.
  (This includes branch coverage). Xenharmlib's test framework is
  `pytest <https://docs.pytest.org/>`_
* Your code should come with type annotations. There are a few
  exceptions: Sometimes python's typing system is not mature enough to
  do proper static-like typing (for example it doesn't support
  higher-kinded types). Sometimes there are design reasons to use
  python's dynamism. Just snoop around the existing code to get a
  feeling for this balance.
* Xenharmlib is designed around functional programming principles.
  Objects should not alter their state when calling methods (except
  on initialization methods)

Changelog
---------

For a list of changes see :doc:`changelog`


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
