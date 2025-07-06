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
This module implements functions for prime form calculations
"""
from typing import TypeVar
from .nf import nf_forte
from .nf import nf_rahn
from ..core.scale import PeriodicScale

ScaleT = TypeVar('ScaleT', bound=PeriodicScale)


def primeform_forte(scale: ScaleT) -> ScaleT:
    """
    The prime form of the scale according to Alan Forte's method.

    Transforms the scale by first calculating its normal form,
    then zero-normalizing it to receive the first candidate,
    then inverting the first candidate and putting the result
    in normal order, then zero normalizing it to receive the
    second candidate.

    The tie between the two candidates is then broken according
    to the procedure described by Alan Forte:

    For each pair of scales compare the interval from the root
    to the element at scale position index k, counting upwards,
    i.e. comparing the intervals between the root element
    (position 0) and the element at 1, then 2, then 3, etc.
    On the first interval that differs between the first and
    the second scale, break the tie in favor of the scale
    with the smaller interval.

    :param scale: The input scale
    """

    if not scale.is_period_normalized:
        raise ValueError(
            'primeform_forte is only defined on period normalized scales'
        )

    nf_a = nf_forte(scale)
    candidate_a = nf_a.zero_normalized()

    inverted = candidate_a.reflection()
    nf_b = nf_forte(inverted)
    candidate_b = nf_b.zero_normalized()

    # break the tie between the two according
    # to the forte tie breaking method:

    n = len(scale)

    for k in range(1, n - 1):
        i1 = candidate_a.spec_interval(0, k)
        i2 = candidate_b.spec_interval(0, k)
        if i1 < i2:
            return candidate_a
        elif i1 > i2:
            return candidate_b

    # the two scales are identical
    return candidate_a


def primeform_rahn(scale: ScaleT) -> ScaleT:
    """
    The prime form of the scale according to John Rahn's method.

    Transforms the scale by first calculating its normal form,
    then zero-normalizing it to receive the first candidate,
    then inverting the first candidate and putting the result
    in normal order, then zero normalizing it to receive the
    second candidate.

    The tie between the two candidates is then broken according
    to the procedure described by John Rahn:

    For each pair of scales compare the interval from the root
    to the element at scale position index 0 < k < n, counting
    downwards, i.e. comparing the intervals between the root
    element (position 0) and the element at (n - 1), then
    (n - 2), then (n - 3), etc.
    On the first interval that differs between the first and
    the second scale, break the tie in favor of the scale
    with the smaller interval.

    :param scale: The input scale
    """

    if not scale.is_period_normalized:
        raise ValueError(
            'primeform_rahn is only defined on period normalized scales'
        )

    nf_a = nf_rahn(scale)
    candidate_a = nf_a.zero_normalized()

    inverted = candidate_a.reflection()
    nf_b = nf_rahn(inverted)
    candidate_b = nf_b.zero_normalized()

    # break the tie between the two according
    # to the rahn tie breaking method:

    n = len(scale)

    for k in range(n - 1, 0, -1):
        i1 = candidate_a.spec_interval(0, k)
        i2 = candidate_b.spec_interval(0, k)
        if i1 < i2:
            return candidate_a
        elif i1 > i2:
            return candidate_b

    # the two scales are identical
    return candidate_a
