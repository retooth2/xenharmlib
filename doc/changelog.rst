Changelog
=======================================


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
