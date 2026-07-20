# Xenharmlib

Xenharmlib is a generalized music theory library that supports traditional
Western and non-western harmonic systems, unconventional microtonal and
macrotonal tunings, diatonic and posttonal set theory and non-standard
notations.

[Click here for the official documentation](https://xenharmlib.readthedocs.io/en/latest/)

## Features

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

## Roadmap

A list of planned features (not necessarily in chronological order):

* Extended Helmholtz-Ellis JI Pitch Notation
* Arel-Ezgi-Uzdilek notation
* Rothenberg propriety and interval matrices
* Scale generation tools (Euler-Fokker genus, combination product set,
  Moment-of-Symmetry scales, odd limit scales)
* Templates for traditional music (Western Scales, Makam tetrachords, etc)
* Plugin interface for score rendering backends
* Advanced posttonal analysis
* Utilities for transformation theory
