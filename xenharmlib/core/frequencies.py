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

import os
from typing import overload
from typing import Self
from typing import TypeAlias
from typing import List
from typing import Optional
from functools import total_ordering
from fractions import Fraction
import sympy as sp

from .utils import get_primes
from .utils import get_all_primes
from .constants import CENTS_PRECISION

# hack for RTD (see doc/conf.py for more info)
if 'READTHEDOCS' in os.environ:
    ScalarLike: TypeAlias = 'int | Fraction | float | FrequencyRatio'
else:
    ScalarLike: TypeAlias = 'int | Fraction | float | FrequencyRatio | sp.Expr'


def _scalar_to_sp_expr(number: object, allow_freq_ratio=True):
    """
    Converts a number to a sympy number expression. A number can be
    an integer, a Fraction, a float, a FrequencyRatio and a sympy
    number expression itself. If a sympy number expression is
    given the function will simply return the expression without
    modification
    """

    # bools are ints for some reason :/
    if isinstance(number, int) and not isinstance(number, bool):
        return sp.Integer(number)

    if isinstance(number, Fraction):
        return sp.Rational(number.numerator, number.denominator)

    if isinstance(number, float):
        # sympy is very strict on floats with different precisions.
        # for example 0.6 != 0.60000 != 3/5. this can have very
        # counter-intuitive results for the user. because of this
        # we convert every float into a fraction
        n, d = number.as_integer_ratio()
        return sp.Rational(n, d)

    if isinstance(number, FrequencyRatio) and allow_freq_ratio:
        return number.sp_expr

    if isinstance(number, sp.Expr):
        if not number.is_number:
            raise ValueError(
                'SymPy expression can not have any free '
                'variables or undefined functions'
            )
        return number

    raise ValueError(
        f'Unsupported inner type for frequency type: {type(number)}'
    )


@total_ordering
class Frequency:
    """
    Frequency is the class to which all pitch definitions ultimately
    come down. Frequencies represent the physical layer of sound,
    stripped from all other abstractions.

    Frequency is a wrapper around symbolic mathematical expressions
    that are provided by the sympy package. Using those expressions
    instead of floats allows us to do exact precision calculations.
    This is especially useful in regard to equal division tunings
    where pitches have irrational frequencies.

    Frequency objects can be constructed by providing an integer,
    float, Fraction or a sympy expression. For example

    >>> from xenharmlib import Frequency
    >>> from fractions import Fraction
    >>> Frequency(440)
    Frequency(440)
    >>> Frequency(1.5)
    Frequency(3/2)
    >>> Frequency(Fraction(3, 2))
    Frequency(3/2)

    >>> import sympy as sp
    >>> Frequency(sp.Integer(2)**sp.Rational(1, 12))
    Frequency(2**(1/12))

    As you might have noticed floats get converted to fractions internally.
    This is done to ensure precision when dealing with frequencies, however
    despite this safeguard using floats has a lot of pitfalls, as you
    can see in this example:

    >>> Frequency(0.2)
    Frequency(3602879701896397/18014398509481984)

    For very technical reasons floats are pretty bad at saving certain
    numbers. So even though it is possible to initialize a Frequency
    from a float it is *highly discouraged*. Instead, you should use
    python's Fraction type

    >>> Frequency(Fraction(2, 10))
    Frequency(1/5)
    >>> Frequency(440 + Fraction(2, 10))
    Frequency(2201/5)

    If you want a more human-readable form you can always convert to float
    after all calculations have been done:

    >>> Frequency(440 + Fraction(2, 10)).to_float()
    440.2

    Frequency objects are part of a dimensionful arithmetic that is defined
    on Frequency objects and various scalars. Frequencies can interact with
    one another and with scalar values in the way how they would in a proper
    physical equation:

    Frequencies can be added to and subtracted from other frequencies:

    >>> Frequency(440) + Frequency(100)
    Frequency(540)
    >>> Frequency(440) - Frequency(100)
    Frequency(340)

    However, the same way as adding a dimensionless quality to a quantity in
    Hz is forbidden in a physical equation Frequency objects and scalar values
    can not be added in xenharmlib:

    >>> Frequency(440) + 100
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    TypeError: unsupported operand type(s) for +: 'Frequency' and 'int'"

    For multiplication the same holds in reverse. Frequencies can be
    multiplied by a scalar, but not with one other:

    >>> from xenharmlib import FrequencyRatio
    >>> 3 * Frequency(100)
    Frequency(300)
    >>> Frequency(200) * FrequencyRatio(3, 2)
    Frequency(300)

    A Frequency can be divided by both a scalar and a frequency. While
    the first case results in a Frequency in Hz, the second will be a
    scalar FrequencyRatio without a physical unit attached to it:

    >>> Frequency(440) / 10
    Frequency(44)
    >>> Frequency(440) / Frequency(100)
    FrequencyRatio(22/5)

    Even though a frequency can be divided by a scalar, the same does not
    hold in reverse: Dividing a scalar by a frequency will raise an error.
    Even though an expression like 1 / 80 Hz is technically legal in a
    physics equation it is outside the scope of this implementation.

    >>> 1 / Frequency(100)
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    TypeError: unsupported operand type(s) for /: 'int' and 'Frequency'"
    """

    def __init__(self, number: ScalarLike):
        sp_expr = _scalar_to_sp_expr(number, allow_freq_ratio=False)
        self.sp_expr = sp_expr

    # A note on error handling: On most arithmetic methods we want to
    # be strict and not give an unknown object the chance to call its
    # right operand method (like __radd__, __rmul__, etc).

    # __add__ and __sub__ are only defined on the Frequency
    # set itself, not in relation with scalars, for example:
    # 40 Hz + 80 Hz = 120 Hz, but 50 Hz + 9 raises an error

    def __add__(self, other: Self) -> Frequency:
        if not isinstance(other, Frequency):
            raise TypeError(
                f"unsupported operand type(s) for +: "
                f"'Frequency' and '{type(other)}'"
            )
        return Frequency(self.sp_expr + other.sp_expr)

    def __sub__(self, other: Self) -> Frequency:
        if not isinstance(other, Frequency):
            raise TypeError(
                f"unsupported operand type(s) for -: "
                f"'Frequency' and '{type(other)}'"
            )
        return Frequency(self.sp_expr - other.sp_expr)

    # __radd__ and __rsub__ are undefined because addition and
    # subtraction is only defined for the Frequency set itself
    # for which __add__ and __sub__ suffice

    # __mul__ / __rmul__ is defined only in relation to scalars
    # 3 * 50 Hz = 150 Hz, but 30 Hz * 20 Hz raises an error

    def __mul__(self, other: ScalarLike) -> Frequency:
        try:
            other_sp_expr = _scalar_to_sp_expr(other)
        except ValueError:
            raise TypeError(
                f"unsupported operand type(s) for *: "
                f"'Frequency' and '{type(other)}'"
            )
        return Frequency(self.sp_expr * other_sp_expr)

    def __rmul__(self, other: ScalarLike) -> Frequency:
        try:
            other_sp_expr = _scalar_to_sp_expr(other)
        except ValueError:
            raise TypeError(
                f"unsupported operand type(s) for *: "
                f"'Frequency' and '{type(other)}'"
            )
        return Frequency(other_sp_expr * self.sp_expr)

    # __truediv__ is defined for both scalars and frequencies
    # but with different result types: dividing a frequency
    # by a scalar returns a frequency: 80 Hz / 2 = 40 Hz,
    # however dividing a frequency by a frequency gives
    # a (scalar) FrequencyRatio: 100 Hz / 20 Hz = 5

    @overload
    def __truediv__(self, other: Self) -> FrequencyRatio: ...

    @overload
    def __truediv__(self, other: ScalarLike) -> Frequency: ...

    def __truediv__(
        self, other: Self | ScalarLike
    ) -> Frequency | FrequencyRatio:

        if isinstance(other, Frequency):
            return FrequencyRatio(self.sp_expr, other.sp_expr)

        try:
            other_sp_expr = _scalar_to_sp_expr(other)
        except ValueError:
            raise TypeError(
                f"unsupported operand type(s) for *: "
                f"'Frequency' and '{type(other)}'"
            )
        return Frequency(self.sp_expr / other_sp_expr)

    # __rtruediv__ is undefined because dividing a scalar through
    # a frequency would make us end up in a whole different part
    # of physics, e.g. 10 / (5 Hz) = 2 Hz^(-1) = 2 seconds

    # __mod__ is only defined inside the Frequency set and not in
    # relation to scalars, because a mod q is defined as r with
    # a = nq + r with |r| < |n|. If scalars were allowed we would
    # receive for 80 Hz % 20 the equation 80 Hz = n * 20 + r.
    # Since n must a scalar, we would have (n * 20) being scalar.
    # In order to obtain r we would need to subtract (n * 20)
    # from both side of the equation, receiving on the left side
    # the expression 80 Hz - (n * 20) which is undefined, since
    # subtraction on the frequency set is only defined for two
    # frequencies, not a frequency and a scalar

    def __mod__(self, other: Self):
        if not isinstance(other, Frequency):
            raise TypeError(
                f"unsupported operand type(s) for %: "
                f"'Frequency' and '{type(other)}'"
            )
        return Frequency(self.sp_expr % other.sp_expr)

    # __rmod__ is undefined because mod is only defined for
    # the Frequency set itself for which __mod__ suffices

    # __floordiv__ is only defined inside the Frequency set and not in
    # relation to scalars, because one definition of floored division
    # is x // y := (x - (x % y)) / y. In this definition the expression
    # 80 Hz // 3 would be (80 Hz - (80 Hz % 3)) / 3 which includes the
    # expression (80 Hz % 3) that is undefined for the reasons stated
    # in the __mod__ section above.

    def __floordiv__(self, other: Self) -> Frequency:
        if not isinstance(other, Frequency):
            raise TypeError(
                f"unsupported operand type(s) for //: "
                f"'Frequency' and '{type(other)}'"
            )
        return Frequency(self.sp_expr // other.sp_expr)

    # __rfloordiv__ is undefined because // is only defined for
    # the Frequency set itself for which __floordiv__ suffices

    # __pow__ and __rpow__ are undefined, because pow() on natural
    # exponents is defined as iterative multiplication of the base
    # with itself: (10 Hz)^3 = 10 Hz * 10 Hz * 10 Hz = 100 Hz^3
    # we exclude this for the same reason we excluded __mul__
    # on two frequencies

    def __abs__(self) -> Frequency:
        return Frequency(abs(self.sp_expr))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Frequency):
            return False
        return self.sp_expr == other.sp_expr

    def __lt__(self, other: Frequency) -> bool:
        if not isinstance(other, Frequency):
            raise TypeError(
                f"'<' not supported between instances of "
                f"'Frequency' and '{type(other)}'"
            )
        return self.sp_expr < other.sp_expr

    def __float__(self) -> float:
        # sympy is very eager to drag other types into its expression
        # system. this causes some problems for us when we have an
        # arithmetic expression like sp.Rational(2, 3) * Frequency(300)
        # where the first operand is a sympy expression and subsequently
        # the first object's __mul__ operator definition has precedence.
        # If we allow standard float conversion sympy will recognize the
        # Frequency object as a float-like object, resulting in the
        # above expression to be a sympy object. This clashes with
        # our definition in __rmul__ stating that the result type
        # of scalar * frequency is frequency. Raising a TypeError
        # deters sympy and makes the expression evaluate according
        # to Frequency.__rmul__
        raise TypeError("For floating point conversion use .to_float()")

    def to_float(self) -> float:
        """
        Converts this object into a floating point number
        """
        return float(self.sp_expr.evalf())

    def __round__(self, ndigits: int = 0) -> float:
        return round(float(self.sp_expr), ndigits)

    def __repr__(self) -> str:
        return f'Frequency({repr(self.sp_expr)})'

    def get_harmonic(self, index: int) -> Frequency:
        """
        Returns the k-th overtone frequency for
        this frequency.

        :param index: Index of the harmonic.
            0 is the original frequency, 1 the
            first harmonic, etc
        """

        return self + (index * self)

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


@total_ordering
class FrequencyRatio:
    """
    The FrequencyRatio class can be understood as an augmented version of
    the Python built-in Fraction type. Different from the built-in Fraction
    type FrequencyRatio can also hold infinite-precision irrational
    fractions like  :math:`\\frac{\\sqrt[12]{2}}{2^{\\frac{1}{12}}}`
    that are essential for equal temperament intervals.

    For infinite-precision calculation, FrequencyRatio wraps the sympy
    package for symbolic arithmetic. Calculation results do not get
    converted to approximations until the user explicitly decides to.

    FrequencyRatio objects can be created like Fractions:

    >>> FrequencyRatio(20, 8)
    FrequencyRatio(5/2)
    >>> FrequencyRatio(3)
    FrequencyRatio(3)

    For both numerator and denominator, sympy expressions can be used:

    >>> import sympy as sp
    >>> FrequencyRatio(sp.Integer(3)**sp.Rational(3, 12), sp.sqrt(3))
    FrequencyRatio(3**(3/4)/3)

    Frequency ratios can also be constructed from prime exponent vectors
    (monzos):

    >>> FrequencyRatio.from_monzo([-11, 7])
    FrequencyRatio(2187/2048)

    Floats are also supported, however *highly discouraged* because of
    the technical limitations of the data type that can lead to surprising
    and unwanted results:

    >>> FrequencyRatio(0.2) # bad
    FrequencyRatio(3602879701896397/18014398509481984)
    >>> FrequencyRatio(2, 10) # good
    FrequencyRatio(1/5)

    Frequency ratios define a standard arithmetic and interact seamlessly
    with other scalar types:

    >>> FrequencyRatio(20, 8) * FrequencyRatio(2)
    FrequencyRatio(5)

    >>> FrequencyRatio(20, 8) + 3
    FrequencyRatio(11/2)
    >>> 3 + FrequencyRatio(20, 8)
    FrequencyRatio(11/2)

    >>> from fractions import Fraction
    >>> FrequencyRatio(20, 8) * Fraction(8, 20)
    FrequencyRatio(1)
    >>> Fraction(16, 20) * FrequencyRatio(20, 8)
    FrequencyRatio(2)

    >>> FrequencyRatio(20) / 10
    FrequencyRatio(2)
    >>> 5 / FrequencyRatio(20)
    FrequencyRatio(1/4)
    """

    def __init__(self, numerator: ScalarLike, denominator: ScalarLike = 1):
        numerator = _scalar_to_sp_expr(numerator)
        denominator = _scalar_to_sp_expr(denominator)
        self.sp_expr = numerator / denominator

    # A note on error handling: On most arithmetic methods we want to
    # be strict and not give an unknown object the chance to call its
    # right operand method (like __radd__, __rmul__, etc). The reason
    # for this is, that sympy is sometimes very lenient on input types
    # and accepts FrequencyRatio as normal number type which can cause
    # an operation with a FrequencyRatio to succeed without returning
    # a FrequencyRatio object. We want to avoid that, since we want a
    # somewhat "closed systems" of Frequency and FrequencyRatio that
    # does not spill other types in operation results.
    # This is why most of the time we raise TypeError and do not
    # return NotImplemented.

    def __add__(self, other: ScalarLike) -> FrequencyRatio:
        try:
            other_sp_expr = _scalar_to_sp_expr(other)
        except ValueError:
            raise TypeError(
                f"unsupported operand type(s) for +: "
                f"'FrequencyRatio' and '{type(other)}'"
            )
        return FrequencyRatio(self.sp_expr + other_sp_expr)

    def __radd__(self, other: ScalarLike) -> FrequencyRatio:
        try:
            other_sp_expr = _scalar_to_sp_expr(other)
        except ValueError:
            raise TypeError(
                f"unsupported operand type(s) for +: "
                f"'{type(other)}' and 'FrequencyRatio'"
            )
        return FrequencyRatio(other_sp_expr + self.sp_expr)

    def __sub__(self, other: ScalarLike) -> FrequencyRatio:
        try:
            other_sp_expr = _scalar_to_sp_expr(other)
        except ValueError:
            raise TypeError(
                f"unsupported operand type(s) for -: "
                f"'FrequencyRatio' and '{type(other)}'"
            )
        return FrequencyRatio(self.sp_expr - other_sp_expr)

    def __rsub__(self, other: ScalarLike) -> FrequencyRatio:
        try:
            other_sp_expr = _scalar_to_sp_expr(other)
        except ValueError:
            raise TypeError(
                f"unsupported operand type(s) for -: "
                f"'{type(other)}' and 'FrequencyRatio'"
            )
        return FrequencyRatio(other_sp_expr - self.sp_expr)

    def __mul__(
        self, other: Frequency | ScalarLike
    ) -> Frequency | FrequencyRatio:

        if isinstance(other, Frequency):
            # give Frequency.__rmul__ a chance
            return NotImplemented

        try:
            other_sp_expr = _scalar_to_sp_expr(other)
        except ValueError:
            raise TypeError(
                f"unsupported operand type(s) for *: "
                f"'FrequencyRatio' and '{type(other)}'"
            )
        return FrequencyRatio(self.sp_expr * other_sp_expr)

    def __rmul__(self, other: ScalarLike) -> FrequencyRatio:
        # we don't need to implement frequency * ratio here
        # because Frequency implements __mul__ for this
        try:
            other_sp_expr = _scalar_to_sp_expr(other)
        except ValueError:
            raise TypeError(
                f"unsupported operand type(s) for *: "
                f"'{type(other)}' and 'FrequencyRatio'"
            )
        return FrequencyRatio(other_sp_expr * self.sp_expr)

    def __truediv__(self, other: ScalarLike) -> FrequencyRatio:
        try:
            other_sp_expr = _scalar_to_sp_expr(other)
        except ValueError:
            raise TypeError(
                f"unsupported operand type(s) for /: "
                f"'FrequencyRatio' and '{type(other)}'"
            )
        return FrequencyRatio(self.sp_expr / other_sp_expr)

    def __rtruediv__(self, other: ScalarLike) -> FrequencyRatio:
        try:
            other_sp_expr = _scalar_to_sp_expr(other)
        except ValueError:
            raise TypeError(
                f"unsupported operand type(s) for /: "
                f"'{type(other)}' and 'FrequencyRatio'"
            )
        return FrequencyRatio(other_sp_expr / self.sp_expr)

    def __floordiv__(self, other: ScalarLike) -> FrequencyRatio:
        try:
            other_sp_expr = _scalar_to_sp_expr(other)
        except ValueError:
            raise TypeError(
                f"unsupported operand type(s) for //: "
                f"'FrequencyRatio' and '{type(other)}'"
            )
        return FrequencyRatio(self.sp_expr // other_sp_expr)

    def __rfloordiv__(self, other: ScalarLike) -> FrequencyRatio:
        try:
            other_sp_expr = _scalar_to_sp_expr(other)
        except ValueError:
            raise TypeError(
                f"unsupported operand type(s) for //: "
                f"'{type(other)}' and 'FrequencyRatio'"
            )
        return FrequencyRatio(other_sp_expr // self.sp_expr)

    def __mod__(self, other: ScalarLike) -> FrequencyRatio:
        try:
            other_sp_expr = _scalar_to_sp_expr(other)
        except ValueError:
            raise TypeError(
                f"unsupported operand type(s) for %: "
                f"'FrequencyRatio' and '{type(other)}'"
            )
        return FrequencyRatio(self.sp_expr % other_sp_expr)

    def __rmod__(self, other: ScalarLike):
        try:
            other_sp_expr = _scalar_to_sp_expr(other)
        except ValueError:
            raise TypeError(
                f"unsupported operand type(s) for %: "
                f"'{type(other)}' and 'FrequencyRatio'"
            )
        return FrequencyRatio(other_sp_expr % self.sp_expr)

    def __pow__(self, other: ScalarLike) -> FrequencyRatio:
        try:
            other_sp_expr = _scalar_to_sp_expr(other)
        except ValueError:
            raise TypeError(
                f"unsupported operand type(s) for ** or pow(): "
                f"'FrequencyRatio' and '{type(other)}'"
            )
        return FrequencyRatio(self.sp_expr**other_sp_expr)

    def __rpow__(self, other: ScalarLike) -> FrequencyRatio:
        try:
            other_sp_expr = _scalar_to_sp_expr(other)
        except ValueError:
            raise TypeError(
                f"unsupported operand type(s) for ** or pow(): "
                f"'{type(other)}' and 'FrequencyRatio'"
            )
        return FrequencyRatio(other_sp_expr**self.sp_expr)

    def __abs__(self) -> FrequencyRatio:
        return FrequencyRatio(abs(self.sp_expr))

    def __eq__(self, other: object) -> bool:
        try:
            other_sp_expr = _scalar_to_sp_expr(other)
        except ValueError:
            return False
        return self.sp_expr == other_sp_expr

    def __lt__(self, other: ScalarLike):
        try:
            other_sp_expr = _scalar_to_sp_expr(other)
        except ValueError:
            raise TypeError(
                f"'<' not supported between instances of "
                f"'FrequencyRatio' and '{type(other)}'"
            )
        return self.sp_expr < other_sp_expr

    def __float__(self) -> float:
        # sympy is very eager to drag other types into its expression
        # system. this causes some problems for us when we have an
        # arithmetic expression like sp.Rational(2, 3) * FrequencyRatio(2)
        # where the first operand is a sympy expression and subsequently
        # the first object's __mul__ operator definition has precedence.
        # If we allow standard float conversion sympy will recognize the
        # FrequencyRatio object as a float-like object, resulting in the
        # above expression to be a sympy object. This clashes with
        # our definition in __rmul__ stating that the result type
        # of scalar * freq ratio is freq ratio. Raising a TypeError
        # deters sympy and makes the expression evaluate according
        # to FrequencyRatio.__rmul__
        raise TypeError("For floating point conversion use .to_float()")

    def to_float(self) -> float:
        """
        Converts this object into a floating point number
        """
        return float(self.sp_expr.evalf())

    def __round__(self, ndigits: int = 0) -> float:
        return round(float(self.sp_expr), ndigits)

    def log(self, base: ScalarLike) -> FrequencyRatio:
        """
        Returns the result of the logarithm of this object

        :param base: The base that should be assumed
            for calculation
        """
        base = _scalar_to_sp_expr(base)
        return FrequencyRatio(sp.log(self.sp_expr, base))

    @property
    def numerator(self) -> FrequencyRatio:
        """
        The numerator of the ratio
        """
        n, _ = sp.fraction(self.sp_expr)
        return FrequencyRatio(n)

    @property
    def denominator(self) -> FrequencyRatio:
        """
        The denominator of the ratio
        """
        _, d = sp.fraction(self.sp_expr)
        return FrequencyRatio(d)

    def __repr__(self) -> str:
        return f'FrequencyRatio({repr(self.sp_expr)})'

    @classmethod
    def from_monzo(cls, monzo: List[int]):
        """
        Creates a frequency ratio from a monzo. A monzo is a
        list of exponents for the prime numbers, for example, the
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
        Factorizes the frequency ratio into a monzo. A monzo is a
        list of exponents for the prime numbers, for example, the
        frequency ratio 3/2 creates the monzo [-1, 1], since
        :math:`2^{-1} * 3^1 = \\frac{3}{2}`
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

    @property
    def cents(self):
        """
        The cents equivalent of this frequency ratio
        """

        return round(1200 * self.log(2), CENTS_PRECISION)
