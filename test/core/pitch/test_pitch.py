from xenharmlib import EDOTuning


def test_pitch_index():

    edo12 = EDOTuning(12)
    assert edo12.pitch(3).pitch_index == 3
    assert edo12.pitch(9).pitch_index == 9
    assert edo12.pitch(17).pitch_index == 17
    assert edo12.pitch(31).pitch_index == 31


def test_pitch_reflection():

    edo12 = EDOTuning(12)
    assert edo12.pitch(0).reflection() == edo12.pitch(0)
    assert edo12.pitch(3).reflection() == edo12.pitch(-3)
    assert edo12.pitch(19).reflection() == edo12.pitch(-19)
    assert edo12.pitch(-5).reflection() == edo12.pitch(5)
    assert edo12.pitch(-20).reflection() == edo12.pitch(20)

    axis = edo12.pitch(3)

    assert edo12.pitch(0).reflection(axis) == edo12.pitch(6)
    assert edo12.pitch(3).reflection(axis) == edo12.pitch(3)
    assert edo12.pitch(19).reflection(axis) == edo12.pitch(-13)
    assert edo12.pitch(-5).reflection(axis) == edo12.pitch(11)
    assert edo12.pitch(-20).reflection(axis) == edo12.pitch(26)

    axis = edo12.pitch(-5)

    assert edo12.pitch(0).reflection(axis) == edo12.pitch(-10)
    assert edo12.pitch(3).reflection(axis) == edo12.pitch(-13)
    assert edo12.pitch(19).reflection(axis) == edo12.pitch(-29)
    assert edo12.pitch(-5).reflection(axis) == edo12.pitch(-5)
    assert edo12.pitch(-20).reflection(axis) == edo12.pitch(10)
