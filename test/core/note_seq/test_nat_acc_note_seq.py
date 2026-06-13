import pytest
from xenharmlib import EDOTuning
from xenharmlib.core.note_seq import NatAccNoteSeq
from ..utils import make_nat_acc_test_notation

edo12 = EDOTuning(12)
n_edo12 = make_nat_acc_test_notation(edo12)
edo24 = EDOTuning(24)
n_edo24 = make_nat_acc_test_notation(edo24)
edo31 = EDOTuning(31)
n_edo31 = make_nat_acc_test_notation(edo31)


@pytest.mark.parametrize(
    'notation, input_pairs, result',
    [
        (
            n_edo12,
            [('E', 1), ('B+', 5), ('D+', 0)],
            [10, 31, 3]
        ),
        (
            n_edo12,
            [('A', 2), ('B+', 0), ('C', 1)],
            [12, 1, 8]
        ),
        (
            n_edo24,
            [('A', 1), ('B+', 1), ('C', 1)],
            [12, 13, 14]
        ),
    ]
)
def test_nat_indices(notation, input_pairs, result):
    """
    Test if nat_indices property is correct
    """

    scale = NatAccNoteSeq(
        notation,
        [notation.note(*pair) for pair in input_pairs]
    )

    assert scale.nat_indices == result


@pytest.mark.parametrize(
    'notation, input_pairs, result',
    [
        (
            n_edo12,
            [('E', 1), ('B+', 5), ('D+', 0)],
            [4, 1, 3]
        ),
        (
            n_edo12,
            [('A', 2), ('B+', 0), ('C', 1)],
            [0, 1, 2]
        ),
        (
            n_edo24,
            [('A', 1), ('B+', 1), ('C', 1)],
            [0, 1, 2]
        ),
    ]
)
def test_natc_indices(notation, input_pairs, result):
    """
    Test if natc_indices property is correct
    """

    scale = NatAccNoteSeq(
        notation,
        [notation.note(*pair) for pair in input_pairs]
    )

    assert scale.natc_indices == result


@pytest.mark.parametrize(
    'notation, input_pairs, result',
    [
        (
            n_edo12,
            [('E', 1), ('B+', 5), ('D+', 0)],
            [1, 5, 0]
        ),
        (
            n_edo12,
            [('A', 2), ('B+', 0), ('C', 1)],
            [2, 0, 1]
        ),
        (
            n_edo24,
            [('A', 1), ('B+', 1), ('C', 1)],
            [1, 1, 1]
        ),
    ]
)
def test_nat_bi_indices(notation, input_pairs, result):
    """
    Test if nat_bi_indices property is correct
    """

    scale = NatAccNoteSeq(
        notation,
        [notation.note(*pair) for pair in input_pairs]
    )

    assert scale.nat_bi_indices == result


@pytest.mark.parametrize(
    'notation, input_pairs, result',
    [
        (
            n_edo12,
            [('E-', 1), ('B+', 5), ('D+', 0)],
            [(-1,), (1,), (1,)]
        ),
        (
            n_edo12,
            [('A', 2), ('B+', 0), ('C', 1)],
            [(0,), (1,), (0,)]
        ),
        (
            n_edo24,
            [('A', 1), ('B+', 1), ('C', 1)],
            [(0,), (1,), (0,)]
        ),
    ]
)
def test_acc_sum_vectors(notation, input_pairs, result):
    """
    Test if acc_sum_vectors property is correct
    """

    scale = NatAccNoteSeq(
        notation,
        [notation.note(*pair) for pair in input_pairs]
    )

    assert scale.acc_sum_vectors == result


@pytest.mark.parametrize(
    'notation, input_pairs, result',
    [
        (
            n_edo12,
            [('E-', 1), ('B+', 5), ('D+', 0)],
            [(-1,), (1,), (1,)]
        ),
        (
            n_edo12,
            [('A', 2), ('B+', 0), ('C', 1)],
            [(0,), (1,), (0,)]
        ),
        (
            n_edo24,
            [('A', 1), ('B+', 1), ('C', 1)],
            [(0,), (1,), (0,)]
        ),
    ]
)
def test_acc_diff_vectors(notation, input_pairs, result):
    """
    Test if acc_diff_vectors property is correct
    """

    # FIXME: the current dummy nat/acc notation does not
    # differentiate between acc_sum and acc_diff vectors
    # by its configuration, so this is sadly the same as
    # testing for add_sum_vectors property

    scale = NatAccNoteSeq(
        notation,
        [notation.note(*pair) for pair in input_pairs]
    )

    assert scale.acc_diff_vectors == result


@pytest.mark.parametrize(
    'notation, input_pairs, result',
    [
        (
            n_edo12,
            [('E-', 1), ('B+', 5), ('D+', 0)],
            [-1, 1, 1]
        ),
        (
            n_edo12,
            [('A', 2), ('B+', 0), ('C', 1)],
            [0, 1, 0]
        ),
        (
            n_edo24,
            [('A', 1), ('B+', 1), ('C', 1)],
            [0, 1, 0]
        ),
    ]
)
def test_acc_values(notation, input_pairs, result):
    """
    Test if acc_values property is correct
    """

    scale = NatAccNoteSeq(
        notation,
        [notation.note(*pair) for pair in input_pairs]
    )

    assert scale.acc_values == result


@pytest.mark.parametrize(
    'notation, input_pairs, result',
    [
        (
            n_edo12,
            [('E-', 1), ('B+', 5), ('D+', 0)],
            [8, 2, 6]
        ),
        (
            n_edo12,
            [('A', 2), ('B+', 0), ('C', 1)],
            [0, 2, 4]
        ),
        (
            n_edo24,
            [('A', 1), ('B+', 1), ('C', 1)],
            [0, 2, 4]
        ),
    ]
)
def test_nat_pc_indices(notation, input_pairs, result):
    """
    Test if nat_pc_indices property is correct
    """

    scale = NatAccNoteSeq(
        notation,
        [notation.note(*pair) for pair in input_pairs]
    )

    assert scale.nat_pc_indices == result


@pytest.mark.parametrize(
    'notation, input_pairs, result',
    [
        (
            n_edo12,
            [('E-', 1), ('B+', 5), ('D+', 0)],
            [20, 62, 6]
        ),
        (
            n_edo12,
            [('A', 2), ('B+', 0), ('C', 1)],
            [24, 2, 16]
        ),
        (
            n_edo24,
            [('A', 1), ('B+', 1), ('C', 1)],
            [24, 26, 28]
        ),
    ]
)
def test_nat_pitch_indices(notation, input_pairs, result):
    """
    Test if nat_pitch_indices property is correct
    """

    scale = NatAccNoteSeq(
        notation,
        [notation.note(*pair) for pair in input_pairs]
    )

    assert scale.nat_pitch_indices == result


@pytest.mark.parametrize(
    'notation, input_pairs, result',
    [
        (
            n_edo12,
            [('E-', 1), ('B+', 5), ('D+', 0)],
            ['E', 'B', 'D']
        ),
        (
            n_edo12,
            [('A', 2), ('B+', 0), ('C', 1)],
            ['A', 'B', 'C']
        ),
        (
            n_edo24,
            [('A', 1), ('B+', 1), ('C', 1)],
            ['A', 'B', 'C']
        ),
    ]
)
def test_natc_symbols(notation, input_pairs, result):
    """
    Test if natc_symbols property is correct
    """

    scale = NatAccNoteSeq(
        notation,
        [notation.note(*pair) for pair in input_pairs]
    )

    assert scale.natc_symbols == result


@pytest.mark.parametrize(
    'notation, input_pairs, result',
    [
        (
            n_edo12,
            [('E-', 1), ('B++', 5), ('D+', 0)],
            ['-', '++', '+']
        ),
        (
            n_edo12,
            [('A', 2), ('B+', 0), ('C', 1)],
            ['', '+', '']
        ),
        (
            n_edo24,
            [('A', 1), ('B+', 1), ('C', 1)],
            ['', '+', '']
        ),
    ]
)
def test_acc_symbols(notation, input_pairs, result):
    """
    Test if acc_symbols property is correct
    """

    scale = NatAccNoteSeq(
        notation,
        [notation.note(*pair) for pair in input_pairs]
    )

    assert scale.acc_symbols == result


@pytest.mark.parametrize(
    'notation, input_pairs, result',
    [
        (
            n_edo12,
            [('E-', 1), ('B+', 5), ('D+', 0)],
            ['E-', 'B+', 'D+']
        ),
        (
            n_edo12,
            [('A', 2), ('B+', 0), ('C', 1)],
            ['A', 'B+', 'C']
        ),
        (
            n_edo24,
            [('A', 1), ('B+', 1), ('C', 1)],
            ['A', 'B+', 'C']
        ),
    ]
)
def test_pc_symbols(notation, input_pairs, result):
    """
    Test if pc_symbols property is correct
    """

    scale = NatAccNoteSeq(
        notation,
        [notation.note(*pair) for pair in input_pairs]
    )

    assert scale.pc_symbols == result


@pytest.mark.parametrize(
    'notation, input_pairs, result',
    [
        (
            n_edo12,
            [('E-', 1), ('B+', 5), ('D+', 0)],
            [-1, 1, 1]
        ),
        (
            n_edo12,
            [('A', 2), ('B+', 0), ('C', 1)],
            [0, 1, 0]
        ),
        (
            n_edo24,
            [('A', 1), ('B+', 1), ('C', 1)],
            [0, 1, 0]
        ),
    ]
)
def test_acc_directions(notation, input_pairs, result):
    """
    Test if acc_directions property is correct
    """

    scale = NatAccNoteSeq(
        notation,
        [notation.note(*pair) for pair in input_pairs]
    )

    assert scale.acc_directions == result
