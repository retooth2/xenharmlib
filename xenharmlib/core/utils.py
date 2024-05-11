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

from typing import Generator


def get_primes(n: int) -> Generator:
    """
    Generates a finite list of primes

    :param n: Number of primes
    """

    for i, prime in enumerate(get_all_primes()):
        yield prime
        if i == n:
            break


def get_all_primes() -> Generator:
    """
    Generates all primes (to be used in a loop
    that has a break condition)
    """

    visited_numbers = []

    k = 1

    while True:
        k += 1
        visited_numbers.append(k)
        for number in visited_numbers[:-1]:
            if k % number == 0:
                break
        else:
            yield k
