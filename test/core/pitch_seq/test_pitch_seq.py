import pytest
from xenharmlib.core.frequencies import FrequencyRatio
from xenharmlib.core.tunings import EDOTuning
from xenharmlib.core.tunings import EDTuning
from xenharmlib.core.pitch_seq import PitchSeq
from xenharmlib.exc import IncompatibleOriginContexts
from xenharmlib.exc import InvalidIndexMask

edo12 = EDOTuning(12)
edo24 = EDOTuning(24)
edo31 = EDOTuning(31)
ed13_3 = EDTuning(13, FrequencyRatio(3))


@pytest.mark.parametrize(
    'tuning',
    [
        edo12, edo24, edo31, ed13_3
    ]
)
def test_init_empty(tuning):
    """
    Test if sequence can be created by omitting element parameter
    """

    sequence = PitchSeq(tuning)

    assert len(sequence) == 0
    pitches = list(sequence)
    assert pitches == []


def test_init_incompatible_origin_contexts():
    """
    Test if init raises IncompatibleOriginContexts if argument
    originates from a different tuning
    """

    edo12_2 = EDTuning(12, FrequencyRatio(2))
    tunings = edo12, edo24, edo31, ed13_3, edo12_2

    for i, tuning_a in enumerate(tunings):

        for tuning_b in tunings[i+1:]:

            with pytest.raises(IncompatibleOriginContexts):
                PitchSeq(
                    tuning_a, [tuning_b.pitch(0)]
                )


@pytest.mark.parametrize(
    'tuning, input_pi, new_pi, result_pi',
    [
        (edo12, [3, 7, 8], 5, [3, 7, 8, 5]),
        (edo24, [22, 4, 1, 9], 20, [22, 4, 1, 9, 20]),
        (edo31, [16, 33, 39], 22, [16, 33, 39, 22]),
        (edo31, [16, 33, 39], 33, [16, 33, 39, 33]),
        (ed13_3, [100, 50, 0], -1, [100, 50, 0, -1]),
    ]
)
def test_with_element(tuning, input_pi, new_pi, result_pi):
    """
    Test if with_element without parameter adds pitches to the end
    """

    sequence = PitchSeq(
        tuning,
        [tuning.pitch(pi) for pi in input_pi]
    )

    sequence = sequence.with_element(
        tuning.pitch(new_pi)
    )

    assert len(sequence) == len(result_pi)
    pitches = list(sequence)
    assert pitches == [tuning.pitch(pi) for pi in result_pi]


def test_with_element_incompatible_origin_contexts():
    """
    Test if with_element raises IncompatibleOriginContexts if argument
    originates from a different tuning
    """

    edo12_2 = EDTuning(12, FrequencyRatio(2))
    tunings = edo12, edo24, edo31, ed13_3, edo12_2

    for i, tuning_a in enumerate(tunings):

        for tuning_b in tunings[i+1:]:

            seq = PitchSeq(
                tuning_a, [tuning_a.pitch(0)]
            )

            with pytest.raises(IncompatibleOriginContexts):
                seq.with_element(tuning_b.pitch(0))


@pytest.mark.parametrize(
    'tuning, input_pi, new_pi, insert_pos, result_pi',
    [
        (edo12, [8, 3, 7], 5, 2, [8, 3, 5, 7]),
        (edo24, [2, 3, 2], 5, 0, [5, 2, 3, 2]),
        (edo24, [2, 3, 2], 5, 10, [2, 3, 2, 5]),
    ]
)
def test_with_element_insert_pos(
    tuning,
    input_pi,
    new_pi,
    insert_pos,
    result_pi
):
    """
    Test if with_element works with insert_pos parameter
    """

    sequence = PitchSeq(
        tuning,
        [tuning.pitch(pi) for pi in input_pi]
    )

    sequence = sequence.with_element(
        tuning.pitch(new_pi), insert_pos
    )

    assert len(sequence) == len(result_pi)
    pitches = list(sequence)
    assert pitches == [tuning.pitch(pi) for pi in result_pi]


def test_eq():
    """
    Test if sequence equalities and inequalities work correctly
    """

    sequence_a = edo12.index_seq([1, 2, 3])
    sequence_b = edo12.index_seq([1, 2, 3])
    sequence_c = edo12.index_seq([1, 2, 3, 4])

    sequence_d = edo31.index_seq([1, 2, 3])
    sequence_e = edo24.index_seq([2, 4, 6])

    assert sequence_a == sequence_a
    assert sequence_a == sequence_b
    assert sequence_a == sequence_e
    assert sequence_a != sequence_c
    assert sequence_a != sequence_d
    assert 'XYZ' != sequence_a
    assert 3 != sequence_a
    assert sequence_a != 'XYZ'
    assert sequence_a != 3


@pytest.mark.parametrize(
    'tuning, input_pi',
    [
        (edo12, [8, 3, 7]),
        (edo24, [22, 4, 1, 9]),
        (edo31, [16, 33, 39]),
        (edo31, [16, 39, 33, 39]),
        (ed13_3, [100, 50, 0]),
    ]
)
def test_getitem(tuning, input_pi):
    """
    Test if fetching single pitch items works correctly
    """

    sequence = PitchSeq(
        tuning,
        [tuning.pitch(pi) for pi in input_pi]
    )
    for i, pitch_index in enumerate(input_pi):
        assert sequence[i] == tuning.pitch(pitch_index)


@pytest.mark.parametrize(
    'tuning, input_pi, start, stop, result_pi',
    [
        (edo12,  [8, 3, 7],         0,  2, [8, 3]),
        (edo24,  [22, 4, 1, 9],     1,  3, [4, 1]),
        (edo31,  [16, 33, 39],      0,  3, [16, 33, 39]),
        (edo31,  [16, 17, 33, 39],  0, -1, [16, 17, 33]),
        (ed13_3, [100, 50, 0],     -3, -1, [100, 50]),
    ]
)
def test_getitem_slice(tuning, input_pi, start, stop, result_pi):
    """
    Test if slicing of sequences works correctly
    """

    sequence = tuning.seq(
        [tuning.pitch(pi) for pi in input_pi]
    )
    sequence_b = tuning.seq(
        [tuning.pitch(pi) for pi in result_pi]
    )
    assert sequence[start:stop] == sequence_b


@pytest.mark.parametrize(
    'tuning, input_pi, start, result_pi',
    [
        (edo12,  [8, 3, 7],         0, [8, 3, 7]),
        (edo24,  [22, 4, 1, 9],     1, [4, 1, 9]),
        (edo31,  [16, 33, 39],     -2, [33, 39]),
        (edo31,  [16, 17, 33, 39], -3, [17, 33, 39]),
        (ed13_3, [100, 50, 0],      2, [0]),
    ]
)
def test_getitem_slice_omit_stop(tuning, input_pi, start, result_pi):
    """
    Test if slicing of sequences works correctly when
    stop parameter is omitted
    """

    sequence = tuning.seq(
        [tuning.pitch(pi) for pi in input_pi]
    )
    sequence_b = tuning.seq(
        [tuning.pitch(pi) for pi in result_pi]
    )
    assert sequence[start:] == sequence_b


@pytest.mark.parametrize(
    'tuning, input_pi, stop, result_pi',
    [
        (edo12,  [8, 3, 7],         2, [8, 3]),
        (edo24,  [22, 4, 1, 9],     1, [22]),
        (edo31,  [16, 33, 39],     -1, [16, 33]),
        (edo31,  [16, 17, 33, 39],  3, [16, 17, 33]),
        (ed13_3, [100, 50, 0],     -2, [100]),
        (ed13_3, [100, 50, 0],     -3, []),
    ]
)
def test_getitem_slice_omit_start(tuning, input_pi, stop, result_pi):
    """
    Test if slicing of sequences works correctly when
    start parameter is omitted
    """

    sequence = tuning.seq(
        [tuning.pitch(pi) for pi in input_pi]
    )
    sequence_b = tuning.seq(
        [tuning.pitch(pi) for pi in result_pi]
    )
    assert sequence[:stop] == sequence_b


@pytest.mark.parametrize(
    'tuning, input_pi, mask, result_pi',
    [
        (edo12,  [3, 7, 8],             1,              [7]),
        (edo31,  [16, 33, 39],          ...,            [16, 33, 39]),
        (edo12,  [3, 7, 8],             (1,),           [7]),
        (edo31,  [16, 33, 39],          (...,),         [16, 33, 39]),
        (edo12,  [3, 7, 8],             (1, 2),         [7, 8]),
        (edo24,  [1, 4, 9, 22],         (1, ...),       [4, 9, 22]),
        (edo31,  [16, 17, 33, 39, 50],  (0, 2, 4),      [16, 33, 50]),
        (edo31,  [16, 17, 33, 39, 50],  (..., 2, 4),    [16, 17, 33, 50]),
        (edo31,  [16, 17, 33, 39, 50],  (0, ..., 2, 4), [16, 17, 33, 50]),
        (edo31,  [16, 17, 33, 39, 50],  (0, 2, ..., 4), [16, 33, 39, 50]),
        (edo31,  [16, 17, 33, 39, 50],  (2, ..., 100),  [33, 39, 50]),
    ]
)
def test_partial(tuning, input_pi, mask, result_pi):
    """
    Test if partial function of sequences works correctly
    """

    sequence = tuning.seq(
        [tuning.pitch(pi) for pi in input_pi]
    )
    sequence_b = tuning.seq(
        [tuning.pitch(pi) for pi in result_pi]
    )
    assert sequence.partial(mask) == sequence_b


@pytest.mark.parametrize(
    'tuning, mask',
    [
        (edo31,  (-1, ..., 2, 4)),
        (edo31,  (..., 4, 3)),
        (edo31,  (..., 4, 3, ...)),
        (edo31,  (3, 2, ...)),
        (edo31,  (1, 2, -1)),
    ]
)
def test_partial_invalid_mask(tuning, mask):
    """
    Test if partial function of sequences raises correct exception
    when invalid mask is given
    """

    sequence = tuning.index_seq([2, 23, 14, 5, 1, 7])

    with pytest.raises(InvalidIndexMask):
        sequence.partial(mask)


@pytest.mark.parametrize(
    'tuning, input_pi, mask, result_pi',
    [
        (edo12,  [3, 7, 8],             1,              [3, 8]),
        (edo31,  [16, 33, 39],          ...,            []),
        (edo12,  [3, 7, 8],             (1,),           [3, 8]),
        (edo31,  [16, 33, 39],          (...,),         []),
        (edo12,  [3, 7, 8],             (1, 2),         [3]),
        (edo24,  [1, 4, 9, 22],         (1, ...),       [1]),
        (edo31,  [16, 17, 33, 39, 50],  (0, 2, 4),      [17, 39]),
        (edo31,  [16, 17, 33, 39, 50],  (..., 2, 4),    [39]),
        (edo31,  [16, 17, 33, 39, 50],  (0, ..., 2, 4), [39]),
        (edo31,  [16, 17, 33, 39, 50],  (0, 2, ..., 4), [17]),
        (edo31,  [16, 17, 33, 39, 50],  (2, ..., 100),  [16, 17]),
    ]
)
def test_partial_not(tuning, input_pi, mask, result_pi):
    """
    Test if partial_not function of sequences works correctly
    """

    sequence = tuning.seq(
        [tuning.pitch(pi) for pi in input_pi]
    )
    sequence_b = tuning.seq(
        [tuning.pitch(pi) for pi in result_pi]
    )
    assert sequence.partial_not(mask) == sequence_b


@pytest.mark.parametrize(
    'tuning, mask',
    [
        (edo31,  (-1, ..., 2, 4)),
        (edo31,  (..., 4, 3)),
        (edo31,  (..., 4, 3, ...)),
        (edo31,  (3, 2, ...)),
        (edo31,  (1, 2, -1)),
    ]
)
def test_partial_not_invalid_mask(tuning, mask):
    """
    Test if partial_not function of sequences raises correct exception
    when invalid mask is given
    """

    sequence = tuning.index_seq([2, 23, 14, 5, 1, 7])

    with pytest.raises(InvalidIndexMask):
        sequence.partial_not(mask)


@pytest.mark.parametrize(
    'tuning, input_pi, mask',
    [
        (edo12,  [3, 7, 8],             1),
        (edo31,  [16, 33, 39],          ...),
        (edo12,  [3, 7, 8],             (1,)),
        (edo31,  [16, 33, 39],          (...,)),
        (edo12,  [3, 7, 8],             (1, 2)),
        (edo24,  [1, 4, 9, 22],         (1, ...)),
        (edo31,  [16, 17, 33, 39, 50],  (0, 2, 4)),
        (edo31,  [16, 17, 33, 39, 50],  (..., 2, 4)),
        (edo31,  [16, 17, 33, 39, 50],  (0, ..., 2, 4)),
        (edo31,  [16, 17, 33, 39, 50],  (0, 2, ..., 4)),
        (edo31,  [16, 17, 33, 39, 50],  (2, ..., 100)),
    ]
)
def test_partition(tuning, input_pi, mask):
    """
    Test if partition function of sequences works correctly
    """

    sequence = tuning.seq(
        [tuning.pitch(pi) for pi in input_pi]
    )

    positive = sequence.partial(mask)
    complement = sequence.partial_not(mask)

    assert sequence.partition(mask) == (positive, complement)


@pytest.mark.parametrize(
    'tuning, mask',
    [
        (edo31,  (-1, ..., 2, 4)),
        (edo31,  (..., 4, 3)),
        (edo31,  (..., 4, 3, ...)),
        (edo31,  (3, 2, ...)),
        (edo31,  (1, 2, -1)),
    ]
)
def test_partition_invalid_mask(tuning, mask):
    """
    Test if partition function of sequences raises correct exception
    when invalid mask is given
    """

    sequence = tuning.index_seq([2, 23, 14, 5, 1, 7])

    with pytest.raises(InvalidIndexMask):
        sequence.partition(mask)


@pytest.mark.parametrize(
    'tuning, input_pi',
    [
        (edo12, [8, 3, 7]),
        (edo24, [22, 4, 1, 9]),
        (edo31, [16, 33, 39]),
        (edo31, [16, 39, 33, 39]),
        (ed13_3, [100, 50, 0]),
    ]
)
def test_in_operator_pitch(tuning, input_pi):
    """
    Test if 'in' operator works on single pitches
    """

    sequence = PitchSeq(
        tuning,
        [tuning.pitch(pi) for pi in input_pi]
    )

    for pitch_index in input_pi:
        assert tuning.pitch(pitch_index) in sequence


@pytest.mark.parametrize(
    'tuning, input_pi, excl_pi',
    [
        (edo12, [8, 3, 7], [0, 1, 4, 9, 10, 31]),
        (edo24, [22, 4, 1, 9], [21, 23, 0, 5, 10]),
        (edo31, [16, 33, 39], [19, 3, 5]),
        (edo31, [16, 39, 33, 39], [13, 2, 44, 74]),
        (ed13_3, [100, 50, 0], [9, 444, 3]),
    ]
)
def test_not_in_operator_pitch(tuning, input_pi, excl_pi):
    """
    Test if 'not in' operator works on single pitches
    """

    sequence = PitchSeq(
        tuning,
        [tuning.pitch(pi) for pi in input_pi]
    )

    for pitch_index in excl_pi:
        assert tuning.pitch(pitch_index) not in sequence


@pytest.mark.parametrize(
    'tuning, input_pi, interval_pi',
    [
        (edo12, [8, 3, 7], [(0, 4), (0, 1), (0, 0)]),
        (edo31, [4, 8, 10, 22, 13], [(4, 16), (8, 12), (0, 9)]),
        (ed13_3, [0, 8, 15, 9, 66], [(1, 67), (8, 15), (7, 65)]),
        (ed13_3, [0, 8, 15, 9, 66], [(67, 1), (15, 8), (65, 7)]),
    ]
)
def test_in_operator_interval(tuning, input_pi, interval_pi):
    """
    Test if 'in' operator works on intervals
    """

    sequence = PitchSeq(
        tuning,
        [tuning.pitch(pi) for pi in input_pi]
    )

    for pi_a, pi_b in interval_pi:
        interval = tuning.pitch(pi_a).interval(
            tuning.pitch(pi_b)
        )
        assert interval in sequence


@pytest.mark.parametrize(
    'tuning, input_pi, excl_interval_pi',
    [
        (edo12, [8, 3, 7], [(0, 7), (1, 3)]),
        (edo31, [4, 8, 10, 22, 13], [(4, 19), (0, 10), (0, 1)]),
        (ed13_3, [0, 8, 15, 9, 66], [(1, 63), (3, 15), (22, 65)]),
    ]
)
def test_not_in_operator_interval(tuning, input_pi, excl_interval_pi):
    """
    Test if 'not in' operator works on intervals
    """

    sequence = PitchSeq(
        tuning,
        [tuning.pitch(pi) for pi in input_pi]
    )

    for pi_a, pi_b in excl_interval_pi:
        interval = tuning.pitch(pi_a).interval(
            tuning.pitch(pi_b)
        )
        assert interval not in sequence


@pytest.mark.parametrize(
    'tuning',
    [
        edo12, edo31, ed13_3
    ]
)
def test_in_operator_bogus(tuning):
    """
    Test if 'in' operator returns False on non-supported types
    """

    sequence = PitchSeq(
        tuning,
        [
            tuning.pitch(8),
            tuning.pitch(3),
            tuning.pitch(7),
        ]
    )

    assert 'XYZ' not in sequence
    assert 8 not in sequence
    assert False not in sequence


@pytest.mark.parametrize(
    'tuning, input_pi, repr_str',
    [
        (edo12, [8, 3, 7], 'PitchSeq([8, 3, 7], 12-EDO)'),
        (edo24, [1, 33, 3, 7], 'PitchSeq([1, 33, 3, 7], 24-EDO)'),
        (edo31, [4, 8, 10, 22, 13], 'PitchSeq([4, 8, 10, 22, 13], 31-EDO)'),
        (ed13_3, [0, 8, 15, 9, 66], 'PitchSeq([0, 8, 15, 9, 66], 13ed3)'),
    ]
)
def test_repr(tuning, input_pi, repr_str):
    """
    Test if repr() returns the right string for sequence
    """

    sequence = PitchSeq(
        tuning,
        [tuning.pitch(pi) for pi in input_pi]
    )
    assert repr(sequence) == repr_str


@pytest.mark.parametrize(
    'tuning',
    [
        edo12, edo24, edo31, ed13_3
    ]
)
def test_frequencies(tuning):
    """
    Test if frequencies property works correctly
    """

    sequence = PitchSeq(
        tuning,
        [
            tuning.pitch(8),
            tuning.pitch(3),
            tuning.pitch(7),
        ]
    )

    assert sequence.frequencies == [
        tuning.pitch(8).frequency,
        tuning.pitch(3).frequency,
        tuning.pitch(7).frequency,
    ]


@pytest.mark.parametrize(
    'tuning, input_pi, result_pi',
    [
        (edo12, [8, 3, 7], [8, 3, 7]),
        (edo12, [8, 3, 7, 3], [8, 3, 7, 3]),
        (edo24, [22, 4, 1, 9], [22, 4, 1, 9]),
        (edo31, [16, 33, 39], [16, 33, 39]),
        (ed13_3, [100, 50, 0], [100, 50, 0]),
    ]
)
def test_pitch_indices(tuning, input_pi, result_pi):
    """
    Test if pitch_indices property works correctly
    """

    sequence = PitchSeq(
        tuning,
        [tuning.pitch(pi) for pi in input_pi]
    )

    assert sequence.pitch_indices == result_pi


@pytest.mark.parametrize(
    'tuning, input_pi, interval_diffs',
    [
        (edo12, [8, 3, 7], [-5, 4]),
        (edo31, [4, 8, 10, 22, 13], [4, 2, 12, -9]),
        (ed13_3, [0, 8, 15, 9, 66], [8, 7, -6, 57]),
    ]
)
def test_to_interval_seq(tuning, input_pi, interval_diffs):
    """
    Test if to_interval_seq method works correctly
    """

    sequence = PitchSeq(
        tuning,
        [tuning.pitch(pi) for pi in input_pi]
    )

    intervals = [
        tuning.diff_interval(diff) for diff in interval_diffs
    ]
    expected_seq = tuning.interval_seq(intervals)

    assert sequence.to_interval_seq() == expected_seq


@pytest.mark.parametrize(
    'tuning, input_pi, diff, result_pi',
    [
        (edo12, [3, 7, 8], 2, [5, 9, 10]),
        (edo24, [2, 9, 14, 44], -10, [-8, -1, 4, 34]),
        (edo31, [-4, -3, 9], 3, [-1, 0, 12]),
        (ed13_3, [1, 2, 3, 4], 3, [4, 5, 6, 7]),
    ]
)
def test_transpose_int(tuning, input_pi, diff, result_pi):
    """
    Test if transpose method works correctly when given an integer
    """

    sequence = PitchSeq(
        tuning,
        [tuning.pitch(pi) for pi in input_pi]
    )

    transposed = sequence.transpose(diff)
    assert transposed == tuning.seq(
        [tuning.pitch(pi) for pi in result_pi]
    )


@pytest.mark.parametrize(
    'tuning, input_pi, interval_pi, result_pi',
    [
        (edo12, [3, 7, 8], (0, 2), [5, 9, 10]),
        (edo24, [2, 9, 14, 44], (1, -9), [-8, -1, 4, 34]),
        (edo31, [-4, -3, 9], (6, 9), [-1, 0, 12]),
        (ed13_3, [1, 2, 3, 4], (31, 34), [4, 5, 6, 7]),
    ]
)
def test_transpose_interval(tuning, input_pi, interval_pi, result_pi):
    """
    Test if transpose method works correctly when given an interval
    """

    sequence = PitchSeq(
        tuning,
        [tuning.pitch(pi) for pi in input_pi]
    )

    pi_a, pi_b = interval_pi
    interval = tuning.pitch(pi_a).interval(
        tuning.pitch(pi_b)
    )

    transposed = sequence.transpose(interval)
    assert transposed == tuning.seq(
        [tuning.pitch(pi) for pi in result_pi]
    )


@pytest.mark.parametrize(
    'tuning_a, input_pi, tuning_b, result_pi',
    [
        (edo12, [0, 3, 7, 8, 10], edo31, [0, 8, 18, 21, 26]),
        (edo12, [1, 4, 6, 7, 8, 11], edo24, [2, 8, 12, 14, 16, 22]),
        (edo24, [2, 8, 12, 14, 16, 22], edo12, [1, 4, 6, 7, 8, 11]),
        (edo24, [1, 8, 12, 14, 16, 22], edo12, [0, 4, 6, 7, 8, 11]),
    ]
)
def test_retune(tuning_a, input_pi, tuning_b, result_pi):
    """
    Test if retune method works correctly
    """

    sequence_a = tuning_a.seq(
        [tuning_a.pitch(pi) for pi in input_pi]
    )

    sequence_b = sequence_a.retune(tuning_b)
    expected_sequence_b = tuning_b.seq(
        [tuning_b.pitch(pi) for pi in result_pi]
    )
    assert sequence_b == expected_sequence_b


@pytest.mark.parametrize(
    'tuning, input_pi_a, input_pi_b, expected',
    [
        (edo12, [7, 8], [5, 7, 8], True),
        (edo24, [1, 11, 12], [1, 11, 12], True),
        (edo31, [9, 3, 12], [1, 9, 12], False),
        (ed13_3, [3, 11, 20], [], False),
        (ed13_3, [], [3, 11, 20], True),
    ]
)
def test_is_subseq(tuning, input_pi_a, input_pi_b, expected):
    """
    Test if is_subseq test works correctly
    """

    sequence_a = PitchSeq(
        tuning,
        [tuning.pitch(pi) for pi in input_pi_a]
    )

    sequence_b = PitchSeq(
        tuning,
        [tuning.pitch(pi) for pi in input_pi_b]
    )

    assert sequence_a.is_subseq(sequence_b) == expected


@pytest.mark.parametrize(
    'tuning, input_pi_a, input_pi_b, expected',
    [
        (edo12, [7, 8], [5, 7, 8], True),
        (edo24, [1, 11, 12], [1, 11, 12], False),
        (edo31, [9, 3, 12], [1, 9, 12], False),
        (ed13_3, [3, 11, 20], [], False),
        (ed13_3, [], [3, 11, 20], True),
    ]
)
def test_is_subseq_proper(tuning, input_pi_a, input_pi_b, expected):
    """
    Test if is_subseq test works correctly with proper=True
    """

    sequence_a = PitchSeq(
        tuning,
        [tuning.pitch(pi) for pi in input_pi_a]
    )

    sequence_b = PitchSeq(
        tuning,
        [tuning.pitch(pi) for pi in input_pi_b]
    )

    assert sequence_a.is_subseq(sequence_b, proper=True) == expected


def test_is_subseq_incompatible_origin_contexts():
    """
    Test if is_subseq test fails if sequences originate
    from different tunings
    """

    edo12_2 = EDTuning(12, FrequencyRatio(2))
    tunings = edo12, edo24, edo31, ed13_3, edo12_2

    for i, tuning_a in enumerate(tunings):

        for tuning_b in tunings[i+1:]:

            sequence_a = PitchSeq(
                tuning_a
            )
            sequence_b = PitchSeq(
                tuning_b
            )

            with pytest.raises(IncompatibleOriginContexts):
                sequence_a.is_subseq(sequence_b)

            with pytest.raises(IncompatibleOriginContexts):
                sequence_a.is_subseq(sequence_b, proper=True)


@pytest.mark.parametrize(
    'tuning, input_pi_a, input_pi_b, expected',
    [
        (edo12, [5, 7, 8], [7, 8], True),
        (edo24, [1, 11, 12], [1, 11, 12], True),
        (edo31, [3, 11, 64], [1, 9, 12], False),
        (ed13_3, [3, 11, 20], [], True),
        (ed13_3, [], [3, 11, 20], False),
    ]
)
def test_is_superseq(tuning, input_pi_a, input_pi_b, expected):
    """
    Test if is_superseq test works correctly
    """

    sequence_a = PitchSeq(
        tuning,
        [tuning.pitch(pi) for pi in input_pi_a]
    )

    sequence_b = PitchSeq(
        tuning,
        [tuning.pitch(pi) for pi in input_pi_b]
    )

    assert sequence_a.is_superseq(sequence_b) == expected


@pytest.mark.parametrize(
    'tuning, input_pi_a, input_pi_b, expected',
    [
        (edo12, [5, 8, 7], [8, 7], True),
        (edo24, [1, 11, 12], [1, 11, 12], False),
        (edo31, [3, 11, 64], [1, 9, 12], False),
        (ed13_3, [3, 11, 20], [], True),
        (ed13_3, [], [3, 11, 20], False),
    ]
)
def test_is_superseq_proper(tuning, input_pi_a, input_pi_b, expected):
    """
    Test if is_superseq test works correctly
    with proper=True
    """

    sequence_a = PitchSeq(
        tuning,
        [tuning.pitch(pi) for pi in input_pi_a]
    )

    sequence_b = PitchSeq(
        tuning,
        [tuning.pitch(pi) for pi in input_pi_b]
    )

    assert sequence_a.is_superseq(sequence_b, proper=True) == expected


def test_is_superseq_incompatible_origin_contexts():
    """
    Test if is_subseq test fails if sequences originate
    from different tunings
    """

    edo12_2 = EDTuning(12, FrequencyRatio(2))
    tunings = edo12, edo24, edo31, ed13_3, edo12_2

    for i, tuning_a in enumerate(tunings):

        for tuning_b in tunings[i+1:]:

            sequence_a = PitchSeq(
                tuning_a
            )
            sequence_b = PitchSeq(
                tuning_b
            )

            with pytest.raises(IncompatibleOriginContexts):
                sequence_a.is_superseq(sequence_b)

            with pytest.raises(IncompatibleOriginContexts):
                sequence_a.is_superseq(sequence_b, proper=True)


@pytest.mark.parametrize(
    'tuning, input_pi, result_pi',
    [
        (edo12, [3, 5, 7, 8, 10], [0, 2, 4, 5, 7]),
        (edo12, [5, 7, 8, 15, 19], [0, 2, 3, 10, 14]),
        (edo31, [10, 19, 23, 36, 37], [0, 9, 13, 26, 27]),
        (edo31, [0, 12, 16, 19, 22, 34, 36], [0, 12, 16, 19, 22, 34, 36]),
    ]
)
def test_zero_normalized(tuning, input_pi, result_pi):
    """
    Test if zero_normalized works correctly
    """

    input_seq = tuning.index_seq(input_pi)
    result_seq = tuning.index_seq(result_pi)
    assert input_seq.zero_normalized() == result_seq


def test_zero_normalized_value_error():
    """
    Test if zero_normalized raises ValueError if sequence is empty
    """

    input_seq = edo12.seq()
    with pytest.raises(ValueError) as excinfo:
        input_seq.zero_normalized()
    assert (
        excinfo.value.args[0] ==
        'zero_normalized is not defined on empty sequence'
    )


@pytest.mark.parametrize(
    'tuning, input_pi, expected',
    [
        (edo12, [3, 5, 7, 8, 10], False),
        (edo12, [5, 7, 8, 15, 19], False),
        (edo31, [10, 19, 23, 36, 37], False),
        (edo31, [0, 12, 16, 19, 22, 34, 36], True),
        (edo31, [0, 9, 12, 14, 17], True),
    ]
)
def test_is_zero_normalized(tuning, input_pi, expected):
    """
    Test if is_zero_normalized works correctly
    """

    input_sequence = tuning.index_seq(input_pi)
    assert input_sequence.is_zero_normalized == expected


def test_is_zero_normalized_value_error():
    """
    Test if is_zero_normalized raises ValueError if sequence is empty
    """

    input_sequence = edo12.seq()
    with pytest.raises(ValueError) as excinfo:
        input_sequence.is_zero_normalized
    assert (
        excinfo.value.args[0] ==
        'is_zero_normalized is not defined on empty sequence'
    )


@pytest.mark.parametrize(
    'tuning, input_pi, search_pi, position',
    [
        (edo12, [8, 3, 7, 3], 3, 1),
        (edo24, [22, 4, 1, 9], 9, 3),
        (edo31, [16, 33, 39], 16, 0),
    ]
)
def test_index(tuning, input_pi, search_pi, position):
    """
    Test if index method works correctly without additional parameters
    """

    sequence = PitchSeq(
        tuning,
        [tuning.pitch(pi) for pi in input_pi]
    )

    pitch = tuning.pitch(search_pi)
    assert sequence.index(pitch) == position


@pytest.mark.parametrize(
    'tuning, input_pi, search_pi',
    [
        (edo12, [8, 3, 7, 3], 11),
        (edo24, [22, 4, 1, 9], 19),
        (edo31, [], 16),
    ]
)
def test_index_value_error(tuning, input_pi, search_pi):
    """
    Test if index method works correctly without additional parameters
    when pitch was not found
    """

    sequence = PitchSeq(
        tuning,
        [tuning.pitch(pi) for pi in input_pi]
    )

    pitch = tuning.pitch(search_pi)

    with pytest.raises(ValueError) as excinfo:
        sequence.index(pitch)
    assert (
        excinfo.value.args[0] ==
        f'{pitch} is not in sequence'
    )


@pytest.mark.parametrize(
    'tuning, input_pi, search_pi, start, position',
    [
        (edo12, [8, 3, 7, 3], 3, 1, 1),
        (edo12, [8, 3, 7, 3], 3, 2, 3),
        (edo24, [22, 4, 1, 9], 9, 0, 3),
    ]
)
def test_index_start(tuning, input_pi, search_pi, start, position):
    """
    Test if index method works correctly with start parameter
    """

    sequence = PitchSeq(
        tuning,
        [tuning.pitch(pi) for pi in input_pi]
    )

    pitch = tuning.pitch(search_pi)
    assert sequence.index(pitch, start) == position


@pytest.mark.parametrize(
    'tuning, input_pi, search_pi, start',
    [
        (edo12, [8, 3, 7, 3], 11, 0),
        (edo24, [22, 4, 1, 9], 19, 3),
        (edo24, [22, 4, 1, 9], 4, 2),
        (edo31, [], 16, 3),
    ]
)
def test_index_value_error_start(tuning, input_pi, search_pi, start):
    """
    Test if index method works correctly with start parameters
    when pitch was not found
    """

    sequence = PitchSeq(
        tuning,
        [tuning.pitch(pi) for pi in input_pi]
    )

    pitch = tuning.pitch(search_pi)

    with pytest.raises(ValueError) as excinfo:
        sequence.index(pitch, start)
    assert (
        excinfo.value.args[0] ==
        f'{pitch} is not in sequence'
    )


@pytest.mark.parametrize(
    'tuning, input_pi, search_pi, start, stop, position',
    [
        (edo12, [8, 3, 7, 3], 3, 1, 2, 1),
        (edo12, [8, 3, 7, 3], 3, 2, 5, 3),
        (edo24, [22, 4, 1, 9], 9, 0, 4, 3),
    ]
)
def test_index_start_stop(tuning, input_pi, search_pi, start, stop, position):
    """
    Test if index method works correctly with start and stop parameter
    """

    sequence = PitchSeq(
        tuning,
        [tuning.pitch(pi) for pi in input_pi]
    )

    pitch = tuning.pitch(search_pi)
    assert sequence.index(pitch, start, stop) == position


@pytest.mark.parametrize(
    'tuning, input_pi, search_pi, start, stop',
    [
        (edo12, [8, 3, 7, 3, 8], 8, 1, 2),
        (edo12, [8, 3, 7, 3], 3, 4, 5),
        (edo24, [22, 4, 1, 9, 3, 4, 9], 9, 4, 6),
    ]
)
def test_index_value_error_start_stop(
    tuning, input_pi, search_pi, start, stop
):
    """
    Test if index method works correctly with start and stop parameters
    when pitch was not found
    """

    sequence = PitchSeq(
        tuning,
        [tuning.pitch(pi) for pi in input_pi]
    )

    pitch = tuning.pitch(search_pi)

    with pytest.raises(ValueError) as excinfo:
        sequence.index(pitch, start, stop)
    assert (
        excinfo.value.args[0] ==
        f'{pitch} is not in sequence'
    )


@pytest.mark.parametrize(
    'tuning, input_pi_a, input_pi_b, result_pi',
    [
        (edo12, [8, 3, 7, 3], [4, 5], [8, 3, 7, 3, 4, 5]),
        (edo24, [22, 4, 1, 9], [], [22, 4, 1, 9]),
        (edo31, [], [16, 17], [16, 17]),
    ]
)
def test_concatenation(tuning, input_pi_a, input_pi_b, result_pi):
    """
    Test if concatenation works properly
    """

    sequence_a = PitchSeq(
        tuning,
        [tuning.pitch(pi) for pi in input_pi_a]
    )

    sequence_b = PitchSeq(
        tuning,
        [tuning.pitch(pi) for pi in input_pi_b]
    )

    result = PitchSeq(
        tuning,
        [tuning.pitch(pi) for pi in result_pi]
    )

    assert sequence_a + sequence_b == result


@pytest.mark.parametrize(
    'tuning, input_pi, scalar, result_pi',
    [
        (edo12, [8, 3, 7, 3], 2, [8, 3, 7, 3, 8, 3, 7, 3]),
        (edo24, [22, 4, 1, 9], 0, []),
        (edo24, [22, 4, 1, 9], -2, []),
        (edo12, [8, 3, 7, 3], 3, [8, 3, 7, 3, 8, 3, 7, 3, 8, 3, 7, 3]),
        (edo12, [8, 3, 7, 3], 1, [8, 3, 7, 3]),
    ]
)
def test_mul(tuning, input_pi, scalar, result_pi):
    """
    Test if * operator works properly
    """

    sequence = PitchSeq(
        tuning,
        [tuning.pitch(pi) for pi in input_pi]
    )

    result = PitchSeq(
        tuning,
        [tuning.pitch(pi) for pi in result_pi]
    )

    assert scalar * sequence == result
    assert sequence * scalar == result


@pytest.mark.parametrize(
    'tuning, input_pi, result_pi',
    [
        (edo24, [22, 4, 1, 9], [9, 1, 4, 22]),
        (edo24, [2, 6, 6, 2], [2, 6, 6, 2]),
        (edo24, [], []),
    ]
)
def test_retrograde(tuning, input_pi, result_pi):
    """
    Test if retrograde method works properly
    """

    sequence = PitchSeq(
        tuning,
        [tuning.pitch(pi) for pi in input_pi]
    )

    result = PitchSeq(
        tuning,
        [tuning.pitch(pi) for pi in result_pi]
    )

    assert sequence.retrograde() == result


@pytest.mark.parametrize(
    'tuning, input_pi, result_pi',
    [
        (edo24, [8, 4, 1, 9], [8, 12, 15, 7]),
        (edo24, [2, 6, 6, 2], [2, -2, -2, 2]),
        (edo24, [], []),
    ]
)
def test_inversion(tuning, input_pi, result_pi):
    """
    Test if inversion method works properly
    """

    sequence = PitchSeq(
        tuning,
        [tuning.pitch(pi) for pi in input_pi]
    )

    result = PitchSeq(
        tuning,
        [tuning.pitch(pi) for pi in result_pi]
    )

    assert sequence.inversion() == result
