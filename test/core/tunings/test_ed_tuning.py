import pytest
import sympy as sp
from fractions import Fraction

from xenharmlib.core.tunings import EDTuning
from xenharmlib.core.frequencies import Frequency
from xenharmlib.core.frequencies import FrequencyRatio
from xenharmlib.exc import IncompatibleOriginContexts
from xenharmlib.exc import InvalidFrequency

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
