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
Frequencies are the prime substance of pitches. Everything in xenharmlib
(and in music, for that matter) ultimately boils down to frequencies and
their relations to one another. In this module, we implement a couple of
useful representations for frequencies and frequency ratios.
"""

from __future__ import annotations

import sympy as sp
from typing import Self
from typing import TypeAlias
from typing import List
from typing import Optional
from functools import total_ordering
from fractions import Fraction
from .utils import get_primes
from .utils import get_all_primes
from .constants import CENTS_PRECISION

FreqNumber: TypeAlias = int | Fraction | float | sp.Expr


def _to_sp_expr(number: object):
    """
    Takes any python builtin number type and converts to
    an equivalent sympy expression
    """

    # bools are ints for some reason :/
    if isinstance(number, int) and not isinstance(number, bool):
        return sp.Integer(number)

    if isinstance(number, Fraction):
        return sp.Rational(number.numerator, number.denominator)

    if isinstance(number, float):
        return sp.Float(number)

    if isinstance(number, sp.Expr):

        if not number.is_number:
            raise ValueError(
                'SymPy expression can not have any free '
                'variables or undefined functions'
            )

        return number

    if isinstance(number, Frequency):
        return number.sp_expr

    raise ValueError(
        f'Unsupported inner type for frequency type: {type(number)}'
    )


@total_ordering
class Frequency:
    """
    Frequency is the class to which all pitch definitions ultimately
    come down to. Frequencies represent the physical layer of sound,
    stripped from all other abstractions.

    Frequency is a wrapper around symbolic mathematical expressions,
    which are provided by the sympy package. Using those expressions
    instead of floats allows us to do exact precision calculations
    which is especially useful in regards to equal division tunings
    where pitches have irrational frequencies.

    Frequency objects can be constructed by providing an integer,
    float, Fraction or a sympy expression. For example

    >>> from xenharmlib import Frequency
    >>> from fractions import Fraction
    >>> Frequency(440)
    Frequency(440)
    >>> Frequency(1.5)
    Frequency(1.50000000000000)
    >>> Frequency(Fraction(3, 2))
    Frequency(3/2)

    >>> import sympy as sp
    >>> Frequency(sp.Integer(2)**sp.Rational(1, 12))
    Frequency(2**(1/12))

    Frequency objects seamlessly interact with all kinds of numbers

    >>> 3 * Frequency(440)
    Frequency(1320)
    >>> Frequency(3) / 2
    Frequency(3/2)
    >>> Frequency(2) - 2
    Frequency(0)
    >>> from fractions import Fraction
    >>> Frequency(2) ** Fraction(1, 3)
    Frequency(2**(1/3))
    """

    def __init__(self, number: Self | FreqNumber):
        sp_expr = _to_sp_expr(number)
        self.sp_expr = sp_expr

    def __add__(self, other: Self | FreqNumber):
        other_sp_expr = _to_sp_expr(other)
        return Frequency(self.sp_expr + other_sp_expr)

    def __sub__(self, other: Self | FreqNumber):
        other_sp_expr = _to_sp_expr(other)
        return Frequency(self.sp_expr - other_sp_expr)

    def __mul__(self, other: Self | FreqNumber):
        other_sp_expr = _to_sp_expr(other)
        return Frequency(self.sp_expr * other_sp_expr)

    def __truediv__(self, other: Self | FreqNumber):
        other_sp_expr = _to_sp_expr(other)
        return Frequency(self.sp_expr / other_sp_expr)

    def __floordiv__(self, other: Self | FreqNumber):
        other_sp_expr = _to_sp_expr(other)
        return Frequency(self.sp_expr // other_sp_expr)

    def __mod__(self, other: Self | FreqNumber):
        other_sp_expr = _to_sp_expr(other)
        return Frequency(self.sp_expr % other_sp_expr)

    def __pow__(self, other: Self | FreqNumber):
        other_sp_expr = _to_sp_expr(other)
        return Frequency(self.sp_expr**other_sp_expr)

    def __radd__(self, other: Self | FreqNumber):
        other_sp_expr = _to_sp_expr(other)
        return Frequency(other_sp_expr + self.sp_expr)

    def __rsub__(self, other: Self | FreqNumber):
        other_sp_expr = _to_sp_expr(other)
        return Frequency(other_sp_expr - self.sp_expr)

    def __rmul__(self, other: Self | FreqNumber):
        other_sp_expr = _to_sp_expr(other)
        return Frequency(other_sp_expr * self.sp_expr)

    def __rtruediv__(self, other: Self | FreqNumber):
        other_sp_expr = _to_sp_expr(other)
        return Frequency(other_sp_expr / self.sp_expr)

    def __rfloordiv__(self, other: Self | FreqNumber):
        other_sp_expr = _to_sp_expr(other)
        return Frequency(other_sp_expr // self.sp_expr)

    def __rmod__(self, other: Self | FreqNumber):
        other_sp_expr = _to_sp_expr(other)
        return Frequency(other_sp_expr % self.sp_expr)

    def __rpow__(self, other: Self | FreqNumber):
        other_sp_expr = _to_sp_expr(other)
        return Frequency(other_sp_expr**self.sp_expr)

    def __abs__(self):
        return Frequency(abs(self.sp_expr))

    def __eq__(self, other: object):
        other_sp_expr = _to_sp_expr(other)
        return self.sp_expr == other_sp_expr

    def __lt__(self, other: Self | FreqNumber):
        other_sp_expr = _to_sp_expr(other)
        return self.sp_expr < other_sp_expr

    def __float__(self) -> float:
        return float(self.sp_expr.evalf())

    def __round__(self, ndigits: int = 0) -> float:
        return round(float(self.sp_expr), ndigits)

    def log(self, base: Self | FreqNumber):
        base = _to_sp_expr(base)
        return Frequency(sp.log(self.sp_expr, base))

    @property
    def numerator(self) -> Frequency:
        n, _ = sp.fraction(self.sp_expr)
        return Frequency(n)

    @property
    def denominator(self) -> Frequency:
        _, d = sp.fraction(self.sp_expr)
        return Frequency(d)

    def __repr__(self) -> str:
        return f'Frequency({repr(self.sp_expr)})'

    @classmethod
    def from_monzo(cls, monzo: List[int]):
        """
        Creates a frequency from a monzo. A monzo is a list of
        exponents for the prime numbers, for example, the
        argument [-1, 1] creates the frequency :math:`2^{-1} * 3^1`
        """

        # generate prime numbers

        primes = list(get_primes(len(monzo)))

        numerator = 1
        denominator = 1

        for prime_i, exp in enumerate(monzo):

            if exp < 0:
                denominator *= primes[prime_i] ** abs(exp)
            if exp >= 0:
                numerator *= primes[prime_i] ** (exp)

        return cls(Fraction(numerator, denominator))

    def to_monzo(self):
        """
        Factorizes the frequency into a monzo.
        """

        if not self.sp_expr.is_rational:
            raise ValueError(
                "Frequency is not rational and can not be "
                "represented as a monzo"
            )

        numerator = self.numerator
        denominator = self.denominator

        monzo = []

        def _extend_and_add(monzo, index, value):

            # adds a value to an index of the monzo
            # if that index does not exist, it fills
            # the monzo with zeroes up until to the
            # requested index first

            monzo_len = len(monzo)

            if index >= monzo_len:
                diff = index - monzo_len + 1
                monzo.extend([0 for _ in range(diff)])
            monzo[index] += value

        for i, prime in enumerate(get_all_primes()):

            while numerator != 1:
                if numerator % prime != 0:
                    break
                numerator = numerator // prime
                _extend_and_add(monzo, i, 1)

            while denominator != 1:
                if denominator % prime != 0:
                    break
                denominator = denominator // prime
                _extend_and_add(monzo, i, -1)

            if numerator == 1 and denominator == 1:
                break

        return monzo

    def get_harmonic(self, index: int) -> Frequency:
        """
        Returns the k-th overtone frequency for
        this frequency.

        :param index: Index of the harmonic.
            0 is the original frequency, 1 the
            first harmonic, etc
        """

        return Frequency(self + (index * self))

    def get_harmonics(
        self, limit: Optional[Frequency] = None
    ) -> List['Frequency']:
        """
        Returns a list of overtone frequencies for
        this note

        :param limit: (optional) upper-frequency limit
            of the list in Hz, defaults to the average
            audible maximum of the human ear of
            20KHz
        """

        if limit is None:
            limit = Frequency(20_000)

        frequency = self
        frequencies = []
        i = 0

        while True:
            frequency = self.get_harmonic(i)
            if frequency > limit:
                break
            frequencies.append(frequency)
            i += 1

        return frequencies

    @property
    def cents(self):
        """
        The cents equivalent of this frequency
        """

        return round(1200 * self.log(2), CENTS_PRECISION)
