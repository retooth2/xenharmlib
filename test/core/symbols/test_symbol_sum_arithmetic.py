import pytest
from xenharmlib.core.symbols import SymbolSumArithmetic
from xenharmlib.core.symbols import UnknownSymbolString
from xenharmlib.core.symbols import AmbiguousSymbol
from xenharmlib.core.symbols import SymbolValueNotMapped


def test_add_symbol_ambiguous():

    arith = SymbolSumArithmetic()
    arith.add_symbol('&', (5,))

    with pytest.raises(AmbiguousSymbol):
        arith.add_symbol('&', (2,))

    with pytest.raises(AmbiguousSymbol):
        arith.add_symbol('!', (5,))


def test_parse():

    arith = SymbolSumArithmetic()
    arith.add_symbol('/^', (3,))
    arith.add_symbol('*!', (-1,))

    literals = arith.parse('/^*!*!')
    assert literals == ['/^', '*!', '*!']


def test_parse_empty_disallowed():

    arith = SymbolSumArithmetic()
    arith.add_symbol('/^', (3,))
    arith.add_symbol('*!', (-1,))

    with pytest.raises(UnknownSymbolString):
        arith.parse('')


def test_parse_empty_allowed():

    arith = SymbolSumArithmetic(
        allow_empty=True
    )
    arith.add_symbol('/^', (3,))
    arith.add_symbol('*!', (-1,))

    literals = arith.parse('')
    assert literals == []


def test_parse_offset():

    arith = SymbolSumArithmetic(
        offset=(3,)
    )
    arith.add_symbol('*!', (-1,))

    literals = arith.parse('*!')
    assert literals == ['*!']


def test_parse_unknown():

    arith = SymbolSumArithmetic()
    arith.add_symbol('*!', (-1,))

    with pytest.raises(UnknownSymbolString):
        arith.parse('*!**!')


def test_parse_min_violation():

    arith = SymbolSumArithmetic()
    arith.add_symbol('++', (1,), min_occurence=1)
    arith.add_symbol('*!', (-1,))

    literals = arith.parse('*!++*!')
    assert literals == ['*!', '++', '*!']

    with pytest.raises(UnknownSymbolString):
        arith.parse('*!*!')


def test_parse_max_violation():

    arith = SymbolSumArithmetic()
    arith.add_symbol('++', (1,), max_occurence=2)
    arith.add_symbol('*!', (-1,))

    literals = arith.parse('*!++++')
    assert literals == ['*!', '++', '++']

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

    arith = SymbolSumArithmetic()
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

    arith = SymbolSumArithmetic(
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

    arith = SymbolSumArithmetic(
        offset=(-2,)
    )
    arith.add_symbol('&', (1,))
    arith.add_symbol('++', (-1,))
    arith.add_symbol('./', (9,))
    arith.add_symbol('.', (2,))

    assert arith.get_vector(symbol_str) == value


def test_get_vector_unknown():

    arith = SymbolSumArithmetic(
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

    arith = SymbolSumArithmetic()
    arith.add_symbol('++', (-1,))
    arith.add_symbol('./', (9,))
    arith.add_symbol('.', (2,))
    arith.add_symbol('&', (1,))

    assert arith.get_symbol_str(value) == symbol_str


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

    arith = SymbolSumArithmetic(
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

    arith = SymbolSumArithmetic(
        offset=(-2,)
    )
    arith.add_symbol('++', (-1,))
    arith.add_symbol('./', (9,))
    arith.add_symbol('.', (2,))
    arith.add_symbol('&', (1,))

    assert arith.get_symbol_str(value) == symbol_str


def test_get_symbol_str_allow_empty():

    arith = SymbolSumArithmetic(
        allow_empty=True
    )
    arith.add_symbol('&', (1,))
    arith.add_symbol('++', (-1,))

    assert arith.get_symbol_str((0,)) == ''


def test_get_symbol_str_not_mapped():

    arith = SymbolSumArithmetic(
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

    empty = SymbolSumArithmetic()

    with pytest.raises(SymbolValueNotMapped):
        assert empty.get_symbol_str((0,))
