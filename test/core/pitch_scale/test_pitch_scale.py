import pytest
from xenharmlib.core.frequencies import Frequency
from xenharmlib.core.tunings import EDTuning
from xenharmlib.core.pitch import EDPitch
from xenharmlib.core.pitch_scale import PitchScale
from xenharmlib.exc import IncompatibleTunings

edo12 = EDTuning(12, Frequency(2))
edo24 = EDTuning(24, Frequency(2))
edo31 = EDTuning(31, Frequency(2))
ed13_3 = EDTuning(13, Frequency(3))


@pytest.mark.parametrize(
    'tuning',
    [
        edo12, edo24, edo31, ed13_3
    ]
)
def test_sort_on_init(tuning):

    scale = PitchScale(
        tuning, 
        [
            tuning.pitch(8),
            tuning.pitch(3),
            tuning.pitch(7),
        ]
    )

    assert len(scale) == 3
    pitches = list(scale)
    assert pitches == [
        tuning.pitch(3),
        tuning.pitch(7),
        tuning.pitch(8),
    ]


@pytest.mark.parametrize(
    'tuning',
    [
        edo12, edo24, edo31, ed13_3
    ]
)
def test_init_empty(tuning):

    scale = PitchScale(tuning)

    assert len(scale) == 0
    pitches = list(scale)
    assert pitches == []


@pytest.mark.parametrize(
    'tuning',
    [
        edo12, edo24, edo31, ed13_3
    ]
)
def test_add_pitch(tuning):

    scale = PitchScale(
        tuning, 
        [
            tuning.pitch(8),
            tuning.pitch(3),
            tuning.pitch(7),
        ]
    )

    scale.add_pitch(
        tuning.pitch(4)
    )

    assert len(scale) == 4
    pitches = list(scale)
    assert pitches == [
        tuning.pitch(3),
        tuning.pitch(4),
        tuning.pitch(7),
        tuning.pitch(8),
    ]


def test_add_pitch_incompatible_tunings():

    tunings = edo12, edo24, edo31, ed13_3

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
    'tuning',
    [
        edo12, edo24, edo31, ed13_3
    ]
)
def test_add_pitch(tuning):

    scale = PitchScale(
        tuning, 
        [
            tuning.pitch(8),
            tuning.pitch(3),
            tuning.pitch(7),
        ]
    )

    scale.add_pitch_index(4)

    assert len(scale) == 4
    pitches = list(scale)
    assert pitches == [
        tuning.pitch(3),
        tuning.pitch(4),
        tuning.pitch(7),
        tuning.pitch(8),
    ]


@pytest.mark.parametrize(
    'tuning',
    [
        edo12, edo24, edo31, ed13_3
    ]
)
def test_from_pitch_indices(tuning):

    scale = PitchScale.from_pitch_indices(
        [8, 3, 7], tuning=tuning
    )

    assert len(scale) == 3
    pitches = list(scale)
    assert pitches == [
        tuning.pitch(3),
        tuning.pitch(7),
        tuning.pitch(8),
    ]


def test_eq():

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

    assert scale_a == scale_a
    assert scale_a == scale_b
    assert scale_a != scale_c
    assert scale_a != scale_d
    assert 'XYZ' != scale_a
    assert 3 != scale_a
    assert scale_a != 'XYZ'
    assert scale_a != 3


@pytest.mark.parametrize(
    'tuning',
    [
        edo12, edo24, edo31, ed13_3
    ]
)
def test_getitem(tuning):

    scale = PitchScale(
        tuning, 
        [
            tuning.pitch(8),
            tuning.pitch(3),
            tuning.pitch(7),
        ]
    )

    assert scale[0] == tuning.pitch(3)
    assert scale[1] == tuning.pitch(7)
    assert scale[2] == tuning.pitch(8)


@pytest.mark.parametrize(
    'tuning',
    [
        edo12, edo24, edo31, ed13_3
    ]
)
def test_getitem_slice(tuning):

    scale = tuning.pitch_scale(
        [
            tuning.pitch(8),
            tuning.pitch(3),
            tuning.pitch(7),
        ]
    )

    scale_b = tuning.pitch_scale(
        [
            tuning.pitch(3),
            tuning.pitch(7),
        ]
    )

    assert scale[0:2] == scale_b


@pytest.mark.parametrize(
    'tuning',
    [
        edo12, edo24, edo31, ed13_3
    ]
)
def test_in_operator_pitch(tuning):

    scale = PitchScale(
        tuning, 
        [
            tuning.pitch(8),
            tuning.pitch(3),
            tuning.pitch(7),
        ]
    )

    assert tuning.pitch(3) in scale
    assert tuning.pitch(7) in scale
    assert tuning.pitch(8) in scale


@pytest.mark.parametrize(
    'tuning',
    [
        edo12, edo24, edo31, ed13_3
    ]
)
def test_in_operator_interval(tuning):

    scale = PitchScale(
        tuning, 
        [
            tuning.pitch(8),
            tuning.pitch(3),
            tuning.pitch(7),
        ]
    )

    interval1 = tuning.pitch(0).interval(
        tuning.pitch(4)
    )
    interval2 = tuning.pitch(0).interval(
        tuning.pitch(1)
    )
    interval3 = tuning.pitch(0).interval(
        tuning.pitch(2)
    )

    assert interval1 in scale
    assert interval2 in scale
    assert interval3 not in scale


@pytest.mark.parametrize(
    'tuning',
    [
        edo12, edo31, ed13_3
    ]
)
def test_in_operator_bogus(tuning):

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
    assert edo24.pitch(8) not in scale


@pytest.mark.parametrize(
    'tuning',
    [
        edo12, edo24, edo31, ed13_3
    ]
)
def test_repr(tuning):

    scale = PitchScale(
        tuning,
        [
            tuning.pitch(8),
            tuning.pitch(3),
            tuning.pitch(7),
        ]
    )
    assert repr(scale) == (
        f'PitchScale([3, 7, 8], {tuning.name})'
    )


@pytest.mark.parametrize(
    'tuning',
    [
        edo12, edo24, edo31, ed13_3
    ]
)
def test_frequencies(tuning):

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
    'tuning',
    [
        edo12, edo24, edo31, ed13_3
    ]
)
def test_pitch_indices(tuning):

    scale = PitchScale(
        tuning, 
        [
            tuning.pitch(8),
            tuning.pitch(3),
            tuning.pitch(7),
        ]
    )

    assert scale.pitch_indices == [3, 7, 8]


@pytest.mark.parametrize(
    'tuning',
    [
        edo12, edo24, edo31, ed13_3
    ]
)
def test_to_pitch_intervals(tuning):

    scale = PitchScale(
        tuning, 
        [
            tuning.pitch(8),
            tuning.pitch(3),
            tuning.pitch(7),
        ]
    )

    interval1 = tuning.pitch_interval(
        tuning.pitch(3), tuning.pitch(7)
    )
    interval2 = tuning.pitch_interval(
        tuning.pitch(7), tuning.pitch(8)
    )

    assert scale.to_pitch_intervals() == [
        interval1, interval2
    ]


@pytest.mark.parametrize(
    'tuning',
    [
        edo12, edo24, edo31, ed13_3
    ]
)
def test_transpose_int(tuning):

    scale = PitchScale(
        tuning, 
        [
            tuning.pitch(8),
            tuning.pitch(3),
            tuning.pitch(7),
        ]
    )

    transposed_up = scale.transpose(9)
    assert transposed_up == tuning.pitch_scale(
        [
            tuning.pitch(12),
            tuning.pitch(17),
            tuning.pitch(16),
        ]
    )

    transposed_down = scale.transpose(-3)
    assert transposed_down == tuning.pitch_scale(
        [
            tuning.pitch(0),
            tuning.pitch(4),
            tuning.pitch(5),
        ]
    )


def test_retune():

    edo12_scale = edo12.pitch_scale(
        edo12.pitch_range(12)
    )

    edo31_scale = edo12_scale.retune(edo31)

    assert edo31_scale[0] == edo31.pitch(0)
    assert edo31_scale[1] == edo31.pitch(3)
    assert edo31_scale[2] == edo31.pitch(5)
    assert edo31_scale[3] == edo31.pitch(8)
    assert edo31_scale[4] == edo31.pitch(10)
    assert edo31_scale[5] == edo31.pitch(13)
    assert edo31_scale[6] == edo31.pitch(15)
    assert edo31_scale[7] == edo31.pitch(18)
    assert edo31_scale[8] == edo31.pitch(21)
    assert edo31_scale[9] == edo31.pitch(23)
    assert edo31_scale[10] == edo31.pitch(26)
    assert edo31_scale[11] == edo31.pitch(28)


@pytest.mark.parametrize(
    'tuning',
    [
        edo12, edo24, edo31, ed13_3
    ]
)
def test_union(tuning):

    scale_a = PitchScale(
        tuning, 
        [
            tuning.pitch(8),
            tuning.pitch(3),
            tuning.pitch(7),
        ]
    )

    scale_b = PitchScale(
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

            scale_a = PitchScale(
                tuning_a
            )
            scale_b = PitchScale(
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

    scale_a = PitchScale(
        tuning, 
        [
            tuning.pitch(8),
            tuning.pitch(3),
            tuning.pitch(7),
        ]
    )

    scale_b = PitchScale(
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


def test_intersection_incompatible_tunings():

    tunings = edo12, edo24, edo31, ed13_3

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
    'tuning',
    [
        edo12, edo24, edo31, ed13_3
    ]
)
def test_difference(tuning):

    scale_a = PitchScale(
        tuning, 
        [
            tuning.pitch(8),
            tuning.pitch(3),
            tuning.pitch(7),
        ]
    )

    scale_b = PitchScale(
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


def test_difference_incompatible_tunings():

    tunings = edo12, edo24, edo31, ed13_3

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
    'tuning',
    [
        edo12, edo24, edo31, ed13_3
    ]
)
def test_symmetric_difference(tuning):

    scale_a = PitchScale(
        tuning, 
        [
            tuning.pitch(8),
            tuning.pitch(3),
            tuning.pitch(7),
        ]
    )

    scale_b = PitchScale(
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


def test_symmetric_difference_incompatible_tunings():

    tunings = edo12, edo24, edo31, ed13_3

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
    'tuning',
    [
        edo12, edo24, edo31, ed13_3
    ]
)
def test_is_disjoint(tuning):

    scale_a = PitchScale(
        tuning, 
        [
            tuning.pitch(8),
            tuning.pitch(3),
            tuning.pitch(7),
        ]
    )

    scale_b = PitchScale(
        tuning, 
        [
            tuning.pitch(8),
            tuning.pitch(5),
            tuning.pitch(7),
        ]
    )

    scale_c = PitchScale(
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


def test_is_disjoint_incompatible_tunings():

    tunings = edo12, edo24, edo31, ed13_3

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
    'tuning',
    [
        edo12, edo24, edo31, ed13_3
    ]
)
def test_is_subset(tuning):

    scale_a = PitchScale(
        tuning, 
        [
            tuning.pitch(8),
            tuning.pitch(7),
        ]
    )

    scale_b = PitchScale(
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


def test_is_subset_incompatible_tunings():

    tunings = edo12, edo24, edo31, ed13_3

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
    'tuning',
    [
        edo12, edo24, edo31, ed13_3
    ]
)
def test_is_superset(tuning):

    scale_a = PitchScale(
        tuning, 
        [
            tuning.pitch(8),
            tuning.pitch(5),
            tuning.pitch(7),
        ]
    )

    scale_b = PitchScale(
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


def test_is_superset_incompatible_tunings():

    tunings = edo12, edo24, edo31, ed13_3

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