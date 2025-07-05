import pytest
from xenharmlib import EDOTuning
from xenharmlib import UpDownNotation
from xenharmlib import periodic
from xenharmlib.exc import InvalidIndexMask

edo12 = EDOTuning(12)
n_edo12 = UpDownNotation(edo12)
edo24 = EDOTuning(24)
n_edo24 = UpDownNotation(edo24)
edo31 = EDOTuning(31)
n_edo31 = UpDownNotation(edo31)

# FIXME: empty scales should also be tested and appropriate
# errors implemented. since is_period_normalized is not
# defined on empty scales, functions in the periodic
# extension module should also not be defined on
# empty scales


@pytest.mark.parametrize(
    'tuning, scale_a_pi, scale_b_pi, mask_expr, result_scales_pi',
    [
        (
            edo12,
            [2, 4, 6, 7, 9, 11],
            [2, 4, 6, 7, 9, 11],
            (0, 2, 4),
            [
                [2, 6, 9],
                [4, 7, 11],
                [6, 9, 14],
                [7, 11, 16],
                [9, 14, 18],
                [11, 16, 19],
            ]
        ),
        (
            edo31,
            [2, 6, 12, 14, 19, 23, 29],
            [12, 14, 19, 27, 29, 33, 39],
            (1, 2, 4),
            [
                [14, 19, 29],
                [29, 33, 43],
            ]
        ),
        (
            edo24,
            [2, 6, 12, 14, 19, 23],
            [1, 6, 12, 13, 14, 23],
            (-1, 1),
            [
                [-1, 6],
            ]
        ),
    ]
)
def test_mod_connectors_pitch(
    tuning, scale_a_pi, scale_b_pi, mask_expr, result_scales_pi
):
    """
    Test if mod_connectors function works on the pitch layer
    """

    scale_a = tuning.index_scale(scale_a_pi)
    scale_b = tuning.index_scale(scale_b_pi)
    result = [
        tuning.index_scale(pi) for pi in result_scales_pi
    ]
    assert list(periodic.mod_connectors(scale_a, scale_b, mask_expr)) == result


@pytest.mark.parametrize(
    'notation, scale_a_pairs, scale_b_pairs, mask_expr, result_scales_pairs',
    [
        (
            n_edo12,
            [('C', 1), ('D', 1), ('E', 1), ('F#', 1), ('A', 1)],
            [('C', 1), ('D', 1), ('E', 1), ('F#', 1), ('A', 1)],
            (0, 2, 4),
            [
                [('C', 1), ('E', 1), ('A', 1)],
                [('D', 1), ('F#', 1), ('C', 2)],
                [('E', 1), ('A', 1), ('D', 2)],
                [('F#', 1), ('C', 2), ('E', 2)],
                [('A', 1), ('D', 2), ('F#', 2)]
            ]
        ),
        (
            n_edo31,
            [('E', 1), ('F', 1), ('G#', 1), ('A', 1), ('C#', 2)],
            [('F', 2), ('G#', 2), ('A#', 2), ('C#', 3), ('E', 3)],
            (0, 1, 3),
            [
                [('F', 1), ('G#', 1), ('C#', 2)],
                [('C#', 2), ('E', 2), ('G#', 2)],
            ]
        ),
    ]
)
def test_mod_connectors_note(
    notation,
    scale_a_pairs,
    scale_b_pairs,
    mask_expr,
    result_scales_pairs
):
    """
    Test if mod_connector function works on the notation layer
    """

    scale_a = notation.scale(
        [notation.note(*pair) for pair in scale_a_pairs]
    )

    scale_b = notation.scale(
        [notation.note(*pair) for pair in scale_b_pairs]
    )

    result = []

    for pairs in result_scales_pairs:
        partial_scale = notation.scale(
            [notation.note(*pair) for pair in pairs]
        )
        result.append(partial_scale)

    iterator = periodic.mod_connectors(scale_a, scale_b, mask_expr)

    for i, partial_scale in enumerate(iterator):
        expected = result[i]
        assert partial_scale == expected
        assert partial_scale.is_notated_same(expected)


def test_mod_connectors_non_period_normalized():
    """
    Test if mod_connectors function throws correct exception if
    scale is not period normalized
    """

    scale_a = n_edo12.pc_scale(['C', 'D', 'E', 'F', 'G', 'A', 'B', 'C'])
    scale_b = n_edo12.pc_scale(['C', 'D', 'E', 'F', 'G', 'A', 'B'])

    with pytest.raises(ValueError) as exc_info:
        list(periodic.mod_connectors(scale_a, scale_b, (0, 2, 4)))

    assert exc_info.value.args[0] == (
        'mod_connectors is only defined on period normalized scales'
    )

    with pytest.raises(ValueError) as exc_info:
        list(periodic.mod_connectors(scale_b, scale_a, (0, 2, 4)))

    assert exc_info.value.args[0] == (
        'mod_connectors is only defined on period normalized scales'
    )


def test_mod_connectors_invalid_mask():
    """
    Test if mod_connectors function throws correct exception on
    invalid mask expression
    """

    scale_a = n_edo12.pc_scale(['C', 'D', 'E', 'F', 'G', 'A', 'B'])
    scale_b = n_edo12.pc_scale(['D', 'E', 'F', 'G', 'A', 'B', 'C'])

    with pytest.raises(InvalidIndexMask) as exc_info:
        list(periodic.mod_connectors(scale_a, scale_b, ...))

    assert exc_info.value.args[0] == (
        'Ellipsis is not allowed on edges of infinite series mask'
    )

    with pytest.raises(InvalidIndexMask) as exc_info:
        list(periodic.mod_connectors(scale_a, scale_b, (1, 4, ...)))

    assert exc_info.value.args[0] == (
        'Ellipsis is not allowed on edges of infinite series mask'
    )

    with pytest.raises(InvalidIndexMask) as exc_info:
        list(periodic.mod_connectors(scale_a, scale_b, (..., 1, 4)))

    assert exc_info.value.args[0] == (
        'Ellipsis is not allowed on edges of infinite series mask'
    )

    with pytest.raises(InvalidIndexMask) as exc_info:
        list(periodic.mod_connectors(scale_a, scale_b, (..., 1, 4, ...)))

    assert exc_info.value.args[0] == (
        'Ellipsis is not allowed on edges of infinite series mask'
    )

    with pytest.raises(InvalidIndexMask) as exc_info:
        list(periodic.mod_connectors(scale_a, scale_b, (2, 1)))

    assert exc_info.value.args[0] == (
        'Indices in masks are not consecutive'
    )


@pytest.mark.parametrize(
    'tuning, scale_pi, iseq_diffs, index_masks',
    [
        (
            edo12,
            [2, 4, 6, 7, 9, 11],
            [2, 2, 3],
            [
                (0, 1, 2, 4),
                (3, 4, 5, 6)
            ]
        ),
        (
            edo31,
            [1, 3, 9, 11, 12, 20, 22],
            [10, 11],
            [
                (0, 3, 6),
                (6, 7, 11)
            ]
        ),
    ]
)
def test_find_iseq_pitch(
    tuning, scale_pi, iseq_diffs, index_masks
):
    """
    Test if find_iseq function works on the pitch layer
    """

    scale = tuning.index_scale(scale_pi)
    iseq = tuning.diff_interval_seq(iseq_diffs)

    assert list(periodic.find_iseq(scale, iseq)) == index_masks


@pytest.mark.parametrize(
    'notation, scale_pairs, iseq_pairs, index_masks',
    [
        (
            n_edo12,
            [('C', 1), ('D', 1), ('Eb', 1), ('F#', 1), ('G#', 1), ('A', 1)],
            [('M', 2), ('m', 2)],
            [
                (0, 1, 2),
                (3, 4, 5)
            ]
        ),
        (
            n_edo24,
            [
                ('A', 3), ('B', 3), ('C', 4), ('D', 4),
                ('E', 4), ('F', 4), ('G', 4)
            ],
            [('m', 3), ('m', 3)],
            [
                (1, 3, 5),
            ]
        ),
        (
            n_edo31,
            [
                ('A', 3), ('B', 3), ('C', 4), ('D', 4),
                ('E', 4), ('F', 4), ('G', 4)
            ],
            [('M', 3), ('m', 3)],
            [
                (2, 4, 6),
                (5, 7, 9),
                (6, 8, 10),
            ]
        ),
    ]
)
def test_find_iseq_note(
    notation,
    scale_pairs,
    iseq_pairs,
    index_masks
):
    """
    Test if find_iseq function works on the notation layer
    """

    scale = notation.scale(
        [notation.note(*pair) for pair in scale_pairs]
    )
    iseq = notation.interval_seq(
        [notation.shorthand_interval(*pair) for pair in iseq_pairs]
    )

    assert list(periodic.find_iseq(scale, iseq)) == index_masks


def test_find_iseq_non_period_normalized():
    """
    Test if find_iseq function throws correct exception if
    scale is not period normalized
    """

    scale = n_edo12.pc_scale(['C', 'D', 'E', 'F', 'G', 'A', 'B', 'C'])
    iseq = n_edo12.interval_seq(
        [
            n_edo12.shorthand_interval('M', 2),
            n_edo12.shorthand_interval('m', 2)
        ]
    )

    with pytest.raises(ValueError) as exc_info:
        list(periodic.find_iseq(scale, iseq))

    assert exc_info.value.args[0] == (
        'find_iseq is only defined on period normalized scales'
    )
