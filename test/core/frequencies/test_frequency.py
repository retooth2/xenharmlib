import pytest
import sympy as sp
from fractions import Fraction
from xenharmlib.core.frequencies import Frequency
from xenharmlib.core.frequencies import FrequencyRatio

# all possible type pairs grouped by (possible) commutativity:

# freq(int) x freq(int)
# freq(int) x ratio(int)
# ratio(int) x freq(int)
# freq(int) x ratio(int, int)
# ratio(int, int) x freq(int)
# freq(int) x ratio(float)
# ratio(float) x freq(int)
# freq(int) x ratio(Fraction)
# ratio(Fraction) x freq(int)
# freq(int) x ratio(SP_NUM)
# ratio(SP_NUM) x freq(int)
# freq(int) x freq(float)
# freq(float) x freq(int)
# freq(int) x freq(Fraction)
# freq(Fraction) x freq(int)
# freq(int) x freq(SP_NUM)
# freq(SP_NUM) x freq(int)
# freq(int) x int
# int x freq(int)
# freq(int) x float
# float x freq(int)
# freq(int) x fraction
# fraction x freq(int)
# freq(int) x SP_NUM
# SP_NUM x freq(int)

# freq(float) x freq(float)
# freq(float) x ratio(int)
# ratio(int) x freq(float)
# freq(float) x ratio(int, int)
# ratio(int, int) x freq(float)
# freq(float) x ratio(float)
# ratio(float) x freq(float)
# freq(float) x ratio(Fraction)
# ratio(Fraction) x freq(float)
# freq(float) x ratio(SP_NUM)
# ratio(SP_NUM) x freq(float)
# freq(float) x freq(Fraction)
# freq(Fraction) x freq(float)
# freq(float) x freq(SP_NUM)
# freq(SP_NUM) x freq(float)
# freq(float) x int
# int x freq(float)
# freq(float) x float
# float x freq(float)
# freq(float) x fraction
# fraction x freq(float)
# freq(float) x SP_NUM
# SP_NUM x freq(float)

# freq(Fraction) x freq(Fraction)
# freq(Fraction) x ratio(int)
# ratio(int) x freq(Fraction)
# freq(Fraction) x ratio(int, int)
# ratio(int, int) x freq(Fraction)
# freq(Fraction) x ratio(float)
# ratio(float) x freq(Fraction)
# freq(Fraction) x ratio(Fraction)
# ratio(Fraction) x freq(Fraction)
# freq(Fraction) x ratio(SP_NUM)
# ratio(SP_NUM) x freq(Fraction)
# freq(Fraction) x freq(SP_NUM)
# freq(SP_NUM) x freq(Fraction)
# freq(Fraction) x int
# int x freq(Fraction)
# freq(Fraction) x float
# float x freq(Fraction)
# freq(Fraction) x fraction
# fraction x freq(Fraction)
# freq(Fraction) x SP_NUM
# SP_NUM x freq(Fraction)

# freq(SP_NUM) x freq(SP_NUM)
# freq(SP_NUM) x ratio(int)
# ratio(int) x freq(SP_NUM)
# freq(SP_NUM) x ratio(int, int)
# ratio(int, int) x freq(SP_NUM)
# freq(SP_NUM) x ratio(float)
# ratio(float) x freq(SP_NUM)
# freq(SP_NUM) x ratio(Fraction)
# ratio(Fraction) x freq(SP_NUM)
# freq(SP_NUM) x ratio(SP_NUM)
# ratio(SP_NUM) x freq(SP_NUM)
# freq(SP_NUM) x int
# int x freq(SP_NUM)
# freq(SP_NUM) x float
# float x freq(SP_NUM)
# freq(SP_NUM) x fraction
# fraction x freq(SP_NUM)
# freq(SP_NUM) x SP_NUM
# SP_NUM x freq(SP_NUM)

SP_NUM = sp.Integer(2) ** sp.Rational(1, 3)
SP_X, SP_Y = sp.symbols('x y')
SP_NON_NUMBER = SP_X**2*2*SP_Y


def test_get_harmonic():
    """
    Test if harmonic series gets calculated correctly
    when calling get_harmonic (sans s) method
    """

    series = [
        Frequency(400),
        Frequency(800),
        Frequency(1200),
        Frequency(1600),
        Frequency(2000),
        Frequency(2400)
    ]

    for i, frequency in enumerate(series):
        assert frequency == Frequency(400).get_harmonic(i)


def test_get_harmonics():
    """
    Test if harmonic series gets calculated correctly
    when calling get_harmonics method with default
    limit parameter of 20k Herz
    """

    series = [
        Frequency(2000),
        Frequency(4000),
        Frequency(6000),
        Frequency(8000),
        Frequency(10000),
        Frequency(12000),
        Frequency(14000),
        Frequency(16000),
        Frequency(18000),
        Frequency(20000),
    ]

    assert Frequency(2000).get_harmonics() == series


def test_get_harmonics_limit():
    """
    Test if harmonic series gets calculated correctly
    when calling get_harmonics method with a custom
    limit parameter
    """

    series = [
        Frequency(2000),
        Frequency(4000),
        Frequency(6000),
        Frequency(8000),
        Frequency(10000),
        Frequency(12000),
        Frequency(14000),
    ]

    assert Frequency(2000).get_harmonics(
        limit=Frequency(15000)
    ) == series


@pytest.mark.parametrize(
    'a, b, result',
    [
        # freq(int) x freq(int)
        (Frequency(3), Frequency(2), Frequency(5)),
        # freq(int) x freq(float)
        (Frequency(3), Frequency(2.0), Frequency(5)),
        # freq(int) x freq(Fraction)
        (Frequency(3), Frequency(Fraction(3, 2)), Frequency(Fraction(9, 2))),
        # freq(int) x freq(SP_NUM)
        (Frequency(3), Frequency(SP_NUM), Frequency(3 + SP_NUM)),
        # freq(float) x freq(float)
        (Frequency(3.5), Frequency(2.5), Frequency(6)),
        # freq(float) x freq(Fraction)
        (Frequency(0.5), Frequency(Fraction(3, 2)), Frequency(2)),
        # freq(float) x freq(SP_NUM)
        (
            Frequency(3.5),
            Frequency(SP_NUM),
            Frequency(Fraction(7, 2) + SP_NUM)
        ),
        # freq(Fraction) x freq(Fraction)
        (
            Frequency(Fraction(5, 3)),
            Frequency(Fraction(1, 2)),
            Frequency(Fraction(13, 6))
        ),
        # freq(Fraction) x freq(SP_NUM)
        (
            Frequency(Fraction(5, 3)),
            Frequency(SP_NUM),
            Frequency(Fraction(5, 3) + SP_NUM)
        ),
        # freq(SP_NUM) x freq(SP_NUM)
        (
            Frequency(SP_NUM),
            Frequency(SP_NUM),
            Frequency(2 * SP_NUM)
        ),
    ]
)
def test_add(a, b, result):
    assert isinstance(a + b, Frequency)
    assert isinstance(b + a, Frequency)
    assert a + b == result
    assert b + a == result


@pytest.mark.parametrize(
    'a, b',
    [
        # freq(int) x ratio(int)
        (Frequency(5), FrequencyRatio(2)),
        # freq(int) x ratio(int, int)
        (Frequency(5), FrequencyRatio(2, 3)),
        # freq(int) x ratio(float)
        (Frequency(5), FrequencyRatio(3.5)),
        # freq(int) x ratio(Fraction)
        (Frequency(5), FrequencyRatio(Fraction(2, 3))),
        # freq(int) x ratio(SP_NUM)
        (Frequency(5), FrequencyRatio(SP_NUM)),
        # freq(int) x int
        (Frequency(5), 2),
        # freq(int) x float
        (Frequency(5), 3.5),
        # freq(int) x fraction
        (Frequency(5), Fraction(2, 3)),
        # freq(int) x SP_NUM
        (Frequency(5), SP_NUM),
        # freq(float) x ratio(int)
        (Frequency(5.4), FrequencyRatio(2)),
        # freq(float) x ratio(int, int)
        (Frequency(2.3), FrequencyRatio(2, 3)),
        # freq(float) x ratio(float)
        (Frequency(5.3), FrequencyRatio(3.5)),
        # freq(float) x ratio(Fraction)
        (Frequency(1.4), FrequencyRatio(Fraction(2, 3))),
        # freq(float) x ratio(SP_NUM)
        (Frequency(1.5), FrequencyRatio(SP_NUM)),
        # freq(float) x int
        (Frequency(5.2), 2),
        # freq(float) x float
        (Frequency(9.2), 2.5),
        # freq(float) x fraction
        (Frequency(1.2), Fraction(2, 3)),
        # freq(float) x SP_NUM
        (Frequency(3.2), SP_NUM),
        # freq(Fraction) x ratio(int)
        (Frequency(Fraction(2, 3)), FrequencyRatio(1)),
        # freq(Fraction) x ratio(int, int)
        (Frequency(Fraction(2, 3)), FrequencyRatio(1, 2)),
        # freq(Fraction) x ratio(float)
        (Frequency(Fraction(2, 3)), FrequencyRatio(3.5)),
        # freq(Fraction) x ratio(Fraction)
        (Frequency(Fraction(2, 3)), FrequencyRatio(Fraction(2, 3))),
        # freq(Fraction) x ratio(SP_NUM)
        (Frequency(Fraction(2, 3)), FrequencyRatio(SP_NUM)),
        # freq(Fraction) x int
        (Frequency(Fraction(2, 3)), 2),
        # freq(Fraction) x float
        (Frequency(Fraction(2, 3)), 2.3),
        # freq(Fraction) x fraction
        (Frequency(Fraction(2, 3)), Fraction(3, 4)),
        # freq(Fraction) x SP_NUM
        (Frequency(Fraction(2, 3)), SP_NUM),
        # freq(SP_NUM) x ratio(int)
        (Frequency(SP_NUM), FrequencyRatio(1)),
        # freq(SP_NUM) x ratio(int, int)
        (Frequency(SP_NUM), FrequencyRatio(1, 2)),
        # freq(SP_NUM) x ratio(float)
        (Frequency(SP_NUM), FrequencyRatio(4.3)),
        # freq(SP_NUM) x ratio(Fraction)
        (Frequency(SP_NUM), FrequencyRatio(Fraction(2, 3))),
        # freq(SP_NUM) x ratio(SP_NUM)
        (Frequency(SP_NUM), FrequencyRatio(SP_NUM)),
        # freq(SP_NUM) x int
        (Frequency(SP_NUM), 4),
        # freq(SP_NUM) x float
        (Frequency(SP_NUM), 4.2),
        # freq(SP_NUM) x fraction
        (Frequency(SP_NUM), Fraction(2, 3)),
        # freq(SP_NUM) x SP_NUM
        (Frequency(SP_NUM), SP_NUM),
        # other incompatible types
        (Frequency(2), 'abc'),
        (Frequency(2), SP_NON_NUMBER),
        (Frequency(2), complex(100, 3)),
        (Frequency(3.5), 'abc'),
        (Frequency(3.5), SP_NON_NUMBER),
        (Frequency(9.2), complex(100, 3)),
        (Frequency(Fraction(2, 3)), 'abc'),
        (Frequency(Fraction(2, 3)), SP_NON_NUMBER),
        (Frequency(Fraction(2, 3)), complex(100, 3)),
    ]
)
def test_add_type_error(a, b):
    with pytest.raises(TypeError):
        a + b
    with pytest.raises(TypeError):
        b + a


@pytest.mark.parametrize(
    'a, b, result',
    [
        # freq(int) x freq(int)
        (Frequency(3), Frequency(2), Frequency(1)),
        # freq(int) x freq(float)
        (Frequency(3), Frequency(2.0), Frequency(1)),
        # freq(float) x freq(int)
        (Frequency(3.0), Frequency(1), Frequency(2)),
        # freq(int) x freq(Fraction)
        (Frequency(3), Frequency(Fraction(3, 2)), Frequency(Fraction(3, 2))),
        # freq(Fraction) x freq(int)
        (Frequency(Fraction(3, 2)), Frequency(3), Frequency(Fraction(-3, 2))),
        # freq(int) x freq(SP_NUM)
        (Frequency(3), Frequency(SP_NUM), Frequency(3 - SP_NUM)),
        # freq(SP_NUM) x freq(int)
        (Frequency(SP_NUM), Frequency(10), Frequency(SP_NUM - 10)),
        # freq(float) x freq(float)
        (Frequency(3.5), Frequency(2.5), Frequency(1)),
        # freq(float) x freq(Fraction)
        (Frequency(3.5), Frequency(Fraction(3, 2)), Frequency(2)),
        # freq(Fraction) x freq(float)
        (Frequency(Fraction(3, 2)), Frequency(0.5), Frequency(1)),
        # freq(float) x freq(SP_NUM)
        (
            Frequency(3.5),
            Frequency(SP_NUM),
            Frequency(Fraction(7, 2) - SP_NUM)
        ),
        # freq(SP_NUM) x freq(float)
        (
            Frequency(SP_NUM),
            Frequency(1.5),
            Frequency(SP_NUM - Fraction(3, 2))
        ),
        # freq(Fraction) x freq(Fraction)
        (
            Frequency(Fraction(3, 2)),
            Frequency(Fraction(1, 5)),
            Frequency(Fraction(13, 10))
        ),
        # freq(Fraction) x freq(SP_NUM)
        (
            Frequency(Fraction(3, 2)),
            Frequency(SP_NUM),
            Frequency(Fraction(3, 2) - SP_NUM)
        ),
        # freq(SP_NUM) x freq(Fraction)
        (
            Frequency(SP_NUM),
            Frequency(Fraction(3, 2)),
            Frequency(SP_NUM - Fraction(3, 2))
        ),
        (Frequency(2 * SP_NUM), Frequency(SP_NUM), Frequency(SP_NUM)),
    ]
)
def test_sub(a, b, result):
    assert isinstance(a - b, Frequency)
    assert a - b == result


@pytest.mark.parametrize(
    'a, b',
    [
        # freq(int) x ratio(int)
        (Frequency(5), FrequencyRatio(2)),
        # freq(int) x ratio(int, int)
        (Frequency(5), FrequencyRatio(2, 3)),
        # freq(int) x ratio(float)
        (Frequency(5), FrequencyRatio(3.5)),
        # freq(int) x ratio(Fraction)
        (Frequency(5), FrequencyRatio(Fraction(2, 3))),
        # freq(int) x ratio(SP_NUM)
        (Frequency(5), FrequencyRatio(SP_NUM)),
        # freq(int) x int
        (Frequency(5), 2),
        # freq(int) x float
        (Frequency(5), 3.5),
        # freq(int) x fraction
        (Frequency(5), Fraction(2, 3)),
        # freq(int) x SP_NUM
        (Frequency(5), SP_NUM),
        # freq(float) x ratio(int)
        (Frequency(5.4), FrequencyRatio(2)),
        # freq(float) x ratio(int, int)
        (Frequency(2.3), FrequencyRatio(2, 3)),
        # freq(float) x ratio(float)
        (Frequency(5.3), FrequencyRatio(3.5)),
        # freq(float) x ratio(Fraction)
        (Frequency(1.4), FrequencyRatio(Fraction(2, 3))),
        # freq(float) x ratio(SP_NUM)
        (Frequency(1.5), FrequencyRatio(SP_NUM)),
        # freq(float) x int
        (Frequency(5.2), 2),
        # freq(float) x float
        (Frequency(9.2), 2.5),
        # freq(float) x fraction
        (Frequency(1.2), Fraction(2, 3)),
        # freq(float) x SP_NUM
        (Frequency(3.2), SP_NUM),
        # freq(Fraction) x ratio(int)
        (Frequency(Fraction(2, 3)), FrequencyRatio(1)),
        # freq(Fraction) x ratio(int, int)
        (Frequency(Fraction(2, 3)), FrequencyRatio(1, 2)),
        # freq(Fraction) x ratio(float)
        (Frequency(Fraction(2, 3)), FrequencyRatio(3.5)),
        # freq(Fraction) x ratio(Fraction)
        (Frequency(Fraction(2, 3)), FrequencyRatio(Fraction(2, 3))),
        # freq(Fraction) x ratio(SP_NUM)
        (Frequency(Fraction(2, 3)), FrequencyRatio(SP_NUM)),
        # freq(Fraction) x int
        (Frequency(Fraction(2, 3)), 2),
        # freq(Fraction) x float
        (Frequency(Fraction(2, 3)), 2.3),
        # freq(Fraction) x fraction
        (Frequency(Fraction(2, 3)), Fraction(3, 4)),
        # freq(Fraction) x SP_NUM
        (Frequency(Fraction(2, 3)), SP_NUM),
        # freq(SP_NUM) x ratio(int)
        (Frequency(SP_NUM), FrequencyRatio(1)),
        # freq(SP_NUM) x ratio(int, int)
        (Frequency(SP_NUM), FrequencyRatio(1, 2)),
        # freq(SP_NUM) x ratio(float)
        (Frequency(SP_NUM), FrequencyRatio(4.3)),
        # freq(SP_NUM) x ratio(Fraction)
        (Frequency(SP_NUM), FrequencyRatio(Fraction(2, 3))),
        # freq(SP_NUM) x ratio(SP_NUM)
        (Frequency(SP_NUM), FrequencyRatio(SP_NUM)),
        # freq(SP_NUM) x int
        (Frequency(SP_NUM), 4),
        # freq(SP_NUM) x float
        (Frequency(SP_NUM), 4.2),
        # freq(SP_NUM) x fraction
        (Frequency(SP_NUM), Fraction(2, 3)),
        # freq(SP_NUM) x SP_NUM
        (Frequency(SP_NUM), SP_NUM),
        # other incompatible types
        (Frequency(2), 'abc'),
        (Frequency(2), SP_NON_NUMBER),
        (Frequency(2), complex(100, 3)),
        (Frequency(3.5), 'abc'),
        (Frequency(3.5), SP_NON_NUMBER),
        (Frequency(9.2), complex(100, 3)),
        (Frequency(Fraction(2, 3)), 'abc'),
        (Frequency(Fraction(2, 3)), SP_NON_NUMBER),
        (Frequency(Fraction(2, 3)), complex(100, 3)),
    ]
)
def test_sub_type_error(a, b):
    with pytest.raises(TypeError):
        a - b
    with pytest.raises(TypeError):
        b - a


@pytest.mark.parametrize(
    'a, b, result',
    [
        # freq(int) x ratio(int)
        (Frequency(4), FrequencyRatio(2), Frequency(8)),
        # freq(int) x ratio(int, int)
        (Frequency(4), FrequencyRatio(3, 2), Frequency(6)),
        # freq(int) x ratio(float)
        (Frequency(4), FrequencyRatio(0.5), Frequency(2)),
        # freq(int) x ratio(Fraction)
        (
            Frequency(4),
            FrequencyRatio(Fraction(2, 3)),
            Frequency(Fraction(8, 3))
        ),
        # freq(int) x ratio(SP_NUM)
        (Frequency(3), FrequencyRatio(SP_NUM), Frequency(3 * SP_NUM)),
        # freq(int) x int
        (Frequency(3), 2, Frequency(6)),
        # freq(int) x float
        (Frequency(3), 2.0, Frequency(6)),
        # freq(int) x fraction
        (Frequency(3), Fraction(3, 2), Frequency(Fraction(9, 2))),
        # freq(int) x SP_NUM
        (Frequency(6), SP_NUM, Frequency(6 * SP_NUM)),
        # freq(float) x ratio(int)
        (Frequency(3.5), FrequencyRatio(2), Frequency(7)),
        # freq(float) x ratio(int, int)
        (Frequency(3.5), FrequencyRatio(2, 3), Frequency(Fraction(7, 3))),
        # freq(float) x ratio(float)
        (Frequency(3.5), FrequencyRatio(1.5), Frequency(Fraction(21, 4))),
        # freq(float) x ratio(Fraction)
        (
            Frequency(1.5),
            FrequencyRatio(Fraction(2, 3)),
            Frequency(1)
        ),
        # freq(float) x ratio(SP_NUM)
        (
            Frequency(1.5),
            FrequencyRatio(SP_NUM),
            Frequency(Fraction(3, 2) * SP_NUM)
        ),
        # freq(float) x int
        (Frequency(3.5), 2, Frequency(7)),
        # freq(float) x float
        (Frequency(3.5), 1.5, Frequency(Fraction(21, 4))),
        # freq(float) x fraction
        (Frequency(3.5), Fraction(7, 2), Frequency(Fraction(49, 4))),
        # freq(float) x SP_NUM
        (
            Frequency(1.5),
            SP_NUM,
            Frequency(Fraction(3, 2) * SP_NUM)
        ),
        # freq(Fraction) x ratio(int)
        (
            Frequency(Fraction(2, 3)),
            FrequencyRatio(3),
            Frequency(2)
        ),
        # freq(Fraction) x ratio(int, int)
        (
            Frequency(Fraction(2, 3)),
            FrequencyRatio(3, 9),
            Frequency(Fraction(2, 9))
        ),
        # freq(Fraction) x ratio(float)
        (
            Frequency(Fraction(2, 3)),
            FrequencyRatio(1.5),
            Frequency(1)
        ),
        # freq(Fraction) x ratio(Fraction)
        (
            Frequency(Fraction(2, 3)),
            FrequencyRatio(Fraction(5, 2)),
            Frequency(Fraction(5, 3))
        ),
        # freq(Fraction) x ratio(SP_NUM)
        (
            Frequency(Fraction(5, 3)),
            FrequencyRatio(SP_NUM),
            Frequency(SP_NUM * Fraction(5, 3))
        ),
        # freq(Fraction) x int
        (Frequency(Fraction(2, 3)), 7, Frequency(Fraction(14, 3))),
        # freq(Fraction) x float
        (Frequency(Fraction(2, 3)), 1.5, Frequency(1)),
        # freq(Fraction) x fraction
        (Frequency(Fraction(2, 3)), Fraction(4, 3), Frequency(Fraction(8, 9))),
        # freq(Fraction) x SP_NUM
        (
            Frequency(Fraction(8, 9)),
            SP_NUM,
            Frequency(SP_NUM * Fraction(8, 9))
        ),
        # freq(SP_NUM) x ratio(float)
        (
            Frequency(SP_NUM),
            FrequencyRatio(3.5),
            Frequency(SP_NUM * Fraction(7, 2))
        ),
        # freq(SP_NUM) x ratio(Fraction)
        (
            Frequency(SP_NUM),
            FrequencyRatio(Fraction(3, 4)),
            Frequency(SP_NUM * Fraction(3, 4))
        ),
        # freq(SP_NUM) x ratio(SP_NUM)
        (
            Frequency(SP_NUM),
            FrequencyRatio(SP_NUM),
            Frequency(SP_NUM * SP_NUM)
        ),
        # freq(SP_NUM) x int
        (Frequency(SP_NUM), 3, Frequency(3 * SP_NUM)),
        # freq(SP_NUM) x float
        (Frequency(SP_NUM), 3.5, Frequency(Fraction(7, 2) * SP_NUM)),
        # freq(SP_NUM) x fraction
        (
            Frequency(SP_NUM),
            Fraction(9, 7),
            Frequency(Fraction(9, 7) * SP_NUM)
        ),
        # freq(SP_NUM) x SP_NUM
        (Frequency(SP_NUM), SP_NUM, Frequency(SP_NUM * SP_NUM)),
    ]
)
def test_mul(a, b, result):
    assert isinstance(a * b, Frequency)
    assert isinstance(b * a, Frequency)
    assert a * b == result
    assert b * a == result


@pytest.mark.parametrize(
    'a, b',
    [
        # freq(int) x freq(int)
        (Frequency(3), Frequency(2)),
        # freq(int) x freq(float)
        (Frequency(3), Frequency(2.0)),
        # freq(float) x freq(int)
        (Frequency(3.0), Frequency(1)),
        # freq(int) x freq(Fraction)
        (Frequency(3), Frequency(Fraction(3, 2))),
        # freq(Fraction) x freq(int)
        (Frequency(Fraction(3, 2)), Frequency(3)),
        # freq(int) x freq(SP_NUM)
        (Frequency(3), Frequency(SP_NUM)),
        # freq(SP_NUM) x freq(int)
        (Frequency(SP_NUM), Frequency(10)),
        # freq(float) x freq(float)
        (Frequency(3.5), Frequency(2.5)),
        # freq(float) x freq(Fraction)
        (Frequency(3.5), Frequency(Fraction(3, 2))),
        # freq(Fraction) x freq(float)
        (Frequency(Fraction(3, 2)), Frequency(0.5)),
        # freq(float) x freq(SP_NUM)
        (Frequency(3.5), Frequency(SP_NUM)),
        # freq(SP_NUM) x freq(float)
        (Frequency(SP_NUM), Frequency(1.5)),
        # freq(Fraction) x freq(Fraction)
        (
            Frequency(Fraction(3, 2)),
            Frequency(Fraction(1, 5)),
        ),
        # freq(Fraction) x freq(SP_NUM)
        (
            Frequency(Fraction(3, 2)),
            Frequency(SP_NUM),
        ),
        # freq(SP_NUM) x freq(Fraction)
        (
            Frequency(SP_NUM),
            Frequency(Fraction(3, 2)),
        ),
        # freq(SP_NUM) x freq(SP_NUM)
        (Frequency(2 * SP_NUM), Frequency(SP_NUM)),
        # other incompatible types
        (Frequency(2), 'abc'),
        (Frequency(2), SP_NON_NUMBER),
        (Frequency(2), complex(100, 3)),
        (Frequency(3.5), 'abc'),
        (Frequency(3.5), SP_NON_NUMBER),
        (Frequency(9.2), complex(100, 3)),
        (Frequency(Fraction(2, 3)), 'abc'),
        (Frequency(Fraction(2, 3)), SP_NON_NUMBER),
        (Frequency(Fraction(2, 3)), complex(100, 3)),
    ]
)
def test_mul_type_error(a, b):
    with pytest.raises(TypeError):
        a * b
    with pytest.raises(TypeError):
        b * a


@pytest.mark.parametrize(
    'a, b, result',
    [
        # freq(int) x freq(int)
        (Frequency(3), Frequency(2), FrequencyRatio(3, 2)),
        # freq(int) x freq(float)
        (Frequency(3), Frequency(1.5), FrequencyRatio(2)),
        # freq(float) x freq(int)
        (Frequency(3.5), Frequency(2), FrequencyRatio(7, 4)),
        # freq(int) x freq(Fraction)
        (
            Frequency(Fraction(3, 4)),
            Frequency(Fraction(9, 7)),
            FrequencyRatio(7, 12)
        ),
        # freq(Fraction) x freq(int)
        (Frequency(Fraction(3, 4)), Frequency(2), FrequencyRatio(3, 8)),
        # freq(int) x freq(SP_NUM)
        (Frequency(3), Frequency(SP_NUM), FrequencyRatio(3 / SP_NUM)),
        # freq(SP_NUM) x freq(int)
        (Frequency(SP_NUM), Frequency(2), FrequencyRatio(SP_NUM / 2)),
        # freq(float) x freq(float)
        (Frequency(1.5), Frequency(2.5), FrequencyRatio(3, 5)),
        # freq(float) x freq(Fraction)
        (Frequency(1.5), Frequency(Fraction(3, 2)), FrequencyRatio(1)),
        # freq(Fraction) x freq(float)
        (Frequency(Fraction(1, 2)), Frequency(2.5), FrequencyRatio(1, 5)),
        # freq(float) x freq(SP_NUM)
        (Frequency(2.5), Frequency(SP_NUM), FrequencyRatio(5, 2 * SP_NUM)),
        # freq(SP_NUM) x freq(float)
        (Frequency(SP_NUM), Frequency(2.5), FrequencyRatio(2 * SP_NUM, 5)),
        # freq(Fraction) x freq(Fraction)
        (
            Frequency(Fraction(1, 2)),
            Frequency(Fraction(2, 3)),
            FrequencyRatio(3, 4)
        ),
        # freq(Fraction) x freq(SP_NUM)
        (
            Frequency(Fraction(1, 2)),
            Frequency(SP_NUM),
            FrequencyRatio(1, 2 * SP_NUM)
        ),
        # freq(SP_NUM) x freq(Fraction)
        (
            Frequency(Fraction(1, 2)),
            Frequency(Fraction(3, 7)),
            FrequencyRatio(7, 6)
        ),
        # freq(SP_NUM) x freq(SP_NUM)
        (
            Frequency(SP_NUM),
            Frequency(SP_NUM),
            FrequencyRatio(1)
        ),
        # freq(int) x ratio(int)
        (Frequency(3), FrequencyRatio(2), Frequency(Fraction(3, 2))),
        # freq(int) x ratio(int, int)
        (Frequency(3), FrequencyRatio(2, 3), Frequency(Fraction(9, 2))),
        # freq(int) x ratio(float)
        (Frequency(4), FrequencyRatio(1.5), Frequency(Fraction(8, 3))),
        # freq(int) x ratio(Fraction)
        (
            Frequency(4),
            FrequencyRatio(1.5),
            Frequency(Fraction(8, 3))
        ),
        # freq(int) x ratio(SP_NUM)
        (Frequency(4), FrequencyRatio(SP_NUM), Frequency(4 / SP_NUM)),
        # freq(int) x int
        (Frequency(4), 3, Frequency(Fraction(4, 3))),
        # freq(int) x float
        (Frequency(4), 1.5, Frequency(Fraction(8, 3))),
        # freq(int) x fraction
        (Frequency(4), Fraction(5, 2), Frequency(Fraction(8, 5))),
        # freq(int) x SP_NUM
        (Frequency(4), SP_NUM, Frequency(4 / SP_NUM)),
        # freq(float) x ratio(int)
        (Frequency(1.5), FrequencyRatio(2), Frequency(Fraction(3, 4))),
        # freq(float) x ratio(int, int)
        (Frequency(1.5), FrequencyRatio(2, 3), Frequency(Fraction(9, 4))),
        # freq(float) x ratio(float)
        (Frequency(1.5), FrequencyRatio(2.5), Frequency(Fraction(3, 5))),
        # freq(float) x ratio(Fraction)
        (
            Frequency(1.5),
            FrequencyRatio(Fraction(7, 3)),
            Frequency(Fraction(9, 14))
        ),
        # freq(float) x ratio(SP_NUM)
        (
            Frequency(1.5),
            FrequencyRatio(SP_NUM),
            Frequency(3 / (2 * SP_NUM))
        ),
        # freq(float) x int
        (Frequency(1.5), 2, Frequency(Fraction(3, 4))),
        # freq(float) x float
        (Frequency(1.5), 0.5, Frequency(3)),
        # freq(float) x fraction
        (Frequency(1.5), Fraction(5, 3), Frequency(Fraction(9, 10))),
        # freq(float) x SP_NUM
        (Frequency(1.5), SP_NUM, Frequency(Fraction(3, 2) / SP_NUM)),
        # freq(Fraction) x ratio(int)
        (
            Frequency(Fraction(2, 3)),
            FrequencyRatio(2),
            Frequency(Fraction(2, 6))
        ),
        # freq(Fraction) x ratio(int, int)
        (
            Frequency(Fraction(2, 3)),
            FrequencyRatio(1, 2),
            Frequency(Fraction(4, 3))
        ),
        # freq(Fraction) x ratio(float)
        (
            Frequency(Fraction(2, 3)),
            FrequencyRatio(0.5),
            Frequency(Fraction(4, 3))
        ),
        # freq(Fraction) x ratio(Fraction)
        (
            Frequency(Fraction(2, 3)),
            FrequencyRatio(Fraction(7, 2)),
            Frequency(Fraction(4, 21))
        ),
        # freq(Fraction) x ratio(SP_NUM)
        (
            Frequency(Fraction(2, 3)),
            FrequencyRatio(SP_NUM),
            Frequency(Fraction(2, 3) / SP_NUM)
        ),
        # freq(Fraction) x int
        (Frequency(Fraction(2, 3)), 5, Frequency(Fraction(2, 15))),
        # freq(Fraction) x float
        (Frequency(Fraction(2, 3)), 1.5, Frequency(Fraction(4, 9))),
        # freq(Fraction) x fraction
        (
            Frequency(Fraction(2, 3)),
            Fraction(7, 2),
            Frequency(Fraction(4, 21))
        ),
        # freq(Fraction) x SP_NUM
        (
            Frequency(Fraction(2, 3)),
            SP_NUM,
            Frequency(Fraction(2, 3) / SP_NUM)
        ),
        # freq(SP_NUM) x ratio(int)
        (
            Frequency(SP_NUM),
            FrequencyRatio(3),
            Frequency(SP_NUM / 3)
        ),
        # freq(SP_NUM) x ratio(int, int)
        (
            Frequency(SP_NUM),
            FrequencyRatio(3, 2),
            Frequency(2 * SP_NUM / 3)
        ),
        # freq(SP_NUM) x ratio(float)
        (
            Frequency(SP_NUM),
            FrequencyRatio(2.5),
            Frequency(2 * SP_NUM / 5)
        ),
        # freq(SP_NUM) x ratio(Fraction)
        (
            Frequency(SP_NUM),
            FrequencyRatio(Fraction(7, 3)),
            Frequency(3 * SP_NUM / 7)
        ),
        # freq(SP_NUM) x ratio(SP_NUM)
        (
            Frequency(SP_NUM),
            FrequencyRatio(SP_NUM),
            Frequency(1)
        ),
        # freq(SP_NUM) x int
        (Frequency(SP_NUM), 2, Frequency(SP_NUM / 2)),
        # freq(SP_NUM) x float
        (Frequency(SP_NUM), 2.5, Frequency(SP_NUM / Fraction(5, 2))),
        # freq(SP_NUM) x fraction
        (
            Frequency(SP_NUM),
            Fraction(6, 7),
            Frequency(SP_NUM / Fraction(6, 7))
        ),
        # freq(SP_NUM) x SP_NUM
        (
            Frequency(SP_NUM),
            SP_NUM,
            Frequency(1)
        ),
    ]
)
def test_truediv(a, b, result):
    assert isinstance(a / b, result.__class__)
    assert a / b == result


@pytest.mark.parametrize(
    'a, b',
    [
        # ratio(int) x freq(int)
        (FrequencyRatio(5), Frequency(2)),
        # ratio(int, int) x freq(int)
        (FrequencyRatio(5, 3), Frequency(2)),
        # ratio(float) x freq(int)
        (FrequencyRatio(1.5), Frequency(5)),
        # ratio(Fraction) x freq(int)
        (FrequencyRatio(Fraction(3, 2)), Frequency(6)),
        # ratio(SP_NUM) x freq(int)
        (FrequencyRatio(SP_NUM), Frequency(9)),
        # int x freq(int)
        (3, Frequency(9)),
        # float x freq(int)
        (9.5, Frequency(7)),
        # fraction x freq(int)
        (Fraction(2, 3), Frequency(4)),
        # SP_NUM x freq(int)
        (SP_NUM, Frequency(4)),
        # ratio(int) x freq(float)
        (FrequencyRatio(5), Frequency(2.5)),
        # ratio(int, int) x freq(float)
        (FrequencyRatio(5, 3), Frequency(4.5)),
        # ratio(float) x freq(float)
        (FrequencyRatio(3.5), Frequency(3.5)),
        # ratio(Fraction) x freq(float)
        (FrequencyRatio(Fraction(2, 3)), Frequency(3.5)),
        # ratio(SP_NUM) x freq(float)
        (FrequencyRatio(SP_NUM), Frequency(3.5)),
        # int x freq(float)
        (4, Frequency(2.5)),
        # float x freq(float)
        (4.8, Frequency(2.5)),
        # fraction x freq(float)
        (Fraction(9, 7), Frequency(2.5)),
        # SP_NUM x freq(float)
        (SP_NUM, Frequency(2.5)),
        # ratio(int) x freq(Fraction)
        (FrequencyRatio(5), Frequency(Fraction(7, 9))),
        # ratio(int, int) x freq(Fraction)
        (FrequencyRatio(5, 3), Frequency(Fraction(7, 9))),
        # ratio(float) x freq(Fraction)
        (FrequencyRatio(2.5), Frequency(Fraction(7, 9))),
        # ratio(Fraction) x freq(Fraction)
        (FrequencyRatio(Fraction(1, 2)), Frequency(Fraction(7, 9))),
        # ratio(SP_NUM) x freq(Fraction)
        (FrequencyRatio(SP_NUM), Frequency(Fraction(7, 9))),
        # int x freq(Fraction)
        (3, Frequency(Fraction(7, 9))),
        # float x freq(Fraction)
        (3.5, Frequency(Fraction(7, 9))),
        # fraction x freq(Fraction)
        (Fraction(7, 9), Frequency(Fraction(7, 9))),
        # SP_NUM x freq(Fraction)
        (SP_NUM, Frequency(Fraction(7, 9))),
        # ratio(int) x freq(SP_NUM)
        (FrequencyRatio(5), Frequency(SP_NUM)),
        # ratio(int, int) x freq(SP_NUM)
        (FrequencyRatio(5, 3), Frequency(SP_NUM)),
        # ratio(float) x freq(SP_NUM)
        (FrequencyRatio(2.5), Frequency(SP_NUM)),
        # ratio(Fraction) x freq(SP_NUM)
        (FrequencyRatio(Fraction(2, 3)), Frequency(SP_NUM)),
        # ratio(SP_NUM) x freq(SP_NUM)
        (FrequencyRatio(SP_NUM), Frequency(SP_NUM)),
        # int x freq(SP_NUM)
        (5, Frequency(SP_NUM)),
        # float x freq(SP_NUM)
        (2.5, Frequency(SP_NUM)),
        # fraction x freq(SP_NUM)
        (Fraction(3, 4), Frequency(SP_NUM)),
        # SP_NUM x freq(SP_NUM)
        (SP_NUM, Frequency(SP_NUM)),
        # other incompatible types
        (Frequency(2), 'abc'),
        (Frequency(2), SP_NON_NUMBER),
        (Frequency(2), complex(100, 3)),
        (Frequency(3.5), 'abc'),
        (Frequency(3.5), SP_NON_NUMBER),
        (Frequency(9.2), complex(100, 3)),
        (Frequency(Fraction(2, 3)), 'abc'),
        (Frequency(Fraction(2, 3)), SP_NON_NUMBER),
        (Frequency(Fraction(2, 3)), complex(100, 3)),
    ]
)
def test_truediv_type_error(a, b):
    with pytest.raises(TypeError):
        a / b


@pytest.mark.parametrize(
    'a, b, result',
    [
        # freq(int) x freq(int)
        (Frequency(3), Frequency(2), Frequency(1)),
        # freq(int) x freq(float)
        (Frequency(3), Frequency(2.5), Frequency(1)),
        # freq(float) x freq(int)
        (Frequency(3.5), Frequency(2), Frequency(1)),
        # freq(int) x freq(Fraction)
        (Frequency(4), Frequency(Fraction(3, 2)), Frequency(2)),
        # freq(Fraction) x freq(int)
        (Frequency(Fraction(5, 2)), Frequency(2), Frequency(1)),
        # freq(int) x freq(SP_NUM)
        (Frequency(3), Frequency(SP_NUM), Frequency(3 // SP_NUM)),
        # freq(SP_NUM) x freq(int)
        (Frequency(SP_NUM), Frequency(10), Frequency(SP_NUM // 10)),
        # freq(float) x freq(float)
        (Frequency(3.5), Frequency(2.5), Frequency(1)),
        # freq(float) x freq(Fraction)
        (Frequency(3.5), Frequency(Fraction(3, 2)), Frequency(2)),
        # freq(Fraction) x freq(float)
        (Frequency(Fraction(3, 2)), Frequency(0.5), Frequency(3)),
        # freq(float) x freq(SP_NUM)
        (Frequency(3.5), Frequency(SP_NUM), Frequency(3.5 // SP_NUM)),
        # freq(SP_NUM) x freq(float)
        (Frequency(SP_NUM), Frequency(1.5), Frequency(SP_NUM // 1.5)),
        # freq(Fraction) x freq(Fraction)
        (
            Frequency(Fraction(3, 2)),
            Frequency(Fraction(1, 5)),
            Frequency(7)
        ),
        # freq(Fraction) x freq(SP_NUM)
        (
            Frequency(Fraction(3, 2)),
            Frequency(SP_NUM),
            Frequency(Fraction(3, 2) // SP_NUM)
        ),
        # freq(SP_NUM) x freq(Fraction)
        (
            Frequency(SP_NUM),
            Frequency(Fraction(3, 2)),
            Frequency(SP_NUM // Fraction(3, 2))
        ),
        # freq(SP_NUM) x freq(SP_NUM)
        (Frequency(2 * SP_NUM), Frequency(SP_NUM), Frequency(2)),
    ]
)
def test_floordiv(a, b, result):
    assert isinstance(a // b, Frequency)
    assert a // b == result


@pytest.mark.parametrize(
    'a, b',
    [
        # freq(int) x ratio(int)
        (Frequency(5), FrequencyRatio(2)),
        # freq(int) x ratio(int, int)
        (Frequency(5), FrequencyRatio(2, 3)),
        # freq(int) x ratio(float)
        (Frequency(5), FrequencyRatio(3.5)),
        # freq(int) x ratio(Fraction)
        (Frequency(5), FrequencyRatio(Fraction(2, 3))),
        # freq(int) x ratio(SP_NUM)
        (Frequency(5), FrequencyRatio(SP_NUM)),
        # freq(int) x int
        (Frequency(5), 2),
        # freq(int) x float
        (Frequency(5), 3.5),
        # freq(int) x fraction
        (Frequency(5), Fraction(2, 3)),
        # freq(int) x SP_NUM
        (Frequency(5), SP_NUM),
        # freq(float) x ratio(int)
        (Frequency(5.4), FrequencyRatio(2)),
        # freq(float) x ratio(int, int)
        (Frequency(2.3), FrequencyRatio(2, 3)),
        # freq(float) x ratio(float)
        (Frequency(5.3), FrequencyRatio(3.5)),
        # freq(float) x ratio(Fraction)
        (Frequency(1.4), FrequencyRatio(Fraction(2, 3))),
        # freq(float) x ratio(SP_NUM)
        (Frequency(1.5), FrequencyRatio(SP_NUM)),
        # freq(float) x int
        (Frequency(5.2), 2),
        # freq(float) x float
        (Frequency(9.2), 2.5),
        # freq(float) x fraction
        (Frequency(1.2), Fraction(2, 3)),
        # freq(float) x SP_NUM
        (Frequency(3.2), SP_NUM),
        # freq(Fraction) x ratio(int)
        (Frequency(Fraction(2, 3)), FrequencyRatio(1)),
        # freq(Fraction) x ratio(int, int)
        (Frequency(Fraction(2, 3)), FrequencyRatio(1, 2)),
        # freq(Fraction) x ratio(float)
        (Frequency(Fraction(2, 3)), FrequencyRatio(3.5)),
        # freq(Fraction) x ratio(Fraction)
        (Frequency(Fraction(2, 3)), FrequencyRatio(Fraction(2, 3))),
        # freq(Fraction) x ratio(SP_NUM)
        (Frequency(Fraction(2, 3)), FrequencyRatio(SP_NUM)),
        # freq(Fraction) x int
        (Frequency(Fraction(2, 3)), 2),
        # freq(Fraction) x float
        (Frequency(Fraction(2, 3)), 2.3),
        # freq(Fraction) x fraction
        (Frequency(Fraction(2, 3)), Fraction(3, 4)),
        # freq(Fraction) x SP_NUM
        (Frequency(Fraction(2, 3)), SP_NUM),
        # freq(SP_NUM) x ratio(int)
        (Frequency(SP_NUM), FrequencyRatio(1)),
        # freq(SP_NUM) x ratio(int, int)
        (Frequency(SP_NUM), FrequencyRatio(1, 2)),
        # freq(SP_NUM) x ratio(float)
        (Frequency(SP_NUM), FrequencyRatio(4.3)),
        # freq(SP_NUM) x ratio(Fraction)
        (Frequency(SP_NUM), FrequencyRatio(Fraction(2, 3))),
        # freq(SP_NUM) x ratio(SP_NUM)
        (Frequency(SP_NUM), FrequencyRatio(SP_NUM)),
        # freq(SP_NUM) x int
        (Frequency(SP_NUM), 4),
        # freq(SP_NUM) x float
        (Frequency(SP_NUM), 4.2),
        # freq(SP_NUM) x fraction
        (Frequency(SP_NUM), Fraction(2, 3)),
        # freq(SP_NUM) x SP_NUM
        (Frequency(SP_NUM), SP_NUM),
        # other incompatible types
        (Frequency(2), 'abc'),
        (Frequency(2), SP_NON_NUMBER),
        (Frequency(2), complex(100, 3)),
        (Frequency(3.5), 'abc'),
        (Frequency(3.5), SP_NON_NUMBER),
        (Frequency(9.2), complex(100, 3)),
        (Frequency(Fraction(2, 3)), 'abc'),
        (Frequency(Fraction(2, 3)), SP_NON_NUMBER),
        (Frequency(Fraction(2, 3)), complex(100, 3)),
    ]
)
def test_floordiv_type_error(a, b):
    with pytest.raises(TypeError):
        a // b
    with pytest.raises(TypeError):
        b // a


@pytest.mark.parametrize(
    'a, result',
    [
        # freq(int)
        (Frequency(-2), Frequency(2)),
        (Frequency(5), Frequency(5)),
        # freq(float)
        (Frequency(-0.1), Frequency(0.1)),
        (Frequency(0.5), Frequency(0.5)),
        # freq(Fraction)
        (Frequency(Fraction(-1, 2)), Frequency(Fraction(1, 2))),
        (Frequency(Fraction(3, 4)), Frequency(Fraction(3, 4))),
        # freq(SP_NUM)
        (Frequency(- SP_NUM), Frequency(SP_NUM)),
        (Frequency(SP_NUM), Frequency(SP_NUM)),
    ]
)
def test_abs(a, result):
    assert isinstance(abs(a), Frequency)
    assert abs(a) == result


@pytest.mark.parametrize(
    'a, b, result',
    [
        # freq(int) x freq(int)
        (Frequency(3), Frequency(2), Frequency(1)),
        # freq(int) x freq(float)
        (Frequency(3), Frequency(2.5), Frequency(Fraction(1, 2))),
        # freq(float) x freq(int)
        (Frequency(3.5), Frequency(2), Frequency(Fraction(3, 2))),
        # freq(int) x freq(Fraction)
        (Frequency(4), Frequency(Fraction(3, 2)), Frequency(1)),
        # freq(Fraction) x freq(int)
        (Frequency(Fraction(5, 2)), Frequency(2), Frequency(Fraction(1, 2))),
        # freq(int) x freq(SP_NUM)
        (Frequency(3), Frequency(SP_NUM), Frequency(3 % SP_NUM)),
        # freq(SP_NUM) x freq(int)
        (Frequency(SP_NUM), Frequency(10), Frequency(SP_NUM % 10)),
        # freq(float) x freq(float)
        (Frequency(9.5), Frequency(2.5), Frequency(2)),
        # freq(float) x freq(Fraction)
        (Frequency(3.5), Frequency(Fraction(3, 2)), Frequency(Fraction(1, 2))),
        # freq(Fraction) x freq(float)
        (Frequency(Fraction(3, 2)), Frequency(0.5), Frequency(0)),
        # freq(float) x freq(SP_NUM)
        (
            Frequency(3.5),
            Frequency(SP_NUM),
            Frequency(Fraction(7, 2) % SP_NUM)
        ),
        # freq(SP_NUM) x freq(float)
        (Frequency(SP_NUM), Frequency(1.5), Frequency(SP_NUM % 1.5)),
        # freq(Fraction) x freq(Fraction)
        (
            Frequency(Fraction(3, 2)),
            Frequency(Fraction(1, 5)),
            Frequency(Fraction(1, 10))
        ),
        # freq(Fraction) x freq(SP_NUM)
        (
            Frequency(Fraction(3, 2)),
            Frequency(SP_NUM),
            Frequency(Fraction(3, 2) % SP_NUM)
        ),
        # freq(SP_NUM) x freq(Fraction)
        (
            Frequency(SP_NUM),
            Frequency(Fraction(3, 2)),
            Frequency(SP_NUM % Fraction(3, 2))
        ),
        # freq(SP_NUM) x freq(SP_NUM)
        (Frequency(2 * SP_NUM), Frequency(SP_NUM), Frequency(0)),
    ]
)
def test_mod(a, b, result):
    assert isinstance(a % b, Frequency)
    assert a % b == result


@pytest.mark.parametrize(
    'a, b',
    [
        # freq(int) x ratio(int)
        (Frequency(5), FrequencyRatio(2)),
        # freq(int) x ratio(int, int)
        (Frequency(5), FrequencyRatio(2, 3)),
        # freq(int) x ratio(float)
        (Frequency(5), FrequencyRatio(3.5)),
        # freq(int) x ratio(Fraction)
        (Frequency(5), FrequencyRatio(Fraction(2, 3))),
        # freq(int) x ratio(SP_NUM)
        (Frequency(5), FrequencyRatio(SP_NUM)),
        # freq(int) x int
        (Frequency(5), 2),
        # freq(int) x float
        (Frequency(5), 3.5),
        # freq(int) x fraction
        (Frequency(5), Fraction(2, 3)),
        # freq(int) x SP_NUM
        (Frequency(5), SP_NUM),
        # freq(float) x ratio(int)
        (Frequency(5.4), FrequencyRatio(2)),
        # freq(float) x ratio(int, int)
        (Frequency(2.3), FrequencyRatio(2, 3)),
        # freq(float) x ratio(float)
        (Frequency(5.3), FrequencyRatio(3.5)),
        # freq(float) x ratio(Fraction)
        (Frequency(1.4), FrequencyRatio(Fraction(2, 3))),
        # freq(float) x ratio(SP_NUM)
        (Frequency(1.5), FrequencyRatio(SP_NUM)),
        # freq(float) x int
        (Frequency(5.2), 2),
        # freq(float) x float
        (Frequency(9.2), 2.5),
        # freq(float) x fraction
        (Frequency(1.2), Fraction(2, 3)),
        # freq(float) x SP_NUM
        (Frequency(3.2), SP_NUM),
        # freq(Fraction) x ratio(int)
        (Frequency(Fraction(2, 3)), FrequencyRatio(1)),
        # freq(Fraction) x ratio(int, int)
        (Frequency(Fraction(2, 3)), FrequencyRatio(1, 2)),
        # freq(Fraction) x ratio(float)
        (Frequency(Fraction(2, 3)), FrequencyRatio(3.5)),
        # freq(Fraction) x ratio(Fraction)
        (Frequency(Fraction(2, 3)), FrequencyRatio(Fraction(2, 3))),
        # freq(Fraction) x ratio(SP_NUM)
        (Frequency(Fraction(2, 3)), FrequencyRatio(SP_NUM)),
        # freq(Fraction) x int
        (Frequency(Fraction(2, 3)), 2),
        # freq(Fraction) x float
        (Frequency(Fraction(2, 3)), 2.3),
        # freq(Fraction) x fraction
        (Frequency(Fraction(2, 3)), Fraction(3, 4)),
        # freq(Fraction) x SP_NUM
        (Frequency(Fraction(2, 3)), SP_NUM),
        # freq(SP_NUM) x ratio(int)
        (Frequency(SP_NUM), FrequencyRatio(1)),
        # freq(SP_NUM) x ratio(int, int)
        (Frequency(SP_NUM), FrequencyRatio(1, 2)),
        # freq(SP_NUM) x ratio(float)
        (Frequency(SP_NUM), FrequencyRatio(4.3)),
        # freq(SP_NUM) x ratio(Fraction)
        (Frequency(SP_NUM), FrequencyRatio(Fraction(2, 3))),
        # freq(SP_NUM) x ratio(SP_NUM)
        (Frequency(SP_NUM), FrequencyRatio(SP_NUM)),
        # freq(SP_NUM) x int
        (Frequency(SP_NUM), 4),
        # freq(SP_NUM) x float
        (Frequency(SP_NUM), 4.2),
        # freq(SP_NUM) x fraction
        (Frequency(SP_NUM), Fraction(2, 3)),
        # freq(SP_NUM) x SP_NUM
        (Frequency(SP_NUM), SP_NUM),
        # other incompatible types
        (Frequency(2), 'abc'),
        (Frequency(2), SP_NON_NUMBER),
        (Frequency(2), complex(100, 3)),
        (Frequency(3.5), 'abc'),
        (Frequency(3.5), SP_NON_NUMBER),
        (Frequency(9.2), complex(100, 3)),
        (Frequency(Fraction(2, 3)), 'abc'),
        (Frequency(Fraction(2, 3)), SP_NON_NUMBER),
        (Frequency(Fraction(2, 3)), complex(100, 3)),
    ]
)
def test_mod_type_error(a, b):
    with pytest.raises(TypeError):
        a % b
    with pytest.raises(TypeError):
        b % a


@pytest.mark.parametrize(
    'a, b',
    [
        # freq(int) x freq(int)
        (Frequency(3), Frequency(3)),
        # freq(int) x freq(float)
        (Frequency(3), Frequency(3.0)),
        # freq(int) x freq(Fraction)
        (Frequency(3), Frequency(Fraction(6, 2))),
        # freq(float) x freq(float)
        (Frequency(3.5), Frequency(3.5)),
        # freq(float) x freq(Fraction)
        (Frequency(0.5), Frequency(Fraction(1, 2))),
        # freq(Fraction) x freq(Fraction)
        (Frequency(Fraction(2, 4)), Frequency(Fraction(1, 2))),
        # freq(SP_NUM) x freq(SP_NUM)
        (Frequency(SP_NUM), Frequency(SP_NUM)),
    ]
)
def test_eq(a, b):
    assert a == b
    assert b == a


@pytest.mark.parametrize(
    'a, b',
    [
        # freq(int) x ratio(int)
        (Frequency(5), FrequencyRatio(5)),
        # freq(int) x ratio(int, int)
        (Frequency(5), FrequencyRatio(10, 2)),
        # freq(int) x ratio(float)
        (Frequency(5), FrequencyRatio(5.0)),
        # freq(int) x ratio(Fraction)
        (Frequency(5), FrequencyRatio(Fraction(10, 2))),
        # freq(int) x int
        (Frequency(5), 5),
        # freq(int) x float
        (Frequency(5), 5.0),
        # freq(int) x fraction
        (Frequency(5), Fraction(10, 2)),
        # freq(float) x ratio(int)
        (Frequency(5.0), FrequencyRatio(2)),
        # freq(float) x ratio(int, int)
        (Frequency(2.5), FrequencyRatio(5, 2)),
        # freq(float) x ratio(float)
        (Frequency(2.5), FrequencyRatio(2.5)),
        # freq(float) x ratio(Fraction)
        (Frequency(1.5), FrequencyRatio(Fraction(3, 2))),
        # freq(float) x int
        (Frequency(2.0), 2),
        # freq(float) x float
        (Frequency(2.5), 2.5),
        # freq(float) x fraction
        (Frequency(1.5), Fraction(3, 2)),
        # freq(Fraction) x ratio(int)
        (Frequency(Fraction(1, 1)), FrequencyRatio(1)),
        # freq(Fraction) x ratio(int, int)
        (Frequency(Fraction(2, 3)), FrequencyRatio(2, 3)),
        # freq(Fraction) x ratio(float)
        (Frequency(Fraction(7, 2)), FrequencyRatio(3.5)),
        # freq(Fraction) x ratio(Fraction)
        (Frequency(Fraction(2, 3)), FrequencyRatio(Fraction(2, 3))),
        # freq(Fraction) x int
        (Frequency(Fraction(2, 1)), 2),
        # freq(Fraction) x float
        (Frequency(Fraction(3, 2)), 1.5),
        # freq(Fraction) x fraction
        (Frequency(Fraction(2, 3)), Fraction(4, 6)),
        # freq(SP_NUM) x ratio(SP_NUM)
        (Frequency(SP_NUM), FrequencyRatio(SP_NUM)),
        # freq(SP_NUM) x SP_NUM
        (Frequency(SP_NUM), SP_NUM),
        # other incompatible types
        (Frequency(2), 'abc'),
        (Frequency(2), SP_NON_NUMBER),
        (Frequency(2), complex(100, 3)),
        (Frequency(3.5), 'abc'),
        (Frequency(3.5), SP_NON_NUMBER),
        (Frequency(9.2), complex(100, 3)),
        (Frequency(Fraction(2, 3)), 'abc'),
        (Frequency(Fraction(2, 3)), SP_NON_NUMBER),
        (Frequency(Fraction(2, 3)), complex(100, 3)),
    ]
)
def test_not_eq(a, b):
    assert a != b
    assert b != a


@pytest.mark.parametrize(
    'a, b',
    [
        # freq(int) x freq(int)
        (Frequency(2), Frequency(3)),
        # freq(int) x freq(float)
        (Frequency(2), Frequency(3.0)),
        # freq(int) x freq(Fraction)
        (Frequency(2), Frequency(Fraction(6, 2))),
        # freq(float) x freq(float)
        (Frequency(1.5), Frequency(3.5)),
        # freq(float) x freq(Fraction)
        (Frequency(0.1), Frequency(Fraction(1, 2))),
        # freq(Fraction) x freq(Fraction)
        (Frequency(Fraction(1, 4)), Frequency(Fraction(1, 2))),
        # freq(SP_NUM) x freq(SP_NUM)
        (Frequency(SP_NUM / 2), Frequency(SP_NUM)),
    ]
)
def test_lt(a, b):
    assert a < b
    assert b > a
    assert a != b
    assert b != a


@pytest.mark.parametrize(
    'a, b',
    [
        # freq(int) x ratio(int)
        (Frequency(5), FrequencyRatio(2)),
        # freq(int) x ratio(int, int)
        (Frequency(5), FrequencyRatio(2, 3)),
        # freq(int) x ratio(float)
        (Frequency(5), FrequencyRatio(3.5)),
        # freq(int) x ratio(Fraction)
        (Frequency(5), FrequencyRatio(Fraction(2, 3))),
        # freq(int) x ratio(SP_NUM)
        (Frequency(5), FrequencyRatio(SP_NUM)),
        # freq(int) x int
        (Frequency(5), 2),
        # freq(int) x float
        (Frequency(5), 3.5),
        # freq(int) x fraction
        (Frequency(5), Fraction(2, 3)),
        # freq(int) x SP_NUM
        (Frequency(5), SP_NUM),
        # freq(float) x ratio(int)
        (Frequency(5.4), FrequencyRatio(2)),
        # freq(float) x ratio(int, int)
        (Frequency(2.3), FrequencyRatio(2, 3)),
        # freq(float) x ratio(float)
        (Frequency(5.3), FrequencyRatio(3.5)),
        # freq(float) x ratio(Fraction)
        (Frequency(1.4), FrequencyRatio(Fraction(2, 3))),
        # freq(float) x ratio(SP_NUM)
        (Frequency(1.5), FrequencyRatio(SP_NUM)),
        # freq(float) x int
        (Frequency(5.2), 2),
        # freq(float) x float
        (Frequency(9.2), 2.5),
        # freq(float) x fraction
        (Frequency(1.2), Fraction(2, 3)),
        # freq(float) x SP_NUM
        (Frequency(3.2), SP_NUM),
        # freq(Fraction) x ratio(int)
        (Frequency(Fraction(2, 3)), FrequencyRatio(1)),
        # freq(Fraction) x ratio(int, int)
        (Frequency(Fraction(2, 3)), FrequencyRatio(1, 2)),
        # freq(Fraction) x ratio(float)
        (Frequency(Fraction(2, 3)), FrequencyRatio(3.5)),
        # freq(Fraction) x ratio(Fraction)
        (Frequency(Fraction(2, 3)), FrequencyRatio(Fraction(2, 3))),
        # freq(Fraction) x ratio(SP_NUM)
        (Frequency(Fraction(2, 3)), FrequencyRatio(SP_NUM)),
        # freq(Fraction) x int
        (Frequency(Fraction(2, 3)), 2),
        # freq(Fraction) x float
        (Frequency(Fraction(2, 3)), 2.3),
        # freq(Fraction) x fraction
        (Frequency(Fraction(2, 3)), Fraction(3, 4)),
        # freq(Fraction) x SP_NUM
        (Frequency(Fraction(2, 3)), SP_NUM),
        # freq(SP_NUM) x ratio(int)
        (Frequency(SP_NUM), FrequencyRatio(1)),
        # freq(SP_NUM) x ratio(int, int)
        (Frequency(SP_NUM), FrequencyRatio(1, 2)),
        # freq(SP_NUM) x ratio(float)
        (Frequency(SP_NUM), FrequencyRatio(4.3)),
        # freq(SP_NUM) x ratio(Fraction)
        (Frequency(SP_NUM), FrequencyRatio(Fraction(2, 3))),
        # freq(SP_NUM) x ratio(SP_NUM)
        (Frequency(SP_NUM), FrequencyRatio(SP_NUM)),
        # freq(SP_NUM) x int
        (Frequency(SP_NUM), 4),
        # freq(SP_NUM) x float
        (Frequency(SP_NUM), 4.2),
        # freq(SP_NUM) x fraction
        (Frequency(SP_NUM), Fraction(2, 3)),
        # freq(SP_NUM) x SP_NUM
        (Frequency(SP_NUM), SP_NUM),
        # other incompatible types
        (Frequency(2), 'abc'),
        (Frequency(2), SP_NON_NUMBER),
        (Frequency(2), complex(100, 3)),
        (Frequency(3.5), 'abc'),
        (Frequency(3.5), SP_NON_NUMBER),
        (Frequency(9.2), complex(100, 3)),
        (Frequency(Fraction(2, 3)), 'abc'),
        (Frequency(Fraction(2, 3)), SP_NON_NUMBER),
        (Frequency(Fraction(2, 3)), complex(100, 3)),
    ]
)
def test_lt_type_error(a, b):
    with pytest.raises(TypeError):
        assert a < b
    with pytest.raises(TypeError):
        assert b < a
    with pytest.raises(TypeError):
        assert a > b
    with pytest.raises(TypeError):
        assert b > a


@pytest.mark.parametrize(
    'freq',
    [
        Frequency(3),
        Frequency(3.4),
        Frequency(SP_NUM),
        Frequency(Fraction(3, 2)),
    ]
)
def test_float_type_error(freq):
    with pytest.raises(TypeError):
        # TODO: check error message
        float(freq)


@pytest.mark.parametrize(
    'freq, result',
    [
        (Frequency(3), 3.0),
        (Frequency(sp.Integer(3)**Fraction(10, 3)), 38.94073839830003),
        (Frequency(Fraction(3, 2)), 1.5),
    ]
)
def test_to_float(freq, result):
    assert freq.to_float() == result


@pytest.mark.parametrize(
    'freq, ndigits, result',
    [
        (Frequency(Fraction(1, 3)), 4, 0.3333),
        (Frequency(sp.Integer(3)**Fraction(10, 3)), 3, 38.941),
        (Frequency(Fraction(3, 2)), 0, 2.0),
    ]
)
def test_round(freq, ndigits, result):
    assert round(freq, ndigits) == result


@pytest.mark.parametrize(
    'freq, result',
    [
        (Frequency(3), 'Frequency(3)'),
        (Frequency(Fraction(3, 2)), 'Frequency(3/2)'),
        (Frequency(sp.Integer(2) ** sp.Rational(3, 2)),
         'Frequency(2*sqrt(2))'),
    ]
)
def test_repr(freq, result):
    assert repr(freq) == result


@pytest.mark.parametrize(
    'inconvertible',
    [
        True,
        complex(2, 3),
        'abc',
        SP_NON_NUMBER
    ]
)
def test_init_inconvertible(inconvertible):
    with pytest.raises(ValueError):
        Frequency(inconvertible)
