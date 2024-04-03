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
The symbol module implements primitives to parse languages
in which each literal and each word represents an integer value.
These languages are called 'symbol codes' and are used as utils
in notations. A typical symbol code for 12-EDO would be a mapping
of accidentals 'b' to -1, 'bb' to -2, '#' to 1, 'x' to 2, etc.
"""

from typing import *
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
    Gets raised whenever a symbol was added to a symbol
    code that already existed or if the associated value
    is already represented by another symbol
    """


class SymbolCode(ABC):
    """
    SymbolCode defines a general interface for different
    strategies to turn symbol strings into integer values
    and vice versa. A typical usecase for this is to map
    strings of accidentals (like 'bbb#') to values which
    signify step differences.

    The interface consists of two abstract methods
    * :meth:`SymbolCode.get_value`
    * :meth:`SymbolCode.get_symbol_str`
    """

    @abstractmethod
    def get_value(self, symbol_str: str) -> int:
        """
        Abstract method placeholder for a specific implementation
        to convert a string of one or more symbols into an integer
        value

        :param string: A string consisting of one or more symbols

        :raises UnknownSymbolString: If mapping has no ruleset
            to convert the string into an integer
        """

    @abstractmethod
    def get_symbol_str(self, value: int) -> str:
        """
        Abstract method placeholder for a specific implementation
        to convert an integer value into a symbol or sequence of
        symbols

        :param value: An integer value

        :raises SymbolValueNotMapped: If mapping has no ruleset
            to convert the integer into a string
        """


class SymbolSumArithmetic(SymbolCode):
    """
    A symbol sum arithmetic is a mapping between string symbol sequences
    and integer sums. It parses expressions like 'b##x' into a list
    of known symbols (like 'b', '#', '#', 'x') and translates it into
    an equivalent list of integers (like -1, 1, 1, 2) from which it
    creates a sum.

    Vice-versa for a given integer value it can create an equivalent
    minimal sequence of symbols (for example 3 -> 'x#').

    SymbolArithmetic parses in a greedy way, so if 'bb', 'b' and
    '#' are registered as symbols, it will parse 'bb#' into the
    list 'bb', '#' (NOT 'b', 'b', '#')

    Symbols and values build a bijective mapping, meaning that each
    value has exactly one symbol pointing to it. If you want to have
    ambigouity in this regard, you should use SymbolArithmeticSet.

    On initialization of an arithmetic an offset can be set, which
    adds a fixed value on all symbol values. This can come in handy
    when defining partial arithmetics in a SymbolArithmeticSet, e.g.
    if one wants to parse 'A' into '4', 'AA' into 5, 'AAA' into 6,
    etc. In a case like this one can define the value of 'A' to be
    1 and the offset to be 3.

    :param offset: (optional, default 0). A fixed value that will
        be added to the integer sum
    :param allow_empty: (optional, default False). If True, empty
        strings are part of this arithmetic (with value of the
        offset, or 0 if offset is not given). If False exceptions
        will be raised on empty strings 
    """

    def __init__(self,
                 offset: int = 0,
                 allow_empty: bool = False):

        self._symbol_values: Dict[str, int] = {}
        self._value_symbols: Dict[int, str] = {}
        self._symbol_min_occurence: Dict[str, int] = {}
        self._symbol_max_occurence: Dict[str, int] = {}
        self._offset = offset
        self._allow_empty = allow_empty

    def add_symbol(self,
                   symbol: str,
                   value: int,
                   min_occurence: Optional[int] = None,
                   max_occurence: Optional[int] = None):
        """
        Adds a string symbol with their corresponding
        value to this arithmetic.

        :raises AmbiguousSymbol: If symbol already exists in
            the arithmetic or if value is already represented
            by another symbol

        :param symbol: A string (can be multi-character)
        :param value: An integer that denotes the value
            of the string symbol in the arithmetic
        :param min_occurence: (optional) The minimum number of
            times this symbol must occur in the arithmetic
            symbol string in order for the string to be
            considered valid
        :param max_occurence: (optional) The maximum number of
            times this symbol can occur in the arithmetic
            symbol string in order for the string to be
            considered valid
        """

        if symbol in self._symbol_values:
            raise AmbiguousSymbol(
                f'Symbol {symbol} already exists in this '
                f'arithmetic'
            )

        if value in self._value_symbols:
            raise AmbiguousSymbol(
                f'Value {value} is already represented by '
                f'symbol {self._value_symbols[value]}'
            )

        self._symbol_values[symbol] = value
        self._value_symbols[value] = symbol

        if min_occurence is not None:
            self._symbol_min_occurence[symbol] = min_occurence

        if max_occurence is not None:
            self._symbol_max_occurence[symbol] = max_occurence

    def parse_symbol_str(self, symbol_str: str) -> Tuple[List[str], List[int], int]:
        """
        Parses a symbol string into a list of symbol literals
        their corresponding integer values and the offset

        >>> from xenharmlib.core.symbols import SymbolSumArithmetic
        >>> arithmetic = SymbolSumArithmetic()
        >>> arithmetic.add_symbol('x', 2)
        >>> arithmetic.add_symbol('#', 1)
        >>> arithmetic.add_symbol('b', -1)
        >>> literals, values, offset = arithmetic.parse_symbol_str('xbb#')

        :raises UnknownSymbolString: If arithmetic did not
            match the string
        
        :param symbol_str: A symbol string consisting of symbols
            defined in this arithmetic
        """

        symbols = []
        values = []

        if not self._allow_empty and symbol_str == '':
            raise UnknownSymbolString(
                'Symbol strings in this arithmetic must '
                'have at least one valued symbol'
            )

        while symbol_str != '':

            best_symbol = ''
            best_value = 0

            for value, symbol in self._value_symbols.items():

                if symbol_str.startswith(symbol):
                    if len(symbol) > len(best_symbol):
                        best_symbol = symbol
                        best_value = value

            if best_symbol == '':
                raise UnknownSymbolString(
                    f'Could not find a meaning for symbol '
                    f'string after {symbol_str}'
                )

            symbol_str = symbol_str[len(best_symbol):]
            symbols.append(best_symbol)
            values.append(best_value)

        for symbol in self._symbol_values.keys():

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

        return (symbols, values, self._offset)

    def get_value(self, symbol_str: str) -> int:
        """
        Returns the integer sum value for a given symbol string

        :raises UnknownSymbolString: If arithmetic did not
            match the string

        :param symbol_str: A string consisting of symbols
            defined in this arithmetic
        """

        _, values, offset = self.parse_symbol_str(symbol_str)
        return sum(values) + offset

    def get_symbol_str(self, value: int) -> str:
        """
        Returns a minimal symbol string for a given value

        :raises SymbolValueNotMapped: If value can not be
            represented by any combination of symbols
            in the arithmetic

        :param value: A positive or negative integer
        """

        # the problem of finding a minimal symbol sequence is
        # surprisingly complicated. i first researched variants
        # of the knapsack problem but did not find something
        # that takes negative capacities into account.

        # in the end i just used integer linear programming
        # stating the problem as:

        # minimimize sum(x)
        # subject to
        # v_1 * x_1 + ... + v_n * x_n = value + offset
        # x_i > min_i
        # x_i < max_i
        # v_i in Z, x_i in N

        symbol_count = len(self._symbol_values)
        adj_value = value - self._offset

        if symbol_count == 0:
            raise SymbolValueNotMapped(
                f'{value} could not be represented as a sum '
                f'of the values for which a symbol is registered '
            )

        c = np.array([1] * symbol_count)
        integrality = np.array([1] * symbol_count)

        sorted_values = sorted(self._value_symbols)
        A_array = [sorted_values]
        lb_list = [adj_value]
        ub_list = [adj_value]
        
        for i, c_value in enumerate(sorted_values):
            symbol = self._value_symbols[c_value]
            lb = self._symbol_min_occurence.get(symbol, 0)
            ub = self._symbol_max_occurence.get(symbol, np.inf)
            A_frag = [0] * i + [1] + [0] * (symbol_count - 1 - i)
            A_array.append(A_frag)
            lb_list.append(lb)
            ub_list.append(ub)

        if not self._allow_empty:
            A_array.append(
                [1] * symbol_count
            )
            lb_list.append(1)
            ub_list.append(np.inf)

        A = np.array(A_array)
        lb = np.array(lb_list)
        ub = np.array(ub_list)

        result = milp(
            c, 
            integrality=integrality, 
            constraints=LinearConstraint(A, lb, ub)
        )

        if not result.success:
            raise SymbolValueNotMapped(
                f'{value} could not be represented as a sum '
                f'of the values for which a symbol is registered '
            )

        counts = {}

        for i in range(symbol_count):
            count = int(result.x[i])
            symbol_value = sorted_values[i]
            counts[symbol_value] = count

        # put all the big symbols (both positive and
        # negative) before the small symbols

        abs_sorted = sorted(
            sorted_values,
            key=lambda x: abs(x),
            reverse=True
        )

        symbol_str = ''

        for symbol_value in abs_sorted:
            count = counts[symbol_value]
            symbol = self._value_symbols[symbol_value]
            symbol_str += symbol * count

        return symbol_str


class SymbolSumArithmeticSet(SymbolCode):
    """
    SymbolSumArithmeticSets combine different SymbolSumArithmetics
    allowing to use multiple symbols for the same value and 
    to segment the space of whole numbers into multiple
    arithmetics with different offsets.

    You can for example combine four arithmetics to represent
    traditional interval naming of imperfect intervals:

    * 'M'  represents value 0
    * 'M^' represents one step over 0
    * 'A'  represents one sharpness values over 0
    * 'm'  represents one sharpness values less than 0
    * 'd'  represents two sharpness values less than 0
    * 'dv' represents two sharpness values less than 0 and
           an additional step downwards.

    :param arithmetics: A list of symbol arithmetics that
        define the set
    """

    def __init__(self, arithmetics: List[SymbolSumArithmetic]):
        self._arithmetics = arithmetics

    def add_arithmetic(self, arithmetic: SymbolSumArithmetic):
        """
        Adds another symbol arithmetic to this set

        :param arithmetic: The arithmetic to add
        """

        self._arithmetics.append(arithmetic)

    def parse_symbol_str(self, symbol_str: str) -> Tuple[List[str], List[int], int]:
        """
        Parses a symbol string into a list of symbol literals,
        their corresponding integer values and the offset which
        should be applied to them.

        >>> literals, values, offset = arithmetic.parse_symbol_str('xbb#')

        Under the hood the method tries to parse the string with
        all available arithmetics in the set, ignoring the ones
        that raise UnknownSymbolString and selecting the one
        with the smallest number of symbols.

        :raises UnknownSymbolString: If no arithmetic in the set
            matched the string
        """

        matches = []

        for a in self._arithmetics:
            try:
                literals, values, offset = a.parse_symbol_str(symbol_str)
                matches.append(
                    (literals, values, offset)
                )
            except UnknownSymbolString:
                continue

        if not matches:
            raise UnknownSymbolString(
                'Symbol string did not match with any '
                'arithmetic in the set'
            )

        matches = sorted(
            matches,
            key=lambda x: len(x[1])
        )

        return matches[0]

    def get_value(self, symbol_str: str) -> int:
        """
        Returns the integer sum value for a given string

        :raises UnknownSymbolString: If no arithmetic in the set
            matched the string

        :param symbol_str: A symbol string consisting of symbols
            defined by at least one arithmetic in the set.
        """
        _, values, offset = self.parse_symbol_str(symbol_str)
        return sum(values) + offset

    def get_symbol_str(self, value: int) -> str:
        """
        Returns a minimal symbol string for a given value

        :raises SymbolValueNotMapped: If value can not be
            represented by any combination of symbols
            in any arithmetic

        :param value: A positive or negative integer
        """

        matches = []

        for a in self._arithmetics:
            try:
                symbol_str = a.get_symbol_str(value)
                matches.append(symbol_str)
            except SymbolValueNotMapped:
                continue

        if not matches:
            raise SymbolValueNotMapped(
                f'Symbol value {value} could not be represented '
                f'by any symbol arithmetic in the set'
            )

        matches = sorted(
            matches,
            key=lambda x: len(x)
        )

        return matches[0]