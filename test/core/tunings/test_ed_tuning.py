import pytest
import sympy as sp

from xenharmlib.core.tunings import EDTuning
from xenharmlib.core.frequencies import Frequency
from xenharmlib.core.frequencies import FrequencyRatio
from xenharmlib.exc import IncompatibleOriginContexts
from xenharmlib.exc import InvalidPitchClassIndex

FREQ_EPSILON = 0.1
FREQ_RATIO_EPSILON = 0.1


@pytest.mark.parametrize(
    'tuning, pitch_index, freq',
    [
        (
            EDTuning(12, FrequencyRatio(2)),
            9+12*4,
            Frequency(440)
        ),
        (
            EDTuning(13, FrequencyRatio(3), ref_frequency=Frequency(20)),
            17,
            Frequency(sp.Integer(60) * sp.Integer(3) ** sp.Rational(4, 13))
        ),
        (
            EDTuning(13, FrequencyRatio(3), ref_frequency=Frequency(50)),
            27,
            Frequency(sp.Integer(450) * sp.Integer(3) ** sp.Rational(1, 13))
        )
    ]
)
def test_get_frequency(tuning, pitch_index, freq):
    pitch = tuning.pitch(pitch_index)
    assert pitch.frequency == freq


def test_get_frequency_deprecated():

    tuning = EDTuning(12, FrequencyRatio(2))
    pitch = tuning.pitch(33)

    with pytest.deprecated_call():
        assert tuning.get_frequency(pitch)


def test_get_frequency_incompatible_origin_contexts():

    edo12 = EDTuning(12, FrequencyRatio(2))
    edo12_2 = EDTuning(12, FrequencyRatio(2))

    edo12_pitch = edo12.pitch(8)

    with pytest.raises(IncompatibleOriginContexts):
        with pytest.deprecated_call():
            edo12_2.get_frequency(edo12_pitch)


@pytest.mark.parametrize(
    'tuning, pitch_index, freq',
    [
        (
            EDTuning(12, FrequencyRatio(2)),
            9+12*4,
            Frequency(440)
        ),
        (
            EDTuning(12, FrequencyRatio(2)),
            -12,
            Frequency(8.175)
        ),
        (
            EDTuning(12, FrequencyRatio(2)),
            6,
            Frequency(16.3) * FrequencyRatio(3**6, 2**9)
        ),
        (
            EDTuning(12, FrequencyRatio(2)),
            6,
            Frequency(16.35) * (FrequencyRatio(2)**(1/12))**6
        ),
        (
            EDTuning(13, FrequencyRatio(3), ref_frequency=Frequency(16.3)),
            17,
            Frequency(68.6)
        ),
        (
            EDTuning(13, FrequencyRatio(3), ref_frequency=Frequency(16.3)),
            27,
            Frequency(159.6)
        ),
    ]
)
def test_closest_freq_repr(tuning, pitch_index, freq):

    with pytest.deprecated_call():
        pitch = tuning.get_approx_pitch(freq)

    assert pitch.pitch_index == pitch_index
    assert (pitch.frequency - freq) < Frequency(FREQ_EPSILON)

    pitch = tuning.closest_freq_repr(freq)

    assert pitch.pitch_index == pitch_index
    assert abs(pitch.frequency - freq) < Frequency(FREQ_EPSILON)


@pytest.mark.parametrize(
    'tuning, ratio, pitch_diff',
    [
        (
            EDTuning(12, FrequencyRatio(2)),
            FrequencyRatio(3, 2),
            7
        ),
        (
            EDTuning(12, FrequencyRatio(2)),
            FrequencyRatio(2, 3),
            -7
        ),
        (
            EDTuning(12, FrequencyRatio(2)),
            FrequencyRatio(1, 1),
            0,
        ),
        (
            EDTuning(12, FrequencyRatio(2)),
            FrequencyRatio(20_000, 20_001),
            0,
        ),
        (
            EDTuning(12, FrequencyRatio(2)),
            FrequencyRatio(8, 9),
            -2
        ),
        (
            EDTuning(24, FrequencyRatio(2)),
            FrequencyRatio(8, 9),
            -4
        ),
        (
            EDTuning(24, FrequencyRatio(2)),
            FrequencyRatio(5, 4),
            8
        ),
        (
            EDTuning(13, FrequencyRatio(3)),
            FrequencyRatio(300, 101),
            13,
        ),
    ]
)
def test_closest_interval(tuning, ratio, pitch_diff):

    exp_interval = tuning.diff_interval(pitch_diff)
    interval = tuning.closest_interval(ratio)

    assert interval == exp_interval
    assert abs(
        interval.frequency_ratio - exp_interval.frequency_ratio
    ) < FrequencyRatio(FREQ_RATIO_EPSILON)


@pytest.mark.parametrize(
    'tuning, frequencies',
    [
        (
            EDTuning(12, FrequencyRatio(2)),
            [Frequency(230), Frequency(300), Frequency(440), Frequency(500)]
        ),
        (
            EDTuning(12, FrequencyRatio(2)),
            [Frequency(170), Frequency(120), Frequency(230), Frequency(340)]
        ),
        (
            EDTuning(31, FrequencyRatio(2)),
            [Frequency(16), Frequency(32), Frequency(90), Frequency(150)]
        ),
        (
            EDTuning(13, FrequencyRatio(3), ref_frequency=Frequency(16.3)),
            [Frequency(99), Frequency(999), Frequency(9999), Frequency(99999)]
        ),
    ]
)
def test_closest_scale(tuning, frequencies):

    # do simple invariance test

    exp_scale = tuning.scale()

    for frequency in frequencies:
        pitch = tuning.closest_freq_repr(frequency)
        exp_scale = exp_scale.with_element(pitch)

    assert tuning.closest_scale(frequencies) == exp_scale


@pytest.mark.parametrize(
    'tuning, ratios',
    [
        (
            EDTuning(12, FrequencyRatio(2)),
            [
                FrequencyRatio(5, 4),
                FrequencyRatio(3, 2),
                FrequencyRatio(2, 1),
            ]
        ),
        (
            EDTuning(12, FrequencyRatio(2)),
            [
                FrequencyRatio(9, 10),
                FrequencyRatio(10, 9),
                FrequencyRatio(3, 2),
                FrequencyRatio(4, 9),
            ]
        ),
        (
            EDTuning(13, FrequencyRatio(3)),
            [
                FrequencyRatio(3, 2),
                FrequencyRatio(4, 9),
                FrequencyRatio(4, 9),
                FrequencyRatio(9, 10),
                FrequencyRatio(10, 9),
            ]
        ),
        (
            EDTuning(31, FrequencyRatio(2)),
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
def test_closest_interval_seq(tuning, ratios):

    # do simple invariance test

    exp_interval_seq = tuning.interval_seq()

    for frequency in ratios:
        interval = tuning.closest_interval(frequency)
        exp_interval_seq = exp_interval_seq.with_interval(interval)

    assert tuning.closest_interval_seq(ratios) == exp_interval_seq


@pytest.mark.parametrize(
    'tuning, ratios',
    [
        (
            EDTuning(12, FrequencyRatio(2)),
            [
                FrequencyRatio(5, 4),
                FrequencyRatio(3, 2),
                FrequencyRatio(2, 1),
            ]
        ),
        (
            EDTuning(12, FrequencyRatio(2)),
            [
                FrequencyRatio(9, 10),
                FrequencyRatio(10, 9),
                FrequencyRatio(3, 2),
                FrequencyRatio(4, 9),
            ]
        ),
        (
            EDTuning(13, FrequencyRatio(3)),
            [
                FrequencyRatio(3, 2),
                FrequencyRatio(4, 9),
                FrequencyRatio(4, 9),
                FrequencyRatio(9, 10),
                FrequencyRatio(10, 9),
            ]
        ),
        (
            EDTuning(31, FrequencyRatio(2)),
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
def test_closest_interval_fan(tuning, ratios):

    # do simple invariance test

    exp_interval_fan = tuning.interval_fan()

    for frequency in ratios:
        interval = tuning.closest_interval(frequency)
        exp_interval_fan = exp_interval_fan.with_interval(interval)

    assert tuning.closest_interval_fan(ratios) == exp_interval_fan


@pytest.mark.parametrize(
    'tuning, frequencies',
    [
        (
            EDTuning(12, FrequencyRatio(2)),
            [Frequency(230), Frequency(300), Frequency(440), Frequency(500)]
        ),
        (
            EDTuning(12, FrequencyRatio(2)),
            [Frequency(170), Frequency(120), Frequency(230), Frequency(340)]
        ),
        (
            EDTuning(31, FrequencyRatio(2)),
            [Frequency(16), Frequency(32), Frequency(90), Frequency(150)]
        ),
        (
            EDTuning(13, FrequencyRatio(3), ref_frequency=Frequency(16.3)),
            [Frequency(99), Frequency(999), Frequency(9999), Frequency(99999)]
        ),
    ]
)
def test_closest_seq(tuning, frequencies):

    # do simple invariance test

    exp_seq = tuning.seq()

    for frequency in frequencies:
        pitch = tuning.closest_freq_repr(frequency)
        exp_seq = exp_seq.with_element(pitch)

    assert tuning.closest_seq(frequencies) == exp_seq


@pytest.mark.parametrize(
    'tuning, generator_pitch_indices',
    [
        (
            EDTuning(12, FrequencyRatio(2)),
            [1, 5, 7, 11]
        ),
        (
            EDTuning(13, FrequencyRatio(3), ref_frequency=Frequency(16.3)),
            list(range(1, 13)),
        )
    ]
)
def test_generator_pitches(tuning, generator_pitch_indices):
    gen_pitches = tuning.generator_pitches
    assert generator_pitch_indices == [
        pitch.pitch_index for pitch in gen_pitches
    ]


@pytest.mark.parametrize(
    'tuning, pc_indices, expected',
    [
        (
            EDTuning(12, FrequencyRatio(2)),
            [],
            []
        ),
        (
            EDTuning(12, FrequencyRatio(2)),
            [3],
            [3]
        ),
        (
            EDTuning(12, FrequencyRatio(2)),
            [7, 9, 3, 5],
            [7, 9, 15, 17]
        ),
        (
            EDTuning(12, FrequencyRatio(2)),
            [3, 3, 3, 3],
            [3, 15, 27, 39]
        ),
        (
            EDTuning(24, FrequencyRatio(2)),
            [3, 6, 10, 16],
            [3, 6, 10, 16]
        ),
    ]
)
def test_pc_scale(tuning, pc_indices, expected):

    scale = tuning.pc_scale(pc_indices)
    assert scale == tuning.scale(
        [tuning.pitch(i) for i in expected]
    )


@pytest.mark.parametrize(
    'tuning, pc_indices',
    [
        (
            EDTuning(12, FrequencyRatio(2)),
            [12]
        ),
        (
            EDTuning(12, FrequencyRatio(2)),
            [3, 4, 14, 3],
        ),
        (
            EDTuning(24, FrequencyRatio(2)),
            [3, 6, 10, 16, 25],
        ),
    ]
)
def test_pc_scale_invalid_pci(tuning, pc_indices):

    with pytest.raises(InvalidPitchClassIndex):
        tuning.pc_scale(pc_indices)


@pytest.mark.parametrize(
    'tuning, pc_indices, root_bi_index, expected',
    [
        (
            EDTuning(12, FrequencyRatio(2)),
            [7, 9, 3, 5],
            4,
            [7+48, 9+48, 3+60, 5+60]
        ),
        (
            EDTuning(31, FrequencyRatio(2)),
            [3, 6, 10, 16],
            2,
            [3+62, 6+62, 10+62, 16+62]
        ),
    ]
)
def test_pc_scale_root_bi_index(tuning, pc_indices, root_bi_index, expected):

    scale = tuning.pc_scale(pc_indices, root_bi_index)
    assert scale == tuning.scale(
        [tuning.pitch(i) for i in expected]
    )


@pytest.mark.parametrize(
    'tuning, indices, expected',
    [
        (
            EDTuning(12, FrequencyRatio(2)),
            [],
            []
        ),
        (
            EDTuning(12, FrequencyRatio(2)),
            [3],
            [3]
        ),
        (
            EDTuning(12, FrequencyRatio(2)),
            [7, 9, 3, 5],
            [3, 5, 7, 9]
        ),
        (
            EDTuning(12, FrequencyRatio(2)),
            [3, 3, 3, 3],
            [3]
        ),
        (
            EDTuning(24, FrequencyRatio(2)),
            [3, 6, 10, 16],
            [3, 6, 10, 16]
        ),
    ]
)
def test_index_scale(tuning, indices, expected):

    scale = tuning.index_scale(indices)
    assert scale == tuning.scale(
        [tuning.pitch(i) for i in expected]
    )


@pytest.mark.parametrize(
    'tuning, pitch_diff',
    [
        (EDTuning(12, FrequencyRatio(2)), 3),
        (EDTuning(24, FrequencyRatio(2)), 0),
        (EDTuning(22, FrequencyRatio(2)), -1),
        (EDTuning(31, FrequencyRatio(2)), -9),
        (EDTuning(14, FrequencyRatio(2)), 18)
    ]
)
def test_diff_interval(tuning, pitch_diff):

    created = tuning.diff_interval(pitch_diff)
    pitch_a = tuning.pitch(10)
    pitch_b = tuning.pitch(10 + pitch_diff)
    expected = pitch_a.interval(pitch_b)

    assert created == expected


def test_len_deprecated():

    tuning = EDTuning(12, FrequencyRatio(3))
    with pytest.deprecated_call():
        len(tuning)
