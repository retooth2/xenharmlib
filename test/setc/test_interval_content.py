import pytest
from xenharmlib import EDOTuning
from xenharmlib import PrimeLimitTuning
from xenharmlib import UpDownNotation
from xenharmlib import WesternNotation
from xenharmlib.setc import ic_vector


@pytest.mark.parametrize(
    'scale, vector',
    [
        (
            WesternNotation().index_scale([0, 2, 4, 5, 7, 9, 11]),
            (2, 5, 4, 3, 6, 1)
        ),
        (
            WesternNotation().index_scale([0, 4, 7]),
            (0, 0, 1, 1, 1, 0)
        ),
        (
            WesternNotation().pc_scale(['G', 'B', 'D']),
            (0, 0, 1, 1, 1, 0)
        ),
        (
            EDOTuning(24).index_scale([0, 8, 14]),
            (0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0)
        ),
        (
            EDOTuning(24).index_scale([2, 10, 16]),
            (0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0)
        ),
        (
            EDOTuning(31).index_scale([0, 10, 18]),
            (0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0)
        ),
        (
            UpDownNotation(EDOTuning(31)).pc_scale(['C', 'E', 'G']),
            (0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0)
        ),
    ]
)
def test_ic_vector(scale, vector):
    assert ic_vector(scale) == vector


def test_ic_vector_empty():

    empty = EDOTuning(24).scale()

    with pytest.raises(ValueError) as exc_info:
        ic_vector(empty)
    assert exc_info.value.args[0] == (
        'ic_vector cannot be calculated on empty scale'
    )


def test_ic_vector_multigen():

    limit7 = PrimeLimitTuning(7)
    scale = limit7.rs_scale(['1/1', '5/4', '3/2'])

    with pytest.raises(ValueError) as exc_info:
        ic_vector(scale)
    assert exc_info.value.args[0] == (
        'ic_vector only supports one-dimensional tunings'
    )
