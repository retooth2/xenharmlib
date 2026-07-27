import pytest
from xenharmlib.core.frequencies import FrequencyRatio
from xenharmlib.core.tunings import EDOTuning
from xenharmlib.core.tunings import EDTuning
from xenharmlib.core.pitch_interval_fan import PitchIntervalFan
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
    Test if interval fan can be created by omitting intervals parameter
    """

    interval_fan = PitchIntervalFan(tuning)

    assert len(interval_fan) == 0
    intervals = list(interval_fan)
    assert intervals == []

    interval_fan = tuning.interval_fan()

    assert len(interval_fan) == 0
    intervals = list(interval_fan)
    assert intervals == []


def test_init_incompatible_origin_contexts():
    """
    Test if correct exception is raised when interval from
    different origin context is given to constructor
    """

    with pytest.raises(IncompatibleOriginContexts):
        PitchIntervalFan(edo12, [edo24.diff_interval(3)])

    with pytest.raises(IncompatibleOriginContexts):
        edo12.interval_fan([edo24.diff_interval(3)])


@pytest.mark.parametrize(
    'tuning, input_diffs, new_diff, result_diffs',
    [
        (edo12, [8, 3, 7], 5, [8, 3, 7, 5]),
        (edo24, [22, 4, 1, 9], 20, [22, 4, 1, 9, 20]),
        (ed13_3, [100, 50, 0], -1, [100, 50, 0, -1]),
    ]
)
def test_with_interval(tuning, input_diffs, new_diff, result_diffs):
    """
    Test if with_interval works
    """

    interval_fan = PitchIntervalFan(
        tuning,
        [tuning.diff_interval(diff) for diff in input_diffs]
    )

    interval_fan = interval_fan.with_interval(
        tuning.diff_interval(new_diff)
    )

    assert len(interval_fan) == len(result_diffs)
    intervals = list(interval_fan)
    assert intervals == [tuning.diff_interval(diff) for diff in result_diffs]


@pytest.mark.parametrize(
    'tuning, input_diffs, new_diff, insert_pos, result_diffs',
    [
        (edo12, [8, 3, 7], 5, 2, [8, 3, 5, 7]),
        (edo24, [2, 3, 2], 5, 0, [5, 2, 3, 2]),
        (edo24, [2, 3, 2], 5, 10, [2, 3, 2, 5]),
    ]
)
def test_with_interval_insert_pos(
    tuning,
    input_diffs,
    new_diff,
    insert_pos,
    result_diffs
):
    """
    Test if with_interval works with insert_pos parameter
    """

    interval_fan = PitchIntervalFan(
        tuning,
        [tuning.diff_interval(diff) for diff in input_diffs]
    )

    interval_fan = interval_fan.with_interval(
        tuning.diff_interval(new_diff), insert_pos
    )

    assert len(interval_fan) == len(result_diffs)
    intervals = list(interval_fan)
    assert intervals == [tuning.diff_interval(diff) for diff in result_diffs]


def test_with_interval_incompatible_origin_contexts():
    """
    Test if with_interval raises IncompatibleOriginContexts if argument
    originates from a different tuning
    """

    edo12_2 = EDTuning(12, FrequencyRatio(2))
    tunings = edo12, edo24, edo31, ed13_3, edo12_2

    for i, tuning_a in enumerate(tunings):

        for tuning_b in tunings[i+1:]:

            interval_fan = PitchIntervalFan(
                tuning_a
            )

            with pytest.raises(IncompatibleOriginContexts):
                interval_fan.with_interval(
                    tuning_b.diff_interval(4)
                )


def test_eq():
    """
    Test if interval_fan equalities and inequalities work correctly
    """

    interval_fan_a = edo12.diff_interval_fan([1, 2, 3])
    interval_fan_b = edo12.diff_interval_fan([1, 2, 3])
    interval_fan_c = edo12.diff_interval_fan([1, 2, 3, 4])

    interval_fan_d = edo31.diff_interval_fan([1, 2, 3])
    interval_fan_e = edo24.diff_interval_fan([2, 4, 6])

    assert interval_fan_a == interval_fan_a
    assert interval_fan_a == interval_fan_b
    assert interval_fan_a == interval_fan_e
    assert interval_fan_a != interval_fan_c
    assert interval_fan_a != interval_fan_d

    assert hash(interval_fan_a) == hash(interval_fan_a)
    assert hash(interval_fan_a) == hash(interval_fan_b)
    assert hash(interval_fan_a) == hash(interval_fan_e)
    assert hash(interval_fan_a) != hash(interval_fan_c)
    assert hash(interval_fan_a) != hash(interval_fan_d)

    assert 'XYZ' != interval_fan_a
    assert 3 != interval_fan_a
    assert interval_fan_a != 'XYZ'
    assert interval_fan_a != 3


@pytest.mark.parametrize(
    'tuning, diffs',
    [
        (edo12, [8, 3, 7]),
        (edo24, [22, 4, 1, 9]),
        (edo31, [16, 33, 39]),
        (edo31, [16, 39, 33, 39]),
        (ed13_3, [100, 50, 0]),
    ]
)
def test_getitem(tuning, diffs):
    """
    Test if fetching single interval items works correctly
    """

    interval_fan = PitchIntervalFan(
        tuning,
        [tuning.diff_interval(diff) for diff in diffs]
    )
    for i, diff in enumerate(diffs):
        assert interval_fan[i] == tuning.diff_interval(diff)


@pytest.mark.parametrize(
    'tuning, input_diffs, start, stop, result_diffs',
    [
        (edo12,  [3, 7, 8],         0,  2, [3, 7]),
        (edo24,  [1, 4, 9, 22],     1,  3, [4, 9]),
        (edo31,  [16, 33, 39],      0,  3, [16, 33, 39]),
        (edo31,  [16, 17, 33, 39],  0, -1, [16, 17, 33]),
        (ed13_3, [0, 50, 100],     -3, -1, [0, 50]),
    ]
)
def test_getitem_slice(tuning, input_diffs, start, stop, result_diffs):
    """
    Test if slicing of interval_fan works correctly
    """

    interval_fan_a = PitchIntervalFan(
        tuning,
        [tuning.diff_interval(diff) for diff in input_diffs]
    )

    interval_fan_b = PitchIntervalFan(
        tuning,
        [tuning.diff_interval(diff) for diff in result_diffs]
    )

    assert interval_fan_a[start:stop] == interval_fan_b


@pytest.mark.parametrize(
    'tuning, input_diffs, start, result_diffs',
    [
        (edo12,  [3, 7, 8],         0, [3, 7, 8]),
        (edo24,  [1, 4, 9, 22],     1, [4, 9, 22]),
        (edo31,  [16, 33, 39],     -2, [33, 39]),
        (edo31,  [16, 17, 33, 39], -3, [17, 33, 39]),
        (ed13_3, [0, 50, 100],      2, [100]),
    ]
)
def test_getitem_slice_omit_stop(tuning, input_diffs, start, result_diffs):
    """
    Test if slicing of interval_fan works correctly when
    stop parameter is omitted
    """

    interval_fan_a = PitchIntervalFan(
        tuning,
        [tuning.diff_interval(diff) for diff in input_diffs]
    )

    interval_fan_b = PitchIntervalFan(
        tuning,
        [tuning.diff_interval(diff) for diff in result_diffs]
    )

    assert interval_fan_a[start:] == interval_fan_b


@pytest.mark.parametrize(
    'tuning, input_diffs, stop, result_diffs',
    [
        (edo12,  [3, 8, 7],         0, []),
        (edo24,  [1, 4, 9, 22],     1, [1]),
        (edo31,  [16, 33, 39],     -2, [16]),
        (edo31,  [16, 17, 33, 39], -3, [16]),
        (ed13_3, [0, 50, 100],      2, [0, 50]),
    ]
)
def test_getitem_slice_omit_start(tuning, input_diffs, stop, result_diffs):
    """
    Test if slicing of interval_fan works correctly when
    start parameter is omitted
    """

    interval_fan_a = PitchIntervalFan(
        tuning,
        [tuning.diff_interval(diff) for diff in input_diffs]
    )

    interval_fan_b = PitchIntervalFan(
        tuning,
        [tuning.diff_interval(diff) for diff in result_diffs]
    )

    assert interval_fan_a[:stop] == interval_fan_b


@pytest.mark.parametrize(
    'tuning, input_diffs, mask, result_diffs',
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
def test_partial(tuning, input_diffs, mask, result_diffs):
    """
    Test if partial function of interval fans works correctly
    """

    interval_fan_a = PitchIntervalFan(
        tuning,
        [tuning.diff_interval(diff) for diff in input_diffs]
    )

    interval_fan_b = PitchIntervalFan(
        tuning,
        [tuning.diff_interval(diff) for diff in result_diffs]
    )
    assert interval_fan_a.partial(mask) == interval_fan_b


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
    Test if partial function of interval fans raises correct exception
    when invalid mask is given
    """

    interval_fan = tuning.diff_interval_fan([2, 23, 14, 5, 1, 7])

    with pytest.raises(InvalidIndexMask):
        interval_fan.partial(mask)


@pytest.mark.parametrize(
    'tuning, input_diffs, mask, result_diffs',
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
def test_partial_not(tuning, input_diffs, mask, result_diffs):
    """
    Test if partial_not function of interval fans works correctly
    """

    interval_fan_a = PitchIntervalFan(
        tuning,
        [tuning.diff_interval(diff) for diff in input_diffs]
    )

    interval_fan_b = PitchIntervalFan(
        tuning,
        [tuning.diff_interval(diff) for diff in result_diffs]
    )
    assert interval_fan_a.partial_not(mask) == interval_fan_b


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
    Test if partial_not function of interval fans raises
    correct exception when invalid mask is given
    """

    interval_fan = tuning.diff_interval_fan([2, 23, 14, 5, 1, 7])

    with pytest.raises(InvalidIndexMask):
        interval_fan.partial_not(mask)


@pytest.mark.parametrize(
    'tuning, input_diffs, mask',
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
def test_partition(tuning, input_diffs, mask):
    """
    Test if partition function of interval fans works correctly
    """

    interval_fan = PitchIntervalFan(
        tuning,
        [tuning.diff_interval(diff) for diff in input_diffs]
    )

    positive = interval_fan.partial(mask)
    complement = interval_fan.partial_not(mask)

    assert interval_fan.partition(mask) == (positive, complement)


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
    Test if partition function of interval fans raises
    correct exception when invalid mask is given
    """

    interval_fan = tuning.diff_interval_fan([2, 23, 14, 5, 1, 7])

    with pytest.raises(InvalidIndexMask):
        interval_fan.partition(mask)


@pytest.mark.parametrize(
    'tuning, input_diffs',
    [
        (edo12, [8, 3, 7]),
        (edo24, [22, 4, 1, 9]),
        (edo31, [16, 33, 39]),
        (edo31, [16, 39, 33, 39]),
        (ed13_3, [100, 50, 0]),
    ]
)
def test_in_operator(tuning, input_diffs):
    """
    Test if 'in' operator works
    """

    interval_fan = PitchIntervalFan(
        tuning,
        [tuning.diff_interval(diff) for diff in input_diffs]
    )

    for diff in input_diffs:
        assert tuning.diff_interval(diff) in interval_fan


@pytest.mark.parametrize(
    'tuning, input_diffs, excl_diffs',
    [
        (edo12, [8, 3, 7], [0, 1, 4, 9, 10, 31]),
        (edo24, [22, 4, 1, 9], [21, 23, 0, 5, 10]),
        (edo31, [16, 33, 39], [19, 3, 5]),
        (edo31, [16, 39, 33, 39], [13, 2, 44, 74]),
        (ed13_3, [100, 50, 0], [9, 444, 3]),
    ]
)
def test_not_in_operator(tuning, input_diffs, excl_diffs):
    """
    Test if 'not in' operator works
    """

    interval_fan = PitchIntervalFan(
        tuning,
        [tuning.diff_interval(diff) for diff in input_diffs]
    )

    for diff in excl_diffs:
        assert tuning.diff_interval(diff) not in interval_fan


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

    interval_fan = PitchIntervalFan(
        tuning,
        [tuning.diff_interval(diff) for diff in [3, 5, 6]]
    )

    assert 'XYZ' not in interval_fan
    assert 8 not in interval_fan
    assert False not in interval_fan


@pytest.mark.parametrize(
    'tuning, input_diffs, repr_str',
    [
        (edo12, [3, 8, 7], 'PitchIntervalFan([3, 8, 7], 12-EDO)'),
        (edo24, [1, 7, 3, 33], 'PitchIntervalFan([1, 7, 3, 33], 24-EDO)'),
        (edo31, [4, 8, 10, 22, 13], 'PitchIntervalFan([4, 8, 10, 22, 13], 31-EDO)'),
        (ed13_3, [0, 8, 9, 15, 2], 'PitchIntervalFan([0, 8, 9, 15, 2], 13ed3)'),
    ]
)
def test_repr(tuning, input_diffs, repr_str):
    """
    Test if repr() returns the right string for scale
    """

    interval_fan = PitchIntervalFan(
        tuning,
        [tuning.diff_interval(diff) for diff in input_diffs]
    )
    assert repr(interval_fan) == repr_str


@pytest.mark.parametrize(
    'tuning',
    [
        edo12, edo24, edo31, ed13_3
    ]
)
def test_frequency_ratios(tuning):
    """
    Test if frequency_ratios property works correctly
    """

    interval_fan = PitchIntervalFan(
        tuning,
        [tuning.diff_interval(diff) for diff in [3, 5, 6]]
    )

    assert interval_fan.frequency_ratios == [
        tuning.diff_interval(3).frequency_ratio,
        tuning.diff_interval(5).frequency_ratio,
        tuning.diff_interval(6).frequency_ratio,
    ]


@pytest.mark.parametrize(
    'tuning',
    [
        edo12, edo24, edo31, ed13_3
    ]
)
def test_cents(tuning):
    """
    Test if cents property works correctly
    """

    interval_fan = PitchIntervalFan(
        tuning,
        [tuning.diff_interval(diff) for diff in [3, 5, 6]]
    )

    assert interval_fan.cents == [
        tuning.diff_interval(3).cents,
        tuning.diff_interval(5).cents,
        tuning.diff_interval(6).cents,
    ]


@pytest.mark.parametrize(
    'tuning, diffs',
    [
        (edo12, [8, 3, 7]),
        (edo12, [8, 3, 7, 3]),
        (edo24, [22, 4, 1, 9]),
        (edo31, [16, 33, 39]),
        (ed13_3, [100, 50, 0]),
    ]
)
def test_pitch_diffs(tuning, diffs):
    """
    Test if pitch_diffs property works correctly
    """

    interval_fan = PitchIntervalFan(
        tuning,
        [tuning.diff_interval(diff) for diff in diffs]
    )

    assert interval_fan.pitch_diffs == diffs


@pytest.mark.parametrize(
    'tuning, diff_a, diff_b, diff_result',
    [
        (edo12, [4, 3, 7], [2, 3], [4, 3, 7, 2, 3]),
        (edo12, [9, 9, 3], [6], [9, 9, 3, 6]),
        (edo24, [22, 4, 1, 9], [], [22, 4, 1, 9]),
        (edo31, [], [16, 33, 39], [16, 33, 39]),
        (edo31, [], [], []),
        (ed13_3, [100, 50, 0], [4, 4, 1], [100, 50, 0, 4, 4, 1]),
    ]
)
def test_addition(tuning, diff_a, diff_b, diff_result):
    """
    Test if interval fan addition works correctly
    """

    interval_fan_a = PitchIntervalFan(
        tuning,
        [tuning.diff_interval(diff) for diff in diff_a]
    )

    interval_fan_b = PitchIntervalFan(
        tuning,
        [tuning.diff_interval(diff) for diff in diff_b]
    )

    interval_fan_result = PitchIntervalFan(
        tuning,
        [tuning.diff_interval(diff) for diff in diff_result]
    )

    assert interval_fan_a + interval_fan_b == interval_fan_result


@pytest.mark.parametrize(
    'tuning, diff, scalar, diff_result',
    [
        (edo12, [4, 3, 7], 3, [4, 3, 7, 4, 3, 7, 4, 3, 7]),
        (edo12, [9, 9, 3], 4, [9, 9, 3, 9, 9, 3, 9, 9, 3, 9, 9, 3]),
        (edo24, [22, 4, 1, 9], 0, []),
        (edo31, [1, 2], 1, [1, 2]),
        (edo31, [], 5, []),
        (ed13_3, [100, 50, 0], 2, [100, 50, 0, 100, 50, 0]),
    ]
)
def test_scalar_multiplication(tuning, diff, scalar, diff_result):
    """
    Test if interval fan can be multiplied with scalars
    """

    interval_fan = PitchIntervalFan(
        tuning,
        [tuning.diff_interval(diff) for diff in diff]
    )

    interval_fan_result = PitchIntervalFan(
        tuning,
        [tuning.diff_interval(diff) for diff in diff_result]
    )

    assert scalar * interval_fan == interval_fan_result
    assert interval_fan * scalar == interval_fan_result


@pytest.mark.parametrize(
    'tuning, diff, diff_result',
    [
        (edo12, [4, 3, 7], [-4, -3, -7]),
        (edo12, [], []),
        (edo24, [-4, 3, 10, -5, 27], [4, -3, -10, 5, -27]),
        (ed13_3, [0, -4], [0, 4]),
    ]
)
def test_inversion(tuning, diff, diff_result):
    """
    Test if interval fan inversion works correctly
    """

    interval_fan = PitchIntervalFan(
        tuning,
        [tuning.diff_interval(diff) for diff in diff]
    )

    interval_fan_result = PitchIntervalFan(
        tuning,
        [tuning.diff_interval(diff) for diff in diff_result]
    )

    assert interval_fan.inversion() == interval_fan_result


@pytest.mark.parametrize(
    'tuning, diff, interval, result',
    [
        (edo12, [4, 3, 7], 3, 1),
        (edo24, [9, 9, 3, 6, 4, 2, 6], 6, 3),
    ]
)
def test_index(tuning, diff, interval, result):
    """
    Test if intervals can be found with index and
    no additional restriction parameters
    """

    interval_fan = PitchIntervalFan(
        tuning,
        [tuning.diff_interval(diff) for diff in diff]
    )

    interval = tuning.diff_interval(interval)

    assert interval_fan.index(interval) == result


@pytest.mark.parametrize(
    'tuning, diff, interval',
    [
        (edo12, [4, 3, 7], 5),
        (edo24, [9, 9, 3, 6, 4, 2, 6], 12),
    ]
)
def test_index_value_error(tuning, diff, interval):
    """
    Test if index raises ValueError if interval was not found
    """

    interval_fan = PitchIntervalFan(
        tuning,
        [tuning.diff_interval(diff) for diff in diff]
    )

    interval = tuning.diff_interval(interval)

    with pytest.raises(ValueError) as excinfo:
        interval_fan.index(interval)
    assert (
        excinfo.value.args[0] ==
        f'{interval} is not in fan'
    )


@pytest.mark.parametrize(
    'tuning, diff, interval, start, result',
    [
        (edo12, [4, 3, 7, 9, 3], 3, 4, 4),
        (edo24, [9, 9, 3, 6, 4, 2, 6], 6, 2, 3),
        (edo24, [9, 9, 3, 6, 4, 2, 6], 6, 4, 6),
    ]
)
def test_index_start(tuning, diff, interval, start, result):
    """
    Test if intervals can be found with index and
    a given start index parameter
    """

    interval_fan = PitchIntervalFan(
        tuning,
        [tuning.diff_interval(diff) for diff in diff]
    )

    interval = tuning.diff_interval(interval)

    assert interval_fan.index(interval, start) == result


@pytest.mark.parametrize(
    'tuning, diff, interval, start',
    [
        (edo12, [4, 3, 7, 9, 1], 3, 4),
        (edo24, [9, 9, 3, 6, 4, 2, 6], 9, 2),
        (edo24, [9, 9, 3, 6, 4, 2, 6], 16, 0),
    ]
)
def test_index_start_value_error(tuning, diff, interval, start):
    """
    Test if index raises ValueError if interval was not found
    after a given start value
    """

    interval_fan = PitchIntervalFan(
        tuning,
        [tuning.diff_interval(diff) for diff in diff]
    )

    interval = tuning.diff_interval(interval)

    with pytest.raises(ValueError) as excinfo:
        interval_fan.index(interval, start)
    assert (
        excinfo.value.args[0] ==
        f'{interval} is not in fan'
    )


@pytest.mark.parametrize(
    'tuning, diff, interval, start, stop, result',
    [
        (edo12, [4, 3, 7, 9, 3, 4, 3], 3, 2, 5, 4),
        (edo24, [9, 9, 3, 6, 4, 2, 6], 6, 2, 6, 3),
    ]
)
def test_index_start_stop(tuning, diff, interval, start, stop, result):
    """
    Test if intervals can be found with index and
    a given start and stop parameter
    """

    interval_fan = PitchIntervalFan(
        tuning,
        [tuning.diff_interval(diff) for diff in diff]
    )

    interval = tuning.diff_interval(interval)

    assert interval_fan.index(interval, start, stop) == result


@pytest.mark.parametrize(
    'tuning, diff, interval, start, stop',
    [
        (edo12, [4, 2, 7, 9, 3, 4, 3], 3, 2, 4),
        (edo24, [9, 9, 3, 6, 4, 2, 6], 6, 0, 3),
    ]
)
def test_index_start_stop_value_error(tuning, diff, interval, start, stop):
    """
    Test if index raises ValueError if interval was not found
    between a given start and end index
    """

    interval_fan = PitchIntervalFan(
        tuning,
        [tuning.diff_interval(diff) for diff in diff]
    )

    interval = tuning.diff_interval(interval)

    with pytest.raises(ValueError) as excinfo:
        interval_fan.index(interval, start, stop)
    assert (
        excinfo.value.args[0] ==
        f'{interval} is not in fan'
    )


@pytest.mark.parametrize(
    'tuning, diff, pitch_index, scale_pi',
    [
        (edo12, [0, 4, 2, 7, 9, 3], 3, [3, 7, 5, 10, 12, 6]),
        (edo24, [2, -1, -5, 3], 6, [8, 5, 1, 9]),
    ]
)
def test_scale_conversion(tuning, diff, pitch_index, scale_pi):
    """
    Test if pitch interval fan can be converted into scale
    """

    interval_fan = PitchIntervalFan(
        tuning,
        [tuning.diff_interval(diff) for diff in diff]
    )
    pitch = tuning.pitch(pitch_index)

    expected_scale = tuning.index_scale(scale_pi)
    assert interval_fan.to_scale(pitch) == expected_scale
    assert pitch.scale(interval_fan) == expected_scale


@pytest.mark.parametrize(
    'tuning, diff, pitch_index, seq_pi',
    [
        (edo12, [4, 2, 7, 9, 3], 3, [7, 5, 10, 12, 6]),
        (edo24, [0, 2, -1, -5, 3], 6, [6, 8, 5, 1, 9]),
    ]
)
def test_seq_conversion(tuning, diff, pitch_index, seq_pi):
    """
    Test if pitch interval fan can be converted into sequence
    """

    interval_fan = PitchIntervalFan(
        tuning,
        [tuning.diff_interval(diff) for diff in diff]
    )
    pitch = tuning.pitch(pitch_index)

    expected_seq = tuning.index_seq(seq_pi)
    assert interval_fan.to_seq(pitch) == expected_seq
    assert pitch.seq(interval_fan) == expected_seq


def test_seq_conversion_incompatible_origin_context():
    """
    Test if sequence conversion raises correct error if parameter is
    from different origin context
    """

    interval_fan = edo12.interval_fan(
        [edo12.diff_interval(diff) for diff in [1, 2, 3]]
    )
    pitch = edo24.pitch(3)

    with pytest.raises(IncompatibleOriginContexts):
        interval_fan.to_seq(pitch)

    with pytest.raises(IncompatibleOriginContexts):
        pitch.seq(interval_fan)


def test_scale_conversion_incompatible_origin_context():
    """
    Test if scale conversion raises correct error if parameter is
    from different origin context
    """

    interval_fan = edo12.interval_fan(
        [edo12.diff_interval(diff) for diff in [1, 2, 3]]
    )
    pitch = edo24.pitch(3)

    with pytest.raises(IncompatibleOriginContexts):
        interval_fan.to_scale(pitch)

    with pytest.raises(IncompatibleOriginContexts):
        pitch.scale(interval_fan)


@pytest.mark.parametrize(
    'tuning_a, input_pd, tuning_b, result_pd',
    [
        (edo12, [0, 3, 7, 8, 10], edo31, [0, 8, 18, 21, 26]),
        (edo12, [1, 4, 6, 7, 8, 11], edo24, [2, 8, 12, 14, 16, 22]),
        (edo24, [8, 16, 2, 12, 14, 22], edo12, [4, 8, 1, 6, 7, 11]),
        (edo24, [12, 1, 8, 14, 16, 22], edo12, [6, 0, 4, 7, 8, 11]),
    ]
)
def test_retune_closest(tuning_a, input_pd, tuning_b, result_pd):
    """
    Test if retune_closest method works correctly
    """

    interval_fan_a = tuning_a.diff_interval_fan(input_pd)

    interval_fan_b = interval_fan_a.retune_closest(tuning_b)

    expected_interval_fan_b = tuning_b.diff_interval_fan(result_pd)
    assert interval_fan_b == expected_interval_fan_b
