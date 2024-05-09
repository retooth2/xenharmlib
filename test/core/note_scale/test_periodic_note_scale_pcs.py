import pytest
from xenharmlib import EDOTuning
from xenharmlib import EDTuning
from xenharmlib import Frequency
from xenharmlib.core.note_scale import PeriodicNoteScale
from ..utils import make_nat_acc_test_notation

edo12 = EDOTuning(12)
n_edo12 = make_nat_acc_test_notation(edo12)
edo24 = EDOTuning(24)
n_edo24 = make_nat_acc_test_notation(edo24)
edo31 = EDOTuning(31)
n_edo31 = make_nat_acc_test_notation(edo31)
ed13_3 = EDTuning(13, Frequency(3))
n_ed13_3 = make_nat_acc_test_notation(ed13_3)


@pytest.mark.parametrize(
    'notation, input_pairs_a, input_pairs_b, result_pairs',
    [
        (
            n_edo12,
            [('A+', 0), ('B+', 0), ('D+', 1)],
            [('A+', 0), ('C', 0), ('D+', 0)],
            [('A+', 0), ('D+', 0)],
        ),
        (
            n_edo12,
            [('A+', 3), ('B+', 0), ('D+', 0)],
            [('A+', 0), ('C', 0), ('E-', 0)],
            [('A+', 0), ('D+', 0)],
        ),
        (
            n_edo12,
            [('A+', 5), ('B+', -1), ('F', 6)],
            [('A+', 0), ('C-', 1), ('Ex', 2)],
            [('A+', 0), ('B+', 0), ('F', 0)],
        ),
        (
            n_edo24,
            [('A+', 0), ('B+', 1), ('F+', 2)],
            [('A', 0), ('B', 0), ('F', 2)],
            [],
        ),
        (
            n_edo24,
            [('A+', 0), ('B+', 1), ('F', 2)],
            [],
            [],
        ),
    ]
)
def test_pcs_intersection(
    notation,
    input_pairs_a,
    input_pairs_b,
    result_pairs
):
    """
    Test if pcs_intersection operation works correctly
    """

    scale_a = PeriodicNoteScale(
        notation,
        [notation.note(*pair) for pair in input_pairs_a]
    )

    scale_b = PeriodicNoteScale(
        notation,
        [notation.note(*pair) for pair in input_pairs_b]
    )

    scale_c = scale_a.pcs_intersection(scale_b)

    assert len(scale_c) == len(result_pairs)
    notes = list(scale_c)
    assert notes == [notation.note(*pair) for pair in result_pairs]
