import pytest
from xenharmlib import EDOTuning
from xenharmlib.exc import IncompatibleNotations
from ..utils import make_nat_acc_test_notation

edo12 = EDOTuning(12)
n_edo12 = make_nat_acc_test_notation(edo12)
edo24 = EDOTuning(24)
n_edo24 = make_nat_acc_test_notation(edo24)

# TODO: builder methods should also be
# properly unit tested


def test_note_interval_incompatible_notations():

    note_a = n_edo12.note('A', 0)
    note_b = n_edo12.note('B', 0)

    with pytest.raises(IncompatibleNotations):
        n_edo24.note_interval(note_a, note_b)


def test_note_scale_incompatible_notations():

    note_a = n_edo12.note('A', 0)
    note_b = n_edo12.note('B', 0)
    note_c = n_edo24.note('B', 0)

    with pytest.raises(IncompatibleNotations):
        n_edo12.note_scale(
            [note_a, note_b, note_c]
        )


def test_natural_scale():

    natural_scale = n_edo12.note_scale(
        [n_edo12.note(s, 0) for s in ['A', 'B', 'C', 'D', 'E', 'F']]
    )

    assert n_edo12.natural_scale().is_notated_same(natural_scale)
