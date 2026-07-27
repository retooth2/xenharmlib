Enharmonic Strategies
===================================

As you already know, each notation layer object has a unique counterpart in
the pitch layer: Every note maps to exactly one pitch, and every note interval
to exactly one pitch interval, etc.

However, the reverse is not true: In 12-EDO, the pitch with index 10 could be
notated in an infinite number of ways: Bb, A#, Cbb, Dbbbb, etc. Whether
index 10 should be understood as Bb or A# depends on various contexts
(at least in tonal music). A mapping from pitches to notes must therefore
be opinionated: It has to choose one note over all the others.

Because no mapping fits every use case and not every use case can be foreseen,
mappings from pitch layer objects to notation layer objects are not
implemented directly in the respective classes but outsourced to objects
that act as a drop-in piece for notations with enharmonic ambiguity.
These are called *enharmonic strategies*. In object-oriented programming,
strategies are a common design pattern to give the user a choice on *how*
a certain functionality is implemented. The term implies that there are
different strategies to tackle a problem.

Most notations with enharmonic ambiguity come with a default enharmonic
strategy, for example UpDownNotation:

.. testcode::

   from xenharmlib import EDOTuning
   from xenharmlib import UpDownNotation

   edo12 = EDOTuning(12)
   n_edo12 = UpDownNotation(edo12)

   note = n_edo12.guess_note(edo12.pitch(3))
   print(note)

.. testoutput::

   UpDownNote(D#, 0, 12-EDO)

The default strategy for UpDownNotation is a heuristic that first sets all the
naturals and then fills in the gaps between the naturals with sharps/flats
from the left and right bordering notes in an alternating fashion. It then
fills the leftover gaps with ups/downs in the same way. (If there is a tie,
then sharps/ups win against flats/downs)

.. testcode::

   edo31 = EDOTuning(31)
   n_edo31 = UpDownNotation(edo31)

   pitch_scale = edo31.scale(
       edo31.pitch_range(0, 18)
   )

   note_scale = n_edo31.guess_note_scale(pitch_scale)
   print(note_scale)

.. testoutput::

   UpDownNoteScale([C0, Dbb0, C#0, Db0, Cx0, D0, Ebb0, D#0, Eb0, Dx0, E0, Fb0, E#0, F0, Gbb0, F#0, Gb0, Fx0], 31-EDO)

This behavior can be changed by resetting the enharmonic strategy of the
notation. An alternative strategy for UpDownNotation is to use
upwards-pointing accidentals (sharps/ups) for all the gaps:

.. testcode::

   from xenharmlib.notation.updown import UpwardsEnharmStrategy

   edo31 = EDOTuning(31)
   n_edo31 = UpDownNotation(edo31)

   strategy = UpwardsEnharmStrategy(n_edo31)
   n_edo31.enharm_strategy = strategy

   pitch_scale = edo31.scale(
       edo31.pitch_range(0, 18)
   )

   note_scale = n_edo31.guess_note_scale(pitch_scale)
   print(note_scale)

.. testoutput::

   UpDownNoteScale([C0, ^C0, C#0, ^C#0, Cx0, D0, ^D0, D#0, ^D#0, Dx0, E0, ^E0, E#0, F0, ^F0, F#0, ^F#0, Fx0], 31-EDO)

Please note that enharmonic strategies only work in the context of the
notation they are originally designed for.

The following strategies are available for UpDownNotation:

  * :class:`~xenharmlib.notation.updown.MixedLeftEnharmStrategy` (default)
  * :class:`~xenharmlib.notation.updown.MixedRightEnharmStrategy`
  * :class:`~xenharmlib.notation.updown.UpwardsEnharmStrategy`
  * :class:`~xenharmlib.notation.updown.DownwardsEnharmStrategy`

A (maybe unexpected) side effect of employing a different enharmonic strategy
is that interval names can change drastically:

.. testcode::

   from xenharmlib.notation.updown import DownwardsEnharmStrategy

   edo12 = EDOTuning(12)
   n_edo12 = UpDownNotation(edo12)

   interval = edo12.interval(
       edo12.pitch(0), edo12.pitch(3)
   )
   n_interval1 = n_edo12.guess_note_interval(interval)
   print(n_interval1)

   strategy = DownwardsEnharmStrategy(n_edo12)
   n_edo12.enharm_strategy = strategy

   n_interval2 = n_edo12.guess_note_interval(interval)
   print(n_interval2)

.. testoutput::

    UpDownNoteInterval(A, 2, 12-EDO)
    UpDownNoteInterval(m, 3, 12-EDO)

Apart from the direct conversion methods, enharmonic strategies enrich the
feature set of other functions of notation layer objects. For example,
they make it possible to use integers in the transpose methods:

.. testcode::

   edo12 = EDOTuning(12)
   n_edo12 = UpDownNotation(edo12)

   c0 = n_edo12.note('C', 0)
   print(c0.transpose(3))

.. testoutput::

    UpDownNote(D#, 0, 12-EDO)

Enharmonic strategies are especially useful for post-tonal music where
transformations of musical objects dismiss functional differences of
notes and intervals but a degree of notational familiarity is still
desired. For example, the :math:`T_3` operation can easily be applied
on a scale:

.. testcode::

   edo12 = EDOTuning(12)
   n_edo12 = UpDownNotation(edo12)

   c_maj = n_edo12.natural_scale()
   print(c_maj.transpose(3))

.. testoutput::

    UpDownNoteScale([D#0, F0, G0, G#0, A#0, C1, D1], 12-EDO)

Please be aware that *in tonal music* this is **not** a valid D# major scale,
even though the pitches are exactly the same. When writing tonal music,
you should not use integers for transpositions but rather note intervals.
Observe the difference:

.. testcode::

   c0 = n_edo12.note('C', 0)
   dsharp0 = n_edo12.note('D#', 0)
   interval = c0.interval(dsharp0)

   print(c_maj.transpose(interval))

.. testoutput::

    UpDownNoteScale([D#0, E#0, Fx0, G#0, A#0, B#0, Cx1], 12-EDO)

If you want to choose the note names for each pitch class yourself, you can
use the :meth:`~xenharmlib.core.enharm_strategies.PCBlueprintStrategy` class
to set each note name manually. This more general class works with all
periodic notations:

.. testcode::

   from xenharmlib.core.enharm_strategies import PCBlueprintStrategy

   edo12 = EDOTuning(12)
   n_edo12 = UpDownNotation(edo12)

   pc_note_names = [
       'C', 'C#', 'D', 'Eb',
       'E', 'F', 'F#', 'G',
       'G#', 'A', 'Bb', 'B'
   ]
   custom_strategy = PCBlueprintStrategy(
       [n_edo12.note(s, 0) for s in pc_note_names]
   )
   n_edo12.enharm_strategy = custom_strategy

   c0 = n_edo12.note('C', 0)
   print(c0.transpose(1))
   print(c0.transpose(3))

.. testoutput::

   UpDownNote(C#, 0, 12-EDO)
   UpDownNote(Eb, 0, 12-EDO)


Designing your own enharmonic strategy from scratch
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

PCBlueprintStrategies are quite primitive. They do not take into account any
context (for example, the original accidental directions of a note scale,
which could indicate the key and a suitable transposition). If you want to
create a heuristic more to your needs or devise an intelligent strategy
to contribute to the library itself, read on.

There are two types of methods in notations that delegate to an enharmonic
strategy object. Methods that *always* delegate to the strategy object
(for example, the pcs complement method) and methods that *sometimes*
delegate to it (for example, the transpose methods that only delegate
if the provided parameter is an integer)

In general, an enharmonic strategy has the following structure:

.. code:: python

   from xenharmlib.core.enharm_strategies import EnharmonicStrategy

   class MyStrategy(EnharmonicStrategy):

       def function_name(self, caller_object, *args):
           ...

The interface definition for enharmonic strategies is as follows:

.. testcode::

   from xenharmlib.core.enharm_strategies import EnharmonicStrategy

   class MyStrategy(EnharmonicStrategy):

       def guess_note(self, notation, pitch):
           """
           The method notation.guess_note delegates to this function.
           It should return a suitable note for the provided pitch
           """
           return notation.note('C', 0)

       def guess_note_interval(self, notation, pitch_interval):
           """
           The method notation.guess_note_interval delegates to this
           function. It should return a suitable note interval for
           the provided pitch interval
           """
           return notation.interval(
               notation.note('C', 0),
               notation.note('C', 3),
           )

       def guess_note_scale(self, notation, pitch_scale):
           """
           The method notation.guess_note_scale delegates to this
           function. It should return a suitable note scale for the
           provided pitch scale
           """
           return notation.scale(
               [notation.note('C', 0), notation.note('C', 3)]
           )

       def guess_note_interval_seq(self, notation, pitch_interval_seq):
           """
           The method notation.guess_note_interval_seq delegates to this
           function. It should return a suitable note interval sequence
           for the provided pitch interval sequence
           """
           return notation.interval_seq(
               [
                   notation.shorthand_interval('M', 2),
                   notation.shorthand_interval('m', 2),
               ]
           )

       def guess_note_interval_fan(self, notation, pitch_interval_fan):
           """
           The method notation.guess_note_interval_fan delegates to this
           function. It should return a suitable note interval fan for
           the provided pitch interval fan
           """
           return notation.interval_fan(
               [
                   notation.shorthand_interval('P', 1),
                   notation.shorthand_interval('m', 2),
               ]
           )

       def guess_note_seq(self, notation, pitch_seq):
           """
           The method notation.guess_note_seq delegates to this
           function. It should return a suitable note sequence for the
           provided pitch sequence
           """
           return notation.seq(
               [notation.note('C', 0), notation.note('C', 3)]
           )

       def note_transpose(self, note, pitch_diff):
           """
           The method note.transpose delegates to this function if
           the desired transposition distance was given as a pitch diff.
           It should return a suitable note with the correct pitch
           difference.
           """
           return note.notation.note('C', 0)

       def note_scale_transpose(self, note_scale, pitch_diff):
           """
           The method note_scale.transpose delegates to this
           function if the desired transposition distance was
           given as a pitch diff. It should return a suitable
           note scale with all notes transposed by the correct
           pitch difference.
           """
           return note_scale.notation.scale(
               [notation.note('C', 0), notation.note('C', 3)]
           )

       def note_seq_transpose(self, note_seq, pitch_diff):
           """
           The method note_seq.transpose delegates to this
           function if the desired transposition distance was
           given as a pitch diff. It should return a suitable
           note sequence with all notes transposed by the correct
           pitch difference.
           """
           return note_seq.notation.seq(
               [notation.note('C', 0), notation.note('C', 3)]
           )

       def note_scale_pcs_complement(self, note_scale):
           """
           The method note_scale.pcs_complement delegates to this
           function. It should return a pcs normalized scale with
           all notes not present in the original scale.
           """
           return notation.scale(
               [notation.note('C', 0), notation.note('D#', 0)]
           )
