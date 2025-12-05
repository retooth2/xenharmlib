import pytest
from xenharmlib.core.frequencies import FrequencyRatio
from xenharmlib import EDTuning
from xenharmlib.tuning.ed import EDPitch
from xenharmlib.tuning.ed import EDPitchInterval
from xenharmlib.exc import IncompatibleOriginContexts

edo12 = EDTuning(12, FrequencyRatio(2))
edo24 = EDTuning(24, FrequencyRatio(2))
edo31 = EDTuning(31, FrequencyRatio(2))
ed13_3 = EDTuning(13, FrequencyRatio(3))

def test_init_incompatible_origin_contexts():
    """
    Test if interval cannot be initialized from two pitches
    that originate from different tunings
    """

    edo12_2 = EDTuning(12, FrequencyRatio(2))

    with pytest.raises(IncompatibleOriginContexts):
        with pytest.deprecated_call():
            EDPitchInterval.from_pitches(
                edo12.pitch(0),
                edo12_2.pitch(0),
            )

    with pytest.raises(IncompatibleOriginContexts):
        EDPitchInterval.from_source_and_target(
            edo12.pitch(0),
            edo12_2.pitch(0),
        )

@pytest.mark.parametrize(
    'interval, gen_pitch, distance',
    [
        (
            edo12.pitch(0).interval(
                edo12.pitch(14)
            ), 
            edo12.pitch(7),
            2
        ),
        (
            edo12.pitch(9).interval(
                edo12.pitch(6)
            ), 
            edo12.pitch(7),
            3
        ),
        (
            edo12.pitch(6).interval(
                edo12.pitch(9)
            ), 
            edo12.pitch(7),
            3
        ),
        (
            edo31.pitch(12).interval(
                edo31.pitch(12)
            ), 
            edo31.pitch(7),
            0
        ),
        (
            edo31.pitch(8).interval(
                edo31.pitch(12)
            ), 
            edo31.pitch(1),
            4
        ),
        (
            edo31.pitch(12).interval(
                edo31.pitch(8)
            ), 
            edo31.pitch(1),
            4
        ),
        (
            edo31.pitch(0).interval(
                edo31.pitch(13)
            ),
            edo31.pitch(18),
            1
        ),
    ]
)
def test_get_generator_distance(interval, gen_pitch, distance):
    """
    Test if get_generator_distance calculates the
    correct distance for the interval
    """

    result = interval.get_generator_distance(gen_pitch)
    assert result == distance
