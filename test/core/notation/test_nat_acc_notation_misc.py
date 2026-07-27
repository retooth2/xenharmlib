import pytest
from xenharmlib import EDOTuning
from xenharmlib import Frequency
from xenharmlib import FrequencyRatio
from xenharmlib.exc import InvalidIntervalNumber
from ..utils import make_nat_acc_test_notation
from ..utils import MyNatAccNotation

FREQ_EPSILON = 0.1
FREQ_RATIO_EPSILON = 0.1

edo12 = EDOTuning(12)
notation_12 = make_nat_acc_test_notation(edo12)
edo31 = EDOTuning(31)
notation_31 = make_nat_acc_test_notation(edo31)


def test_invalid_interval_number():

    tuning = EDOTuning(12)
    notation = MyNatAccNotation(tuning, acc_weights=(1,))

    notation.append_natural('C', 3)

    with pytest.raises(InvalidIntervalNumber):
        notation.interval_number_to_nat_diff(0)


@pytest.mark.parametrize(
    'notation, freq, exp_note',
    [
        (
            notation_12,
            Frequency(440),
            notation_12.note('E+', 4)
        ),
        (
            notation_31,
            Frequency(8.175),
            notation_31.note('A', -1)
        ),
    ]
)
def test_closest_freq_repr(notation, freq, exp_note):

    note = notation.closest_freq_repr(freq)

    assert note.is_notated_same(exp_note)
    assert abs(note.frequency - freq) < Frequency(FREQ_EPSILON)


@pytest.mark.parametrize(
    'notation, ratio, exp_interval',
    [
        (
            notation_12,
            FrequencyRatio(1, 1),
            notation_12.shorthand_interval('F', 1)
        ),
        (
            notation_12,
            FrequencyRatio(3, 2),
            notation_12.shorthand_interval('+C', 4)
        ),
        (
            notation_31,
            FrequencyRatio(3, 2),
            notation_31.shorthand_interval('C', 10)
        ),
    ]
)
def test_closest_interval(notation, ratio, exp_interval):

    interval = notation.closest_interval(ratio)

    assert interval.is_notated_same(exp_interval)
    assert abs(
        interval.frequency_ratio - ratio
    ) < FrequencyRatio(FREQ_RATIO_EPSILON)


@pytest.mark.parametrize(
    'notation, frequencies',
    [
        (
            notation_12,
            [Frequency(230), Frequency(300), Frequency(440), Frequency(500)]
        ),
        (
            notation_12,
            [Frequency(170), Frequency(120), Frequency(230), Frequency(340)]
        ),
        (
            notation_31,
            [Frequency(16), Frequency(32), Frequency(90), Frequency(150)]
        ),
        (
            notation_31,
            [Frequency(99), Frequency(999), Frequency(9999), Frequency(99999)]
        ),
    ]
)
def test_closest_scale(notation, frequencies):

    # do simple invariance test

    exp_scale = notation.scale()

    for frequency in frequencies:
        pitch = notation.closest_freq_repr(frequency)
        exp_scale = exp_scale.with_element(pitch)

    assert notation.closest_scale(frequencies) == exp_scale


@pytest.mark.parametrize(
    'notation, ratios',
    [
        (
            notation_12,
            [
                FrequencyRatio(5, 4),
                FrequencyRatio(3, 2),
                FrequencyRatio(2, 1),
            ]
        ),
        (
            notation_12,
            [
                FrequencyRatio(9, 10),
                FrequencyRatio(10, 9),
                FrequencyRatio(3, 2),
                FrequencyRatio(4, 9),
            ]
        ),
        (
            notation_31,
            [
                FrequencyRatio(3, 2),
                FrequencyRatio(4, 9),
                FrequencyRatio(4, 9),
                FrequencyRatio(9, 10),
                FrequencyRatio(10, 9),
            ]
        ),
        (
            notation_31,
            [
                FrequencyRatio(9, 10),
                FrequencyRatio(9, 5),
                FrequencyRatio(10, 9),
                FrequencyRatio(4, 9),
                FrequencyRatio(3, 2),
                FrequencyRatio(4, 9),
                FrequencyRatio(9, 5),
            ]
        ),
    ]
)
def test_closest_interval_seq(notation, ratios):

    # do simple invariance test

    exp_interval_seq = notation.interval_seq()

    for frequency in ratios:
        interval = notation.closest_interval(frequency)
        exp_interval_seq = exp_interval_seq.with_interval(interval)

    assert notation.closest_interval_seq(ratios) == exp_interval_seq


@pytest.mark.parametrize(
    'notation, ratios',
    [
        (
            notation_12,
            [
                FrequencyRatio(5, 4),
                FrequencyRatio(3, 2),
                FrequencyRatio(2, 1),
            ]
        ),
        (
            notation_12,
            [
                FrequencyRatio(9, 10),
                FrequencyRatio(10, 9),
                FrequencyRatio(3, 2),
                FrequencyRatio(4, 9),
            ]
        ),
        (
            notation_12,
            [
                FrequencyRatio(3, 2),
                FrequencyRatio(4, 9),
                FrequencyRatio(4, 9),
                FrequencyRatio(9, 10),
                FrequencyRatio(10, 9),
            ]
        ),
        (
            notation_31,
            [
                FrequencyRatio(9, 10),
                FrequencyRatio(9, 5),
                FrequencyRatio(10, 9),
                FrequencyRatio(4, 9),
                FrequencyRatio(3, 2),
                FrequencyRatio(4, 9),
                FrequencyRatio(9, 5),
            ]
        ),
    ]
)
def test_closest_interval_fan(notation, ratios):

    # do simple invariance test

    exp_interval_fan = notation.interval_fan()

    for frequency in ratios:
        interval = notation.closest_interval(frequency)
        exp_interval_fan = exp_interval_fan.with_interval(interval)

    assert notation.closest_interval_fan(ratios) == exp_interval_fan


@pytest.mark.parametrize(
    'notation, frequencies',
    [
        (
            notation_12,
            [Frequency(230), Frequency(300), Frequency(440), Frequency(500)]
        ),
        (
            notation_12,
            [Frequency(170), Frequency(120), Frequency(230), Frequency(340)]
        ),
        (
            notation_31,
            [Frequency(16), Frequency(32), Frequency(90), Frequency(150)]
        ),
        (
            notation_31,
            [Frequency(99), Frequency(999), Frequency(9999), Frequency(99999)]
        ),
    ]
)
def test_closest_seq(notation, frequencies):

    # do simple invariance test

    exp_seq = notation.seq()

    for frequency in frequencies:
        pitch = notation.closest_freq_repr(frequency)
        exp_seq = exp_seq.with_element(pitch)

    assert notation.closest_seq(frequencies) == exp_seq
