import pytest
from xenharmlib import EDOTuning
from xenharmlib import EDTuning
from xenharmlib import FrequencyRatio
from xenharmlib.core.note_scale import NoteScale
from xenharmlib.exc import IncompatibleOriginContexts
from xenharmlib.exc import InvalidIndexMask
from ..utils import make_nat_acc_test_notation

edo12 = EDOTuning(12)
n_edo12 = make_nat_acc_test_notation(edo12)
edo24 = EDOTuning(24)
n_edo24 = make_nat_acc_test_notation(edo24)
edo31 = EDOTuning(31)
n_edo31 = make_nat_acc_test_notation(edo31)
ed13_3 = EDTuning(13, FrequencyRatio(3))
n_ed13_3 = make_nat_acc_test_notation(ed13_3)


def test_init_incompatible_origin_contexts():
    """
    Test that IncompatibleOriginContexts exception is raised
    in constructor when given notes are not from the
    given notational context
    """

    n_edo12 = make_nat_acc_test_notation(edo12)
    n_edo12_2 = make_nat_acc_test_notation(edo12)

    with pytest.raises(IncompatibleOriginContexts):
        NoteScale(
            n_edo12,
            [n_edo12_2.note('A', 0)]
        )


@pytest.mark.parametrize(
    'notation, notes, pitch_indices',
    [
        (n_edo12, [('A', 0), ('C+', 0), ('B', 1)], [0, 5, 14]),
        (n_edo12, [('C+', 0), ('A', 0), ('B', 1)], [0, 5, 14]),
    ]
)
def test_pitch_scale(notation, notes, pitch_indices):
    """
    Test if property pitch_scale returns the pitches of the notes
    added to the scale in an ordered fashion
    """

    note_scale = NoteScale(
        notation,
        [notation.note(*note_pair) for note_pair in notes]
    )

    tuning = notation.tuning

    with pytest.deprecated_call():
        expected = tuning.pitch_scale(
            [tuning.pitch(pitch_index) for pitch_index in pitch_indices]
        )
    note_scale.pitch_scale == expected

    expected = tuning.scale(
        [tuning.pitch(pitch_index) for pitch_index in pitch_indices]
    )
    note_scale.pitch_scale == expected


@pytest.mark.parametrize(
    'notation, notes, ordered_notes',
    [
        (
            n_edo12,
            [('A', 0), ('C+', 0), ('B', 1)],
            [('A', 0), ('C+', 0), ('B', 1)],
        ),
        (
            n_edo12,
            [('B', 1), ('C+', 0), ('A', 0)],
            [('A', 0), ('C+', 0), ('B', 1)],
        ),
    ]
)
def test_add_note(notation, notes, ordered_notes):
    """
    Test that add_note insorts notes correctly
    """

    note_scale = NoteScale(notation)

    for pc_symbol, nat_bi_index in notes:
        note_scale.add_note(
            notation.note(pc_symbol, nat_bi_index)
        )

    ordered_note_list = []

    for pc_symbol, nat_bi_index in ordered_notes:
        ordered_note_list.append(
            notation.note(pc_symbol, nat_bi_index)
        )

    note_list = list(note_scale)
    assert note_list == ordered_note_list


def test_add_note_incompatible_origin_contexts():
    """
    Test that IncompatibleOriginContexts exception is raised
    when note is added that is from a different notational
    context
    """

    n_edo12 = make_nat_acc_test_notation(edo12)
    n_edo12_2 = make_nat_acc_test_notation(edo12)

    with pytest.raises(IncompatibleOriginContexts):
        note_scale = NoteScale(n_edo12)
        note_scale.add_note(n_edo12_2.note('A', 0))


@pytest.mark.parametrize(
    'notation, input_pairs, result_pairs',
    [
        (
            n_edo12,
            [('B+', 1), ('C+', 0), ('A', 0)],
            [('A', 0), ('C+', 0), ('B+', 1)],
        ),
        (
            n_edo12,
            [('B+', 1), ('C+', 0), ('A', 0), ('A+++', 1)],
            [('A', 0), ('C+', 0), ('B+', 1)],
        ),
        (
            n_edo31,
            [('A', 0), ('C+', 0), ('B+', 1)],
            [('A', 0), ('C+', 0), ('B+', 1)],
        )
    ]
)
def test_sort_on_init(notation, input_pairs, result_pairs):
    """
    Test if notes get sorted correctly on scale init
    """

    scale = NoteScale(
        notation,
        [notation.note(*pair) for pair in input_pairs]
    )

    assert len(scale) == len(result_pairs)
    pitches = list(scale)
    assert pitches == [notation.note(*pair) for pair in result_pairs]


@pytest.mark.parametrize(
    'tuning',
    [
        n_edo12, n_edo24, n_edo31, n_ed13_3
    ]
)
def test_init_empty(tuning):
    """
    Test if note scale can be created by omitting notes parameter
    """

    scale = NoteScale(tuning)

    assert len(scale) == 0
    notes = list(scale)
    assert notes == []


def test_eq():
    """
    Test if scale equalities and inequalities work correctly
    """

    scale_a = NoteScale(
        n_edo12,
        [
            n_edo12.note('A', 0),
            n_edo12.note('A+', 0),
            n_edo12.note('B', 0),
        ]
    )
    scale_a_enharm = NoteScale(
        n_edo12,
        [
            n_edo12.note('A', 0),
            n_edo12.note('B-', 0),
            n_edo12.note('A++', 0),
        ]
    )
    scale_b = NoteScale(
        n_edo12,
        [
            n_edo12.note('A', 0),
            n_edo12.note('A+', 0),
            n_edo12.note('B', 0),
        ]
    )
    scale_c = NoteScale(
        n_edo12,
        [
            n_edo12.note('A', 0),
            n_edo12.note('A+', 0),
            n_edo12.note('B', 0),
            n_edo12.note('B+', 0),
        ]
    )
    scale_d = NoteScale(
        n_edo31,
        [
            n_edo31.note('A', 0),
            n_edo31.note('A+', 0),
            n_edo31.note('B', 0),
        ]
    )
    scale_e = NoteScale(
        n_edo24,
        [
            n_edo24.note('A', 0),
            n_edo24.note('B', 0),
            n_edo24.note('C', 0),
        ]
    )

    assert scale_a == scale_a
    assert scale_a == scale_a_enharm
    assert scale_a_enharm == scale_a
    assert scale_a == scale_b
    assert scale_a == scale_e
    assert scale_a != scale_c
    assert scale_a != scale_d
    assert 'XYZ' != scale_a
    assert 3 != scale_a
    assert scale_a != 'XYZ'
    assert scale_a != 3


@pytest.mark.parametrize(
    'notation, note_pairs_a, note_pairs_b, result',
    [
        (
            n_edo12,
            [('A', 0), ('C+', 0), ('B+', 1)],
            [('A', 0), ('C+', 0), ('B+', 1)],
            True
        ),
        (
            n_edo24,
            [('A', 0), ('C+', 0), ('B+', 1)],
            [('A', 0), ('C-', 0), ('B+', 1)],
            False
        ),
        (
            n_edo31,
            [('A', 0), ('C+', 0), ('B-', 1)],
            [('A', 0), ('C+', 0)],
            False
        )
    ]
)
def test_is_notated_same(notation, note_pairs_a, note_pairs_b, result):
    """
    Test if is_notated_same works correctly
    """

    scale_a = NoteScale(
        notation,
        [notation.note(*pair) for pair in note_pairs_a]
    )
    scale_b = NoteScale(
        notation,
        [notation.note(*pair) for pair in note_pairs_b]
    )
    assert scale_a.is_notated_same(scale_b) == result


@pytest.mark.parametrize(
    'notation, input_pairs, result_pairs',
    [
        (
            n_edo12,
            [('B+', 1), ('C+', 0), ('A', 0)],
            [('A', 0), ('C+', 0), ('B+', 1)],
        ),
        (
            n_edo24,
            [('B+', 1), ('C+', 0), ('A', 0), ('A++', 1)],
            [('A', 0), ('C+', 0), ('A++', 1), ('B+', 1)],
        ),
        (
            n_edo31,
            [('A', 0), ('C+', 0), ('B-', 1)],
            [('A', 0), ('C+', 0), ('B-', 1)],
        ),
        (
            n_ed13_3,
            [('B', 0), ('C+-', 0), ('F+', 1)],
            [('B', 0), ('C+-', 0), ('F+', 1)],
        )
    ]
)
def test_getitem(notation, input_pairs, result_pairs):
    """
    Test if fetching single note items works correctly
    """

    scale = NoteScale(
        notation,
        [notation.note(*pair) for pair in input_pairs]
    )
    for i, pair in enumerate(result_pairs):
        expected_note = notation.note(*pair)
        assert scale[i] == expected_note
        assert scale[i].is_notated_same(
            expected_note
        )


@pytest.mark.parametrize(
    'notation, input_pairs, start, stop, result_pairs',
    [
        (
            n_edo12,
            [('B+', 1), ('C+', 0), ('A', 0)],
            0, 2,
            [('A', 0), ('C+', 0)],
        ),
        (
            n_edo24,
            [('B+', 1), ('C+', 0), ('A', 0), ('A+++', 1)],
            1, 3,
            [('C+', 0), ('B+', 1)],
        ),
        (
            n_edo31,
            [('A', 0), ('C+', 0), ('B-', 1)],
            0, 3,
            [('A', 0), ('C+', 0), ('B-', 1)],
        ),
        (
            n_edo31,
            [('B', 1), ('C+', 1), ('E-', 1), ('F+', 1)],
            0, -1,
            [('B', 1), ('C+', 1), ('E-', 1)],
        ),
        (
            n_ed13_3,
            [('B', 0), ('C+-', 0), ('F+', 1)],
            -3, -2,
            [('B', 0)],
        )
    ]
)
def test_getitem_slice(notation, input_pairs, start, stop, result_pairs):
    """
    Test if slicing of scales works correctly
    """

    scale = NoteScale(
        notation,
        [notation.note(*pair) for pair in input_pairs]
    )
    scale_b = NoteScale(
        notation,
        [notation.note(*pair) for pair in result_pairs]
    )
    assert scale[start:stop] == scale_b


@pytest.mark.parametrize(
    'notation, input_pairs, start, result_pairs',
    [
        (
            n_edo12,
            [('B+', 1), ('C+', 0), ('A', 0)],
            0,
            [('A', 0), ('C+', 0), ('B+', 1)],
        ),
        (
            n_edo24,
            [('B+', 1), ('C+', 0), ('A', 0), ('A+++', 1)],
            1,
            [('C+', 0), ('B+', 1), ('A+++', 1)],
        ),
        (
            n_edo31,
            [('A', 0), ('C+', 0), ('B-', 1)],
            -2,
            [('C+', 0), ('B-', 1)],
        ),
        (
            n_edo31,
            [('B', 1), ('C+', 1), ('E-', 1), ('F+', 1)],
            -3,
            [('C+', 1), ('E-', 1), ('F+', 1)],
        ),
        (
            n_ed13_3,
            [('B', 0), ('C+-', 0), ('F+', 1)],
            2,
            [('F+', 1)],
        )
    ]
)
def test_getitem_slice_omit_stop(notation,
                                 input_pairs,
                                 start,
                                 result_pairs):
    """
    Test if slicing of scales works correctly when
    stop parameter is omitted
    """

    scale = NoteScale(
        notation,
        [notation.note(*pair) for pair in input_pairs]
    )
    scale_b = NoteScale(
        notation,
        [notation.note(*pair) for pair in result_pairs]
    )
    assert scale[start:] == scale_b


@pytest.mark.parametrize(
    'notation, input_pairs, stop, result_pairs',
    [
        (
            n_edo12,
            [('B+', 1), ('C+', 0), ('A', 0)],
            2,
            [('A', 0), ('C+', 0)],
        ),
        (
            n_edo24,
            [('B+', 1), ('C+', 0), ('A', 0), ('A+++', 1)],
            1,
            [('A', 0)],
        ),
        (
            n_edo31,
            [('A', 0), ('C+', 0), ('B-', 1)],
            -1,
            [('A', 0), ('C+', 0)],
        ),
        (
            n_edo31,
            [('B', 1), ('C+', 1), ('E-', 1), ('F+', 1)],
            3,
            [('B', 1), ('C+', 1), ('E-', 1)],
        ),
        (
            n_ed13_3,
            [('B', 0), ('C+-', 0), ('F+', 1)],
            -2,
            [('B', 0)],
        ),
        (
            n_ed13_3,
            [('B', 0), ('C+-', 0), ('F+', 1)],
            -3,
            [],
        )
    ]
)
def test_getitem_slice_omit_start(notation,
                                  input_pairs,
                                  stop,
                                  result_pairs):
    """
    Test if slicing of scales works correctly when
    start parameter is omitted
    """

    scale = NoteScale(
        notation,
        [notation.note(*pair) for pair in input_pairs]
    )
    scale_b = NoteScale(
        notation,
        [notation.note(*pair) for pair in result_pairs]
    )
    assert scale[:stop] == scale_b


@pytest.mark.parametrize(
    'notation, input_pcsym, mask, exp_pcsym',
    [
        (n_edo12,  ['A', 'B', 'C'],              1,              ['B']),
        (n_edo31,  ['A+', 'C', 'F+'],            ...,            ['A+', 'C', 'F+']),
        (n_edo12,  ['A', 'B', 'C'],              (1,),           ['B']),
        (n_edo31,  ['A+', 'C', 'F+'],            (...,),         ['A+', 'C', 'F+']),
        (n_edo31,  ['B', 'C+', 'G+', 'C'],       (1, 2),         ['C+', 'G+']),
        (n_edo31,  ['B', 'C+', 'G+', 'C'],       (1, ...),       ['C+', 'G+', 'C']),
        (n_edo31,  ['E+', 'F', 'H', 'I+', 'J'],  (0, 2, 4),      ['E+', 'H', 'J']),
        (n_edo31,  ['E+', 'F', 'H', 'I+', 'J'],  (..., 2, 4),    ['E+', 'F', 'H', 'J']),
        (n_edo31,  ['E+', 'F', 'H', 'I+', 'J'],  (0, ..., 2, 4), ['E+', 'F', 'H', 'J']),
        (n_edo31,  ['E+', 'F', 'H', 'I+', 'J'],  (0, 2, ..., 4), ['E+', 'H', 'I+', 'J']),
        (n_edo31,  ['E+', 'F', 'H', 'I+', 'J'],  (2, ..., 100),  ['H', 'I+', 'J']),
    ]
)
def test_partial(notation, input_pcsym, mask, exp_pcsym):
    """
    Test if partial function of scales works correctly
    """

    scale = notation.pc_scale(input_pcsym)
    expected_scale = notation.pc_scale(exp_pcsym)
    assert scale.partial(mask).is_notated_same(expected_scale)


@pytest.mark.parametrize(
    'notation, mask',
    [
        (n_edo31,  (-1, ..., 2, 4)),
        (n_edo31,  (..., 4, 3)),
        (n_edo31,  (..., 4, 3, ...)),
        (n_edo31,  (3, 2, ...)),
        (n_edo31,  (1, 2, -1)),
    ]
)
def test_partial_invalid_mask(notation, mask):
    """
    Test if partial function of scales raises correct exception
    when invalid mask is given
    """

    scale = notation.pc_scale(['A', 'B+', 'D', 'F'])

    with pytest.raises(InvalidIndexMask):
        scale.partial(mask)


@pytest.mark.parametrize(
    'notation, input_pcsym, mask, exp_pcsym',
    [
        (n_edo12,  ['A', 'B', 'C'],              1,              ['A', 'C']),
        (n_edo31,  ['A+', 'C', 'F+'],            ...,            []),
        (n_edo12,  ['A', 'B', 'C'],              (1,),           ['A', 'C']),
        (n_edo31,  ['A+', 'C', 'F+'],            (...,),         []),
        (n_edo31,  ['B', 'C+', 'G+', 'H'],       (1, 2),         ['B', 'H']),
        (n_edo31,  ['B', 'C+', 'G+', 'C'],       (1, ...),       ['B']),
        (n_edo31,  ['E+', 'F', 'H', 'I+', 'J'],  (0, 2, 4),      ['F', 'I+']),
        (n_edo31,  ['E+', 'F', 'H', 'I+', 'J'],  (..., 2, 4),    ['I+']),
        (n_edo31,  ['E+', 'F', 'H', 'I+', 'J'],  (0, ..., 2, 4), ['I+']),
        (n_edo31,  ['E+', 'F', 'H', 'I+', 'J'],  (0, 2, ..., 4), ['F']),
        (n_edo31,  ['E+', 'F', 'H', 'I+', 'J'],  (2, ..., 100),  ['E+', 'F']),
    ]
)
def test_partial_not(notation, input_pcsym, mask, exp_pcsym):
    """
    Test if partial_not function of scales works correctly
    """

    scale = notation.pc_scale(input_pcsym)
    expected_scale = notation.pc_scale(exp_pcsym)
    assert scale.partial_not(mask).is_notated_same(expected_scale)


@pytest.mark.parametrize(
    'notation, mask',
    [
        (n_edo31,  (-1, ..., 2, 4)),
        (n_edo31,  (..., 4, 3)),
        (n_edo31,  (..., 4, 3, ...)),
        (n_edo31,  (3, 2, ...)),
        (n_edo31,  (1, 2, -1)),
    ]
)
def test_partial_not_invalid_mask(notation, mask):
    """
    Test if partial_not function of scales raises correct exception
    when invalid mask is given
    """

    scale = notation.pc_scale(['A', 'B+', 'D', 'F'])

    with pytest.raises(InvalidIndexMask):
        scale.partial_not(mask)


@pytest.mark.parametrize(
    'notation, input_pcsym, mask',
    [
        (n_edo12,  ['A', 'B', 'C'],              1),
        (n_edo31,  ['A+', 'C', 'F+'],            ...),
        (n_edo12,  ['A', 'B', 'C'],              (1,)),
        (n_edo31,  ['A+', 'C', 'F+'],            (...,)),
        (n_edo31,  ['B', 'C+', 'G+', 'C'],       (1, 2)),
        (n_edo31,  ['B', 'C+', 'G+', 'C'],       (1, ...)),
        (n_edo31,  ['E+', 'F', 'H', 'I+', 'J'],  (0, 2, 4)),
        (n_edo31,  ['E+', 'F', 'H', 'I+', 'J'],  (..., 2, 4)),
        (n_edo31,  ['E+', 'F', 'H', 'I+', 'J'],  (0, ..., 2, 4)),
        (n_edo31,  ['E+', 'F', 'H', 'I+', 'J'],  (0, 2, ..., 4)),
        (n_edo31,  ['E+', 'F', 'H', 'I+', 'J'],  (2, ..., 100))
    ]
)
def test_partition(notation, input_pcsym, mask):
    """
    Test if partition function of scales works correctly
    """

    scale = notation.pc_scale(input_pcsym)

    positive = scale.partial(mask)
    complement = scale.partial_not(mask)
    a, b = scale.partition(mask)
    assert a.is_notated_same(positive)
    assert b.is_notated_same(complement)


@pytest.mark.parametrize(
    'notation, mask',
    [
        (n_edo31,  (-1, ..., 2, 4)),
        (n_edo31,  (..., 4, 3)),
        (n_edo31,  (..., 4, 3, ...)),
        (n_edo31,  (3, 2, ...)),
        (n_edo31,  (1, 2, -1)),
    ]
)
def test_partition_invalid_mask(notation, mask):
    """
    Test if partition function of scales raises correct exception
    when invalid mask is given
    """

    scale = notation.pc_scale(['A', 'B+', 'D', 'F'])

    with pytest.raises(InvalidIndexMask):
        scale.partition(mask)


@pytest.mark.parametrize(
    'notation_a, input_pairs_a, notation_b, input_pairs_b',
    [
        (
            n_edo12,
            [('E', 0), ('B+', 0), ('D+', 0)],
            n_edo12,
            [('E', 0), ('B+', 0), ('D+', 0)],
        ),
        (
            n_edo12,
            [('A', 0), ('B+', 0), ('C', 0)],
            n_edo24,
            [('A', 0), ('D', 0), ('E', 0)],
        ),
        (
            n_edo24,
            [('A', 0), ('B+', 1), ('C', 1)],
            n_edo24,
            [('A', 0), ('B+', 1), ('C', 1)],
        ),
    ]
)
def test_in_operator_note(notation_a,
                          input_pairs_a,
                          notation_b,
                          input_pairs_b):
    """
    Test if 'in' operator works on single notes
    """

    scale = NoteScale(
        notation_a,
        [notation_a.note(*pair) for pair in input_pairs_a]
    )

    for pair in input_pairs_b:
        assert notation_b.note(*pair) in scale


@pytest.mark.parametrize(
    'notation_a, input_pairs_a, notation_b, input_pairs_b',
    [
        (
            n_edo12,
            [('E', 0), ('B+', 0), ('D+', 0)],
            n_edo12,
            [('A', 0), ('C+', 0), ('F', 0)],
        ),
        (
            n_edo12,
            [('A', 0), ('B+', 0), ('C', 0)],
            n_edo24,
            [('A+', 0), ('C', 0), ('C-', 0)],
        ),
        (
            n_edo24,
            [('A', 0), ('B+', 1), ('C', 1)],
            n_edo24,
            [('A+', 0), ('D.', 2), ('C-', 3)],
        ),
    ]
)
def test_not_in_operator_note(notation_a,
                              input_pairs_a,
                              notation_b,
                              input_pairs_b):
    """
    Test if 'not in' operator works on single notes
    """

    scale = NoteScale(
        notation_a,
        [notation_a.note(*pair) for pair in input_pairs_a]
    )

    for pair in input_pairs_b:
        assert notation_b.note(*pair) not in scale


@pytest.mark.parametrize(
    'notation, input_pairs, tuning, input_pi',
    [
        (
            n_edo12,
            [('E', 0), ('B+', 0), ('D+', 0)],
            edo12,
            [8, 3, 7]
        ),
        (
            n_edo12,
            [('A', 0), ('B+', 0), ('C', 0)],
            edo24,
            [0, 6, 8]
        ),
        (
            n_edo24,
            [('A', 0), ('B+', 1), ('C', 1)],
            edo24,
            [0, 27, 28]
        ),
    ]
)
def test_in_operator_pitch(notation, input_pairs, tuning, input_pi):
    """
    Test if 'in' operator works on single pitches
    """

    scale = NoteScale(
        notation,
        [notation.note(*pair) for pair in input_pairs]
    )

    for pitch_index in input_pi:
        assert tuning.pitch(pitch_index) in scale


@pytest.mark.parametrize(
    'notation, input_pairs, tuning, input_pi',
    [
        (
            n_edo12,
            [('E', 0), ('B+', 0), ('D+', 0)],
            edo12,
            [0, 9, 4, 13, 22, 16]
        ),
        (
            n_edo12,
            [('A', 0), ('B+', 0), ('C', 0)],
            edo24,
            [11, 4, 16, 33, 5, 9]
        ),
        (
            n_edo24,
            [('A', 0), ('B+', 1), ('C', 1)],
            edo24,
            [2, 4, 66, 14, 17]
        ),
    ]
)
def test_not_in_operator_pitch(notation, input_pairs, tuning, input_pi):
    """
    Test if 'not in' operator works on single pitches
    """

    scale = NoteScale(
        notation,
        [notation.note(*pair) for pair in input_pairs]
    )

    for pitch_index in input_pi:
        assert tuning.pitch(pitch_index) not in scale


@pytest.mark.parametrize(
    'notation_a, input_pairs, notation_b, intervals',
    [
        (
            n_edo12,
            [('E', 0), ('B+', 0), ('D+', 0)],
            n_edo12,
            [(('E', 0), ('B+', 0)), (('D+', 0), ('E', 0))],
        ),
        (
            n_edo12,
            [('A', 0), ('B+', 0), ('C', 0)],
            n_edo24,
            [(('A+', 0), ('E+', 0)), (('C', 0), ('B', 0))],
        ),
        (
            n_edo24,
            [('A', 0), ('B+', 1), ('C', 1)],
            n_edo24,
            [(('B-', 0), ('C', 1)), (('C', 1), ('A', 0))],
        ),
    ]
)
def test_in_operator_note_interval(notation_a,
                                   input_pairs,
                                   notation_b,
                                   intervals):
    """
    Test if 'in' operator works on note intervals
    """

    scale = NoteScale(
        notation_a,
        [notation_a.note(*pair) for pair in input_pairs]
    )

    for note_pair_a, note_pair_b in intervals:
        assert notation_b.note(*note_pair_a).interval(
            notation_b.note(*note_pair_b)
        ) in scale


@pytest.mark.parametrize(
    'notation_a, input_pairs, notation_b, intervals',
    [
        (
            n_edo12,
            [('E', 0), ('B+', 0), ('D+', 0)],
            n_edo12,
            [(('E', 1), ('B+', 0)), (('D+', 0), ('E', 1))],
        ),
        (
            n_edo12,
            [('A', 0), ('B+', 0), ('C', 0)],
            n_edo31,
            [(('A+', 0), ('E+', 0)), (('C', 0), ('B', 0))],
        ),
        (
            n_edo24,
            [('A', 0), ('B+', 1), ('C', 1)],
            n_edo24,
            [(('B', 0), ('C', 1)), (('C', 1), ('A', 1))],
        ),
    ]
)
def test_not_in_operator_note_interval(notation_a,
                                       input_pairs,
                                       notation_b,
                                       intervals):
    """
    Test if 'not in' operator works on note intervals
    """

    scale = NoteScale(
        notation_a,
        [notation_a.note(*pair) for pair in input_pairs]
    )

    for note_pair_a, note_pair_b in intervals:
        assert notation_b.note(*note_pair_a).interval(
            notation_b.note(*note_pair_b)
        ) not in scale


@pytest.mark.parametrize(
    'notation, input_pairs, tuning, intervals',
    [
        (
            n_edo12,
            [('E', 0), ('B+', 0), ('D+', 0)],
            edo12,
            [(6, 2), (7, 6)],
        ),
        (
            n_edo12,
            [('A', 0), ('B+', 0), ('C', 0)],
            edo24,
            [(1, 9), (4, 2)],
        ),
        (
            n_edo24,
            [('A', 0), ('B+', 1), ('C', 1)],
            edo24,
            [(1, 28), (4, 5)],
        ),
    ]
)
def test_in_operator_pitch_interval(notation,
                                    input_pairs,
                                    tuning,
                                    intervals):
    """
    Test if 'in' operator works on pitch intervals
    """

    scale = NoteScale(
        notation,
        [notation.note(*pair) for pair in input_pairs]
    )

    for pi_a, pi_b in intervals:
        assert tuning.pitch(pi_a).interval(
            tuning.pitch(pi_b)
        ) in scale


@pytest.mark.parametrize(
    'notation, input_pairs, tuning, intervals',
    [
        (
            n_edo12,
            [('E', 0), ('B+', 0), ('D+', 0)],
            edo12,
            [(6, 0), (7, 22)],
        ),
        (
            n_edo12,
            [('A', 0), ('B+', 0), ('C', 0)],
            edo24,
            [(1, 30), (-4, 9)],
        ),
        (
            n_edo24,
            [('A', 0), ('B+', 1), ('C', 1)],
            edo24,
            [(1, 10), (4, -5)],
        ),
    ]
)
def test_not_in_operator_pitch_interval(notation,
                                        input_pairs,
                                        tuning,
                                        intervals):
    """
    Test if 'not in' operator works on pitch intervals
    """

    scale = NoteScale(
        notation,
        [notation.note(*pair) for pair in input_pairs]
    )

    for pi_a, pi_b in intervals:
        assert tuning.pitch(pi_a).interval(
            tuning.pitch(pi_b)
        ) not in scale


@pytest.mark.parametrize(
    'notation',
    [
        n_edo12, n_edo31, n_edo24
    ]
)
def test_in_operator_bogus(notation):
    """
    Test if 'in' operator returns False on non-supported types
    """

    scale = NoteScale(
        notation,
        [notation.note('A', 0), notation.note('B+', 1)]
    )

    assert 'XYZ' not in scale
    assert 8 not in scale
    assert False not in scale


@pytest.mark.parametrize(
    'notation, input_pairs, repr_str',
    [
        (n_edo12, [('A', 0), ('B', 1), ('C+', 1)], 'NoteScale([A0, B1, C+1], 12-EDO)'),
        (n_edo24, [('C+', 0), ('B-', 0), ('C+', 1)], 'NoteScale([B-0, C+0, C+1], 24-EDO)'),
    ]
)
def test_repr(notation, input_pairs, repr_str):
    """
    Test if repr() returns the right string for scale
    """

    scale = NoteScale(
        notation,
        [notation.note(*pair) for pair in input_pairs]
    )
    assert repr(scale) == repr_str


@pytest.mark.parametrize(
    'notation',
    [
        n_edo12, n_edo24, n_edo31
    ]
)
def test_frequencies(notation):
    """
    Test if frequencies property works correctly
    """

    scale = NoteScale(
        notation,
        [
            notation.note('A', 0),
            notation.note('C+', 3),
            notation.note('D-', 2),
        ]
    )

    tuning = notation.tuning

    assert scale.frequencies == [
        tuning.pitch(0).frequency,
        tuning.pitch(5+2*len(tuning)).frequency,
        tuning.pitch(5+3*len(tuning)).frequency,
    ]


@pytest.mark.parametrize(
    'notation, input_pairs, result_pi',
    [
        (
            n_edo12,
            [('E', 0), ('B+', 0), ('D+', 0)],
            [3, 7, 8]
        ),
        (
            n_edo12,
            [('A', 0), ('B+', 0), ('C', 0)],
            [0, 3, 4]
        ),
        (
            n_edo24,
            [('A', 0), ('B+', 1), ('C', 1)],
            [0, 27, 28]
        ),
    ]
)
def test_pitch_indices(notation, input_pairs, result_pi):
    """
    Test if pitch_indices property is correct
    """

    scale = NoteScale(
        notation,
        [notation.note(*pair) for pair in input_pairs]
    )

    assert scale.pitch_indices == result_pi


@pytest.mark.parametrize(
    'notation, input_pairs, intervals',
    [
        (
            n_edo12,
            [('A+', 0), ('B+', 0), ('D+', 0)],
            [(('A+', 0), ('B+', 0)), (('B+', 0), ('D+', 0))],
        ),
        (
            n_edo12,
            [('A', 0), ('B+', 0), ('C', 0)],
            [(('A', 0), ('B+', 0)), (('B+', 0), ('C', 0))],
        ),
        (
            n_edo24,
            [('A', 0), ('B+', 1), ('C', 1)],
            [(('A', 0), ('B+', 1)), (('B+', 1), ('C', 1))],
        ),
    ]
)
def test_to_note_intervals(notation, input_pairs, intervals):
    """
    Test if to_note_intervals method works correctly
    """

    scale = NoteScale(
        notation,
        [notation.note(*pair) for pair in input_pairs]
    )

    note_intervals = []
    for note_a, note_b in intervals:
        interval = notation.note(*note_a).interval(
            notation.note(*note_b)
        )
        note_intervals.append(interval)

    with pytest.deprecated_call():
        assert scale.to_note_intervals() == note_intervals

    assert scale.to_intervals() == note_intervals


@pytest.mark.parametrize(
    'notation, input_pairs, interval, result_pairs',
    [
        (
            n_edo12,
            [('A+', 0), ('B+', 0), ('D+', 0)],
            (('A', 0), ('B', 0)),
            [('B+', 0), ('C+', 0), ('E+', 0)],
        ),
        (
            n_edo12,
            [('A+', 0), ('B+', 1), ('F', 2)],
            (('A', 0), ('B', 1)),
            [('B+', 1), ('C+', 2), ('A', 4)],
        ),
        (
            n_edo24,
            [('A+', 0), ('B+', 1), ('F', 2)],
            (('B', 0), ('A', 0)),
            [('L+', -1), ('A+', 1), ('E', 2)],
        ),
        (
            n_edo24,
            [('A+', 0), ('B+', 1), ('F', 2)],
            (('B', 1), ('A', 0)),
            [('L+', -2), ('A+', 0), ('E', 1)],
        ),
    ]
)
def test_transpose_interval(notation, input_pairs, interval, result_pairs):
    """
    Test if transpose method works correctly when given an interval
    """

    scale = NoteScale(
        notation,
        [notation.note(*pair) for pair in input_pairs]
    )

    note_a, note_b = interval
    note_interval = notation.note(*note_a).interval(
        notation.note(*note_b)
    )

    transposed = scale.transpose(note_interval)

    with pytest.deprecated_call():
        assert transposed == notation.note_scale(
            [notation.note(*pair) for pair in result_pairs]
        )

    assert transposed == notation.scale(
        [notation.note(*pair) for pair in result_pairs]
    )


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

    scale = NoteScale(
        notation,
        [notation.note(*pair) for pair in input_pairs]
    )

    transposed = scale.transpose_bi_index(bi_diff)

    with pytest.deprecated_call():
        assert transposed == notation.note_scale(
            [notation.note(*pair) for pair in result_pairs]
        )

    assert transposed == notation.scale(
        [notation.note(*pair) for pair in result_pairs]
    )


@pytest.mark.parametrize(
    'notation, input_pairs_a, input_pairs_b, result_pairs',
    [
        (
            n_edo12,
            [('A+', 0), ('B+', 0), ('D+', 0)],
            [('A+', 0), ('C', 0), ('D+', 0)],
            [('A+', 0), ('B+', 0), ('C', 0), ('D+', 0)],
        ),
        (
            n_edo12,
            [('A+', 0), ('B+', 1), ('F', 2)],
            [('A+', 0), ('B+', 1), ('F', 2)],
            [('A+', 0), ('B+', 1), ('F', 2)],
        ),
        (
            n_edo24,
            [('A+', 0), ('B+', 1), ('F+', 2)],
            [('A', 0), ('B', 0), ('F', 2)],
            [('A', 0), ('A+', 0), ('B', 0), ('B+', 1), ('F', 2), ('F+', 2)],
        ),
        (
            n_edo24,
            [('A+', 0), ('B+', 1), ('F', 2)],
            [],
            [('A+', 0), ('B+', 1), ('F', 2)],
        ),
    ]
)
def test_union(notation, input_pairs_a, input_pairs_b, result_pairs):
    """
    Test if union operation works correctly
    """

    scale_a = NoteScale(
        notation,
        [notation.note(*pair) for pair in input_pairs_a]
    )

    scale_b = NoteScale(
        notation,
        [notation.note(*pair) for pair in input_pairs_b]
    )

    scale_c = scale_a.union(scale_b)
    assert len(scale_c) == len(result_pairs)
    notes = list(scale_c)
    assert notes == [notation.note(*pair) for pair in result_pairs]

    scale_c = scale_a | scale_b
    assert len(scale_c) == len(result_pairs)
    notes = list(scale_c)
    assert notes == [notation.note(*pair) for pair in result_pairs]


def test_union_incompatible_origin_contexts():
    """
    Test if union operation fails if scales originate from
    different notations
    """

    n_edo12_2 = make_nat_acc_test_notation(edo12)
    notations = n_edo12, n_edo24, n_edo31, n_edo12_2

    for i, notation_a in enumerate(notations):

        for notation_b in notations[i+1:]:

            scale_a = NoteScale(
                notation_a
            )
            scale_b = NoteScale(
                notation_b
            )

            with pytest.raises(IncompatibleOriginContexts):
                scale_a.union(scale_b)

            with pytest.raises(IncompatibleOriginContexts):
                scale_a | scale_b


@pytest.mark.parametrize(
    'notation, input_pairs_a, input_pairs_b, result_pairs',
    [
        (
            n_edo12,
            [('A+', 0), ('B+', 0), ('D+', 0)],
            [('A+', 0), ('C', 0), ('D+', 0)],
            [('A+', 0), ('D+', 0)],
        ),
        (
            n_edo12,
            [('A+', 0), ('B+', 0), ('D+', 0)],
            [('A+', 0), ('C', 0), ('E-', 0)],
            [('A+', 0), ('D+', 0)],
        ),
        (
            n_edo12,
            [('A+', 0), ('B+', 1), ('F', 2)],
            [('A+', 0), ('C-', 1), ('Ex', 2)],
            [('A+', 0), ('B+', 1), ('F', 2)],
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
def test_intersection(notation, input_pairs_a, input_pairs_b, result_pairs):
    """
    Test if intersection operation works correctly
    """

    scale_a = NoteScale(
        notation,
        [notation.note(*pair) for pair in input_pairs_a]
    )

    scale_b = NoteScale(
        notation,
        [notation.note(*pair) for pair in input_pairs_b]
    )

    scale_c = scale_a.intersection(scale_b)
    assert len(scale_c) == len(result_pairs)
    notes = list(scale_c)
    assert notes == [notation.note(*pair) for pair in result_pairs]

    scale_c = scale_a & scale_b
    assert len(scale_c) == len(result_pairs)
    notes = list(scale_c)
    assert notes == [notation.note(*pair) for pair in result_pairs]


@pytest.mark.parametrize(
    'notation, input_pairs_a, input_pairs_b, result_pairs',
    [
        (
            n_edo12,
            [('A+', 0), ('B+', 0), ('D+', 0)],
            [('A+', 0), ('C', 0), ('D+', 0)],
            [('A+', 0), ('D+', 0)],
        ),
        (
            n_edo12,
            [('A+', 0), ('B+', 0), ('D+', 0)],
            [('A+', 0), ('C', 0), ('E-', 0)],
            [('A+', 0)],
        ),
        (
            n_edo12,
            [('A+', 0), ('B+', 1), ('F', 2)],
            [('A+', 0), ('C-', 1), ('Ex', 2)],
            [('A+', 0)],
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
def test_note_intersection(
    notation,
    input_pairs_a,
    input_pairs_b,
    result_pairs
):
    """
    Test if note_intersection operation works correctly
    """

    scale_a = NoteScale(
        notation,
        [notation.note(*pair) for pair in input_pairs_a]
    )

    scale_b = NoteScale(
        notation,
        [notation.note(*pair) for pair in input_pairs_b]
    )

    scale_c = scale_a.note_intersection(scale_b)

    assert len(scale_c) == len(result_pairs)
    notes = list(scale_c)
    assert notes == [notation.note(*pair) for pair in result_pairs]


def test_intersection_incompatible_origin_contexts():
    """
    Test if intersection operation fails if scales originate from
    different notations
    """

    n_edo12_2 = make_nat_acc_test_notation(edo12)
    notations = n_edo12, n_edo24, n_edo31, n_edo12_2

    for i, notation_a in enumerate(notations):

        for notation_b in notations[i+1:]:

            scale_a = NoteScale(
                notation_a
            )
            scale_b = NoteScale(
                notation_b
            )

            with pytest.raises(IncompatibleOriginContexts):
                scale_a.intersection(scale_b)

            with pytest.raises(IncompatibleOriginContexts):
                scale_a & scale_b


def test_note_intersection_incompatible_origin_contexts():
    """
    Test if note_intersection operation fails if scales originate from
    different notations
    """

    n_edo12_2 = make_nat_acc_test_notation(edo12)
    notations = n_edo12, n_edo24, n_edo31, n_edo12_2

    for i, notation_a in enumerate(notations):

        for notation_b in notations[i+1:]:

            scale_a = NoteScale(
                notation_a
            )
            scale_b = NoteScale(
                notation_b
            )

            with pytest.raises(IncompatibleOriginContexts):
                scale_a.note_intersection(scale_b)


@pytest.mark.parametrize(
    'notation, input_pairs_a, input_pairs_b, result_pairs',
    [
        (
            n_edo12,
            [('A+', 0), ('B+', 0), ('D+', 0)],
            [('A+', 0), ('C', 0), ('D+', 0)],
            [('B+', 0)],
        ),
        (
            n_edo12,
            [('A+', 0), ('B+', 0), ('D+', 0)],
            [('A+', 0), ('C', 0), ('E-', 0)],
            [('B+', 0)],
        ),
        (
            n_edo12,
            [('A+', 0), ('B+', 1), ('F', 2)],
            [('A+', 0), ('C-', 1), ('Ex', 2)],
            [],
        ),
        (
            n_edo24,
            [('A+', 0), ('B+', 1), ('F+', 2)],
            [('A', 0), ('B', 0), ('F', 2)],
            [('A+', 0), ('B+', 1), ('F+', 2)],
        ),
        (
            n_edo24,
            [('A+', 0), ('B+', 1), ('F', 2)],
            [],
            [('A+', 0), ('B+', 1), ('F', 2)],
        ),
    ]
)
def test_difference(notation, input_pairs_a, input_pairs_b, result_pairs):
    """
    Test if difference operation works correctly
    """

    scale_a = NoteScale(
        notation,
        [notation.note(*pair) for pair in input_pairs_a]
    )

    scale_b = NoteScale(
        notation,
        [notation.note(*pair) for pair in input_pairs_b]
    )

    scale_c = scale_a.difference(scale_b)
    assert len(scale_c) == len(result_pairs)
    notes = list(scale_c)
    assert notes == [notation.note(*pair) for pair in result_pairs]

    scale_c = scale_a - scale_b
    assert len(scale_c) == len(result_pairs)
    notes = list(scale_c)
    assert notes == [notation.note(*pair) for pair in result_pairs]


@pytest.mark.parametrize(
    'notation, input_pairs_a, input_pairs_b, result_pairs',
    [
        (
            n_edo12,
            [('A+', 0), ('B+', 0), ('D+', 0)],
            [('A+', 0), ('C', 0), ('D+', 0)],
            [('B+', 0)],
        ),
        (
            n_edo12,
            [('A+', 0), ('B+', 0), ('D+', 0)],
            [('A+', 0), ('C', 0), ('E-', 0)],
            [('B+', 0), ('D+', 0)],
        ),
        (
            n_edo12,
            [('A+', 0), ('B+', 1), ('F', 2)],
            [('A+', 0), ('C-', 1), ('Ex', 2)],
            [('B+', 1), ('F', 2)],
        ),
        (
            n_edo24,
            [('A+', 0), ('B+', 1), ('F+', 2)],
            [('A', 0), ('B', 0), ('F', 2)],
            [('A+', 0), ('B+', 1), ('F+', 2)],
        ),
        (
            n_edo24,
            [('A+', 0), ('B+', 1), ('F', 2)],
            [],
            [('A+', 0), ('B+', 1), ('F', 2)],
        ),
    ]
)
def test_note_difference(
    notation,
    input_pairs_a,
    input_pairs_b,
    result_pairs
):
    """
    Test if note_difference operation works correctly
    """

    scale_a = NoteScale(
        notation,
        [notation.note(*pair) for pair in input_pairs_a]
    )

    scale_b = NoteScale(
        notation,
        [notation.note(*pair) for pair in input_pairs_b]
    )

    scale_c = scale_a.note_difference(scale_b)

    assert len(scale_c) == len(result_pairs)
    notes = list(scale_c)
    assert notes == [notation.note(*pair) for pair in result_pairs]


def test_difference_incompatible_origin_contexts():
    """
    Test if difference operation fails if scales originate from
    different notations
    """

    n_edo12_2 = make_nat_acc_test_notation(edo12)
    notations = n_edo12, n_edo24, n_edo31, n_edo12_2

    for i, notation_a in enumerate(notations):

        for notation_b in notations[i+1:]:

            scale_a = NoteScale(
                notation_a
            )
            scale_b = NoteScale(
                notation_b
            )

            with pytest.raises(IncompatibleOriginContexts):
                scale_a.difference(scale_b)

            with pytest.raises(IncompatibleOriginContexts):
                scale_a - scale_b


def test_note_difference_incompatible_origin_contexts():
    """
    Test if note_difference operation fails if scales originate from
    different notations
    """

    n_edo12_2 = make_nat_acc_test_notation(edo12)
    notations = n_edo12, n_edo24, n_edo31, n_edo12_2

    for i, notation_a in enumerate(notations):

        for notation_b in notations[i+1:]:

            scale_a = NoteScale(
                notation_a
            )
            scale_b = NoteScale(
                notation_b
            )

            with pytest.raises(IncompatibleOriginContexts):
                scale_a.note_difference(scale_b)


@pytest.mark.parametrize(
    'notation, input_pairs_a, input_pairs_b, result_pairs',
    [
        (
            n_edo12,
            [('A+', 0), ('B+', 0), ('D+', 0)],
            [('A+', 0), ('C', 0), ('D+', 0)],
            [('B+', 0), ('C', 0)],
        ),
        (
            n_edo12,
            [('A+', 0), ('B+', 1), ('F', 2)],
            [('A+', 0), ('B+', 1), ('F', 2)],
            [],
        ),
        (
            n_edo24,
            [('A+', 0), ('B+', 1), ('F+', 2)],
            [('A', 0), ('B', 0), ('F', 2)],
            [('A', 0), ('A+', 0), ('B', 0), ('B+', 1), ('F', 2), ('F+', 2)],
        ),
        (
            n_edo24,
            [('A+', 0), ('B+', 1), ('F', 2)],
            [],
            [('A+', 0), ('B+', 1), ('F', 2)],
        ),
    ]
)
def test_symmetric_difference(notation, input_pairs_a, input_pairs_b, result_pairs):
    """
    Test if symmetric_difference operation works correctly
    """

    scale_a = NoteScale(
        notation,
        [notation.note(*pair) for pair in input_pairs_a]
    )

    scale_b = NoteScale(
        notation,
        [notation.note(*pair) for pair in input_pairs_b]
    )

    scale_c = scale_a.symmetric_difference(scale_b)
    assert len(scale_c) == len(result_pairs)
    notes = list(scale_c)
    assert notes == [notation.note(*pair) for pair in result_pairs]

    scale_c = scale_a ^ scale_b
    assert len(scale_c) == len(result_pairs)
    notes = list(scale_c)
    assert notes == [notation.note(*pair) for pair in result_pairs]


def test_symmetric_difference_incompatible_origin_contexts():
    """
    Test if symmetric_difference operation fails if scales originate from
    different notations
    """

    n_edo12_2 = make_nat_acc_test_notation(edo12)
    notations = n_edo12, n_edo24, n_edo31, n_edo12_2

    for i, notation_a in enumerate(notations):

        for notation_b in notations[i+1:]:

            scale_a = NoteScale(
                notation_a
            )
            scale_b = NoteScale(
                notation_b
            )

            with pytest.raises(IncompatibleOriginContexts):
                scale_a.symmetric_difference(scale_b)

            with pytest.raises(IncompatibleOriginContexts):
                scale_a ^ scale_b


@pytest.mark.parametrize(
    'notation, input_pairs_a, input_pairs_b, expected',
    [
        (
            n_edo12,
            [('A+', 0), ('B+', 0), ('D+', 0)],
            [('A+', 0), ('C', 0), ('D+', 0)],
            False
        ),
        (
            n_edo12,
            [('A+', 0), ('B+', 0), ('D+', 0)],
            [('A+', 0), ('C', 0), ('E-', 0)],
            False
        ),
        (
            n_edo12,
            [('A+', 0), ('B+', 1), ('F', 2)],
            [('A+', 0), ('C-', 1), ('Ex', 2)],
            False
        ),
        (
            n_edo24,
            [('A+', 0), ('B+', 1), ('F+', 2)],
            [('A', 0), ('B', 0), ('F', 2)],
            True
        ),
        (
            n_edo24,
            [('A+', 0), ('B+', 1), ('F', 2)],
            [],
            True
        ),
    ]
)
def test_is_disjoint(notation, input_pairs_a, input_pairs_b, expected):
    """
    Test if is_disjoint operation works correctly
    """

    scale_a = NoteScale(
        notation,
        [notation.note(*pair) for pair in input_pairs_a]
    )

    scale_b = NoteScale(
        notation,
        [notation.note(*pair) for pair in input_pairs_b]
    )

    assert scale_a.is_disjoint(scale_b) == expected


@pytest.mark.parametrize(
    'notation, input_pairs_a, input_pairs_b, expected',
    [
        (
            n_edo12,
            [('A+', 0), ('B+', 0), ('D+', 0)],
            [('A+', 0), ('C', 0), ('D+', 0)],
            False
        ),
        (
            n_edo12,
            [('A+', 0), ('B+', 0), ('D+', 0)],
            [('A+', 0), ('C', 0), ('E-', 0)],
            False
        ),
        (
            n_edo12,
            [('A+', 0), ('B+', 1), ('F', 2)],
            [('A+', 0), ('C-', 1), ('Ex', 2)],
            False
        ),
        (
            n_edo24,
            [('A+', 0), ('B+', 1), ('F+', 2)],
            [('A', 0), ('B', 0), ('F', 2)],
            True
        ),
        (
            n_edo24,
            [('A+', 0), ('B+', 1), ('F', 2)],
            [],
            True
        ),
    ]
)
def test_is_notated_disjoint(notation, input_pairs_a, input_pairs_b, expected):
    """
    Test if is_notated_disjoint operation works correctly
    """

    scale_a = NoteScale(
        notation,
        [notation.note(*pair) for pair in input_pairs_a]
    )

    scale_b = NoteScale(
        notation,
        [notation.note(*pair) for pair in input_pairs_b]
    )

    assert scale_a.is_notated_disjoint(scale_b) == expected


def test_is_disjoint_incompatible_origin_contexts():
    """
    Test if is_disjoint operation fails if scales originate from
    different notations
    """

    n_edo12_2 = make_nat_acc_test_notation(edo12)
    notations = n_edo12, n_edo24, n_edo31, n_edo12_2

    for i, notation_a in enumerate(notations):

        for notation_b in notations[i+1:]:

            scale_a = NoteScale(
                notation_a
            )
            scale_b = NoteScale(
                notation_b
            )

            with pytest.raises(IncompatibleOriginContexts):
                scale_a.is_disjoint(scale_b)


def test_is_notated_disjoint_incompatible_origin_contexts():
    """
    Test if is_notated_disjoint operation fails if scales originate from
    different notations
    """

    n_edo12_2 = make_nat_acc_test_notation(edo12)
    notations = n_edo12, n_edo24, n_edo31, n_edo12_2

    for i, notation_a in enumerate(notations):

        for notation_b in notations[i+1:]:

            scale_a = NoteScale(
                notation_a
            )
            scale_b = NoteScale(
                notation_b
            )

            with pytest.raises(IncompatibleOriginContexts):
                scale_a.is_notated_disjoint(scale_b)


@pytest.mark.parametrize(
    'notation, input_pairs_a, input_pairs_b, expected',
    [
        (
            n_edo12,
            [('A+', 0), ('D+', 0)],
            [('A+', 0), ('B+', 0), ('D+', 0)],
            True
        ),
        (
            n_edo12,
            [('A+', 0), ('E-', 0)],
            [('A+', 0), ('B+', 0), ('D+', 0)],
            True
        ),
        (
            n_edo12,
            [('A+', 0), ('B+', 1), ('F', 2)],
            [('A+', 0), ('C-', 1), ('Ex', 2)],
            True
        ),
        (
            n_edo24,
            [('A+', 0), ('B+', 1), ('F+', 2)],
            [('A', 0), ('B', 0), ('F', 2)],
            False
        ),
        (
            n_edo24,
            [],
            [('A+', 0), ('B+', 1), ('F', 2)],
            True
        ),
        (
            n_edo24,
            [('A+', 0), ('B+', 1), ('F', 2)],
            [],
            False
        ),
    ]
)
def test_is_subset(notation, input_pairs_a, input_pairs_b, expected):
    """
    Test if is_subset operation works correctly
    """

    scale_a = NoteScale(
        notation,
        [notation.note(*pair) for pair in input_pairs_a]
    )

    scale_b = NoteScale(
        notation,
        [notation.note(*pair) for pair in input_pairs_b]
    )

    assert scale_a.is_subset(scale_b) == expected


@pytest.mark.parametrize(
    'notation, input_pairs_a, input_pairs_b, expected',
    [
        (
            n_edo12,
            [('A+', 0), ('D+', 0)],
            [('A+', 0), ('B+', 0), ('D+', 0)],
            True
        ),
        (
            n_edo12,
            [('A+', 0), ('E-', 0)],
            [('A+', 0), ('B+', 0), ('D+', 0)],
            True
        ),
        (
            n_edo12,
            [('A+', 0), ('B+', 1), ('F', 2)],
            [('A+', 0), ('C-', 1), ('Ex', 2)],
            False
        ),
        (
            n_edo24,
            [('A+', 0), ('B+', 1), ('F+', 2)],
            [('A', 0), ('B', 0), ('F', 2)],
            False
        ),
        (
            n_edo24,
            [],
            [('A+', 0), ('B+', 1), ('F', 2)],
            True
        ),
        (
            n_edo24,
            [('A+', 0), ('B+', 1), ('F', 2)],
            [],
            False
        ),
    ]
)
def test_is_subset_proper(notation, input_pairs_a, input_pairs_b, expected):
    """
    Test if is_subset operation works correctly
    on proper=True
    """

    scale_a = NoteScale(
        notation,
        [notation.note(*pair) for pair in input_pairs_a]
    )

    scale_b = NoteScale(
        notation,
        [notation.note(*pair) for pair in input_pairs_b]
    )

    assert scale_a.is_subset(scale_b, proper=True) == expected


@pytest.mark.parametrize(
    'notation, input_pairs_a, input_pairs_b, expected',
    [
        (
            n_edo12,
            [('A+', 0), ('D+', 0)],
            [('A+', 0), ('B+', 0), ('D+', 0)],
            True
        ),
        (
            n_edo12,
            [('A+', 0), ('B+', 0), ('D+', 0)],
            [('A+', 0), ('B+', 0), ('D+', 0)],
            True
        ),
        (
            n_edo12,
            [('A+', 0), ('E-', 0)],
            [('A+', 0), ('B+', 0), ('D+', 0)],
            False
        ),
        (
            n_edo12,
            [('A+', 0), ('B+', 1), ('F', 2)],
            [('A+', 0), ('C-', 1), ('Ex', 2)],
            False
        ),
        (
            n_edo24,
            [('A+', 0), ('B+', 1), ('F+', 2)],
            [('A', 0), ('B', 0), ('F', 2)],
            False
        ),
        (
            n_edo24,
            [],
            [('A+', 0), ('B+', 1), ('F', 2)],
            True
        ),
        (
            n_edo24,
            [('A+', 0), ('B+', 1), ('F', 2)],
            [],
            False
        ),
    ]
)
def test_is_note_subset(notation, input_pairs_a, input_pairs_b, expected):
    """
    Test if is_note_subset operation works correctly
    """

    scale_a = NoteScale(
        notation,
        [notation.note(*pair) for pair in input_pairs_a]
    )

    scale_b = NoteScale(
        notation,
        [notation.note(*pair) for pair in input_pairs_b]
    )

    assert scale_a.is_note_subset(scale_b) == expected


@pytest.mark.parametrize(
    'notation, input_pairs_a, input_pairs_b, expected',
    [
        (
            n_edo12,
            [('A+', 0), ('D+', 0)],
            [('A+', 0), ('B+', 0), ('D+', 0)],
            True
        ),
        (
            n_edo12,
            [('A+', 0), ('B+', 0), ('D+', 0)],
            [('A+', 0), ('B+', 0), ('D+', 0)],
            False
        ),
        (
            n_edo12,
            [('A+', 0), ('E-', 0)],
            [('A+', 0), ('B+', 0), ('D+', 0)],
            False
        ),
        (
            n_edo12,
            [('A+', 0), ('B+', 1), ('F', 2)],
            [('A+', 0), ('C-', 1), ('Ex', 2)],
            False
        ),
        (
            n_edo24,
            [('A+', 0), ('B+', 1), ('F+', 2)],
            [('A', 0), ('B', 0), ('F', 2)],
            False
        ),
        (
            n_edo24,
            [],
            [('A+', 0), ('B+', 1), ('F', 2)],
            True
        ),
        (
            n_edo24,
            [('A+', 0), ('B+', 1), ('F', 2)],
            [],
            False
        ),
    ]
)
def test_is_note_subset_proper(
    notation,
    input_pairs_a,
    input_pairs_b,
    expected
):
    """
    Test if is_note_subset operation works correctly
    on proper=True
    """

    scale_a = NoteScale(
        notation,
        [notation.note(*pair) for pair in input_pairs_a]
    )

    scale_b = NoteScale(
        notation,
        [notation.note(*pair) for pair in input_pairs_b]
    )

    assert scale_a.is_note_subset(
        scale_b,
        proper=True
    ) == expected


def test_is_subset_incompatible_origin_contexts():
    """
    Test if is_subset operation fails if scales originate from
    different notations
    """

    n_edo12_2 = make_nat_acc_test_notation(edo12)
    notations = n_edo12, n_edo24, n_edo31, n_edo12_2

    for i, notation_a in enumerate(notations):

        for notation_b in notations[i+1:]:

            scale_a = NoteScale(
                notation_a
            )
            scale_b = NoteScale(
                notation_b
            )

            with pytest.raises(IncompatibleOriginContexts):
                scale_a.is_subset(scale_b)


def test_is_note_subset_incompatible_origin_contexts():
    """
    Test if is_note_subset operation fails if scales originate from
    different notations
    """

    n_edo12_2 = make_nat_acc_test_notation(edo12)
    notations = n_edo12, n_edo24, n_edo31, n_edo12_2

    for i, notation_a in enumerate(notations):

        for notation_b in notations[i+1:]:

            scale_a = NoteScale(
                notation_a
            )
            scale_b = NoteScale(
                notation_b
            )

            with pytest.raises(IncompatibleOriginContexts):
                scale_a.is_note_subset(scale_b)


@pytest.mark.parametrize(
    'notation, input_pairs_a, input_pairs_b, expected',
    [
        (
            n_edo12,
            [('A+', 0), ('B+', 0), ('D+', 0)],
            [('A+', 0), ('D+', 0)],
            True
        ),
        (
            n_edo12,
            [('A+', 0), ('B+', 0), ('D+', 0)],
            [('A+', 0), ('E-', 0)],
            True
        ),
        (
            n_edo12,
            [('A+', 0), ('C-', 1), ('Ex', 2)],
            [('A+', 0), ('B+', 1), ('F', 2)],
            True
        ),
        (
            n_edo24,
            [('A', 0), ('B', 0), ('F', 2)],
            [('A+', 0), ('B+', 1), ('F+', 2)],
            False
        ),
        (
            n_edo24,
            [('A+', 0), ('B+', 1), ('F', 2)],
            [],
            True
        ),
        (
            n_edo24,
            [],
            [('A+', 0), ('B+', 1), ('F', 2)],
            False
        ),
    ]
)
def test_is_superset(notation, input_pairs_a, input_pairs_b, expected):
    """
    Test if is_superset operation works correctly
    """

    scale_a = NoteScale(
        notation,
        [notation.note(*pair) for pair in input_pairs_a]
    )

    scale_b = NoteScale(
        notation,
        [notation.note(*pair) for pair in input_pairs_b]
    )

    assert scale_a.is_superset(scale_b) == expected


@pytest.mark.parametrize(
    'notation, input_pairs_a, input_pairs_b, expected',
    [
        (
            n_edo12,
            [('A+', 0), ('B+', 0), ('D+', 0)],
            [('A+', 0), ('D+', 0)],
            True
        ),
        (
            n_edo12,
            [('A+', 0), ('B+', 0), ('D+', 0)],
            [('A+', 0), ('E-', 0)],
            True
        ),
        (
            n_edo12,
            [('A+', 0), ('C-', 1), ('Ex', 2)],
            [('A+', 0), ('B+', 1), ('F', 2)],
            False
        ),
        (
            n_edo24,
            [('A', 0), ('B', 0), ('F', 2)],
            [('A+', 0), ('B+', 1), ('F+', 2)],
            False
        ),
        (
            n_edo24,
            [('A+', 0), ('B+', 1), ('F', 2)],
            [],
            True
        ),
        (
            n_edo24,
            [],
            [('A+', 0), ('B+', 1), ('F', 2)],
            False
        ),
    ]
)
def test_is_superset_proper(notation, input_pairs_a, input_pairs_b, expected):
    """
    Test if is_superset operation works correctly
    on proper=True
    """

    scale_a = NoteScale(
        notation,
        [notation.note(*pair) for pair in input_pairs_a]
    )

    scale_b = NoteScale(
        notation,
        [notation.note(*pair) for pair in input_pairs_b]
    )

    assert scale_a.is_superset(scale_b, proper=True) == expected


@pytest.mark.parametrize(
    'notation, input_pairs_a, input_pairs_b, expected',
    [
        (
            n_edo12,
            [('A+', 0), ('B+', 0), ('D+', 0)],
            [('A+', 0), ('D+', 0)],
            True
        ),
        (
            n_edo12,
            [('A+', 0), ('B+', 0), ('D+', 0)],
            [('A+', 0), ('B+', 0), ('D+', 0)],
            True
        ),
        (
            n_edo12,
            [('A+', 0), ('B+', 0), ('D+', 0)],
            [('A+', 0), ('E-', 0)],
            False
        ),
        (
            n_edo12,
            [('A+', 0), ('C-', 1), ('Ex', 2)],
            [('A+', 0), ('B+', 1), ('F', 2)],
            False
        ),
        (
            n_edo24,
            [('A', 0), ('B', 0), ('F', 2)],
            [('A+', 0), ('B+', 1), ('F+', 2)],
            False
        ),
        (
            n_edo24,
            [('A+', 0), ('B+', 1), ('F', 2)],
            [],
            True
        ),
        (
            n_edo24,
            [],
            [('A+', 0), ('B+', 1), ('F', 2)],
            False
        ),
    ]
)
def test_is_note_superset(notation, input_pairs_a, input_pairs_b, expected):
    """
    Test if is_note_superset operation works correctly
    """

    scale_a = NoteScale(
        notation,
        [notation.note(*pair) for pair in input_pairs_a]
    )

    scale_b = NoteScale(
        notation,
        [notation.note(*pair) for pair in input_pairs_b]
    )

    assert scale_a.is_note_superset(scale_b) == expected


@pytest.mark.parametrize(
    'notation, input_pairs_a, input_pairs_b, expected',
    [
        (
            n_edo12,
            [('A+', 0), ('B+', 0), ('D+', 0)],
            [('A+', 0), ('D+', 0)],
            True
        ),
        (
            n_edo12,
            [('A+', 0), ('B+', 0), ('D+', 0)],
            [('A+', 0), ('B+', 0), ('D+', 0)],
            False
        ),
        (
            n_edo12,
            [('A+', 0), ('B+', 0), ('D+', 0)],
            [('A+', 0), ('E-', 0)],
            False
        ),
        (
            n_edo12,
            [('A+', 0), ('C-', 1), ('Ex', 2)],
            [('A+', 0), ('B+', 1), ('F', 2)],
            False
        ),
        (
            n_edo24,
            [('A', 0), ('B', 0), ('F', 2)],
            [('A+', 0), ('B+', 1), ('F+', 2)],
            False
        ),
        (
            n_edo24,
            [('A+', 0), ('B+', 1), ('F', 2)],
            [],
            True
        ),
        (
            n_edo24,
            [],
            [('A+', 0), ('B+', 1), ('F', 2)],
            False
        ),
    ]
)
def test_is_note_superset_proper(
    notation,
    input_pairs_a,
    input_pairs_b,
    expected
):
    """
    Test if is_note_superset operation works correctly
    on proper=True
    """

    scale_a = NoteScale(
        notation,
        [notation.note(*pair) for pair in input_pairs_a]
    )

    scale_b = NoteScale(
        notation,
        [notation.note(*pair) for pair in input_pairs_b]
    )

    assert scale_a.is_note_superset(
        scale_b,
        proper=True
    ) == expected


def test_is_superset_incompatible_origin_contexts():
    """
    Test if is_superset operation fails if scales originate from
    different notations
    """

    n_edo12_2 = make_nat_acc_test_notation(edo12)
    notations = n_edo12, n_edo24, n_edo31, n_edo12_2

    for i, notation_a in enumerate(notations):

        for notation_b in notations[i+1:]:

            scale_a = NoteScale(
                notation_a
            )
            scale_b = NoteScale(
                notation_b
            )

            with pytest.raises(IncompatibleOriginContexts):
                scale_a.is_superset(scale_b)


def test_is_note_superset_incompatible_origin_contexts():
    """
    Test if is_note_superset operation fails if scales originate from
    different notations
    """

    n_edo12_2 = make_nat_acc_test_notation(edo12)
    notations = n_edo12, n_edo24, n_edo31, n_edo12_2

    for i, notation_a in enumerate(notations):

        for notation_b in notations[i+1:]:

            scale_a = NoteScale(
                notation_a
            )
            scale_b = NoteScale(
                notation_b
            )

            with pytest.raises(IncompatibleOriginContexts):
                scale_a.is_note_superset(scale_b)
