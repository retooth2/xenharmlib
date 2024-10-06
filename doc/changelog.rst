Changelog
=======================================

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
