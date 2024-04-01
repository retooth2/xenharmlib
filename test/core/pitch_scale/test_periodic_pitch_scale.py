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
        (edo31, [13, 39, 48, 65], [3, 8, 11, 13])
    ]
)

def test_get_bi_normalized(tuning, pi_list, n_pi_list):

    pitches = [
        tuning.pitch(pi) for pi in pi_list
    ]
    scale = PeriodicPitchScale(
        tuning, pitches
    )
    normalized = scale.get_bi_normalized()
    for i, n_pi in enumerate(n_pi_list):
        normalized[i] == tuning.pitch(n_pi)


@pytest.mark.parametrize(
    'tuning, pi_list, n_pi_list',
    [
        (edo12, [7, 12, 19, 24], [1, 2, 3, 4, 5, 6, 8, 9, 10, 11]),
        (edo12, [0, 2, 4, 17, 7, 13, 11], [1, 3, 6, 8, 10])
    ]
)

def test_get_bi_normalized_complement(tuning, pi_list, n_pi_list):

    pitches = [
        tuning.pitch(pi) for pi in pi_list
    ]
    scale = PeriodicPitchScale(
        edo12, pitches
    )
    normalized = scale.get_bi_normalized_complement()
    for i, n_pi in enumerate(n_pi_list):
        normalized[i] == tuning.pitch(n_pi)


@pytest.mark.parametrize(
    'tuning, original_pi, inverted_pi',
    [
        (edo12, [2, 5, 9], [5, 9, 14]),
        (edo31, [5, 18, 28], [18, 28, 36]),
        (edo12, [2, 5, 13], [5, 13, 14]),
    ]
)
def test_inverted_up(tuning, original_pi, inverted_pi):

    pitches = [
        tuning.pitch(pi) for pi in original_pi
    ]
    scale = tuning.pitch_scale(
        pitches
    )
    inverted = scale.inverted_up()
    for i, pi in enumerate(inverted_pi):
        inverted[i] == tuning.pitch(pi)


@pytest.mark.parametrize(
    'tuning, original_pi, inverted_pi',
    [
        (edo12, [5, 9, 14], [2, 5, 9]),
        (edo31, [18, 28, 36], [5, 18, 28]),
        (edo12, [5, 13, 14], [2, 5, 13]),
        (edo12, [14, 19, 28], [4, 14, 19]),
    ]
)
def test_inverted_down(tuning, original_pi, inverted_pi):

    pitches = [
        tuning.pitch(pi) for pi in original_pi
    ]
    scale = tuning.pitch_scale(
        pitches
    )
    inverted = scale.inverted_down()
    for i, pi in enumerate(inverted_pi):
        inverted[i] == tuning.pitch(pi)


@pytest.mark.parametrize(
    'tuning, original_pi, order, inverted_pi',
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
        (edo12, [24, 29, 38], -2, [17, 22, 24]),
    ]
)
def test_inversion(tuning, original_pi, order, inverted_pi):

    pitches = [
        tuning.pitch(pi) for pi in original_pi
    ]
    scale = tuning.pitch_scale(
        pitches
    )
    inverted = scale.inversion(order)
    for i, pi in enumerate(inverted_pi):
        inverted[i] == tuning.pitch(pi)


@pytest.mark.parametrize(
    'tuning, pitch_indices, pc_indices',
    [
        (edo12, [3, 5, 9, 15, 19, 20], [3, 5, 9, 3, 7, 8]),
        (edo31, [19, 20, 36, 51, 58], [19, 20, 5, 20, 27]),
    ]
)
def test_pc_indices(tuning, pitch_indices, pc_indices):
    pitches = [
        tuning.pitch(pi) for pi in pitch_indices
    ]
    scale = tuning.pitch_scale(pitches)
    scale.pc_indices == pc_indices


@pytest.mark.parametrize(
    'tuning',
    [
        edo12, edo24, edo31, ed13_3
    ]
)
def test_union(tuning):

    scale_a = PeriodicPitchScale(
        tuning, 
        [
            tuning.pitch(8),
            tuning.pitch(3),
            tuning.pitch(7),
        ]
    )

    scale_b = PeriodicPitchScale(
        tuning, 
        [
            tuning.pitch(8),
            tuning.pitch(5),
            tuning.pitch(7),
        ]
    )

    scale_c = scale_a.union(scale_b)

    assert len(scale_c) == 4
    pitches = list(scale_c)
    assert pitches == [
        tuning.pitch(3),
        tuning.pitch(5),
        tuning.pitch(7),
        tuning.pitch(8),
    ]


def test_union_incompatible_tunings():

    tunings = edo12, edo24, edo31, ed13_3

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
    'tuning',
    [
        edo12, edo24, edo31, ed13_3
    ]
)
def test_intersection(tuning):

    scale_a = PeriodicPitchScale(
        tuning, 
        [
            tuning.pitch(8),
            tuning.pitch(3),
            tuning.pitch(7),
        ]
    )

    scale_b = PeriodicPitchScale(
        tuning, 
        [
            tuning.pitch(8),
            tuning.pitch(5),
            tuning.pitch(7),
        ]
    )

    scale_c = scale_a.intersection(scale_b)

    assert len(scale_c) == 2
    pitches = list(scale_c)
    assert pitches == [
        tuning.pitch(7),
        tuning.pitch(8),
    ]


@pytest.mark.parametrize(
    'tuning',
    [
        edo12, edo24, edo31, ed13_3
    ]
)
def test_intersection_ignore_bi_index(tuning):

    scale_a = PeriodicPitchScale(
        tuning, 
        [
            tuning.pitch(8),
            tuning.pitch(3),
            tuning.pitch(7),
        ]
    )

    scale_b = PeriodicPitchScale(
        tuning, 
        [
            tuning.pitch(8),
            tuning.pitch(5),
            tuning.pitch(7+len(tuning)),
        ]
    )

    scale_c = scale_a.intersection(
        scale_b, ignore_bi_index=True
    )

    assert len(scale_c) == 3
    pitches = list(scale_c)
    assert pitches == [
        tuning.pitch(7),
        tuning.pitch(8),
        tuning.pitch(7+len(tuning)),
    ]


def test_intersection_incompatible_tunings():

    tunings = edo12, edo24, edo31, ed13_3

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
    'tuning',
    [
        edo12, edo24, edo31, ed13_3
    ]
)
def test_difference(tuning):

    scale_a = PeriodicPitchScale(
        tuning, 
        [
            tuning.pitch(8),
            tuning.pitch(3),
            tuning.pitch(7),
        ]
    )

    scale_b = PeriodicPitchScale(
        tuning, 
        [
            tuning.pitch(8),
            tuning.pitch(5),
            tuning.pitch(7),
        ]
    )

    scale_c = scale_a.difference(scale_b)

    assert len(scale_c) == 1
    pitches = list(scale_c)
    assert pitches == [
        tuning.pitch(3),
    ]


@pytest.mark.parametrize(
    'tuning',
    [
        edo12, edo24, edo31, ed13_3
    ]
)
def test_difference_ignore_bi_index(tuning):

    scale_a = PeriodicPitchScale(
        tuning, 
        [
            tuning.pitch(8),
            tuning.pitch(3),
            tuning.pitch(7),
        ]
    )

    scale_b = PeriodicPitchScale(
        tuning, 
        [
            tuning.pitch(8+len(tuning)),
            tuning.pitch(5),
            tuning.pitch(7+len(tuning)),
        ]
    )

    scale_c = scale_a.difference(
        scale_b, ignore_bi_index=True
    )

    assert len(scale_c) == 1
    pitches = list(scale_c)
    assert pitches == [
        tuning.pitch(3),
    ]


def test_difference_incompatible_tunings():

    tunings = edo12, edo24, edo31, ed13_3

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
    'tuning',
    [
        edo12, edo24, edo31, ed13_3
    ]
)
def test_symmetric_difference(tuning):

    scale_a = PeriodicPitchScale(
        tuning, 
        [
            tuning.pitch(8),
            tuning.pitch(3),
            tuning.pitch(7),
        ]
    )

    scale_b = PeriodicPitchScale(
        tuning, 
        [
            tuning.pitch(8),
            tuning.pitch(5),
            tuning.pitch(7),
        ]
    )

    scale_c = scale_a.symmetric_difference(scale_b)

    assert len(scale_c) == 2
    pitches = list(scale_c)
    assert pitches == [
        tuning.pitch(3),
        tuning.pitch(5),
    ]


@pytest.mark.parametrize(
    'tuning',
    [
        edo12, edo24, edo31, ed13_3
    ]
)
def test_symmetric_difference_ignore_bi_index(tuning):

    scale_a = PeriodicPitchScale(
        tuning, 
        [
            tuning.pitch(8),
            tuning.pitch(3),
            tuning.pitch(4),
            tuning.pitch(7),
        ]
    )

    scale_b = PeriodicPitchScale(
        tuning, 
        [
            tuning.pitch(8),
            tuning.pitch(5),
            tuning.pitch(7),
            tuning.pitch(3+len(tuning)),
        ]
    )

    scale_c = scale_a.symmetric_difference(
        scale_b, ignore_bi_index=True
    )

    assert len(scale_c) == 2
    pitches = list(scale_c)
    assert pitches == [
        tuning.pitch(4),
        tuning.pitch(5),
    ]


def test_symmetric_difference_incompatible_tunings():

    tunings = edo12, edo24, edo31, ed13_3

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
    'tuning',
    [
        edo12, edo24, edo31, ed13_3
    ]
)
def test_is_disjoint(tuning):

    scale_a = PeriodicPitchScale(
        tuning, 
        [
            tuning.pitch(8),
            tuning.pitch(3),
            tuning.pitch(7),
        ]
    )

    scale_b = PeriodicPitchScale(
        tuning, 
        [
            tuning.pitch(8),
            tuning.pitch(5),
            tuning.pitch(7),
        ]
    )

    scale_c = PeriodicPitchScale(
        tuning, 
        [
            tuning.pitch(1),
            tuning.pitch(5),
            tuning.pitch(9),
        ]
    )

    assert scale_a.is_disjoint(scale_c)
    assert scale_c.is_disjoint(scale_a)
    assert not scale_a.is_disjoint(scale_b)
    assert not scale_b.is_disjoint(scale_a)


@pytest.mark.parametrize(
    'tuning',
    [
        edo12, edo24, edo31, ed13_3
    ]
)
def test_is_disjoint_ignore_bi_index(tuning):

    scale_a = PeriodicPitchScale(
        tuning, 
        [
            tuning.pitch(8),
            tuning.pitch(3),
            tuning.pitch(7),
        ]
    )

    scale_b = PeriodicPitchScale(
        tuning, 
        [
            tuning.pitch(8),
            tuning.pitch(5),
            tuning.pitch(7),
        ]
    )

    scale_c = PeriodicPitchScale(
        tuning, 
        [
            tuning.pitch(1),
            tuning.pitch(5),
            tuning.pitch(9),
        ]
    )

    scale_d = PeriodicPitchScale(
        tuning, 
        [
            tuning.pitch(8+2*len(tuning)),
            tuning.pitch(9),
            tuning.pitch(7+len(tuning)),
        ]
    )

    assert scale_a.is_disjoint(
        scale_c,
        ignore_bi_index=True
    )
    assert scale_c.is_disjoint(
        scale_a,
        ignore_bi_index=True
    )
    assert not scale_a.is_disjoint(
        scale_b,
        ignore_bi_index=True
    )
    assert not scale_b.is_disjoint(
        scale_a,
        ignore_bi_index=True
    )
    assert not scale_a.is_disjoint(
        scale_d,
        ignore_bi_index=True
    )
    assert not scale_d.is_disjoint(
        scale_a,
        ignore_bi_index=True
    )


def test_is_disjoint_incompatible_tunings():

    tunings = edo12, edo24, edo31, ed13_3

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
    'tuning',
    [
        edo12, edo24, edo31, ed13_3
    ]
)
def test_is_equivalent(tuning):

    scale_a = PeriodicPitchScale(
        tuning, 
        [
            tuning.pitch(8),
            tuning.pitch(5),
            tuning.pitch(7),
        ]
    )

    scale_b = PeriodicPitchScale(
        tuning, 
        [
            tuning.pitch(8),
            tuning.pitch(5+len(tuning)),
            tuning.pitch(7+2*len(tuning)),
        ]
    )

    scale_c = PeriodicPitchScale(
        tuning, 
        [
            tuning.pitch(8),
            tuning.pitch(5+len(tuning)),
            tuning.pitch(8+2*len(tuning)),
        ]
    )

    assert scale_a.is_equivalent(scale_b)
    assert scale_b.is_equivalent(scale_a)
    assert not scale_a.is_equivalent(scale_c)
    assert not scale_b.is_equivalent(scale_c)
    assert not scale_c.is_equivalent(scale_a)
    assert not scale_c.is_equivalent(scale_b)


def test_is_equivalent_incompatible_tunings():

    tunings = edo12, edo24, edo31, ed13_3

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
    'tuning',
    [
        edo12, edo24, edo31, ed13_3
    ]
)
def test_is_subset(tuning):

    scale_a = PeriodicPitchScale(
        tuning, 
        [
            tuning.pitch(8),
            tuning.pitch(7),
        ]
    )

    scale_b = PeriodicPitchScale(
        tuning, 
        [
            tuning.pitch(8),
            tuning.pitch(5),
            tuning.pitch(7),
        ]
    )

    assert scale_a.is_subset(scale_b)
    assert not scale_b.is_subset(scale_a)
    assert scale_a.is_subset(scale_a)
    assert not scale_a.is_subset(scale_a, proper=True)


@pytest.mark.parametrize(
    'tuning',
    [
        edo12, edo24, edo31, ed13_3
    ]
)
def test_is_subset_ignore_bi_index(tuning):

    scale_a = PeriodicPitchScale(
        tuning, 
        [
            tuning.pitch(8),
            tuning.pitch(7),
        ]
    )

    scale_b = PeriodicPitchScale(
        tuning, 
        [
            tuning.pitch(8),
            tuning.pitch(5),
            tuning.pitch(7+len(tuning)),
        ]
    )

    assert scale_a.is_subset(
        scale_b, ignore_bi_index=True
    )
    assert not scale_b.is_subset(
        scale_a, ignore_bi_index=True
    )
    assert scale_a.is_subset(
        scale_a, ignore_bi_index=True
    )
    assert not scale_a.is_subset(
        scale_a, 
        ignore_bi_index=True,
        proper=True
    )


def test_is_subset_incompatible_tunings():

    tunings = edo12, edo24, edo31, ed13_3

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
    'tuning',
    [
        edo12, edo24, edo31, ed13_3
    ]
)
def test_is_superset(tuning):

    scale_a = PeriodicPitchScale(
        tuning, 
        [
            tuning.pitch(8),
            tuning.pitch(5),
            tuning.pitch(7),
        ]
    )

    scale_b = PeriodicPitchScale(
        tuning, 
        [
            tuning.pitch(8),
            tuning.pitch(7),
        ]
    )

    assert scale_a.is_superset(scale_b)
    assert not scale_b.is_superset(scale_a)
    assert scale_a.is_superset(scale_a)
    assert not scale_a.is_superset(scale_a, proper=True)


@pytest.mark.parametrize(
    'tuning',
    [
        edo12, edo24, edo31, ed13_3
    ]
)
def test_is_superset_ignore_bi_index(tuning):

    scale_a = PeriodicPitchScale(
        tuning, 
        [
            tuning.pitch(8),
            tuning.pitch(5),
            tuning.pitch(7+len(tuning)),
        ]
    )

    scale_b = PeriodicPitchScale(
        tuning, 
        [
            tuning.pitch(8),
            tuning.pitch(7),
        ]
    )

    assert scale_a.is_superset(
        scale_b, ignore_bi_index=True
    )
    assert not scale_b.is_superset(
        scale_a, ignore_bi_index=True
    )
    assert scale_a.is_superset(
        scale_a, ignore_bi_index=True
    )
    assert not scale_a.is_superset(
        scale_a, 
        ignore_bi_index=True,
        proper=True
    )


def test_is_superset_incompatible_tunings():

    tunings = edo12, edo24, edo31, ed13_3

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
