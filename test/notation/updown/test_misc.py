import pytest

from xenharmlib import EDOTuning
from xenharmlib import EDTuning
from xenharmlib import Frequency
from xenharmlib import UpDownNotation
from xenharmlib.exc import UnfittingNotation
from xenharmlib.exc import UnknownNoteSymbol


def test_unfitting_notation():

    bp = EDTuning(13, Frequency(3))

    with pytest.raises(UnfittingNotation):
        UpDownNotation(bp)


def test_misplaced_updown():

    edo31 = EDOTuning(31)
    n_edo31 = UpDownNotation(edo31)

    with pytest.raises(UnknownNoteSymbol):
        n_edo31.parse_pc_symbol('C^')


@pytest.mark.parametrize(
    'divisions, expected',
    [
        (12, 'UpDownNotation(12-EDO)'),
        (31, 'UpDownNotation(31-EDO)'),
        (18, 'UpDownNotation(18-EDO)'),
    ]
)
def test_name(divisions, expected):

    edo31 = EDOTuning(divisions)
    n_edo31 = UpDownNotation(edo31)
    assert n_edo31.name == expected


@pytest.mark.parametrize(
    'divisions, expected',
    [
        (12, 'UpDownNotation(12-EDO)'),
        (31, 'UpDownNotation(31-EDO)'),
        (18, 'UpDownNotation(18-EDO)'),
    ]
)
def test_repr(divisions, expected):

    edo31 = EDOTuning(divisions)
    n_edo31 = UpDownNotation(edo31)
    assert repr(n_edo31) == expected
