import pytest
from xenharmlib.core.frequencies import FrequencyRatio
from xenharmlib.core.tunings import EDOTuning
from xenharmlib.core.tunings import EDTuning
from xenharmlib.core.note_interval_seq import NoteIntervalSeq
from xenharmlib.core.note_interval_seq import NatAccNoteIntervalSeq
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


@pytest.mark.parametrize(
    'notation',
    [
        n_edo12, n_edo24, n_edo31, n_ed13_3
    ]
)
def test_init_empty(notation):
    """
    Test if interval sequence can be created by omitting
    intervals parameter
    """

    interval_seq = NoteIntervalSeq(notation)

    assert len(interval_seq) == 0
    intervals = list(interval_seq)
    assert intervals == []

    interval_seq = notation.interval_seq()

    assert len(interval_seq) == 0
    intervals = list(interval_seq)
    assert intervals == []


def test_init_incompatible_origin_contexts():
    """
    Test if correct exception is raised when interval from
    different origin context is given to constructor
    """
    interval = n_edo24.interval(
        n_edo24.note('A', 1),
        n_edo24.note('B', 1)
    )

    with pytest.raises(IncompatibleOriginContexts):
        NoteIntervalSeq(n_edo12, [interval])

    with pytest.raises(IncompatibleOriginContexts):
        edo12.interval_seq([interval])


@pytest.mark.parametrize(
    'notation, input_shn, interval_shn, result_shn',
    [
        (
            n_edo12,
            [('+C', 2), ('C', 4), ('++F', 5)],
            ('C', 4),
            [('+C', 2), ('C', 4), ('++F', 5), ('C', 4)],
        ),
        (
            n_edo24,
            [('++C', 4), ('--C', 6), ('C', 10)],
            ('++F', 7),
            [('++C', 4), ('--C', 6), ('C', 10), ('++F', 7)],
        ),
    ]
)
def test_with_interval(notation, input_shn, interval_shn, result_shn):
    """
    Test if with_interval works
    """

    interval_seq = NoteIntervalSeq(
        notation,
        [notation.shorthand_interval(*shn) for shn in input_shn]
    )

    interval_seq = interval_seq.with_interval(
        notation.shorthand_interval(*interval_shn)
    )

    assert len(interval_seq) == len(result_shn)
    intervals = list(interval_seq)
    assert intervals == [
        notation.shorthand_interval(*shn) for shn in result_shn
    ]


@pytest.mark.parametrize(
    'notation, input_shn, interval_shn, insert_pos, result_shn',
    [
        (
            n_edo12,
            [('+C', 2), ('C', 2), ('++F', 3)],
            ('C', 10),
            2,
            [('+C', 2), ('C', 2), ('C', 10), ('++F', 3)],
        ),
        (
            n_edo24,
            [('++C', 6), ('--C', 4), ('C', 2)],
            ('++F', 5),
            0,
            [('++F', 5), ('++C', 6), ('--C', 4), ('C', 2)],
        ),
        (
            n_edo31,
            [('++C', 6), ('--C', 4), ('C', 2)],
            ('++F', 21),
            20,
            [('++C', 6), ('--C', 4), ('C', 2), ('++F', 21)],
        ),
    ]
)
def test_with_interval_insert_pos(
    notation,
    input_shn,
    interval_shn,
    insert_pos,
    result_shn
):
    """
    Test if with_interval works with insert_pos parameter
    """

    interval_seq = NoteIntervalSeq(
        notation,
        [notation.shorthand_interval(*shn) for shn in input_shn]
    )

    interval_seq = interval_seq.with_interval(
        notation.shorthand_interval(*interval_shn), insert_pos
    )

    assert len(interval_seq) == len(result_shn)
    intervals = list(interval_seq)
    assert intervals == [
        notation.shorthand_interval(*shn) for shn in result_shn
    ]


def test_with_interval_incompatible_origin_contexts():
    """
    Test if with_interval raises IncompatibleOriginContexts if argument
    originates from a different notation
    """

    notations = n_edo12, n_edo24, n_edo31

    for i, notation_a in enumerate(notations):

        for notation_b in notations[i+1:]:

            interval_seq = NoteIntervalSeq(
                n_ed13_3
            )

            with pytest.raises(IncompatibleOriginContexts):
                interval_seq.with_interval(
                    notation_b.shorthand_interval('C', 2)
                )


def test_eq():
    """
    Test if interval_seq equalities and inequalities work correctly
    """

    interval_seq_a = n_edo12.interval_seq(
        [
            n_edo12.shorthand_interval('+F', 1),
            n_edo12.shorthand_interval('C', 2),
            n_edo12.shorthand_interval('F', 3),
        ]
    )
    interval_seq_b = n_edo12.interval_seq(
        [
            n_edo12.shorthand_interval('+F', 1),
            n_edo12.shorthand_interval('C', 2),
            n_edo12.shorthand_interval('F', 3),
        ]
    )
    interval_seq_c = n_edo12.interval_seq(
        [
            n_edo12.shorthand_interval('+F', 1),
            n_edo12.shorthand_interval('C', 2),
            n_edo12.shorthand_interval('F', 3),
            n_edo12.shorthand_interval('C', 4),
        ]
    )

    interval_seq_d = n_edo31.interval_seq(
        [
            n_edo31.shorthand_interval('+F', 1),
            n_edo31.shorthand_interval('C', 2),
            n_edo31.shorthand_interval('F', 3),
        ]
    )

    interval_seq_e = n_edo24.interval_seq(
        [
            n_edo24.shorthand_interval('C', 2),
            n_edo24.shorthand_interval('F', 3),
            n_edo24.shorthand_interval('--C', 6),
        ]
    )

    assert interval_seq_a == interval_seq_a
    assert interval_seq_a == interval_seq_b
    assert interval_seq_a == interval_seq_e
    assert interval_seq_a != interval_seq_c
    assert interval_seq_a != interval_seq_d
    assert 'XYZ' != interval_seq_a
    assert 3 != interval_seq_a
    assert interval_seq_a != 'XYZ'
    assert interval_seq_a != 3


@pytest.mark.parametrize(
    'notation, input_shn',
    [
        (n_edo12, [('++C', 6), ('--C', 4), ('C', 2)]),
        (n_edo24, [('F', 3), ('+C', 10), ('+C', 6)]),
        (n_edo31, [('C', 4), ('F', 3), ('F', 33)]),
    ]
)
def test_getitem(notation, input_shn):
    """
    Test if fetching single interval items works correctly
    """

    interval_seq = NoteIntervalSeq(
        notation,
        [notation.shorthand_interval(*shn) for shn in input_shn]
    )
    for i, shn in enumerate(input_shn):
        assert interval_seq[i] == notation.shorthand_interval(*shn)


@pytest.mark.parametrize(
    'notation, input_shn, start, stop, result_shn',
    [
        (
            n_edo12,
            [('C', 6), ('+C', 4), ('-F', 3)],
            0,  2,
            [('C', 6), ('+C', 4)],
        ),
        (
            n_edo24,
            [('C', 6), ('+C', 6), ('-F', 7), ('C', 4)],
            1,  3,
            [('+C', 6), ('-F', 7)],
        ),
        (
            n_edo31,
            [('C', 10), ('+C', 6), ('-F', 7), ('C', 4)],
            0,  3,
            [('C', 10), ('+C', 6), ('-F', 7)],
        ),
        (
            n_edo31,
            [('C', 10), ('+C', 6), ('-F', 7), ('C', 4)],
            0,  -1,
            [('C', 10), ('+C', 6), ('-F', 7)],
        ),
        (
            n_edo31,
            [('C', 10), ('+C', 6), ('-F', 7), ('C', 4)],
            -3,  -1,
            [('+C', 6), ('-F', 7)],
        )
    ]
)
def test_getitem_slice(notation, input_shn, start, stop, result_shn):
    """
    Test if slicing of interval_seq works correctly
    """

    interval_seq_a = NoteIntervalSeq(
        notation,
        [notation.shorthand_interval(*shn) for shn in input_shn]
    )

    interval_seq_b = NoteIntervalSeq(
        notation,
        [notation.shorthand_interval(*shn) for shn in result_shn]
    )

    assert interval_seq_a[start:stop] == interval_seq_b


@pytest.mark.parametrize(
    'notation, input_shn, start, result_shn',
    [
        (
            n_edo12,
            [('C', 6), ('+C', 4), ('-F', 3)],
            0,
            [('C', 6), ('+C', 4), ('-F', 3)],
        ),
        (
            n_edo24,
            [('C', 6), ('+C', 6), ('-F', 7), ('C', 4)],
            1,
            [('+C', 6), ('-F', 7), ('C', 4)],
        ),
        (
            n_edo31,
            [('C', 10), ('+C', 6), ('-F', 7), ('C', 4)],
            -2,
            [('-F', 7), ('C', 4)],
        ),
        (
            n_edo31,
            [('C', 10), ('+C', 6), ('-F', 7), ('C', 4)],
            -3,
            [('+C', 6), ('-F', 7), ('C', 4)],
        ),
        (
            n_edo31,
            [('C', 10), ('+C', 6), ('-F', 7), ('C', 4)],
            2,
            [('-F', 7), ('C', 4)],
        )
    ]
)
def test_getitem_slice_omit_stop(notation, input_shn, start, result_shn):
    """
    Test if slicing of interval_seq works correctly when
    stop parameter is omitted
    """

    interval_seq_a = NoteIntervalSeq(
        notation,
        [notation.shorthand_interval(*shn) for shn in input_shn]
    )

    interval_seq_b = NoteIntervalSeq(
        notation,
        [notation.shorthand_interval(*shn) for shn in result_shn]
    )

    assert interval_seq_a[start:] == interval_seq_b


@pytest.mark.parametrize(
    'notation, input_shn, stop, result_shn',
    [
        (
            n_edo12,
            [('C', 6), ('+C', 4), ('-F', 3)],
            0,
            [],
        ),
        (
            n_edo24,
            [('C', 6), ('+C', 6), ('-F', 7), ('C', 4)],
            1,
            [('C', 6)],
        ),
        (
            n_edo31,
            [('C', 10), ('+C', 6), ('-F', 7), ('C', 4), ('C', 4)],
            -2,
            [('C', 10), ('+C', 6), ('-F', 7)],
        ),
        (
            n_edo31,
            [('C', 10), ('+C', 6), ('-F', 7), ('C', 4)],
            -3,
            [('C', 10)],
        ),
        (
            n_edo31,
            [('C', 10), ('+C', 6), ('-F', 7), ('C', 4)],
            2,
            [('C', 10), ('+C', 6)],
        )
    ]
)
def test_getitem_slice_omit_start(notation, input_shn, stop, result_shn):
    """
    Test if slicing of interval_seq works correctly when
    start parameter is omitted
    """

    interval_seq_a = NoteIntervalSeq(
        notation,
        [notation.shorthand_interval(*shn) for shn in input_shn]
    )

    interval_seq_b = NoteIntervalSeq(
        notation,
        [notation.shorthand_interval(*shn) for shn in result_shn]
    )

    assert interval_seq_a[:stop] == interval_seq_b


@pytest.mark.parametrize(
    'notation, input_shn, mask, result_shn',
    [
        (
            n_edo12,
            [('C', 6), ('+C', 4), ('-F', 3)],
            1,
            [('+C', 4)],
        ),
        (
            n_edo24,
            [('C', 6), ('+C', 6), ('-F', 7), ('C', 4)],
            ...,
            [('C', 6), ('+C', 6), ('-F', 7), ('C', 4)],
        ),
        (
            n_edo31,
            [('C', 10), ('+C', 6), ('-F', 7), ('C', 4), ('C', 4)],
            (1,),
            [('+C', 6)],
        ),
        (
            n_edo31,
            [('C', 10), ('+C', 6), ('-F', 7), ('C', 4)],
            (...,),
            [('C', 10), ('+C', 6), ('-F', 7), ('C', 4)],
        ),
        (
            n_edo24,
            [('C', 12), ('+F', 7), ('-F', 9), ('C', 4)],
            (1, 2),
            [('+F', 7), ('-F', 9)],
        ),
        (
            n_edo12,
            [('F', 3), ('+C', 6), ('-F', 9), ('C', 2)],
            (1, ...),
            [('+C', 6), ('-F', 9), ('C', 2)],
        ),
        (
            n_edo12,
            [('++C', 12), ('--F', 7), ('-F', 7), ('C', 10), ('F', 1)],
            (0, 2, 4),
            [('++C', 12), ('-F', 7), ('F', 1)],
        ),
        (
            n_edo24,
            [('C', 12), ('+C', 4), ('-F', 7), ('C', 2), ('F', 3)],
            (..., 2, 4),
            [('C', 12), ('+C', 4), ('-F', 7), ('F', 3)],
        ),
        (
            n_edo31,
            [('+F', 3), ('C', 6), ('-F', 9), ('C', 2), ('F', 3)],
            (0, ..., 2, 4),
            [('+F', 3), ('C', 6), ('-F', 9), ('F', 3)],
        ),
        (
            n_edo31,
            [('C', 10), ('+C', 6), ('-F', 7), ('C', 4), ('C', 2)],
            (0, 2, ..., 4),
            [('C', 10), ('-F', 7), ('C', 4), ('C', 2)],
        ),
        (
            n_edo12,
            [('C', 10), ('+C', 6), ('-F', 7), ('C', 4)],
            (2, ..., 100),
            [('-F', 7), ('C', 4)],
        ),
    ]
)
def test_partial(notation, input_shn, mask, result_shn):
    """
    Test if partial function of interval sequences works correctly
    """

    interval_seq_a = NoteIntervalSeq(
        notation,
        [notation.shorthand_interval(*shn) for shn in input_shn]
    )

    interval_seq_b = NoteIntervalSeq(
        notation,
        [notation.shorthand_interval(*shn) for shn in result_shn]
    )
    assert interval_seq_a.partial(mask) == interval_seq_b


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
    Test if partial function of interval sequences raises correct exception
    when invalid mask is given
    """

    input_shn = [('C', 12), ('+C', 4), ('-F', 7), ('C', 2), ('F', 3)]
    interval_seq = notation.interval_seq(
        [notation.shorthand_interval(*shn) for shn in input_shn]
    )

    with pytest.raises(InvalidIndexMask):
        interval_seq.partial(mask)


@pytest.mark.parametrize(
    'notation, input_shn, mask, result_shn',
    [
        (
            n_edo12,
            [('C', 6), ('+C', 4), ('-F', 3)],
            1,
            [('C', 6), ('-F', 3)],
        ),
        (
            n_edo24,
            [('C', 6), ('+C', 6), ('-F', 7), ('C', 4)],
            ...,
            [],
        ),
        (
            n_edo31,
            [('C', 10), ('+C', 6), ('-F', 7), ('C', 4), ('C', 4)],
            (1,),
            [('C', 10), ('-F', 7), ('C', 4), ('C', 4)],
        ),
        (
            n_edo31,
            [('C', 10), ('+C', 6), ('-F', 7), ('C', 4)],
            (...,),
            [],
        ),
        (
            n_edo24,
            [('C', 12), ('+F', 7), ('-F', 9), ('C', 4)],
            (1, 2),
            [('C', 12), ('C', 4)],
        ),
        (
            n_edo12,
            [('F', 3), ('+C', 6), ('-F', 9), ('C', 2)],
            (1, ...),
            [('F', 3)],
        ),
        (
            n_edo12,
            [('++C', 12), ('--F', 7), ('-F', 7), ('C', 10), ('F', 1)],
            (0, 2, 4),
            [('--F', 7), ('C', 10)],
        ),
        (
            n_edo24,
            [('C', 12), ('+C', 4), ('-F', 7), ('C', 2), ('F', 3)],
            (..., 2, 4),
            [('C', 2)],
        ),
        (
            n_edo31,
            [('+F', 3), ('C', 6), ('-F', 9), ('C', 2), ('F', 3)],
            (0, ..., 2, 4),
            [('C', 2)],
        ),
        (
            n_edo31,
            [('C', 10), ('+C', 6), ('-F', 7), ('C', 4), ('C', 2)],
            (0, 2, ..., 4),
            [('+C', 6)],
        ),
        (
            n_edo12,
            [('C', 10), ('+C', 6), ('-F', 7), ('C', 4)],
            (2, ..., 100),
            [('C', 10), ('+C', 6)],
        ),
    ]
)
def test_partial_not(notation, input_shn, mask, result_shn):
    """
    Test if partial_not function of interval sequences works correctly
    """

    interval_seq_a = NoteIntervalSeq(
        notation,
        [notation.shorthand_interval(*shn) for shn in input_shn]
    )

    interval_seq_b = NoteIntervalSeq(
        notation,
        [notation.shorthand_interval(*shn) for shn in result_shn]
    )
    assert interval_seq_a.partial_not(mask) == interval_seq_b


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
    Test if partial_not function of interval sequences raises
    correct exception when invalid mask is given
    """

    input_shn = [('C', 12), ('+C', 4), ('-F', 7), ('C', 2), ('F', 3)]
    interval_seq = notation.interval_seq(
        [notation.shorthand_interval(*shn) for shn in input_shn]
    )

    with pytest.raises(InvalidIndexMask):
        interval_seq.partial_not(mask)


@pytest.mark.parametrize(
    'notation, input_shn, mask',
    [
        (
            n_edo12,
            [('C', 6), ('+C', 4), ('-F', 3)],
            1,
        ),
        (
            n_edo24,
            [('C', 6), ('+C', 6), ('-F', 7), ('C', 4)],
            ...,
        ),
        (
            n_edo31,
            [('C', 10), ('+C', 6), ('-F', 7), ('C', 4), ('C', 4)],
            (1,),
        ),
        (
            n_edo31,
            [('C', 10), ('+C', 6), ('-F', 7), ('C', 4)],
            (...,),
        ),
        (
            n_edo24,
            [('C', 12), ('+F', 7), ('-F', 9), ('C', 4)],
            (1, 2),
        ),
        (
            n_edo12,
            [('F', 3), ('+C', 6), ('-F', 9), ('C', 2)],
            (1, ...),
        ),
        (
            n_edo12,
            [('++C', 12), ('--F', 7), ('-F', 7), ('C', 10), ('F', 1)],
            (0, 2, 4),
        ),
        (
            n_edo24,
            [('C', 12), ('+C', 4), ('-F', 7), ('C', 2), ('F', 3)],
            (..., 2, 4),
        ),
        (
            n_edo31,
            [('+F', 3), ('C', 6), ('-F', 9), ('C', 2), ('F', 3)],
            (0, ..., 2, 4),
        ),
        (
            n_edo31,
            [('C', 10), ('+C', 6), ('-F', 7), ('C', 4), ('C', 2)],
            (0, 2, ..., 4),
        ),
        (
            n_edo12,
            [('C', 10), ('+C', 6), ('-F', 7), ('C', 4)],
            (2, ..., 100),
        ),
    ]
)
def test_partition(notation, input_shn, mask):
    """
    Test if partition function of interval sequences works correctly
    """

    interval_seq = NoteIntervalSeq(
        notation,
        [notation.shorthand_interval(*shn) for shn in input_shn]
    )

    positive = interval_seq.partial(mask)
    complement = interval_seq.partial_not(mask)

    assert interval_seq.partition(mask) == (positive, complement)


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
    Test if partition function of interval sequences raises
    correct exception when invalid mask is given
    """

    input_shn = [('C', 12), ('+C', 4), ('-F', 7), ('C', 2), ('F', 3)]
    interval_seq = notation.interval_seq(
        [notation.shorthand_interval(*shn) for shn in input_shn]
    )

    with pytest.raises(InvalidIndexMask):
        interval_seq.partition(mask)


@pytest.mark.parametrize(
    'notation, input_shn',
    [
        (
            n_edo12,
            [('C', 6), ('+C', 4), ('-F', 3)],
        ),
        (
            n_edo24,
            [('C', 6), ('+C', 6), ('-F', 7), ('C', 4)],
        ),
        (
            n_edo31,
            [('C', 10), ('+C', 6), ('-F', 7), ('C', 4), ('C', 4)],
        ),
        (
            n_edo31,
            [('C', 10), ('+C', 6), ('-F', 7), ('C', 4)],
        ),
        (
            n_edo24,
            [('C', 12), ('+F', 7), ('-F', 9), ('C', 4)],
        ),
    ]
)
def test_in_operator(notation, input_shn):
    """
    Test if 'in' operator works
    """

    interval_seq = NoteIntervalSeq(
        notation,
        [notation.shorthand_interval(*shn) for shn in input_shn]
    )

    for shn in input_shn:
        assert notation.shorthand_interval(*shn) in interval_seq


@pytest.mark.parametrize(
    'notation, input_shn, excl_shn',
    [
        (
            n_edo12,
            [('C', 6), ('+C', 4), ('-F', 3)],
            [('C', 8), ('+F', 3), ('F', 3)],
        ),
        (
            n_edo24,
            [('C', 6), ('+C', 6), ('-F', 7), ('C', 4)],
            [('+++C', 6), ('--F', 9), ('+F', 7), ('C', 2)],
        ),
        (
            n_edo31,
            [('C', 10), ('+C', 6), ('-F', 7), ('C', 4), ('C', 4)],
            [('C', 6), ('+C', 4), ('-F', 5), ('C', 2), ('C', 8)],
        ),
        (
            n_edo31,
            [('C', 10), ('+C', 6), ('-F', 7), ('C', 4)],
            [('C', 12), ('+C', 4), ('-F', 3), ('F', 3)],
        ),
        (
            n_edo24,
            [('C', 12), ('+F', 7), ('-F', 9), ('C', 4)],
            [('++C', 6), ('--F', 9), ('+F', 77), ('C', 2)],
        ),
    ]
)
def test_not_in_operator_pitch(notation, input_shn, excl_shn):
    """
    Test if 'not in' operator works
    """

    interval_seq = NoteIntervalSeq(
        notation,
        [notation.shorthand_interval(*shn) for shn in input_shn]
    )

    for shn in excl_shn:
        assert notation.shorthand_interval(*shn) not in interval_seq


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

    input_shn = [('C', 12), ('+C', 4), ('-F', 7), ('C', 2), ('F', 3)]
    interval_seq = NoteIntervalSeq(
        notation,
        [notation.shorthand_interval(*shn) for shn in input_shn]
    )

    assert 'XYZ' not in interval_seq
    assert 8 not in interval_seq
    assert False not in interval_seq


@pytest.mark.parametrize(
    'notation, input_shn, repr_str',
    [
        (
            n_edo12,
            [('C', 6), ('+C', 4), ('-F', 3)],
            'NoteIntervalSeq([C6, +C4, -F3], 12-EDO)'
        ),
        (
            n_edo24,
            [('C', 6), ('+C', 6), ('-F', 7), ('C', 4)],
            'NoteIntervalSeq([C6, +C6, -F7, C4], 24-EDO)'
        ),
        (
            n_edo31,
            [('C', 10), ('+C', 6), ('-F', 7), ('C', 4), ('C', 4)],
            'NoteIntervalSeq([C10, +C6, -F7, C4, C4], 31-EDO)'
        ),
        (
            n_edo31,
            [('C', 10), ('+C', 6), ('-F', 7), ('C', 4)],
            'NoteIntervalSeq([C10, +C6, -F7, C4], 31-EDO)'
        ),
        (
            n_edo24,
            [('C', 12), ('+F', 7), ('-F', 9), ('C', 4)],
            'NoteIntervalSeq([C12, +F7, -F9, C4], 24-EDO)'
        ),
    ]
)
def test_repr(notation, input_shn, repr_str):
    """
    Test if repr() returns the right string
    """

    interval_seq = NoteIntervalSeq(
        notation,
        [notation.shorthand_interval(*shn) for shn in input_shn]
    )
    assert repr(interval_seq) == repr_str


@pytest.mark.parametrize(
    'notation',
    [
        n_edo12, n_edo24, n_edo31
    ]
)
def test_frequency_ratios(notation):
    """
    Test if frequency_ratios property works correctly
    """

    input_shn = [('C', 12), ('+C', 4), ('-F', 7)]
    interval_seq = NoteIntervalSeq(
        notation,
        [notation.shorthand_interval(*shn) for shn in input_shn]
    )

    assert interval_seq.frequency_ratios == [
        notation.shorthand_interval('C', 12).frequency_ratio,
        notation.shorthand_interval('+C', 4).frequency_ratio,
        notation.shorthand_interval('-F', 7).frequency_ratio,
    ]


@pytest.mark.parametrize(
    'notation',
    [
        n_edo12, n_edo24, n_edo31
    ]
)
def test_cents(notation):
    """
    Test if cents property works correctly
    """

    input_shn = [('C', 12), ('+C', 4), ('-F', 7)]
    interval_seq = NoteIntervalSeq(
        notation,
        [notation.shorthand_interval(*shn) for shn in input_shn]
    )

    assert interval_seq.cents == [
        notation.shorthand_interval('C', 12).cents,
        notation.shorthand_interval('+C', 4).cents,
        notation.shorthand_interval('-F', 7).cents,
    ]


@pytest.mark.parametrize(
    'notation',
    [
        n_edo12, n_edo24, n_edo31
    ]
)
def test_pitch_diffs(notation):
    """
    Test if pitch_diffs property works correctly
    """

    input_shn = [('C', 12), ('+C', 4), ('-F', 7)]
    interval_seq = NoteIntervalSeq(
        notation,
        [notation.shorthand_interval(*shn) for shn in input_shn]
    )

    assert interval_seq.pitch_diffs == [
        notation.shorthand_interval('C', 12).pitch_diff,
        notation.shorthand_interval('+C', 4).pitch_diff,
        notation.shorthand_interval('-F', 7).pitch_diff,
    ]


@pytest.mark.parametrize(
    'notation, shn_a, shn_b, shn_result',
    [
        (
            n_edo12,
            [('C', 6), ('+C', 4), ('-F', 3)],
            [('C', 8), ('F', 3)],
            [('C', 6), ('+C', 4), ('-F', 3), ('C', 8), ('F', 3)],
        ),
        (
            n_edo24,
            [('C', 6), ('+C', 6), ('-F', 7), ('C', 4)],
            [],
            [('C', 6), ('+C', 6), ('-F', 7), ('C', 4)],
        ),
        (
            n_edo31,
            [],
            [('C', 6), ('+C', 4), ('-F', 5), ('C', 2), ('C', 8)],
            [('C', 6), ('+C', 4), ('-F', 5), ('C', 2), ('C', 8)],
        ),
        (
            n_edo31,
            [('C', 10), ('C', 10)],
            [('F', 7), ('F', 7)],
            [('C', 10), ('C', 10), ('F', 7), ('F', 7)],
        ),
        (
            n_edo24,
            [],
            [],
            [],
        ),
    ]
)
def test_addition(notation, shn_a, shn_b, shn_result):
    """
    Test if interval sequence addition works correctly
    """

    interval_seq_a = NoteIntervalSeq(
        notation,
        [notation.shorthand_interval(*shn) for shn in shn_a]
    )

    interval_seq_b = NoteIntervalSeq(
        notation,
        [notation.shorthand_interval(*shn) for shn in shn_b]
    )

    interval_seq_result = NoteIntervalSeq(
        notation,
        [notation.shorthand_interval(*shn) for shn in shn_result]
    )

    assert interval_seq_a + interval_seq_b == interval_seq_result


@pytest.mark.parametrize(
    'notation, input_shn, scalar, result_shn',
    [
        (
            n_edo12,
            [('C', 8), ('F', 3)],
            3,
            [('C', 8), ('F', 3), ('C', 8), ('F', 3), ('C', 8), ('F', 3)],
        ),
        (
            n_edo24,
            [('C', 6), ('+C', 6), ('-F', 7), ('C', 4)],
            0,
            [],
        ),
        (
            n_edo31,
            [('C', 6), ('+C', 6), ('-F', 7), ('C', 4)],
            1,
            [('C', 6), ('+C', 6), ('-F', 7), ('C', 4)],
        ),
        (
            n_edo31,
            [],
            5,
            [],
        ),
    ]
)
def test_scalar_multiplication(notation, input_shn, scalar, result_shn):
    """
    Test if interval sequence can multiplied with scalars
    """

    interval_seq = NoteIntervalSeq(
        notation,
        [notation.shorthand_interval(*shn) for shn in input_shn]
    )

    interval_seq_result = NoteIntervalSeq(
        notation,
        [notation.shorthand_interval(*shn) for shn in result_shn]
    )

    assert scalar * interval_seq == interval_seq_result
    assert interval_seq * scalar == interval_seq_result


@pytest.mark.parametrize(
    'notation, input_shn, interval, result',
    [
        (
            n_edo12,
            [('C', 8), ('F', 3), ('C', 8), ('F', 3), ('C', 8), ('F', 3)],
            ('F', 3),
            1
        ),
        (
            n_edo24,
            [('C', 6), ('+C', 4), ('-F', 5), ('C', 2), ('C', 8)],
            ('C', 2),
            3
        ),
        (
            n_edo31,
            [('C', 6), ('+C', 6), ('-F', 7), ('F', 3), ('C', 4)],
            ('C', 4),
            4
        ),
    ]
)
def test_index(notation, input_shn, interval, result):
    """
    Test if intervals can be found with index and
    no additional restriction parameters
    """

    interval_seq = NoteIntervalSeq(
        notation,
        [notation.shorthand_interval(*shn) for shn in input_shn]
    )

    interval = notation.shorthand_interval(*interval)

    assert interval_seq.index(interval) == result


@pytest.mark.parametrize(
    'notation, input_shn, interval',
    [
        (
            n_edo12,
            [('C', 8), ('F', 3), ('C', 8), ('F', 3), ('C', 8), ('F', 3)],
            ('F', 5),
        ),
        (
            n_edo24,
            [],
            ('C', 2),
        ),
        (
            n_edo31,
            [('C', 6), ('+C', 6), ('-F', 7), ('F', 3), ('C', 4)],
            ('C', 10),
        ),
    ]
)
def test_index_value_error(notation, input_shn, interval):
    """
    Test if index raises ValueError if interval was not found
    """

    interval_seq = NoteIntervalSeq(
        notation,
        [notation.shorthand_interval(*shn) for shn in input_shn]
    )

    interval = notation.shorthand_interval(*interval)

    with pytest.raises(ValueError) as excinfo:
        interval_seq.index(interval)
    assert (
        excinfo.value.args[0] ==
        f'{interval} is not in sequence'
    )


@pytest.mark.parametrize(
    'notation, input_shn, interval, start, result',
    [
        (
            n_edo12,
            [('C', 8), ('F', 3), ('C', 8), ('F', 3), ('C', 8), ('F', 3)],
            ('F', 3),
            2,
            3
        ),
        (
            n_edo24,
            [('C', 6), ('+C', 4), ('+C', 2), ('C', 2), ('+C', 4)],
            ('+C', 4),
            2,
            4
        ),
    ]
)
def test_index_start(notation, input_shn, interval, start, result):
    """
    Test if intervals can be found with index and
    a given start index parameter
    """

    interval_seq = NoteIntervalSeq(
        notation,
        [notation.shorthand_interval(*shn) for shn in input_shn]
    )

    interval = notation.shorthand_interval(*interval)

    assert interval_seq.index(interval, start) == result


@pytest.mark.parametrize(
    'notation, input_shn, interval, start',
    [
        (
            n_edo12,
            [('C', 8), ('F', 3), ('C', 10), ('F', 7), ('C', 20), ('F', 9)],
            ('F', 3),
            2,
        ),
        (
            n_edo24,
            [('C', 6), ('+C', 4), ('+C', 2), ('C', 2), ('+C', 4)],
            ('+C', 2),
            3,
        ),
    ]
)
def test_index_start_value_error(notation, input_shn, interval, start):
    """
    Test if index raises ValueError if interval was not found
    after a given start value
    """

    interval_seq = NoteIntervalSeq(
        notation,
        [notation.shorthand_interval(*shn) for shn in input_shn]
    )

    interval = notation.shorthand_interval(*interval)

    with pytest.raises(ValueError) as excinfo:
        interval_seq.index(interval, start)
    assert (
        excinfo.value.args[0] ==
        f'{interval} is not in sequence'
    )


@pytest.mark.parametrize(
    'notation, input_shn, interval, start, stop, result',
    [
        (
            n_edo12,
            [('C', 8), ('F', 3), ('C', 10), ('F', 3), ('C', 20), ('F', 9)],
            ('F', 3),
            2,
            4,
            3
        ),
        (
            n_edo24,
            [('C', 6), ('+C', 4), ('+C', 2), ('C', 2), ('+C', 4)],
            ('+C', 2),
            1,
            -1,
            2
        ),
    ]
)
def test_index_start_stop(notation, input_shn, interval, start, stop, result):
    """
    Test if intervals can be found with index and
    a given start index parameter
    """

    interval_seq = NoteIntervalSeq(
        notation,
        [notation.shorthand_interval(*shn) for shn in input_shn]
    )

    interval = notation.shorthand_interval(*interval)

    assert interval_seq.index(interval, start, stop) == result


@pytest.mark.parametrize(
    'notation, input_shn, interval, start, stop',
    [
        (
            n_edo12,
            [('C', 8), ('F', 9), ('C', 10), ('F', 3), ('C', 20), ('F', 9)],
            ('F', 3),
            0,
            2,
        ),
        (
            n_edo24,
            [('C', 6), ('+C', 4), ('+C', 2), ('C', 2), ('+C', 4)],
            ('C', 6),
            1,
            -1,
        ),
    ]
)
def test_index_start_stop_value_error(
    notation,
    input_shn,
    interval,
    start,
    stop
):
    """
    Test if index raises ValueError if interval was not found
    between a given start and end index
    """

    interval_seq = NoteIntervalSeq(
        notation,
        [notation.shorthand_interval(*shn) for shn in input_shn]
    )

    interval = notation.shorthand_interval(*interval)

    with pytest.raises(ValueError) as excinfo:
        interval_seq.index(interval, start, stop)
    assert (
        excinfo.value.args[0] ==
        f'{interval} is not in sequence'
    )


@pytest.mark.parametrize(
    'notation, input_shn, note_pair, scale_pairs',
    [
        (
            n_edo12,
            [('C', 8), ('F', 9), ('C', 10), ('F', 3), ('C', 20), ('F', 9)],
            ('A', 3),
            [
                ('A', 3), ('B', 4), ('D', 5), ('A', 7),
                ('C', 7), ('D', 10), ('F', 11)
            ]
        ),
        (
            n_edo24,
            [('C', 2), ('+C', 2), ('+C', 2), ('C', 2), ('+C', 4)],
            ('C+', 3),
            [
                ('C+', 3), ('D+', 3), ('Ex', 3),
                ('F+x', 3), ('G+x', 3), ('Jxx', 3)
            ]
        ),
    ]
)
def test_to_scale(notation, input_shn, note_pair, scale_pairs):
    """
    Test if pitch interval sequence can be converted into scale
    """

    interval_seq = NoteIntervalSeq(
        notation,
        [notation.shorthand_interval(*shn) for shn in input_shn]
    )
    note = notation.note(*note_pair)

    expected_scale = notation.scale(
        notation.note(*pair) for pair in scale_pairs
    )
    assert interval_seq.to_scale(note) == expected_scale


def test_to_scale_incompatible_origin_context():
    """
    Test if to_scale raises correct error if parameter is
    from different origin context
    """

    input_shn = [('C', 12), ('+C', 4), ('-F', 7), ('C', 2), ('F', 3)]
    interval_seq = n_edo12.interval_seq(
        [n_edo12.shorthand_interval(*shn) for shn in input_shn]
    )
    note = n_edo24.note('A', 1)

    with pytest.raises(IncompatibleOriginContexts):
        interval_seq.to_scale(note)


@pytest.mark.parametrize(
    'notation, input_shn, result_diff',
    [
        (n_edo12, [('++C', 6), ('--C', 4), ('C', 2)], [12, 4, 2]),
        (n_edo24, [('F', 3), ('+C', 10), ('+C', 6)], [4, 19, 11]),
        (n_edo31, [('C', 4), ('F', 3), ('F', 21)], [6, 4, 39]),
    ]
)
def test_pitch_interval_seq(notation, input_shn, result_diff):
    """
    Test if converting to pitch interval sequence works correctly
    """

    interval_seq = NoteIntervalSeq(
        notation,
        [notation.shorthand_interval(*shn) for shn in input_shn]
    )
    expected = notation.tuning.diff_interval_seq(result_diff)
    assert interval_seq.pitch_interval_seq == expected
