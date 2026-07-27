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
This module implements base classes for intervals
"""

from typing import Self
from typing import SupportsAbs
from typing import Generic
from typing import TypeVar
from functools import total_ordering
from abc import ABC
from abc import abstractmethod
from .frequencies import FrequencyRatio
from .freq_repr import FreqRepr
from .freq_repr import IndexedFreqRepr
from .protocols import Index

FreqReprT = TypeVar('FreqReprT', bound=FreqRepr)


@total_ordering
class Interval(ABC, SupportsAbs, Generic[FreqReprT]):
    """
    Interval is the abstract bass class for all interval types, consisting
    only of an origin context and a frequency ratio. Based on frequency ratio
    it implements the cents property and a total ordering.

    It forces subclasses to implement the __abs__ method, the class method
    from_source_and_target and the property short_repr

    :param origin_context: An origin context (like a tuning or a notation)
    :param frequency_ratio: A frequency ratio object
    """

    def __init__(self, origin_context, frequency_ratio: FrequencyRatio):
        self._origin_context = origin_context
        self._frequency_ratio = frequency_ratio

    @property
    def origin_context(self):
        """
        The context this interval originated from (like a tuning or
        notation)
        """
        return self._origin_context

    @property
    def frequency_ratio(self) -> FrequencyRatio:
        """
        The frequency ratio of this interval (e.g. 2 for an octave)
        """
        return self._frequency_ratio

    def __hash__(self):
        return hash(('Interval', self.frequency_ratio))

    @property
    def sign(self) -> int:
        """
        Returns 1 if this interval is an upward interval, -1
        if it is a downward interval and 0 if it is the
        unison interval
        """
        if self.frequency_ratio > FrequencyRatio(1):
            return 1
        if self.frequency_ratio < FrequencyRatio(1):
            return -1
        return 0

    @abstractmethod
    def __abs__(self) -> Self:
        """
        Returns the absolute of this interval. On downwards interval it
        returns an upwards interval of the same absolute size. On upwards
        intervals it acts as the identity function.
        (must be implemented by subclass)
        """

    @abstractmethod
    def __neg__(self) -> Self:
        """
        Returns the negative of this pitch interval. On downwards
        interval it returns an upwards interval of the same absolute
        size. On upwards intervals it returns the corresponding
        downwards interval
        (must be implemented by subclass)
        """

    @abstractmethod
    def __add__(self, other) -> Self:
        """
        Returns the combination of two intervals
        (must be implemented by subclass)
        """

    def __sub__(self, other) -> Self:
        """
        Subtracts an interval from this one
        """
        return self + (-other)

    def __mul__(self, other) -> Self:
        """
        Scalar multiplication for intervals (which is the same
        as stacking the interval a number of times). Negative
        scalars flip the interval direction. Multiplying by 0
        returns the unison interval
        """

        if not isinstance(other, int):
            raise TypeError(
                f"unsupported operand type(s) for <: "
                f"'{type(self)}' and '{type(other)}'"
            )

        current = self.origin_context.unison_interval

        if other > 0:
            for _ in range(0, other):
                current += self

        if other < 0:
            for _ in range(0, abs(other)):
                current -= self

        return current

    __rmul__ = __mul__

    # methods necessary for total ordering

    def __eq__(self, other):
        if not isinstance(other, Interval):
            return False
        return self.frequency_ratio == other.frequency_ratio

    def __lt__(self, other):
        if not isinstance(other, Interval):
            raise TypeError(
                f"unsupported operand type(s) for <: "
                f"'{type(self)}' and '{type(other)}'"
            )
        return self.frequency_ratio < other.frequency_ratio

    @property
    def cents(self) -> float:
        """
        The interval size in cents (e.g. 1200 for an octave)
        """
        return self.frequency_ratio.cents

    @property
    @abstractmethod
    def short_repr(self) -> str:
        """
        A short string representation of the interval
        (must be implemented by subclass)
        """

    @classmethod
    @abstractmethod
    def from_source_and_target(
        cls, source: FreqReprT, target: FreqReprT
    ) -> Self:
        """
        Constructs an interval from two frequency representations
        (must be implemented by subclass)

        :param source: The starting point of the interval
        :param target: The end point of the interval
        """

    def retune_closest(self, origin_context) -> Self:
        """
        Gets the interval in a target origin context that
        is closest to the frequency ratio of this object.

        :param origin_context: The target origin context

        :raises TypeError: If the target context does not have
            a proper definition of a closest representation to
            a given frequency ratio
        """

        return origin_context.closest_interval(self.frequency_ratio)


IndexedFreqReprT = TypeVar('IndexedFreqReprT', bound=IndexedFreqRepr)
IndexT = TypeVar('IndexT', bound=Index)


class IndexedInterval(
    Interval[IndexedFreqReprT], Generic[IndexT, IndexedFreqReprT]
):
    """
    IndexedInterval extends the Interval class by a pitch_diff property.
    """

    def __init__(
        self,
        origin_context,
        frequency_ratio: FrequencyRatio,
        pitch_diff: IndexT,
    ):
        super().__init__(origin_context, frequency_ratio)
        self._pitch_diff = pitch_diff

    @property
    def pitch_diff(self) -> IndexT:
        return self._pitch_diff
