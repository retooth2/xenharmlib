import pytest

from xenharmlib.core.tunings import EDTuning
from xenharmlib.core.frequencies import Frequency
from xenharmlib.exc import IncompatibleTunings
from xenharmlib.exc import InvalidFrequency

FREQ_EPSILON = 0.1


@pytest.mark.parametrize(
    'tuning, pitch_index, freq',
    [
        (
            EDTuning('12edo', 12, Frequency(2)), 
            9+12*4, 
            440
        ),
        (
            EDTuning('13ed3', 13, Frequency(3), ref_frequency=Frequency(16.3)),
            17,
            68.6
        ),
        (
            EDTuning('13ed3', 13, Frequency(3), ref_frequency=Frequency(16.3)),
            27,
            159.6
        )
    ]
)
def test_get_frequency(tuning, pitch_index, freq):
    pitch = tuning.pitch(pitch_index)
    assert (float(pitch.frequency) - freq) < FREQ_EPSILON
    assert (float(tuning.get_frequency(pitch) - freq)) < FREQ_EPSILON


def test_get_frequency_incompatible_tunings():

    edo12 = EDTuning('12-EDO', 12, Frequency(2))
    edo31 = EDTuning('31-EDO', 31, Frequency(2))

    edo12_pitch = edo12.pitch(8)

    with pytest.raises(IncompatibleTunings):
        edo31.get_frequency(edo12_pitch)


@pytest.mark.parametrize(
    'tuning, pitch_index, freq',
    [
        (
            EDTuning('12edo', 12, Frequency(2)), 
            9+12*4, 
            440
        ),
        (
            EDTuning('12edo', 12, Frequency(2)),
            -12,
            8.175
        ),
        (
            EDTuning('13edo', 12, Frequency(2)),
            6,
            Frequency(16.3) * Frequency(3**6, 2**9)
        ),
        (
            EDTuning('13edo', 12, Frequency(2)),
            6,
            Frequency(16.35) * (Frequency(2)**(1/12))**6
        ),
        (
            EDTuning('13ed3', 13, Frequency(3), ref_frequency=Frequency(16.3)),
            17,
            68.6
        ),
        (
            EDTuning('13ed3', 13, Frequency(3), ref_frequency=Frequency(16.3)),
            27,
            159.6
        ),
    ]
)
def test_get_approx_pitch(tuning, pitch_index, freq):
    pitch = tuning.get_approx_pitch(freq)
    assert pitch.pitch_index == pitch_index
    assert (float(pitch.frequency) - freq) < FREQ_EPSILON


@pytest.mark.parametrize(
    'tuning, generator_pitch_indices',
    [
        (
            EDTuning('12edo', 12, Frequency(2)), 
            [1, 5, 7, 11] 
        ),
        (
            EDTuning('13ed3', 13, Frequency(3), ref_frequency=Frequency(16.3)),
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
    'tuning, generator_pitch_indices',
    [
        (
            EDTuning('12edo', 12, Frequency(2)), 
            [1, 5, 7, 11] 
        ),
        (
            EDTuning('13ed3', 13, Frequency(3), ref_frequency=Frequency(16.3)),
            list(range(1, 13)),
        )
    ]
)
def test_generator_pitches(tuning, generator_pitch_indices):
    gen_pitches = tuning.generator_pitches
    assert generator_pitch_indices == [
        pitch.pitch_index for pitch in gen_pitches
    ]