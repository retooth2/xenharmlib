import pytest
from xenharmlib import EDOTuning
from xenharmlib import UpDownNotation
from xenharmlib import periodic
from xenharmlib.exc import IncompatibleOriginContexts

edo12 = EDOTuning(12)
n_edo12 = UpDownNotation(edo12)
edo24 = EDOTuning(24)
n_edo24 = UpDownNotation(edo24)
edo31 = EDOTuning(31)
n_edo31 = UpDownNotation(edo31)


@pytest.mark.parametrize(
    'tuning, scale_pi, index, result_pi',
    [
        (edo12, [2, 4, 6, 7, 9, 11], 0, 2),
        (edo12, [2, 4, 6, 7, 9, 11], -1, -1),
        (edo24, [2, 3, 5, 7, 9, 12, 14, 19, 22], 10, 27),
        (edo31, [2, 4, 6, 7, 9, 11, 14, 19, 22], -1, -9),
    ]
)
def test_scale_element_pitch(tuning, scale_pi, index, result_pi):
    """
    Test if scale_element works correctly on the pitch layer
    """

    scale = tuning.index_scale(scale_pi)
    expected_pitch = tuning.pitch(result_pi)

    assert periodic.scale_element(scale, index) == expected_pitch


@pytest.mark.parametrize(
    'notation, scale_pairs, index, result_pair',
    [
        (
            n_edo12,
            [('C', 1), ('D', 1), ('E', 1), ('F#', 1), ('A', 1)],
            0,
            ('C', 1)
        ),
        (
            n_edo12,
            [('C', 1), ('D', 1), ('E', 1), ('F#', 1), ('A', 1)],
            3,
            ('F#', 1)
        ),
        (
            n_edo12,
            [('C', 1), ('D', 1), ('E', 1), ('F#', 1), ('A', 1)],
            5,
            ('C', 2)
        ),
        (
            n_edo12,
            [('C', 1), ('D', 1), ('E', 1), ('F#', 1), ('A', 1)],
            12,
            ('E', 3)
        ),
        (
            n_edo12,
            [('C', 1), ('D', 1), ('E', 1), ('F#', 1), ('A', 1)],
            -4,
            ('D', 0)
        )
    ]
)
def test_scale_element_note(notation, scale_pairs, index, result_pair):
    """
    Test if scale_element works correctly on the notation layer
    """

    scale = notation.scale(
        [notation.note(*pair) for pair in scale_pairs]
    )
    expected_note = notation.note(*result_pair)

    assert periodic.scale_element(scale, index) == expected_note
    assert periodic.scale_element(scale, index).is_notated_same(
        expected_note
    )


def test_scale_element_non_period_normalized():
    """
    Test if scale_element raises ValueError if scale is not
    period normalized
    """

    scale = n_edo31.pc_scale(['C', 'E', 'G', 'B', 'D', 'F'])

    with pytest.raises(ValueError) as exc_info:
        periodic.scale_element(scale, 10)

    assert exc_info.value.args[0] == (
        'scale_element is only defined on period normalized scales'
    )


@pytest.mark.parametrize(
    'tuning, scale_pi, element_pi, result_index',
    [
        (edo12, [2, 4, 6, 7, 9, 11], 2, 0),
        (edo12, [2, 4, 6, 7, 9, 11], -1, -1),
        (edo24, [2, 3, 5, 7, 9, 12, 14, 19, 22], 27, 10),
        (edo31, [2, 4, 6, 7, 9, 11, 14, 19, 22], -9, -1),
    ]
)
def test_index_pitch(tuning, scale_pi, element_pi, result_index):
    """
    Test if index function works correctly on the pitch layer
    """

    scale = tuning.index_scale(scale_pi)
    element = tuning.pitch(element_pi)

    assert periodic.index(scale, element) == result_index


@pytest.mark.parametrize(
    'notation, scale_pairs, element_pair, result_index',
    [
        (
            n_edo12,
            [('C', 1), ('D', 1), ('E', 1), ('F#', 1), ('A', 1)],
            ('C', 1),
            0
        ),
        (
            n_edo12,
            [('C', 1), ('D', 1), ('E', 1), ('F#', 1), ('A', 1)],
            ('F#', 1),
            3
        ),
        (
            n_edo12,
            [('C', 1), ('D', 1), ('E', 1), ('F#', 1), ('A', 1)],
            ('C', 2),
            5
        ),
        (
            n_edo12,
            [('C', 1), ('D', 1), ('E', 1), ('F#', 1), ('A', 1)],
            ('E', 3),
            12
        ),
        (
            n_edo12,
            [('C', 1), ('D', 1), ('E', 1), ('F#', 1), ('A', 1)],
            ('D', 0),
            -4
        ),
        (
            n_edo12,
            [('A', 1), ('B', 1), ('C#', 2), ('D#', 2), ('F', 2)],
            ('D#', 3),
            8
        )
    ]
)
def test_index_note(notation, scale_pairs, element_pair, result_index):
    """
    Test if index function works correctly on the notation layer
    """

    scale = notation.scale(
        [notation.note(*pair) for pair in scale_pairs]
    )
    element = notation.note(*element_pair)
    assert periodic.index(scale, element) == result_index


def test_index_non_period_normalized():
    """
    Test if index raises ValueError if scale is not
    period normalized
    """

    scale = n_edo31.pc_scale(['C', 'E', 'G', 'B', 'D', 'F'])
    element = n_edo31.note('C', 0)

    with pytest.raises(ValueError) as exc_info:
        periodic.index(scale, element)

    assert exc_info.value.args[0] == (
        'index is only defined on period normalized scales'
    )


def test_index_not_found():
    """
    Test if index raises ValueError if element is not found in
    periodic extension of the scale
    """

    scale = n_edo31.pc_scale(['C', 'E', 'G', 'B'])
    element = n_edo31.note('D#', 1)

    with pytest.raises(ValueError) as exc_info:
        periodic.index(scale, element)

    assert exc_info.value.args[0] == (
        'UpDownNote(D#, 1, 31-EDO) was not found in '
        'periodic extension of the scale'
    )


def test_index_incompatible_origin_contexts():
    """
    Test if index raises correct error if origin contexts of
    scale and note do not match
    """

    scale = n_edo12.pc_scale(['C', 'E', 'G', 'B'])
    element = n_edo24.note('E', 1)

    with pytest.raises(IncompatibleOriginContexts):
        periodic.index(scale, element)


@pytest.mark.parametrize(
    'tuning, scale_pi, mask_expr, result_scale_pi',
    [
        (edo12, [2, 4, 6, 7, 9, 11], (1, 3), [4, 7]),
        (edo12, [2, 4, 6, 7, 9, 11], (1, ..., 4), [4, 6, 7, 9]),
        (edo12, [2, 4, 6, 7, 9, 11], (5, ..., 9), [11, 14, 16, 18, 19]),
        (edo12, [2, 4, 6, 7, 9, 11], (-2, 0), [-3, 2]),
    ]
)
def test_partial_pitch(tuning, scale_pi, mask_expr, result_scale_pi):
    """
    Test if partial function works on the pitch layer
    """

    scale = tuning.index_scale(scale_pi)
    result_scale = tuning.index_scale(result_scale_pi)

    assert periodic.partial(scale, mask_expr) == result_scale


@pytest.mark.parametrize(
    'notation, scale_pairs, mask_expr, result_scale_pairs',
    [
        (
            n_edo12,
            [('C', 1), ('D', 1), ('E', 1), ('F#', 1), ('A', 1)],
            (1, ..., 4),
            [('D', 1), ('E', 1), ('F#', 1), ('A', 1)]
        ),
        (
            n_edo12,
            [('C', 1), ('D', 1), ('E', 1), ('F#', 1), ('A', 1)],
            (-2, 4),
            [('F#', 0), ('A', 1)]
        ),
        (
            n_edo12,
            [('C', 1), ('D', 1), ('E', 1), ('F#', 1), ('A', 1)],
            (4, ..., 7),
            [('A', 1), ('C', 2), ('D', 2), ('E', 2)]
        ),
        (
            n_edo24,
            [('C', 1), ('D', 1), ('E', 1), ('F#', 1), ('A', 1)],
            12,
            [('E', 3)]
        ),
        (
            n_edo31,
            [('C', 1), ('D', 1), ('E', 1), ('F#', 1), ('A', 1)],
            (-4, ..., -2),
            [('D', 0), ('E', 0), ('F#', 0)]
        )
    ]
)
def test_partial_note(
    notation,
    scale_pairs,
    mask_expr,
    result_scale_pairs
):
    """
    Test if partial function works on the notation layer
    """

    scale = notation.scale(
        [notation.note(*pair) for pair in scale_pairs]
    )
    result_scale = notation.scale(
        [notation.note(*pair) for pair in result_scale_pairs]
    )

    assert periodic.partial(scale, mask_expr) == result_scale
    assert periodic.partial(scale, mask_expr).is_notated_same(result_scale)


def test_partial_non_period_normalized():
    """
    Test if partial raises ValueError if scale is not
    period normalized
    """

    scale = n_edo31.pc_scale(['C', 'E', 'G', 'B', 'D', 'F'])

    with pytest.raises(ValueError) as exc_info:
        periodic.partial(scale, (1, ..., 2))

    assert exc_info.value.args[0] == (
        'partial is only defined on period normalized scales'
    )


@pytest.mark.parametrize(
    'tuning, scale_pi, partial_pi, mask_expr',
    [
        (edo12, [2, 4, 6, 7, 9, 11], [4, 7], (1, 3)),
        (edo12, [2, 4, 6, 7, 9, 11], [4, 6, 7, 9], (1, 2, 3, 4)),
        (edo12, [2, 4, 6, 7, 9, 11], [11, 14, 16, 18, 19], (5, 6, 7, 8, 9)),
        (edo12, [2, 4, 6, 7, 9, 11], [-3, 2], (-2, 0)),
    ]
)
def test_index_mask_pitch(
    tuning,
    scale_pi,
    partial_pi,
    mask_expr
):
    """
    Test if index_mask function works on the pitch layer
    """

    scale = tuning.index_scale(scale_pi)
    partial_ = tuning.index_scale(partial_pi)

    assert periodic.index_mask(scale, partial_) == mask_expr


@pytest.mark.parametrize(
    'notation, scale_pairs, partial_pairs, mask_expr',
    [
        (
            n_edo12,
            [('C', 1), ('D', 1), ('E', 1), ('F#', 1), ('A', 1)],
            [('D', 1), ('E', 1), ('F#', 1), ('A', 1)],
            (1, 2, 3, 4)
        ),
        (
            n_edo12,
            [('C', 1), ('D', 1), ('E', 1), ('F#', 1), ('A', 1)],
            [('F#', 0), ('A', 1)],
            (-2, 4)
        ),
        (
            n_edo12,
            [('C', 1), ('D', 1), ('E', 1), ('F#', 1), ('A', 1)],
            [('A', 1), ('C', 2), ('D', 2), ('E', 2)],
            (4, 5, 6, 7)
        ),
        (
            n_edo24,
            [('C', 1), ('D', 1), ('E', 1), ('F#', 1), ('A', 1)],
            [('E', 3)],
            (12,)
        ),
        (
            n_edo31,
            [('C', 1), ('D', 1), ('E', 1), ('F#', 1), ('A', 1)],
            [('D', 0), ('E', 0), ('F#', 0)],
            (-4, -3, -2),
        )
    ]
)
def test_index_mask_note(
    notation,
    scale_pairs,
    partial_pairs,
    mask_expr
):
    """
    Test if index_mask function works on the notation layer
    """

    scale = notation.scale(
        [notation.note(*pair) for pair in scale_pairs]
    )
    partial_ = notation.scale(
        [notation.note(*pair) for pair in partial_pairs]
    )

    assert periodic.index_mask(scale, partial_) == mask_expr


def test_index_mask_non_period_normalized():
    """
    Test if index_mask raises ValueError if scale is not
    period normalized
    """

    scale = n_edo31.pc_scale(['C', 'E', 'G', 'B', 'D', 'F'])
    partial_scale = n_edo31.pc_scale(['C', 'G', 'D', 'F'])

    with pytest.raises(ValueError) as exc_info:
        periodic.index_mask(scale, partial_scale)

    assert exc_info.value.args[0] == (
        'index_mask is only defined on period normalized scales'
    )


def test_index_mask_not_found():
    """
    Test if index_mask raises ValueError if element is not found in
    periodic extension of the scale
    """

    scale = n_edo31.pc_scale(['C', 'E', 'G', 'B'])
    partial_scale = n_edo31.pc_scale(['C', 'D', 'G'])

    with pytest.raises(ValueError) as exc_info:
        periodic.index_mask(scale, partial_scale)

    assert exc_info.value.args[0] == (
        'UpDownNote(D, 0, 31-EDO) was not found in '
        'periodic extension of the scale'
    )


def test_index_mask_incompatible_origin_contexts():
    """
    Test if index_mask raises correct error if scale and search_scale
    do not originate from the same origin context
    """

    scale = n_edo12.pc_scale(['C', 'E', 'G', 'B'])
    partial_scale = n_edo24.pc_scale(['C', 'G'])

    with pytest.raises(IncompatibleOriginContexts):
        periodic.index_mask(scale, partial_scale)


@pytest.mark.parametrize(
    'tuning, ref_scale_pi, transposable_pi, steps, result_pi',
    [
        (edo12, [2, 4, 6, 7, 9, 11], 2, 2, 6),
        (edo12, [2, 4, 6, 7, 9, 11], -1, 1, 2),
        (edo24, [2, 3, 5, 7, 9, 12, 14, 19, 22], 27, -2, 22),
        (edo31, [2, 4, 6, 7, 9, 11, 14, 19, 22], 4, 8, 33),
        (edo31, [2, 4, 6, 7, 9, 11, 14, 19, 22], 4, 0, 4),
    ]
)
def test_scalar_transpose_pitch(
    tuning,
    ref_scale_pi,
    transposable_pi,
    steps,
    result_pi
):
    """
    Test if scalar transposition works on single pitches
    """

    ref_scale = tuning.index_scale(ref_scale_pi)
    transposable = tuning.pitch(transposable_pi)
    result = tuning.pitch(result_pi)

    assert periodic.scalar_transpose(
        ref_scale,
        transposable,
        steps
    ) == result


@pytest.mark.parametrize(
    'tuning, scale_pi, transposable_scale_pi, steps, result_scale_pi',
    [
        (
            edo12,
            [2, 4, 6, 7, 9, 11],
            [2, 6, 11],
            2,
            [6, 9, 16]
        ),
        (
            edo31,
            [2, 5, 10, 18, 21, 26, 29],
            [5, 18, 21],
            -2,
            [-2, 5, 10]
        ),
        (
            edo24,
            [0, 5, 10, 18, 20, 22],
            [0, 5, 20],
            12,
            [48, 53, 68]
        ),
        (
            edo24,
            [0, 5, 10, 18, 20, 22],
            [0, 18, 22],
            0,
            [0, 18, 22],
        ),
        (
            edo12,
            [0, 2, 5, 7, 10, 11],
            [12, 19, 23],
            3,
            [19, 24, 29],
        ),
    ]
)
def test_scalar_transpose_pitch_scale(
    tuning,
    scale_pi,
    transposable_scale_pi,
    steps,
    result_scale_pi
):
    """
    Test if scalar transposition works on pitch scales
    """

    scale = tuning.index_scale(scale_pi)
    transposable = tuning.index_scale(transposable_scale_pi)
    result = tuning.index_scale(result_scale_pi)

    assert periodic.scalar_transpose(
        scale,
        transposable,
        steps
    ) == result


@pytest.mark.parametrize(
    'notation, scale_pairs, transposable_pair, steps, result_pair',
    [
        (
            n_edo12,
            [('C', 1), ('D', 1), ('E', 1), ('F#', 1), ('A', 1)],
            ('C', 1),
            2,
            ('E', 1),
        ),
        (
            n_edo12,
            [('C#', 1), ('D#', 1), ('E', 1), ('F', 1)],
            ('F', 1),
            -4,
            ('F', 0),
        ),
        (
            n_edo12,
            [('A', 1), ('B', 1), ('C#', 1), ('D#', 1), ('F', 1)],
            ('D#', 2),
            4,
            ('C#', 3),
        ),
        (
            n_edo12,
            [('C', 1), ('D', 1), ('E', 1), ('F#', 1), ('A', 1)],
            ('E', 3),
            0,
            ('E', 3),
        ),
    ]
)
def test_scalar_transpose_note(
    notation,
    scale_pairs,
    transposable_pair,
    steps,
    result_pair
):
    """
    Test if scalar transposition works on single notes
    """

    scale = notation.scale(
        [notation.note(*pair) for pair in scale_pairs]
    )
    transposable = notation.note(*transposable_pair)
    result = notation.note(*result_pair)

    assert periodic.scalar_transpose(scale, transposable, steps) == result


@pytest.mark.parametrize(
    'notation, scale_pairs, transposable_pairs, steps, result_pairs',
    [
        (
            n_edo12,
            [('C', 1), ('D', 1), ('E', 1), ('F#', 1), ('A', 1)],
            [('D', 1), ('F#', 1)],
            2,
            [('F#', 1), ('C', 2)],
        ),
        (
            n_edo12,
            [('C#', 1), ('D#', 1), ('E', 1), ('F', 1)],
            [('C#', 0), ('F', 0)],
            -3,
            [('D#', -1), ('C#', 0)],
        ),
        (
            n_edo12,
            [('A', 1), ('B', 1), ('C#', 2), ('D#', 2), ('F', 2)],
            [('D#', 2), ('A', 3)],
            2,
            [('A', 2), ('C#', 4)],
        ),
        (
            n_edo12,
            [('C', 1), ('D', 1), ('E', 1), ('F#', 1), ('A', 1)],
            [('D', 1), ('E', 1), ('A', 1)],
            0,
            [('D', 1), ('E', 1), ('A', 1)],
        ),
    ]
)
def test_scalar_transpose_note_scale(
    notation,
    scale_pairs,
    transposable_pairs,
    steps,
    result_pairs
):
    """
    Test if scalar transposition works on single note scales
    """

    scale = notation.scale(
        [notation.note(*pair) for pair in scale_pairs]
    )
    transposable = notation.scale(
        [notation.note(*t_pair) for t_pair in transposable_pairs]
    )
    result = notation.scale(
        [notation.note(*r_pair) for r_pair in result_pairs]
    )

    assert periodic.scalar_transpose(
        scale,
        transposable,
        steps
    ) == result


def test_scalar_transpose_non_period_normalized():
    """
    Test if scalar_transpose raises ValueError if ref scale is not
    period normalized
    """

    scale = n_edo31.pc_scale(['C', 'E', 'G', 'B', 'D', 'F'])
    partial_scale = n_edo31.pc_scale(['C', 'G', 'D', 'F'])

    with pytest.raises(ValueError) as exc_info:
        periodic.scalar_transpose(scale, partial_scale, 3)

    assert exc_info.value.args[0] == (
        'ref_scale must be period normalized'
    )


def test_scalar_transpose_incompatible_origin_contexts():
    """
    Test if scalar_transpose function raises IncompatibleOriginContext
    if reference scale and the transposable object do not have the same
    origin context
    """

    scale = n_edo31.pc_scale(['C', 'E', 'G', 'B'])
    note = n_edo12.note('C', 1)

    with pytest.raises(IncompatibleOriginContexts):
        periodic.scalar_transpose(scale, note, 3)

    partial_scale = n_edo12.pc_scale(['C', 'G', 'D', 'F'])

    with pytest.raises(IncompatibleOriginContexts):
        periodic.scalar_transpose(scale, partial_scale, 3)


def test_scalar_transpose_not_found():
    """
    Test if scalar_transpose raises ValueError if element is not found in
    periodic extension of the scale
    """

    scale = n_edo31.pc_scale(['C', 'E', 'G', 'B'])
    note = n_edo31.note('D#', 1)

    with pytest.raises(ValueError) as exc_info:
        periodic.scalar_transpose(scale, note, 3)

    assert exc_info.value.args[0] == (
        'UpDownNote(D#, 1, 31-EDO) was not found in '
        'periodic extension of the scale'
    )

    scale = n_edo31.pc_scale(['C', 'E', 'G', 'B'])
    partial_scale = n_edo31.pc_scale(['C', 'G#', 'B'])

    with pytest.raises(ValueError) as exc_info:
        periodic.scalar_transpose(scale, partial_scale, 3)

    assert exc_info.value.args[0] == (
        'UpDownNote(G#, 0, 31-EDO) was not found in '
        'periodic extension of the scale'
    )


@pytest.mark.parametrize(
    'tuning, scale_pi, element_pi, found',
    [
        (edo12, [2, 4, 6, 7, 9, 11], 2, True),
        (edo12, [2, 4, 6, 7, 9, 11], -1, True),
        (edo12, [2, 4, 6, 7, 9, 11], -4, False),
        (edo24, [2, 3, 5, 7, 9, 12, 14, 19, 22], 27, True),
        (edo31, [2, 4, 6, 7, 9, 11, 14, 19, 22], -9, True),
        (edo31, [2, 4, 6, 7, 9, 11, 14, 19, 22], 32, False),
    ]
)
def test_is_in_pitch(tuning, scale_pi, element_pi, found):
    """
    Test if is_in function works correctly on the pitch layer
    """

    scale = tuning.index_scale(scale_pi)
    element = tuning.pitch(element_pi)

    assert periodic.is_in(scale, element) is found


@pytest.mark.parametrize(
    'notation, scale_pairs, element_pair, found',
    [
        (
            n_edo12,
            [('C', 1), ('D', 1), ('E', 1), ('F#', 1), ('A', 1)],
            ('C', 1),
            True
        ),
        (
            n_edo12,
            [('C', 1), ('D', 1), ('E', 1), ('F#', 1), ('A', 1)],
            ('F#', 1),
            True
        ),
        (
            n_edo12,
            [('C', 1), ('D', 1), ('E', 1), ('F#', 1), ('A', 1)],
            ('D#', 1),
            False
        ),
        (
            n_edo12,
            [('C', 1), ('D', 1), ('E', 1), ('F#', 1), ('A', 1)],
            ('C', 2),
            True
        ),
        (
            n_edo12,
            [('C', 1), ('D', 1), ('E', 1), ('F#', 1), ('A', 1)],
            ('E', 3),
            True
        ),
        (
            n_edo12,
            [('C', 1), ('D', 1), ('E', 1), ('F#', 1), ('A', 1)],
            ('D', 0),
            True
        ),
        (
            n_edo12,
            [('A', 1), ('B', 1), ('C#', 2), ('D#', 2), ('F', 2)],
            ('D#', 3),
            True
        ),
        (
            n_edo12,
            [('C', 1), ('D', 1), ('E', 1), ('F#', 1), ('A', 1)],
            ('F', 3),
            False
        ),
    ]
)
def test_is_in_note(notation, scale_pairs, element_pair, found):
    """
    Test if is_in function works correctly on the notation layer
    """

    scale = notation.scale(
        [notation.note(*pair) for pair in scale_pairs]
    )
    element = notation.note(*element_pair)
    assert periodic.is_in(scale, element) is found


def test_is_in_non_period_normalized():
    """
    Test if is_in raises ValueError if scale is not
    period normalized
    """

    scale = n_edo31.pc_scale(['C', 'E', 'G', 'B', 'D', 'F'])
    element = n_edo31.note('C', 0)

    with pytest.raises(ValueError) as exc_info:
        periodic.is_in(scale, element)

    assert exc_info.value.args[0] == (
        'is_in is only defined on period normalized scales'
    )


def test_is_in_incompatible_origin_contexts():
    """
    Test if is_in raises correct error if origin contexts of
    scale and note do not match
    """

    scale = n_edo12.pc_scale(['C', 'E', 'G', 'B'])
    element = n_edo24.note('E', 1)

    with pytest.raises(IncompatibleOriginContexts):
        periodic.is_in(scale, element)
