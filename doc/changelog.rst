Changelog
=======================================

.. _changelog_0_4_0:

0.4.0
--------------------------------------

* refactor: made sounddevice an extra.
  sounddevice needs additional system libraries on various
  platforms (e.g. portaudio on mac), so making sounddevice
  mandatory could land people who just want to play around
  with the library in a configuration hell for a feature
  that is not very central or necessary.
  now sounddevice will only be installed if explicitely
  demanded as the 'console-audio' extra.
* introduced retune_closest methods, deprecated retune method
* introduced closest_x method family, deprecated get_approx_pitch
* added python infix operators for subset / superset tests
* added ic_vector function to setc package
* added to_int() to Frequency and FrequencyRatio
* fix: monzo vectors were lists, should be tuples
* refactor: allow collections to be built from all iterables.
  there was a mismatch the way constructors and builder methods
  for collections were typed: some of them took sequences as
  arguments, some iterables.  this would lead inevitabely to
  confusion, e.g. "why can i use a generator here, but not there?"
* fixed missing enharmonic strategy relay for interval seq
* refactor: Made all constructor parameters refering to primitive classes
  keyword-only. This solves the headache that for every new
  primitive we introduce we need to shuffle things around
  (e.g. the ref_frequency parameter changes its position)
  Also made ref_frequency parameter keyword-only because
  of a somewhat shortsighted design choice in the beginning
  to put it an the end of the constructor args
* introduced interval fan primitive
* introduced sequence primitive
* introduced is_notated_same on interval sequences
* introduced inversion operation on interval sequences
* fixed a bug in scale equivalency functions. while removing the branching
  for identical and compatible origin contexts we unearthed a bug where
  identical and compatible origin contexts were treated differently in
  the sequential equivalency test. while in identical contexts C0-E0-G0
  and C0-E1-G1 were considered sequentially equivalent, in compatible origins
  they were not.
* introduced full interval arithmetic
* introduced multi-generator tunings
* deprecated tuning.get_frequency
* implemented __hash__ on all harmonic primitives
* introduced lattice point indexing
* introduced accidental weights into natural/accidental notation class,
  resulting in a difference between accidental diff vectors (vectors
  where each dimension points to an accidental class, e.g., sharp/flat
  class and up/down class, and values denoting the pitch difference
  introduced by the accidental class) and accidental sum vectors
  (a vector, in which values are just the sum of the occurences
  of each accidental class). **This introduces breaking changes for
  semi-internal functions**, which were never part of the documentation
  prose, but also not prefixed with an underscore. Functions
  note_by_numdef, get_acc_symbol, get_interval_symbol,
  gen_pc_symbol now take an accidental sum vector instead of
  an accidental diff vector

.. _changelog_0_3_0:

0.3.0
--------------------------------------

* Introduced IntervalSeq class for tunings and notations
* Introduced to_interval_seq method on scales, deprecated to_intervals
* Introduced diff_interval and diff_interval_seq on origin contexts
* Introduced Forte/Rahn normal form & prime form
* Introduced periodic extension module
* Fixed an ambiguous definition problem of equivalency on periodic
  scales. (is_equivalent is now deprecated in favor of is_set_equivalent
  and is_seq_equivalent)
* Added WesternNotation as an alias for UpDownNotation(edo12)
* Introduced caching to tests to reduce test run time
* Added root_bi_index parameter to pc_scale method on tuning layer
* Added root_nat_bi_index parameter to pc_scale method on notation layer
* Added spec_interval method to scale class
* Added scale method to note / pitch

.. _changelog_0_2_0:

0.2.0
--------------------------------------

* Introduced enharmonic strategy interface, including PCBlueprintStrategy
  base class and 4 reasonable default implementations for UpDownNotation
* Introduced Python infix set operators for scales
* Added convenience builder methods for scales
* Added index masks and scale methods .partial/.partial_not/.partition
* Introduced new normalization methods for scales:
  .zero_normalized/.period_normalized/.zp_normalized
* Introduced .reflection method for scales
* Removed unnecessary reference pitch recalculation in PeriodicPitchInterval
  builder method
* Optimized scale construction by sorting once instead of resorting element
  by element. Python's lists are not linked lists, so insort is not O(log(n))
  but O(n), meaning the original implementation had O(n^2) complexity instead
  of the expected O(n*log(n))
* Fixed bug in rotation/rotated_up/rotated_down scale methods. 
  When in a scale the last element was equivalent to the first
  element rotation would swallow one element
* Optimized order (<, ==, etc) comparisons on frequency representations.
  If objects to be compared are part of the same tuning context costly
  frequency evaluation and comparison are unnecessary. Instead, objects
  can be compared by their pitch_index
* Optimized frequency and frequency_ratio calculation of frequency
  representations and intervals. Instead of being calculated every
  time the value is needed, values are now calculated *once* on
  object creation
* Refactored constructors for notes and pitches so they now take an
  additional frequency and pitch_index argument. Frequency and pitch_index
  are now calculated in the .note/.pitch builder methods of the origin context
  instead of the constructor.
  *This breaks direct calls to the pitch/note constructor. We justify
  doing this in a minor release because per documentation notes/pitches
  should be constructed by the builder methods of the origin context*
* Introduced FreqRepr and SDFreqRepr base classes to centralize
  methods and properties shared between pitches and notes
* Introduced Interval and SDInterval base classes to centralize
  methods and properties shared between pitch intervals and note intervals
* Introduced OriginContext base class to centralize methods and properties
  shared between tunings and notations.
* Changed the constructor parameters of interval-like classes to align
  with interval base classes.
  *This breaks direct calls to the interval class constructors. We justify
  doing this in a minor release, because per documentation intervals
  should be constructed by the builder methods of the origin context*
* Fixed wrong method signature of transpose_bi_index in protocols
* To provide a unified interface certain builder methods are now considered
  deprecated:
  Notation.note_scale (replaced by .scale),
  Tuning.pitch_scale (replaced by .scale),
  PitchScale.to_pitch_intervals (replaced by .to_intervals),
  NoteScale.to_note_intervals (replaced by .to_intervals)
* Replaced exceptions IncompatibleTunings and IncompatibleNotations with
  a more generic IncompatibleOriginContexts.
  *This breaks possible exception handling in client code, but handling
  those exceptions is a rather unlikely case for now*
* To follow through with xenharmlib's functional design philosophy,
  mutating methods PitchScale.{add_pitch, add_pitch_index} as well
  as NoteScale.add_note are deprecated and replaced by the functional-style
  with_element method that is implemented in the scale base class
* Deprecated PitchScale.from_pitch_indices in favor of the new
  index_scale builder method

0.1.1
--------------------------------------

* Fixed a conceptual issue regarding the Frequency class. In 0.1.0 the
  Frequency class was simply a wrapper around sympy number expressions
  and behaved like any other number otherwise. This lumped together
  frequencies and frequency ratios (and scalars in general) which is
  illegal in physical equations where dimensionful qualities (like
  400 Hz) and dimensionless qualities (like 3/2) can not arbitrarily
  interact arithmetically (a term like 400 Hz + 80 e.g. has simply no
  defined result). For 0.1.1 the Frequency class was refactored so it
  would only define the usual arithmetic operators in regards to the
  appropriate sets. In addition a FrequencyRatio class was introduced
  which acts as a scalar with additional domain-specific functionality
  (like monzo factorization). Thanks to Lumi Pakkanen for pointing out
  the issue and helping me with the implementation.
