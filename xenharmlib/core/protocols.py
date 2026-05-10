# This file is part of xenharmlib.
#
# xenharmlib is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# xenharmlib is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with xenharmlib. If not, see <https://www.gnu.org/licenses/>.

"""
The protocols module outlines type protocols for various
purposes. With protocols we can annotate variables and
arguments according to the needed capabilities without
making complicated inheritance hierarchies.
"""

from __future__ import annotations
from typing import Protocol
from typing import runtime_checkable
from typing import List
from collections.abc import Iterator
from .frequencies import Frequency


@runtime_checkable
class Index(Protocol):
    """
    Protocol for pitch index types that defines a range of operations:
    Binary arithmetic operators (+, -, *), unitary arihmetic operators
    (negation and abs), equality and ordering (=, <, >, <=, >=) and a
    __hash__ function
    """

    def __add__(self, other): ...
    def __sub__(self, other): ...
    def __mul__(self, other): ...

    def __radd__(self, other): ...
    def __rsub__(self, other): ...
    def __rmul__(self, other): ...

    def __neg__(self): ...
    def __abs__(self): ...

    def __eq__(self, other): ...
    def __lt__(self, other): ...
    def __gt__(self, other): ...
    def __le__(self, other): ...
    def __ge__(self, other): ...

    def __hash__(self): ...


@runtime_checkable
class PeriodicIndex(Index, Protocol):
    """
    Protocol for periodic index types that extends the Index protocol
    with the operations modulo (%), floor division (//) and divmod()
    """

    def __divmod__(self, other): ...
    def __mod__(self, other): ...
    def __floordiv__(self, other): ...


@runtime_checkable
class HasFrequency(Protocol):
    """
    Protocol for everything that provides a frequency
    property (all types of pitch and note classes)
    """

    @property
    def frequency(self) -> Frequency: ...


@runtime_checkable
class PitchLike(HasFrequency, Protocol):
    """
    An extension protocol for HasFrequency. Demands in
    addition that the properties tuning and pitch_index
    exists
    """

    @property
    def tuning(self): ...

    @property
    def pitch_index(self) -> Index: ...


@runtime_checkable
class SDPitchLike(HasFrequency, Protocol):
    """
    An extension protocol for HasFrequency. Demands in
    addition that the properties tuning and pitch_index
    exists and pitch_index has type integer.
    """

    @property
    def tuning(self): ...

    @property
    def pitch_index(self) -> int: ...


@runtime_checkable
class PeriodicPitchLike(PitchLike, Protocol):
    """
    An extension protocol for PitchLike. Demands in
    addition that the properties pc_index and bi_index
    exist
    """

    @property
    def pc_index(self) -> PeriodicIndex: ...

    @property
    def bi_index(self) -> int: ...

    def transpose_bi_index(self, bi_diff: int) -> PeriodicPitchLike: ...

    def pcs_normalized(self) -> PeriodicPitchLike: ...


@runtime_checkable
class SDPeriodicPitchLike(SDPitchLike, Protocol):
    """
    An extension protocol for SDPitchLike. Demands in
    addition that the properties pc_index and bi_index
    exist and pc_index is an integer
    """

    @property
    def pc_index(self) -> int: ...

    @property
    def bi_index(self) -> int: ...

    def transpose_bi_index(self, bi_diff: int) -> SDPeriodicPitchLike: ...

    def pcs_normalized(self) -> SDPeriodicPitchLike: ...


@runtime_checkable
class NoteLike(PitchLike, Protocol):
    """
    An extension protocol for PitchLike. Demands in
    addition that the property notation exists
    """

    @property
    def notation(self): ...


@runtime_checkable
class PeriodicNoteLike(PeriodicPitchLike, Protocol):
    """
    An extension protocol for PeriodicPitchLike. Demands
    in addition that the property notation and pc_symbol
    exists
    """

    @property
    def notation(self): ...

    @property
    def pc_symbol(self) -> str: ...


@runtime_checkable
class HasFrequencyRatio(Protocol):
    """
    Protocol for all types that define a ratio between
    two frequencies. Demands that a frequency_ratio
    property and a cents property is present
    """

    @property
    def frequency_ratio(self) -> Frequency: ...

    @property
    def cents(self) -> float: ...


@runtime_checkable
class SDPitchIntervalLike(HasFrequencyRatio, Protocol):
    """
    Extension protocol for HasFrequencyRatio. Demands the
    existence of a tuning and a pitch_diff property
    """

    @property
    def tuning(self): ...

    @property
    def pitch_diff(self) -> int: ...


@runtime_checkable
class HasFrequencies(Protocol):
    """
    Protocol for everything that provides a frequencies
    property listing multiple frequencies
    """

    @property
    def frequencies(self) -> List[Frequency]: ...


@runtime_checkable
class HasFrequencyRatios(Protocol):
    """
    Protocol for all types that define multiple ratios between
    two frequencies. Demands that a frequency_ratios property
    and a cents property is present
    """

    @property
    def frequency_ratios(self) -> List[Frequency]: ...

    @property
    def cents(self) -> List[Frequency]: ...


@runtime_checkable
class PitchScaleLike(HasFrequencies, HasFrequencyRatios, Protocol):
    """
    Extension protocol that builds both on HasFrequencies and
    HasFrequencyRatios. Demands in addition that the properties
    tuning, pitch_indices and pitch_diffs are present.
    """

    @property
    def tuning(self): ...

    @property
    def pitch_indices(self) -> List[int]: ...

    @property
    def pitch_diffs(self) -> List[int]: ...

    def __iter__(self) -> Iterator: ...

    def __len__(self) -> int: ...

    def __getitem__(self, index_or_slice: int | slice): ...


@runtime_checkable
class PeriodicPitchScaleLike(PitchScaleLike, Protocol):
    """
    Extension protocol that builds on PitchScaleLike. Demands
    in addition that the properties pc_indices and bi_indices
    are present.
    """

    @property
    def pc_indices(self) -> List[int]: ...

    @property
    def bi_indices(self) -> List[int]: ...

    def pcs_normalized(self) -> PeriodicPitchScaleLike: ...


@runtime_checkable
class NoteScaleLike(PitchScaleLike, Protocol):
    """
    Extension protocol for PitchScaleLike. Demands in addition
    that the property notation is present
    """

    @property
    def notation(self): ...


@runtime_checkable
class PeriodicNoteScaleLike(PeriodicPitchScaleLike, Protocol):
    """
    Extension protocol for PeriodicPitchScaleLike. Demands in addition
    that the property notation and the property pc_symbols is present
    """

    @property
    def notation(self): ...

    @property
    def pc_symbols(self) -> List[str]: ...


class TuningLike(Protocol):
    """
    Protocol for basic tuning class structure
    (used to type mixin classes)
    """

    def pitch(self, pitch_index): ...
    def __len__(self) -> int: ...
