import pytest

from xenharmlib.core.pitch import Pitch
from xenharmlib.core.tunings import EDOTuning
from xenharmlib.exc import InvalidPitchIndex

edo31 = EDOTuning('31edo', 31)


def test_pitch_index_change():

    pitch = Pitch(edo31, 41)
    assert pitch.pitch_index == 41

    pitch.pitch_index = 3
    assert pitch.pitch_index == 3