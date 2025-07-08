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
This module implements utils to match structures in scales
"""
from .utils import scale_element
from .iter import cutouts
from typing import List
from typing import Tuple


def find_iseq(scale, interval_seq) -> List[Tuple[int, ...]]:
    """
    Searches an interval sequence in the periodic extension of
    the given scale and returns a list of periodic index masks
    indicating the partial scales which fit the sequence.

    >>> from xenharmlib import EDOTuning
    >>> from xenharmlib import UpDownNotation
    >>> from xenharmlib import periodic
    >>>
    >>> edo12 = EDOTuning(12)
    >>> n_edo12 = UpDownNotation(edo12)
    >>>
    >>> c_major_scale = n_edo12.natural_scale()
    >>> c_major_triad = c_major_scale.partial((0, 2, 4))
    >>> major_triad = c_major_triad.to_interval_seq()
    >>>
    >>> periodic.find_iseq(c_major_scale, major_triad)
    [(0, 2, 4), (3, 5, 7), (4, 6, 8)]

    :param scale: A period normalized scale
    :param interval_seq: An interval sequence
    """

    if not scale.is_period_normalized:
        raise ValueError(
            'find_iseq is only defined on period normalized scales'
        )

    masks = []

    for start_index, start in enumerate(scale):

        mask = (start_index,)
        interval_list = list(interval_seq)

        while interval_list:

            search_interval = interval_list.pop(0)

            # assume scale is fitting to interval seq
            # unless determined otherwise
            fitting = True
            offset = 1

            while True:

                last_index = mask[-1]
                next_index = last_index + offset
                offset += 1

                a = scale_element(scale, last_index)
                b = scale_element(scale, next_index)
                current_interval = a.interval(b)

                if current_interval == search_interval:
                    mask = mask + (next_index,)
                    break

                if current_interval > search_interval:
                    fitting = False
                    break

            if not fitting:
                break

        if fitting:
            masks.append(mask)

    return masks


def mod_connectors(scale_a, scale_b, cutout_pattern):
    """
    Returns partial scales of a specific structure (such as I-III-V) that
    are shared between two scales. These partial scales can be interpreted
    as chords that connect two different keys ("modulation connectors").
    If you e.g. want to pivot from C major to G minor using standard triads
    you can get the key-connecting chords like this:

    >>> from xenharmlib import EDOTuning
    >>> from xenharmlib import UpDownNotation
    >>> from xenharmlib.periodic import mod_connectors
    >>>
    >>> edo12 = EDOTuning(12)
    >>> n_edo12 = UpDownNotation(edo12)
    >>>
    >>> c_maj = n_edo12.pc_scale(['C', 'D', 'E', 'F', 'G', 'A', 'B'])
    >>> g_min = n_edo12.pc_scale(['G', 'A', 'Bb', 'C', 'D', 'Eb', 'F'])
    >>>
    >>> for connector in mod_connectors(c_maj, g_min, (0, 2, 4)):
    ...     print(connector)
    UpDownNoteScale([D0, F0, A0], 12-EDO)
    UpDownNoteScale([F0, A0, C1], 12-EDO)

    Since in theory every shared partial scale has infinite equivalents
    on the periodic extension the scales are normalized to the first
    occurence in the first scale

    :param scale_a: The first scale
    :param scale_b: The second scale
    :param cutout_pattern: A mask expression used to iteratively
        cut out partial scales from the two scales.
    """

    if not scale_a.is_period_normalized or not scale_b.is_period_normalized:
        raise ValueError(
            'mod_connectors is only defined on period normalized scales'
        )

    connectors = []

    for partial_a in cutouts(scale_a, cutout_pattern):
        for partial_b in cutouts(scale_b, cutout_pattern):
            if partial_a.is_seq_equivalent(partial_b):
                connectors.append(partial_a)

    return connectors
