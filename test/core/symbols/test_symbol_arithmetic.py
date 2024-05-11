import pytest
from xenharmlib.core.symbols import SymbolArithmetic
from xenharmlib.core.symbols import UnknownSymbolString
from xenharmlib.core.symbols import AmbiguousSymbol
from xenharmlib.core.symbols import SymbolValueNotMapped
from xenharmlib.core.symbols import UnfittingDimensions


def test_init_unfitting_dimensions():

    with pytest.raises(UnfittingDimensions):
        SymbolArithmetic(
            dimensions=2,
            offset=(2,)
        )

    with pytest.raises(UnfittingDimensions):
        SymbolArithmetic(
            dimensions=2,
            offset=(2, 3, 4)
        )


def test_add_symbol_ambiguous():

    arith = SymbolArithmetic()
    arith.add_symbol('&', (5,))

    with pytest.raises(AmbiguousSymbol):
        arith.add_symbol('&', (2,))

    with pytest.raises(AmbiguousSymbol):
        arith.add_symbol('!', (5,))


def test_add_symbol_unfitting_dimensions():

    arith = SymbolArithmetic(dimensions=2)

    with pytest.raises(UnfittingDimensions):
        arith.add_symbol('&', (2,))

    with pytest.raises(UnfittingDimensions):
        arith.add_symbol('!', (5, 5, 3))


def test_parse():

    arith = SymbolArithmetic()
    arith.add_symbol('/^', (3,))
    arith.add_symbol('*!', (-1,))

    literals = arith.parse('/^*!*!')
    assert literals == ('/^', '*!', '*!')


def test_parse_empty_disallowed():

    arith = SymbolArithmetic()
    arith.add_symbol('/^', (3,))
    arith.add_symbol('*!', (-1,))

    with pytest.raises(UnknownSymbolString):
        arith.parse('')


def test_parse_empty_allowed():

    arith = SymbolArithmetic(
        allow_empty=True
    )
    arith.add_symbol('/^', (3,))
    arith.add_symbol('*!', (-1,))

    literals = arith.parse('')
    assert literals == tuple()


def test_parse_offset():

    arith = SymbolArithmetic(
        offset=(3,)
    )
    arith.add_symbol('*!', (-1,))

    literals = arith.parse('*!')
    assert literals == ('*!',)


def test_parse_unknown():

    arith = SymbolArithmetic()
    arith.add_symbol('*!', (-1,))

    with pytest.raises(UnknownSymbolString):
        arith.parse('*!**!')


def test_parse_min_violation():

    arith = SymbolArithmetic()
    arith.add_symbol('++', (1,), min_occurence=1)
    arith.add_symbol('*!', (-1,))

    literals = arith.parse('*!++*!')
    assert literals == ('*!', '++', '*!')

    with pytest.raises(UnknownSymbolString):
        arith.parse('*!*!')


def test_parse_max_violation():

    arith = SymbolArithmetic()
    arith.add_symbol('++', (1,), max_occurence=2)
    arith.add_symbol('*!', (-1,))

    literals = arith.parse('*!++++')
    assert literals == ('*!', '++', '++')

    with pytest.raises(UnknownSymbolString):
        arith.parse('*!++*!++*!++')


@pytest.mark.parametrize(
    'symbol_str, value',
    [
        ('&', (1,)),
        ('&++', (0,)),
        ('....../', (19,)),
        ('&../++.&./', (1+2+9-1+2+1+9,)),
        ('&../&./', (1+2+9+1+9,)),
    ]
)
def test_get_vector(symbol_str, value):

    arith = SymbolArithmetic()
    arith.add_symbol('&', (1,))
    arith.add_symbol('++', (-1,))
    arith.add_symbol('./', (9,))
    arith.add_symbol('.', (2,))

    assert arith.get_vector(symbol_str) == value


@pytest.mark.parametrize(
    'symbol_str, value',
    [
        ('&', (5,)),
        ('&++', (4,)),
        ('....../', (23,)),
        ('&../++.&./', (1+2+9-1+2+1+9+4,)),
        ('&../&./', (1+2+9+1+9+4,)),
    ]
)
def test_get_vector_offset(symbol_str, value):

    arith = SymbolArithmetic(
        offset=(4,)
    )
    arith.add_symbol('&', (1,))
    arith.add_symbol('++', (-1,))
    arith.add_symbol('./', (9,))
    arith.add_symbol('.', (2,))

    assert arith.get_vector(symbol_str) == value


@pytest.mark.parametrize(
    'symbol_str, value',
    [
        ('&', (-1,)),
        ('&++', (-2,)),
        ('....../', (17,)),
        ('&../++.&./', (1+2+9-1+2+1+9-2,)),
        ('&../&./', (1+2+9+1+9-2,)),
    ]
)
def test_get_vector_offset_neg(symbol_str, value):

    arith = SymbolArithmetic(
        offset=(-2,)
    )
    arith.add_symbol('&', (1,))
    arith.add_symbol('++', (-1,))
    arith.add_symbol('./', (9,))
    arith.add_symbol('.', (2,))

    assert arith.get_vector(symbol_str) == value


def test_get_vector_unknown():

    arith = SymbolArithmetic(
        offset=(-2,)
    )
    arith.add_symbol('&', (1,), min_occurence=1)
    arith.add_symbol('++', (-1,), max_occurence=1)
    arith.add_symbol('./', (9,))
    arith.add_symbol('.', (2,))

    with pytest.raises(UnknownSymbolString):
        assert arith.get_vector('+&../')

    with pytest.raises(UnknownSymbolString):
        assert arith.get_vector('++./')

    with pytest.raises(UnknownSymbolString):
        assert arith.get_vector('++.++')


@pytest.mark.parametrize(
    'symbol_str, value',
    [
        ('&', (1,)),
        ('++&', (0,)),
        ('././&', (19,)),
        ('././..&', (23,)),
        ('././..', (22,)),
    ]
)
def test_get_symbol_str(symbol_str, value):

    arith = SymbolArithmetic()
    arith.add_symbol('++', (-1,))
    arith.add_symbol('./', (9,))
    arith.add_symbol('.', (2,))
    arith.add_symbol('&', (1,))

    assert arith.get_symbol_str(value) == symbol_str


def test_get_symbol_str_unfitting_dimensions():

    arith = SymbolArithmetic()
    arith.add_symbol('&', (5,))

    with pytest.raises(UnfittingDimensions):
        arith.get_symbol_str((2, 3, 4))


@pytest.mark.parametrize(
    'symbol_str, value',
    [
        ('&', (5,)),
        ('++&', (4,)),
        ('././&', (23,)),
        ('././..&', (27,)),
        ('././..', (26,)),
    ]
)
def test_get_symbol_str_offset(symbol_str, value):

    arith = SymbolArithmetic(
        offset=(4,)
    )
    arith.add_symbol('++', (-1,))
    arith.add_symbol('./', (9,))
    arith.add_symbol('.', (2,))
    arith.add_symbol('&', (1,))

    assert arith.get_symbol_str(value) == symbol_str


@pytest.mark.parametrize(
    'symbol_str, value',
    [
        ('&', (-1,)),
        ('++&', (-2,)),
        ('././&', (17,)),
        ('././..&', (21,)),
        ('././..', (20,)),
    ]
)
def test_get_symbol_str_offset_neg(symbol_str, value):

    arith = SymbolArithmetic(
        offset=(-2,)
    )
    arith.add_symbol('++', (-1,))
    arith.add_symbol('./', (9,))
    arith.add_symbol('.', (2,))
    arith.add_symbol('&', (1,))

    assert arith.get_symbol_str(value) == symbol_str


def test_get_symbol_str_allow_empty():

    arith = SymbolArithmetic(
        allow_empty=True
    )
    arith.add_symbol('&', (1,))
    arith.add_symbol('++', (-1,))

    assert arith.get_symbol_str((0,)) == ''


def test_get_symbol_str_not_mapped():

    arith = SymbolArithmetic(
        offset=(-2,)
    )
    arith.add_symbol('./', (9,))
    arith.add_symbol('.', (2,))

    with pytest.raises(SymbolValueNotMapped):
        assert arith.get_symbol_str((1,))

    with pytest.raises(SymbolValueNotMapped):
        assert arith.get_symbol_str((1,))

    # TODO: should we allow empty arithmetics
    # that map to 0 if allow_empty=True?

    empty = SymbolArithmetic()

    with pytest.raises(SymbolValueNotMapped):
        assert empty.get_symbol_str((0,))


@pytest.mark.parametrize(
    'symbols, value',
    [
        (('&',), (1,)),
        (('++', '&'), (0,)),
        (('./', './', '&'), (19,)),
        (('./', './', '.', '.', '&'), (23,)),
        (('./', './', '.', '.'), (22,)),
    ]
)
def test_get_symbols(symbols, value):

    arith = SymbolArithmetic()
    arith.add_symbol('++', (-1,))
    arith.add_symbol('./', (9,))
    arith.add_symbol('.', (2,))
    arith.add_symbol('&', (1,))

    assert arith.get_symbols(value) == symbols


def test_get_symbols_unfitting_dimensions():

    arith = SymbolArithmetic()
    arith.add_symbol('&', (5,))

    with pytest.raises(UnfittingDimensions):
        arith.get_symbols((2, 3, 4))


@pytest.mark.parametrize(
    'symbols, value',
    [
        (('&',), (5,)),
        (('++', '&'), (4,)),
        (('./', './', '&'), (23,)),
        (('./', './', '.', '.', '&'), (27,)),
        (('./', './', '.', '.'), (26,)),
    ]
)
def test_get_symbols_offset(symbols, value):

    arith = SymbolArithmetic(
        offset=(4,)
    )
    arith.add_symbol('++', (-1,))
    arith.add_symbol('./', (9,))
    arith.add_symbol('.', (2,))
    arith.add_symbol('&', (1,))

    assert arith.get_symbols(value) == symbols


@pytest.mark.parametrize(
    'symbols, value',
    [
        (('&',), (-1,)),
        (('++', '&'), (-2,)),
        (('./', './', '&'), (17,)),
        (('./', './', '.', '.', '&'), (21,)),
        (('./', './', '.', '.'), (20,)),
    ]
)
def test_get_symbols_offset_neg(symbols, value):

    arith = SymbolArithmetic(
        offset=(-2,)
    )
    arith.add_symbol('++', (-1,))
    arith.add_symbol('./', (9,))
    arith.add_symbol('.', (2,))
    arith.add_symbol('&', (1,))

    assert arith.get_symbols(value) == symbols


def test_get_symbols_allow_empty():

    arith = SymbolArithmetic(
        allow_empty=True
    )
    arith.add_symbol('&', (1,))
    arith.add_symbol('++', (-1,))

    assert arith.get_symbols((0,)) == tuple()


def test_get_symbols_not_mapped():

    arith = SymbolArithmetic(
        offset=(-2,)
    )
    arith.add_symbol('./', (9,))
    arith.add_symbol('.', (2,))

    with pytest.raises(SymbolValueNotMapped):
        assert arith.get_symbols((1,))

    with pytest.raises(SymbolValueNotMapped):
        assert arith.get_symbols((1,))

    # TODO: should we allow empty arithmetics
    # that map to 0 if allow_empty=True?

    empty = SymbolArithmetic()

    with pytest.raises(SymbolValueNotMapped):
        assert empty.get_symbols((0,))
