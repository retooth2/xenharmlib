import pytest
from xenharmlib.core.frequencies import Frequency


def test_get_harmonics():

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
    'monzo',
    [
        [1, -2, 3, 0, 0, 1],
        [-4, 2, 3],
        [2, 2, -3, 0, 0, 6, -6],
        [9, 2, -3, 0, 0, -6, -6],
    ]
)
def test_monzo_identity(monzo):
    freq = Frequency.from_monzo(monzo)
    assert freq.to_monzo() == monzo


@pytest.mark.parametrize(
    'frequency, cents',
    [
        (Frequency(3, 2), 701.9550008654),
        (Frequency(2, 1), 1200),
        (Frequency(4, 1), 2400)
    ]
)
def test_cents(frequency, cents):
    assert frequency.cents == cents