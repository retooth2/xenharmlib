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
This module implements base classes for frequency representations
(pitches, notes, etc)
"""

from __future__ import annotations

from typing import Self
from typing import Optional
from functools import total_ordering
from abc import ABC
from abc import abstractmethod
from .frequencies import Frequency
from ..exc import IncompatibleOriginContexts


@total_ordering
class FreqRepr(ABC):
    """
    FreqRepr is the base class for all frequency representations
    (pitches, notes, etc). The class implements a total order on
    the set of all frequency representations (based on the total
    order of frequency values). It also saves the origin context
    of the frequency representation (a tuning or notation)

    In addition it defines an abstract method for short string
    representation and a proxy method 'interval' which redirects
    to the interval method of the origin context.
    """

    def __init__(self, origin_context, frequency: Frequency):
        self._origin_context = origin_context
        self._frequency = frequency

    @abstractmethod
    def __hash__(self): ...

    @property
    def origin_context(self):
        """
        The origin context associated with this frequency representation
        """
        return self._origin_context

    @abstractmethod
    def transpose(self, diff) -> Self:
        """
        (Must be implemented by subclasses)
        Transposes the frequency representation
        """

    def interval(self, other: Self):
        """
        Returns an interval between this frequency representation and
        another representation of the same origin context.

        :param other: Another frequency representation of the
            same origin context
        """
        return self.origin_context.interval(self, other)

    def __eq__(self, other) -> bool:
        if not isinstance(other, FreqRepr):
            return False
        return self.frequency == other.frequency

    def __lt__(self, other) -> bool:
        if not isinstance(other, FreqRepr):
            return NotImplemented
        return self.frequency < other.frequency

    @property
    def frequency(self) -> Frequency:
        """
        The frequency of this object
        """
        return self._frequency

    @property
    @abstractmethod
    def short_repr(self) -> str:
        """
        (Must be implemented by subclasses)
        A shortened representation of this note
        (to be used in collection objects like scales)
        """

    def reflection(self, axis: Optional[Self] = None) -> Self:
        """
        A reflection of this pitch/note across a pitch/note axis.
        In technical terms the method calculates the interval from
        this object to the axis and then applies that interval to
        to the axis.

        :param axis: The element across which this object is
            reflected (optional, defaults to the zero element
            of the origin context)
        """

        if axis is None:
            _axis = self.origin_context.zero_element
        else:
            _axis = axis

        interval = self.interval(_axis)
        return _axis.transpose(interval)

    # FIXME: type annotation is omitted here because types have
    # cicular dependencies (we need to find a good solution for
    # this problem soon)
    def scale(self, interval_seq):
        """
        Returns a scale that starts with this note and continues
        with the given interval structure

        :param interval_seq: An interval sequence of the same
            origin context
        """

        if interval_seq.origin_context is not self.origin_context:
            raise IncompatibleOriginContexts(
                'The interval sequence does not originate from the '
                'same origin context'
            )

        current = self
        scale_elements = [self]

        for interval in interval_seq:
            current = current.transpose(interval)
            scale_elements.append(current)

        return self.origin_context.scale(scale_elements)


class SDFreqRepr(FreqRepr):
    """
    Base class for single dimensional frequency representation
    objects. Assumes an integer pitch index in addition to the
    frequency as part of the data structure.

    Implements optimizations on the total order based on pitch
    index data (if objects originate from same context).

    Demands that subclasses implement a transpose method
    """

    def __init__(self, origin_context, frequency: Frequency, pitch_index: int):
        super().__init__(origin_context, frequency)
        self._pitch_index = pitch_index

    def __hash__(self):
        return hash(self._pitch_index)

    @property
    def pitch_index(self) -> int:
        """
        The pitch index of this object
        """
        return self._pitch_index

    def __eq__(self, other) -> bool:
        if not isinstance(other, FreqRepr):
            return False
        if (
            isinstance(other, SDFreqRepr)
            and self.origin_context is other.origin_context
        ):
            return self.pitch_index == other.pitch_index
        return self.frequency == other.frequency

    def __lt__(self, other) -> bool:
        if not isinstance(other, FreqRepr):
            return NotImplemented
        if (
            isinstance(other, SDFreqRepr)
            and self.origin_context is other.origin_context
        ):
            return self.pitch_index < other.pitch_index
        return self.frequency < other.frequency
