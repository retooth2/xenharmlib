from xenharmlib.core.pitch import Pitch
from xenharmlib.core.tunings import EDOTuning


def test_pitch_index():

    edo12 = EDOTuning(12)
    assert Pitch(edo12, 3).pitch_index == 3
    assert Pitch(edo12, 9).pitch_index == 9
    assert Pitch(edo12, 17).pitch_index == 17
    assert Pitch(edo12, 31).pitch_index == 31
