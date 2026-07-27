import pytest
from xenharmlib import EDOTuning
from xenharmlib import EDTuning
from xenharmlib import FrequencyRatio
from xenharmlib.core.note_seq import PeriodicNoteSeq
from xenharmlib.exc import IncompatibleOriginContexts
from ..utils import make_nat_acc_test_notation

edo12 = EDOTuning(12)
n_edo12 = make_nat_acc_test_notation(edo12)
edo24 = EDOTuning(24)
n_edo24 = make_nat_acc_test_notation(edo24)
edo31 = EDOTuning(31)
n_edo31 = make_nat_acc_test_notation(edo31)
ed13_3 = EDTuning(13, FrequencyRatio(3))
n_ed13_3 = make_nat_acc_test_notation(ed13_3)


@pytest.mark.parametrize(
    'notation, input_pairs, result_pci',
    [
        (
            n_edo12,
            [('E', 1), ('B+', 5), ('D+', 0)],
            [8, 3, 7]
        ),
        (
            n_edo12,
            [('A', 2), ('B+', 0), ('C', 1)],
            [0, 3, 4]
        ),
        (
            n_edo24,
            [('A', 1), ('B+', 1), ('C', 1)],
            [0, 3, 4]
        ),
    ]
)
def test_pc_indices(notation, input_pairs, result_pci):
    """
    Test if pc_indices property is correct
    """

    seq = PeriodicNoteSeq(
        notation,
        [notation.note(*pair) for pair in input_pairs]
    )

    assert seq.pc_indices == result_pci


@pytest.mark.parametrize(
    'notation, input_pairs, bi_diff, result_pairs',
    [
        (
            n_edo12,
            [('A+', 0), ('B+', 0), ('D+', 0)],
            2,
            [('A+', 2), ('B+', 2), ('D+', 2)],
        ),
        (
            n_edo12,
            [('A+', 0), ('B+', 1), ('F', 2)],
            0,
            [('A+', 0), ('B+', 1), ('F', 2)],
        ),
        (
            n_edo24,
            [('A+', 0), ('B+', 1), ('F', 2)],
            -1,
            [('A+', -1), ('B+', 0), ('F', 1)],
        ),
        (
            n_edo24,
            [('A+', 0), ('B+', 1), ('F', 2)],
            5,
            [('A+', 5), ('B+', 6), ('F', 7)],
        ),
    ]
)
def test_transpose_bi_index(notation, input_pairs, bi_diff, result_pairs):
    """
    Test if transpose method works correctly when given an interval
    """

    seq = PeriodicNoteSeq(
        notation,
        [notation.note(*pair) for pair in input_pairs]
    )

    transposed = seq.transpose_bi_index(bi_diff)

    assert transposed == notation.seq(
        [notation.note(*pair) for pair in result_pairs]
    )


@pytest.mark.parametrize(
    'notation, input_pairs_a, input_pairs_b, is_equivalent',
    [
        (
            n_edo12,
            [('A+', 0), ('B+', 0), ('D+', 0)],
            [('A+', 2), ('B+', 2), ('D+', 2)],
            True
        ),
        (
            n_edo12,
            [('A+', 0), ('B+', 0)],
            [('A+', 2), ('B+', 2), ('D+', 2)],
            False
        ),
        (
            n_edo12,
            [('A+', 0), ('B+', 0), ('D+', 0)],
            [('B-', 2), ('B+', 2), ('D+', 2)],
            True
        ),
        (
            n_edo12,
            [('A+', 0), ('B+', 0), ('D+', 0)],
            [('B+', 2), ('B+', 2), ('D+', 2)],
            False
        ),
        (
            n_edo12,
            [('A+', 0), ('B+', 1), ('F', 2)],
            [('A+', 0), ('B+', 1), ('F', 2)],
            True
        ),
        (
            n_edo24,
            [('A+', 0), ('B+', 1), ('F', 2)],
            [('A+', -1), ('B+', 1), ('F', 0)],
            True
        ),
        (
            n_edo24,
            [('A+', 0), ('B+', 1), ('F', 2)],
            [('A+', -1), ('C', 1), ('F', 0)],
            False
        ),
        (
            n_edo24,
            [('A+', 0), ('B+', 1), ('F', 2)],
            [('A+', 1), ('B+', 1), ('F', 3)],
            True
        ),
    ]
)
def test_is_equivalent(notation, input_pairs_a, input_pairs_b, is_equivalent):
    """
    Test if is_equivalent method works correctly
    """

    seq_a = PeriodicNoteSeq(
        notation,
        [notation.note(*pair) for pair in input_pairs_a]
    )

    seq_b = PeriodicNoteSeq(
        notation,
        [notation.note(*pair) for pair in input_pairs_b]
    )

    assert seq_a.is_equivalent(seq_b) == is_equivalent


def test_is_equivalent_incompatible():
    """
    Test if is_equivalent raises correct exception
    on incompatible tunings
    """

    seq_a = PeriodicNoteSeq(
        n_edo12,
        [n_edo12.note(*pair) for pair in [('A', 3), ('B', 2)]]
    )

    seq_b = PeriodicNoteSeq(
        n_ed13_3,
        [n_ed13_3.note(*pair) for pair in [('A', 3), ('B', 2)]]
    )

    with pytest.raises(IncompatibleOriginContexts):
        assert seq_a.is_equivalent(seq_b)


@pytest.mark.parametrize(
    'notation, input_pairs_a, input_pairs_b, is_equivalent',
    [
        (
            n_edo12,
            [('A+', 0), ('B+', 0), ('D+', 0)],
            [('A+', 2), ('B+', 2), ('D+', 2)],
            True
        ),
        (
            n_edo12,
            [('A+', 0), ('B+', 0), ('D+', 0)],
            [('A+', 2), ('B+', 2)],
            False
        ),
        (
            n_edo12,
            [('A+', 0), ('B+', 0), ('D+', 0)],
            [('B-', 2), ('B+', 2), ('D+', 2)],
            False
        ),
        (
            n_edo12,
            [('A+', 0), ('B+', 0), ('D+', 0)],
            [('B+', 2), ('B+', 2), ('D+', 2)],
            False
        ),
        (
            n_edo12,
            [('A+', 0), ('B+', 1), ('F', 2)],
            [('A+', 0), ('B+', 1), ('F', 2)],
            True
        ),
        (
            n_edo24,
            [('A+', 0), ('B+', 1), ('F', 2)],
            [('A+', -1), ('B+', 1), ('F', 0)],
            True
        ),
        (
            n_edo24,
            [('A+', 0), ('B+', 1), ('F', 2)],
            [('A+', -1), ('C', 1), ('F', 0)],
            False
        ),
        (
            n_edo24,
            [('A+', 0), ('B+', 1), ('F', 2)],
            [('A+', 1), ('B+', 1), ('F', 3)],
            True
        ),
    ]
)
def test_is_notated_equivalent(
    notation, input_pairs_a, input_pairs_b, is_equivalent
):
    """
    Test if is_notated_equivalent method works correctly
    """

    seq_a = PeriodicNoteSeq(
        notation,
        [notation.note(*pair) for pair in input_pairs_a]
    )

    seq_b = PeriodicNoteSeq(
        notation,
        [notation.note(*pair) for pair in input_pairs_b]
    )

    assert seq_a.is_notated_equivalent(seq_b) == is_equivalent


def test_is_notated_equivalent_incompatible():
    """
    Test if is_notated_equivalent raises correct exception
    on incompatible tunings
    """

    seq_a = PeriodicNoteSeq(
        n_edo12,
        [n_edo12.note(*pair) for pair in [('A', 3), ('B', 2)]]
    )

    seq_b = PeriodicNoteSeq(
        n_ed13_3,
        [n_ed13_3.note(*pair) for pair in [('A', 3), ('B', 2)]]
    )

    with pytest.raises(IncompatibleOriginContexts):
        assert seq_a.is_notated_equivalent(seq_b)
