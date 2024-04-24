import pytest
from xenharmlib.core.frequencies import Frequency
from xenharmlib.core.tunings import EDTuning
from xenharmlib.core.pitch import EDPitch
from xenharmlib.core.pitch_scale import PeriodicPitchScale
from xenharmlib.exc import IncompatibleTunings

edo12 = EDTuning(12, Frequency(2))
edo24 = EDTuning(24, Frequency(2))
edo31 = EDTuning(31, Frequency(2))
ed13_3 = EDTuning(13, Frequency(3))

@pytest.mark.parametrize(
    'tuning, pi_list, n_pi_list',
    [
        (edo12, [7, 13, 19, 24], [0, 1, 7]),
        (edo31, [13, 39, 48, 65], [3, 8, 13, 17])
    ]
)
def test_pcs_normalized(tuning, pi_list, n_pi_list):
    """
    Test if pcs_normalized method works correctly
    """

    pitches = [
        tuning.pitch(pi) for pi in pi_list
    ]
    scale = PeriodicPitchScale(
        tuning, pitches
    )
    normalized = scale.pcs_normalized()
    for i, n_pi in enumerate(n_pi_list):
        assert normalized[i] == tuning.pitch(n_pi)


@pytest.mark.parametrize(
    'tuning, pi_list, n_pi_list',
    [
        (edo12, [7, 12, 19, 24], [1, 2, 3, 4, 5, 6, 8, 9, 10, 11]),
        (edo12, [0, 2, 4, 17, 7, 13, 11], [3, 6, 8, 9, 10])
    ]
)
def test_pcs_normalized_complement(tuning, pi_list, n_pi_list):
    """
    Test if pcs_normalized_complement method works correctly
    """

    pitches = [
        tuning.pitch(pi) for pi in pi_list
    ]
    scale = PeriodicPitchScale(
        edo12, pitches
    )
    normalized = scale.pcs_normalized_complement()
    for i, n_pi in enumerate(n_pi_list):
        assert normalized[i] == tuning.pitch(n_pi)


@pytest.mark.parametrize(
    'tuning, original_pi, rotated_pi',
    [
        (edo12, [2, 5, 9], [5, 9, 14]),
        (edo31, [5, 18, 28], [18, 28, 36]),
        (edo12, [2, 5, 13], [5, 13, 14]),
    ]
)
def test_rotated_up(tuning, original_pi, rotated_pi):
    """
    Test if rotated_up method works correctly
    """

    pitches = [
        tuning.pitch(pi) for pi in original_pi
    ]
    scale = tuning.pitch_scale(
        pitches
    )
    rotated = scale.rotated_up()
    for i, pi in enumerate(rotated_pi):
        assert rotated[i] == tuning.pitch(pi)


@pytest.mark.parametrize(
    'tuning, original_pi, rotated_pi',
    [
        (edo12, [5, 9, 14], [2, 5, 9]),
        (edo31, [18, 28, 36], [5, 18, 28]),
        (edo12, [5, 13, 14], [2, 5, 13]),
        (edo12, [14, 19, 28], [4, 14, 19]),
    ]
)
def test_rotated_down(tuning, original_pi, rotated_pi):
    """
    Test if rotated_down method works correctly
    """

    pitches = [
        tuning.pitch(pi) for pi in original_pi
    ]
    scale = tuning.pitch_scale(
        pitches
    )
    rotated = scale.rotated_down()
    for i, pi in enumerate(rotated_pi):
        assert rotated[i] == tuning.pitch(pi)


@pytest.mark.parametrize(
    'tuning, original_pi, order, rotated_pi',
    [
        (edo12, [2, 5, 9], 0, [2, 5, 9]),
        (edo12, [2, 5, 9], 1, [5, 9, 14]),
        (edo31, [5, 18, 28], 1, [18, 28, 36]),
        (edo12, [2, 5, 13], 1, [5, 13, 14]),
        (edo12, [2, 5, 13], 2, [13, 14, 17]),
        (edo12, [5, 9, 14], -1, [2, 5, 9]),
        (edo31, [18, 28, 36], -1, [5, 18, 28]),
        (edo12, [5, 13, 14], -1, [2, 5, 13]),
        (edo12, [14, 19, 28], -1, [4, 14, 19]),
        (edo12, [24, 29, 38], -2, [5, 14, 24]),
    ]
)
def test_rotation(tuning, original_pi, order, rotated_pi):
    """
    Test if rotation method works correctly
    """

    pitches = [
        tuning.pitch(pi) for pi in original_pi
    ]
    scale = tuning.pitch_scale(
        pitches
    )
    rotated = scale.rotation(order)
    for i, pi in enumerate(rotated_pi):
        assert rotated[i] == tuning.pitch(pi)


@pytest.mark.parametrize(
    'tuning, pitch_indices, pc_indices',
    [
        (edo12, [3, 5, 9, 15, 19, 20], [3, 5, 9, 3, 7, 8]),
        (edo31, [19, 20, 36, 51, 58], [19, 20, 5, 20, 27]),
    ]
)
def test_pc_indices(tuning, pitch_indices, pc_indices):
    """
    Test if pc_indices property works correctly
    """

    pitches = [
        tuning.pitch(pi) for pi in pitch_indices
    ]
    scale = tuning.pitch_scale(pitches)
    assert scale.pc_indices == pc_indices


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

    scale_a = PeriodicPitchScale(
        tuning, 
        [tuning.pitch(pi) for pi in input_pi_a]
    )

    scale_b = PeriodicPitchScale(
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

            scale_a = PeriodicPitchScale(
                tuning_a
            )
            scale_b = PeriodicPitchScale(
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

    scale_a = PeriodicPitchScale(
        tuning, 
        [tuning.pitch(pi) for pi in input_pi_a]
    )

    scale_b = PeriodicPitchScale(
        tuning, 
        [tuning.pitch(pi) for pi in input_pi_b]
    )

    scale_c = scale_a.intersection(scale_b)

    assert len(scale_c) == len(result_pi)
    pitches = list(scale_c)
    assert pitches == [tuning.pitch(pi) for pi in result_pi]


@pytest.mark.parametrize(
    'tuning, input_pi_a, input_pi_b, result_pi',
    [
        (edo12, [3, 8, 19], [5, 7, 8], [7, 8, 19]),
        (edo24, [1, 11, 12], [1, 11, 36], [1, 11, 12, 36]),
        (edo31, [3, 11, 64], [1, 9, 12], []),
        (ed13_3, [3, 11, 20], [], []),
    ]
)
def test_intersection_ignore_bi_index(tuning,
                                      input_pi_a,
                                      input_pi_b,
                                      result_pi):
    """
    Test if intersection operation works correctly
    on ignore_bi_index=True
    """

    scale_a = PeriodicPitchScale(
        tuning, 
        [tuning.pitch(pi) for pi in input_pi_a]
    )

    scale_b = PeriodicPitchScale(
        tuning, 
        [tuning.pitch(pi) for pi in input_pi_b]
    )

    scale_c = scale_a.intersection(
        scale_b, ignore_bi_index=True
    )

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

            scale_a = PeriodicPitchScale(
                tuning_a
            )
            scale_b = PeriodicPitchScale(
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

    scale_a = PeriodicPitchScale(
        tuning, 
        [tuning.pitch(pi) for pi in input_pi_a]
    )

    scale_b = PeriodicPitchScale(
        tuning, 
        [tuning.pitch(pi) for pi in input_pi_b]
    )

    scale_c = scale_a.difference(scale_b)

    assert len(scale_c) == len(result_pi)
    pitches = list(scale_c)
    assert pitches == [tuning.pitch(pi) for pi in result_pi]


@pytest.mark.parametrize(
    'tuning, input_pi_a, input_pi_b, result_pi',
    [
        (edo12, [3, 8, 7], [5, 19, 8], [3]),
        (edo24, [1, 11, 12], [25, 35, 36], []),
        (edo31, [3, 11, 64], [32, 40, 43], [3, 11, 64]),
        (ed13_3, [3, 11, 20], [], [3, 11, 20]),
    ]
)
def test_difference_ignore_bi_index(tuning,
                                    input_pi_a,
                                    input_pi_b,
                                    result_pi):
    """
    Test if difference operation works correctly
    on ignore_bi_index=True
    """

    scale_a = PeriodicPitchScale(
        tuning, 
        [tuning.pitch(pi) for pi in input_pi_a]
    )

    scale_b = PeriodicPitchScale(
        tuning, 
        [tuning.pitch(pi) for pi in input_pi_b]
    )

    scale_c = scale_a.difference(
        scale_b, ignore_bi_index=True
    )

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

            scale_a = PeriodicPitchScale(
                tuning_a
            )
            scale_b = PeriodicPitchScale(
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

    scale_a = PeriodicPitchScale(
        tuning, 
        [tuning.pitch(pi) for pi in input_pi_a]
    )

    scale_b = PeriodicPitchScale(
        tuning, 
        [tuning.pitch(pi) for pi in input_pi_b]
    )

    scale_c = scale_a.symmetric_difference(scale_b)

    assert len(scale_c) == len(result_pi)
    pitches = list(scale_c)
    assert pitches == [tuning.pitch(pi) for pi in result_pi]


@pytest.mark.parametrize(
    'tuning, input_pi_a, input_pi_b, result_pi',
    [
        (edo12, [3, 8, 7], [5, 7, 20], [3, 5]),
        (edo24, [1, 11, 12], [1, 11, 12], []),
        (edo31, [3, 11, 8, 64], [1, 9, 12, 39], [1, 3, 9, 11, 12, 64]),
        (ed13_3, [3, 11, 20], [], [3, 11, 20]),
    ]
)
def test_symmetric_difference_ignore_bi_index(tuning,
                                              input_pi_a,
                                              input_pi_b,
                                              result_pi):
    """
    Test if symmetric difference operation works correctly
    on ignore_bi_index=True
    """

    scale_a = PeriodicPitchScale(
        tuning, 
        [tuning.pitch(pi) for pi in input_pi_a]
    )

    scale_b = PeriodicPitchScale(
        tuning, 
        [tuning.pitch(pi) for pi in input_pi_b]
    )

    scale_c = scale_a.symmetric_difference(
        scale_b,
        ignore_bi_index=True
    )

    assert len(scale_c) == len(result_pi)
    pitches = list(scale_c)
    assert pitches == [tuning.pitch(pi) for pi in result_pi]


def test_symmetric_difference_incompatible_tunings():
    """
    Test if symmetric difference operation fails if scales
    originate from different tunings
    """

    edo12_2 = EDTuning(12, Frequency(2))
    tunings = edo12, edo24, edo31, ed13_3, edo12_2

    for i, tuning_a in enumerate(tunings):

        for tuning_b in tunings[i+1:]:

            scale_a = PeriodicPitchScale(
                tuning_a
            )
            scale_b = PeriodicPitchScale(
                tuning_b
            )

            with pytest.raises(IncompatibleTunings):
                scale_a.symmetric_difference(scale_b)


@pytest.mark.parametrize(
    'tuning, input_pi_a, input_pi_b, result_pi',
    [
        (edo12, [3, 8, 7], [5, 7, 20], [7, 8]),
        (edo24, [1, 11, 26], [1, 11, 26], [1, 2, 11]),
        (edo31, [3, 11, 8, 64], [1, 9, 12, 40], []),
        (ed13_3, [3, 11, 20], [], []),
    ]
)
def test_equivalents(tuning,
                     input_pi_a,
                     input_pi_b,
                     result_pi):
    """
    Test if equivalents method works correctly
    """

    scale_a = PeriodicPitchScale(
        tuning,
        [tuning.pitch(pi) for pi in input_pi_a]
    )

    scale_b = PeriodicPitchScale(
        tuning,
        [tuning.pitch(pi) for pi in input_pi_b]
    )

    scale_c = scale_a.equivalents(scale_b)

    assert len(scale_c) == len(result_pi)
    pitches = list(scale_c)
    assert pitches == [tuning.pitch(pi) for pi in result_pi]


def test_equivalents_incompatible_tunings():
    """
    Test if equivalents method fails if scales originate from
    different tunings
    """

    edo12_2 = EDTuning(12, Frequency(2))
    tunings = edo12, edo24, edo31, ed13_3, edo12_2

    for i, tuning_a in enumerate(tunings):

        for tuning_b in tunings[i+1:]:

            scale_a = PeriodicPitchScale(
                tuning_a
            )
            scale_b = PeriodicPitchScale(
                tuning_b
            )

            with pytest.raises(IncompatibleTunings):
                scale_a.equivalents(scale_b)


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

    scale_a = PeriodicPitchScale(
        tuning, 
        [tuning.pitch(pi) for pi in input_pi_a]
    )

    scale_b = PeriodicPitchScale(
        tuning, 
        [tuning.pitch(pi) for pi in input_pi_b]
    )

    assert scale_a.is_disjoint(scale_b) == expected


@pytest.mark.parametrize(
    'tuning, input_pi_a, input_pi_b, expected',
    [
        (edo12, [3, 20, 19], [5, 7, 8], False),
        (edo24, [1, 11, 12], [25, 35, 36], False),
        (edo31, [3, 11, 64], [32, 9, 12], True),
        (ed13_3, [3, 11, 20], [], True),
    ]
)
def test_is_disjoint_ignore_bi_index(tuning,
                                     input_pi_a,
                                     input_pi_b,
                                     expected):
    """
    Test if is_disjoint set test works correctly
    on ignore_bi_index=True
    """

    scale_a = PeriodicPitchScale(
        tuning, 
        [tuning.pitch(pi) for pi in input_pi_a]
    )

    scale_b = PeriodicPitchScale(
        tuning, 
        [tuning.pitch(pi) for pi in input_pi_b]
    )

    assert scale_a.is_disjoint(
        scale_b, ignore_bi_index=True
    ) == expected


def test_is_disjoint_incompatible_tunings():
    """
    Test if is_disjoint set test fails if scales
    originate from different tunings
    """

    edo12_2 = EDTuning(12, Frequency(2))
    tunings = edo12, edo24, edo31, ed13_3, edo12_2

    for i, tuning_a in enumerate(tunings):

        for tuning_b in tunings[i+1:]:

            scale_a = PeriodicPitchScale(
                tuning_a
            )
            scale_b = PeriodicPitchScale(
                tuning_b
            )

            with pytest.raises(IncompatibleTunings):
                scale_a.is_disjoint(scale_b)


@pytest.mark.parametrize(
    'tuning, input_pi_a, input_pi_b, expected',
    [
        (edo12, [5, 8, 7], [5, 8, 19], True),
        (edo12, [8, 7], [5, 8, 19], False),
        (edo12, [5, 8, 7], [5, 8], False),
        (edo24, [1, 11, 12], [25, 35, 36], True),
        (edo31, [3, 11, 64], [1, 9, 12], False),
        (ed13_3, [3, 11, 20], [], False),
        (ed13_3, [], [3, 11, 20], False),
    ]
)
def test_is_equivalent(tuning, input_pi_a, input_pi_b, expected):
    """
    Test if is_equivalent method works correctly
    """

    scale_a = PeriodicPitchScale(
        tuning, 
        [tuning.pitch(pi) for pi in input_pi_a]
    )

    scale_b = PeriodicPitchScale(
        tuning, 
        [tuning.pitch(pi) for pi in input_pi_b]
    )
    assert scale_a.is_equivalent(scale_b) == expected


def test_is_equivalent_incompatible_tunings():
    """
    Test if is_equivalent fails if scales originate from
    different tunings
    """

    edo12_2 = EDTuning(12, Frequency(2))
    tunings = edo12, edo24, edo31, ed13_3, edo12_2

    for i, tuning_a in enumerate(tunings):

        for tuning_b in tunings[i+1:]:

            scale_a = PeriodicPitchScale(
                tuning_a
            )
            scale_b = PeriodicPitchScale(
                tuning_b
            )

            with pytest.raises(IncompatibleTunings):
                scale_a.is_equivalent(scale_b)


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

    scale_a = PeriodicPitchScale(
        tuning, 
        [tuning.pitch(pi) for pi in input_pi_a]
    )

    scale_b = PeriodicPitchScale(
        tuning, 
        [tuning.pitch(pi) for pi in input_pi_b]
    )

    assert scale_a.is_subset(scale_b) == expected


@pytest.mark.parametrize(
    'tuning, input_pi_a, input_pi_b, expected',
    [
        (edo12, [8, 7], [5, 7, 20], True),
        (edo24, [1, 11, 12], [11, 12, 25], True),
        (edo31, [3, 11, 64], [1, 9, 43], False),
        (ed13_3, [3, 11, 20], [], False),
        (ed13_3, [], [3, 11, 20], True),
    ]
)
def test_is_subset_ignore_bi_index(tuning, 
                                   input_pi_a,
                                   input_pi_b, 
                                   expected):
    """
    Test if is_subset test works correctly
    on ignore_bi_index=True
    """

    scale_a = PeriodicPitchScale(
        tuning, 
        [tuning.pitch(pi) for pi in input_pi_a]
    )

    scale_b = PeriodicPitchScale(
        tuning, 
        [tuning.pitch(pi) for pi in input_pi_b]
    )

    assert scale_a.is_subset(
        scale_b,
        ignore_bi_index=True
    ) == expected


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

    scale_a = PeriodicPitchScale(
        tuning, 
        [tuning.pitch(pi) for pi in input_pi_a]
    )

    scale_b = PeriodicPitchScale(
        tuning, 
        [tuning.pitch(pi) for pi in input_pi_b]
    )

    assert scale_a.is_subset(scale_b, proper=True) == expected


@pytest.mark.parametrize(
    'tuning, input_pi_a, input_pi_b, expected',
    [
        (edo12, [8, 7], [5, 7, 20], True),
        (edo24, [1, 11, 12], [1, 11, 12, 25], False),
        (edo31, [3, 11, 64], [1, 9, 43], False),
        (ed13_3, [3, 11, 20], [], False),
        (ed13_3, [], [3, 11, 20], True),
    ]
)
def test_is_subset_proper_ignore_bi_index(tuning, 
                                          input_pi_a,
                                          input_pi_b, 
                                          expected):
    """
    Test if is_subset test works correctly
    on ignore_bi_index=True and proper=True
    """

    scale_a = PeriodicPitchScale(
        tuning, 
        [tuning.pitch(pi) for pi in input_pi_a]
    )

    scale_b = PeriodicPitchScale(
        tuning, 
        [tuning.pitch(pi) for pi in input_pi_b]
    )

    assert scale_a.is_subset(
        scale_b, 
        ignore_bi_index=True,
        proper=True
    ) == expected


def test_is_subset_incompatible_tunings():
    """
    Test if is_subset test fails if scales
    originate from different tunings
    """

    edo12_2 = EDTuning(12, Frequency(2))
    tunings = edo12, edo24, edo31, ed13_3, edo12_2

    for i, tuning_a in enumerate(tunings):

        for tuning_b in tunings[i+1:]:

            scale_a = PeriodicPitchScale(
                tuning_a
            )
            scale_b = PeriodicPitchScale(
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

    scale_a = PeriodicPitchScale(
        tuning, 
        [tuning.pitch(pi) for pi in input_pi_a]
    )

    scale_b = PeriodicPitchScale(
        tuning, 
        [tuning.pitch(pi) for pi in input_pi_b]
    )

    assert scale_a.is_superset(scale_b) == expected


@pytest.mark.parametrize(
    'tuning, input_pi_a, input_pi_b, expected',
    [
        (edo12, [5, 8, 19], [7, 8], True),
        (edo24, [25, 35, 36], [1, 11, 12], True),
        (edo31, [3, 11, 64], [1, 9, 12], False),
        (ed13_3, [3, 11, 20], [], True),
        (ed13_3, [], [3, 11, 20], False),
    ]
)
def test_is_superset_ignore_bi_index(tuning,
                                     input_pi_a,
                                     input_pi_b,
                                     expected):
    """
    Test if is_superset test works correctly
    on ignore_bi_index=True
    """

    scale_a = PeriodicPitchScale(
        tuning, 
        [tuning.pitch(pi) for pi in input_pi_a]
    )

    scale_b = PeriodicPitchScale(
        tuning, 
        [tuning.pitch(pi) for pi in input_pi_b]
    )

    assert scale_a.is_superset(
        scale_b,
        ignore_bi_index=True
    ) == expected


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
def test_is_superset_proper(tuning,
                            input_pi_a,
                            input_pi_b,
                            expected):
    """
    Test if is_superset test works correctly
    on proper=True
    """

    scale_a = PeriodicPitchScale(
        tuning, 
        [tuning.pitch(pi) for pi in input_pi_a]
    )

    scale_b = PeriodicPitchScale(
        tuning, 
        [tuning.pitch(pi) for pi in input_pi_b]
    )

    assert scale_a.is_superset(
        scale_b, proper=True
    ) == expected


@pytest.mark.parametrize(
    'tuning, input_pi_a, input_pi_b, expected',
    [
        (edo12, [5, 8, 19], [7, 8], True),
        (edo24, [25, 35, 36], [1, 11, 12], False),
        (edo31, [3, 11, 64], [1, 9, 12], False),
        (ed13_3, [3, 11, 20], [], True),
        (ed13_3, [], [3, 11, 20], False),
    ]
)
def test_is_superset_proper_ignore_bi_index(tuning,
                                            input_pi_a,
                                            input_pi_b,
                                            expected):
    """
    Test if is_superset test works correctly
    on proper=True and ignore_bi_index=True
    """

    scale_a = PeriodicPitchScale(
        tuning, 
        [tuning.pitch(pi) for pi in input_pi_a]
    )

    scale_b = PeriodicPitchScale(
        tuning, 
        [tuning.pitch(pi) for pi in input_pi_b]
    )

    assert scale_a.is_superset(
        scale_b,
        proper=True,
        ignore_bi_index=True
    ) == expected


def test_is_superset_incompatible_tunings():
    """
    Test if is_superset test fails if scales
    originate from different tunings
    """

    edo12_2 = EDTuning(12, Frequency(2))
    tunings = edo12, edo24, edo31, ed13_3, edo12_2

    for i, tuning_a in enumerate(tunings):

        for tuning_b in tunings[i+1:]:

            scale_a = PeriodicPitchScale(
                tuning_a
            )
            scale_b = PeriodicPitchScale(
                tuning_b
            )

            with pytest.raises(IncompatibleTunings):
                scale_a.is_superset(scale_b)
