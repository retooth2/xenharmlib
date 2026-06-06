import operator
import sympy as sp
import pytest
from xenharmlib import EDTuning
from xenharmlib import EDOTuning
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

multigen_weird = MultiGenTuning(
    (
        FrequencyRatio(sp.Integer(2) ** sp.Rational(1, 2)),
        FrequencyRatio(7),
        FrequencyRatio(11),
    ),
    (0, 1, 0)
)


@pytest.mark.parametrize(
    'tuning',
    [
        multigen_23, multigen_25, multigen_235, multigen_257, multigen_weird
    ]
)
def test_init_empty(tuning):
    """
    Test if interval sequence can be created by omitting intervals parameter
    """

    interval_seq = tuning.interval_seq()

    assert len(interval_seq) == 0
    intervals = list(interval_seq)
    assert intervals == []

    interval_seq = tuning.interval_seq()

    assert len(interval_seq) == 0
    intervals = list(interval_seq)
    assert intervals == []


def test_init_incompatible_origin_contexts():
    """
    Test if correct exception is raised when interval from
    different origin context is given to constructor
    """

    with pytest.raises(IncompatibleOriginContexts):
        multigen_257.interval_seq(
            [multigen_235.diff_interval(multigen_235.lattice.point((0, 0, 0)))]
        )

    with pytest.raises(IncompatibleOriginContexts):
        multigen_weird.interval_seq(
            [multigen_235.diff_interval(multigen_235.lattice.point((0, 0, 0)))]
        )


@pytest.mark.parametrize(
    'tuning, diff_vecs, new_diff_vec, result_vecs',
    [
        (
            multigen_23,
            [(0, 1), (-1, 1), (-7, 11)],
            (-1, 1),
            [(0, 1), (-1, 1), (-7, 11), (-1, 1)],
        ),
        (
            multigen_235,
            [(0, 1, 2), (-1, 1, 3), (-7, 11, 4)],
            (-1, 0, 3),
            [(0, 1, 2), (-1, 1, 3), (-7, 11, 4), (-1, 0, 3)],
        ),
        (
            multigen_weird,
            [(0, 1, 2), (-1, 1, 3), (-7, 11, 4)],
            (-1, 0, 0),
            [(0, 1, 2), (-1, 1, 3), (-7, 11, 4), (-1, 0, 0)],
        ),
    ]
)
def test_with_interval(tuning, diff_vecs, new_diff_vec, result_vecs):
    """
    Test if with_interval works
    """

    interval_seq = tuning.interval_seq(
        [tuning.diff_interval(tuning.lattice.point(diff))
         for diff in diff_vecs]
    )

    interval_seq = interval_seq.with_interval(
        tuning.diff_interval(tuning.lattice.point(new_diff_vec))
    )

    assert len(interval_seq) == len(result_vecs)
    intervals = list(interval_seq)
    assert intervals == [
        tuning.diff_interval(tuning.lattice.point(diff))
        for diff in result_vecs
    ]


@pytest.mark.parametrize(
    'tuning, diff_vecs, new_diff_vec, insert_pos, result_vecs',
    [
        (
            multigen_23,
            [(0, 1), (-1, 1), (-7, 11)],
            (-1, 1),
            0,
            [(-1, 1), (0, 1), (-1, 1), (-7, 11)],
        ),
        (
            multigen_235,
            [(0, 1, 2), (-1, 1, 3), (-7, 11, 4)],
            (-1, 0, 3),
            2,
            [(0, 1, 2), (-1, 1, 3), (-1, 0, 3), (-7, 11, 4)],
        ),
        (
            multigen_weird,
            [(0, 1, 2), (-1, 1, 3), (-7, 11, 4)],
            (-1, 0, 0),
            10,
            [(0, 1, 2), (-1, 1, 3), (-7, 11, 4), (-1, 0, 0)],
        ),
        (
            multigen_weird,
            [(0, 1, 2), (-1, 1, 3), (-7, 11, 4)],
            (-1, 0, 0),
            -2,
            [(0, 1, 2), (-1, 0, 0), (-1, 1, 3), (-7, 11, 4)],
        ),
    ]
)
def test_with_interval_insert_pos(
    tuning, diff_vecs, new_diff_vec, insert_pos, result_vecs
):
    """
    Test if with_interval works
    """

    interval_seq = tuning.interval_seq(
        [tuning.diff_interval(tuning.lattice.point(diff))
         for diff in diff_vecs]
    )

    interval_seq = interval_seq.with_interval(
        tuning.diff_interval(tuning.lattice.point(new_diff_vec)),
        insert_pos
    )

    assert len(interval_seq) == len(result_vecs)
    intervals = list(interval_seq)
    assert intervals == [
        tuning.diff_interval(tuning.lattice.point(diff))
        for diff in result_vecs
    ]


def test_with_interval_incompatible_origin_contexts():
    """
    Test if with_interval raises IncompatibleOriginContexts if argument
    originates from a different tuning
    """

    edo12_2 = EDTuning(12, FrequencyRatio(2))
    tunings = edo12_2, multigen_weird, multigen_235, multigen_25

    for i, tuning_a in enumerate(tunings):

        for tuning_b in tunings[i+1:]:

            interval_seq = tuning_a.interval_seq()

            with pytest.raises(IncompatibleOriginContexts):
                interval_seq.with_interval(
                    tuning_b.diff_interval(
                        tuning_b.zero_index
                    )
                )


def test_eq():
    """
    Test if interval_seq equalities and inequalities work correctly
    """

    interval_seq_a = multigen_23.diff_interval_seq(
        [multigen_23.lattice.point(vec)
         for vec in [(7, -11), (-4, 2), (-1, 1)]]
    )
    interval_seq_b = multigen_23.diff_interval_seq(
        [multigen_23.lattice.point(vec)
         for vec in [(7, -11), (-4, 2), (-1, 1)]]
    )
    interval_seq_c = multigen_23.diff_interval_seq(
        [multigen_23.lattice.point(vec)
         for vec in [(7, -11), (-4, 2), (-1, 1), (1, 0)]]
    )

    interval_seq_d = multigen_weird.diff_interval_seq(
        [multigen_weird.lattice.point(vec)
         for vec in [(7, -11, 0), (-4, 2, 0), (-1, 1, 0)]]
    )
    interval_seq_e = multigen_235.diff_interval_seq(
        [multigen_235.lattice.point(vec)
         for vec in [(7, -11, 0), (-4, 2, 0), (-1, 1, 0)]]
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
    'tuning, diff_vecs',
    [
        (multigen_235, [(0, 0, 0), (-11, 7, 0), (-3, 2, 0), (-6, 4, 0)]),
        (multigen_23, [(-11, 7), (-3, 2), (-6, 4), (-1, 1)]),
        (multigen_weird, [(-1, 0, 0), (0, 0, 1), (11, 0, 0), (0, 2, 0)]),
    ]
)
def test_getitem(tuning, diff_vecs):
    """
    Test if fetching single interval items works correctly
    """

    interval_seq = tuning.diff_interval_seq(
        [tuning.lattice.point(vec) for vec in diff_vecs]
    )

    for i, vec in enumerate(diff_vecs):
        assert interval_seq[i] == tuning.diff_interval(
            tuning.lattice.point(vec)
        )


@pytest.mark.parametrize(
    'tuning, diff_vecs, start, stop, result_vecs',
    [
        (
            multigen_235,
            [(0, 0, 0), (-11, 7, 0), (-3, 2, 0), (-6, 4, 0)],
            0, 2,
            [(0, 0, 0), (-11, 7, 0)]
        ),
        (
            multigen_23,
            [(-11, 7), (-3, 2), (-6, 4), (-1, 1)],
            1, 3,
            [(-3, 2), (-6, 4)],
        ),
        (
            multigen_weird,
            [(-1, 0, 0), (0, 0, 1), (11, 0, 0), (0, 2, 0)],
            1, -1,
            [(0, 0, 1), (11, 0, 0)],
        ),
        (
            multigen_weird,
            [(-1, 0, 0), (0, 0, 1), (11, 0, 0), (0, 2, 0)],
            -4, -1,
            [(-1, 0, 0), (0, 0, 1), (11, 0, 0)],
        ),
    ]
)
def test_getitem_slice(tuning, diff_vecs, start, stop, result_vecs):
    """
    Test if slicing of interval sequences works correctly
    """

    interval_seq = tuning.diff_interval_seq(
        [tuning.lattice.point(vec) for vec in diff_vecs]
    )
    result_interval_seq = tuning.diff_interval_seq(
        [tuning.lattice.point(vec) for vec in result_vecs]
    )

    for i, vec in enumerate(diff_vecs):
        assert interval_seq[i] == tuning.diff_interval(
            tuning.lattice.point(vec)
        )

    assert interval_seq[start:stop] == result_interval_seq


@pytest.mark.parametrize(
    'tuning, diff_vecs, start, result_vecs',
    [
        (
            multigen_235,
            [(0, 0, 0), (-11, 7, 0), (-3, 2, 0), (-6, 4, 0)],
            0,
            [(0, 0, 0), (-11, 7, 0), (-3, 2, 0), (-6, 4, 0)],
        ),
        (
            multigen_23,
            [(-11, 7), (-3, 2), (-6, 4), (-1, 1)],
            1,
            [(-3, 2), (-6, 4), (-1, 1)],
        ),
        (
            multigen_weird,
            [(-1, 0, 0), (0, 0, 1), (11, 0, 0), (0, 2, 0)],
            -2,
            [(11, 0, 0), (0, 2, 0)],
        ),
        (
            multigen_weird,
            [(-1, 0, 0), (0, 0, 1), (11, 0, 0), (0, 2, 0)],
            2,
            [(11, 0, 0), (0, 2, 0)],
        ),
    ]
)
def test_getitem_slice_omit_stop(tuning, diff_vecs, start, result_vecs):
    """
    Test if slicing of interval sequences works correctly when
    stop parameter is omitted
    """

    interval_seq = tuning.diff_interval_seq(
        [tuning.lattice.point(vec) for vec in diff_vecs]
    )
    result_interval_seq = tuning.diff_interval_seq(
        [tuning.lattice.point(vec) for vec in result_vecs]
    )

    for i, vec in enumerate(diff_vecs):
        assert interval_seq[i] == tuning.diff_interval(
            tuning.lattice.point(vec)
        )

    assert interval_seq[start:] == result_interval_seq


@pytest.mark.parametrize(
    'tuning, diff_vecs, stop, result_vecs',
    [
        (
            multigen_235,
            [(0, 0, 0), (-11, 7, 0), (-3, 2, 0), (-6, 4, 0)],
            0,
            [],
        ),
        (
            multigen_23,
            [(-11, 7), (-3, 2), (-6, 4), (-1, 1)],
            2,
            [(-11, 7), (-3, 2)],
        ),
        (
            multigen_weird,
            [(-1, 0, 0), (0, 0, 1), (11, 0, 0), (0, 2, 0)],
            -2,
            [(-1, 0, 0), (0, 0, 1)],
        ),
        (
            multigen_weird,
            [(-1, 0, 0), (0, 0, 1), (11, 0, 0), (0, 2, 0)],
            -3,
            [(-1, 0, 0)],
        ),
    ]
)
def test_getitem_slice_omit_start(tuning, diff_vecs, stop, result_vecs):
    """
    Test if slicing of interval sequence works correctly when
    start parameter is omitted
    """

    interval_seq = tuning.diff_interval_seq(
        [tuning.lattice.point(vec) for vec in diff_vecs]
    )
    result_interval_seq = tuning.diff_interval_seq(
        [tuning.lattice.point(vec) for vec in result_vecs]
    )

    for i, vec in enumerate(diff_vecs):
        assert interval_seq[i] == tuning.diff_interval(
            tuning.lattice.point(vec)
        )
    assert interval_seq[:stop] == result_interval_seq


@pytest.mark.parametrize(
    'tuning, diff_vecs, mask, result_vecs',
    [
        (
            multigen_235,
            [(0, 0, 0), (-11, 7, 0), (-3, 2, 0), (-6, 4, 0)],
            1,
            [(-11, 7, 0)],
        ),
        (
            multigen_235,
            [(0, 0, 0), (-11, 7, 0), (-3, 2, 0), (-6, 4, 0)],
            ...,
            [(0, 0, 0), (-11, 7, 0), (-3, 2, 0), (-6, 4, 0)],
        ),
        (
            multigen_235,
            [(0, 0, 0), (-11, 7, 0), (-3, 2, 0), (-6, 4, 0)],
            (1,),
            [(-11, 7, 0)],
        ),
        (
            multigen_235,
            [(0, 0, 0), (-11, 7, 0), (-3, 2, 0), (-6, 4, 0)],
            (...,),
            [(0, 0, 0), (-11, 7, 0), (-3, 2, 0), (-6, 4, 0)],
        ),
        (
            multigen_23,
            [(-11, 7), (-3, 2), (-6, 4), (-1, 1)],
            (1, 2),
            [(-3, 2), (-6, 4)],
        ),
        (
            multigen_23,
            [(-11, 7), (-3, 2), (-6, 4), (-1, 1)],
            (1, 2),
            [(-3, 2), (-6, 4)],
        ),
        (
            multigen_weird,
            [(-1, 0, 0), (0, 0, 1), (11, 0, 0), (0, 2, 0)],
            (1, ...),
            [(0, 0, 1), (11, 0, 0), (0, 2, 0)],
        ),
        (
            multigen_235,
            [(0, 0, 0), (-11, 7, 0), (-3, 2, 0), (-6, 4, 0), (-1, 1, 0)],
            (0, 2, 4),
            [(0, 0, 0), (-3, 2, 0), (-1, 1, 0)],
        ),
        (
            multigen_235,
            [(0, 0, 0), (-11, 7, 0), (-3, 2, 0), (-6, 4, 0), (-1, 1, 0)],
            (..., 2, 4),
            [(0, 0, 0), (-11, 7, 0), (-3, 2, 0), (-1, 1, 0)],
        ),
        (
            multigen_235,
            [(0, 0, 0), (-11, 7, 0), (-3, 2, 0), (-6, 4, 0), (-1, 1, 0)],
            (0, ..., 2, 4),
            [(0, 0, 0), (-11, 7, 0), (-3, 2, 0), (-1, 1, 0)],
        ),
        (
            multigen_235,
            [(0, 0, 0), (-11, 7, 0), (-3, 2, 0), (-6, 4, 0), (-1, 1, 0)],
            (0, 2, ..., 4),
            [(0, 0, 0), (-3, 2, 0), (-6, 4, 0), (-1, 1, 0)],
        ),
        (
            multigen_235,
            [(0, 0, 0), (-11, 7, 0), (-3, 2, 0), (-6, 4, 0), (-1, 1, 0)],
            (2, ..., 100),
            [(-3, 2, 0), (-6, 4, 0), (-1, 1, 0)],
        ),
    ]
)
def test_partial(tuning, diff_vecs, mask, result_vecs):
    """
    Test if partial function of interval sequences works correctly
    """

    interval_seq = tuning.diff_interval_seq(
        [tuning.lattice.point(vec) for vec in diff_vecs]
    )
    result_interval_seq = tuning.diff_interval_seq(
        [tuning.lattice.point(vec) for vec in result_vecs]
    )

    assert interval_seq.partial(mask) == result_interval_seq


@pytest.mark.parametrize(
    'tuning, diff_vecs, mask',
    [
        (
            multigen_235,
            [(0, 0, 0), (-11, 7, 0), (-3, 2, 0), (-6, 4, 0)],
            (-1, ..., 2, 4),
        ),
        (
            multigen_235,
            [(0, 0, 0), (-11, 7, 0), (-3, 2, 0), (-6, 4, 0)],
            (..., 4, 3),
        ),
        (
            multigen_235,
            [(0, 0, 0), (-11, 7, 0), (-3, 2, 0), (-6, 4, 0)],
            (..., 4, 3, ...),
        ),
        (
            multigen_23,
            [(-11, 7), (-3, 2), (-6, 4), (-1, 1)],
            (3, 2, ...),
        ),
        (
            multigen_23,
            [(-11, 7), (-3, 2), (-6, 4), (-1, 1)],
            (1, 2, -1),
        ),
    ]
)
def test_partial_invalid_mask(tuning, diff_vecs, mask):
    """
    Test if partial function of interval sequences raises correct
    exception when invalid mask is given
    """

    interval_seq = tuning.diff_interval_seq(
        [tuning.lattice.point(vec) for vec in diff_vecs]
    )

    with pytest.raises(InvalidIndexMask):
        interval_seq.partial(mask)


@pytest.mark.parametrize(
    'tuning, diff_vecs, mask, result_vecs',
    [
        (
            multigen_235,
            [(0, 0, 0), (-11, 7, 0), (-3, 2, 0), (-6, 4, 0)],
            1,
            [(0, 0, 0), (-3, 2, 0), (-6, 4, 0)],
        ),
        (
            multigen_235,
            [(0, 0, 0), (-11, 7, 0), (-3, 2, 0), (-6, 4, 0)],
            ...,
            [],
        ),
        (
            multigen_235,
            [(0, 0, 0), (-11, 7, 0), (-3, 2, 0), (-6, 4, 0)],
            (1,),
            [(0, 0, 0), (-3, 2, 0), (-6, 4, 0)],
        ),
        (
            multigen_235,
            [(0, 0, 0), (-11, 7, 0), (-3, 2, 0), (-6, 4, 0)],
            (...,),
            [],
        ),
        (
            multigen_23,
            [(-11, 7), (-3, 2), (-6, 4), (-1, 1)],
            (1, 2),
            [(-11, 7), (-1, 1)],
        ),
        (
            multigen_weird,
            [(-1, 0, 0), (0, 0, 1), (11, 0, 0), (0, 2, 0)],
            (1, ...),
            [(-1, 0, 0)],
        ),
        (
            multigen_235,
            [(0, 0, 0), (-11, 7, 0), (-3, 2, 0), (-6, 4, 0), (-1, 1, 0)],
            (0, 2, 4),
            [(-11, 7, 0), (-6, 4, 0)],
        ),
        (
            multigen_235,
            [(0, 0, 0), (-11, 7, 0), (-3, 2, 0), (-6, 4, 0), (-1, 1, 0)],
            (..., 2, 4),
            [(-6, 4, 0)],
        ),
        (
            multigen_235,
            [(0, 0, 0), (-11, 7, 0), (-3, 2, 0), (-6, 4, 0), (-1, 1, 0)],
            (0, ..., 2, 4),
            [(-6, 4, 0)],
        ),
        (
            multigen_235,
            [(0, 0, 0), (-11, 7, 0), (-3, 2, 0), (-6, 4, 0), (-1, 1, 0)],
            (0, 2, ..., 4),
            [(-11, 7, 0)],
        ),
        (
            multigen_235,
            [(0, 0, 0), (-11, 7, 0), (-3, 2, 0), (-6, 4, 0), (-1, 1, 0)],
            (2, ..., 100),
            [(0, 0, 0), (-11, 7, 0)],
        ),
    ]
)
def test_partial_not(tuning, diff_vecs, mask, result_vecs):
    """
    Test if partial_not function of interval sequences works correctly
    """

    interval_seq = tuning.diff_interval_seq(
        [tuning.lattice.point(vec) for vec in diff_vecs]
    )
    result_interval_seq = tuning.diff_interval_seq(
        [tuning.lattice.point(vec) for vec in result_vecs]
    )

    assert interval_seq.partial_not(mask) == result_interval_seq


@pytest.mark.parametrize(
    'tuning, diff_vecs, mask',
    [
        (
            multigen_235,
            [(0, 0, 0), (-11, 7, 0), (-3, 2, 0), (-6, 4, 0)],
            (-1, ..., 2, 4),
        ),
        (
            multigen_235,
            [(0, 0, 0), (-11, 7, 0), (-3, 2, 0), (-6, 4, 0)],
            (..., 4, 3),
        ),
        (
            multigen_235,
            [(0, 0, 0), (-11, 7, 0), (-3, 2, 0), (-6, 4, 0)],
            (..., 4, 3, ...),
        ),
        (
            multigen_23,
            [(-11, 7), (-3, 2), (-6, 4), (-1, 1)],
            (3, 2, ...),
        ),
        (
            multigen_23,
            [(-11, 7), (-3, 2), (-6, 4), (-1, 1)],
            (1, 2, -1),
        ),
    ]
)
def test_partial_not_invalid_mask(tuning, diff_vecs, mask):
    """
    Test if partial_not function of interval sequences raises correct
    exception when invalid mask is given
    """

    interval_seq = tuning.diff_interval_seq(
        [tuning.lattice.point(vec) for vec in diff_vecs]
    )

    with pytest.raises(InvalidIndexMask):
        interval_seq.partial_not(mask)


@pytest.mark.parametrize(
    'tuning, diff_vecs, mask',
    [
        (
            multigen_235,
            [(0, 0, 0), (-11, 7, 0), (-3, 2, 0), (-6, 4, 0)],
            1,
        ),
        (
            multigen_235,
            [(0, 0, 0), (-11, 7, 0), (-3, 2, 0), (-6, 4, 0)],
            ...,
        ),
        (
            multigen_235,
            [(0, 0, 0), (-11, 7, 0), (-3, 2, 0), (-6, 4, 0)],
            (1,),
        ),
        (
            multigen_235,
            [(0, 0, 0), (-11, 7, 0), (-3, 2, 0), (-6, 4, 0)],
            (...,),
        ),
        (
            multigen_23,
            [(-11, 7), (-3, 2), (-6, 4), (-1, 1)],
            (1, 2),
        ),
        (
            multigen_weird,
            [(-1, 0, 0), (0, 0, 1), (11, 0, 0), (0, 2, 0)],
            (1, ...),
        ),
        (
            multigen_235,
            [(0, 0, 0), (-11, 7, 0), (-3, 2, 0), (-6, 4, 0), (-1, 1, 0)],
            (0, 2, 4),
        ),
        (
            multigen_235,
            [(0, 0, 0), (-11, 7, 0), (-3, 2, 0), (-6, 4, 0), (-1, 1, 0)],
            (..., 2, 4),
        ),
        (
            multigen_235,
            [(0, 0, 0), (-11, 7, 0), (-3, 2, 0), (-6, 4, 0), (-1, 1, 0)],
            (0, ..., 2, 4),
        ),
        (
            multigen_235,
            [(0, 0, 0), (-11, 7, 0), (-3, 2, 0), (-6, 4, 0), (-1, 1, 0)],
            (0, 2, ..., 4),
        ),
        (
            multigen_235,
            [(0, 0, 0), (-11, 7, 0), (-3, 2, 0), (-6, 4, 0), (-1, 1, 0)],
            (2, ..., 100),
        ),
    ]
)
def test_partition(tuning, diff_vecs, mask):
    """
    Test if partition function of interval sequences works correctly
    """

    interval_seq = tuning.diff_interval_seq(
        [tuning.lattice.point(vec) for vec in diff_vecs]
    )

    positive = interval_seq.partial(mask)
    complement = interval_seq.partial_not(mask)

    assert interval_seq.partition(mask) == (positive, complement)


@pytest.mark.parametrize(
    'tuning, diff_vecs, mask',
    [
        (
            multigen_235,
            [(0, 0, 0), (-11, 7, 0), (-3, 2, 0), (-6, 4, 0)],
            (-1, ..., 2, 4),
        ),
        (
            multigen_235,
            [(0, 0, 0), (-11, 7, 0), (-3, 2, 0), (-6, 4, 0)],
            (..., 4, 3),
        ),
        (
            multigen_235,
            [(0, 0, 0), (-11, 7, 0), (-3, 2, 0), (-6, 4, 0)],
            (..., 4, 3, ...),
        ),
        (
            multigen_23,
            [(-11, 7), (-3, 2), (-6, 4), (-1, 1)],
            (3, 2, ...),
        ),
        (
            multigen_23,
            [(-11, 7), (-3, 2), (-6, 4), (-1, 1)],
            (1, 2, -1),
        ),
    ]
)
def test_partition_invalid_mask(tuning, diff_vecs, mask):
    """
    Test if partition function of interval sequences raises correct
    exception when invalid mask is given
    """

    interval_seq = tuning.diff_interval_seq(
        [tuning.lattice.point(vec) for vec in diff_vecs]
    )

    with pytest.raises(InvalidIndexMask):
        interval_seq.partition(mask)


@pytest.mark.parametrize(
    'tuning, diff_vecs',
    [
        (
            multigen_235,
            [(0, 0, 0), (-11, 7, 0), (-3, 2, 0), (-6, 4, 0)],
        ),
        (
            multigen_23,
            [(-11, 7), (-3, 2), (-6, 4), (-1, 1)],
        ),
    ]
)
def test_in_operator(tuning, diff_vecs):
    """
    Test if 'in' operator works on interval sequences
    """

    interval_seq = tuning.diff_interval_seq(
        [tuning.lattice.point(vec) for vec in diff_vecs]
    )

    for vec in diff_vecs:
        assert tuning.diff_interval(tuning.lattice.point(vec)) in interval_seq


@pytest.mark.parametrize(
    'tuning, diff_vecs, excl_vecs',
    [
        (
            multigen_235,
            [(0, 0, 0), (-11, 7, 0), (-3, 2, 0), (-6, 4, 0)],
            [(0, 1, 0), (-12, 7, 0), (-3, -2, 0), (-3, 3, 0)],
        ),
        (
            multigen_235,
            [(0, 1, 0), (-12, 7, 0), (-3, -2, 0), (-3, 3, 0)],
            [(0, 0, 0), (-11, 7, 0), (-3, 2, 0), (-6, 4, 0)],
        ),
        (
            multigen_23,
            [(-11, 7), (-3, 2), (-6, 4), (-1, 1)],
            [(-12, 7), (-2, 1), (-5, 2), (-2, 1)],
        ),
        (
            multigen_23,
            [(-11, 7), (-3, 2), (-6, 4), (-1, 1)],
            [(-8, 3), (-2, 1), (-2, 1), (-4, 5)],
        ),
    ]
)
def test_not_in_operator(tuning, diff_vecs, excl_vecs):
    """
    Test if 'not in' operator works on interval sequences
    """

    interval_seq = tuning.diff_interval_seq(
        [tuning.lattice.point(vec) for vec in diff_vecs]
    )

    for vec in excl_vecs:
        assert tuning.diff_interval(
            tuning.lattice.point(vec)
        ) not in interval_seq


@pytest.mark.parametrize(
    'tuning, diff_vecs, repr_str',
    [
        (
            multigen_235,
            [(0, 0, 0), (-11, 7, 0), (-3, 2, 0), (-6, 4, 0)],
            'MultiGenPitchIntervalSeq(['
            '(0, 0, 0), (-11, 7, 0), (-3, 2, 0), (-6, 4, 0)'
            '], G=(2, 3, 5))',
        ),
        (
            multigen_235,
            [(0, 1, 0), (-12, 7, 0), (-3, -2, 0), (-3, 3, 0)],
            'MultiGenPitchIntervalSeq(['
            '(0, 1, 0), (-12, 7, 0), (-3, -2, 0), (-3, 3, 0)'
            '], G=(2, 3, 5))',
        ),
        (
            multigen_23,
            [(-11, 7), (-3, 2), (-6, 4), (-1, 1)],
            'MultiGenPitchIntervalSeq(['
            '(-11, 7), (-3, 2), (-6, 4), (-1, 1)'
            '], G=(2, 3))',
        ),
        (
            multigen_weird,
            [(-11, 7, 2), (-3, 2, 1), (-6, 4, 1), (-1, 1, 1)],
            'MultiGenPitchIntervalSeq(['
            '(-11, 7, 2), (-3, 2, 1), (-6, 4, 1), (-1, 1, 1)'
            '], G=(sqrt(2), 7, 11))',
        ),
    ]
)
def test_repr(tuning, diff_vecs, repr_str):
    """
    Test if repr() returns the right string
    """

    interval_seq = tuning.diff_interval_seq(
        [tuning.lattice.point(vec) for vec in diff_vecs]
    )

    assert repr(interval_seq) == repr_str


@pytest.mark.parametrize(
    'tuning, diff_vecs',
    [
        (
            multigen_235,
            [(0, 0, 0), (-11, 7, 0), (-3, 2, 0), (-6, 4, 0)],
        ),
        (
            multigen_23,
            [(-11, 7), (-3, 2), (-6, 4), (-1, 1)],
        ),
    ]
)
def test_frequency_ratios(tuning, diff_vecs):
    """
    Test if frequency_ratios property works correctly
    """

    interval_seq = tuning.diff_interval_seq(
        [tuning.lattice.point(vec) for vec in diff_vecs]
    )

    assert interval_seq.frequency_ratios == [
        tuning.diff_interval(tuning.lattice.point(vec)).frequency_ratio
        for vec in diff_vecs
    ]


@pytest.mark.parametrize(
    'tuning, diff_vecs',
    [
        (
            multigen_235,
            [(0, 0, 0), (-11, 7, 0), (-3, 2, 0), (-6, 4, 0)],
        ),
        (
            multigen_23,
            [(-11, 7), (-3, 2), (-6, 4), (-1, 1)],
        ),
    ]
)
def test_cents(tuning, diff_vecs):
    """
    Test if cents property works correctly
    """

    interval_seq = tuning.diff_interval_seq(
        [tuning.lattice.point(vec) for vec in diff_vecs]
    )

    assert interval_seq.cents == [
        tuning.diff_interval(tuning.lattice.point(vec)).cents
        for vec in diff_vecs
    ]


@pytest.mark.parametrize(
    'tuning, diff_vecs',
    [
        (
            multigen_235,
            [(0, 0, 0), (-11, 7, 0), (-3, 2, 0), (-6, 4, 0)],
        ),
        (
            multigen_23,
            [(-11, 7), (-3, 2), (-6, 4), (-1, 1)],
        ),
    ]
)
def test_pitch_diffs(tuning, diff_vecs):
    """
    Test if pitch_diffs property works correctly
    """

    pitch_diffs = [tuning.lattice.point(vec) for vec in diff_vecs]
    interval_seq = tuning.diff_interval_seq(pitch_diffs)
    assert interval_seq.pitch_diffs == pitch_diffs


@pytest.mark.parametrize(
    'tuning, diff_vecs_a, diff_vecs_b, result_vecs',
    [
        (
            multigen_235,
            [(0, 0, 0), (-11, 7, 0), (-3, 2, 0), (-6, 4, 0)],
            [(0, 1, 0), (-12, 7, 0), (-3, -2, 0), (-3, 3, 0)],
            [(0, 0, 0), (-11, 7, 0), (-3, 2, 0), (-6, 4, 0),
             (0, 1, 0), (-12, 7, 0), (-3, -2, 0), (-3, 3, 0)],
        ),
        (
            multigen_weird,
            [(0, 1, 0), (-12, 7, 0), (-3, -2, 0), (-3, 3, 0)],
            [(0, 0, 0), (-11, 7, 0), (-3, 2, 0), (-6, 4, 0)],
            [(0, 1, 0), (-12, 7, 0), (-3, -2, 0), (-3, 3, 0),
             (0, 0, 0), (-11, 7, 0), (-3, 2, 0), (-6, 4, 0)],
        ),
        (
            multigen_23,
            [(-11, 7), (-3, 2), (-6, 4), (-1, 1)],
            [(-12, 7), (-2, 1), (-5, 2), (-2, 1)],
            [(-11, 7), (-3, 2), (-6, 4), (-1, 1),
             (-12, 7), (-2, 1), (-5, 2), (-2, 1)],
        ),
    ]
)
def test_addition(tuning, diff_vecs_a, diff_vecs_b, result_vecs):
    """
    Test if 'addition' operator works on interval sequences
    """

    interval_seq_a = tuning.diff_interval_seq(
        [tuning.lattice.point(vec) for vec in diff_vecs_a]
    )

    interval_seq_b = tuning.diff_interval_seq(
        [tuning.lattice.point(vec) for vec in diff_vecs_b]
    )

    result = tuning.diff_interval_seq(
        [tuning.lattice.point(vec) for vec in result_vecs]
    )

    assert interval_seq_a + interval_seq_b == result


@pytest.mark.parametrize(
    'tuning, diff_vecs, result_vecs',
    [
        (
            multigen_235,
            [(-11, 7, 0), (0, 0, 0), (-3, 2, 0), (-6, 4, 0)],
            [(11, -7, 0), (0, 0, 0), (3, -2, 0), (6, -4, 0)],
        ),
        (
            multigen_235,
            [],
            [],
        ),
        (
            multigen_weird,
            [(0, 1, 0), (-12, 7, 0), (-3, -2, 0), (-3, 3, 0)],
            [(0, -1, 0), (12, -7, 0), (3, 2, 0), (3, -3, 0)],
        ),
    ]
)
def test_inversion(tuning, diff_vecs, result_vecs):
    """
    Test if inversion operation works on interval sequences
    """

    interval_seq = tuning.diff_interval_seq(
        [tuning.lattice.point(vec) for vec in diff_vecs]
    )

    result = tuning.diff_interval_seq(
        [tuning.lattice.point(vec) for vec in result_vecs]
    )

    assert interval_seq.inversion() == result


@pytest.mark.parametrize(
    'tuning, diff_vecs, scalar, result_vecs',
    [
        (
            multigen_235,
            [(0, 0, 0), (-11, 7, 0), (-3, 2, 0), (-6, 4, 0)],
            3,
            [(0, 0, 0), (-11, 7, 0), (-3, 2, 0), (-6, 4, 0),
             (0, 0, 0), (-11, 7, 0), (-3, 2, 0), (-6, 4, 0),
             (0, 0, 0), (-11, 7, 0), (-3, 2, 0), (-6, 4, 0)],
        ),
        (
            multigen_weird,
            [(0, 1, 0), (-12, 7, 0), (-3, -2, 0), (-3, 3, 0)],
            0,
            [],
        ),
        (
            multigen_23,
            [(-11, 7), (-3, 2), (-6, 4), (-1, 1)],
            1,
            [(-11, 7), (-3, 2), (-6, 4), (-1, 1)],
        ),
        (
            multigen_23,
            [(-11, 7), (-3, 2), (-6, 4), (-1, 1)],
            2,
            [(-11, 7), (-3, 2), (-6, 4), (-1, 1),
             (-11, 7), (-3, 2), (-6, 4), (-1, 1)],
        ),
    ]
)
def test_scalar_multiplication(tuning, diff_vecs, scalar, result_vecs):
    """
    Test if 'scalar multiplication' works on interval sequences
    """

    interval_seq = tuning.diff_interval_seq(
        [tuning.lattice.point(vec) for vec in diff_vecs]
    )

    result = tuning.diff_interval_seq(
        [tuning.lattice.point(vec) for vec in result_vecs]
    )

    assert scalar * interval_seq == result
    assert interval_seq * scalar == result


@pytest.mark.parametrize(
    'tuning, diff_vecs, diff_vec, result',
    [
        (
            multigen_235,
            [(0, 0, 0), (-11, 7, 0), (-3, 2, 0), (-6, 4, 0)],
            (-11, 7, 0),
            1
        ),
        (
            multigen_23,
            [(-11, 7), (-3, 2), (-6, -4), (-1, 1), (-6, -4)],
            (-6, -4),
            2
        ),
    ]
)
def test_index(tuning, diff_vecs, diff_vec, result):
    """
    Test if index method works correctly
    """

    interval_seq = tuning.diff_interval_seq(
        [tuning.lattice.point(vec) for vec in diff_vecs]
    )

    interval = tuning.diff_interval(
        tuning.lattice.point(diff_vec)
    )

    assert interval_seq.index(interval) == result


@pytest.mark.parametrize(
    'tuning, diff_vecs, diff_vec',
    [
        (
            multigen_235,
            [(0, 0, 0), (-11, 7, 0), (-3, 2, 0), (-6, 4, 0)],
            (-11, 8, 0),
        ),
        (
            multigen_23,
            [(5, -6), (-6, 1), (-1, -2), (-7, 2), (1, -3)],
            (-5, -4),
        ),
    ]
)
def test_index_value_error(tuning, diff_vecs, diff_vec):
    """
    Test if index raises ValueError if interval was not found
    """

    interval_seq = tuning.diff_interval_seq(
        [tuning.lattice.point(vec) for vec in diff_vecs]
    )

    interval = tuning.diff_interval(
        tuning.lattice.point(diff_vec)
    )

    with pytest.raises(ValueError) as excinfo:
        interval_seq.index(interval)
    assert (
        excinfo.value.args[0] ==
        f'{interval} is not in sequence'
    )


@pytest.mark.parametrize(
    'tuning, diff_vecs, diff_vec, start, result',
    [
        (
            multigen_235,
            [(0, 0, 0), (-11, 7, 0), (-3, 2, 0), (-6, 4, 0), (-3, 2, 0)],
            (-3, 2, 0),
            3,
            4
        ),
        (
            multigen_23,
            [(-11, 7), (-3, 2), (-6, -4), (-1, 1), (-1, 1), (-6, -4)],
            (-6, -4),
            3,
            5,
        ),
        (
            multigen_23,
            [(-11, 7), (-3, 2), (-6, -4), (-1, 1), (-1, 1), (-6, -4)],
            (-6, -4),
            2,
            2
        ),
    ]
)
def test_index_start(tuning, diff_vecs, diff_vec, start, result):
    """
    Test if index method works correctly
    with start parameter
    """

    interval_seq = tuning.diff_interval_seq(
        [tuning.lattice.point(vec) for vec in diff_vecs]
    )

    interval = tuning.diff_interval(
        tuning.lattice.point(diff_vec)
    )

    assert interval_seq.index(interval, start) == result


@pytest.mark.parametrize(
    'tuning, diff_vecs, diff_vec, start',
    [
        (
            multigen_235,
            [(0, 0, 0), (-11, 7, 0), (-3, 2, 0), (-6, 4, 0), (-3, -2, 0)],
            (-3, 2, 0),
            3,
        ),
        (
            multigen_23,
            [(-11, 7), (-3, 2), (-6, -4), (-1, 1), (-1, 1), (-6, -4)],
            (-1, 1),
            5,
        ),
        (
            multigen_23,
            [(-11, 7), (-3, 2), (-6, -4), (-1, 1), (-1, 1), (-6, -4)],
            (-3, 2),
            2,
        ),
    ]
)
def test_index_start_value_error(tuning, diff_vecs, diff_vec, start):
    """
    Test if index raises ValueError if interval was not found
    after a given start value
    """

    interval_seq = tuning.diff_interval_seq(
        [tuning.lattice.point(vec) for vec in diff_vecs]
    )

    interval = tuning.diff_interval(
        tuning.lattice.point(diff_vec)
    )

    with pytest.raises(ValueError) as excinfo:
        interval_seq.index(interval, start)
    assert (
        excinfo.value.args[0] ==
        f'{interval} is not in sequence'
    )


@pytest.mark.parametrize(
    'tuning, diff_vecs, diff_vec, start, stop, result',
    [
        (
            multigen_235,
            [(-3, 2, 0), (-11, 7, 0), (-3, 2, 0), (-6, 4, 0), (-3, 2, 0)],
            (-3, 2, 0),
            1,
            3,
            2
        ),
        (
            multigen_23,
            [(-11, 7), (-3, 2), (-6, -4), (-1, 1), (-1, 1), (-6, -4)],
            (-6, -4),
            1,
            5,
            2,
        ),
    ]
)
def test_index_start_stop(tuning, diff_vecs, diff_vec, start, stop, result):
    """
    Test if intervals can be found with index and
    a given start and stop parameter
    """

    interval_seq = tuning.diff_interval_seq(
        [tuning.lattice.point(vec) for vec in diff_vecs]
    )

    interval = tuning.diff_interval(
        tuning.lattice.point(diff_vec)
    )

    assert interval_seq.index(interval, start, stop) == result


@pytest.mark.parametrize(
    'tuning, diff_vecs, diff_vec, start, stop',
    [
        (
            multigen_235,
            [(-3, 2, 0), (-11, 7, 0), (-1, 2, 0), (-6, 4, 0), (-3, 2, 0)],
            (-3, 2, 0),
            1,
            3,
        ),
        (
            multigen_23,
            [(-11, 7), (-3, 2), (-6, -4), (-1, 1), (-1, 1), (-6, -4)],
            (-6, -4),
            3,
            5,
        ),
    ]
)
def test_index_start_stop_value_error(
    tuning, diff_vecs, diff_vec, start, stop
):
    """
    Test if intervals can be found with index and
    a given start and stop parameter
    """

    interval_seq = tuning.diff_interval_seq(
        [tuning.lattice.point(vec) for vec in diff_vecs]
    )

    interval = tuning.diff_interval(
        tuning.lattice.point(diff_vec)
    )

    with pytest.raises(ValueError) as excinfo:
        interval_seq.index(interval, start, stop)
    assert (
        excinfo.value.args[0] ==
        f'{interval} is not in sequence'
    )


@pytest.mark.parametrize(
    'tuning, diff_vecs, pitch_vec, pitch_vecs',
    [
        (
            multigen_235,
            [(0, 1, 0), (-11, 7, 1), (-3, 2, 0), (-6, 4, 3)],
            (-11, 7, 1),
            [(-11, 7, 1), (-11, 8, 1), (-22, 15, 2),
             (-25, 17, 2), (-31, 21, 5)],
        ),
        (
            multigen_23,
            [(-11, 7), (-3, 2), (-6, -4), (-1, 1), (-6, -4)],
            (-6, -4),
            [(-6, -4), (-17, 3), (-20, 5), (-26, 1), (-27, 2), (-33, -2)],
        ),
    ]
)
def test_to_scale(tuning, diff_vecs, pitch_vec, pitch_vecs):
    """
    Test if pitch interval sequence can be converted into scale
    """

    interval_seq = tuning.diff_interval_seq(
        [tuning.lattice.point(vec) for vec in diff_vecs]
    )
    scale = tuning.index_scale(
        [tuning.lattice.point(vec) for vec in pitch_vecs]
    )
    pitch = tuning.pitch(
        tuning.lattice.point(pitch_vec)
    )

    assert interval_seq.to_scale(pitch) == scale
