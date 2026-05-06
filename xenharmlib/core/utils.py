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
from typing import Tuple

# even though we already have numpy as dependency we want to
# define our own vector operations. there are two reasons:
#
#   1. a technical one: when converting tuples of native python
#      integers to numpy arrays for vector operations and then
#      cast them back with tuple() the elements will still be
#      numpy integers instead of python integers which creates
#      input/output inconsistency (and possible problems with
#      libraries expecting python integers and not numpy ones)
#
#   2. a design-related one: often we are in the position to
#      do arithmetic not on integer vectors but on more general
#      "arithmetic object" vectors like vectors of lattice
#      points. if we stay inside the standard python context
#      we can build more abstract vector structures that work
#      on all kinds of objects supporting arithmetic operators


def componentwise(operator, vector_a: Tuple, vector_b: Tuple) -> Tuple:
    """
    Applies an operator componentwise on two tuples with the
    same dimensions.

    :param operator: A binary operator function (typically
        taken from the python builtin operator module)
    :param vector_a: The first operand
    :param vector_b: The second operand
    """
    result = tuple()
    for e_a, e_b in zip(vector_a, vector_b, strict=True):
        e_r = operator(e_a, e_b)
        result += (e_r,)
    return result


def scalar_op(operator, vector: Tuple, scalar) -> Tuple:
    """
    Applies a binary operator on each component of a tuple with
    a scalar value, resulting in another tuple.

    :param operator: A binary operator function (typically
        taken from the python builtin operator module)
    :param vector: The vector operand
    :param scalar: The scalar operand
    """
    result = tuple()
    for element in vector:
        e_r = operator(element, scalar)
        result += (e_r,)
    return result


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
