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
This module implements the logic behind index masks (used e.g.
in the partial method of scales)
"""

from __future__ import annotations
import math
from typing import Self
from typing import Iterable
from ..exc import InvalidIndexMask


def mask_select(mask_expr, iterable):
    """
    This generator will for a given index mask expression
    and an iterable yield every item of the iterable together
    with a boolean that indicates if the item is part of the
    selection defined by the mask.

    :param mask_expr: An index mask expression
    ;param iterable: Any iterable

    >>> iterable = range(0, 14, 2)
    >>> for is_selected, item in mask_select((1, 3, ...), iterable):
    >>>     print(is_selected, item)
    False 0
    True 2
    False 4
    True 6
    True 8
    True 10
    True 12
    """

    mask = IndexMask(mask_expr)
    for i, element in enumerate(iterable):
        yield i in mask, element


class IndexMask:
    """
    An IndexMask defines a selection of indices of an iterable.
    Index masks are generalizations of slices insofar as multiple
    index ranges can be selected at once. An index mask can be
    defined in various ways:

    As a list of consecutive indices:
    >>> IndexMask((1, 2, 5))
    IndexMask(1, 2, 5)

    An ellipsis between two indices adds all indices between
    them to the selection
    >>> IndexMask((1, ..., 5, 9))
    IndexMask(1, 2, 3, 4, 5, 9)

    If a mask begins with an ellipsis all indices from 0 to
    the next index are added to the selection
    >>> IndexMask((..., 5, 9))
    IndexMask(0, 1, 2, 3, 4, 5, 9)

    A mask without a last index is right-open and will select
    all indices from the last index to the end of the iterable
    it is applied to
    >>> IndexMask((7, ..., 9, ...))
    IndexMask(7, 8, 9, ...)

    Integers can be used as shortform for 1-tuples
    >>> IndexMask(4)

    The trivial complete mask
    >>> IndexMask(...)

    The trivial empty mask
    >>> IndexMask()

    Once defined the IndexMask object allows containment
    testing over the in-operator:

    >>> 4 in IndexMask((..., 5, 9))
    True
    >>> 6 in IndexMask((..., 5, 9))
    False
    >>> 972319 in IndexMask((4, ...))
    True
    """

    def __init__(self, expr=None):

        self.open_from = math.inf

        if not expr:
            self.indices = []
            self.index_set = set()
            return

        if not isinstance(expr, Iterable):
            expr = (expr,)

        # we inline-define two list operations which make sure that
        # every newly added element does honor the constraint of
        # strict monotony and positivity

        def _append_index(list_, e):
            if list_ and list_[-1] >= e:
                raise InvalidIndexMask('Indices in masks are not consecutive')
            if e < 0:
                raise InvalidIndexMask('Indices in masks must be positive')
            list_.append(e)

        def _extend_indices(list_a, list_b):
            for e in list_b:
                _append_index(list_a, e)

        # unwrap the mask into a list of consecutive indices

        indices = [0] if expr[0] is ... else []

        # by definition of zip and [1:] this for-loop gets only
        # executed when there are at least two elements in the
        # expression

        for e1, e2 in zip(expr, expr[1:]):
            if e1 is not ...:
                _append_index(indices, e1)
            if e1 is ... and e2 is not ...:
                last = indices[-1]
                _extend_indices(indices, range(last + 1, e2))

        # for-loop only considers elements up until to the last
        # (excluding) so we need to look at the last element
        # seperately. in case len(expr) = 1 the for-loop gets
        # omitted and the following code describes the treatment
        # of the only element in the expression

        last = expr[-1]
        if last is ...:
            self.open_from = indices[-1]
        else:
            _append_index(indices, last)

        # the purpose of index mask is to support fast lookup
        # operations, so we cast our list into a set.

        self.index_set = set(indices)
        self.indices = indices

    def with_offset(self, offset: int) -> Self:
        """
        Derives another index mask from this one with all
        integers moved according to the given offset

        :param offset: An integer offset
        """

        mask_expr = tuple()
        for index in self.indices:
            mask_expr = mask_expr + (index + offset,)
        return InfiniteIndexMask(mask_expr)

    def __iter__(self):
        return self.indices.__iter__()

    def __contains__(self, index):
        return index in self.index_set or index > self.open_from


class InfiniteIndexMask:
    """
    An InfiniteIndexMask defines a finite selection of indices on an
    infinite series. Index masks are generalizations of slices insofar
    as multiple index ranges can be selected at once. An index mask
    can be defined in various ways:

    As a list of consecutive indices:
    >>> InfiniteIndexMask((-3, 2, 5))
    InfiniteIndexMask(-3, 2, 5)

    An ellipsis between two indices adds all indices between
    them to the selection
    >>> InfiniteIndexMask((-2, ..., 5, 9))
    InfiniteIndexMask(-2, -1, 0, 1, 2, 3, 4, 5, 9)

    Integers can be used as shortform for 1-tuples
    >>> InfiniteIndexMask(4)

    The trivial empty mask
    >>> InfiniteIndexMask()

    In contrast to IndexMask which operates on a finite series
    infinite index masks cannot be right-open or left-open
    (having an ellipsis as first or last element), because
    this would not result in a finite set of indices.

    Once defined the IndexMask object allows containment
    testing over the in-operator:

    >>> -1 in InfiniteIndexMask((-2, ..., 5, 9))
    True
    >>> 6 in InfiniteIndexMask((1, ..., 5, 9))
    False
    """

    def __init__(self, expr=None):

        if not expr:
            self.indices = []
            self.index_set = set()
            return

        if not isinstance(expr, Iterable):
            expr = (expr,)

        if type(expr[0]) is not int:
            raise InvalidIndexMask(
                'Ellipsis is not allowed on edges of infinite series mask'
            )

        if type(expr[-1]) is not int:
            raise InvalidIndexMask(
                'Ellipsis is not allowed on edges of infinite series mask'
            )

        # we inline-define two list operations which make sure that
        # every newly added element does honor the constraint of
        # strict monotony and positivity

        def _append_index(list_, e):
            if list_ and list_[-1] >= e:
                raise InvalidIndexMask('Indices in masks are not consecutive')
            list_.append(e)

        def _extend_indices(list_a, list_b):
            for e in list_b:
                _append_index(list_a, e)

        # unwrap the mask into a list of consecutive indices

        indices = []

        # by definition of zip and [1:] this for-loop gets only
        # executed when there are at least two elements in the
        # expression

        for e1, e2 in zip(expr, expr[1:]):
            if e1 is not ...:
                _append_index(indices, e1)
            if e1 is ... and e2 is not ...:
                last = indices[-1]
                _extend_indices(indices, range(last + 1, e2))

        # for-loop only considers elements up until to the last
        # (excluding) so we need to look at the last element
        # seperately. in case len(expr) = 1 the for-loop gets
        # omitted and the following code describes the treatment
        # of the only element in the expression

        _append_index(indices, expr[-1])

        # the purpose of index mask is to support fast lookup
        # operations, so we cast our list into a set.

        self.index_set = set(indices)
        self.indices = indices

    def with_offset(self, offset: int) -> Self:
        """
        Derives another index mask from this one with all
        integers moved according to the given offset

        :param offset: An integer offset
        """

        mask_expr = tuple()
        for index in self.indices:
            mask_expr = mask_expr + (index + offset,)
        return InfiniteIndexMask(mask_expr)

    def __iter__(self):
        return self.indices.__iter__()

    def __contains__(self, index):
        return index in self.index_set
