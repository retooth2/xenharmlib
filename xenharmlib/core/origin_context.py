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
This module implements the OriginContext class which
is the abstract base class for tunings and notations
"""

from typing import Optional
from typing import Iterable
from typing import Generic
from typing import TypeVar
from abc import ABC
from abc import abstractmethod
from ..exc import IncompatibleOriginContexts
from .freq_repr import FreqRepr
from .interval import Interval
from .scale import Scale

FreqReprT = TypeVar('FreqReprT', bound=FreqRepr)
IntervalT = TypeVar('IntervalT', bound=Interval)
ScaleT = TypeVar('ScaleT', bound=Scale)


class OriginContext(Generic[FreqReprT, IntervalT, ScaleT], ABC):
    """
    OriginContext is the abstract base class for both tunings and notations.
    It defines a unified interface for collection and interval builder
    methods as well as an interface for a defined "zero element" which
    is used as a reference point for other objects.

    OriginContext does not define an interface for the builder method
    of the FreqRepr object (such as pitch or note) as the name and the
    function signature vary greatly from context to context (e.g. one
    dimensional tunings demand an integer as construction argument,
    more-dimensional tunings a vector, notes in periodic tunings
    mostly demand a string symbol and a base interval index, etc)
    """

    def __init__(
        self,
        freq_repr_cls: type[FreqReprT],
        interval_cls: type[IntervalT],
        scale_cls: type[ScaleT],
    ):

        self._freq_repr_cls = freq_repr_cls
        self._interval_cls = interval_cls
        self._scale_cls = scale_cls

    @property
    @abstractmethod
    def zero_element(self) -> FreqReprT:
        """
        The zero element is a reference point, in one-dimensional tunings
        it is the element with index 0, in western notation typically C-0,
        etc
        """

    def interval(self, source: FreqReprT, target: FreqReprT) -> IntervalT:
        """
        Returns an interval having the interval type
        this origin context was configured with

        :raises IncompatibleOriginContexts: If either source or
            target have a different origin context than this one

        :param source: The source of the interval
        :param target: The target of the interval
        """

        # .from_source_and_target can only make sure that
        # the two elements are from the same origin context,
        # not that they are from THIS context. consequently
        # we need to check it here

        for freq_repr in [source, target]:
            if freq_repr.origin_context is not self:
                raise IncompatibleOriginContexts(
                    'At least one in the given interval pair does not '
                    'originate from this origin context'
                )

        return self._interval_cls.from_source_and_target(source, target)

    def scale(self, elements: Optional[Iterable[FreqReprT]] = None) -> ScaleT:
        """
        Returns a scale having the scale type this origin context
        was configured with

        :raises IncompatibleOriginContexts: If at least one given
            element has a different origin context than this one

        :param elements: A list of frequency representations
            originating from this context
        """

        return self._scale_cls(self, elements)
