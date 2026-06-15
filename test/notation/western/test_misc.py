from xenharmlib.core.frequencies import Frequency
from xenharmlib.notation.western import WesternNotation


def test_ref_frequency():

    notation = WesternNotation(ref_frequency=Frequency(20))
    assert notation.note('C', 0).frequency == Frequency(20)
    assert notation.note('C', 1).frequency == Frequency(40)


def test_name():

    notation = WesternNotation()
    assert notation.name == 'WesternNotation'


def test_repr():

    notation = WesternNotation()
    assert repr(notation) == 'WesternNotation(A4=440Hz)'
