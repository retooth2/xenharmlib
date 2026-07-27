import pytest
from xenharmlib import EDOTuning
from xenharmlib.core.note_scale import NatAccNoteScale
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
            [3, 10, 31]
        ),
        (
            n_edo12,
            [('A', 2), ('B+', 0), ('C', 1)],
            [1, 8, 12]
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

    scale = NatAccNoteScale(
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
            [3, 4, 1]
        ),
        (
            n_edo12,
            [('A', 2), ('B+', 0), ('C', 1)],
            [1, 2, 0]
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

    scale = NatAccNoteScale(
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
            [0, 1, 5]
        ),
        (
            n_edo12,
            [('A', 2), ('B+', 0), ('C', 1)],
            [0, 1, 2]
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

    scale = NatAccNoteScale(
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
            [(1,), (-1,), (1,)]
        ),
        (
            n_edo12,
            [('A', 2), ('B+', 0), ('C', 1)],
            [(1,), (0,), (0,)]
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

    scale = NatAccNoteScale(
        notation,
        [notation.note(*pair) for pair in input_pairs]
    )

    with pytest.deprecated_call():
        assert scale.acc_vectors == result

    assert scale.acc_diff_vectors == result


@pytest.mark.parametrize(
    'notation, input_pairs, result',
    [
        (
            n_edo12,
            [('E-', 1), ('B+', 5), ('D+', 0)],
            [1, -1, 1]
        ),
        (
            n_edo12,
            [('A', 2), ('B+', 0), ('C', 1)],
            [1, 0, 0]
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

    scale = NatAccNoteScale(
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
            [6, 8, 2]
        ),
        (
            n_edo12,
            [('A', 2), ('B+', 0), ('C', 1)],
            [2, 4, 0]
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

    scale = NatAccNoteScale(
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
            [6, 20, 62]
        ),
        (
            n_edo12,
            [('A', 2), ('B+', 0), ('C', 1)],
            [2, 16, 24]
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

    scale = NatAccNoteScale(
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
            ['D', 'E', 'B']
        ),
        (
            n_edo12,
            [('A', 2), ('B+', 0), ('C', 1)],
            ['B', 'C', 'A']
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

    scale = NatAccNoteScale(
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
            ['+', '-', '++']
        ),
        (
            n_edo12,
            [('A', 2), ('B+', 0), ('C', 1)],
            ['+', '', '']
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

    scale = NatAccNoteScale(
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
            ['D+', 'E-', 'B+']
        ),
        (
            n_edo12,
            [('A', 2), ('B+', 0), ('C', 1)],
            ['B+', 'C', 'A']
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

    scale = NatAccNoteScale(
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
            [1, -1, 1]
        ),
        (
            n_edo12,
            [('A', 2), ('B+', 0), ('C', 1)],
            [1, 0, 0]
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

    scale = NatAccNoteScale(
        notation,
        [notation.note(*pair) for pair in input_pairs]
    )

    assert scale.acc_directions == result


@pytest.mark.parametrize(
    'notation_a, input_pi, notation_b, result_pi',
    [
        (n_edo12, [0, 3, 7, 8, 10], n_edo31, [0, 8, 18, 21, 26]),
        (n_edo12, [1, 4, 6, 7, 8, 11], n_edo24, [2, 8, 12, 14, 16, 22]),
        (n_edo24, [2, 8, 12, 14, 16, 22], n_edo12, [1, 4, 6, 7, 8, 11]),
        (n_edo24, [1, 8, 12, 14, 16, 22], n_edo12, [0, 4, 6, 7, 8, 11]),
    ]
)
def test_retune_closest(notation_a, input_pi, notation_b, result_pi):
    """
    Test if retune_closest method works correctly
    """

    scale_a = notation_a.index_scale(input_pi)
    expected_scale_b = notation_b.index_scale(result_pi)

    scale_b = scale_a.retune_closest(notation_b)
    assert scale_b == expected_scale_b
