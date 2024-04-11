import pytest
from xenharmlib.core.frequencies import Frequency
from xenharmlib.core.tunings import EDTuning
from xenharmlib.core.pitch import EDPitch
from xenharmlib.core.pitch import EDPitchInterval
from xenharmlib.exc import IncompatibleTunings

edo12 = EDTuning(12, Frequency(2))
edo24 = EDTuning(24, Frequency(2))
edo31 = EDTuning(31, Frequency(2))
ed13_3 = EDTuning(13, Frequency(3))

def test_init_incompatible_tunings():

    with pytest.raises(IncompatibleTunings):
        EDPitchInterval.from_pitches(
            EDPitch(edo12, 0),
            EDPitch(edo31, 0),
        )

@pytest.mark.parametrize(
    'interval, gen_pitch, distance',
    [
        (
            EDPitch(edo12, 0).interval(
                EDPitch(edo12, 14)
            ), 
            EDPitch(edo12, 7),
            2
        ),
        (
            EDPitch(edo12, 9).interval(
                EDPitch(edo12, 6)
            ), 
            EDPitch(edo12, 7),
            3
        ),
        (
            EDPitch(edo12, 6).interval(
                EDPitch(edo12, 9)
            ), 
            EDPitch(edo12, 7),
            3
        ),
        (
            EDPitch(edo31, 12).interval(
                EDPitch(edo31, 12)
            ), 
            EDPitch(edo31, 7),
            0
        ),
        (
            EDPitch(edo31, 8).interval(
                EDPitch(edo31, 12)
            ), 
            EDPitch(edo31, 1),
            4
        ),
        (
            EDPitch(edo31, 12).interval(
                EDPitch(edo31, 8)
            ), 
            EDPitch(edo31, 1),
            4
        ),
        (
            EDPitch(edo31, 0).interval(
                EDPitch(edo31, 13)
            ),
            EDPitch(edo31, 18),
            1
        ),
    ]
)
def test_get_generator_distance(interval, gen_pitch, distance):
    result = interval.get_generator_distance(gen_pitch)
    assert result == distance