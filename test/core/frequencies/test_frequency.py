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
        (Frequency(Fraction(3, 2)), 701.9550008653969),
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
