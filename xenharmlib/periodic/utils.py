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
This module includes basic utils for the periodic package such as
extractions methods for scale elements and partial scales, scalar
transposition and element / partial scale lookup functions
"""
from ..core.freq_repr import FreqRepr
from ..core.scale import PeriodicScale
from ..exc import IncompatibleOriginContexts
from ..core.masks import InfiniteIndexMask
from typing import TypeVar
from typing import Tuple
from typing import overload
from types import EllipsisType

FreqReprT = TypeVar('FreqReprT', bound=FreqRepr)
ScaleT = TypeVar('ScaleT', bound=PeriodicScale)


def scale_element(
    scale: PeriodicScale[FreqReprT],
    index: int
) -> FreqReprT:
    """
    Gets an element at a given index from the periodic extension of a
    period normalized scale.

    >>> from xenharmlib import EDOTuning
    >>> from xenharmlib import UpDownNotation
    >>> from xenharmlib import periodic
    >>>
    >>> edo12 = EDOTuning(12)
    >>> n_edo12 = UpDownNotation(edo12)
    >>>
    >>> c_maj = n_edo12.pc_scale(['C', 'D', 'E', 'F', 'G', 'A', 'B'])
    >>> periodic.scale_element(c_maj, 8)
    UpDownNote(D, 1, 12-EDO)

    :param scale: A period normalized scale
    :param index: An index of the periodic extension of the scale

    :raises ValueError: If given scale is not period normalized
    """

    if not scale.is_period_normalized:
        raise ValueError(
            'scale_element is only defined on period normalized scales'
        )

    n = len(scale)
    scale_index = index % n
    element = scale[scale_index]

    bi_index = index // n
    if bi_index != 0:
        element = element.transpose_bi_index(bi_index)

    return element


def index(scale: PeriodicScale[FreqReprT], element: FreqReprT) -> int:
    """
    Returns the index where an element is found in the periodic
    extension of a period normalized scale

    >>> from xenharmlib import EDOTuning
    >>> from xenharmlib import UpDownNotation
    >>> from xenharmlib import periodic
    >>>
    >>> edo12 = EDOTuning(12)
    >>> n_edo12 = UpDownNotation(edo12)
    >>>
    >>> c_maj = n_edo12.pc_scale(['C', 'D', 'E', 'F', 'G', 'A', 'B'])
    >>> periodic.index(c_maj, n_edo12.note('D', 1))
    8

    :param scale: A period normalized scale
    :param element: The element to be found

    :raises ValueError: If given scale is not period normalized
    :raises ValueError: If element was not found in periodic extension
    """

    if not scale.is_period_normalized:
        raise ValueError(
            'index is only defined on period normalized scales'
        )

    if scale.origin_context is not element.origin_context:
        raise IncompatibleOriginContexts(
            'Element and scale must have same origin context'
        )

    for i, maybe_equivalent in enumerate(scale):
        if element.is_equivalent(maybe_equivalent):
            break
    else:
        raise ValueError(
            f'{element} was not found in periodic extension of the scale'
        )

    bi_index_diff = (element.bi_index - maybe_equivalent.bi_index)
    return i + (bi_index_diff * len(scale))


def is_in(scale: PeriodicScale[FreqReprT], element: FreqReprT) -> bool:
    """
    Returns bool if element exists in periodic extension of a period
    normalized scale

    >>> from xenharmlib import EDOTuning
    >>> from xenharmlib import UpDownNotation
    >>> from xenharmlib import periodic
    >>>
    >>> edo12 = EDOTuning(12)
    >>> n_edo12 = UpDownNotation(edo12)
    >>>
    >>> c_maj = n_edo12.pc_scale(['C', 'D', 'E', 'F', 'G', 'A', 'B'])
    >>> periodic.is_in(c_maj, n_edo12.note('D', 1))
    True

    :param scale: A period normalized scale
    :param element: The element to be found

    :raises ValueError: If given scale is not period normalized
    :raises IncompatibleOriginContexts: If element and scale have
        different origin contexts
    """

    if not scale.is_period_normalized:
        raise ValueError(
            'is_in is only defined on period normalized scales'
        )

    if scale.origin_context is not element.origin_context:
        raise IncompatibleOriginContexts(
            'Element and scale must have same origin context'
        )

    for i, maybe_equivalent in enumerate(scale):
        if element.is_equivalent(maybe_equivalent):
            return True
    return False


@overload
def scalar_transpose(
    ref_scale: ScaleT,
    transposable: FreqReprT,
    steps: int
) -> FreqReprT: ...


@overload
def scalar_transpose(
    ref_scale: ScaleT,
    transposable: ScaleT,
    steps: int
) -> ScaleT: ...


def scalar_transpose(
    ref_scale: ScaleT,
    transposable: ScaleT | FreqReprT,
    steps: int
) -> ScaleT | FreqReprT:
    """
    Scalar transposition moves a note, pitch or scale along the
    steps of a reference scale. This is in contrast to normal
    transposition which moves a note along the steps of the
    complete scale (e.g. the chromatic scale in 12-EDO):

    >>> from xenharmlib import EDOTuning
    >>> from xenharmlib import UpDownNotation
    >>> from xenharmlib import periodic
    >>>
    >>> edo12 = EDOTuning(12)
    >>> n_edo12 = UpDownNotation(edo12)
    >>>
    >>> c_maj = n_edo12.pc_scale(['C', 'D', 'E', 'F', 'G', 'A', 'B'])
    >>> periodic.scalar_transpose(c_maj, n_edo12.note('D', 1), 3)
    UpDownNote(G, 1, 12-EDO)

    When scalar transposition is applied to collections of notes or
    pitches interval content can change, for example if a C major
    triad is transposed 1 step in reference to the C major scale
    the result will be D minor(!):

    >>> triad = n_edo12.pc_scale(['C', 'E', 'G'])
    >>> periodic.scalar_transpose(c_maj, triad, 1)
    UpDownNoteScale([D0, F0, A0], 12-EDO)

    :param ref_scale: A period normalized reference scale
    :param transposable: The object to be transposed
    :param steps: The number of scale steps the object should be
        transposed

    :raises IncompatibleOriginContexts: If reference scale and tranposable
        are not from the same origin context
    :raises ValueError: If reference scale is not period normalized
    :raises ValueError: If transposable object was not found in periodic
        extension of the reference scale
    """

    if not ref_scale.is_period_normalized:
        raise ValueError(
            'ref_scale must be period normalized'
        )

    if ref_scale.origin_context is not transposable.origin_context:
        raise IncompatibleOriginContexts(
            'Reference scale and object to be transposed have a '
            'different origin context'
        )

    if isinstance(transposable, FreqRepr):
        i = index(ref_scale, transposable)
        return scale_element(ref_scale, i + steps)

    elements = []
    for element in transposable:
        elements.append(
            scalar_transpose(ref_scale, element, steps)
        )

    context = ref_scale.origin_context
    return context.scale(elements)


def partial(
    scale: ScaleT,
    mask_expr: int | Tuple[int | EllipsisType, ...]
) -> ScaleT:
    """
    Returns a new scale consisting of a selection of indices
    of the periodic extension of the given scale. The selection
    is defined by an index mask expression.

    An index mask can be defined as a tuple of consecutive
    indices, e.g. (1, 2, 5) gives a scale including the
    second, third and sixth element of the origin scale

    An ellipsis between two indices indicates that all
    indices between them should be selected as well, e.g.
    (1, ..., 5, 9) is equivalent to (1, 2, 3, 4, 5, 9).

    Indices in the mask expression can be greater or smaller
    than the available indices in the origin scale. In this
    case the elements are taken from the periodic extension,
    e.g.

    >>> from xenharmlib import EDOTuning
    >>> from xenharmlib import UpDownNotation
    >>> from xenharmlib import periodic
    >>>
    >>> edo12 = EDOTuning(12)
    >>> n_edo12 = UpDownNotation(edo12)
    >>>
    >>> c_maj = n_edo12.pc_scale(['C', 'D', 'E', 'F', 'G', 'A', 'B'])
    >>> periodic.partial(c_maj, (-1, 1, 3))
    UpDownNoteScale([B-1, D0, F0], 12-EDO)
    >>> periodic.partial(c_maj, (5, ..., 12))
    UpDownNoteScale([A0, B0, C1, D1, E1, F1, G1, A1], 12-EDO)

    If only one element should be selected a simple integer
    can be used

    :param scale: A period normalized scale
    :param mask_expr: An index mask expression which defines
        the selection of indices from the periodic extension
        of the origin scale.

    :raises ValueError: If given scale is not period normalized
    """

    if not scale.is_period_normalized:
        raise ValueError(
            'partial is only defined on period normalized scales'
        )

    mask = InfiniteIndexMask(mask_expr)
    elements = []

    for index in mask:
        element = scale_element(scale, index)
        elements.append(element)

    context = scale.origin_context
    return context.scale(elements)


def index_mask(parent: ScaleT, partial: ScaleT) -> Tuple[int, ...]:
    """
    Searches for a partial scale in a scale and returns the
    periodic index mask of where the partial scale can be
    found.

    >>> from xenharmlib import EDOTuning
    >>> from xenharmlib import UpDownNotation
    >>> from xenharmlib import periodic
    >>>
    >>> edo12 = EDOTuning(12)
    >>> n_edo12 = UpDownNotation(edo12)
    >>> c_maj = n_edo12.pc_scale(['C', 'D', 'E', 'F', 'G', 'A', 'B'])
    >>> Bdim = n_edo12.pc_scale(['B', 'D', 'F'])
    >>> periodic.index_mask(c_maj, Bdim)
    (6, 8, 10)

    :param parent: The parent scale to search in
    :param partial: The partial scale that should be found

    :raises IncompatibleOriginContexts: If parent scale and partial
        scale are not from the same origin context
    :raises ValueError: If parent scale is not period normalized
    :raises ValueError: If partial scale was not found in periodic
        extension of the reference scale
    """

    if not parent.is_period_normalized:
        raise ValueError(
            'index_mask is only defined on period normalized scales'
        )

    if parent.origin_context is not partial.origin_context:
        raise IncompatibleOriginContexts(
            'Parent scale and object to be transposed have a '
            'different origin context'
        )

    mask = tuple()

    for element in partial:
        i = index(parent, element)
        mask += (i,)

    return mask
