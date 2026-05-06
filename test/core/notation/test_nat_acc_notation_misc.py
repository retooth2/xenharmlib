import pytest
from xenharmlib import EDOTuning
from xenharmlib.exc import InvalidIntervalNumber
from ..utils import MyNatAccNotation


def test_invalid_interval_number():

    tuning = EDOTuning(12)
    notation = MyNatAccNotation(tuning, acc_weights=(1,))

    notation.append_natural('C', 3)

    with pytest.raises(InvalidIntervalNumber):
        notation.interval_number_to_nat_diff(0)
