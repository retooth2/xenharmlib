import pytest
from xenharmlib import EDOTuning
from xenharmlib.exc import InvalidIntervalNumber
from xenharmlib.core.notation import NatAccNotation


def test_invalid_interval_number():

    tuning = EDOTuning(12)
    notation = NatAccNotation(tuning)

    notation.append_natural('C', 3)

    with pytest.raises(InvalidIntervalNumber):
        notation.interval_number_to_nat_diff(0)
