import pytest
import sympy as sp
from fractions import Fraction
from xenharmlib.core.frequencies import Frequency


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
    'monzo, expected_freq',
    [
        (
            [1, -2, 3, 0, 0, 1],
            Frequency(Fraction(2*(5**3)*13, 3**2))
        ),
        (
            [-4, 2, 3],
            Frequency(Fraction((3**2)*(5**3), 2**4))
        ),
        (
            [2, 2, -3, 0, 0, 6, -6],
            Frequency(Fraction((2**2)*(3**2)*(13**6), (5**3)*(17**6)))
        ),
        (
            [9, 2, -3, 0, 0, -6, -6],
            Frequency(Fraction((2**9)*(3**2), (5**3)*(13**6)*(17**6))),
        )
    ]
)
def test_monzo_identity(monzo, expected_freq):
    """
    Test if frequency generation from mondo and mondo
    factorization works correctly
    """
    freq = Frequency.from_monzo(monzo)
    assert freq == expected_freq
    assert freq.to_monzo() == monzo


@pytest.mark.parametrize(
    'frequency, cents',
    [
        (Frequency(Fraction(3, 2)), 701.9550008654),
        (Frequency(Fraction(2, 1)), 1200),
        (Frequency(Fraction(4, 1)), 2400)
    ]
)
def test_cents(frequency, cents):
    """
    Test if cents value of frequency is calculated correctly
    """

    assert frequency.cents == cents


@pytest.mark.parametrize(
    'freq, x, result',
    [
        (Frequency(3), Frequency(2), Frequency(5)),
        (Frequency(3), 2, Frequency(5)),
        (Frequency(3), 2.0, Frequency(5)),
        (Frequency(3), Fraction(3, 2), Frequency(Fraction(9, 2))),
    ]
)
def test_add(freq, x, result):
    assert freq + x == result
    assert x + freq == result


def test_add_sp():
    freq = Frequency(3)
    x = sp.Integer(2) ** sp.Rational(1, 3)
    result = Frequency(x + 3)
    assert freq + x == result


@pytest.mark.parametrize(
    'freq, x, result',
    [
        (Frequency(3), Frequency(2), Frequency(1)),
        (Frequency(3), 2, Frequency(1)),
        (Frequency(3), 2.0, Frequency(1)),
        (Frequency(3), Fraction(3, 2), Frequency(Fraction(3, 2))),
        (3, Frequency(Fraction(3, 2)), Frequency(Fraction(3, 2))),
    ]
)
def test_sub(freq, x, result):
    assert freq - x == result


def test_sub_sp():
    freq = Frequency(3)
    x = sp.Integer(2) ** sp.Rational(1, 3)
    result = Frequency(3 - x)
    assert freq - x == result


@pytest.mark.parametrize(
    'freq, x, result',
    [
        (Frequency(3), Frequency(2), Frequency(6)),
        (Frequency(3), 2, Frequency(6)),
        (Frequency(3), 2.0, Frequency(6)),
        (Frequency(3), Fraction(3, 2), Frequency(Fraction(9, 2))),
    ]
)
def test_mul(freq, x, result):
    assert freq * x == result
    assert x * freq == result


def test_mul_sp():
    freq = Frequency(3)
    x = sp.Integer(2) ** sp.Rational(1, 3)
    result = Frequency(x * 3)
    assert freq * x == result


@pytest.mark.parametrize(
    'freq, x, result',
    [
        (Frequency(3), Frequency(2), Frequency(Fraction(3, 2))),
        (Frequency(3), 2, Frequency(Fraction(3, 2))),
        (Frequency(3), 2.0, Frequency(Fraction(3, 2))),
        (Frequency(3), Fraction(3, 2), Frequency(2)),
        (3, Frequency(Fraction(3, 2)), Frequency(2)),
    ]
)
def test_truediv(freq, x, result):
    assert freq / x == result


def test_truediv_sp():
    freq = Frequency(3)
    x = sp.Integer(2) ** sp.Rational(1, 3)
    result = Frequency(3 / x)
    assert freq / x == result


@pytest.mark.parametrize(
    'freq, x, result',
    [
        (Frequency(3), Frequency(2), Frequency(1)),
        (Frequency(3), 2, Frequency(1)),
        (Frequency(3), 2.0, Frequency(1)),
        (3, Frequency(2), Frequency(1)),
    ]
)
def test_floordiv(freq, x, result):
    assert freq // x == result


def test_floordiv_sp():
    freq = Frequency(3)
    x = sp.Integer(2) ** sp.Rational(1, 3)
    result = Frequency(3 // x)
    assert freq // x == result


@pytest.mark.parametrize(
    'freq, x, result',
    [
        (Frequency(3), Frequency(2), Frequency(1)),
        (Frequency(3), 2, Frequency(1)),
        (Frequency(3), 2.0, Frequency(1)),
        (3, Frequency(2), Frequency(1)),
    ]
)
def test_mod(freq, x, result):
    assert freq % x == result


def test_mod_sp():
    freq = Frequency(3)
    x = sp.Integer(2) ** sp.Rational(1, 3)
    result = Frequency(3 % x)
    assert freq % x == result


@pytest.mark.parametrize(
    'freq, x, result',
    [
        (Frequency(3), Frequency(2), Frequency(9)),
        (Frequency(3), 2, Frequency(9)),
        (Frequency(3), 2.0, Frequency(9)),
        (Frequency(3), Fraction(3, 2),
         Frequency(sp.Integer(3)**Fraction(3, 2))),
        (3, Frequency(2), Frequency(9)),
    ]
)
def test_pow(freq, x, result):
    assert freq ** x == result


def test_pow_sp():
    freq = Frequency(3)
    x = sp.Integer(2) ** sp.Rational(1, 3)
    result = Frequency(3 ** x)
    assert freq ** x == result


@pytest.mark.parametrize(
    'freq, result',
    [
        (Frequency(3), Frequency(3)),
        (Frequency(-2), Frequency(2)),
        (Frequency(-sp.Integer(3)**Fraction(3, 2)),
         Frequency(sp.Integer(3)**Fraction(3, 2))),
    ]
)
def test_abs(freq, result):
    assert abs(freq) == result


@pytest.mark.parametrize(
    'freq_a, freq_b',
    [
        (Frequency(3), 3),
        (Frequency(-6), Frequency(-6)),
        (Frequency(sp.Integer(3)*Fraction(3, 2)),
         Frequency(Fraction(9, 2))),
    ]
)
def test_eq(freq_a, freq_b):
    assert freq_a == freq_b
    assert freq_b == freq_a


@pytest.mark.parametrize(
    'freq_a, freq_b',
    [
        (Frequency(2), Frequency(3)),
        (Frequency(2), 3),
        (Frequency(2), Fraction(5, 2)),
        (Frequency(3), 6.4),
        (Frequency(3), sp.Integer(3)**Fraction(10, 3)),
    ]
)
def test_lt_gt(freq_a, freq_b):
    assert freq_a < freq_b
    assert freq_b > freq_a


@pytest.mark.parametrize(
    'freq, result',
    [
        (Frequency(3), 3.0),
        (Frequency(sp.Integer(3)**Fraction(10, 3)), 38.94073839830003),
        (Frequency(Fraction(3, 2)), 1.5),
    ]
)
def test_float(freq, result):
    assert float(freq) == result


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
    'freq, base, result',
    [
        (Frequency(4), 2, Frequency(2)),
        (Frequency(9), 3, Frequency(2)),
        (Frequency(125), 5, Frequency(3)),
    ]
)
def test_log(freq, base, result):
    assert freq.log(base) == result


@pytest.mark.parametrize(
    'freq, result',
    [
        (Frequency(3), Frequency(3)),
        (Frequency(Fraction(3, 2)), Frequency(3)),
        (Frequency(Fraction(2.5)), Frequency(5)),
    ]
)
def test_numerator(freq, result):
    assert freq.numerator == result


@pytest.mark.parametrize(
    'freq, result',
    [
        (Frequency(3), Frequency(1)),
        (Frequency(Fraction(3, 2)), Frequency(2)),
        (Frequency(Fraction(2.5)), Frequency(2)),
    ]
)
def test_denominator(freq, result):
    assert freq.denominator == result


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
        complex(2, 3)
    ]
)
def test_inconvertible_bool_complex(inconvertible):
    """
    Test if correct error is raised when __init__ or
    arithmetic functions receive a bool or complex number
    """

    with pytest.raises(ValueError):
        Frequency(inconvertible)

    with pytest.raises(ValueError):
        Frequency(3) + inconvertible

    with pytest.raises(ValueError):
        inconvertible + Frequency(3)

    with pytest.raises(ValueError):
        Frequency(3) - inconvertible

    with pytest.raises(ValueError):
        inconvertible - Frequency(3)

    with pytest.raises(ValueError):
        Frequency(3) * inconvertible

    with pytest.raises(ValueError):
        inconvertible * Frequency(3)

    with pytest.raises(ValueError):
        Frequency(3) / inconvertible

    with pytest.raises(ValueError):
        inconvertible / Frequency(3)

    with pytest.raises(ValueError):
        Frequency(3) // inconvertible

    with pytest.raises(ValueError):
        inconvertible // Frequency(3)

    with pytest.raises(ValueError):
        Frequency(3) % inconvertible

    with pytest.raises(ValueError):
        inconvertible % Frequency(3)

    with pytest.raises(ValueError):
        Frequency(3) ** inconvertible

    with pytest.raises(ValueError):
        inconvertible ** Frequency(3)

    with pytest.raises(ValueError):
        Frequency(3) < inconvertible

    with pytest.raises(ValueError):
        inconvertible < Frequency(3)

    with pytest.raises(ValueError):
        Frequency(3) > inconvertible

    with pytest.raises(ValueError):
        inconvertible > Frequency(3)

    with pytest.raises(ValueError):
        Frequency(3) <= inconvertible

    with pytest.raises(ValueError):
        inconvertible <= Frequency(3)

    with pytest.raises(ValueError):
        Frequency(3) >= inconvertible

    with pytest.raises(ValueError):
        inconvertible >= Frequency(3)

    with pytest.raises(ValueError):
        Frequency(3) == inconvertible

    with pytest.raises(ValueError):
        inconvertible == Frequency(3)

    with pytest.raises(ValueError):
        Frequency(3).log(inconvertible)


def test_inconvertible_string():
    """
    Test if correct error is raised when __init__ or
    arithmetic functions receive a string
    """

    inconvertible = 'abcdef'

    with pytest.raises(ValueError):
        Frequency(inconvertible)

    with pytest.raises(ValueError):
        Frequency(3) + inconvertible

    with pytest.raises(ValueError):
        inconvertible + Frequency(3)

    with pytest.raises(ValueError):
        Frequency(3) - inconvertible

    with pytest.raises(ValueError):
        inconvertible - Frequency(3)

    with pytest.raises(ValueError):
        Frequency(3) * inconvertible

    with pytest.raises(ValueError):
        inconvertible * Frequency(3)

    with pytest.raises(ValueError):
        Frequency(3) / inconvertible

    with pytest.raises(ValueError):
        inconvertible / Frequency(3)

    with pytest.raises(ValueError):
        Frequency(3) // inconvertible

    with pytest.raises(ValueError):
        inconvertible // Frequency(3)

    with pytest.raises(ValueError):
        Frequency(3) % inconvertible

    with pytest.raises(ValueError):
        Frequency(3) ** inconvertible

    with pytest.raises(ValueError):
        inconvertible ** Frequency(3)

    with pytest.raises(ValueError):
        Frequency(3) < inconvertible

    with pytest.raises(ValueError):
        inconvertible < Frequency(3)

    with pytest.raises(ValueError):
        Frequency(3) > inconvertible

    with pytest.raises(ValueError):
        inconvertible > Frequency(3)

    with pytest.raises(ValueError):
        Frequency(3) <= inconvertible

    with pytest.raises(ValueError):
        inconvertible <= Frequency(3)

    with pytest.raises(ValueError):
        Frequency(3) >= inconvertible

    with pytest.raises(ValueError):
        inconvertible >= Frequency(3)

    with pytest.raises(ValueError):
        Frequency(3) == inconvertible

    with pytest.raises(ValueError):
        inconvertible == Frequency(3)

    with pytest.raises(ValueError):
        Frequency(3).log(inconvertible)


def test_inconvertible_sp_expr():
    """
    Test if correct error is raised when __init__ or
    arithmetic functions receive a sympy expression
    that is not a number
    """

    x, y = sp.symbols('x y')
    inconvertible = x**2*2*y

    with pytest.raises(ValueError):
        Frequency(inconvertible)

    with pytest.raises(ValueError):
        Frequency(3) + inconvertible

    with pytest.raises(ValueError):
        Frequency(3) - inconvertible

    with pytest.raises(ValueError):
        Frequency(3) * inconvertible

    with pytest.raises(ValueError):
        Frequency(3) / inconvertible

    with pytest.raises(ValueError):
        Frequency(3) // inconvertible

    with pytest.raises(ValueError):
        Frequency(3) % inconvertible

    with pytest.raises(ValueError):
        Frequency(3) ** inconvertible

    with pytest.raises(ValueError):
        Frequency(3) < inconvertible

    with pytest.raises(ValueError):
        Frequency(3) > inconvertible

    with pytest.raises(ValueError):
        Frequency(3) <= inconvertible

    with pytest.raises(ValueError):
        Frequency(3) >= inconvertible

    with pytest.raises(ValueError):
        Frequency(3) == inconvertible

    with pytest.raises(ValueError):
        Frequency(3).log(inconvertible)
