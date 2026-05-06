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
The lattice module implements a generalization of pitch indices.

In sparse, equally-spaced tunings the pitch index group
:math:`(\\mathbb{Z}, +)` can be mapped to the frequency
ratio group :math:`(\\mathbb{R}, \\cdot)` by group homomorphism
:math:`H_b` as follows:

    :math:`H_b(x)     := b^x`

    :math:`H_b(x + y) := b^x \\cdot b^y = b^{(x + y)}`

Lattices generalize this homomorphism by mapping a vector
group :math:`(\\mathbb{Z}^n, +)` to the frequency ratio group
:math:`(R, \\cdot)` refering to a base vector B:

    :math:`H_B(X)     := b_1^{x_1} \\cdot b_2^{x_2} \\cdot ... \\cdot b_n^{x_n}`

    :math:`H_B(X + Y) := b_1^{(x_1 + y_1)} \\cdot b_2^{(x_2 + y_2)} \\cdot ... \\cdot b_n^{(x_n + y_n)}`

By defining an order on :math:`\\mathbb{Z}^n` with the following definition

    :math:`X < Y`      iff :math:`H_B(X) < H_B(Y)`

and by introducing scalar multiplication :math:`kX` on :math:`\\mathbb{Z}^n`
as a short form for repeated addition of an element :math:`X` in
:math:`\\mathbb{Z}^n` with itself, equivalency classes on
:math:`\\mathbb{Z}^n` can be obtained by defining division with remainder:

    :math:`\\lfloor \\frac{X}{Y} \\rfloor = C`

    :math:`X \\bmod Y  = k`

    so that :math:`X = kY + C` with :math:`C < Y`

For :math:`n = 1` this reduces to simple integer modulo arithmetic.

Using this definition for a n-dimensional pitch index both pitch class
indices and base interval indices can be obtained with C being the
n-dimensional pitch class index and k being the integer base interval
index.

While for :math:`n = 1` pitch class indices are finite, for
:math:`n > 1` pitch class indices are infinite.
"""

from __future__ import annotations

import operator
from functools import total_ordering
from typing import Tuple
from typing import Self
from .utils import componentwise
from .utils import scalar_op
from .frequencies import FrequencyRatio


class Lattice:
    """
    A Lattice is a point cloud representing a frequency ratio space.
    For a given base :math:`b_1, ...., b_n` and integer lattice coordinates
    :math:`x_1, ..., x_n` the point represents
    :math:`r(X) = b_1^{x_1} \\cdot ... \\cdot b_n^{x_n}`.

    The 0 is understood as an n-dimensional 0-vector and can be obtained
    through the :py:attr:`zero` property.

    :param base: A tuple of frequency ratios
    """

    def __init__(self, base: Tuple[FrequencyRatio, ...]):
        self.base = base

    def point(self, index: Tuple[int, ...]) -> LatticePoint:
        """
        Create a point inside this lattice

        :param index: The lattice coordinates
        """
        return LatticePoint(index, self.base)

    def contains_point(self, point: LatticePoint) -> bool:
        """
        Returns True if a given lattice point is part of
        this lattice, False otherwise.

        :param point: A lattice point
        """
        return self.base == point.base

    @property
    def zero(self) -> LatticePoint:
        """
        Returns the lattice point with the zero vector
        coordinates
        """
        return LatticePoint.zero(self.base)

    def __repr__(self) -> str:

        base_strings = [ratio.short_repr for ratio in self.base]
        base_string = ', '.join(base_strings)
        return f'Lattice({base_string})'


@total_ordering
class LatticePoint:
    """
    A point in a n-dimensional lattice representing a frequency ratio.
    For a given base :math:`b_1, ..., b_n` and integer lattice coordinates
    :math:`x_1, ..., x_n` the point represents
    :math:`r(X) = b_1^{x_1} \\cdot ... \\cdot b_n^{x_n}`.

    The 0 is understood as an n-dimensional 0-vector and can be obtained
    through the :py:meth:`zero` class method.

    For two lattice points X and Y with the same base the class
    implements the following operations:

    * addition (X + Y): defined as vector addition, equivalent
      to frequency ratio multiplication r(X + Y) = r(X) * r(Y)
    * subtraction (X - Y): defined as vector subtraction,
      equivalent to frequency ratio division r(X - Y) = r(X) / r(Y)
    * scalar multiplication (k * X): defined as scalar vector
      multiplication
    * modulo (X % Y): being defined as X - kY so that (X - kY) < Y
      and (X - kY) >= 0
    * floordiv (X // Y): being defined for two lattice points X and
      Y as k with X - kY so that (X - kY) < Y and (X - kY) >= 0
    * equality (X == Y): defined as vector equality X == Y
    * ordering operations (X < Y): defined as X < Y iff r(X) < r(Y)

    As unitary operators the class implements:

    * negation (-X): being defined as component-wise negation or,
      geometrically, point reflection through 0
    * abs (abs(X)): being defined as -X for X < 0, X otherwise

    LatticePoints are also hashable, so they can be used in sets

    :param index: An integer tuple
    :param base: A base vector of frequency ratios with the same
        dimensions as the index
    """

    def __init__(
        self, index: Tuple[int, ...], base: Tuple[FrequencyRatio, ...]
    ):
        if len(index) != len(base):
            raise ValueError(
                'Index vector dimensions must match base dimensions'
            )

        self.index = index
        self.base = base

        ratio = 1
        for x, base in zip(index, base):
            if x >= 0:
                ratio *= base ** x
            else:
                ratio *= FrequencyRatio(1, base ** (-x))

        self._frequency_ratio = ratio

    @classmethod
    def zero(cls, base: Tuple[FrequencyRatio]):
        """
        Returns the 0 vector for a given base
        """

        index = (0,) * len(base)
        return cls(index, base)

    def __hash__(self):
        return hash((self.index, self.base))

    def __repr__(self) -> str:
        return (
            'LatticePoint(' + str(self.index) + ' ^= ' +
            str(self.frequency_ratio) + ')'
        )

    @property
    def frequency_ratio(self) -> FrequencyRatio:
        """
        Returns the frequency ratio represented by this lattice point
        """
        return self._frequency_ratio

    def _ensure_sametype_operand(self, other, op_str: str):

        if not isinstance(other, type(self)):
            raise TypeError(
                f"unsupported operand type(s) for {op_str}: "
                f"'{type(self)}' and '{type(other)}'"
            )

        if self.base != other.base:
            raise TypeError(
                f"unsupported operator {op_str}: "
                f"lattice points originate from different lattices"
            )

    # binary arithmetic operations

    def __add__(self, other: Self) -> Self:

        self._ensure_sametype_operand(other, '+')
        index = componentwise(
            operator.add,
            self.index,
            other.index
        )
        return self.__class__(index, self.base)

    def __sub__(self, other: Self) -> Self:
        self._ensure_sametype_operand(other, '-')
        index = componentwise(
            operator.sub,
            self.index,
            other.index
        )
        return self.__class__(index, self.base)

    def __divmod__(self, other: Self) -> Self:

        self._ensure_sametype_operand(other, '__divmod__')
        zero_point = LatticePoint.zero(self.base)

        if other == zero_point:
            raise ZeroDivisionError()

        k = 0
        current = self

        if other > zero_point:

            while current >= other:
                current -= other
                k += 1

            while current < zero_point:
                current += other
                k -= 1

        if other < zero_point:

            while current <= other:
                current -= other
                k += 1

            while current > zero_point:
                current += other
                k -= 1

        return k, current

    def __mod__(self, other: Self) -> Self:
        self._ensure_sametype_operand(other, '%')
        return divmod(self, other)[1]

    def __floordiv__(self, other: Self) -> int:
        self._ensure_sametype_operand(other, '//')
        return divmod(self, other)[0]

    # scalar multiplication

    def __mul__(self, other: int) -> Self:

        if not isinstance(other, int):
            raise TypeError(
                f"unsupported operand type(s) for *: "
                f"'{type(self)}' and '{type(other)}'"
            )

        index = scalar_op(operator.mul, self.index, other)
        return self.__class__(index, self.base)

    __rmul__ = __mul__

    # unary arithmetic operations

    def __abs__(self):
        zero = LatticePoint.zero(self.base)
        if self >= zero:
            return self
        else:
            return (-self)

    def __neg__(self) -> Self:
        index = tuple(map(lambda x: -x, self.index))
        return self.__class__(index, self.base)

    # comparisons

    def __eq__(self, other):
        if not isinstance(other, LatticePoint):
            return False
        return self.index == other.index and self.base == other.base

    def __lt__(self, other) -> bool:
        self._ensure_sametype_operand(other, '<')
        return self.frequency_ratio < other.frequency_ratio
