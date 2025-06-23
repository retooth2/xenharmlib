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


@pytest.mark.parametrize(
    'tuning, scale_pi, mask_expr, result_scales_pi',
    [
        (
            edo12,
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
            (1, ..., 4),
            [
                [6, 12, 14, 19],
                [12, 14, 19, 23],
                [14, 19, 23, 29],
                [19, 23, 29, 33],
                [23, 29, 33, 37],
                [29, 33, 37, 43],
                [33, 37, 43, 45]
            ]
        ),
        (
            edo24,
            [2, 6, 12, 14, 19, 23],
            (-1, 1),
            [
                [-1, 6],
                [2, 12],
                [6, 14],
                [12, 19],
                [14, 23],
                [19, 26],
            ]
        ),
    ]
)
def test_cutout_pitch(tuning, scale_pi, mask_expr, result_scales_pi):
    """
    Test if cutouts function works on the pitch layer
    """

    scale = tuning.index_scale(scale_pi)
    result = [
        tuning.index_scale(pi) for pi in result_scales_pi
    ]
    assert list(periodic.cutouts(scale, mask_expr)) == result


@pytest.mark.parametrize(
    'notation, scale_pairs, mask_expr, result_scales_pairs',
    [
        (
            n_edo12,
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
            (0, 2, 4, 7),
            [
                [('E', 1), ('G#', 1), ('C#', 2), ('G#', 2)],
                [('F', 1), ('A', 1), ('E', 2), ('A', 2)],
                [('G#', 1), ('C#', 2), ('F', 2), ('C#', 3)],
                [('A', 1), ('E', 2), ('G#', 2), ('E', 3)],
                [('C#', 2), ('F', 2), ('A', 2), ('F', 3)],
            ]
        ),
    ]
)
def test_cutouts_note(
    notation,
    scale_pairs,
    mask_expr,
    result_scales_pairs
):
    """
    Test if cutouts function works on the notation layer
    """

    scale = notation.scale(
        [notation.note(*pair) for pair in scale_pairs]
    )

    result = []

    for pairs in result_scales_pairs:
        partial_scale = notation.scale(
            [notation.note(*pair) for pair in pairs]
        )
        result.append(partial_scale)

    for i, partial_scale in enumerate(periodic.cutouts(scale, mask_expr)):
        expected = result[i]
        assert partial_scale == expected
        assert partial_scale.is_notated_same(expected)


def test_cutouts_non_period_normalized():
    """
    Test if cutouts function throws correct exception if
    scale is not period normalized
    """

    scale = n_edo12.pc_scale(['C', 'D', 'E', 'F', 'G', 'A', 'B', 'C'])

    with pytest.raises(ValueError) as exc_info:
        list(periodic.cutouts(scale, (0, 2, 4)))

    assert exc_info.value.args[0] == (
        'cutouts is only defined on period normalized scales'
    )


def test_cutouts_invalid_mask():
    """
    Test if cutouts function throws correct exception on
    invalid mask expression
    """

    scale = n_edo12.pc_scale(['C', 'D', 'E', 'F', 'G', 'A', 'B'])

    with pytest.raises(InvalidIndexMask) as exc_info:
        list(periodic.cutouts(scale, ...))

    assert exc_info.value.args[0] == (
        'Ellipsis is not allowed on edges of infinite series mask'
    )

    with pytest.raises(InvalidIndexMask) as exc_info:
        list(periodic.cutouts(scale, (1, 4, ...)))

    assert exc_info.value.args[0] == (
        'Ellipsis is not allowed on edges of infinite series mask'
    )

    with pytest.raises(InvalidIndexMask) as exc_info:
        list(periodic.cutouts(scale, (..., 1, 4)))

    assert exc_info.value.args[0] == (
        'Ellipsis is not allowed on edges of infinite series mask'
    )

    with pytest.raises(InvalidIndexMask) as exc_info:
        list(periodic.cutouts(scale, (..., 1, 4, ...)))

    assert exc_info.value.args[0] == (
        'Ellipsis is not allowed on edges of infinite series mask'
    )


@pytest.mark.parametrize(
    'tuning, scale_pi, dist, result_pair_pi',
    [
        (
            edo12,
            [2, 4, 6, 7, 9, 11],
            1,
            [
                [2, 4],
                [4, 6],
                [6, 7],
                [7, 9],
                [9, 11],
                [11, 14],
            ]
        ),
        (
            edo31,
            [2, 6, 12, 14, 19, 23, 29],
            3,
            [
                [2, 14],
                [6, 19],
                [12, 23],
                [14, 29],
                [19, 33],
                [23, 37],
                [29, 43],
            ]
        ),
    ]
)
def test_pairs_pitch(tuning, scale_pi, dist, result_pair_pi):
    """
    Test if pairs function works on the pitch layer
    """

    scale = tuning.index_scale(scale_pi)
    result = [
        (tuning.pitch(first), tuning.pitch(second))
        for first, second in result_pair_pi
    ]

    for i, pair in enumerate(periodic.pairs(scale, dist)):
        expected = result[i]
        assert pair == expected


@pytest.mark.parametrize(
    'tuning, scale_pi, result_pair_pi',
    [
        (
            edo12,
            [2, 4, 6, 7, 9, 11],
            [
                [2, 4],
                [4, 6],
                [6, 7],
                [7, 9],
                [9, 11],
                [11, 14],
            ]
        ),
        (
            edo31,
            [2, 6, 12, 14, 19, 23, 29],
            [
                [2, 6],
                [6, 12],
                [12, 14],
                [14, 19],
                [19, 23],
                [23, 29],
                [29, 33],
            ]
        ),
    ]
)
def test_pairs_pitch_default_dist(tuning, scale_pi, result_pair_pi):
    """
    Test if pairs function works on the pitch layer
    when omitting the distance parameter
    """

    scale = tuning.index_scale(scale_pi)
    result = [
        (tuning.pitch(first), tuning.pitch(second))
        for first, second in result_pair_pi
    ]

    for i, pair in enumerate(periodic.pairs(scale)):
        expected = result[i]
        assert pair == expected


@pytest.mark.parametrize(
    'notation, scale_pairs, dist, result_pair_pairs',
    [
        (
            n_edo12,
            [('C', 1), ('D', 1), ('E', 1), ('F#', 1), ('A', 1)],
            7,
            [
                [('C', 1), ('E', 2)],
                [('D', 1), ('F#', 2)],
                [('E', 1), ('A', 2)],
                [('F#', 1), ('C', 3)],
                [('A', 1), ('D', 3)],
            ]
        ),
        (
            n_edo31,
            [('E', 1), ('F', 1), ('G#', 1), ('A', 1), ('C#', 2)],
            2,
            [
                [('E', 1), ('G#', 1)],
                [('F', 1), ('A', 1)],
                [('G#', 1), ('C#', 2)],
                [('A', 1), ('E', 2)],
                [('C#', 2), ('F', 2)],
            ]
        ),
    ]
)
def test_pairs_note(
    notation,
    scale_pairs,
    dist,
    result_pair_pairs
):
    """
    Test if pairs function works on the notation layer
    """

    scale = notation.scale(
        [notation.note(*pair) for pair in scale_pairs]
    )
    result = [
        (notation.note(*first), notation.note(*second))
        for first, second in result_pair_pairs
    ]

    for i, pair in enumerate(periodic.pairs(scale, dist)):
        expected = result[i]
        assert pair == expected
        assert pair[0].is_notated_same(expected[0])
        assert pair[1].is_notated_same(expected[1])


@pytest.mark.parametrize(
    'notation, scale_pairs, result_pair_pairs',
    [
        (
            n_edo12,
            [('C', 1), ('D', 1), ('E', 1), ('F#', 1), ('A', 1)],
            [
                [('C', 1), ('D', 1)],
                [('D', 1), ('E', 1)],
                [('E', 1), ('F#', 1)],
                [('F#', 1), ('A', 1)],
                [('A', 1), ('C', 2)],
            ]
        ),
        (
            n_edo31,
            [('E', 1), ('F', 1), ('G#', 1), ('A', 1), ('C#', 2)],
            [
                [('E', 1), ('F', 1)],
                [('F', 1), ('G#', 1)],
                [('G#', 1), ('A', 1)],
                [('A', 1), ('C#', 2)],
                [('C#', 2), ('E', 2)],
            ]
        ),
    ]
)
def test_pairs_note_default_dist(
    notation,
    scale_pairs,
    result_pair_pairs
):
    """
    Test if pairs function works on the notation layer
    when omitting the distance parameter
    """

    scale = notation.scale(
        [notation.note(*pair) for pair in scale_pairs]
    )
    result = [
        (notation.note(*first), notation.note(*second))
        for first, second in result_pair_pairs
    ]

    for i, pair in enumerate(periodic.pairs(scale)):
        expected = result[i]
        assert pair == expected
        assert pair[0].is_notated_same(expected[0])
        assert pair[1].is_notated_same(expected[1])


def test_pairs_non_period_normalized():
    """
    Test if pairs function throws correct exception if
    scale is not period normalized
    """

    scale = n_edo12.pc_scale(['C', 'D', 'E', 'F', 'G', 'A', 'B', 'C'])

    with pytest.raises(ValueError) as exc_info:
        list(periodic.pairs(scale))

    assert exc_info.value.args[0] == (
        'pairs is only defined on period normalized scales'
    )
