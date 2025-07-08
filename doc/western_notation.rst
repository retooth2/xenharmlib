Western Notation
======================================

The WesternNotation class is an implementation of the American standard
pitch notation (ASPN), which designates octaves by numbers with C4 being
the "middle C" and a frequency centering of :math:`A4 = 440Hz`.

.. note::

   This chapter only gives a brief overview of features specific
   to this notation. For a general overview on what you can do
   with the various musical objects in xenharmlib head to the
   Quickstart.

A WesternNotation context is created like this:

.. testcode::

   from xenharmlib import WesternNotation

   n = WesternNotation()

Note objects are created as follows:

.. testcode::

   a4 = n.note('A', 4)
   print(a4.frequency)

.. testoutput::

   Frequency(440)

Intervals can be created by their Western shorthand name, with the first
parameter being the interval quality (minor, Major, diminished, 
Augmented) and the second being the scale degree (1-indexed):

.. testcode::

   # augmented five
   aug5 = n.shorthand_interval('A', 5)
   print(aug5.cents)

.. testoutput::

   800.0

.. testcode::

   # diminished fourth
   dim4 = n.shorthand_interval('d', 4)
   print(dim4.cents)

.. testoutput::

   400.0

.. testcode::

   # major third
   maj3 = n.shorthand_interval('M', 3)
   print(maj3.cents)

.. testoutput::

   400.0

.. testcode::

   # minor second
   min2 = n.shorthand_interval('m', 2)
   print(min2.cents)

.. testoutput::

   100.0

Intervals in WesternNotation are "harmonic function aware", meaning that
transposition by enharmonically equal but functionally different
intervals will result in enharmonically equal but functionally
different notes:

.. testcode::

   C4 = n.note('C', 4)
   
   note_a = C4.transpose(maj3)
   note_b = C4.transpose(dim4)

   print(note_a)
   print(note_b)

.. testoutput::

   WesternNote(E, 4)
   WesternNote(Fb, 4)

.. testcode::

   print(note_a == note_b)

.. testoutput::

   True

Intervals created by two notes (e.g. by calling the
:meth:`~xenharmlib.core.freq_repr.FreqRepr.interval` method of a note)
can be examined to obtain their shorthand name:

.. testcode::

   D4 = n.note('D', 4)
   Fsharp4 = n.note('F#', 4)

   interval = D4.interval(Fsharp4)

   print(interval.shorthand_name)

.. testoutput::

   ('M', 3)


Other than with the
:meth:`~xenharmlib.core.origin_context.OriginContext.scale` method
scales in WesternNotation can be defined by only providing a list
of pitch class symbols and an (optional) root base interval with the
:meth:`~xenharmlib.core.notation.NatAccNotation.pc_scale` method:

.. testcode::

   C4maj = n.pc_scale(['C', 'D', 'E', 'F', 'G', 'A', 'B'], 4)
   print(C4maj)

.. testoutput::

   WesternNoteScale([C4, D4, E4, F4, G4, A4, B4])

WesternNotation implements a default enharmonic strategy, so transposition
by integers is possible:

.. testcode::

   D4 = n.note('D', 4)
   note = D4.transpose(1)
   print(note)

.. testoutput::

   WesternNote(D#4])
