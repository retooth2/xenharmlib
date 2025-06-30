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
This module implements iterators for the periodic package
"""
from __future__ import annotations
from typing import Tuple
from typing import Generator
from typing import TypeVar
from ..core.scale import PeriodicScale
from ..core.freq_repr import FreqRepr
from ..core.masks import InfiniteIndexMask
from .utils import scale_element


FreqReprT = TypeVar('FreqReprT', bound=FreqRepr)
ScaleT = TypeVar('ScaleT', bound=PeriodicScale)


def cutouts(
    scale: ScaleT,
    mask_expr: int | Tuple[int, ...]
) -> Generator[ScaleT]:
    """
    Returns a generator yielding partial scales obtained by
    sliding a mask over the periodical extension of the scale
    until periodic equivalence is detected.

    The function can be used to generate all triads or seven
    chord scales from a key scale. For example:

    >>> from xenharmlib import EDOTuning
    >>> from xenharmlib import UpDownNotation
    >>> from xenharmlib import periodic
    >>>
    >>> edo12 = EDOTuning(12)
    >>> n_edo12 = UpDownNotation(edo12)
    >>> c_maj = n_edo12.pc_scale(['C', 'D', 'E', 'F', 'G', 'A', 'B'])
    >>>
    >>> for chord_scale in periodic.cutouts(c_maj, (0, 2, 4)):
    ...    print(chord_scale)
    UpDownNoteScale([C0, E0, G0], 12-EDO)
    UpDownNoteScale([D0, F0, A0], 12-EDO)
    UpDownNoteScale([E0, G0, B0], 12-EDO)
    UpDownNoteScale([F0, A0, C1], 12-EDO)
    UpDownNoteScale([G0, B0, D1], 12-EDO)
    UpDownNoteScale([A0, C1, E1], 12-EDO)
    UpDownNoteScale([B0, D1, F1], 12-EDO)

    :param scale: The scale from which the partials are taken
    :param mask_expr: An index mask expression defining the template
        that the generator slides over the scale.
    """

    if not scale.is_period_normalized:
        raise ValueError(
            'cutouts is only defined on period normalized scales'
        )

    mask = InfiniteIndexMask(mask_expr)

    for offset in range(0, len(scale)):
        elements = []
        for index in mask.with_offset(offset):
            elements.append(scale_element(scale, index))
        yield scale.origin_context.scale(elements)


def pairs(
    scale: PeriodicScale[FreqReprT],
    distance: int = 1
) -> Generator[Tuple[FreqReprT, FreqReprT]]:
    """
    Returns a generator yielding tuples of neighboring elements
    of the periodic extension of a scale (either direct neighbors
    or neighbors with a bigger fixed distance)

    :param scale: The origin scale
    :param distance: The distance of the two elements
        (optional, defaults to 1 meaning "direct neighbors")
    """

    if not scale.is_period_normalized:
        raise ValueError(
            'pairs is only defined on period normalized scales'
        )

    n = len(scale)
    for i in range(0, n):
        first = scale_element(scale, i)
        second = scale_element(scale, i + distance)
        yield first, second
