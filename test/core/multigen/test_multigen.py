import pytest
from xenharmlib.core.lattice import Lattice
from xenharmlib.exc import IncompatibleOriginContexts
from xenharmlib.exc import InvalidIndexMask
from xenharmlib.core.utils import componentwise
from xenharmlib.core.utils import scalar_op
from xenharmlib.core.frequencies import Hz440C0
from xenharmlib.core.frequencies import FrequencyRatio
from xenharmlib.core.multigen import MultiGenTuning

multigen_23 = MultiGenTuning(
    (FrequencyRatio(2), FrequencyRatio(3)), (1, 0)
)

multigen_25 = MultiGenTuning(
    (FrequencyRatio(2), FrequencyRatio(5)), (1, 0)
)

multigen_235 = MultiGenTuning(
    (FrequencyRatio(2), FrequencyRatio(3), FrequencyRatio(5)), (1, 0, 0)
)

multigen_257 = MultiGenTuning(
    (FrequencyRatio(2), FrequencyRatio(5), FrequencyRatio(7)), (1, 0, 0)
)


def test_incompatible_period_vec():
    """
    Test if dimensionality of period vec is checked
    """

    with pytest.raises(ValueError) as excinfo:
        MultiGenTuning(
            (FrequencyRatio(2), FrequencyRatio(5)), (1, 0, 0)
        )
    assert (
        excinfo.value.args[0] ==
        'Period vector must have the same dimensions '
        'as the generator vector'
    )

    with pytest.raises(ValueError) as excinfo:
        MultiGenTuning(
            (FrequencyRatio(2), FrequencyRatio(5), FrequencyRatio(7)), (1, 0)
        )
    assert (
        excinfo.value.args[0] ==
        'Period vector must have the same dimensions '
        'as the generator vector'
    )


@pytest.mark.parametrize(
    'tuning',
    [multigen_23, multigen_25, multigen_235, multigen_257]
)
def test_incompatible_lattice(tuning):
    """
    Test if points from different lattices are not
    accepted as pitch index or index diffs
    """

    lattice = Lattice((FrequencyRatio(9), FrequencyRatio(31)))

    with pytest.raises(ValueError) as excinfo:
        tuning.pitch(lattice.point((1, 2)))
    assert (
        excinfo.value.args[0] ==
        'Pitch index must be a lattice point from the '
        'same lattice as this tuning was configured with.'
    )

    with pytest.raises(ValueError) as excinfo:
        tuning.diff_interval(lattice.point((1, 2)))
    assert (
        excinfo.value.args[0] ==
        'Pitch difference must be a lattice point from the '
        'same lattice as this tuning was configured with.'
    )

    with pytest.raises(ValueError) as excinfo:
        tuning.index_scale([lattice.point((1, 2)), lattice.point((2, 3))])
    assert (
        excinfo.value.args[0] ==
        'Pitch index must be a lattice point from the '
        'same lattice as this tuning was configured with.'
    )

    with pytest.raises(ValueError) as excinfo:
        tuning.diff_interval_seq(
            [lattice.point((1, 2)), lattice.point((2, 3))]
        )
    assert (
        excinfo.value.args[0] ==
        'Pitch difference must be a lattice point from the '
        'same lattice as this tuning was configured with.'
    )


@pytest.mark.parametrize(
    'tuning, name',
    [
        (
            multigen_23,
            'MultiGenTuning(2, 3)'
        ),
        (
            multigen_257,
            'MultiGenTuning(2, 5, 7)'
        )
    ]
)
def test_tuning_name(tuning, name):
    """
    Test if name property returns correct result
    """

    assert tuning.name == name


@pytest.mark.parametrize(
    'tuning, name',
    [
        (
            multigen_23,
            'MultiGenTuning(2, 3)'
        ),
        (
            multigen_257,
            'MultiGenTuning(2, 5, 7)'
        )
    ]
)
def test_repr(tuning, name):
    """
    Test if __repr__ returns correct result
    """

    assert repr(tuning) == name


@pytest.mark.parametrize(
    'tuning, vec',
    [
        (multigen_23, (2, 3)),
        (multigen_23, (-3, -3)),
        (multigen_23, (-1, 0)),
        (multigen_23, (0, 0)),
        (multigen_257, (0, 2, -1)),
        (multigen_257, (3, -1, -1)),
        (multigen_257, (1, 0, -1)),
        (multigen_257, (-1, 2, 1)),
    ]
)
def test_vec_pitch(tuning, vec):
    """
    Test if vec_pitch works correctly
    """

    pitch = tuning.vec_pitch(vec)
    expected_pitch = tuning.pitch(
        tuning.lattice.point(vec)
    )
    assert pitch == expected_pitch
    assert pitch.pitch_index == tuning.lattice.point(vec)


@pytest.mark.parametrize(
    'tuning, vec',
    [
        (multigen_23, (2, 3)),
        (multigen_23, (-3, -3)),
        (multigen_23, (-1, 0)),
        (multigen_23, (0, 0)),
        (multigen_257, (0, 2, -1)),
        (multigen_257, (3, -1, -1)),
        (multigen_257, (1, 0, -1)),
        (multigen_257, (-1, 2, 1)),
    ]
)
def test_vec_interval(tuning, vec):
    """
    Test if vec_interval works correctly
    """

    interval = tuning.vec_interval(vec)
    expected_interval = tuning.diff_interval(
        tuning.lattice.point(vec)
    )
    assert interval == expected_interval
    assert interval.pitch_diff == tuning.lattice.point(vec)


@pytest.mark.parametrize(
    'tuning, vecs',
    [
        (
            multigen_23,
            [(0, -3), (5, -6), (-6, 1), (-1, -2), (-7, 2)],
        ),
        (
            multigen_235,
            [(-1, 0, -1), (0, -2, 0), (1, -1, -1), (-1, -1, 0)],
        )
    ]
)
def test_vec_scale(tuning, vecs):
    """
    Test if vec_scale works correctly
    """

    scale = tuning.vec_scale(vecs)
    expected_scale = tuning.index_scale(
        [tuning.lattice.point(vec) for vec in vecs]
    )
    assert scale == expected_scale
    assert scale.pitch_indices == [tuning.lattice.point(vec) for vec in vecs]


@pytest.mark.parametrize(
    'tuning, vecs',
    [
        (
            multigen_23,
            [(0, -3), (5, -6), (-6, 1), (-1, -2), (-7, 2)],
        ),
        (
            multigen_235,
            [(-1, 0, -1), (0, -2, 0), (1, -1, -1), (-1, -1, 0)],
        )
    ]
)
def test_vec_seq(tuning, vecs):
    """
    Test if vec_seq works correctly
    """

    seq = tuning.vec_seq(vecs)
    expected_seq = tuning.index_seq(
        [tuning.lattice.point(vec) for vec in vecs]
    )
    assert seq == expected_seq
    assert seq.pitch_indices == [tuning.lattice.point(vec) for vec in vecs]


@pytest.mark.parametrize(
    'tuning',
    [multigen_23, multigen_25, multigen_235, multigen_257]
)
def test_vec_scale_empty(tuning):
    """
    Test if vec_scale works correctly with parameter omitted
    """

    scale = tuning.vec_scale()
    assert len(scale) == 0
    assert scale == tuning.scale()


@pytest.mark.parametrize(
    'tuning, vecs',
    [
        (
            multigen_23,
            [(0, -3), (5, -6), (-6, 1), (-1, -2), (-7, 2)],
        ),
        (
            multigen_235,
            [(-1, 0, -1), (0, -2, 0), (1, -1, -1), (-1, -1, 0)],
        )
    ]
)
def test_vec_interval_seq(tuning, vecs):
    """
    Test if vec_interval_seq works correctly
    """

    interval_seq = tuning.vec_interval_seq(vecs)
    expected_interval_seq = tuning.diff_interval_seq(
        [tuning.lattice.point(vec) for vec in vecs]
    )
    assert interval_seq == expected_interval_seq
    assert interval_seq.pitch_diffs == [
        tuning.lattice.point(vec) for vec in vecs
    ]


@pytest.mark.parametrize(
    'tuning',
    [multigen_23, multigen_25, multigen_235, multigen_257]
)
def test_vec_interval_seq_empty(tuning):
    """
    Test if vec_interval_seq works correctly with parameter omitted
    """

    interval_seq = tuning.vec_interval_seq()
    assert len(interval_seq) == 0
    assert interval_seq == tuning.interval_seq()


@pytest.mark.parametrize(
    'tuning, vecs',
    [
        (
            multigen_23,
            [(0, -3), (5, -6), (-6, 1), (-1, -2), (-7, 2)],
        ),
        (
            multigen_235,
            [(-1, 0, -1), (0, -2, 0), (1, -1, -1), (-1, -1, 0)],
        )
    ]
)
def test_vec_interval_fan(tuning, vecs):
    """
    Test if vec_interval_fan works correctly
    """

    interval_fan = tuning.vec_interval_fan(vecs)
    expected_interval_fan = tuning.diff_interval_fan(
        [tuning.lattice.point(vec) for vec in vecs]
    )
    assert interval_fan == expected_interval_fan
    assert interval_fan.pitch_diffs == [
        tuning.lattice.point(vec) for vec in vecs
    ]


@pytest.mark.parametrize(
    'tuning',
    [multigen_23, multigen_25, multigen_235, multigen_257]
)
def test_vec_interval_fan_empty(tuning):
    """
    Test if vec_interval_fan works correctly with parameter omitted
    """

    interval_fan = tuning.vec_interval_fan()
    assert len(interval_fan) == 0
    assert interval_fan == tuning.interval_fan()
