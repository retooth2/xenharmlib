import pytest
import sympy as sp

from xenharmlib import EDTuning
from xenharmlib.core.frequencies import Frequency
from xenharmlib.core.frequencies import FrequencyRatio
from xenharmlib.exc import IncompatibleOriginContexts
from xenharmlib.exc import InvalidPitchClassIndex

FREQ_EPSILON = 0.1


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
    assert tuning.get_frequency(pitch) == freq


def test_get_frequency_incompatible_origin_contexts():

    edo12 = EDTuning(12, FrequencyRatio(2))
    edo12_2 = EDTuning(12, FrequencyRatio(2))

    edo12_pitch = edo12.pitch(8)

    with pytest.raises(IncompatibleOriginContexts):
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
def test_get_approx_pitch(tuning, pitch_index, freq):
    pitch = tuning.get_approx_pitch(freq)
    assert pitch.pitch_index == pitch_index
    assert (pitch.frequency - freq) < Frequency(FREQ_EPSILON)


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
