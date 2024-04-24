import pytest
from xenharmlib.core.frequencies import Frequency
from xenharmlib.core.tunings import EDOTuning
from xenharmlib.core.tunings import EDTuning
from xenharmlib.core.pitch import EDPitch
from xenharmlib.core.pitch_scale import PitchScale
from xenharmlib.exc import IncompatibleTunings

edo12 = EDOTuning(12)
edo24 = EDOTuning(24)
edo31 = EDOTuning(31)
ed13_3 = EDTuning(13, Frequency(3))


@pytest.mark.parametrize(
    'tuning, input_pi, result_pi',
    [
        (edo12, [8, 3, 7], [3, 7, 8]),
        (edo12, [8, 3, 7, 3], [3, 7, 8]),
        (edo24, [22, 4, 1, 9], [1, 4, 9, 22]),
        (edo31, [16, 33, 39], [16, 33, 39]),
        (ed13_3, [100, 50, 0], [0, 50, 100]),
    ]
)
def test_sort_on_init(tuning, input_pi, result_pi):
    """
    Test if pitches get sorted correctly on scale init
    """

    scale = PitchScale(
        tuning, 
        [tuning.pitch(pi) for pi in input_pi]
    )

    assert len(scale) == len(result_pi)
    pitches = list(scale)
    assert pitches == [tuning.pitch(pi) for pi in result_pi]


@pytest.mark.parametrize(
    'tuning',
    [
        edo12, edo24, edo31, ed13_3
    ]
)
def test_init_empty(tuning):
    """
    Test if scale can be created by omitting pitches parameter
    """

    scale = PitchScale(tuning)

    assert len(scale) == 0
    pitches = list(scale)
    assert pitches == []


@pytest.mark.parametrize(
    'tuning, input_pi, new_pi, result_pi',
    [
        (edo12, [8, 3, 7], 5, [3, 5, 7, 8]),
        (edo24, [22, 4, 1, 9], 20, [1, 4, 9, 20, 22]),
        (edo31, [16, 33, 39], 22, [16, 22, 33, 39]),
        (edo31, [16, 33, 39], 33, [16, 33, 39]),
        (ed13_3, [100, 50, 0], -1, [-1, 0, 50, 100]),
    ]
)
def test_add_pitch(tuning, input_pi, new_pi, result_pi):
    """
    Test if add_pitch correctly insorts new pitch
    """

    scale = PitchScale(
        tuning, 
        [tuning.pitch(pi) for pi in input_pi]
    )

    scale.add_pitch(
        tuning.pitch(new_pi)
    )

    assert len(scale) == len(result_pi)
    pitches = list(scale)
    assert pitches == [tuning.pitch(pi) for pi in result_pi]


def test_add_pitch_incompatible_tunings():
    """
    Test if add_pitch raises IncompatibleTunings if argument
    originates from a different tuning
    """

    edo12_2 = EDTuning(12, Frequency(2))
    tunings = edo12, edo24, edo31, ed13_3, edo12_2

    for i, tuning_a in enumerate(tunings):

        for tuning_b in tunings[i+1:]:

            scale = PitchScale(
                tuning_a
            )

            with pytest.raises(IncompatibleTunings):
                scale.add_pitch(
                    tuning_b.pitch(4)
                )


@pytest.mark.parametrize(
    'tuning, input_pi, new_pi, result_pi',
    [
        (edo12, [8, 3, 7], 5, [3, 5, 7, 8]),
        (edo24, [22, 4, 1, 9], 20, [1, 4, 9, 20, 22]),
        (edo24, [22, 4, 1, 9], 1, [1, 4, 9, 22]),
        (edo31, [16, 33, 39], 22, [16, 22, 33, 39]),
        (ed13_3, [100, 50, 0], -1, [-1, 0, 50, 100]),
    ]
)
def test_add_pitch_index(tuning, input_pi, new_pi, result_pi):
    """
    Test if add_pitch_index correctly insorts new pitch
    """

    scale = PitchScale(
        tuning, 
        [tuning.pitch(pi) for pi in input_pi]
    )

    scale.add_pitch_index(new_pi)

    assert len(scale) == len(result_pi)
    pitches = list(scale)
    assert pitches == [tuning.pitch(pi) for pi in result_pi]


@pytest.mark.parametrize(
    'tuning, input_pi, result_pi',
    [
        (edo12, [8, 3, 7], [3, 7, 8]),
        (edo24, [22, 4, 1, 9], [1, 4, 9, 22]),
        (edo31, [16, 33, 39], [16, 33, 39]),
        (edo31, [16, 39, 33, 39], [16, 33, 39]),
        (ed13_3, [100, 50, 0], [0, 50, 100]),
    ]
)
def test_from_pitch_indices(tuning, input_pi, result_pi):
    """
    Test if builder method from_pitch_indices works
    correctly
    """

    scale = PitchScale.from_pitch_indices(
        input_pi, tuning=tuning
    )

    assert len(scale) == len(result_pi)
    pitches = list(scale)
    assert pitches == [tuning.pitch(pi) for pi in result_pi]


def test_eq():
    """
    Test if scale equalities and inequalities work correctly
    """

    scale_a = PitchScale.from_pitch_indices(
        [1, 2, 3], tuning=edo12
    )
    scale_b = PitchScale.from_pitch_indices(
        [1, 2, 3], tuning=edo12
    )
    scale_c = PitchScale.from_pitch_indices(
        [1, 2, 3, 4], tuning=edo12
    )
    scale_d = PitchScale.from_pitch_indices(
        [1, 2, 3], tuning=edo31
    )
    scale_e = PitchScale.from_pitch_indices(
        [2, 4, 6], tuning=edo24
    )

    assert scale_a == scale_a
    assert scale_a == scale_b
    assert scale_a == scale_e
    assert scale_a != scale_c
    assert scale_a != scale_d
    assert 'XYZ' != scale_a
    assert 3 != scale_a
    assert scale_a != 'XYZ'
    assert scale_a != 3


@pytest.mark.parametrize(
    'tuning, input_pi, result_pi',
    [
        (edo12, [8, 3, 7], [3, 7, 8]),
        (edo24, [22, 4, 1, 9], [1, 4, 9, 22]),
        (edo31, [16, 33, 39], [16, 33, 39]),
        (edo31, [16, 39, 33, 39], [16, 33, 39]),
        (ed13_3, [100, 50, 0], [0, 50, 100]),
    ]
)
def test_getitem(tuning, input_pi, result_pi):
    """
    Test if fetching single pitch items works correctly
    """

    scale = PitchScale(
        tuning, 
        [tuning.pitch(pi) for pi in input_pi]
    )
    for i, pitch_index in enumerate(result_pi):
        assert scale[i] == tuning.pitch(pitch_index)


@pytest.mark.parametrize(
    'tuning, input_pi, start, stop, result_pi',
    [
        (edo12,  [8, 3, 7],         0,  2, [3, 7]),
        (edo24,  [22, 4, 1, 9],     1,  3, [4, 9]),
        (edo31,  [16, 33, 39],      0,  3, [16, 33, 39]),
        (edo31,  [16, 17, 33, 39],  0, -1, [16, 17, 33]),
        (ed13_3, [100, 50, 0],     -3, -1, [0, 50]),
    ]
)
def test_getitem_slice(tuning, input_pi, start, stop, result_pi):
    """
    Test if slicing of scales works correctly
    """

    scale = tuning.pitch_scale(
        [tuning.pitch(pi) for pi in input_pi]
    )
    scale_b = tuning.pitch_scale(
        [tuning.pitch(pi) for pi in result_pi]
    )
    assert scale[start:stop] == scale_b


@pytest.mark.parametrize(
    'tuning, input_pi, start, result_pi',
    [
        (edo12,  [8, 3, 7],         0, [3, 7, 8]),
        (edo24,  [22, 4, 1, 9],     1, [4, 9, 22]),
        (edo31,  [16, 33, 39],     -2, [33, 39]),
        (edo31,  [16, 17, 33, 39], -3, [17, 33, 39]),
        (ed13_3, [100, 50, 0],      2, [100]),
    ]
)
def test_getitem_slice_omit_stop(tuning, input_pi, start, result_pi):
    """
    Test if slicing of scales works correctly when
    stop parameter is omitted
    """

    scale = tuning.pitch_scale(
        [tuning.pitch(pi) for pi in input_pi]
    )
    scale_b = tuning.pitch_scale(
        [tuning.pitch(pi) for pi in result_pi]
    )
    assert scale[start:] == scale_b


@pytest.mark.parametrize(
    'tuning, input_pi, stop, result_pi',
    [
        (edo12,  [8, 3, 7],         2, [3, 7]),
        (edo24,  [22, 4, 1, 9],     1, [1]),
        (edo31,  [16, 33, 39],     -1, [16, 33]),
        (edo31,  [16, 17, 33, 39],  3, [16, 17, 33]),
        (ed13_3, [100, 50, 0],     -2, [0]),
        (ed13_3, [100, 50, 0],     -3, []),
    ]
)
def test_getitem_slice_omit_start(tuning, input_pi, stop, result_pi):
    """
    Test if slicing of scales works correctly when
    start parameter is omitted
    """

    scale = tuning.pitch_scale(
        [tuning.pitch(pi) for pi in input_pi]
    )
    scale_b = tuning.pitch_scale(
        [tuning.pitch(pi) for pi in result_pi]
    )
    assert scale[:stop] == scale_b


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

    scale = PitchScale(
        tuning, 
        [tuning.pitch(pi) for pi in input_pi]
    )

    for pitch_index in input_pi:
        assert tuning.pitch(pitch_index) in scale


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

    scale = PitchScale(
        tuning, 
        [tuning.pitch(pi) for pi in input_pi]
    )

    for pitch_index in excl_pi:
        assert tuning.pitch(pitch_index) not in scale


@pytest.mark.parametrize(
    'tuning, input_pi, interval_pi',
    [
        (edo12, [8, 3, 7], [(0, 4), (0, 1), (0, 0)]),
        (edo31, [4, 8, 10, 22, 13], [(4, 16), (8, 12), (0, 9)]),
        (ed13_3, [0, 8, 15, 9, 66], [(1, 67), (8, 15), (7, 65)]),
    ]
)
def test_in_operator_interval(tuning, input_pi, interval_pi):
    """
    Test if 'in' operator works on intervals
    """

    scale = PitchScale(
        tuning, 
        [tuning.pitch(pi) for pi in input_pi]
    )

    for pi_a, pi_b in interval_pi:
        interval = tuning.pitch(pi_a).interval(
            tuning.pitch(pi_b)
        )
        assert interval in scale


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

    scale = PitchScale(
        tuning, 
        [tuning.pitch(pi) for pi in input_pi]
    )

    for pi_a, pi_b in excl_interval_pi:
        interval = tuning.pitch(pi_a).interval(
            tuning.pitch(pi_b)
        )
        assert interval not in scale


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

    scale = PitchScale(
        tuning, 
        [
            tuning.pitch(8),
            tuning.pitch(3),
            tuning.pitch(7),
        ]
    )

    assert 'XYZ' not in scale
    assert 8 not in scale
    assert False not in scale


@pytest.mark.parametrize(
    'tuning, input_pi, repr_str',
    [
        (edo12, [8, 3, 7], 'PitchScale([3, 7, 8], 12-EDO)'),
        (edo24, [1, 33, 3, 7], 'PitchScale([1, 3, 7, 33], 24-EDO)'),
        (edo31, [4, 8, 10, 22, 13], 'PitchScale([4, 8, 10, 13, 22], 31-EDO)'),
        (ed13_3, [0, 8, 15, 9, 66], 'PitchScale([0, 8, 9, 15, 66], 13ed3)' ),
    ]
)
def test_repr(tuning, input_pi, repr_str):
    """
    Test if repr() returns the right string for scale
    """

    scale = PitchScale(
        tuning,
        [tuning.pitch(pi) for pi in input_pi]
    )
    assert repr(scale) == repr_str


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

    scale = PitchScale(
        tuning, 
        [
            tuning.pitch(8),
            tuning.pitch(3),
            tuning.pitch(7),
        ]
    )

    assert scale.frequencies == [
        tuning.pitch(3).frequency,
        tuning.pitch(7).frequency,
        tuning.pitch(8).frequency,
    ]


@pytest.mark.parametrize(
    'tuning, input_pi, result_pi',
    [
        (edo12, [8, 3, 7], [3, 7, 8]),
        (edo12, [8, 3, 7, 3], [3, 7, 8]),
        (edo24, [22, 4, 1, 9], [1, 4, 9, 22]),
        (edo31, [16, 33, 39], [16, 33, 39]),
        (ed13_3, [100, 50, 0], [0, 50, 100]),
    ]
)
def test_pitch_indices(tuning, input_pi, result_pi):
    """
    Test if pitch_indices property works correctly
    """

    scale = PitchScale(
        tuning, 
        [tuning.pitch(pi) for pi in input_pi]
    )

    assert scale.pitch_indices == result_pi


@pytest.mark.parametrize(
    'tuning, input_pi, interval_pi',
    [
        (edo12, [8, 3, 7], [(3, 7), (7, 8)]),
        (edo31, [4, 8, 10, 22, 13], [(4, 8), (8, 10), (10, 13), (13, 22)]),
        (ed13_3, [0, 8, 15, 9, 66], [(0, 8), (8, 9), (9, 15), (15, 66)]),
    ]
)
def test_to_pitch_intervals(tuning, input_pi, interval_pi):
    """
    Test if to_pitch_intervals method works correctly
    """

    scale = PitchScale(
        tuning, 
        [tuning.pitch(pi) for pi in input_pi]
    )

    intervals = []
    for pi_a, pi_b in interval_pi:
        interval = tuning.pitch_interval(
            tuning.pitch(pi_a), tuning.pitch(pi_b)
        )
        intervals.append(interval)

    assert scale.to_pitch_intervals() == intervals


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

    scale = PitchScale(
        tuning, 
        [tuning.pitch(pi) for pi in input_pi]
    )

    transposed = scale.transpose(diff)
    assert transposed == tuning.pitch_scale(
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

    scale = PitchScale(
        tuning, 
        [tuning.pitch(pi) for pi in input_pi]
    )

    pi_a, pi_b = interval_pi
    interval = tuning.pitch(pi_a).interval(
        tuning.pitch(pi_b)
    )

    transposed = scale.transpose(interval)
    assert transposed == tuning.pitch_scale(
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

    scale_a = tuning_a.pitch_scale(
        [tuning_a.pitch(pi) for pi in input_pi]
    )

    scale_b = scale_a.retune(tuning_b)
    expected_scale_b = tuning_b.pitch_scale(
        [tuning_b.pitch(pi) for pi in result_pi]
    )
    assert scale_b == expected_scale_b


@pytest.mark.parametrize(
    'tuning, input_pi_a, input_pi_b, result_pi',
    [
        (edo12, [3, 8, 7], [5, 7, 8], [3, 5, 7, 8]),
        (edo24, [1, 11, 12], [1, 11, 12], [1, 11, 12]),
        (edo31, [3, 11, 64], [1, 9, 12], [1, 3, 9, 11, 12, 64]),
        (ed13_3, [3, 11, 20], [], [3, 11, 20]),
    ]
)
def test_union(tuning, input_pi_a, input_pi_b, result_pi):
    """
    Test if union operation works correctly
    """

    scale_a = PitchScale(
        tuning, 
        [tuning.pitch(pi) for pi in input_pi_a]
    )

    scale_b = PitchScale(
        tuning, 
        [tuning.pitch(pi) for pi in input_pi_b]
    )

    scale_c = scale_a.union(scale_b)

    assert len(scale_c) == len(result_pi)
    pitches = list(scale_c)
    assert pitches == [tuning.pitch(pi) for pi in result_pi]


def test_union_incompatible_tunings():
    """
    Test if union operation fails if scales originate from
    different tunings
    """

    edo12_2 = EDTuning(12, Frequency(2))
    tunings = edo12, edo24, edo31, ed13_3, edo12_2

    for i, tuning_a in enumerate(tunings):

        for tuning_b in tunings[i+1:]:

            scale_a = PitchScale(
                tuning_a
            )
            scale_b = PitchScale(
                tuning_b
            )

            with pytest.raises(IncompatibleTunings):
                scale_a.union(scale_b)


@pytest.mark.parametrize(
    'tuning, input_pi_a, input_pi_b, result_pi',
    [
        (edo12, [3, 8, 7], [5, 7, 8], [7, 8]),
        (edo24, [1, 11, 12], [1, 11, 12], [1, 11, 12]),
        (edo31, [3, 11, 64], [1, 9, 12], []),
        (ed13_3, [3, 11, 20], [], []),
    ]
)
def test_intersection(tuning, input_pi_a, input_pi_b, result_pi):
    """
    Test if intersection operation works correctly
    """

    scale_a = PitchScale(
        tuning, 
        [tuning.pitch(pi) for pi in input_pi_a]
    )

    scale_b = PitchScale(
        tuning, 
        [tuning.pitch(pi) for pi in input_pi_b]
    )

    scale_c = scale_a.intersection(scale_b)

    assert len(scale_c) == len(result_pi)
    pitches = list(scale_c)
    assert pitches == [tuning.pitch(pi) for pi in result_pi]


def test_intersection_incompatible_tunings():
    """
    Test if intersection operation fails if scales originate from
    different tunings
    """

    edo12_2 = EDTuning(12, Frequency(2))
    tunings = edo12, edo24, edo31, ed13_3, edo12_2

    for i, tuning_a in enumerate(tunings):

        for tuning_b in tunings[i+1:]:

            scale_a = PitchScale(
                tuning_a
            )
            scale_b = PitchScale(
                tuning_b
            )

            with pytest.raises(IncompatibleTunings):
                scale_a.intersection(scale_b)


@pytest.mark.parametrize(
    'tuning, input_pi_a, input_pi_b, result_pi',
    [
        (edo12, [3, 8, 7], [5, 7, 8], [3]),
        (edo24, [1, 11, 12], [1, 11, 12], []),
        (edo31, [3, 11, 64], [1, 9, 12], [3, 11, 64]),
        (ed13_3, [3, 11, 20], [], [3, 11, 20]),
    ]
)
def test_difference(tuning, input_pi_a, input_pi_b, result_pi):
    """
    Test if difference operation works correctly
    """

    scale_a = PitchScale(
        tuning, 
        [tuning.pitch(pi) for pi in input_pi_a]
    )

    scale_b = PitchScale(
        tuning, 
        [tuning.pitch(pi) for pi in input_pi_b]
    )

    scale_c = scale_a.difference(scale_b)

    assert len(scale_c) == len(result_pi)
    pitches = list(scale_c)
    assert pitches == [tuning.pitch(pi) for pi in result_pi]


def test_difference_incompatible_tunings():
    """
    Test if difference operation fails if scales originate from
    different tunings
    """

    edo12_2 = EDTuning(12, Frequency(2))
    tunings = edo12, edo24, edo31, ed13_3, edo12_2

    for i, tuning_a in enumerate(tunings):

        for tuning_b in tunings[i+1:]:

            scale_a = PitchScale(
                tuning_a
            )
            scale_b = PitchScale(
                tuning_b
            )

            with pytest.raises(IncompatibleTunings):
                scale_a.difference(scale_b)


@pytest.mark.parametrize(
    'tuning, input_pi_a, input_pi_b, result_pi',
    [
        (edo12, [3, 8, 7], [5, 7, 8], [3, 5]),
        (edo24, [1, 11, 12], [1, 11, 12], []),
        (edo31, [3, 11, 64], [1, 9, 12], [1, 3, 9, 11, 12, 64]),
        (ed13_3, [3, 11, 20], [], [3, 11, 20]),
    ]
)
def test_symmetric_difference(tuning, input_pi_a, input_pi_b, result_pi):
    """
    Test if symmetric difference operation works correctly
    """

    scale_a = PitchScale(
        tuning, 
        [tuning.pitch(pi) for pi in input_pi_a]
    )

    scale_b = PitchScale(
        tuning, 
        [tuning.pitch(pi) for pi in input_pi_b]
    )

    scale_c = scale_a.symmetric_difference(scale_b)

    assert len(scale_c) == len(result_pi)
    pitches = list(scale_c)
    assert pitches == [tuning.pitch(pi) for pi in result_pi]


def test_symmetric_difference_incompatible_tunings():
    """
    Test if symmetric difference operation fails if scales originate
    from different tunings
    """

    edo12_2 = EDTuning(12, Frequency(2))
    tunings = edo12, edo24, edo31, ed13_3, edo12_2

    for i, tuning_a in enumerate(tunings):

        for tuning_b in tunings[i+1:]:

            scale_a = PitchScale(
                tuning_a
            )
            scale_b = PitchScale(
                tuning_b
            )

            with pytest.raises(IncompatibleTunings):
                scale_a.symmetric_difference(scale_b)


@pytest.mark.parametrize(
    'tuning, input_pi_a, input_pi_b, expected',
    [
        (edo12, [3, 8, 7], [5, 7, 8], False),
        (edo24, [1, 11, 12], [1, 11, 12], False),
        (edo31, [3, 11, 64], [1, 9, 12], True),
        (ed13_3, [3, 11, 20], [], True),
    ]
)
def test_is_disjoint(tuning, input_pi_a, input_pi_b, expected):
    """
    Test if is_disjoint set test works correctly
    """

    scale_a = PitchScale(
        tuning, 
        [tuning.pitch(pi) for pi in input_pi_a]
    )

    scale_b = PitchScale(
        tuning, 
        [tuning.pitch(pi) for pi in input_pi_b]
    )

    assert scale_a.is_disjoint(scale_b) == expected


def test_is_disjoint_incompatible_tunings():
    """
    Test if is_disjoint set test fails if scales originate
    from different tunings
    """

    edo12_2 = EDTuning(12, Frequency(2))
    tunings = edo12, edo24, edo31, ed13_3, edo12_2

    for i, tuning_a in enumerate(tunings):

        for tuning_b in tunings[i+1:]:

            scale_a = PitchScale(
                tuning_a
            )
            scale_b = PitchScale(
                tuning_b
            )

            with pytest.raises(IncompatibleTunings):
                scale_a.is_disjoint(scale_b)


@pytest.mark.parametrize(
    'tuning, input_pi_a, input_pi_b, expected',
    [
        (edo12, [8, 7], [5, 7, 8], True),
        (edo24, [1, 11, 12], [1, 11, 12], True),
        (edo31, [3, 11, 64], [1, 9, 12], False),
        (ed13_3, [3, 11, 20], [], False),
        (ed13_3, [], [3, 11, 20], True),
    ]
)
def test_is_subset(tuning, input_pi_a, input_pi_b, expected):
    """
    Test if is_subset test works correctly
    """

    scale_a = PitchScale(
        tuning, 
        [tuning.pitch(pi) for pi in input_pi_a]
    )

    scale_b = PitchScale(
        tuning, 
        [tuning.pitch(pi) for pi in input_pi_b]
    )

    assert scale_a.is_subset(scale_b) == expected


@pytest.mark.parametrize(
    'tuning, input_pi_a, input_pi_b, expected',
    [
        (edo12, [8, 7], [5, 7, 8], True),
        (edo24, [1, 11, 12], [1, 11, 12], False),
        (edo31, [3, 11, 64], [1, 9, 12], False),
        (ed13_3, [3, 11, 20], [], False),
        (ed13_3, [], [3, 11, 20], True),
    ]
)
def test_is_subset_proper(tuning, input_pi_a, input_pi_b, expected):
    """
    Test if is_subset test works correctly
    with proper=True
    """

    scale_a = PitchScale(
        tuning, 
        [tuning.pitch(pi) for pi in input_pi_a]
    )

    scale_b = PitchScale(
        tuning, 
        [tuning.pitch(pi) for pi in input_pi_b]
    )

    assert scale_a.is_subset(scale_b, proper=True) == expected


def test_is_subset_incompatible_tunings():
    """
    Test if is_subset test fails if scales originate
    from different tunings
    """

    edo12_2 = EDTuning(12, Frequency(2))
    tunings = edo12, edo24, edo31, ed13_3, edo12_2

    for i, tuning_a in enumerate(tunings):

        for tuning_b in tunings[i+1:]:

            scale_a = PitchScale(
                tuning_a
            )
            scale_b = PitchScale(
                tuning_b
            )

            with pytest.raises(IncompatibleTunings):
                scale_a.is_subset(scale_b)


@pytest.mark.parametrize(
    'tuning, input_pi_a, input_pi_b, expected',
    [
        (edo12, [5, 8, 7], [7, 8], True),
        (edo24, [1, 11, 12], [1, 11, 12], True),
        (edo31, [3, 11, 64], [1, 9, 12], False),
        (ed13_3, [3, 11, 20], [], True),
        (ed13_3, [], [3, 11, 20], False),
    ]
)
def test_is_superset(tuning, input_pi_a, input_pi_b, expected):
    """
    Test if is_superset test works correctly
    """

    scale_a = PitchScale(
        tuning, 
        [tuning.pitch(pi) for pi in input_pi_a]
    )

    scale_b = PitchScale(
        tuning, 
        [tuning.pitch(pi) for pi in input_pi_b]
    )

    assert scale_a.is_superset(scale_b) == expected


@pytest.mark.parametrize(
    'tuning, input_pi_a, input_pi_b, expected',
    [
        (edo12, [5, 8, 7], [7, 8], True),
        (edo24, [1, 11, 12], [1, 11, 12], False),
        (edo31, [3, 11, 64], [1, 9, 12], False),
        (ed13_3, [3, 11, 20], [], True),
        (ed13_3, [], [3, 11, 20], False),
    ]
)
def test_is_superset_proper(tuning, input_pi_a, input_pi_b, expected):
    """
    Test if is_superset test works correctly
    with proper=True
    """

    scale_a = PitchScale(
        tuning, 
        [tuning.pitch(pi) for pi in input_pi_a]
    )

    scale_b = PitchScale(
        tuning, 
        [tuning.pitch(pi) for pi in input_pi_b]
    )

    assert scale_a.is_superset(scale_b, proper=True) == expected


def test_is_superset_incompatible_tunings():
    """
    Test if is_subset test fails if scales originate
    from different tunings
    """

    edo12_2 = EDTuning(12, Frequency(2))
    tunings = edo12, edo24, edo31, ed13_3, edo12_2

    for i, tuning_a in enumerate(tunings):

        for tuning_b in tunings[i+1:]:

            scale_a = PitchScale(
                tuning_a
            )
            scale_b = PitchScale(
                tuning_b
            )

            with pytest.raises(IncompatibleTunings):
                scale_a.is_superset(scale_b)