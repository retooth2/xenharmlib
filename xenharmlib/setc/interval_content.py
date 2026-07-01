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
This module implements functions relating to interval content
"""

from typing import Tuple


def ic_vector(scale) -> Tuple[int, ...]:
    """
    Returns the interval class vector (also sometimes called
    "interval vector" or "interval content") of a scale as
    an integer tuple.

    The interval class vector is defined as a counting vector
    that counts the interval of every unordered pair of
    pitches/notes in the scale with the first vector position
    being the number of occurences of intervals with ic_index
    1, the second with ic_index 2, etc.

    Consequently the dimensions of the vector depend on the
    number of available interval classes in a tuning, e.g.
    in 12-EDO the vector has length 6, in 31-EDO the vector
    has length 31 // 2 = 15

    .. warning::

       Since the vector dimensions of ic_vector depend on the
       period length of the tuning, only one-dimensional
       tunings are elligible for this function

    :param scale: A scale object originating from any tuning
        with pitch index dimensions of 1.

    :raises ValueError: If scale originates from a tuning with
        multiple generators / lattice point indices
    :raises ValueError: If scale is empty
    """

    if len(scale) == 0:
        raise ValueError('ic_vector cannot be calculated on empty scale')

    eq_diff = scale.tuning.eq_diff

    if not isinstance(eq_diff, int):
        raise ValueError('ic_vector only supports one-dimensional tunings')

    scale = scale.period_normalized()
    result = [0] * (eq_diff // 2)

    for i in range(0, len(scale) - 1):
        for j in range(i + 1, len(scale)):
            interval = scale[i].interval(scale[j])
            result[interval.ic_index - 1] += 1

    return tuple(result)
