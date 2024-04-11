import pytest
from xenharmlib.core.frequencies import Frequency
from xenharmlib.core.tunings import EDTuning
from xenharmlib.core.pitch import EDPitch
from xenharmlib.core.pitch import PitchInterval
from xenharmlib.exc import IncompatibleTunings

edo12 = EDTuning(12, Frequency(2))
edo24 = EDTuning(24, Frequency(2))
edo31 = EDTuning(31, Frequency(2))
ed13_3 = EDTuning(13, Frequency(3))


def test_init():

    interval = PitchInterval.from_pitches(
        EDPitch(edo31, 2),
        EDPitch(edo31, 8),
    )

    interval.ref_pitch == edo31.pitch(2)
    interval.pitch_diff == 6


def test_lt_gt():

    interval_a = PitchInterval.from_pitches(
        EDPitch(edo31, 2),
        EDPitch(edo31, 8),
    )
    interval_b = PitchInterval.from_pitches(
        EDPitch(edo31, 1),
        EDPitch(edo31, 9),
    )
    assert interval_a < interval_b
    assert interval_b > interval_a


def test_eq():

    interval_a = PitchInterval.from_pitches(
        EDPitch(edo31, 6),
        EDPitch(edo31, 7),
    )
    interval_b = PitchInterval.from_pitches(
        EDPitch(edo31, 6),
        EDPitch(edo31, 7),
    )
    assert interval_a == interval_b


def test_abs():

    interval_a = PitchInterval.from_pitches(
        EDPitch(edo31, 6),
        EDPitch(edo31, 35),
    )
    interval_b = PitchInterval.from_pitches(
        EDPitch(edo31, 35),
        EDPitch(edo31, 6),
    )
    assert abs(interval_a) == abs(interval_b)
    assert abs(interval_b) == interval_a


def test_cents():

    interval = PitchInterval.from_pitches(
        EDPitch(edo12, 6),
        EDPitch(edo12, 8),
    )
    assert interval.cents == 200


def test_init_incompatible_tunings():

    with pytest.raises(IncompatibleTunings):
        PitchInterval.from_pitches(
            EDPitch(edo12, 0),
            EDPitch(edo31, 0),
        )