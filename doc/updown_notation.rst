Up/Down Notation
======================

:class:`~xenharmlib.notation.updown.UpDownNotation` is an implementation of
Kite Giedraitis’ classic Up/Down Notation for "equal division of the octave"
tunings for divisions between 5 and 72. The original paper can be found
`here <https://tallkite.com/misc_files/notation%20guide%20for%20edos%205-72.pdf>`_.

Up/Down Notation augments the classical Western systems with up and down
arrows (:code:`^`/:code:`v` in ASCII), so in addition to sharps and flats
you can "finetune" notes with an arrow signifying one EDO step in upward
or downward direction.
An Up/Down Notation context can be created by wrapping an
:class:`~xenharmlib.core.tunings.EDOTuning` instance:

.. testcode::

   from xenharmlib import EDOTuning
   from xenharmlib import UpDownNotation

   edo31 = EDOTuning(31)
   n_edo31 = UpDownNotation(edo31)

.. note::

   This section only gives a brief overview of the specifics of
   Up/Down Notation. To find out details on how the notation
   behaves e.g. in regards to the various harmonic primitives,
   head to the :doc:`chapter on primitives <prim_intro>` that
   gives extensive examples on Up/Down notation

Notes
------------------------------------------

Notes in Up/Down Notation are created by giving a pitch class symbol
and the base interval index of the natural of the symbol. For the
subset of notes that are symbolically equal to the Western system,
not much changes:

.. testcode::

   A4 = n_edo31.note('A', 4)
   Eb4 = n_edo31.note('Eb', 4)

   print(A4)
   print(Eb4)

.. testoutput::

   UpDownNote(A, 4, 31-EDO)
   UpDownNote(Eb, 4, 31-EDO)

Up arrows and down arrows are written as prefixes in front of the
natural symbol, while flat and sharp symbols are written behind
it:

.. testcode::

   from xenharmlib import EDOTuning
   from xenharmlib import UpDownNotation

   edo24 = EDOTuning(24)
   n_edo24 = UpDownNotation(edo24)

   # the quartertone that lies in between C and C#
   Cup4 = n_edo24.note('^C', 4)

   # the same quartertone with different enharmonic spelling
   Csharpdown4 = n_edo24.note('vC#', 4)

   print(Cup4)
   print(Csharpdown4)

   # notes with only different enharmonic spelling
   # are considered equal in xenharmlib
   print(Cup4 == Csharpdown4)

.. testoutput::

   UpDownNote(^C, 4, 24-EDO)
   UpDownNote(vC#, 4, 24-EDO)
   True

Intervals
---------------------------------------------------

Interval objects in Up/Down Notation can be obtained from two different
note objects. Xenharmlib names them automatically:

.. testcode::

   from xenharmlib import EDOTuning
   from xenharmlib import UpDownNotation

   edo31 = EDOTuning(31)
   n_edo31 = UpDownNotation(edo31)

   C4 = n_edo31.note('C', 4)
   Eup4 = n_edo31.note('^E', 4)

   supermajor_third = C4.interval(Eup4)
   print(supermajor_third)

.. testoutput::

   UpDownNoteInterval(^M, 3, 31-EDO)

Transposition by intervals is "harmonic function aware":

.. testcode::

   note = Eup4.transpose(supermajor_third)
   print(note)

.. testoutput::

   UpDownNote(^^G#, 4, 31-EDO)

Intervals can be inspected with regard to their shorthand name and
also created from it:

.. testcode::

   print(supermajor_third.shorthand_name)

   P5 = n_edo31.shorthand_interval('P', 5)
   print(P5)

.. testoutput::

   ('^M', 3)
   UpDownNoteInterval(P, 5, 31-EDO)

By convention, imperfect intervals (like major, minor, augmented, diminished)
are notated with their qualifier (:code:`M`, :code:`m`, :code:`A`, :code:`d`)
and ups and downs as prefix, while perfect intervals are only notated with
their qualifier (:code:`P`) if not altered by ups and downs:

.. testcode::

   # down-perfect fifth is notated without the 'P' qualifier
   interval = n_edo31.shorthand_interval('v', 5)
   print(interval)

   # .. while down-minor third is notated with (!) the 'm' qualifier
   interval = n_edo31.shorthand_interval('vm', 3)
   print(interval)

   # the same goes for augmented intervals (e.g. the augmented fifth)
   interval = n_edo31.shorthand_interval('^A', 5)
   print(interval)

.. testoutput::

   UpDownNoteInterval(v, 5, 31-EDO)
   UpDownNoteInterval(vm, 3, 31-EDO)
   UpDownNoteInterval(^A, 5, 31-EDO)

Shortform symbols for augmented (:code:`A`) and diminished intervals
(:code:`d`) can be repeated to retrieve intervals like the double-augmented
third:

.. testcode::

   interval = n_edo31.shorthand_interval('AA', 3)
   print(interval)

   interval = n_edo31.shorthand_interval('dd', 5)
   print(interval)

.. testoutput::

   UpDownNoteInterval(AA, 3, 31-EDO)
   UpDownNoteInterval(dd, 5, 31-EDO)


Reference Frequency
--------------------------------

C0 is tuned to the same frequency as the standard Western system for
:math:`A4 = 440Hz`. However, since A4 is defined differently depending
on the chosen EDO, the :math:`A4 = 440Hz` relationship is only left
intact for EDOs that are multiples of 12:

.. testcode::

   from xenharmlib import EDOTuning
   from xenharmlib import UpDownNotation

   for d in [12, 24, 31]:
       edo = EDOTuning(d)
       n_edo = UpDownNotation(edo)
       A4 = n_edo.note('A', 4)
       print(d, A4.frequency.to_float())

.. testoutput::

   12 440.0
   24 440.0
   31 437.54730702501126

If you want to have frequency equality on A4 instead of C0, you can
redefine the notation instance like this:

.. testcode::

   from xenharmlib import EDOTuning
   from xenharmlib import UpDownNotation
   from xenharmlib import Frequency

   # first define a standard notation instance
   edo31 = EDOTuning(31)
   n_edo31 = UpDownNotation(edo31)

   # then calculate the frequency ratio between the
   # desired frequency for A4 and the current one
   ratio = Frequency(440) / n_edo31.note('A', 4).frequency

   # transpose the standard frequency of C0
   new_ref = n_edo31.note('C', 0).frequency * ratio

   # redefine the notation
   edo31 = EDOTuning(31, ref_frequency=new_ref)
   n_edo31 = UpDownNotation(edo31)

   print(n_edo31.note('A', 4).frequency.to_float())

.. testoutput::

   440.0


Implementation Details
---------------------------------

Xenharmlib's implementation differs from the paper in a couple of minor ways:

* EDOs for which the paper does recommend subnotation are not generated by
  subnotation in this implementation. The class is a ‘pure’ implementation
  of the system that does not resort to heuristics even if the pure
  implementation is unfitting for a specific EDO.
* EDOs that are only mentioned in the variant of a flattened fifth (like
  13b, 18b) are calculated in their sharp variant if EDOTuning is used.
* In interval naming, the mid symbol (~) and related symbols (like ^~, v~)
  are not implemented, because they introduce ambiguity when transposing
  notes (There is, e.g., no strict definition whether in 31-EDO C0 transposed
  by ~3 results in the note vE or ^Em)
