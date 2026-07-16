import pytest
from xenharmlib import EDOTuning
from xenharmlib import EDTuning
from xenharmlib import FrequencyRatio
from xenharmlib.core.note_seq import NoteSeq
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
        NoteSeq(
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
def test_pitch_seq(notation, notes, pitch_indices):
    """
    Test if property pitch_seq returns the pitches of the notes
    added to the seq in an ordered fashion
    """

    note_seq = NoteSeq(
        notation,
        [notation.note(*note_pair) for note_pair in notes]
    )

    tuning = notation.tuning
    expected = tuning.seq(
        [tuning.pitch(pitch_index) for pitch_index in pitch_indices]
    )
    note_seq.pitch_seq == expected


@pytest.mark.parametrize(
    'notation, notes',
    [
        (
            n_edo12,
            [('A', 0), ('C+', 0), ('B', 1)],
        ),
        (
            n_edo12,
            [('B', 1), ('C+', 0), ('A', 0)],
        ),
    ]
)
def test_with_element(notation, notes):
    """
    Test that with_element constructs sequences correctly
    """

    note_seq = NoteSeq(notation)

    for pc_symbol, nat_bi_index in notes:
        note_seq = note_seq.with_element(
            notation.note(pc_symbol, nat_bi_index)
        )

    note_list = list(note_seq)
    assert note_list == [
        notation.note(*pair) for pair in notes
    ]


def test_with_element_incompatible_origin_contexts():
    """
    Test that IncompatibleOriginContexts exception is raised
    in with_element when given note is not from the
    existing notational context
    """

    n_edo12 = make_nat_acc_test_notation(edo12)
    n_edo12_2 = make_nat_acc_test_notation(edo12)
    seq = NoteSeq(
        n_edo12,
        [n_edo12.note('A', 0)]
    )

    with pytest.raises(IncompatibleOriginContexts):
        seq.with_element(n_edo12_2.note('C', 1))


@pytest.mark.parametrize(
    'tuning',
    [
        n_edo12, n_edo24, n_edo31, n_ed13_3
    ]
)
def test_init_empty(tuning):
    """
    Test if note sequence can be created by omitting notes parameter
    """

    seq = NoteSeq(tuning)

    assert len(seq) == 0
    assert list(seq) == []


def test_eq():
    """
    Test if sequence equalities and inequalities work correctly
    """

    seq_a = NoteSeq(
        n_edo12,
        [
            n_edo12.note('A', 0),
            n_edo12.note('A+', 0),
            n_edo12.note('B', 0),
        ]
    )
    seq_a_enharm = NoteSeq(
        n_edo12,
        [
            n_edo12.note('A', 0),
            n_edo12.note('B-', 0),
            n_edo12.note('A++', 0),
        ]
    )
    seq_b = NoteSeq(
        n_edo12,
        [
            n_edo12.note('A', 0),
            n_edo12.note('A+', 0),
            n_edo12.note('B', 0),
        ]
    )
    seq_c = NoteSeq(
        n_edo12,
        [
            n_edo12.note('A', 0),
            n_edo12.note('A+', 0),
            n_edo12.note('B', 0),
            n_edo12.note('B+', 0),
        ]
    )
    seq_d = NoteSeq(
        n_edo31,
        [
            n_edo31.note('A', 0),
            n_edo31.note('A+', 0),
            n_edo31.note('B', 0),
        ]
    )
    seq_e = NoteSeq(
        n_edo24,
        [
            n_edo24.note('A', 0),
            n_edo24.note('B', 0),
            n_edo24.note('C', 0),
        ]
    )

    assert seq_a == seq_a
    assert seq_a == seq_a_enharm
    assert seq_a_enharm == seq_a
    assert seq_a == seq_b
    assert seq_a == seq_e
    assert seq_a != seq_c
    assert seq_a != seq_d

    assert hash(seq_a) == hash(seq_a)
    assert hash(seq_a) == hash(seq_b)
    assert hash(seq_a) == hash(seq_a_enharm)
    assert hash(seq_a_enharm) == hash(seq_a)
    assert hash(seq_a) == hash(seq_e)
    assert hash(seq_a) != hash(seq_c)
    assert hash(seq_a) != hash(seq_d)

    assert 'XYZ' != seq_a
    assert 3 != seq_a
    assert seq_a != 'XYZ'
    assert seq_a != 3


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
            [('A', 0), ('D-', 0), ('B+', 1)],
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

    seq_a = NoteSeq(
        notation,
        [notation.note(*pair) for pair in note_pairs_a]
    )
    seq_b = NoteSeq(
        notation,
        [notation.note(*pair) for pair in note_pairs_b]
    )
    assert seq_a.is_notated_same(seq_b) == result


@pytest.mark.parametrize(
    'notation, input_pairs',
    [
        (
            n_edo12,
            [('B+', 1), ('C+', 0), ('A', 0)],
        ),
        (
            n_edo24,
            [('B+', 1), ('C+', 0), ('A', 0), ('A++', 1)],
        ),
        (
            n_edo31,
            [('A', 0), ('C+', 0), ('B-', 1)],
        ),
        (
            n_ed13_3,
            [('B', 0), ('C+-', 0), ('F+', 1)],
        )
    ]
)
def test_getitem(notation, input_pairs):
    """
    Test if fetching single note items works correctly
    """

    seq = NoteSeq(
        notation,
        [notation.note(*pair) for pair in input_pairs]
    )
    for i, pair in enumerate(input_pairs):
        expected_note = notation.note(*pair)
        assert seq[i] == expected_note
        assert seq[i].is_notated_same(
            expected_note
        )


@pytest.mark.parametrize(
    'notation, input_pairs, start, stop, result_pairs',
    [
        (
            n_edo12,
            [('B+', 1), ('C+', 0), ('A', 0)],
            0, 2,
            [('B+', 1), ('C+', 0)],
        ),
        (
            n_edo24,
            [('B+', 1), ('C+', 0), ('A', 0), ('A+++', 1)],
            1, 3,
            [('C+', 0), ('A', 0)],
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
    Test if slicing of seqs works correctly
    """

    seq = NoteSeq(
        notation,
        [notation.note(*pair) for pair in input_pairs]
    )
    seq_b = NoteSeq(
        notation,
        [notation.note(*pair) for pair in result_pairs]
    )
    assert seq[start:stop] == seq_b


@pytest.mark.parametrize(
    'notation, input_pairs, start, result_pairs',
    [
        (
            n_edo12,
            [('B+', 1), ('C+', 0), ('A', 0)],
            0,
            [('B+', 1), ('C+', 0), ('A', 0)],
        ),
        (
            n_edo24,
            [('B+', 1), ('C+', 0), ('A', 0), ('A+++', 1)],
            1,
            [('C+', 0), ('A', 0), ('A+++', 1)],
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
    Test if slicing of seqs works correctly when
    stop parameter is omitted
    """

    seq = NoteSeq(
        notation,
        [notation.note(*pair) for pair in input_pairs]
    )
    seq_b = NoteSeq(
        notation,
        [notation.note(*pair) for pair in result_pairs]
    )
    assert seq[start:] == seq_b


@pytest.mark.parametrize(
    'notation, input_pairs, stop, result_pairs',
    [
        (
            n_edo12,
            [('B+', 1), ('C+', 0), ('A', 0)],
            2,
            [('B+', 1), ('C+', 0)],
        ),
        (
            n_edo24,
            [('B+', 1), ('C+', 0), ('A', 0), ('A+++', 1)],
            1,
            [('B+', 1)],
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
    Test if slicing of seqs works correctly when
    start parameter is omitted
    """

    seq = NoteSeq(
        notation,
        [notation.note(*pair) for pair in input_pairs]
    )
    seq_b = NoteSeq(
        notation,
        [notation.note(*pair) for pair in result_pairs]
    )
    assert seq[:stop] == seq_b


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
    Test if partial function of seqs works correctly
    """

    seq = notation.seq(
        [notation.note(pcsym, 4) for pcsym in input_pcsym]
    )
    expected_seq = notation.seq(
        [notation.note(pcsym, 4) for pcsym in exp_pcsym]
    )
    assert seq.partial(mask).is_notated_same(expected_seq)


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
    Test if partial function of seqs raises correct exception
    when invalid mask is given
    """

    seq = notation.seq(
        [notation.note(*pair) for pair in [('A', 4), ('B+', 3), ('A', 1)]]
    )

    with pytest.raises(InvalidIndexMask):
        seq.partial(mask)


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
    Test if partial_not function of seqs works correctly
    """

    seq = notation.seq(
        [notation.note(pcsym, 4) for pcsym in input_pcsym]
    )
    expected_seq = notation.seq(
        [notation.note(pcsym, 4) for pcsym in exp_pcsym]
    )

    assert seq.partial_not(mask).is_notated_same(expected_seq)


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

    seq = notation.seq(
        [notation.note(*pair) for pair in [('A', 4), ('B+', 3), ('A', 1)]]
    )

    with pytest.raises(InvalidIndexMask):
        seq.partial_not(mask)


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

    seq = notation.seq(
        [notation.note(pcsym, 4) for pcsym in input_pcsym]
    )

    positive = seq.partial(mask)
    complement = seq.partial_not(mask)
    a, b = seq.partition(mask)
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
    Test if partition function of seq raises correct exception
    when invalid mask is given
    """

    seq = notation.seq(
        [notation.note(*pair) for pair in [('A', 4), ('B+', 3), ('A', 1)]]
    )

    with pytest.raises(InvalidIndexMask):
        seq.partition(mask)


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

    seq = NoteSeq(
        notation_a,
        [notation_a.note(*pair) for pair in input_pairs_a]
    )

    for pair in input_pairs_b:
        assert notation_b.note(*pair) in seq


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

    seq = NoteSeq(
        notation_a,
        [notation_a.note(*pair) for pair in input_pairs_a]
    )

    for pair in input_pairs_b:
        assert notation_b.note(*pair) not in seq


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

    seq = NoteSeq(
        notation,
        [notation.note(*pair) for pair in input_pairs]
    )

    for pitch_index in input_pi:
        assert tuning.pitch(pitch_index) in seq


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

    seq = NoteSeq(
        notation,
        [notation.note(*pair) for pair in input_pairs]
    )

    for pitch_index in input_pi:
        assert tuning.pitch(pitch_index) not in seq


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

    seq = NoteSeq(
        notation_a,
        [notation_a.note(*pair) for pair in input_pairs]
    )

    for note_pair_a, note_pair_b in intervals:
        assert notation_b.note(*note_pair_a).interval(
            notation_b.note(*note_pair_b)
        ) in seq


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

    seq = NoteSeq(
        notation_a,
        [notation_a.note(*pair) for pair in input_pairs]
    )

    for note_pair_a, note_pair_b in intervals:
        assert notation_b.note(*note_pair_a).interval(
            notation_b.note(*note_pair_b)
        ) not in seq


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

    seq = NoteSeq(
        notation,
        [notation.note(*pair) for pair in input_pairs]
    )

    for pi_a, pi_b in intervals:
        assert tuning.pitch(pi_a).interval(
            tuning.pitch(pi_b)
        ) in seq


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

    seq = NoteSeq(
        notation,
        [notation.note(*pair) for pair in input_pairs]
    )

    for pi_a, pi_b in intervals:
        assert tuning.pitch(pi_a).interval(
            tuning.pitch(pi_b)
        ) not in seq


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

    seq = NoteSeq(
        notation,
        [notation.note('A', 0), notation.note('B+', 1)]
    )

    assert 'XYZ' not in seq
    assert 8 not in seq
    assert False not in seq


@pytest.mark.parametrize(
    'notation, input_pairs, repr_str',
    [
        (n_edo12, [('A', 0), ('B', 1), ('C+', 1)], 'NoteSeq([A0, B1, C+1], 12-EDO)'),
        (n_edo24, [('C+', 0), ('B-', 0), ('C+', 1)], 'NoteSeq([C+0, B-0, C+1], 24-EDO)'),
    ]
)
def test_repr(notation, input_pairs, repr_str):
    """
    Test if repr() returns the right string for seq
    """

    seq = NoteSeq(
        notation,
        [notation.note(*pair) for pair in input_pairs]
    )
    assert repr(seq) == repr_str


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

    seq = NoteSeq(
        notation,
        [
            notation.note('A', 0),
            notation.note('D-', 2),
            notation.note('C+', 3),
        ]
    )

    tuning = notation.tuning

    assert seq.frequencies == [
        tuning.pitch(0).frequency,
        tuning.pitch(5+2*tuning.eq_diff).frequency,
        tuning.pitch(5+3*tuning.eq_diff).frequency,
    ]


@pytest.mark.parametrize(
    'notation, input_pairs, result_pi',
    [
        (
            n_edo12,
            [('E', 0), ('B+', 0), ('D+', 0)],
            [8, 3, 7]
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

    seq = NoteSeq(
        notation,
        [notation.note(*pair) for pair in input_pairs]
    )

    assert seq.pitch_indices == result_pi


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
def test_interval_seq(notation, input_pairs, intervals):
    """
    Test if to_interval_seq method works correctly
    """

    seq = NoteSeq(
        notation,
        [notation.note(*pair) for pair in input_pairs]
    )

    note_intervals = []
    for note_a, note_b in intervals:
        interval = notation.note(*note_a).interval(
            notation.note(*note_b)
        )
        note_intervals.append(interval)
    interval_seq = notation.interval_seq(note_intervals)

    assert seq.to_interval_seq() == interval_seq


@pytest.mark.parametrize(
    'notation, input_pairs, interval_notes',
    [
        (
            n_edo12,
            [('A+', 0), ('B+', 0), ('C', -1), ('D+', 0)],
            [
                (('A+', 0), ('A+', 0)),
                (('A+', 0), ('B+', 0)),
                (('A+', 0), ('C', -1)),
                (('A+', 0), ('D+', 0))
            ],
        ),
        (
            n_edo12,
            [('A', 0), ('B+', 0), ('A', 0), ('C', 1)],
            [
                (('A', 0), ('A', 0)),
                (('A', 0), ('B+', 0)),
                (('A', 0), ('A', 0)),
                (('A', 0), ('C', 1))
            ],
        ),
        (
            n_edo24,
            [('B', -1), ('B+', 0), ('C', 1)],
            [
                (('B', -1), ('B', -1)),
                (('B', -1), ('B+', 0)),
                (('B', -1), ('C', 1))
            ],
        ),
        (
            n_edo24,
            [],
            []
        ),
    ]
)
def test_to_interval_fan_no_param(notation, input_pairs, interval_notes):
    """
    Test if to_interval_fan method works correctly
    without giving additional ref parameter
    """

    seq = NoteSeq(
        notation,
        [notation.note(*pair) for pair in input_pairs]
    )

    note_intervals = []
    for note_a, note_b in interval_notes:
        interval = notation.note(*note_a).interval(
            notation.note(*note_b)
        )
        note_intervals.append(interval)

    ifan = notation.interval_fan(note_intervals)
    assert seq.to_interval_fan() == ifan


@pytest.mark.parametrize(
    'notation, input_pairs, ref_pair, interval_notes',
    [
        (
            n_edo12,
            [('A+', 0), ('B+', 0), ('D+', 0)],
            ('B+', 0),
            [
                (('B+', 0), ('A+', 0)),
                (('B+', 0), ('B+', 0)),
                (('B+', 0), ('D+', 0))
            ],
        ),
        (
            n_edo12,
            [('A', 0), ('B+', 0), ('C', 1)],
            ('A', 0),
            [
                (('A', 0), ('A', 0)),
                (('A', 0), ('B+', 0)),
                (('A', 0), ('C', 1))
            ],
        ),
        (
            n_edo24,
            [('B', -1), ('B+', 0), ('C', 1)],
            ('B', 0),
            [
                (('B', 0), ('B', -1)),
                (('B', 0), ('B+', 0)),
                (('B', 0), ('C', 1))
            ],
        ),
        (
            n_edo24,
            [],
            ('B', 0),
            [],
        ),
    ]
)
def test_to_interval_fan_ref_param(
    notation, input_pairs, ref_pair, interval_notes
):
    """
    Test if to_interval_fan method works correctly
    when giving additional ref parameter
    """

    seq = NoteSeq(
        notation,
        [notation.note(*pair) for pair in input_pairs]
    )

    note_intervals = []
    for note_a, note_b in interval_notes:
        interval = notation.note(*note_a).interval(
            notation.note(*note_b)
        )
        note_intervals.append(interval)

    ref = notation.note(*ref_pair)
    ifan = notation.interval_fan(note_intervals)
    assert seq.to_interval_fan(ref) == ifan


def test_to_interval_fan_incompatible_origin_context():
    """
    Test if to_interval_fan method raises error
    when giving incompatible ref parameter
    """

    seq = NoteSeq(
        n_edo12,
        [n_edo12.note(*pair) for pair in [('A+', 0), ('B', 1)]]
    )

    ref = n_edo24.note('A+', 0)
    with pytest.raises(IncompatibleOriginContexts) as excinfo:
        seq.to_interval_fan(ref)
    assert (
        excinfo.value.args[0] ==
        f'The ref parameter {ref} does not originate from context '
        f'{seq.origin_context}. Cannot construct interval fan.'
    )


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

    seq = NoteSeq(
        notation,
        [notation.note(*pair) for pair in input_pairs]
    )

    note_a, note_b = interval
    note_interval = notation.note(*note_a).interval(
        notation.note(*note_b)
    )

    transposed = seq.transpose(note_interval)

    assert transposed == notation.seq(
        [notation.note(*pair) for pair in result_pairs]
    )


@pytest.mark.parametrize(
    'notation, input_pairs_a, input_pairs_b, expected',
    [
        (
            n_edo12,
            [('B+', 0), ('D+', 0)],
            [('A+', 0), ('B+', 0), ('D+', 0)],
            True
        ),
        (
            n_edo12,
            [('B+', 0), ('D+', 0)],
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
def test_is_subseq(notation, input_pairs_a, input_pairs_b, expected):
    """
    Test if is_subseq operation works correctly
    """

    seq_a = NoteSeq(
        notation,
        [notation.note(*pair) for pair in input_pairs_a]
    )

    seq_b = NoteSeq(
        notation,
        [notation.note(*pair) for pair in input_pairs_b]
    )

    assert seq_a.is_subseq(seq_b) == expected


@pytest.mark.parametrize(
    'notation, input_pairs_a, input_pairs_b, expected',
    [
        (
            n_edo12,
            [('A+', 0), ('B+', 0)],
            [('A+', 0), ('B+', 0), ('D+', 0)],
            True
        ),
        (
            n_edo12,
            [('B+', 0), ('D+', 0)],
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
def test_is_subseq_proper(notation, input_pairs_a, input_pairs_b, expected):
    """
    Test if is_subseq operation works correctly
    on proper=True
    """

    seq_a = NoteSeq(
        notation,
        [notation.note(*pair) for pair in input_pairs_a]
    )

    seq_b = NoteSeq(
        notation,
        [notation.note(*pair) for pair in input_pairs_b]
    )

    assert seq_a.is_subseq(seq_b, proper=True) == expected


def test_is_subseq_cross_origin():
    """
    Test if is_subseq works across origin contexts
    """

    seq_a = n_edo12.seq(
        [
            n_edo12.note('A', 1),
            n_edo12.note('B', 2),
            n_edo12.note('C+', 1),
            n_edo12.note('C++', 1),
            n_edo12.note('B', 1),
            n_edo12.note('A', 1),
        ]
    )
    seq_b = n_edo24.seq(
        [
            n_edo24.note('F', 1),
            n_edo24.note('F++', 1),
        ]
    )
    seq_c = n_edo24.seq(
        [
            n_edo24.note('F++', 1),
            n_edo24.note('F++', 1),
        ]
    )

    assert seq_b.is_subseq(seq_a)
    assert not seq_c.is_subseq(seq_a)


@pytest.mark.parametrize(
    'notation, input_pairs_a, input_pairs_b, expected',
    [
        (
            n_edo12,
            [('A+', 0), ('B+', 0), ('D+', 0)],
            [('A+', 0), ('B+', 0)],
            True
        ),
        (
            n_edo12,
            [('A+', 0), ('B+', 0), ('D+', 0)],
            [('B+', 0), ('D+', 0)],
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
def test_is_superseq(notation, input_pairs_a, input_pairs_b, expected):
    """
    Test if is_superseq operation works correctly
    """

    seq_a = NoteSeq(
        notation,
        [notation.note(*pair) for pair in input_pairs_a]
    )

    seq_b = NoteSeq(
        notation,
        [notation.note(*pair) for pair in input_pairs_b]
    )

    assert seq_a.is_superseq(seq_b) == expected


@pytest.mark.parametrize(
    'notation, input_pairs_a, input_pairs_b, expected',
    [
        (
            n_edo12,
            [('A+', 0), ('B+', 0), ('D+', 0)],
            [('A+', 0), ('B+', 0)],
            True
        ),
        (
            n_edo12,
            [('A+', 0), ('B+', 0), ('D+', 0)],
            [('B+', 0), ('D+', 0)],
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
def test_is_superseq_proper(notation, input_pairs_a, input_pairs_b, expected):
    """
    Test if is_superseq operation works correctly
    on proper=True
    """

    seq_a = NoteSeq(
        notation,
        [notation.note(*pair) for pair in input_pairs_a]
    )

    seq_b = NoteSeq(
        notation,
        [notation.note(*pair) for pair in input_pairs_b]
    )

    assert seq_a.is_superseq(seq_b, proper=True) == expected


def test_is_superseq_cross_origin():
    """
    Test if is_superseq works across origin contexts
    """

    seq_a = n_edo12.seq(
        [
            n_edo12.note('A', 1),
            n_edo12.note('B', 2),
            n_edo12.note('C+', 1),
            n_edo12.note('C++', 1),
            n_edo12.note('B', 1),
            n_edo12.note('A', 1),
        ]
    )
    seq_b = n_edo24.seq(
        [
            n_edo24.note('F', 1),
            n_edo24.note('F++', 1),
        ]
    )
    seq_c = n_edo24.seq(
        [
            n_edo24.note('F++', 1),
            n_edo24.note('F++', 1),
        ]
    )

    assert seq_a.is_superseq(seq_b)
    assert not seq_a.is_superseq(seq_c)


@pytest.mark.parametrize(
    'notation, input_pairs, result_pairs',
    [
        (
            n_edo12,
            [('A+', 0), ('B+', 0), ('D+', 0)],
            [('A', 0), ('B', 0), ('D', 0)],
        ),
        (
            n_edo12,
            [('A+', 0), ('B', 0), ('E+', 0), ('B+', 1)],
            [('A', 0), ('B-', 0), ('E', 0), ('B', 1)],
        ),
        (
            n_edo24,
            [('C', 0), ('D+', 0), ('F', 2)],
            [('A', 0), ('B+', 0), ('D', 2)],
        ),
        (
            n_edo24,
            [('A', 0), ('B+', 0), ('F', 2)],
            [('A', 0), ('B+', 0), ('F', 2)],
        ),
        (
            n_edo24,
            [('A', 0), ('B+', 0), ('F', 0)],
            [('A', 0), ('B+', 0), ('F', 0)],
        ),
    ]
)
def test_zero_normalized(
    notation,
    input_pairs,
    result_pairs
):
    """
    Test if zero_normalized works correctly
    """

    input_seq = notation.seq(
        [notation.note(*pair) for pair in input_pairs]
    )
    result_seq = notation.seq(
        [notation.note(*pair) for pair in result_pairs]
    )
    assert input_seq.zero_normalized().is_notated_same(result_seq)


def test_zero_normalized_value_error():
    """
    Test if zero_normalized raises ValueError if seq is empty
    """

    input_seq = n_edo12.seq()
    with pytest.raises(ValueError) as excinfo:
        input_seq.zero_normalized()
    assert (
        excinfo.value.args[0] ==
        'zero_normalized is not defined on empty sequence'
    )


@pytest.mark.parametrize(
    'notation, input_pairs, expected',
    [
        (
            n_edo12,
            [('A+', 0), ('B+', 0), ('D+', 0)],
            False
        ),
        (
            n_edo12,
            [('A+', 0), ('B', 0), ('E+', 0), ('B+', 1)],
            False
        ),
        (
            n_edo24,
            [('C', 0), ('D+', 0), ('F', 2)],
            False
        ),
        (
            n_edo24,
            [('A', 0), ('B+', 0), ('F', 2)],
            True
        ),
        (
            n_edo24,
            [('A', 0), ('B+', 0), ('F', 0)],
            True
        ),
    ]
)
def test_is_zero_normalized(
    notation,
    input_pairs,
    expected
):
    """
    Test if is_zero_normalized works correctly
    """

    input_seq = notation.seq(
        [notation.note(*pair) for pair in input_pairs]
    )
    assert input_seq.is_zero_normalized == expected


def test_is_zero_normalized_value_error():
    """
    Test if is_zero_normalized raises ValueError if seq is empty
    """

    input_seq = n_edo12.seq()
    with pytest.raises(ValueError) as excinfo:
        input_seq.is_zero_normalized
    assert (
        excinfo.value.args[0] ==
        'is_zero_normalized is not defined on empty sequence'
    )


@pytest.mark.parametrize(
    'notation, input_pairs, pair, result',
    [
        (
            n_edo12,
            [('A+', 0), ('B', 0), ('E+', 0), ('B+', 1)],
            ('B', 0),
            1
        ),
        (
            n_edo24,
            [('C', 0), ('D+', 0), ('F', 2), ('F-', 2), ('A+', 3)],
            ('F-', 2),
            3
        ),
        (
            n_edo31,
            [('C', 0), ('D+', 0), ('F', 2), ('F-', 2), ('A+', 3)],
            ('A+', 3),
            4
        ),
    ]
)
def test_index(notation, input_pairs, pair, result):
    """
    Test if notes can be found with index and
    no additional restriction parameters
    """

    seq = NoteSeq(
        notation,
        [notation.note(*pair) for pair in input_pairs]
    )

    note = notation.note(*pair)

    assert seq.index(note) == result


@pytest.mark.parametrize(
    'notation, input_pairs, pair',
    [
        (
            n_edo12,
            [('A+', 0), ('B', 0), ('E+', 0), ('B+', 1)],
            ('B++', 0),
        ),
        (
            n_edo24,
            [('C', 0), ('D+', 0), ('F', 2), ('F-', 2), ('A+', 3)],
            ('F-', 3),
        ),
        (
            n_edo31,
            [('C', 0), ('D+', 0), ('F', 2), ('F-', 2), ('A+', 3)],
            ('A-', 3),
        ),
        (
            n_edo31,
            [],
            ('A-', 3),
        ),
    ]
)
def test_index_value_error(notation, input_pairs, pair):
    """
    Test if index raises ValueError if note was not found
    """

    seq = NoteSeq(
        notation,
        [notation.note(*pair) for pair in input_pairs]
    )

    note = notation.note(*pair)

    with pytest.raises(ValueError) as excinfo:
        seq.index(note)
    assert (
        excinfo.value.args[0] ==
        f'{note} is not in sequence'
    )


@pytest.mark.parametrize(
    'notation, input_pairs, pair, start, result',
    [
        (
            n_edo12,
            [('A+', 0), ('B', 0), ('B+', 0), ('B+', 1)],
            ('B+', 0),
            2,
            2
        ),
        (
            n_edo24,
            [('C', 0), ('F-', 0), ('F', 2), ('F-', 2), ('A+', 3)],
            ('F-', 2),
            2,
            3
        ),
        (
            n_edo31,
            [('C', 0), ('D+', 0), ('F', 2), ('F-', 2), ('C', 3)],
            ('C', 3),
            1,
            4
        ),
    ]
)
def test_index_start(notation, input_pairs, pair, start, result):
    """
    Test if notes can be found with index and
    a given start index parameter
    """

    seq = NoteSeq(
        notation,
        [notation.note(*pair) for pair in input_pairs]
    )

    note = notation.note(*pair)

    assert seq.index(note, start) == result


@pytest.mark.parametrize(
    'notation, input_pairs, pair, start',
    [
        (
            n_edo12,
            [('A+', 0), ('B', 0), ('B+', 0), ('B+', 1)],
            ('B', 0),
            2,
        ),
        (
            n_edo24,
            [('C', 0), ('F-', 0), ('F', 2), ('F-', 2), ('A+', 3)],
            ('F', 2),
            3,
        ),
        (
            n_edo31,
            [('C', 0), ('D+', 0), ('F', 2), ('F-', 2), ('C', 3)],
            ('C', 0),
            1,
        ),
    ]
)
def test_index_start_value_error(notation, input_pairs, pair, start):
    """
    Test if index raises ValueError if note was not found
    with given start parameter
    """

    seq = NoteSeq(
        notation,
        [notation.note(*pair) for pair in input_pairs]
    )

    note = notation.note(*pair)

    with pytest.raises(ValueError) as excinfo:
        seq.index(note, start)
    assert (
        excinfo.value.args[0] ==
        f'{note} is not in sequence'
    )


@pytest.mark.parametrize(
    'notation, input_pairs, pair, start, stop, result',
    [
        (
            n_edo12,
            [('A+', 0), ('B', 0), ('B+', 0), ('B+', 1)],
            ('B+', 0),
            1,
            3,
            2
        ),
        (
            n_edo24,
            [('C', 0), ('F-', 0), ('F', 0), ('F-', 2), ('A+', 3)],
            ('F-', 0),
            0,
            3,
            1
        ),
        (
            n_edo31,
            [('C', 0), ('D+', 0), ('F', 2), ('F-', 2), ('C', 3)],
            ('C', 3),
            1,
            5,
            4
        ),
    ]
)
def test_index_start_stop(notation, input_pairs, pair, start, stop, result):
    """
    Test if notes can be found with index and
    a given start index and stop parameter
    """

    seq = NoteSeq(
        notation,
        [notation.note(*pair) for pair in input_pairs]
    )

    note = notation.note(*pair)

    assert seq.index(note, start, stop) == result


@pytest.mark.parametrize(
    'notation, input_pairs, pair, start, stop',
    [
        (
            n_edo12,
            [('A+', 0), ('B', 0), ('B+', 0), ('B+', 1)],
            ('B', 0),
            2,
            3,
        ),
        (
            n_edo24,
            [],
            ('F-', 2),
            2,
            3,
        ),
        (
            n_edo31,
            [('C', 0), ('D+', 0), ('F', 2), ('F-', 2), ('C', 3)],
            ('C', 3),
            1,
            3
        ),
    ]
)
def test_index_start_stop_value_error(
    notation, input_pairs, pair, start, stop
):
    """
    Test if index raises ValueError if note was not found
    with given start and stop parameter
    """

    seq = NoteSeq(
        notation,
        [notation.note(*pair) for pair in input_pairs]
    )

    note = notation.note(*pair)

    with pytest.raises(ValueError) as excinfo:
        seq.index(note, start, stop)
    assert (
        excinfo.value.args[0] ==
        f'{note} is not in sequence'
    )


@pytest.mark.parametrize(
    'notation_a, input_pairs_a, input_pairs_b, result_pairs',
    [
        (
            n_edo12,
            [('E', 0), ('B+', 0), ('D+', 0)],
            [('C', 1), ('B-', -1), ('A', 0)],
            [('E', 0), ('B+', 0), ('D+', 0),
             ('C', 1), ('B-', -1), ('A', 0)],
        ),
        (
            n_edo12,
            [('A', 0), ('B+', 0), ('C', 0)],
            [],
            [('A', 0), ('B+', 0), ('C', 0)],
        ),
        (
            n_edo24,
            [('A', 0), ('B+', 1), ('C', 1)],
            [('B-', 2), ('C+', 1)],
            [('A', 0), ('B+', 1), ('C', 1),
             ('B-', 2), ('C+', 1)],
        ),
    ]
)
def test_concatenation(notation_a,
                       input_pairs_a,
                       input_pairs_b,
                       result_pairs):
    """
    Test if + operator works
    """

    seq_a = NoteSeq(
        notation_a,
        [notation_a.note(*pair) for pair in input_pairs_a]
    )
    seq_b = NoteSeq(
        notation_a,
        [notation_a.note(*pair) for pair in input_pairs_b]
    )

    result_seq = NoteSeq(
        notation_a,
        [notation_a.note(*pair) for pair in result_pairs]
    )

    assert seq_a + seq_b == result_seq


@pytest.mark.parametrize(
    'notation_a, input_pairs, scalar, result_pairs',
    [
        (
            n_edo12,
            [('E', 0), ('B+', 0), ('D+', 0)],
            3,
            [('E', 0), ('B+', 0), ('D+', 0),
             ('E', 0), ('B+', 0), ('D+', 0),
             ('E', 0), ('B+', 0), ('D+', 0)],
        ),
        (
            n_edo12,
            [('A', 0), ('B+', 0), ('C', 0)],
            0,
            [],
        ),
    ]
)
def test_mul(notation_a,
             input_pairs,
             scalar,
             result_pairs):
    """
    Test if * operator works
    """

    seq = NoteSeq(
        notation_a,
        [notation_a.note(*pair) for pair in input_pairs]
    )
    result_seq = NoteSeq(
        notation_a,
        [notation_a.note(*pair) for pair in result_pairs]
    )

    assert scalar * seq == result_seq
    assert seq * scalar == result_seq


@pytest.mark.parametrize(
    'notation_a, input_pairs, result_pairs',
    [
        (
            n_edo12,
            [('E', 0), ('B+', 0), ('D+', 0)],
            [('D+', 0), ('B+', 0), ('E', 0)],
        ),
        (
            n_edo24,
            [('E', 1), ('B+', 2), ('E', 3)],
            [('E', 3), ('B+', 2), ('E', 1)],
        ),
        (
            n_edo12,
            [],
            [],
        ),
    ]
)
def test_retrograde(notation_a,
                    input_pairs,
                    result_pairs):
    """
    Test if retrograde method works
    """

    seq = NoteSeq(
        notation_a,
        [notation_a.note(*pair) for pair in input_pairs]
    )
    result_seq = NoteSeq(
        notation_a,
        [notation_a.note(*pair) for pair in result_pairs]
    )

    assert seq.retrograde() == result_seq


@pytest.mark.parametrize(
    'notation_a, input_pairs, result_pairs',
    [
        (
            n_edo12,
            [('C', 0), ('B+', 0), ('D+', 0)],
            [('C', 0), ('D-', 0), ('B-', 0)],
        ),
        (
            n_edo24,
            [('E', 1), ('B+', 2), ('E', 1)],
            [('E', 1), ('H-', 0), ('E', 1)],
        ),
        (
            n_edo12,
            [],
            [],
        ),
    ]
)
def test_inversion(notation_a,
                   input_pairs,
                   result_pairs):
    """
    Test if inversion method works
    """

    seq = NoteSeq(
        notation_a,
        [notation_a.note(*pair) for pair in input_pairs]
    )
    result_seq = NoteSeq(
        notation_a,
        [notation_a.note(*pair) for pair in result_pairs]
    )

    assert seq.inversion() == result_seq
