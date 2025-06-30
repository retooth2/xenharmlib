from xenharmlib.notation.western import WesternNotation


def test_name():

    notation = WesternNotation()
    assert notation.name == 'WesternNotation'


def test_repr():

    notation = WesternNotation()
    assert repr(notation) == 'WesternNotation(A4=440Hz)'
