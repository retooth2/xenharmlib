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
their relations to one another. In this module we implement a couple of
useful representations for frequencies and frequency ratios.
"""

from __future__ import annotations

import math
from typing import *
from numbers import Number
from fractions import Fraction
from .utils import get_primes
from .utils import get_all_primes
from .constants import CENTS_PRECISION

class Frequency(Fraction):

    """
    In xenharmlib frequencies are build as python Fraction types. 
    This might be a bit slower than floats but it makes better
    approximations in the lower ranges for EDOs and even creates
    exact values for just intonation tunings.

    Frequencies can be instantiated exactly like Fractions:

    >>> Frequency(440) # 440 Hz
    >>> Frequency(3, 2) # The perfect fifth ratio
    """

    @classmethod
    def from_monzo(cls, monzo: List[int]):
        """
        Creates a frequency from a monzo. A monzo is a list of
        exponents for the prime numbers, for example the
        argument [-1, 1] creates the frequency :math:`2^{-1} * 3^1`
        """

        # generate prime numbers

        primes = list(
            get_primes(len(monzo))
        )

        numerator = 1
        denominator = 1

        for prime_i, exp in enumerate(monzo):

            if exp < 0:
                denominator *= primes[prime_i]**abs(exp)
            if exp >= 0:
                numerator *= primes[prime_i]**(exp)

        return cls(numerator, denominator)

    def to_monzo(self):
        """
        Factorizes the frequency into a monzo.
        """

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
                monzo.extend(
                    [0 for _ in range(diff)]
                )
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

    def get_harmonic(
        self,
        index: int
    ) -> Frequency:
        """
        Returns the k-th overtone frequency for
        this frequency.

        :param index: Index of the harmonic.
            0 is the original frequency, 1 the
            first harmonic, etc    
        """

        return Frequency(
            self + (index * self)
        )

    def get_harmonics(
        self,
        limit: Optional[Frequency] = None
    ) -> List['Frequency']:
        """
        Returns a list of overtone frequencies for
        this note

        :param limit: (optional) upper frequency limit
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

        return round(
            1200 * math.log(self, 2),
            CENTS_PRECISION
        )