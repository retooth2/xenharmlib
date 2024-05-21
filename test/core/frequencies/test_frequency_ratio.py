import pytest
import sympy as sp
from fractions import Fraction
from xenharmlib.core.frequencies import Frequency
from xenharmlib.core.frequencies import FrequencyRatio

SP_NUM = sp.Integer(2) ** sp.Rational(1, 3)
SP_X, SP_Y = sp.symbols('x y')
SP_NON_NUMBER = SP_X**2*2*SP_Y

# all possible type pairs grouped by (possible) commutativity:

# ratio(int) x ratio(int)
# ratio(int) x ratio(int, int)
# ratio(int, int) x ratio(int)
# ratio(int) x ratio(float)
# ratio(float) x ratio(int)
# ratio(int) x ratio(Fraction)
# ratio(Fraction) x ratio(int)
# ratio(int) x ratio(SP_NUM)
# ratio(SP_NUM) x ratio(int)
# ratio(int) x int
# int x ratio(int)
# ratio(int) x float
# float x ratio(int)
# ratio(int) x fraction
# fraction x ratio(int)
# ratio(int) x SP_NUM
# SP_NUM x ratio(int)

# ratio(int, int) x ratio(int, int)
# ratio(int, int) x ratio(float)
# ratio(float) x ratio(int, int)
# ratio(int, int) x ratio(Fraction)
# ratio(Fraction) x ratio(int, int)
# ratio(int, int) x ratio(SP_NUM)
# ratio(SP_NUM) x ratio(int, int)
# ratio(int, int) x int
# int x ratio(int, int)
# ratio(int, int) x float
# float x ratio(int, int)
# ratio(int, int) x fraction
# fraction x ratio(int, int)
# ratio(int, int) x SP_NUM
# SP_NUM x ratio(int, int)

# ratio(float) x ratio(float)
# ratio(float) x ratio(Fraction)
# ratio(Fraction) x ratio(float)
# ratio(float) x ratio(SP_NUM)
# ratio(SP_NUM) x ratio(float)
# ratio(float) x int
# int x ratio(float)
# ratio(float) x float
# float x ratio(float)
# ratio(float) x fraction
# fraction x ratio(float)
# ratio(float) x SP_NUM
# SP_NUM x ratio(float)

# ratio(Fraction) x ratio(Fraction)
# ratio(Fraction) x ratio(SP_NUM)
# ratio(SP_NUM) x ratio(Fraction)
# ratio(Fraction) x int
# int x ratio(Fraction)
# ratio(Fraction) x float
# float x ratio(Fraction)
# ratio(Fraction) x fraction
# fraction x ratio(Fraction)
# ratio(Fraction) x SP_NUM
# SP_NUM x ratio(Fraction)

# ratio(SP_NUM) x ratio(SP_NUM)
# ratio(SP_NUM) x int
# int x ratio(SP_NUM)
# ratio(SP_NUM) x float
# float x ratio(SP_NUM)
# ratio(SP_NUM) x fraction
# fraction x ratio(SP_NUM)
# ratio(SP_NUM) x SP_NUM
# SP_NUM x ratio(SP_NUM)


@pytest.mark.parametrize(
    'x, y, result',
    [
        # ratio(int) x ratio(int)
        (FrequencyRatio(3), FrequencyRatio(2), FrequencyRatio(5)),
        # ratio(int) x ratio(int, int)
        (FrequencyRatio(1, 3), FrequencyRatio(2), FrequencyRatio(7, 3)),
        # ratio(int) x ratio(float)
        (FrequencyRatio(3), FrequencyRatio(4.0), FrequencyRatio(7)),
        # ratio(int) x ratio(Fraction)
        (
            FrequencyRatio(1),
            FrequencyRatio(Fraction(1, 2)),
            FrequencyRatio(3, 2)
        ),
        # ratio(int) x ratio(SP_NUM)
        (
            FrequencyRatio(9),
            FrequencyRatio(SP_NUM),
            FrequencyRatio(9 + SP_NUM)
        ),
        # ratio(int) x int
        (FrequencyRatio(22), 9, FrequencyRatio(31)),
        # ratio(int) x float
        (FrequencyRatio(22), 0.5, FrequencyRatio(45, 2)),
        # ratio(int) x fraction
        (FrequencyRatio(33), Fraction(2, 3), FrequencyRatio(101, 3)),
        # ratio(int) x SP_NUM
        (FrequencyRatio(31), SP_NUM, FrequencyRatio(31 + SP_NUM)),
        # ---------------------------------------------------------------------
        # ratio(int, int) x ratio(int, int)
        (FrequencyRatio(1, 3), FrequencyRatio(2, 3), FrequencyRatio(1)),
        # ratio(int, int) x ratio(float)
        (FrequencyRatio(1, 2), FrequencyRatio(2.5), FrequencyRatio(3)),
        # ratio(int, int) x ratio(Fraction)
        (
            FrequencyRatio(1, 3),
            FrequencyRatio(Fraction(1, 6)),
            FrequencyRatio(1, 2)
        ),
        # ratio(int, int) x ratio(SP_NUM)
        (
            FrequencyRatio(1, 3),
            FrequencyRatio(SP_NUM),
            FrequencyRatio(SP_NUM + Fraction(1, 3))
        ),
        # ratio(int, int) x int
        (FrequencyRatio(1, 3), 3, FrequencyRatio(10, 3)),
        # ratio(int, int) x float
        (FrequencyRatio(1, 3), 0.5, FrequencyRatio(5, 6)),
        # ratio(int, int) x fraction
        (FrequencyRatio(1, 3), Fraction(1, 6), FrequencyRatio(1, 2)),
        # ratio(int, int) x SP_NUM
        (
            FrequencyRatio(1, 3),
            SP_NUM,
            FrequencyRatio(SP_NUM + Fraction(1, 3))
        ),
        # ---------------------------------------------------------------------
        # ratio(float) x ratio(float)
        (FrequencyRatio(0.5), FrequencyRatio(2.5), FrequencyRatio(3)),
        # ratio(float) x ratio(Fraction)
        (
            FrequencyRatio(0.5),
            FrequencyRatio(Fraction(1, 6)),
            FrequencyRatio(2, 3)
        ),
        # ratio(float) x ratio(SP_NUM)
        (
            FrequencyRatio(0.5),
            FrequencyRatio(SP_NUM),
            FrequencyRatio(SP_NUM + Fraction(1, 2))
        ),
        # ratio(float) x int
        (
            FrequencyRatio(0.5), 2, FrequencyRatio(5, 2)
        ),
        # ratio(float) x float
        (
            FrequencyRatio(0.5), 0.25, FrequencyRatio(3, 4)
        ),
        # ratio(float) x fraction
        (
            FrequencyRatio(0.25), Fraction(3, 4), FrequencyRatio(1)
        ),
        (
            FrequencyRatio(0.25),
            SP_NUM,
            FrequencyRatio(SP_NUM + Fraction(1, 4))
        ),
        # ---------------------------------------------------------------------
        # ratio(Fraction) x ratio(Fraction)
        (
            FrequencyRatio(Fraction(1, 3)),
            FrequencyRatio(Fraction(4, 3)),
            FrequencyRatio(5, 3)
        ),
        # ratio(Fraction) x ratio(SP_NUM)
        (
            FrequencyRatio(Fraction(2, 3)),
            FrequencyRatio(SP_NUM),
            FrequencyRatio(SP_NUM + Fraction(2, 3))
        ),
        # ratio(Fraction) x int
        (FrequencyRatio(Fraction(1, 3)), 3, FrequencyRatio(10, 3)),
        # ratio(Fraction) x float
        (FrequencyRatio(Fraction(1, 3)), 1.5, FrequencyRatio(11, 6)),
        # ratio(Fraction) x fraction
        (
            FrequencyRatio(Fraction(1, 3)),
            Fraction(5, 2),
            FrequencyRatio(17, 6)
        ),
        # ratio(Fraction) x SP_NUM
        (
            FrequencyRatio(Fraction(1, 3)),
            SP_NUM,
            FrequencyRatio(SP_NUM + Fraction(1, 3))
        ),
        # ---------------------------------------------------------------------
        # ratio(SP_NUM) x ratio(SP_NUM)
        (
            FrequencyRatio(SP_NUM),
            FrequencyRatio(SP_NUM),
            FrequencyRatio(SP_NUM + SP_NUM)
        ),
        # ratio(SP_NUM) x int
        (FrequencyRatio(SP_NUM), 3, FrequencyRatio(3 + SP_NUM)),
        # ratio(SP_NUM) x float
        (FrequencyRatio(SP_NUM), 0.5, FrequencyRatio(SP_NUM + Fraction(1, 2))),
        # ratio(SP_NUM) x fraction
        (
            FrequencyRatio(SP_NUM),
            Fraction(1, 3),
            FrequencyRatio(SP_NUM + Fraction(1, 3))
        ),
        # ratio(SP_NUM) x SP_NUM
        (
            FrequencyRatio(SP_NUM),
            SP_NUM,
            FrequencyRatio(SP_NUM + SP_NUM)
        ),
    ]
)
def test_add(x, y, result):
    assert isinstance(x + y, FrequencyRatio)
    assert isinstance(y + x, FrequencyRatio)
    assert x + y == result
    assert y + x == result


@pytest.mark.parametrize(
    'x, y',
    [
        (FrequencyRatio(1, 2), 'abc'),
        (FrequencyRatio(1, 2), SP_NON_NUMBER),
        (FrequencyRatio(1, 2), Frequency(100)),
        (FrequencyRatio(1, 2), complex(100, 3)),
        (FrequencyRatio(3), 'abc'),
        (FrequencyRatio(3), SP_NON_NUMBER),
        (FrequencyRatio(5), Frequency(100)),
        (FrequencyRatio(6), complex(100, 3)),
        (FrequencyRatio(3.5), 'abc'),
        (FrequencyRatio(3.5), SP_NON_NUMBER),
        (FrequencyRatio(2.1), Frequency(100)),
        (FrequencyRatio(9.2), complex(100, 3)),
    ]
)
def test_add_bogus(x, y):

    with pytest.raises(TypeError):
        x + y

    with pytest.raises(TypeError):
        y + x


@pytest.mark.parametrize(
    'x, y, result',
    [
        # ratio(int) x ratio(int)
        (FrequencyRatio(3), FrequencyRatio(2), FrequencyRatio(1)),
        # ratio(int) x ratio(int, int)
        (FrequencyRatio(4), FrequencyRatio(1, 2), FrequencyRatio(7, 2)),
        # ratio(int, int) x ratio(int)
        (FrequencyRatio(4, 3), FrequencyRatio(1, 3), FrequencyRatio(1)),
        # ratio(int) x ratio(float)
        (FrequencyRatio(1), FrequencyRatio(0.5), FrequencyRatio(1, 2)),
        # ratio(float) x ratio(int)
        (FrequencyRatio(9.5), FrequencyRatio(1), FrequencyRatio(17, 2)),
        # ratio(int) x ratio(Fraction)
        (
            FrequencyRatio(4),
            FrequencyRatio(Fraction(1, 3)),
            FrequencyRatio(11, 3)
        ),
        # ratio(Fraction) x ratio(int)
        (
            FrequencyRatio(Fraction(5, 2)),
            FrequencyRatio(1),
            FrequencyRatio(3, 2)
        ),
        # ratio(int) x ratio(SP_NUM)
        (
            FrequencyRatio(80),
            FrequencyRatio(SP_NUM),
            FrequencyRatio(80 - SP_NUM)
        ),
        # ratio(SP_NUM) x ratio(int)
        (
            FrequencyRatio(SP_NUM),
            FrequencyRatio(3),
            FrequencyRatio(SP_NUM - 3)
        ),
        # ratio(int) x int
        (FrequencyRatio(4), 3, FrequencyRatio(1)),
        # int x ratio(int)
        (5, FrequencyRatio(2), FrequencyRatio(3)),
        # ratio(int) x float
        (FrequencyRatio(2), 1.5, FrequencyRatio(1, 2)),
        # float x ratio(int)
        (3.5, FrequencyRatio(1), FrequencyRatio(5, 2)),
        # ratio(int) x fraction
        (FrequencyRatio(4), Fraction(2, 3), FrequencyRatio(10, 3)),
        # fraction x ratio(int)
        (Fraction(5, 3), FrequencyRatio(1), FrequencyRatio(2, 3)),
        # ratio(int) x SP_NUM
        (FrequencyRatio(10), SP_NUM, FrequencyRatio(10 - SP_NUM)),
        # SP_NUM x ratio(int)
        (SP_NUM, FrequencyRatio(2), FrequencyRatio(SP_NUM) - 2),
        # ratio(int, int) x ratio(int, int)
        (FrequencyRatio(2, 3), FrequencyRatio(1, 5), FrequencyRatio(7, 15)),
        # ratio(int, int) x ratio(float)
        (FrequencyRatio(2, 3), FrequencyRatio(0.5), FrequencyRatio(1, 6)),
        # ratio(float) x ratio(int, int)
        (FrequencyRatio(0.5), FrequencyRatio(1, 3), FrequencyRatio(1, 6)),
        # ratio(int, int) x ratio(Fraction)
        (
            FrequencyRatio(5, 2),
            FrequencyRatio(Fraction(1, 2)),
            FrequencyRatio(2)
        ),
        # ratio(Fraction) x ratio(int, int)
        (
            FrequencyRatio(Fraction(11, 2)),
            FrequencyRatio(5, 2),
            FrequencyRatio(3)
        ),
        # ratio(int, int) x ratio(SP_NUM)
        (
            FrequencyRatio(5, 2),
            FrequencyRatio(SP_NUM),
            FrequencyRatio(Fraction(5, 2) - SP_NUM)
        ),
        # ratio(SP_NUM) x ratio(int, int)
        (
            FrequencyRatio(SP_NUM),
            FrequencyRatio(5, 2),
            FrequencyRatio(SP_NUM - Fraction(5, 2))
        ),
        # ratio(int, int) x int
        (FrequencyRatio(4, 3), 1, FrequencyRatio(1, 3)),
        # int x ratio(int, int)
        (2, FrequencyRatio(4, 3), FrequencyRatio(2, 3)),
        # ratio(int, int) x float
        (FrequencyRatio(5, 3), 1.5, FrequencyRatio(1, 6)),
        # float x ratio(int, int)
        (5.5, FrequencyRatio(1, 2), FrequencyRatio(5)),
        # ratio(int, int) x fraction
        (FrequencyRatio(5, 2), Fraction(3, 2), FrequencyRatio(1)),
        # fraction x ratio(int, int)
        (Fraction(10, 2), FrequencyRatio(5, 2), FrequencyRatio(5, 2)),
        # ratio(int, int) x SP_NUM
        (
            FrequencyRatio(10, 2),
            SP_NUM,
            FrequencyRatio(Fraction(10, 2) - SP_NUM)
        ),
        # SP_NUM x ratio(int, int)
        (
            SP_NUM,
            FrequencyRatio(10, 2),
            FrequencyRatio(SP_NUM - Fraction(10, 2)),
        ),
        # ratio(float) x ratio(float)
        (
            FrequencyRatio(10.5),
            FrequencyRatio(4.5),
            FrequencyRatio(6),
        ),
        # ratio(float) x ratio(Fraction)
        (
            FrequencyRatio(6.5),
            FrequencyRatio(Fraction(3, 2)),
            FrequencyRatio(5),
        ),
        # ratio(Fraction) x ratio(float)
        (
            FrequencyRatio(Fraction(3, 2)),
            FrequencyRatio(0.5),
            FrequencyRatio(1),
        ),
        # ratio(float) x ratio(SP_NUM)
        (
            FrequencyRatio(6.5),
            FrequencyRatio(SP_NUM),
            FrequencyRatio(Fraction(13, 2) - SP_NUM),
        ),
        # ratio(SP_NUM) x ratio(float)
        (
            FrequencyRatio(SP_NUM),
            FrequencyRatio(6.5),
            FrequencyRatio(SP_NUM - Fraction(13, 2)),
        ),
        # ratio(float) x int
        (FrequencyRatio(1.5), 1, FrequencyRatio(1, 2)),
        # int x ratio(float)
        (3, FrequencyRatio(1.5), FrequencyRatio(3, 2)),
        # ratio(float) x float
        (FrequencyRatio(1.5), 0.5, FrequencyRatio(1)),
        # float x ratio(float)
        (2.5, FrequencyRatio(1.5), FrequencyRatio(1)),
        # ratio(float) x fraction
        (FrequencyRatio(1.5), Fraction(1, 2), FrequencyRatio(1)),
        # fraction x ratio(float)
        (Fraction(4, 3), FrequencyRatio(0.5), FrequencyRatio(5, 6)),
        # ratio(float) x SP_NUM
        (FrequencyRatio(1.5), SP_NUM, FrequencyRatio(Fraction(3, 2) - SP_NUM)),
        # SP_NUM x ratio(float)
        (SP_NUM, FrequencyRatio(1.5), FrequencyRatio(SP_NUM - Fraction(3, 2))),
        # ratio(Fraction) x ratio(Fraction)
        (
            FrequencyRatio(Fraction(10, 3)),
            FrequencyRatio(Fraction(5, 3)),
            FrequencyRatio(5, 3)
        ),
        # ratio(Fraction) x ratio(SP_NUM)
        (
            FrequencyRatio(Fraction(10, 3)),
            SP_NUM,
            FrequencyRatio(Fraction(10, 3) - SP_NUM)
        ),
        # ratio(SP_NUM) x ratio(Fraction)
        (
            SP_NUM,
            FrequencyRatio(Fraction(10, 3)),
            FrequencyRatio(SP_NUM - Fraction(10, 3))
        ),
        # ratio(Fraction) x int
        (FrequencyRatio(Fraction(10, 3)), 3, FrequencyRatio(1, 3)),
        # int x ratio(Fraction)
        (4, FrequencyRatio(Fraction(10, 3)), FrequencyRatio(2, 3)),
        # ratio(Fraction) x float
        (FrequencyRatio(Fraction(11, 2)), 0.5, FrequencyRatio(5)),
        # float x ratio(Fraction)
        (6.5, FrequencyRatio(Fraction(11, 2)), FrequencyRatio(1)),
        # ratio(Fraction) x fraction
        (
            FrequencyRatio(Fraction(10, 3)),
            Fraction(1, 2),
            FrequencyRatio(17, 6)
        ),
        # fraction x ratio(Fraction)
        (
            Fraction(31, 3),
            FrequencyRatio(Fraction(10, 3)),
            FrequencyRatio(7)
        ),
        # ratio(Fraction) x SP_NUM
        (
            FrequencyRatio(Fraction(10, 3)),
            SP_NUM,
            FrequencyRatio(Fraction(10, 3) - SP_NUM)
        ),
        # SP_NUM x ratio(Fraction)
        (
            SP_NUM,
            FrequencyRatio(Fraction(10, 3)),
            FrequencyRatio(SP_NUM - Fraction(10, 3))
        ),
        # ratio(SP_NUM) x ratio(SP_NUM)
        (
            FrequencyRatio(2 * SP_NUM),
            FrequencyRatio(SP_NUM),
            FrequencyRatio(SP_NUM)
        ),
        # ratio(SP_NUM) x int
        (FrequencyRatio(SP_NUM), 3, FrequencyRatio(SP_NUM - 3)),
        # int x ratio(SP_NUM)
        (3, FrequencyRatio(SP_NUM), FrequencyRatio(3 - SP_NUM)),
        # ratio(SP_NUM) x float
        (FrequencyRatio(SP_NUM), 1.5, FrequencyRatio(SP_NUM - Fraction(3, 2))),
        # float x ratio(SP_NUM)
        (1.5, FrequencyRatio(SP_NUM), FrequencyRatio(Fraction(3, 2) - SP_NUM)),
        # ratio(SP_NUM) x fraction
        (
            FrequencyRatio(SP_NUM),
            Fraction(5, 7),
            FrequencyRatio(SP_NUM - Fraction(5, 7))
        ),
        # fraction x ratio(SP_NUM)
        (
            Fraction(5, 7),
            FrequencyRatio(SP_NUM),
            FrequencyRatio(Fraction(5, 7) - SP_NUM)
        ),
        # ratio(SP_NUM) x SP_NUM
        (FrequencyRatio(2 * SP_NUM), SP_NUM, FrequencyRatio(SP_NUM)),
        # SP_NUM x ratio(SP_NUM)
        (2 * SP_NUM, FrequencyRatio(SP_NUM), FrequencyRatio(SP_NUM)),
    ]
)
def test_sub(x, y, result):
    assert isinstance(x - y, FrequencyRatio)
    assert x - y == result


@pytest.mark.parametrize(
    'x, y',
    [
        (FrequencyRatio(1, 2), 'abc'),
        (FrequencyRatio(1, 2), SP_NON_NUMBER),
        (FrequencyRatio(1, 2), Frequency(100)),
        (FrequencyRatio(1, 2), complex(100, 3)),
        (FrequencyRatio(3), 'abc'),
        (FrequencyRatio(3), SP_NON_NUMBER),
        (FrequencyRatio(5), Frequency(100)),
        (FrequencyRatio(6), complex(100, 3)),
        (FrequencyRatio(3.5), 'abc'),
        (FrequencyRatio(3.5), SP_NON_NUMBER),
        (FrequencyRatio(2.1), Frequency(100)),
        (FrequencyRatio(9.2), complex(100, 3)),
    ]
)
def test_sub_bogus(x, y):

    with pytest.raises(TypeError):
        x - y

    with pytest.raises(TypeError):
        y - x


@pytest.mark.parametrize(
    'x, y, result',
    [
        # ratio(int) x ratio(int)
        (FrequencyRatio(3), FrequencyRatio(2), FrequencyRatio(6)),
        # ratio(int) x ratio(int, int)
        (FrequencyRatio(1, 3), FrequencyRatio(2), FrequencyRatio(2, 3)),
        # ratio(int) x ratio(float)
        (FrequencyRatio(3), FrequencyRatio(4.0), FrequencyRatio(12)),
        # ratio(int) x ratio(Fraction)
        (
            FrequencyRatio(1),
            FrequencyRatio(Fraction(1, 2)),
            FrequencyRatio(1, 2)
        ),
        # ratio(int) x ratio(SP_NUM)
        (
            FrequencyRatio(9),
            FrequencyRatio(SP_NUM),
            FrequencyRatio(9 * SP_NUM)
        ),
        # ratio(int) x int
        (FrequencyRatio(2), 9, FrequencyRatio(18)),
        # ratio(int) x float
        (FrequencyRatio(22), 0.5, FrequencyRatio(11)),
        # ratio(int) x fraction
        (FrequencyRatio(99), Fraction(2, 3), FrequencyRatio(66)),
        # ratio(int) x SP_NUM
        (FrequencyRatio(31), SP_NUM, FrequencyRatio(31 * SP_NUM)),
        # ---------------------------------------------------------------------
        # ratio(int, int) x ratio(int, int)
        (FrequencyRatio(1, 3), FrequencyRatio(2, 3), FrequencyRatio(2, 9)),
        # ratio(int, int) x ratio(float)
        (FrequencyRatio(1, 2), FrequencyRatio(2.5), FrequencyRatio(5, 4)),
        # ratio(int, int) x ratio(Fraction)
        (
            FrequencyRatio(1, 3),
            FrequencyRatio(Fraction(3, 4)),
            FrequencyRatio(1, 4)
        ),
        # ratio(int, int) x ratio(SP_NUM)
        (
            FrequencyRatio(1, 3),
            FrequencyRatio(SP_NUM),
            FrequencyRatio(SP_NUM * Fraction(1, 3))
        ),
        # ratio(int, int) x int
        (FrequencyRatio(1, 3), 3, FrequencyRatio(1)),
        # ratio(int, int) x float
        (FrequencyRatio(1, 3), 0.5, FrequencyRatio(1, 6)),
        # ratio(int, int) x fraction
        (FrequencyRatio(1, 3), Fraction(1, 6), FrequencyRatio(1, 18)),
        # ratio(int, int) x SP_NUM
        (
            FrequencyRatio(1, 3),
            SP_NUM,
            FrequencyRatio(SP_NUM * Fraction(1, 3))
        ),
        # ---------------------------------------------------------------------
        # ratio(float) x ratio(float)
        (FrequencyRatio(0.5), FrequencyRatio(2.5), FrequencyRatio(5, 4)),
        # ratio(float) x ratio(Fraction)
        (
            FrequencyRatio(0.5),
            FrequencyRatio(Fraction(1, 6)),
            FrequencyRatio(1, 12)
        ),
        # ratio(float) x ratio(SP_NUM)
        (
            FrequencyRatio(0.5),
            FrequencyRatio(SP_NUM),
            FrequencyRatio(SP_NUM * Fraction(1, 2))
        ),
        # ratio(float) x int
        (
            FrequencyRatio(0.5), 2, FrequencyRatio(1)
        ),
        # ratio(float) x float
        (
            FrequencyRatio(0.5), 0.25, FrequencyRatio(1, 8)
        ),
        # ratio(float) x fraction
        (
            FrequencyRatio(0.25), Fraction(3, 4), FrequencyRatio(3, 16)
        ),
        (
            FrequencyRatio(0.25),
            SP_NUM,
            FrequencyRatio(SP_NUM * Fraction(1, 4))
        ),
        # ---------------------------------------------------------------------
        # ratio(Fraction) x ratio(Fraction)
        (
            FrequencyRatio(Fraction(1, 3)),
            FrequencyRatio(Fraction(4, 3)),
            FrequencyRatio(4, 9)
        ),
        # ratio(Fraction) x ratio(SP_NUM)
        (
            FrequencyRatio(Fraction(2, 3)),
            FrequencyRatio(SP_NUM),
            FrequencyRatio(SP_NUM * Fraction(2, 3))
        ),
        # ratio(Fraction) x int
        (FrequencyRatio(Fraction(1, 3)), 3, FrequencyRatio(1)),
        # ratio(Fraction) x float
        (FrequencyRatio(Fraction(1, 3)), 1.5, FrequencyRatio(1, 2)),
        # ratio(Fraction) x fraction
        (
            FrequencyRatio(Fraction(1, 3)),
            Fraction(5, 2),
            FrequencyRatio(5, 6)
        ),
        # ratio(Fraction) x SP_NUM
        (
            FrequencyRatio(Fraction(1, 3)),
            SP_NUM,
            FrequencyRatio(SP_NUM * Fraction(1, 3))
        ),
        # ---------------------------------------------------------------------
        # ratio(SP_NUM) x ratio(SP_NUM)
        (
            FrequencyRatio(SP_NUM),
            FrequencyRatio(SP_NUM),
            FrequencyRatio(SP_NUM * SP_NUM)
        ),
        # ratio(SP_NUM) x int
        (FrequencyRatio(SP_NUM), 3, FrequencyRatio(3 * SP_NUM)),
        # ratio(SP_NUM) x float
        (FrequencyRatio(SP_NUM), 0.5, FrequencyRatio(SP_NUM * Fraction(1, 2))),
        # ratio(SP_NUM) x fraction
        (
            FrequencyRatio(SP_NUM),
            Fraction(1, 3),
            FrequencyRatio(SP_NUM * Fraction(1, 3))
        ),
        # ratio(SP_NUM) x SP_NUM
        (
            FrequencyRatio(SP_NUM),
            SP_NUM,
            FrequencyRatio(SP_NUM * SP_NUM)
        ),
    ]
)
def test_mul(x, y, result):
    assert x * y == result
    assert y * x == result


@pytest.mark.parametrize(
    'x, y',
    [
        (FrequencyRatio(1, 2), 'abc'),
        (FrequencyRatio(1, 2), complex(100, 3)),
        (FrequencyRatio(1, 2), SP_NON_NUMBER),
        (FrequencyRatio(3), 'abc'),
        (FrequencyRatio(6), complex(100, 3)),
        (FrequencyRatio(2), SP_NON_NUMBER),
        (FrequencyRatio(3.5), 'abc'),
        (FrequencyRatio(9.2), complex(100, 3)),
        (FrequencyRatio(2.4), SP_NON_NUMBER),
    ]
)
def test_mul_bogus(x, y):

    with pytest.raises(TypeError):
        x * y

    with pytest.raises(TypeError):
        y * x


@pytest.mark.parametrize(
    'x, y, result',
    [
        # ratio(int) x ratio(int)
        (FrequencyRatio(3), FrequencyRatio(2), FrequencyRatio(3, 2)),
        # ratio(int) x ratio(int, int)
        (FrequencyRatio(4), FrequencyRatio(1, 2), FrequencyRatio(8)),
        # ratio(int, int) x ratio(int)
        (FrequencyRatio(4, 3), FrequencyRatio(1, 3), FrequencyRatio(4)),
        # ratio(int) x ratio(float)
        (FrequencyRatio(1), FrequencyRatio(0.5), FrequencyRatio(2)),
        # ratio(float) x ratio(int)
        (FrequencyRatio(9.5), FrequencyRatio(2), FrequencyRatio(19, 4)),
        # ratio(int) x ratio(Fraction)
        (
            FrequencyRatio(4),
            FrequencyRatio(Fraction(1, 3)),
            FrequencyRatio(12)
        ),
        # ratio(Fraction) x ratio(int)
        (
            FrequencyRatio(Fraction(5, 2)),
            FrequencyRatio(9),
            FrequencyRatio(5, 18)
        ),
        # ratio(int) x ratio(SP_NUM)
        (
            FrequencyRatio(80),
            FrequencyRatio(SP_NUM),
            FrequencyRatio(80 / SP_NUM)
        ),
        # ratio(SP_NUM) x ratio(int)
        (
            FrequencyRatio(SP_NUM),
            FrequencyRatio(3),
            FrequencyRatio(SP_NUM / 3)
        ),
        # ratio(int) x int
        (FrequencyRatio(4), 3, FrequencyRatio(4, 3)),
        # int x ratio(int)
        (5, FrequencyRatio(2), FrequencyRatio(5, 2)),
        # ratio(int) x float
        (FrequencyRatio(2), 1.5, FrequencyRatio(4, 3)),
        # float x ratio(int)
        (3.5, FrequencyRatio(2), FrequencyRatio(7, 4)),
        # ratio(int) x fraction
        (FrequencyRatio(4), Fraction(2, 3), FrequencyRatio(6)),
        # fraction x ratio(int)
        (Fraction(5, 3), FrequencyRatio(9), FrequencyRatio(5, 27)),
        # ratio(int) x SP_NUM
        (FrequencyRatio(10), SP_NUM, FrequencyRatio(10 / SP_NUM)),
        # SP_NUM x ratio(int)
        (SP_NUM, FrequencyRatio(2), FrequencyRatio(SP_NUM) / 2),
        # ratio(int, int) x ratio(int, int)
        (FrequencyRatio(2, 3), FrequencyRatio(1, 5), FrequencyRatio(10, 3)),
        # ratio(int, int) x ratio(float)
        (FrequencyRatio(2, 3), FrequencyRatio(0.5), FrequencyRatio(4, 3)),
        # ratio(float) x ratio(int, int)
        (FrequencyRatio(0.5), FrequencyRatio(1, 3), FrequencyRatio(3, 2)),
        # ratio(int, int) x ratio(Fraction)
        (
            FrequencyRatio(5, 2),
            FrequencyRatio(Fraction(1, 2)),
            FrequencyRatio(5)
        ),
        # ratio(Fraction) x ratio(int, int)
        (
            FrequencyRatio(Fraction(11, 2)),
            FrequencyRatio(5, 2),
            FrequencyRatio(11, 5)
        ),
        # ratio(int, int) x ratio(SP_NUM)
        (
            FrequencyRatio(5, 2),
            FrequencyRatio(SP_NUM),
            FrequencyRatio(Fraction(5, 2) / SP_NUM)
        ),
        # ratio(SP_NUM) x ratio(int, int)
        (
            FrequencyRatio(SP_NUM),
            FrequencyRatio(5, 2),
            FrequencyRatio(SP_NUM / Fraction(5, 2))
        ),
        # ratio(int, int) x int
        (FrequencyRatio(4, 3), 7, FrequencyRatio(4, 21)),
        # int x ratio(int, int)
        (2, FrequencyRatio(4, 3), FrequencyRatio(3, 2)),
        # ratio(int, int) x float
        (FrequencyRatio(5, 3), 1.5, FrequencyRatio(10, 9)),
        # float x ratio(int, int)
        (5.5, FrequencyRatio(1, 2), FrequencyRatio(11)),
        # ratio(int, int) x fraction
        (FrequencyRatio(5, 2), Fraction(3, 2), FrequencyRatio(5, 3)),
        # fraction x ratio(int, int)
        (Fraction(10, 2), FrequencyRatio(5, 2), FrequencyRatio(2)),
        # ratio(int, int) x SP_NUM
        (
            FrequencyRatio(10, 2),
            SP_NUM,
            FrequencyRatio(Fraction(10, 2) / SP_NUM)
        ),
        # SP_NUM x ratio(int, int)
        (
            SP_NUM,
            FrequencyRatio(10, 2),
            FrequencyRatio(SP_NUM / Fraction(10, 2)),
        ),
        # ratio(float) x ratio(float)
        (
            FrequencyRatio(10.5),
            FrequencyRatio(4.5),
            FrequencyRatio(7, 3),
        ),
        # ratio(float) x ratio(Fraction)
        (
            FrequencyRatio(6.5),
            FrequencyRatio(Fraction(3, 2)),
            FrequencyRatio(13, 3),
        ),
        # ratio(Fraction) x ratio(float)
        (
            FrequencyRatio(Fraction(3, 2)),
            FrequencyRatio(0.5),
            FrequencyRatio(3),
        ),
        # ratio(float) x ratio(SP_NUM)
        (
            FrequencyRatio(6.5),
            FrequencyRatio(SP_NUM),
            FrequencyRatio(Fraction(13, 2) / SP_NUM),
        ),
        # ratio(SP_NUM) x ratio(float)
        (
            FrequencyRatio(SP_NUM),
            FrequencyRatio(6.5),
            FrequencyRatio(SP_NUM / Fraction(13, 2)),
        ),
        # ratio(float) x int
        (FrequencyRatio(1.5), 2, FrequencyRatio(3, 4)),
        # int x ratio(float)
        (3, FrequencyRatio(1.5), FrequencyRatio(2)),
        # ratio(float) x float
        (FrequencyRatio(1.5), 0.5, FrequencyRatio(3)),
        # float x ratio(float)
        (2.5, FrequencyRatio(1.5), FrequencyRatio(5, 3)),
        # ratio(float) x fraction
        (FrequencyRatio(1.5), Fraction(1, 2), FrequencyRatio(3)),
        # fraction x ratio(float)
        (Fraction(4, 3), FrequencyRatio(0.5), FrequencyRatio(8, 3)),
        # ratio(float) x SP_NUM
        (FrequencyRatio(1.5), SP_NUM, FrequencyRatio(Fraction(3, 2) / SP_NUM)),
        # SP_NUM x ratio(float)
        (SP_NUM, FrequencyRatio(1.5), FrequencyRatio(SP_NUM / Fraction(3, 2))),
        # ratio(Fraction) x ratio(Fraction)
        (
            FrequencyRatio(Fraction(10, 3)),
            FrequencyRatio(Fraction(5, 3)),
            FrequencyRatio(2)
        ),
        # ratio(Fraction) x ratio(SP_NUM)
        (
            FrequencyRatio(Fraction(10, 3)),
            SP_NUM,
            FrequencyRatio(Fraction(10, 3) / SP_NUM)
        ),
        # ratio(SP_NUM) x ratio(Fraction)
        (
            SP_NUM,
            FrequencyRatio(Fraction(10, 3)),
            FrequencyRatio(SP_NUM / Fraction(10, 3))
        ),
        # ratio(Fraction) x int
        (FrequencyRatio(Fraction(10, 3)), 3, FrequencyRatio(10, 9)),
        # int x ratio(Fraction)
        (4, FrequencyRatio(Fraction(10, 3)), FrequencyRatio(6, 5)),
        # ratio(Fraction) x float
        (FrequencyRatio(Fraction(11, 2)), 0.5, FrequencyRatio(11)),
        # float x ratio(Fraction)
        (6.5, FrequencyRatio(Fraction(11, 2)), FrequencyRatio(13, 11)),
        # ratio(Fraction) x fraction
        (
            FrequencyRatio(Fraction(10, 3)),
            Fraction(1, 2),
            FrequencyRatio(20, 3)
        ),
        # fraction x ratio(Fraction)
        (
            Fraction(31, 3),
            FrequencyRatio(Fraction(10, 3)),
            FrequencyRatio(31, 10)
        ),
        # ratio(Fraction) x SP_NUM
        (
            FrequencyRatio(Fraction(10, 3)),
            SP_NUM,
            FrequencyRatio(Fraction(10, 3) / SP_NUM)
        ),
        # SP_NUM x ratio(Fraction)
        (
            SP_NUM,
            FrequencyRatio(Fraction(10, 3)),
            FrequencyRatio(SP_NUM / Fraction(10, 3))
        ),
        # ratio(SP_NUM) x ratio(SP_NUM)
        (
            FrequencyRatio(2 * SP_NUM),
            FrequencyRatio(SP_NUM),
            FrequencyRatio(2)
        ),
        # ratio(SP_NUM) x int
        (FrequencyRatio(SP_NUM), 3, FrequencyRatio(SP_NUM / 3)),
        # int x ratio(SP_NUM)
        (3, FrequencyRatio(SP_NUM), FrequencyRatio(3 / SP_NUM)),
        # ratio(SP_NUM) x float
        (FrequencyRatio(SP_NUM), 1.5, FrequencyRatio(SP_NUM / Fraction(3, 2))),
        # float x ratio(SP_NUM)
        (1.5, FrequencyRatio(SP_NUM), FrequencyRatio(Fraction(3, 2) / SP_NUM)),
        # ratio(SP_NUM) x fraction
        (
            FrequencyRatio(SP_NUM),
            Fraction(5, 7),
            FrequencyRatio(SP_NUM / Fraction(5, 7))
        ),
        # fraction x ratio(SP_NUM)
        (
            Fraction(5, 7),
            FrequencyRatio(SP_NUM),
            FrequencyRatio(Fraction(5, 7) / SP_NUM)
        ),
        # ratio(SP_NUM) x SP_NUM
        (FrequencyRatio(2 * SP_NUM), SP_NUM, FrequencyRatio(2)),
        # SP_NUM x ratio(SP_NUM)
        (2 * SP_NUM, FrequencyRatio(SP_NUM), FrequencyRatio(2)),
    ]
)
def test_truediv(x, y, result):
    assert x / y == result


@pytest.mark.parametrize(
    'x, y',
    [
        (FrequencyRatio(1, 2), 'abc'),
        (FrequencyRatio(2, 4), SP_NON_NUMBER),
        (FrequencyRatio(1, 2), complex(100, 3)),
        (FrequencyRatio(3), 'abc'),
        (FrequencyRatio(2), SP_NON_NUMBER),
        (FrequencyRatio(6), complex(100, 3)),
        (FrequencyRatio(3.5), 'abc'),
        (FrequencyRatio(2.3), SP_NON_NUMBER),
        (FrequencyRatio(9.2), complex(100, 3)),
    ]
)
def test_truediv_bogus(x, y):

    with pytest.raises(TypeError):
        x / y

    with pytest.raises(TypeError):
        y / x


@pytest.mark.parametrize(
    'x, y, result',
    [
        # ratio(int) x ratio(int)
        (FrequencyRatio(3), FrequencyRatio(2), FrequencyRatio(1)),
        # ratio(int) x ratio(int, int)
        (FrequencyRatio(4), FrequencyRatio(1, 2), FrequencyRatio(8)),
        # ratio(int, int) x ratio(int)
        (FrequencyRatio(4, 3), FrequencyRatio(1, 3), FrequencyRatio(4)),
        # ratio(int) x ratio(float)
        (FrequencyRatio(1), FrequencyRatio(0.5), FrequencyRatio(2)),
        # ratio(float) x ratio(int)
        (FrequencyRatio(9.5), FrequencyRatio(2), FrequencyRatio(4)),
        # ratio(int) x ratio(Fraction)
        (
            FrequencyRatio(4),
            FrequencyRatio(Fraction(5, 3)),
            FrequencyRatio(2)
        ),
        # ratio(Fraction) x ratio(int)
        (
            FrequencyRatio(Fraction(5, 2)),
            FrequencyRatio(9),
            FrequencyRatio(0)
        ),
        # ratio(int) x ratio(SP_NUM)
        (
            FrequencyRatio(80),
            FrequencyRatio(SP_NUM),
            FrequencyRatio(80 // SP_NUM)
        ),
        # ratio(SP_NUM) x ratio(int)
        (
            FrequencyRatio(SP_NUM),
            FrequencyRatio(3),
            FrequencyRatio(SP_NUM // 3)
        ),
        # ratio(int) x int
        (FrequencyRatio(4), 3, FrequencyRatio(1)),
        # int x ratio(int)
        (5, FrequencyRatio(2), FrequencyRatio(2)),
        # ratio(int) x float
        (FrequencyRatio(2), 1.5, FrequencyRatio(1)),
        # float x ratio(int)
        (3.5, FrequencyRatio(2), FrequencyRatio(1)),
        # ratio(int) x fraction
        (FrequencyRatio(4), Fraction(5, 3), FrequencyRatio(2)),
        # fraction x ratio(int)
        (Fraction(5, 3), FrequencyRatio(9), FrequencyRatio(0)),
        # ratio(int) x SP_NUM
        (FrequencyRatio(10), SP_NUM, FrequencyRatio(10 // SP_NUM)),
        # SP_NUM x ratio(int)
        (SP_NUM, FrequencyRatio(2), FrequencyRatio(SP_NUM) // 2),
        # ratio(int, int) x ratio(int, int)
        (FrequencyRatio(2, 3), FrequencyRatio(1, 5), FrequencyRatio(3)),
        # ratio(int, int) x ratio(float)
        (FrequencyRatio(2, 3), FrequencyRatio(0.5), FrequencyRatio(1)),
        # ratio(float) x ratio(int, int)
        (FrequencyRatio(0.5), FrequencyRatio(1, 3), FrequencyRatio(1)),
        # ratio(int, int) x ratio(Fraction)
        (
            FrequencyRatio(5, 2),
            FrequencyRatio(Fraction(7, 2)),
            FrequencyRatio(0)
        ),
        # ratio(Fraction) x ratio(int, int)
        (
            FrequencyRatio(Fraction(11, 2)),
            FrequencyRatio(5, 2),
            FrequencyRatio(2)
        ),
        # ratio(int, int) x ratio(SP_NUM)
        (
            FrequencyRatio(5, 2),
            FrequencyRatio(SP_NUM),
            FrequencyRatio(Fraction(5, 2) // SP_NUM)
        ),
        # ratio(SP_NUM) x ratio(int, int)
        (
            FrequencyRatio(SP_NUM),
            FrequencyRatio(5, 2),
            FrequencyRatio(SP_NUM // Fraction(5, 2))
        ),
        # ratio(int, int) x int
        (FrequencyRatio(4, 3), 7, FrequencyRatio(0)),
        # int x ratio(int, int)
        (2, FrequencyRatio(4, 3), FrequencyRatio(1)),
        # ratio(int, int) x float
        (FrequencyRatio(5, 3), 1.5, FrequencyRatio(1)),
        # float x ratio(int, int)
        (5.5, FrequencyRatio(1, 2), FrequencyRatio(11)),
        # ratio(int, int) x fraction
        (FrequencyRatio(5, 2), Fraction(3, 2), FrequencyRatio(1)),
        # fraction x ratio(int, int)
        (Fraction(10, 2), FrequencyRatio(5, 2), FrequencyRatio(2)),
        # ratio(int, int) x SP_NUM
        (
            FrequencyRatio(10, 2),
            SP_NUM,
            FrequencyRatio(Fraction(10, 2) // SP_NUM)
        ),
        # SP_NUM x ratio(int, int)
        (
            SP_NUM,
            FrequencyRatio(10, 2),
            FrequencyRatio(SP_NUM // Fraction(10, 2)),
        ),
        # ratio(float) x ratio(float)
        (
            FrequencyRatio(10.5),
            FrequencyRatio(4.5),
            FrequencyRatio(2),
        ),
        # ratio(float) x ratio(Fraction)
        (
            FrequencyRatio(6.5),
            FrequencyRatio(Fraction(3, 2)),
            FrequencyRatio(4),
        ),
        # ratio(Fraction) x ratio(float)
        (
            FrequencyRatio(Fraction(3, 2)),
            FrequencyRatio(0.5),
            FrequencyRatio(3),
        ),
        # ratio(float) x ratio(SP_NUM)
        (
            FrequencyRatio(6.5),
            FrequencyRatio(SP_NUM),
            FrequencyRatio(Fraction(13, 2) // SP_NUM),
        ),
        # ratio(SP_NUM) x ratio(float)
        (
            FrequencyRatio(SP_NUM),
            FrequencyRatio(6.5),
            FrequencyRatio(SP_NUM // Fraction(13, 2)),
        ),
        # ratio(float) x int
        (FrequencyRatio(1.5), 2, FrequencyRatio(0)),
        # int x ratio(float)
        (3, FrequencyRatio(1.5), FrequencyRatio(2)),
        # ratio(float) x float
        (FrequencyRatio(1.5), 0.5, FrequencyRatio(3)),
        # float x ratio(float)
        (2.5, FrequencyRatio(1.5), FrequencyRatio(1)),
        # ratio(float) x fraction
        (FrequencyRatio(1.5), Fraction(1, 2), FrequencyRatio(3)),
        # fraction x ratio(float)
        (Fraction(4, 3), FrequencyRatio(0.5), FrequencyRatio(2)),
        # ratio(float) x SP_NUM
        (
            FrequencyRatio(1.5),
            SP_NUM,
            FrequencyRatio(Fraction(3, 2) // SP_NUM)
        ),
        # SP_NUM x ratio(float)
        (
            SP_NUM,
            FrequencyRatio(1.5),
            FrequencyRatio(SP_NUM // Fraction(3, 2))
        ),
        # ratio(Fraction) x ratio(Fraction)
        (
            FrequencyRatio(Fraction(10, 3)),
            FrequencyRatio(Fraction(5, 3)),
            FrequencyRatio(2)
        ),
        # ratio(Fraction) x ratio(SP_NUM)
        (
            FrequencyRatio(Fraction(10, 3)),
            SP_NUM,
            FrequencyRatio(Fraction(10, 3) // SP_NUM)
        ),
        # ratio(SP_NUM) x ratio(Fraction)
        (
            SP_NUM,
            FrequencyRatio(Fraction(10, 3)),
            FrequencyRatio(SP_NUM // Fraction(10, 3))
        ),
        # ratio(Fraction) x int
        (FrequencyRatio(Fraction(10, 3)), 3, FrequencyRatio(1)),
        # int x ratio(Fraction)
        (4, FrequencyRatio(Fraction(10, 3)), FrequencyRatio(1)),
        # ratio(Fraction) x float
        (FrequencyRatio(Fraction(11, 2)), 0.5, FrequencyRatio(11)),
        # float x ratio(Fraction)
        (6.5, FrequencyRatio(Fraction(11, 2)), FrequencyRatio(1)),
        # ratio(Fraction) x fraction
        (
            FrequencyRatio(Fraction(10, 3)),
            Fraction(1, 2),
            FrequencyRatio(6)
        ),
        # fraction x ratio(Fraction)
        (
            Fraction(31, 3),
            FrequencyRatio(Fraction(10, 3)),
            FrequencyRatio(3)
        ),
        # ratio(Fraction) x SP_NUM
        (
            FrequencyRatio(Fraction(10, 3)),
            SP_NUM,
            FrequencyRatio(Fraction(10, 3) // SP_NUM)
        ),
        # SP_NUM x ratio(Fraction)
        (
            SP_NUM,
            FrequencyRatio(Fraction(10, 3)),
            FrequencyRatio(SP_NUM // Fraction(10, 3))
        ),
        # ratio(SP_NUM) x ratio(SP_NUM)
        (
            FrequencyRatio(2 * SP_NUM),
            FrequencyRatio(SP_NUM),
            FrequencyRatio(2)
        ),
        # ratio(SP_NUM) x int
        (FrequencyRatio(SP_NUM), 3, FrequencyRatio(SP_NUM // 3)),
        # int x ratio(SP_NUM)
        (3, FrequencyRatio(SP_NUM), FrequencyRatio(3 // SP_NUM)),
        # ratio(SP_NUM) x float
        (
            FrequencyRatio(SP_NUM),
            1.5,
            FrequencyRatio(SP_NUM // Fraction(3, 2))
        ),
        # float x ratio(SP_NUM)
        (
            1.5,
            FrequencyRatio(SP_NUM),
            FrequencyRatio(Fraction(3, 2) // SP_NUM)
        ),
        # ratio(SP_NUM) x fraction
        (
            FrequencyRatio(SP_NUM),
            Fraction(5, 7),
            FrequencyRatio(SP_NUM // Fraction(5, 7))
        ),
        # fraction x ratio(SP_NUM)
        (
            Fraction(5, 7),
            FrequencyRatio(SP_NUM),
            FrequencyRatio(Fraction(5, 7) // SP_NUM)
        ),
        # ratio(SP_NUM) x SP_NUM
        (FrequencyRatio(2.5 * SP_NUM), SP_NUM, FrequencyRatio(2)),
        # SP_NUM x ratio(SP_NUM)
        (2.5 * SP_NUM, FrequencyRatio(SP_NUM), FrequencyRatio(2)),
    ]
)
def test_floordiv(x, y, result):
    assert x // y == result


@pytest.mark.parametrize(
    'x, y',
    [
        (FrequencyRatio(1, 2), 'abc'),
        (FrequencyRatio(1, 2), SP_NON_NUMBER),
        (FrequencyRatio(1, 2), Frequency(100)),
        (FrequencyRatio(1, 2), complex(100, 3)),
        (FrequencyRatio(3), 'abc'),
        (FrequencyRatio(3), SP_NON_NUMBER),
        (FrequencyRatio(5), Frequency(100)),
        (FrequencyRatio(6), complex(100, 3)),
        (FrequencyRatio(3.5), 'abc'),
        (FrequencyRatio(3.5), SP_NON_NUMBER),
        (FrequencyRatio(2.1), Frequency(100)),
        (FrequencyRatio(9.2), complex(100, 3)),
    ]
)
def test_floordiv_bogus(x, y):

    with pytest.raises(TypeError):
        x // y

    with pytest.raises(TypeError):
        y // x


@pytest.mark.parametrize(
    'x, y, result',
    [
        # ratio(int) x ratio(int)
        (FrequencyRatio(3), FrequencyRatio(2), FrequencyRatio(1)),
        # ratio(int) x ratio(int, int)
        (FrequencyRatio(4), FrequencyRatio(1, 2), FrequencyRatio(0)),
        # ratio(int, int) x ratio(int)
        (FrequencyRatio(4, 3), FrequencyRatio(1, 3), FrequencyRatio(0)),
        # ratio(int) x ratio(float)
        (FrequencyRatio(1), FrequencyRatio(0.5), FrequencyRatio(0)),
        # ratio(float) x ratio(int)
        (FrequencyRatio(9.5), FrequencyRatio(2), FrequencyRatio(3, 2)),
        # ratio(int) x ratio(Fraction)
        (
            FrequencyRatio(4),
            FrequencyRatio(Fraction(5, 3)),
            FrequencyRatio(2, 3)
        ),
        # ratio(Fraction) x ratio(int)
        (
            FrequencyRatio(Fraction(5, 2)),
            FrequencyRatio(9),
            FrequencyRatio(5, 2)
        ),
        # ratio(int) x ratio(SP_NUM)
        (
            FrequencyRatio(80),
            FrequencyRatio(SP_NUM),
            FrequencyRatio(80 % SP_NUM)
        ),
        # ratio(SP_NUM) x ratio(int)
        (
            FrequencyRatio(SP_NUM),
            FrequencyRatio(3),
            FrequencyRatio(SP_NUM % 3)
        ),
        # ratio(int) x int
        (FrequencyRatio(4), 3, FrequencyRatio(1)),
        # int x ratio(int)
        (5, FrequencyRatio(2), FrequencyRatio(1)),
        # ratio(int) x float
        (FrequencyRatio(2), 1.5, FrequencyRatio(1, 2)),
        # float x ratio(int)
        (3.5, FrequencyRatio(2), FrequencyRatio(3, 2)),
        # ratio(int) x fraction
        (FrequencyRatio(4), Fraction(5, 3), FrequencyRatio(2, 3)),
        # fraction x ratio(int)
        (Fraction(5, 3), FrequencyRatio(9), FrequencyRatio(5, 3)),
        # ratio(int) x SP_NUM
        (FrequencyRatio(10), SP_NUM, FrequencyRatio(10 % SP_NUM)),
        # SP_NUM x ratio(int)
        (SP_NUM, FrequencyRatio(2), FrequencyRatio(SP_NUM) % 2),
        # ratio(int, int) x ratio(int, int)
        (FrequencyRatio(2, 3), FrequencyRatio(1, 5), FrequencyRatio(1, 15)),
        # ratio(int, int) x ratio(float)
        (FrequencyRatio(2, 3), FrequencyRatio(0.5), FrequencyRatio(1, 6)),
        # ratio(float) x ratio(int, int)
        (FrequencyRatio(0.5), FrequencyRatio(1, 3), FrequencyRatio(1, 6)),
        # ratio(int, int) x ratio(Fraction)
        (
            FrequencyRatio(5, 2),
            FrequencyRatio(Fraction(10, 2)),
            FrequencyRatio(5, 2)
        ),
        # ratio(Fraction) x ratio(int, int)
        (
            FrequencyRatio(Fraction(11, 2)),
            FrequencyRatio(5, 2),
            FrequencyRatio(1, 2)
        ),
        # ratio(int, int) x ratio(SP_NUM)
        (
            FrequencyRatio(5, 2),
            FrequencyRatio(SP_NUM),
            FrequencyRatio(Fraction(5, 2) % SP_NUM)
        ),
        # ratio(SP_NUM) x ratio(int, int)
        (
            FrequencyRatio(SP_NUM),
            FrequencyRatio(5, 2),
            FrequencyRatio(SP_NUM % Fraction(5, 2))
        ),
        # ratio(int, int) x int
        (FrequencyRatio(4, 3), 7, FrequencyRatio(4, 3)),
        # int x ratio(int, int)
        (2, FrequencyRatio(4, 3), FrequencyRatio(2, 3)),
        # ratio(int, int) x float
        (FrequencyRatio(5, 3), 1.5, FrequencyRatio(1, 6)),
        # float x ratio(int, int)
        (5.5, FrequencyRatio(1, 2), FrequencyRatio(0)),
        # ratio(int, int) x fraction
        (FrequencyRatio(5, 2), Fraction(3, 2), FrequencyRatio(1)),
        # fraction x ratio(int, int)
        (Fraction(10, 2), FrequencyRatio(5, 2), FrequencyRatio(0)),
        # ratio(int, int) x SP_NUM
        (
            FrequencyRatio(10, 2),
            SP_NUM,
            FrequencyRatio(Fraction(10, 2) % SP_NUM)
        ),
        # SP_NUM x ratio(int, int)
        (
            SP_NUM,
            FrequencyRatio(10, 2),
            FrequencyRatio(SP_NUM % Fraction(10, 2)),
        ),
        # ratio(float) x ratio(float)
        (
            FrequencyRatio(10.5),
            FrequencyRatio(4.5),
            FrequencyRatio(3, 2),
        ),
        # ratio(float) x ratio(Fraction)
        (
            FrequencyRatio(6.5),
            FrequencyRatio(Fraction(3, 2)),
            FrequencyRatio(1, 2),
        ),
        # ratio(Fraction) x ratio(float)
        (
            FrequencyRatio(Fraction(3, 2)),
            FrequencyRatio(0.5),
            FrequencyRatio(0),
        ),
        # ratio(float) x ratio(SP_NUM)
        (
            FrequencyRatio(6.5),
            FrequencyRatio(SP_NUM),
            FrequencyRatio(Fraction(13, 2) % SP_NUM),
        ),
        # ratio(SP_NUM) x ratio(float)
        (
            FrequencyRatio(SP_NUM),
            FrequencyRatio(6.5),
            FrequencyRatio(SP_NUM % Fraction(13, 2)),
        ),
        # ratio(float) x int
        (FrequencyRatio(1.5), 2, FrequencyRatio(3, 2)),
        # int x ratio(float)
        (3, FrequencyRatio(1.5), FrequencyRatio(0)),
        # ratio(float) x float
        (FrequencyRatio(1.5), 0.5, FrequencyRatio(0)),
        # float x ratio(float)
        (2.5, FrequencyRatio(1.5), FrequencyRatio(1)),
        # ratio(float) x fraction
        (FrequencyRatio(1.5), Fraction(1, 2), FrequencyRatio(0)),
        # fraction x ratio(float)
        (Fraction(4, 3), FrequencyRatio(0.5), FrequencyRatio(1, 3)),
        # ratio(float) x SP_NUM
        (
            FrequencyRatio(1.5),
            SP_NUM,
            FrequencyRatio(Fraction(3, 2) % SP_NUM)
        ),
        # SP_NUM x ratio(float)
        (
            SP_NUM,
            FrequencyRatio(1.5),
            FrequencyRatio(SP_NUM % Fraction(3, 2))
        ),
        # ratio(Fraction) x ratio(Fraction)
        (
            FrequencyRatio(Fraction(10, 3)),
            FrequencyRatio(Fraction(4, 3)),
            FrequencyRatio(2, 3)
        ),
        # ratio(Fraction) x ratio(SP_NUM)
        (
            FrequencyRatio(Fraction(10, 3)),
            SP_NUM,
            FrequencyRatio(Fraction(10, 3) % SP_NUM)
        ),
        # ratio(SP_NUM) x ratio(Fraction)
        (
            SP_NUM,
            FrequencyRatio(Fraction(10, 3)),
            FrequencyRatio(SP_NUM % Fraction(10, 3))
        ),
        # ratio(Fraction) x int
        (FrequencyRatio(Fraction(10, 3)), 3, FrequencyRatio(1, 3)),
        # int x ratio(Fraction)
        (4, FrequencyRatio(Fraction(10, 3)), FrequencyRatio(2, 3)),
        # ratio(Fraction) x float
        (FrequencyRatio(Fraction(11, 2)), 0.5, FrequencyRatio(0)),
        # float x ratio(Fraction)
        (6.5, FrequencyRatio(Fraction(11, 2)), FrequencyRatio(1)),
        # ratio(Fraction) x fraction
        (
            FrequencyRatio(Fraction(10, 3)),
            Fraction(1, 2),
            FrequencyRatio(1, 3)
        ),
        # fraction x ratio(Fraction)
        (
            Fraction(31, 3),
            FrequencyRatio(Fraction(10, 3)),
            FrequencyRatio(1, 3)
        ),
        # ratio(Fraction) x SP_NUM
        (
            FrequencyRatio(Fraction(10, 3)),
            SP_NUM,
            FrequencyRatio(Fraction(10, 3) % SP_NUM)
        ),
        # SP_NUM x ratio(Fraction)
        (
            SP_NUM,
            FrequencyRatio(Fraction(10, 3)),
            FrequencyRatio(SP_NUM % Fraction(10, 3))
        ),
        # ratio(SP_NUM) x ratio(SP_NUM)
        (
            FrequencyRatio(2 * SP_NUM + 1),
            FrequencyRatio(SP_NUM),
            FrequencyRatio(1)
        ),
        # ratio(SP_NUM) x int
        (FrequencyRatio(SP_NUM), 3, FrequencyRatio(SP_NUM % 3)),
        # int x ratio(SP_NUM)
        (3, FrequencyRatio(SP_NUM), FrequencyRatio(3 % SP_NUM)),
        # ratio(SP_NUM) x float
        (
            FrequencyRatio(SP_NUM),
            1.5,
            FrequencyRatio(SP_NUM % Fraction(3, 2))
        ),
        # float x ratio(SP_NUM)
        (
            1.5,
            FrequencyRatio(SP_NUM),
            FrequencyRatio(Fraction(3, 2) % SP_NUM)
        ),
        # ratio(SP_NUM) x fraction
        (
            FrequencyRatio(SP_NUM),
            Fraction(5, 7),
            FrequencyRatio(SP_NUM % Fraction(5, 7))
        ),
        # fraction x ratio(SP_NUM)
        (
            Fraction(5, 7),
            FrequencyRatio(SP_NUM),
            FrequencyRatio(Fraction(5, 7) % SP_NUM)
        ),
        # ratio(SP_NUM) x SP_NUM
        (FrequencyRatio(2 * SP_NUM + 1), SP_NUM, FrequencyRatio(1)),
        # SP_NUM x ratio(SP_NUM)
        (SP_NUM + 1, FrequencyRatio(SP_NUM), FrequencyRatio(1)),
    ]
)
def test_mod(x, y, result):
    assert x % y == result


@pytest.mark.parametrize(
    'x, y',
    [
        (FrequencyRatio(1, 2), 'abc'),
        (FrequencyRatio(1, 2), complex(100, 3)),
        (FrequencyRatio(1, 2), SP_NON_NUMBER),
        (FrequencyRatio(1, 2), Frequency(100)),
        (FrequencyRatio(3), 'abc'),
        (FrequencyRatio(3), SP_NON_NUMBER),
        (FrequencyRatio(5), Frequency(100)),
        (FrequencyRatio(6), complex(100, 3)),
        (FrequencyRatio(3.5), 'abc'),
        (FrequencyRatio(3.5), SP_NON_NUMBER),
        (FrequencyRatio(2.1), Frequency(100)),
        (FrequencyRatio(9.2), complex(100, 3)),
    ]
)
def test_mod_bogus(x, y):

    with pytest.raises(TypeError):
        x % y

    with pytest.raises(TypeError):
        y % x


@pytest.mark.parametrize(
    'x, y, result',
    [
        # ratio(int) x ratio(int)
        (FrequencyRatio(3), FrequencyRatio(2), FrequencyRatio(9)),
        # ratio(int) x ratio(int, int)
        (
            FrequencyRatio(4),
            FrequencyRatio(1, 2),
            FrequencyRatio(4 ** sp.Rational(1, 2))
        ),
        # ratio(int, int) x ratio(int)
        (
            FrequencyRatio(4, 3),
            FrequencyRatio(1, 3),
            FrequencyRatio(sp.Rational(4, 3) ** sp.Rational(1, 3))
        ),
        # ratio(int) x ratio(float)
        (
            FrequencyRatio(2),
            FrequencyRatio(0.5),
            FrequencyRatio(2 ** sp.Rational(1, 2))
        ),
        # ratio(float) x ratio(int)
        (FrequencyRatio(9.5), FrequencyRatio(2), FrequencyRatio(361, 4)),
        # ratio(int) x ratio(Fraction)
        (
            FrequencyRatio(4),
            FrequencyRatio(Fraction(5, 3)),
            FrequencyRatio(4 ** sp.Rational(5, 3))
        ),
        # ratio(Fraction) x ratio(int)
        (
            FrequencyRatio(Fraction(5, 2)),
            FrequencyRatio(3),
            FrequencyRatio(125, 8)
        ),
        # ratio(int) x ratio(SP_NUM)
        (
            FrequencyRatio(80),
            FrequencyRatio(SP_NUM),
            FrequencyRatio(80 ** SP_NUM)
        ),
        # ratio(SP_NUM) x ratio(int)
        (
            FrequencyRatio(SP_NUM),
            FrequencyRatio(3),
            FrequencyRatio(SP_NUM ** 3)
        ),
        # ratio(int) x int
        (FrequencyRatio(4), 3, FrequencyRatio(64)),
        # int x ratio(int)
        (5, FrequencyRatio(2), FrequencyRatio(25)),
        # ratio(int) x float
        (
            FrequencyRatio(2),
            1.5,
            FrequencyRatio(2 ** sp.Rational(3, 2))
        ),
        # float x ratio(int)
        (3.5, FrequencyRatio(2), FrequencyRatio(49, 4)),
        # ratio(int) x fraction
        (
            FrequencyRatio(4),
            Fraction(5, 3),
            FrequencyRatio(4 ** sp.Rational(5, 3))
        ),
        # fraction x ratio(int)
        (Fraction(5, 3), FrequencyRatio(9), FrequencyRatio(1953125, 19683)),
        # ratio(int) x SP_NUM
        (FrequencyRatio(10), SP_NUM, FrequencyRatio(10 ** SP_NUM)),
        # SP_NUM x ratio(int)
        (SP_NUM, FrequencyRatio(2), FrequencyRatio(SP_NUM) ** 2),
        # ratio(int, int) x ratio(int, int)
        (
            FrequencyRatio(2, 3),
            FrequencyRatio(5, 3),
            FrequencyRatio(sp.Rational(2, 3) ** sp.Rational(5, 3))
        ),
        # ratio(int, int) x ratio(float)
        (
            FrequencyRatio(2, 3),
            FrequencyRatio(0.5),
            FrequencyRatio(sp.Rational(2, 3) ** sp.Rational(1, 2))
        ),
        # ratio(float) x ratio(int, int)
        (
            FrequencyRatio(0.5),
            FrequencyRatio(1, 3),
            FrequencyRatio(sp.Rational(1, 2) ** sp.Rational(1, 3))
        ),
        # ratio(int, int) x ratio(Fraction)
        (
            FrequencyRatio(5, 2),
            FrequencyRatio(Fraction(10, 2)),
            FrequencyRatio(sp.Rational(5, 2) ** sp.Rational(10, 2))
        ),
        # ratio(Fraction) x ratio(int, int)
        (
            FrequencyRatio(Fraction(10, 2)),
            FrequencyRatio(5, 2),
            FrequencyRatio(5 ** sp.Rational(5, 2))
        ),
        # ratio(int, int) x ratio(SP_NUM)
        (
            FrequencyRatio(5, 2),
            FrequencyRatio(SP_NUM),
            FrequencyRatio(sp.Rational(5, 2) ** SP_NUM)
        ),
        # ratio(SP_NUM) x ratio(int, int)
        (
            FrequencyRatio(SP_NUM),
            FrequencyRatio(5, 2),
            FrequencyRatio(SP_NUM ** Fraction(5, 2))
        ),
        # ratio(int, int) x int
        (FrequencyRatio(4, 3), 7, FrequencyRatio(16384, 2187)),
        # int x ratio(int, int)
        (
            2,
            FrequencyRatio(4, 3),
            FrequencyRatio(2 ** sp.Rational(4, 3))
        ),
        # ratio(int, int) x float
        (
            FrequencyRatio(4, 3),
            1.5,
            FrequencyRatio(sp.Rational(4, 3) ** sp.Rational(3, 2))
        ),
        # float x ratio(int, int)
        (
            1.5,
            FrequencyRatio(4, 3),
            FrequencyRatio(sp.Rational(3, 2) ** sp.Rational(4, 3))
        ),
        # ratio(int, int) x fraction
        (
            FrequencyRatio(5, 2),
            Fraction(3, 2),
            FrequencyRatio(sp.Rational(5, 2) ** sp.Rational(3, 2))
        ),
        # fraction x ratio(int, int)
        (
            Fraction(10, 2),
            FrequencyRatio(5, 2),
            FrequencyRatio(5 ** sp.Rational(5, 2))
        ),
        # ratio(int, int) x SP_NUM
        (
            FrequencyRatio(10, 2),
            SP_NUM,
            FrequencyRatio(sp.Rational(10, 2) ** SP_NUM)
        ),
        # SP_NUM x ratio(int, int)
        (
            SP_NUM,
            FrequencyRatio(10, 2),
            FrequencyRatio(SP_NUM ** sp.Rational(10, 2)),
        ),
        # ratio(float) x ratio(float)
        (
            FrequencyRatio(10.5),
            FrequencyRatio(4.5),
            FrequencyRatio(sp.Rational(21, 2) ** sp.Rational(9, 2)),
        ),
        # ratio(float) x ratio(Fraction)
        (
            FrequencyRatio(6.5),
            FrequencyRatio(Fraction(3, 2)),
            FrequencyRatio(sp.Rational(13, 2) ** sp.Rational(3, 2)),
        ),
        # ratio(Fraction) x ratio(float)
        (
            FrequencyRatio(Fraction(3, 2)),
            FrequencyRatio(0.5),
            FrequencyRatio(sp.Rational(3, 2) ** sp.Rational(1, 2)),
        ),
        # ratio(float) x ratio(SP_NUM)
        (
            FrequencyRatio(6.5),
            FrequencyRatio(SP_NUM),
            FrequencyRatio(sp.Rational(13, 2) ** SP_NUM),
        ),
        # ratio(SP_NUM) x ratio(float)
        (
            FrequencyRatio(SP_NUM),
            FrequencyRatio(6.5),
            FrequencyRatio(SP_NUM ** sp.Rational(13, 2)),
        ),
        # ratio(float) x int
        (FrequencyRatio(1.5), 2, FrequencyRatio(9, 4)),
        # int x ratio(float)
        (
            3,
            FrequencyRatio(1.5),
            FrequencyRatio(3 ** sp.Rational(3, 2))
        ),
        # ratio(float) x float
        (
            FrequencyRatio(1.5),
            0.5,
            FrequencyRatio(sp.Rational(3, 2) ** sp.Rational(1, 2))
        ),
        # float x ratio(float)
        (
            2.5,
            FrequencyRatio(1.5),
            FrequencyRatio(sp.Rational(5, 2) ** sp.Rational(3, 2))
        ),
        # ratio(float) x fraction
        (
            FrequencyRatio(1.5),
            Fraction(1, 2),
            FrequencyRatio(sp.Rational(3, 2) ** sp.Rational(1, 2))
        ),
        # fraction x ratio(float)
        (
            Fraction(4, 3),
            FrequencyRatio(0.5),
            FrequencyRatio(sp.Rational(4, 3) ** sp.Rational(1, 2))
        ),
        # ratio(float) x SP_NUM
        (
            FrequencyRatio(1.5),
            SP_NUM,
            FrequencyRatio(sp.Rational(3, 2) ** SP_NUM)
        ),
        # SP_NUM x ratio(float)
        (
            SP_NUM,
            FrequencyRatio(1.5),
            FrequencyRatio(SP_NUM ** sp.Rational(3, 2))
        ),
        # ratio(Fraction) x ratio(Fraction)
        (
            FrequencyRatio(Fraction(10, 3)),
            FrequencyRatio(Fraction(4, 3)),
            FrequencyRatio(sp.Rational(10, 3) ** sp.Rational(4, 3))
        ),
        # ratio(Fraction) x ratio(SP_NUM)
        (
            FrequencyRatio(Fraction(10, 3)),
            SP_NUM,
            FrequencyRatio(sp.Rational(10, 3) ** SP_NUM)
        ),
        # ratio(SP_NUM) x ratio(Fraction)
        (
            SP_NUM,
            FrequencyRatio(Fraction(10, 3)),
            FrequencyRatio(SP_NUM ** Fraction(10, 3))
        ),
        # ratio(Fraction) x int
        (FrequencyRatio(Fraction(10, 3)), 3, FrequencyRatio(1000, 27)),
        # int x ratio(Fraction)
        (
            4,
            FrequencyRatio(Fraction(10, 3)),
            FrequencyRatio(4 ** sp.Rational(10, 3))
        ),
        # ratio(Fraction) x float
        (
            FrequencyRatio(Fraction(11, 2)),
            0.5,
            FrequencyRatio(sp.Rational(11, 2) ** sp.Rational(1, 2))
        ),
        # float x ratio(Fraction)
        (
            6.5,
            FrequencyRatio(Fraction(11, 2)),
            FrequencyRatio(sp.Rational(13, 2) ** sp.Rational(11, 2))
        ),
        # ratio(Fraction) x fraction
        (
            FrequencyRatio(Fraction(10, 3)),
            Fraction(1, 2),
            FrequencyRatio(sp.Rational(10, 3) ** sp.Rational(1, 2))
        ),
        # fraction x ratio(Fraction)
        (
            Fraction(31, 3),
            FrequencyRatio(Fraction(10, 3)),
            FrequencyRatio(sp.Rational(31, 3) ** sp.Rational(10, 3))
        ),
        # ratio(Fraction) x SP_NUM
        (
            FrequencyRatio(Fraction(10, 3)),
            SP_NUM,
            FrequencyRatio(sp.Rational(10, 3) ** SP_NUM)
        ),
        # SP_NUM x ratio(Fraction)
        (
            SP_NUM,
            FrequencyRatio(Fraction(10, 3)),
            FrequencyRatio(SP_NUM ** Fraction(10, 3))
        ),
        # ratio(SP_NUM) x ratio(SP_NUM)
        (
            FrequencyRatio(2 * SP_NUM),
            FrequencyRatio(SP_NUM),
            FrequencyRatio((2 * SP_NUM) ** SP_NUM)
        ),
        # ratio(SP_NUM) x int
        (FrequencyRatio(SP_NUM), 3, FrequencyRatio(SP_NUM ** 3)),
        # int x ratio(SP_NUM)
        (3, FrequencyRatio(SP_NUM), FrequencyRatio(3 ** SP_NUM)),
        # ratio(SP_NUM) x float
        (
            FrequencyRatio(SP_NUM),
            1.5,
            FrequencyRatio(SP_NUM ** sp.Rational(3, 2))
        ),
        # float x ratio(SP_NUM)
        (
            1.5,
            FrequencyRatio(SP_NUM),
            FrequencyRatio(sp.Rational(3, 2) ** SP_NUM)
        ),
        # ratio(SP_NUM) x fraction
        (
            FrequencyRatio(SP_NUM),
            Fraction(5, 7),
            FrequencyRatio(SP_NUM ** sp.Rational(5, 7))
        ),
        # fraction x ratio(SP_NUM)
        (
            Fraction(5, 7),
            FrequencyRatio(SP_NUM),
            FrequencyRatio(sp.Rational(5, 7) ** SP_NUM)
        ),
        # ratio(SP_NUM) x SP_NUM
        (FrequencyRatio(SP_NUM), SP_NUM, FrequencyRatio(SP_NUM ** SP_NUM)),
        # SP_NUM x ratio(SP_NUM)
        (SP_NUM, FrequencyRatio(SP_NUM), FrequencyRatio(SP_NUM ** SP_NUM)),
    ]
)
def test_pow(x, y, result):
    assert x ** y == result
    assert pow(x, y) == result


@pytest.mark.parametrize(
    'x, y',
    [
        (FrequencyRatio(1, 2), 'abc'),
        (FrequencyRatio(1, 2), Frequency(100)),
        (FrequencyRatio(1, 2), SP_NON_NUMBER),
        (FrequencyRatio(1, 2), complex(100, 3)),
        (FrequencyRatio(3), 'abc'),
        (FrequencyRatio(3), SP_NON_NUMBER),
        (FrequencyRatio(5), Frequency(100)),
        (FrequencyRatio(6), complex(100, 3)),
        (FrequencyRatio(3.5), 'abc'),
        (FrequencyRatio(3.5), SP_NON_NUMBER),
        (FrequencyRatio(2.1), Frequency(100)),
        (FrequencyRatio(9.2), complex(100, 3)),
    ]
)
def test_pow_bogus(x, y):

    with pytest.raises(TypeError):
        x ** y

    with pytest.raises(TypeError):
        pow(x, y)

    with pytest.raises(TypeError):
        y ** x

    with pytest.raises(TypeError):
        pow(y, x)


@pytest.mark.parametrize(
    'x, y',
    [
        # ratio(int) x ratio(int)
        (FrequencyRatio(3), FrequencyRatio(4)),
        # ratio(int) x ratio(int, int)
        (FrequencyRatio(4), FrequencyRatio(9, 2)),
        # ratio(int, int) x ratio(int)
        (FrequencyRatio(1, 3), FrequencyRatio(3, 4)),
        # ratio(int) x ratio(float)
        (FrequencyRatio(1), FrequencyRatio(2.5)),
        # ratio(float) x ratio(int)
        (FrequencyRatio(9.5), FrequencyRatio(10)),
        # ratio(int) x ratio(Fraction)
        (
            FrequencyRatio(2),
            FrequencyRatio(Fraction(11, 3))
        ),
        # ratio(Fraction) x ratio(int)
        (
            FrequencyRatio(Fraction(5, 2)),
            FrequencyRatio(9)
        ),
        # ratio(int) x ratio(SP_NUM)
        (
            FrequencyRatio(10),
            FrequencyRatio(10 * SP_NUM)
        ),
        # ratio(SP_NUM) x ratio(int)
        (
            FrequencyRatio(SP_NUM),
            FrequencyRatio(300000)
        ),
        # ratio(int) x int
        (FrequencyRatio(4), 5),
        # int x ratio(int)
        (5, FrequencyRatio(10)),
        # ratio(int) x float
        (FrequencyRatio(2), 4.5),
        # float x ratio(int)
        (3.5, FrequencyRatio(8)),
        # ratio(int) x fraction
        (FrequencyRatio(4), Fraction(20, 3)),
        # fraction x ratio(int)
        (Fraction(5, 3), FrequencyRatio(9)),
        # ratio(int) x SP_NUM
        (FrequencyRatio(10), 10 * SP_NUM),
        # SP_NUM x ratio(int)
        (SP_NUM, FrequencyRatio(200)),
        # ratio(int, int) x ratio(int, int)
        (FrequencyRatio(2, 3), FrequencyRatio(23, 5)),
        # ratio(int, int) x ratio(float)
        (FrequencyRatio(2, 3), FrequencyRatio(2.5)),
        # ratio(float) x ratio(int, int)
        (FrequencyRatio(0.5), FrequencyRatio(2, 3)),
        # ratio(int, int) x ratio(Fraction)
        (
            FrequencyRatio(5, 2),
            FrequencyRatio(Fraction(7, 2))
        ),
        # ratio(Fraction) x ratio(int, int)
        (
            FrequencyRatio(Fraction(11, 2)),
            FrequencyRatio(23, 2)
        ),
        # ratio(int, int) x ratio(SP_NUM)
        (
            FrequencyRatio(5, 2),
            FrequencyRatio(44 * SP_NUM)
        ),
        # ratio(SP_NUM) x ratio(int, int)
        (
            FrequencyRatio(SP_NUM),
            FrequencyRatio(99, 2),
        ),
        # ratio(int, int) x int
        (FrequencyRatio(4, 3), 7),
        # int x ratio(int, int)
        (2, FrequencyRatio(11, 3)),
        # ratio(int, int) x float
        (FrequencyRatio(5, 3), 9.5),
        # float x ratio(int, int)
        (5.5, FrequencyRatio(23, 2)),
        # ratio(int, int) x fraction
        (FrequencyRatio(5, 2), Fraction(11, 2)),
        # fraction x ratio(int, int)
        (Fraction(10, 2), FrequencyRatio(29, 2)),
        # ratio(int, int) x SP_NUM
        (
            FrequencyRatio(1, 1000),
            SP_NUM
        ),
        # SP_NUM x ratio(int, int)
        (
            SP_NUM,
            FrequencyRatio(999999, 2)
        ),
        # ratio(float) x ratio(float)
        (
            FrequencyRatio(10.5),
            FrequencyRatio(14.5)
        ),
        # ratio(float) x ratio(Fraction)
        (
            FrequencyRatio(6.5),
            FrequencyRatio(Fraction(43, 2))
        ),
        # ratio(Fraction) x ratio(float)
        (
            FrequencyRatio(Fraction(3, 2)),
            FrequencyRatio(3.5),
        ),
        # ratio(float) x ratio(SP_NUM)
        (
            FrequencyRatio(0.0025),
            FrequencyRatio(SP_NUM)
        ),
        # ratio(SP_NUM) x ratio(float)
        (
            FrequencyRatio(SP_NUM),
            FrequencyRatio(6.5)
        ),
        # ratio(float) x int
        (FrequencyRatio(1.5), 2),
        # int x ratio(float)
        (3, FrequencyRatio(3.5)),
        # ratio(float) x float
        (FrequencyRatio(1.5), 2.5),
        # float x ratio(float)
        (2.5, FrequencyRatio(9.5)),
        # ratio(float) x fraction
        (FrequencyRatio(1.5), Fraction(9, 2)),
        # fraction x ratio(float)
        (Fraction(4, 3), FrequencyRatio(10.5)),
        # ratio(float) x SP_NUM
        (FrequencyRatio(0.015), SP_NUM),
        # SP_NUM x ratio(float)
        (SP_NUM, FrequencyRatio(23.5)),
        # ratio(Fraction) x ratio(Fraction)
        (
            FrequencyRatio(Fraction(10, 3)),
            FrequencyRatio(Fraction(13, 3)),
        ),
        # ratio(Fraction) x ratio(SP_NUM)
        (
            FrequencyRatio(Fraction(1, 9999)),
            SP_NUM,
        ),
        # ratio(SP_NUM) x ratio(Fraction)
        (
            SP_NUM,
            FrequencyRatio(Fraction(9991, 3)),
        ),
        # ratio(Fraction) x int
        (FrequencyRatio(Fraction(10, 3)), 55),
        # int x ratio(Fraction)
        (4, FrequencyRatio(Fraction(67, 3))),
        # ratio(Fraction) x float
        (FrequencyRatio(Fraction(11, 2)), 76.5),
        # float x ratio(Fraction)
        (6.5, FrequencyRatio(Fraction(35, 2))),
        # ratio(Fraction) x fraction
        (
            FrequencyRatio(Fraction(1, 3)),
            Fraction(1, 2),
        ),
        # fraction x ratio(Fraction)
        (
            Fraction(1, 3),
            FrequencyRatio(Fraction(2, 3)),
        ),
        # ratio(Fraction) x SP_NUM
        (
            FrequencyRatio(Fraction(1, 77777)),
            SP_NUM,
        ),
        # SP_NUM x ratio(Fraction)
        (
            SP_NUM,
            FrequencyRatio(Fraction(99991, 3)),
        ),
        # ratio(SP_NUM) x ratio(SP_NUM)
        (
            FrequencyRatio(SP_NUM),
            FrequencyRatio(2 * SP_NUM),
        ),
        # ratio(SP_NUM) x int
        (FrequencyRatio(SP_NUM), 3333),
        # int x ratio(SP_NUM)
        (3, FrequencyRatio(51 * SP_NUM)),
        # ratio(SP_NUM) x float
        (FrequencyRatio(SP_NUM), 23.5),
        # float x ratio(SP_NUM)
        (0.0005, FrequencyRatio(SP_NUM)),
        # ratio(SP_NUM) x fraction
        (
            FrequencyRatio(SP_NUM),
            Fraction(99, 7)
        ),
        # fraction x ratio(SP_NUM)
        (
            Fraction(1, 999999),
            FrequencyRatio(SP_NUM)
        ),
        # ratio(SP_NUM) x SP_NUM
        (FrequencyRatio(SP_NUM), 9 * SP_NUM),
        # SP_NUM x ratio(SP_NUM)
        (SP_NUM, FrequencyRatio(2 * SP_NUM)),
    ]
)
def test_lt(x, y):
    assert x < y
    assert y > x
    assert x != y
    assert y != x


@pytest.mark.parametrize(
    'x, y',
    [
        (FrequencyRatio(1, 2), 'abc'),
        (FrequencyRatio(1, 2), Frequency(100)),
        (FrequencyRatio(1, 2), SP_NON_NUMBER),
        (FrequencyRatio(1, 2), complex(100, 3)),
        (FrequencyRatio(3), 'abc'),
        (FrequencyRatio(3), SP_NON_NUMBER),
        (FrequencyRatio(5), Frequency(100)),
        (FrequencyRatio(6), complex(100, 3)),
        (FrequencyRatio(3.5), 'abc'),
        (FrequencyRatio(3.5), SP_NON_NUMBER),
        (FrequencyRatio(2.1), Frequency(100)),
        (FrequencyRatio(9.2), complex(100, 3)),
    ]
)
def test_lt_bogus(x, y):

    with pytest.raises(TypeError):
        x < y

    with pytest.raises(TypeError):
        y < x


@pytest.mark.parametrize(
    'x, y',
    [
        # ratio(int) x ratio(int)
        (FrequencyRatio(3), FrequencyRatio(3)),
        # ratio(int) x ratio(int, int)
        (FrequencyRatio(6, 3), FrequencyRatio(2)),
        # ratio(int) x ratio(float)
        (FrequencyRatio(3), FrequencyRatio(3.0)),
        # ratio(int) x ratio(Fraction)
        (
            FrequencyRatio(2),
            FrequencyRatio(Fraction(4, 2))
        ),
        # ratio(int) x int
        (FrequencyRatio(22), 22),
        # ratio(int) x float
        (FrequencyRatio(22), 22.0),
        # ratio(int) x fraction
        (FrequencyRatio(33), Fraction(66, 2)),
        # ---------------------------------------------------------------------
        # ratio(int, int) x ratio(int, int)
        (FrequencyRatio(1, 3), FrequencyRatio(1, 3)),
        # ratio(int, int) x ratio(float)
        (FrequencyRatio(1, 2), FrequencyRatio(0.5)),
        # ratio(int, int) x ratio(Fraction)
        (
            FrequencyRatio(1, 3),
            FrequencyRatio(Fraction(1, 3)),
        ),
        # ratio(int, int) x int
        (FrequencyRatio(4, 2), 2),
        # ratio(int, int) x float
        (FrequencyRatio(5, 2), 2.5),
        # ratio(int, int) x fraction
        (FrequencyRatio(1, 3), Fraction(1, 3)),
        # ---------------------------------------------------------------------
        # ratio(float) x ratio(float)
        (FrequencyRatio(0.5), FrequencyRatio(0.5)),
        # ratio(float) x ratio(Fraction)
        (
            FrequencyRatio(0.5),
            FrequencyRatio(Fraction(1, 2)),
        ),
        # ratio(float) x int
        (
            FrequencyRatio(2.0), 2
        ),
        # ratio(float) x float
        (
            FrequencyRatio(0.5), 0.5
        ),
        # ratio(float) x fraction
        (
            FrequencyRatio(0.75), Fraction(3, 4)
        ),
        # ---------------------------------------------------------------------
        # ratio(Fraction) x ratio(Fraction)
        (
            FrequencyRatio(Fraction(4, 3)),
            FrequencyRatio(Fraction(4, 3)),
        ),
        # ratio(Fraction) x int
        (FrequencyRatio(Fraction(9, 3)), 3),
        # ratio(Fraction) x float
        (FrequencyRatio(Fraction(3, 2)), 1.5),
        # ratio(Fraction) x fraction
        (
            FrequencyRatio(Fraction(1, 3)),
            Fraction(1, 3),
        ),
        # ---------------------------------------------------------------------
        # ratio(SP_NUM) x ratio(SP_NUM)
        (
            FrequencyRatio(SP_NUM),
            FrequencyRatio(SP_NUM),
        ),
        # ratio(SP_NUM) x SP_NUM
        (
            FrequencyRatio(SP_NUM),
            SP_NUM,
        ),
    ]
)
def test_eq(x, y):
    assert x == y
    assert y == x


@pytest.mark.parametrize(
    'x, y',
    [
        (FrequencyRatio(1, 2), 'abc'),
        (FrequencyRatio(1, 2), Frequency(100)),
        (FrequencyRatio(1, 2), SP_NON_NUMBER),
        (FrequencyRatio(1, 2), complex(100, 3)),
        (FrequencyRatio(3), 'abc'),
        (FrequencyRatio(3), SP_NON_NUMBER),
        (FrequencyRatio(5), Frequency(100)),
        (FrequencyRatio(6), complex(100, 3)),
        (FrequencyRatio(3.5), 'abc'),
        (FrequencyRatio(3.5), SP_NON_NUMBER),
        (FrequencyRatio(2.1), Frequency(100)),
        (FrequencyRatio(9.2), complex(100, 3)),
    ]
)
def test_eq_bogus(x, y):
    assert x != y
    assert y != x


@pytest.mark.parametrize(
    'x, as_float',
    [
        # ratio(int)
        (FrequencyRatio(3), 3.0),
        # ratio(int, int)
        (FrequencyRatio(7, 2), 3.5),
        # ratio(float)
        (FrequencyRatio(0.5), 0.5),
        # ratio(Fraction)
        (FrequencyRatio(Fraction(5, 2)), 2.5),
        # ratio(SP_NUM)
        (FrequencyRatio(SP_NUM), 1.2599210498948732),
    ]
)
def test_to_float(x, as_float):

    with pytest.raises(TypeError):
        float(x)

    assert x.to_float() == as_float


@pytest.mark.parametrize(
    'ratio, cents',
    [
        (FrequencyRatio(Fraction(3, 2)), 701.9550008654),
        (FrequencyRatio(Fraction(2, 1)), 1200),
        (FrequencyRatio(Fraction(4, 1)), 2400)
    ]
)
def test_cents(ratio, cents):
    """
    Test if cents value of ratio is calculated correctly
    """

    assert ratio.cents == cents


@pytest.mark.parametrize(
    'ratio, base, result',
    [
        (FrequencyRatio(4), 2, FrequencyRatio(2)),
        (FrequencyRatio(9), 3, FrequencyRatio(2)),
        (FrequencyRatio(125), 5, FrequencyRatio(3)),
    ]
)
def test_log(ratio, base, result):
    assert ratio.log(base) == result


@pytest.mark.parametrize(
    'monzo, expected_ratio',
    [
        (
            [1, -2, 3, 0, 0, 1],
            FrequencyRatio(Fraction(2*(5**3)*13, 3**2))
        ),
        (
            [-4, 2, 3],
            FrequencyRatio(Fraction((3**2)*(5**3), 2**4))
        ),
        (
            [2, 2, -3, 0, 0, 6, -6],
            FrequencyRatio(Fraction((2**2)*(3**2)*(13**6), (5**3)*(17**6)))
        ),
        (
            [9, 2, -3, 0, 0, -6, -6],
            FrequencyRatio(Fraction((2**9)*(3**2), (5**3)*(13**6)*(17**6))),
        )
    ]
)
def test_monzo_identity(monzo, expected_ratio):
    """
    Test if ratio generation from mondo and mondo
    factorization works correctly
    """
    ratio = FrequencyRatio.from_monzo(monzo)
    assert ratio == expected_ratio
    assert ratio.to_monzo() == monzo


def test_to_monzo_irrational():
    """
    Test if ValueError is raised when trying to factorize
    an irrational ratio
    """
    ratio = FrequencyRatio(sp.Integer(3)**sp.Rational(3, 12))

    with pytest.raises(ValueError):
        ratio.to_monzo()
