import pytest
from xenharmlib.core.symbols import SymbolArithmetic
from xenharmlib.core.symbols import SymbolArithmeticSet
from xenharmlib.core.symbols import UnknownSymbolString
from xenharmlib.core.symbols import SymbolValueNotMapped
from xenharmlib.core.symbols import UnfittingDimensions


def test_add_arithmetic_unfitting_dimensions():

    arith = SymbolArithmetic(
        offset=(3,)
    )
    arith.add_symbol('U', (0,))

    arith_set = SymbolArithmeticSet(dimensions=2)

    with pytest.raises(UnfittingDimensions):
        arith_set.add_arithmetic(arith)


@pytest.mark.parametrize(
    'symbol_str, literals',
    [
        ('U&&&', ('U', '&', '&', '&')),
        ('M&%', ('M', '&', '%')),
        ('L%&%', ('L', '%', '&', '%')),
    ]
)
def test_parse(symbol_str, literals):

    upper = SymbolArithmetic(
        offset=(3,)
    )
    upper.add_symbol('U', (0,), min_occurence=1)
    upper.add_symbol('&', (1,))
    upper.add_symbol('%', (-1,), max_occurence=2)

    lower = SymbolArithmetic(
        offset=(-3,)
    )
    lower.add_symbol('L', (0,), min_occurence=1)
    lower.add_symbol('&', (1,), max_occurence=2)
    lower.add_symbol('%', (-1,))

    mid = SymbolArithmetic()
    mid.add_symbol('M', (0,), min_occurence=1)
    mid.add_symbol('&', (1,))
    mid.add_symbol('%', (-1,))

    arith_set = SymbolArithmeticSet()
    arith_set.add_arithmetic(mid)
    arith_set.add_arithmetic(upper)
    arith_set.add_arithmetic(lower)

    # TODO: also check matching arithmetic
    _, parsed_literals = arith_set.parse(symbol_str)

    assert parsed_literals == literals


@pytest.mark.parametrize(
    'unknown_symbol_str',
    [
        'U\%\%\%',
        'UL',
        'UM&&'
    ]
)
def test_parse_unknown_symbol_string(unknown_symbol_str):

    upper = SymbolArithmetic(
        offset=(3,)
    )
    upper.add_symbol('U', (0,), min_occurence=1)
    upper.add_symbol('&', (1,))
    upper.add_symbol('%', (-1,), max_occurence=2)

    lower = SymbolArithmetic(
        offset=(-3,)
    )
    lower.add_symbol('L', (0,), min_occurence=1)
    lower.add_symbol('&', (1,), max_occurence=2)
    lower.add_symbol('%', (-1,))

    mid = SymbolArithmetic()
    mid.add_symbol('M', (0,), min_occurence=1)
    mid.add_symbol('&', (1,))
    mid.add_symbol('%', (-1,))

    arith_set = SymbolArithmeticSet()
    arith_set.add_arithmetic(mid)
    arith_set.add_arithmetic(upper)
    arith_set.add_arithmetic(lower)

    with pytest.raises(UnknownSymbolString):
        arith_set.parse(unknown_symbol_str)


@pytest.mark.parametrize(
    'symbol_str, vector',
    [
        ('U&&&', (6,)),
        ('M&%', (0,)),
        ('L%&%', (-4,))
    ]
)
def test_get_vector(symbol_str, vector):

    upper = SymbolArithmetic(
        offset=(3,)
    )
    upper.add_symbol('U', (0,), min_occurence=1)
    upper.add_symbol('&', (1,))
    upper.add_symbol('%', (-1,), max_occurence=2)

    lower = SymbolArithmetic(
        offset=(-3,)
    )
    lower.add_symbol('L', (0,), min_occurence=1)
    lower.add_symbol('&', (1,), max_occurence=2)
    lower.add_symbol('%', (-1,))

    mid = SymbolArithmetic()
    mid.add_symbol('M', (0,), min_occurence=1)
    mid.add_symbol('&', (1,))
    mid.add_symbol('%', (-1,))

    arith_set = SymbolArithmeticSet()
    arith_set.add_arithmetic(mid)
    arith_set.add_arithmetic(upper)
    arith_set.add_arithmetic(lower)

    assert arith_set.get_vector(symbol_str) == vector


@pytest.mark.parametrize(
    'unknown_symbol_str',
    [
        'U\%\%\%',
        'UL',
        'UM&&'
    ]
)
def test_get_vector_unknown(unknown_symbol_str):

    upper = SymbolArithmetic(
        offset=(3,)
    )
    upper.add_symbol('U', (0,), min_occurence=1)
    upper.add_symbol('&', (1,))
    upper.add_symbol('%', (-1,), max_occurence=2)

    lower = SymbolArithmetic(
        offset=(-3,)
    )
    lower.add_symbol('L', (0,), min_occurence=1)
    lower.add_symbol('&', (1,), max_occurence=2)
    lower.add_symbol('%', (-1,))

    mid = SymbolArithmetic()
    mid.add_symbol('M', (0,), min_occurence=1)
    mid.add_symbol('&', (1,))
    mid.add_symbol('%', (-1,))

    arith_set = SymbolArithmeticSet()
    arith_set.add_arithmetic(mid)
    arith_set.add_arithmetic(upper)
    arith_set.add_arithmetic(lower)

    with pytest.raises(UnknownSymbolString):
        arith_set.get_vector(unknown_symbol_str)


@pytest.mark.parametrize(
    'symbol_str, value',
    [
        ('U&&&', (6,)),
        ('M', (0,)),
        ('L%', (-4,))
    ]
)
def test_get_symbol_str(symbol_str, value):

    upper = SymbolArithmetic(
        offset=(3,)
    )
    upper.add_symbol('U', (0,), min_occurence=1)
    upper.add_symbol('&', (1,))
    upper.add_symbol('%', (-1,), max_occurence=2)

    lower = SymbolArithmetic(
        offset=(-3,)
    )
    lower.add_symbol('L', (0,), min_occurence=1)
    lower.add_symbol('&', (1,), max_occurence=2)
    lower.add_symbol('%', (-1,))

    mid = SymbolArithmetic()
    mid.add_symbol('M', (0,), min_occurence=1)
    mid.add_symbol('&', (1,))
    mid.add_symbol('%', (-1,))

    arith_set = SymbolArithmeticSet()
    arith_set.add_arithmetic(mid)
    arith_set.add_arithmetic(upper)
    arith_set.add_arithmetic(lower)

    assert arith_set.get_symbol_str(value) == symbol_str


@pytest.mark.parametrize(
    'unmapped_value',
    [(-4,), (9,), (18,), (23,)]
)
def test_get_symbol_str_not_mapped(unmapped_value):

    upper = SymbolArithmetic(
        offset=(3,)
    )
    upper.add_symbol('U', (0,), min_occurence=1)
    upper.add_symbol('&', (1,), max_occurence=1)
    upper.add_symbol('%', (-1,), max_occurence=2)

    mid = SymbolArithmetic()
    mid.add_symbol('M', (0,), min_occurence=1)
    mid.add_symbol('&', (5,))
    mid.add_symbol('%', (-5,), max_occurence=5)

    arith_set = SymbolArithmeticSet()
    arith_set.add_arithmetic(mid)
    arith_set.add_arithmetic(upper)

    with pytest.raises(SymbolValueNotMapped):
        assert arith_set.get_symbol_str(unmapped_value)
