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
from typing import Generic
from typing import TypeVar
from functools import total_ordering
from abc import ABC
from abc import abstractmethod
from .frequencies import FrequencyRatio
from .freq_repr import FreqRepr
from .freq_repr import SDFreqRepr
from .constants import CENTS_PRECISION

FreqReprT = TypeVar('FreqReprT', bound=FreqRepr)


@total_ordering
class Interval(Generic[FreqReprT], ABC):
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

    @abstractmethod
    def __abs__(self) -> Self:
        """
        Returns the absolute of this pitch interval. On downwards
        interval it returns an upwards interval of the same absolute
        size. On upwards intervals it acts as the identity function.
        (must be implemented by subclass)
        """

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
        return round(1200 * self.frequency_ratio.log(2), CENTS_PRECISION)

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


SDFreqReprT = TypeVar('SDFreqReprT', bound=SDFreqRepr)


class SDInterval(Interval[SDFreqReprT]):
    """
    SDInterval (single dimensional interval) extends the Interval class
    by a pitch_diff property.
    """

    def __init__(
        self,
        origin_context,
        frequency_ratio: FrequencyRatio,
        pitch_diff: int,
    ):
        super().__init__(origin_context, frequency_ratio)
        self._pitch_diff = pitch_diff

    @property
    def pitch_diff(self) -> int:
        return self._pitch_diff
