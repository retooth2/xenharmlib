import pytest
from xenharmlib.core.symbols import SymbolSumArithmetic
from xenharmlib.core.symbols import SymbolSumArithmeticSet
from xenharmlib.core.symbols import UnknownSymbolString
from xenharmlib.core.symbols import SymbolValueNotMapped

@pytest.mark.parametrize(
    'symbol_str, literals, values, offset',
    [
        ('U&&&', ['U', '&', '&', '&'], [0, 1, 1, 1], 3),
        ('M&%', ['M', '&', '%'], [0, 1, -1], 0),
        ('L%&%', ['L', '%', '&', '%'], [0, -1, 1, -1], -3)
    ]
)

def test_parse_symbol_str(symbol_str, literals, values, offset):

    upper = SymbolSumArithmetic(
        offset=3
    )
    upper.add_symbol('U', 0, min_occurence=1)
    upper.add_symbol('&', 1)
    upper.add_symbol('%', -1, max_occurence=2)

    lower = SymbolSumArithmetic(
        offset=-3
    )
    lower.add_symbol('L', 0, min_occurence=1)
    lower.add_symbol('&', 1, max_occurence=2)
    lower.add_symbol('%', -1)

    mid = SymbolSumArithmetic()
    mid.add_symbol('M', 0, min_occurence=1)
    mid.add_symbol('&', 1)
    mid.add_symbol('%', -1)

    arith_set = SymbolSumArithmeticSet([mid])
    arith_set.add_arithmetic(upper)
    arith_set.add_arithmetic(lower)

    assert arith_set.parse_symbol_str(symbol_str) == (literals, values, offset)


@pytest.mark.parametrize(
    'unknown_symbol_str',
    [
        'U\%\%\%',
        'UL',
        'UM&&'
    ]
)
def test_parse_symbol_str_unknown(unknown_symbol_str):

    upper = SymbolSumArithmetic(
        offset=3
    )
    upper.add_symbol('U', 0, min_occurence=1)
    upper.add_symbol('&', 1)
    upper.add_symbol('%', -1, max_occurence=2)

    lower = SymbolSumArithmetic(
        offset=-3
    )
    lower.add_symbol('L', 0, min_occurence=1)
    lower.add_symbol('&', 1, max_occurence=2)
    lower.add_symbol('%', -1)

    mid = SymbolSumArithmetic()
    mid.add_symbol('M', 0, min_occurence=1)
    mid.add_symbol('&', 1)
    mid.add_symbol('%', -1)

    arith_set = SymbolSumArithmeticSet([mid])
    arith_set.add_arithmetic(upper)
    arith_set.add_arithmetic(lower)

    with pytest.raises(UnknownSymbolString):
        arith_set.parse_symbol_str(unknown_symbol_str)


@pytest.mark.parametrize(
    'symbol_str, value',
    [
        ('U&&&', 6),
        ('M&%', 0),
        ('L%&%', -4)
    ]
)

def test_get_value(symbol_str, value):

    upper = SymbolSumArithmetic(
        offset=3
    )
    upper.add_symbol('U', 0, min_occurence=1)
    upper.add_symbol('&', 1)
    upper.add_symbol('%', -1, max_occurence=2)

    lower = SymbolSumArithmetic(
        offset=-3
    )
    lower.add_symbol('L', 0, min_occurence=1)
    lower.add_symbol('&', 1, max_occurence=2)
    lower.add_symbol('%', -1)

    mid = SymbolSumArithmetic()
    mid.add_symbol('M', 0, min_occurence=1)
    mid.add_symbol('&', 1)
    mid.add_symbol('%', -1)

    arith_set = SymbolSumArithmeticSet([mid])
    arith_set.add_arithmetic(upper)
    arith_set.add_arithmetic(lower)

    assert arith_set.get_value(symbol_str) == value


@pytest.mark.parametrize(
    'unknown_symbol_str',
    [
        'U\%\%\%',
        'UL',
        'UM&&'
    ]
)
def test_get_value_unknown(unknown_symbol_str):

    upper = SymbolSumArithmetic(
        offset=3
    )
    upper.add_symbol('U', 0, min_occurence=1)
    upper.add_symbol('&', 1)
    upper.add_symbol('%', -1, max_occurence=2)

    lower = SymbolSumArithmetic(
        offset=-3
    )
    lower.add_symbol('L', 0, min_occurence=1)
    lower.add_symbol('&', 1, max_occurence=2)
    lower.add_symbol('%', -1)

    mid = SymbolSumArithmetic()
    mid.add_symbol('M', 0, min_occurence=1)
    mid.add_symbol('&', 1)
    mid.add_symbol('%', -1)

    arith_set = SymbolSumArithmeticSet([mid])
    arith_set.add_arithmetic(upper)
    arith_set.add_arithmetic(lower)

    with pytest.raises(UnknownSymbolString):
        arith_set.get_value(unknown_symbol_str)


@pytest.mark.parametrize(
    'symbol_str, value',
    [
        ('&&&U', 6),
        ('M', 0),
        ('%L', -4)
    ]
)

def test_get_symbol_str(symbol_str, value):

    upper = SymbolSumArithmetic(
        offset=3
    )
    upper.add_symbol('U', 0, min_occurence=1)
    upper.add_symbol('&', 1)
    upper.add_symbol('%', -1, max_occurence=2)

    lower = SymbolSumArithmetic(
        offset=-3
    )
    lower.add_symbol('L', 0, min_occurence=1)
    lower.add_symbol('&', 1, max_occurence=2)
    lower.add_symbol('%', -1)

    mid = SymbolSumArithmetic()
    mid.add_symbol('M', 0, min_occurence=1)
    mid.add_symbol('&', 1)
    mid.add_symbol('%', -1)

    arith_set = SymbolSumArithmeticSet([mid])
    arith_set.add_arithmetic(upper)
    arith_set.add_arithmetic(lower)

    assert arith_set.get_symbol_str(value) == symbol_str


@pytest.mark.parametrize(
    'unmapped_value',
    [-4, 9, 18, 23]
)

def test_get_symbol_str_not_mapped(unmapped_value):

    upper = SymbolSumArithmetic(
        offset=3
    )
    upper.add_symbol('U', 0, min_occurence=1)
    upper.add_symbol('&', 1, max_occurence=1)
    upper.add_symbol('%', -1, max_occurence=2)

    mid = SymbolSumArithmetic()
    mid.add_symbol('M', 0, min_occurence=1)
    mid.add_symbol('&', 5)
    mid.add_symbol('%', -5, max_occurence=5)

    arith_set = SymbolSumArithmeticSet([mid])
    arith_set.add_arithmetic(upper)

    with pytest.raises(SymbolValueNotMapped):
        assert arith_set.get_symbol_str(unmapped_value)
    

    