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

   from xenharmlib import PrimeLimitTuning
   from xenharmlib import FrequencyRatio
   from xenharmlib.periodic import partial

   limit11 = PrimeLimitTuning(11)

   # generate a scale built from the pure
   # harmonic series up to the 11th prime

   scale = limit11.ratio_scale(
       FrequencyRatio(k) for k in range(1, 12)
   ).period_normalized()
   print(scale)

   # show the harmonic structure of the second triad
   # in the scale as an enumerated chord expression

   triad = partial(scale, (1, 3, 5))
   ifan = triad.to_interval_fan()
   print(ifan.to_ec_expr())

.. testoutput::

   PrimeLimitPitchScale([1, 9/8, 5/4, 11/8, 3/2, 7/4], 11-Limit)
   9:11:14

-----------

.. testcode::

   from xenharmlib import EDOTuning
   from xenharmlib import UpDownNotation

   # create a supermajor 7 chord in up/down notation for
   # a tuning defined by 31 divisions of the octave and
   # show the named interval distances between the notes

   edo31 = EDOTuning(31)
   n_edo31 = UpDownNotation(edo31)

   CsupM7 = n_edo31.pc_scale(['C', '^E', 'G', 'Bb'])
   iseq = CsupM7.to_interval_seq()
   print(iseq)

   # use the interval sequence object as a blueprint to
   # create supermajor 7 chords with different root notes

   print(n_edo31.note('vD', 4).scale(iseq))
   print(n_edo31.note('E#', 4).scale(iseq))

.. testoutput::

   UpDownNoteIntervalSeq([^M3, vm3, m3], 31-EDO)
   UpDownNoteScale([vD4, F#4, vA4, vC5], 31-EDO)
   UpDownNoteScale([E#4, ^Gx4, B#4, D#5], 31-EDO)

Features
---------------

A selection of things supported by xenharmlib:

* Scale, interval, sequence and abstract scale calculation in **any
  regular temperament** (including, but not limited to: Western, Turkish
  Makam, Slendro, Just Intonation / Prime Limit Tunings, Quarter-Comma
  Meantone, Bohlen-Pierce, Wendy Carlos' Gamma Tuning)
* Western notation (including interval naming)
* Up/Down notation (a superset of Western notation)
* Complete interval arithmetic with awareness of harmonic function
* Posttonal analysis: Normal form & prime form calculation, pitch class
  set arithmetic, interval vector calculation, etc
* Extraction of playable chords from any scale
* Structure discovery / Pattern matching in scales
* Modulation suggestions for arbitrary key changes
* Approximation of arbitrary frequencies to pitches and notes
  for spectralist compositions, including error calculation

Roadmap
-----------------

Planned for 0.5.0
~~~~~~~~~~~~~~~~~~

* Extended Helmholtz-Ellis JI Pitch Notation
* Arel-Ezgi-Uzdilek notation
* Rothenberg propriety and interval matrices
* Scale generation tools (Euler-Fokker genus, combination product set,
  Moment-of-Symmetry scales, odd limit scales)

Planned for later versions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

(not necessarily in chronological order)

* Templates for traditional music (Western Scales, Makam tetrachords, etc)
* Plugin interface for score rendering backends
* Advanced posttonal analysis
* Utilities for transformation theory

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
   :caption: Intro

   quickstart

.. toctree::
   :maxdepth: 2
   :caption: Harmonic Primitives

   prim_intro
   prim_freq_repr
   prim_interval
   prim_scale
   prim_interval_seq
   prim_interval_fan
   prim_seq

.. toctree::
   :maxdepth: 2
   :caption: Tunings

   primelimit_tunings
   multigen_tunings
   lattice_points

.. toctree::
   :maxdepth: 2
   :caption: Notations

   western_notation
   updown_notation
   adv_notation_features

.. toctree::
   :maxdepth: 2
   :caption: Utilities

   periodic_package
   posttonal

.. toctree::
   :maxdepth: 2
   :caption: API

   core_api
   export_api
   notation_api
   periodic_api
   setc_api

.. toctree::
   :maxdepth: 2
   :caption: Misc

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
