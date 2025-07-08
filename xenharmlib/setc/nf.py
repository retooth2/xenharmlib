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
This module implements functions for normal form calculations
"""
from typing import TypeVar
from ..core.scale import PeriodicScale

ScaleT = TypeVar('ScaleT', bound=PeriodicScale)


def nf_forte(scale: ScaleT) -> ScaleT:
    """
    The normal form of the scale according to Alan Forte.

    Returns a rotation of this scale with minimal interval size
    from first to last note and the new root element sitting in
    the first base interval.

    If there is more than one rotation having minimal span the
    tie is broken according to the procedure described by Alan
    Forte:

    For each pair of scales compare the interval from the root
    to the element at scale position index k, counting upwards,
    i.e. comparing the intervals between the root element
    (position 0) and the element at 1, then 2, then 3, etc.
    On the first interval that differs between the first and
    the second scale, break the tie in favor of the scale
    with the smaller interval (the scale in which intervals
    are more "tightly packed to the left")

    In case of an absolute tie, in which multiple scales have
    perfectly same uniform distance (for example the whole
    tone scale), the scale with the lowest pitch class index
    as root is chosen.

    Period normalizes the scale and returns the rotation that
    is most compact and tightly packed to the left.

    .. note::

       A generalization of this method is implemented by the
       :meth:`compact_forte` method.
    """

    if not scale.is_period_normalized:
        raise ValueError(
            'nf_forte is only defined on period normalized scales'
        )

    return compact_forte(scale)


def compact_forte(scale: ScaleT) -> ScaleT:
    """
    A generalization of the :meth:`nf_forte` method

    Returns a rotation of this scale with minimal interval size
    from first to last note and the new root element sitting in
    the first base interval.

    If there is more than one rotation having minimal span the
    tie is broken according to the procedure described by Alan
    Forte:

    For each pair of scales compare the interval from the root
    to the element at scale position index k, counting upwards,
    i.e. comparing the intervals between the root element
    (position 0) and the element at 1, then 2, then 3, etc.
    On the first interval that differs between the first and
    the second scale, break the tie in favor of the scale
    with the smaller interval (the scale in which intervals
    are more "tightly packed to the left")

    In case of an absolute tie, in which multiple scales have
    perfectly same uniform distance (for example the whole
    tone scale), the scale with the lowest pitch class index
    as root is chosen.
    """

    # first round
    # -----------

    # find rotation with minimal span interval

    min_span = None
    r1_candidates = []

    for r_order in range(len(scale)):

        rotation = scale.rotation(r_order)
        span = rotation.spec_interval(0, -1)

        if min_span is None or span < min_span:
            r1_candidates = [rotation]
            min_span = span
        elif min_span is not None and span == min_span:
            r1_candidates.append(rotation)

    if len(r1_candidates) == 1:
        result = r1_candidates[0]
        return result.transpose_bi_index(
            -result[0].bi_index
        )

    # second round
    # ------------

    # more than one rotation with minimal span interval
    # has been found. try to break the tie by applying
    # Alan Forte's approach

    n = len(scale)
    r2_candidates = [r1_candidates[0]]

    for r1_candidate in r1_candidates[1:]:

        # r2_candidates have always the same uniform
        # interval distribution so comparing with the
        # first candidate is sufficient

        r2_candidate = r2_candidates[0]

        for k in range(1, n - 1):
            i1 = r1_candidate.spec_interval(0, k)
            i2 = r2_candidate.spec_interval(0, k)
            if i1 < i2:
                r2_candidates = [r1_candidate]
                break
            elif i1 > i2:
                break
        else:
            # interval distribution is exactly the same,
            # add scale to candidate set
            r2_candidates.append(r1_candidate)

    if len(r2_candidates) == 1:
        result = r2_candidates[0]
        return result.transpose_bi_index(
            -result[0].bi_index
        )

    # third round
    # -----------

    # all candidates have uniform interval structure
    # return the scale whose root has the lowest pc index

    best_candidate = r2_candidates[0]

    for r2_candidate in r2_candidates[1:]:
        if r2_candidate[0].pc_index < best_candidate[0].pc_index:
            best_candidate = r2_candidate

    return best_candidate.transpose_bi_index(
        -best_candidate[0].bi_index
    )


def nf_rahn(scale: ScaleT) -> ScaleT:
    """
    The normal form of the scale according to John Rahn.

    Returns a rotation of this scale with minimal interval size
    from first to last note and the new root element sitting in
    the first base interval.

    If there is more than one rotation having minimal span the
    tie is broken according to the procedure described by John
    Rahn:

    For each pair of scales compare the interval from the root
    to the element at scale position index 0 < k < n, counting
    downwards, i.e. comparing the intervals between the root
    element (position 0) and the element at (n - 1), then
    (n - 2), then (n - 3), etc.
    On the first interval that differs between the first and
    the second scale, break the tie in favor of the scale
    with the smaller interval (the scale in which intervals
    are more "tightly packed to the left")

    In case of an absolute tie, in which multiple scales have
    perfectly same uniform distance (for example the whole
    tone scale), the scale with the lowest pitch class index
    as root is chosen.
    """

    if not scale.is_period_normalized:
        raise ValueError(
            'nf_rahn is only defined on period normalized scales'
        )

    return compact_rahn(scale)


def compact_rahn(scale: ScaleT) -> ScaleT:
    """
    A generalization of the :meth:`nf_rahn` method

    Returns a rotation of this scale with minimal interval size
    from first to last note and the new root element sitting in
    the first base interval.

    If there is more than one rotation having minimal span the
    tie is broken according to the procedure described by John
    Rahn:

    For each pair of scales compare the interval from the root
    to the element at scale position index 0 < k < n, counting
    downwards, i.e. comparing the intervals between the root
    element (position 0) and the element at (n - 1), then
    (n - 2), then (n - 3), etc.
    On the first interval that differs between the first and
    the second scale, break the tie in favor of the scale
    with the smaller interval (the scale in which intervals
    are more "tightly packed to the left")

    In case of an absolute tie, in which multiple scales have
    perfectly same uniform distance (for example the whole
    tone scale), the scale with the lowest pitch class index
    as root is chosen.
    """

    # first round
    # -----------

    # find rotation that is most tightly packed to left
    # according to John Rahns definition

    n = len(scale)
    candidates = []

    for r_order in range(len(scale)):

        rotation = scale.rotation(r_order)

        if not candidates:
            candidates.append(rotation)
            continue

        # candidates have always the same uniform
        # interval distribution so comparing with the
        # first candidate is sufficient
        candidate = candidates[0]

        for k in range(n - 1, 0, -1):
            i1 = rotation.spec_interval(0, k)
            i2 = candidate.spec_interval(0, k)
            if i1 < i2:
                candidates = [rotation]
                break
            elif i1 > i2:
                break
        else:
            # interval distribution is exactly the same,
            # add scale to candidate set
            candidates.append(rotation)

    if len(candidates) == 1:
        result = candidates[0]
        return result.transpose_bi_index(
            -result[0].bi_index
        )

    # second round
    # -----------

    # all candidates have uniform interval structure
    # return the scale whose root has the lowest pc index

    best_candidate = candidates[0]

    for r1_candidate in candidates[1:]:
        if r1_candidate[0].pc_index < best_candidate[0].pc_index:
            best_candidate = r1_candidate

    return best_candidate.transpose_bi_index(
        -best_candidate[0].bi_index
    )
