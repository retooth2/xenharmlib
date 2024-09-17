from xenharmlib.core.pitch import Pitch
from xenharmlib.core.tunings import EDOTuning


def test_pitch_index():

    edo12 = EDOTuning(12)
    assert edo12.pitch(3).pitch_index == 3
    assert edo12.pitch(9).pitch_index == 9
    assert edo12.pitch(17).pitch_index == 17
    assert edo12.pitch(31).pitch_index == 31
