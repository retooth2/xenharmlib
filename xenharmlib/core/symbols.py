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
The symbol module implements primitives to parse languages in which each
literal and each word represents an integer vector. These languages are
called 'symbol codes' and are used as utils in notations.
"""

from typing import Tuple
from typing import List
from typing import Dict
from typing import Callable
from typing import Optional
from abc import ABC, abstractmethod

import numpy as np
from scipy.optimize import milp
from scipy.optimize import LinearConstraint


class UnknownSymbolString(Exception):
    """
    Gets raised whenever a SymbolCode receives a
    string that is not part of its grammar
    """


class SymbolValueNotMapped(Exception):
    """
    Gets raised whenever an integer value is not
    mapped by a word in a symbol code
    """


class AmbiguousSymbol(Exception):
    """
    Gets raised whenever a symbol is added to a symbol
    code that already exists or if the associated value
    is already represented by another symbol
    """


class UnfittingDimensions(Exception):
    """
    Gets raised whenever a vector does not fit to the dimension
    configuration of the symbol code
    """


class SymbolCode(ABC):
    """
    SymbolCode defines a general interface for different strategies
    to turn symbol strings into integer vectors and vice versa.

    The interface consists of two abstract methods
        * :meth:`SymbolCode.get_value`
        * :meth:`SymbolCode.get_symbol_str`
    """

    @abstractmethod
    def get_vector(self, symbol_str: str) -> Tuple[int, ...]:
        """
        Abstract method placeholder for a specific implementation
        to convert a string of one or more symbols into an integer
        vector

        :param string: A string consisting of one or more symbols

        :raises UnknownSymbolString: If mapping has no ruleset
            to convert the string into an integer vector
        """

    @abstractmethod
    def get_symbol_str(self, vector: Tuple[int, ...]) -> str:
        """
        Abstract method placeholder for a specific implementation
        to convert an integer vector into a symbol or sequence of
        symbols

        :param vector: An integer vector

        :raises SymbolValueNotMapped: If mapping has no ruleset
            to convert the vector into a string
        """


class SymbolArithmetic(SymbolCode):
    """
    A symbol arithmetic is a mapping between string symbol sequences
    and integer vector sums.

    A simple use case is to parse and generate accidentals, for example
    parsing the standard western accidental string 'x#b' into a list of
    one-dimensional integer vectors that signify the pitch index
    alterations of each accidental (like (2,), (1,), (-1,)), resulting
    in the sum (2,) denoting the total pitch index alteration of an
    accidental string.

    Higher dimensional arithmetics can be useful if there are multiple
    classes of accidentals (like sharp/flat on the one hand and up/down
    on the other). Given a value dimensionality of 2, it can e.g. parse
    an expression like '^b##x' into a list of integer vectors (here:
    (0, 1), (-1, 0), (1, 0), (1, 0), (2, 0)) from which it creates a
    sum vector (3, 1)

    Vice-versa for a given integer or integer vector it can create an
    equivalent minimal sequence of symbols (e.g. (-1, 1) -> 'b^').

    SymbolArithmetic parses in a greedy way, so if 'bb', 'b' and '#'
    are registered as symbols, it will parse 'bb#' into the list 'bb',
    '#' (NOT 'b', 'b', '#')

    The class can also be used to design accidental systems for dense
    tunings (like prime limit tunings), that don't have an enumerable
    pitch index sequence. For example, given a 3-limit tuning one can
    define accidentals as their monzo, defining '#' as the value
    vector (-11, 7), 'b' as the vector (11, -7), and so forth. The
    addition of the monzo vectors is then equal to the product in
    |R+: (e.g. 'b#' = (11, -7) + (-11, 7) = (0, 0), which is the
    same as (2^11)/(3^7) * (3^7)/(2^11) = (2^0) * (3^0) = 1.

    On initialization of an arithmetic, an offset can be set, which
    adds a fixed integer vector to all symbol value vectors. This
    is especially powerful when defining partial arithmetics in a
    SymbolArithmeticSet, e.g. if one wants to parse '^A' into (4, 1),
    'AA' into (5, 0), '^AAA' into (6, 1), etc. In a case like this
    one can define the value of 'A' to be (1, 0), the value of '^'
    to be (0, 1) and the offset to be (3, 0).

    :param dimensions: Dimensions of the value vector (optional,
        defaults to 1)
    :param offset: (optional, defaults to the 0-vector). A fixed
        value vector that will be added to the sum
    :param allow_empty: (optional, default False). If True, empty
        strings are part of this arithmetic (with the value of the
        offset, or the 0 vector if offset is not given). If False
        exceptions will be raised on empty strings
    """

    def __init__(
        self,
        dimensions: int = 1,
        offset: Optional[Tuple[int, ...]] = None,
        allow_empty: bool = False,
    ):

        if offset is None:
            _offset = (0,) * dimensions
        else:
            _offset = offset

        if len(_offset) != dimensions:
            raise UnfittingDimensions(
                'Offset dimensions must match the value '
                'given in dimensions argument'
            )

        self._dimensions = dimensions

        self._symbol_vectors: Dict[str, Tuple[int, ...]] = {}
        self._vector_symbols: Dict[Tuple[int, ...], str] = {}
        self._symbol_position: Dict[str, int] = {}
        self._symbol_min_occurence: Dict[str, int] = {}
        self._symbol_max_occurence: Dict[str, int] = {}
        self._offset = _offset
        self._allow_empty = allow_empty

    @property
    def dimensions(self) -> int:
        return self._dimensions

    @property
    def offset(self) -> Tuple[int, ...]:
        return self._offset

    def add_symbol(
        self,
        symbol: str,
        vector: Tuple[int, ...],
        position: Optional[int] = None,
        min_occurence: Optional[int] = None,
        max_occurence: Optional[int] = None,
    ):
        """
        Adds a string symbol with its corresponding integer
        vector to this arithmetic

        :raises AmbiguousSymbol: If symbol already exists in
            the arithmetic or if vector is already represented
            by another symbol

        :param symbol: A string (can be multi-character)
        :param vector: An integer tuple defining the
            value vector of the symbol (dimensions must
            match the dimensions with which the arithmetic
            was initialized)
        :param position: The desired positional value of the
            symbol in the sorting process of get_symbol_str
            (optional, if no parameter is given the position
            of the symbol will be analogous to the order
            in which symbols were added to the arithmetic)
        :param min_occurence: (optional) The minimum number of
            times this symbol must occur in the arithmetic
            symbol string in order for the string to be
            considered valid
        :param max_occurence: (optional) The maximum number of
            times this symbol can occur in the arithmetic
            symbol string in order for the string to be
            considered valid
        """

        if len(vector) != self.dimensions:
            raise UnfittingDimensions(
                f'Value dimensions did not match the dimensions '
                f'of this arithmetic ({self.dimensions})'
            )

        if position is None:
            # if no position was given simply take the biggest
            # already existing position and increment by one:
            biggest_pos = 0
            for position in self._symbol_position.values():
                biggest_pos = max(position, biggest_pos)
            position = biggest_pos + 1

        if symbol in self._symbol_vectors:
            raise AmbiguousSymbol(
                f'Symbol {symbol} already exists in this arithmetic'
            )

        if vector in self._vector_symbols:
            raise AmbiguousSymbol(
                f'Vector {vector} is already represented by '
                f'symbol {self._vector_symbols[vector]}'
            )

        self._symbol_vectors[symbol] = vector
        self._vector_symbols[vector] = symbol
        self._symbol_position[symbol] = position

        if min_occurence is not None:
            self._symbol_min_occurence[symbol] = min_occurence

        if max_occurence is not None:
            self._symbol_max_occurence[symbol] = max_occurence

    def get_vector(self, symbol_str: str) -> Tuple[int, ...]:
        """
        Returns the vector integer sum (adjusted for offset,
        if set) for a given symbol string.

        :raises UnknownSymbolString: If arithmetic did not
            match the string

        :param symbol_str: A string consisting of symbols
            defined in this arithmetic
        """

        symbols = self.parse(symbol_str)
        return self.get_vector_from_symbols(symbols)

    def get_vector_from_symbols(
        self, symbols: Tuple[str, ...]
    ) -> Tuple[int, ...]:
        """
        Returns the vector integer sum (adjusted for offset,
        if set) for a given tuple of parsed symbol literals

        :param symbols: A tuple with each element being a
            symbol literal in this arithmetic
        """

        result = np.array(self._offset)

        for symbol in symbols:
            value = self._symbol_vectors[symbol]
            result = np.add(result, value)

        return tuple(result)

    def parse(self, symbol_str: str) -> Tuple[str, ...]:
        """
        Parses a symbol string into a list of symbols

        >>> from xenharmlib.core.symbols import SymbolArithmetic
        >>> arithmetic = SymbolArithmetic(dimensions=2)
        >>> arithmetic.add_symbol('x', (2, 0))
        >>> arithmetic.add_symbol('#', (1, 0))
        >>> arithmetic.add_symbol('b', (-1, 0))
        >>> arithmetic.add_symbol('^', (0, 1))
        >>> symbols = arithmetic.parse('xbb#')
        >>> symbols
        ('x', 'b', 'b', '#')

        :raises UnknownSymbolString: If arithmetic did not
            match the string

        :param symbol_str: A symbol string consisting of symbols
            defined in this arithmetic
        """

        symbols = []
        def_symbols = list(self._symbol_vectors)

        if not self._allow_empty and symbol_str == '':
            raise UnknownSymbolString(
                'Symbol strings in this arithmetic must '
                'have at least one symbol'
            )

        while symbol_str != '':

            best_symbol = ''

            for symbol in def_symbols:
                if symbol_str.startswith(symbol):
                    if len(symbol) > len(best_symbol):
                        best_symbol = symbol

            if best_symbol == '':
                raise UnknownSymbolString(
                    f'Could not find a meaning for symbol '
                    f'string after {symbol_str}'
                )

            symbol_str = symbol_str[len(best_symbol):]
            symbols.append(best_symbol)

        for symbol in def_symbols:

            count = symbols.count(symbol)

            min_occ = self._symbol_min_occurence.get(symbol)
            if min_occ is not None and count < min_occ:
                raise UnknownSymbolString(
                    f'Symbol {symbol} must occur at least '
                    f'{min_occ} times, however only {count} '
                    f'occurences were counted'
                )

            max_occ = self._symbol_max_occurence.get(symbol)
            if max_occ is not None and count > max_occ:
                raise UnknownSymbolString(
                    f'Symbol {symbol} can occur at most '
                    f'{max_occ} times, however {count} '
                    f'occurences were counted'
                )

        return tuple(symbols)

    def get_symbol_str(self, vector: Tuple[int, ...]) -> str:
        """
        Partitions the given vector into vector summands that are
        represented by symbols and returns those symbols sorted
        according to the positional value of each symbol and
        joined as a single string.

        :param vector: The sum vector that should be resolved
            into a symbol term
        """

        if len(vector) != self.dimensions:
            raise UnfittingDimensions(
                f'Vector dimensions did not match the dimensions '
                f'of this arithmetic ({self.dimensions})'
            )

        return ''.join(self.get_symbols(vector))

    def get_symbols(self, vector: Tuple[int, ...]) -> Tuple[str, ...]:
        """
        Returns a sorted, minimal tuple of symbols whose combined
        value together with the offset result in the given sum.

        :raises SymbolValueNotMapped: If the value can not be
            represented by any combination of symbols
            in the arithmetic

        :param vector: The sum vector that should be resolved
            into a symbol term
        """

        if len(vector) != self.dimensions:
            raise UnfittingDimensions(
                f'Value vector must have exactly'
                f'{self.dimensions} dimensions'
            )

        symbol_count = len(self._symbol_vectors)
        adj_vector = list(np.subtract(vector, self.offset))

        if symbol_count == 0:
            raise SymbolValueNotMapped(
                f'{vector} could not be represented as a sum '
                f'of the vectors for which a symbol is registered '
            )

        # minimimize sum(x)
        # subject to

        # v_1,1 * x_1 + ... + v_n,1 * x_n = value_1 + offset_1
        # v_1,2 * x_1 + ... + v_n,2 * x_n = value_2 + offset_2
        # ...
        # v_1,n * x_1 + ... + v_n,n * x_n = value_n + offset_n

        # x_i > min_i
        # x_i < max_i
        # v_i in Z, x_i in N

        c = np.array([1] * symbol_count)
        integrality = np.array([1] * symbol_count)

        A_array = []
        sorted_symbols = sorted(self._symbol_vectors)

        for i in range(0, self.dimensions):
            row = []
            for symbol in sorted_symbols:
                value = self._symbol_vectors[symbol]
                row.append(value[i])
            A_array.append(row)

        lb_list = adj_vector[:]
        ub_list = adj_vector[:]

        for i, c_symbol in enumerate(sorted_symbols):
            lb = self._symbol_min_occurence.get(c_symbol, 0)
            ub = self._symbol_max_occurence.get(c_symbol, np.inf)
            A_frag = [0] * i + [1] + [0] * (symbol_count - 1 - i)
            A_array.append(A_frag)
            lb_list.append(lb)
            ub_list.append(ub)

        if not self._allow_empty:
            A_array.append([1] * symbol_count)
            lb_list.append(1)
            ub_list.append(np.inf)

        A = np.array(A_array)
        lb_array = np.array(lb_list)
        ub_array = np.array(ub_list)

        result = milp(
            c,
            integrality=integrality,
            constraints=LinearConstraint(A, lb_array, ub_array),
        )

        if not result.success:
            raise SymbolValueNotMapped(
                f'{vector} could not be represented as a sum '
                f'of the vectors for which a symbol is registered '
            )

        counts = {}

        for i in range(symbol_count):
            count = int(result.x[i])
            symbol = sorted_symbols[i]
            counts[symbol] = count

        # sort symbols in regards to their
        # positional value

        position_sorted = sorted(
            self._symbol_vectors,
            key=lambda x: self._symbol_position[x],
        )

        symbols = []

        for symbol in position_sorted:
            count = counts[symbol]
            symbols += [symbol] * count

        return tuple(symbols)


class SymbolArithmeticSet(SymbolCode):
    """
    SymbolArithmeticSets combine different SymbolArithmetics
    allowing to use multiple symbols for the same integer vector
    and to segment the space of integer vectors into multiple
    arithmetics with different offsets.

    You can for example combine four arithmetics to represent
    traditional interval naming of imperfect intervals:

    * 'M'  represents vector (0, 0)
    * '^M' represents vector (0, 1)
    * 'A'  represents vector (2, 0)
    * 'm'  represents vector (-1, 0)
    * 'd'  represents vector (-2, 0)
    * 'vd' represents vector (-2, -1)

    :param dimensions: The dimensions of the arithmetics
        in the set (optional, defaults to 1)
    :param pref_func: (optional) A preference function that
        returns a definite parsing result from a list of
        possible ones. The function should accept a list
        of tuples (arithmetic, parsed_str) with parsed_str
        being a tuple of single symbols. It should return
        one element of the list that should be preferred.
        If no preference function is given, then the class
        will choose the result with the shortest length.
    """

    def __init__(
        self,
        dimensions: int = 1,
        pref_func: (
            Callable[
                [List[Tuple[SymbolArithmetic, Tuple[str, ...]]]],
                Tuple[SymbolArithmetic, Tuple[str, ...]],
            ]
            | None
        ) = None,
    ):
        self._dimensions = dimensions
        self._arithmetics: List[SymbolArithmetic] = []

        if pref_func is None:
            pref_func = self._default_pref_func

        self._pref_func = pref_func

    @property
    def dimensions(self) -> int:
        """
        The vector dimensions of arithmetics in this set
        """
        return self._dimensions

    def add_arithmetic(self, arithmetic: SymbolArithmetic):
        """
        Adds another symbol arithmetic to this set

        :param arithmetic: The arithmetic to add
        """

        if arithmetic.dimensions != self.dimensions:
            raise UnfittingDimensions(
                'The vector dimension number of the arithmetic'
                'is different to the one of the set.'
            )

        self._arithmetics.append(arithmetic)

    @staticmethod
    def _default_pref_func(
        results: List[Tuple[SymbolArithmetic, Tuple[str, ...]]]
    ) -> Tuple[SymbolArithmetic, Tuple[str, ...]]:
        """
        The default preference function. Simply chooses the
        parsing result with the minimum number of symbols
        """

        best = results[0]

        for result in results[1:]:
            _, parsed_str = result
            _, best_parsed_str = best
            if len(parsed_str) < len(best_parsed_str):
                best = result

        return best

    def parse(
        self, symbol_str: str
    ) -> Tuple[SymbolArithmetic, Tuple[str, ...]]:
        """
        Tries to parse a symbol string by each arithmetic in the
        set. If an arithmetic returns a result it is added to the
        list of possible results from which then subsequently one
        result is selected using the preference function given
        during set initialization.

        The function returns a tuple (arithmetic, symbols) with
        the first element being the chosen arithmetic and the
        second being the parsing result from that arithmetic.

        :raises UnknownSymbolString: If no arithmetic in the set
            matched the string
        """

        matches = []

        for a in self._arithmetics:
            try:
                symbols = a.parse(symbol_str)
                matches.append((a, symbols))
            except UnknownSymbolString:
                continue

        if not matches:
            raise UnknownSymbolString(
                'Symbol string did not match with any arithmetic in the set'
            )

        return self._pref_func(matches)

    def get_vector(self, symbol_str: str) -> Tuple[int, ...]:
        """
        Returns the vector sum value for a given string

        :raises UnknownSymbolString: If no arithmetic in the set
            matched the string

        :param symbol_str: A symbol string consisting of symbols
            defined by at least one arithmetic in the set.
        """
        arithmetic, symbols = self.parse(symbol_str)
        return arithmetic.get_vector_from_symbols(symbols)

    def get_symbol_str(self, vector: Tuple[int, ...]) -> str:
        """
        Returns a minimal symbol string for a given value

        :raises SymbolValueNotMapped: If the value can not be
            represented by any combination of symbols
            in any arithmetic

        :param value: A positive or negative integer
        """

        matches = []

        for a in self._arithmetics:
            try:
                symbols = a.get_symbols(vector)
                matches.append((a, symbols))
            except SymbolValueNotMapped:
                continue

        if not matches:
            raise SymbolValueNotMapped(
                f'Vector {vector} could not be represented '
                f'by any symbol arithmetic in the set'
            )

        _, symbols = self._pref_func(matches)

        return ''.join(symbols)
