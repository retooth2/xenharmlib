import sympy as sp
import pytest
from xenharmlib import EDTuning
from xenharmlib import EDOTuning
from xenharmlib.exc import IncompatibleOriginContexts
from xenharmlib.exc import InvalidIndexMask
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
    Test if interval fan can be created by omitting intervals parameter
    """

    interval_fan = tuning.interval_fan()

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
        multigen_257.interval_fan(
            [multigen_235.diff_interval(multigen_235.lattice.point((0, 0, 0)))]
        )

    with pytest.raises(IncompatibleOriginContexts):
        multigen_weird.interval_fan(
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

    interval_fan = tuning.interval_fan(
        [tuning.diff_interval(tuning.lattice.point(diff))
         for diff in diff_vecs]
    )

    interval_fan = interval_fan.with_interval(
        tuning.diff_interval(tuning.lattice.point(new_diff_vec))
    )

    assert len(interval_fan) == len(result_vecs)
    intervals = list(interval_fan)
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

    interval_fan = tuning.interval_fan(
        [tuning.diff_interval(tuning.lattice.point(diff))
         for diff in diff_vecs]
    )

    interval_fan = interval_fan.with_interval(
        tuning.diff_interval(tuning.lattice.point(new_diff_vec)),
        insert_pos
    )

    assert len(interval_fan) == len(result_vecs)
    intervals = list(interval_fan)
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

            interval_fan = tuning_a.interval_fan()

            with pytest.raises(IncompatibleOriginContexts):
                interval_fan.with_interval(
                    tuning_b.diff_interval(
                        tuning_b.zero_index
                    )
                )


def test_eq():
    """
    Test if interval_fan equalities and inequalities work correctly
    """

    interval_fan_a = multigen_23.diff_interval_fan(
        [multigen_23.lattice.point(vec)
         for vec in [(7, -11), (-4, 2), (-1, 1)]]
    )
    interval_fan_b = multigen_23.diff_interval_fan(
        [multigen_23.lattice.point(vec)
         for vec in [(7, -11), (-4, 2), (-1, 1)]]
    )
    interval_fan_c = multigen_23.diff_interval_fan(
        [multigen_23.lattice.point(vec)
         for vec in [(7, -11), (-4, 2), (-1, 1), (1, 0)]]
    )

    interval_fan_d = multigen_weird.diff_interval_fan(
        [multigen_weird.lattice.point(vec)
         for vec in [(7, -11, 0), (-4, 2, 0), (-1, 1, 0)]]
    )
    interval_fan_e = multigen_235.diff_interval_fan(
        [multigen_235.lattice.point(vec)
         for vec in [(7, -11, 0), (-4, 2, 0), (-1, 1, 0)]]
    )

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

    interval_fan = tuning.diff_interval_fan(
        [tuning.lattice.point(vec) for vec in diff_vecs]
    )

    for i, vec in enumerate(diff_vecs):
        assert interval_fan[i] == tuning.diff_interval(
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
    Test if slicing of interval fans works correctly
    """

    interval_fan = tuning.diff_interval_fan(
        [tuning.lattice.point(vec) for vec in diff_vecs]
    )
    result_interval_fan = tuning.diff_interval_fan(
        [tuning.lattice.point(vec) for vec in result_vecs]
    )

    for i, vec in enumerate(diff_vecs):
        assert interval_fan[i] == tuning.diff_interval(
            tuning.lattice.point(vec)
        )

    assert interval_fan[start:stop] == result_interval_fan


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
    Test if slicing of interval fans works correctly when
    stop parameter is omitted
    """

    interval_fan = tuning.diff_interval_fan(
        [tuning.lattice.point(vec) for vec in diff_vecs]
    )
    result_interval_fan = tuning.diff_interval_fan(
        [tuning.lattice.point(vec) for vec in result_vecs]
    )

    for i, vec in enumerate(diff_vecs):
        assert interval_fan[i] == tuning.diff_interval(
            tuning.lattice.point(vec)
        )

    assert interval_fan[start:] == result_interval_fan


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
    Test if slicing of interval fan works correctly when
    start parameter is omitted
    """

    interval_fan = tuning.diff_interval_fan(
        [tuning.lattice.point(vec) for vec in diff_vecs]
    )
    result_interval_fan = tuning.diff_interval_fan(
        [tuning.lattice.point(vec) for vec in result_vecs]
    )

    for i, vec in enumerate(diff_vecs):
        assert interval_fan[i] == tuning.diff_interval(
            tuning.lattice.point(vec)
        )
    assert interval_fan[:stop] == result_interval_fan


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
    Test if partial function of interval fans works correctly
    """

    interval_fan = tuning.diff_interval_fan(
        [tuning.lattice.point(vec) for vec in diff_vecs]
    )
    result_interval_fan = tuning.diff_interval_fan(
        [tuning.lattice.point(vec) for vec in result_vecs]
    )

    assert interval_fan.partial(mask) == result_interval_fan


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
    Test if partial function of interval fans raises correct
    exception when invalid mask is given
    """

    interval_fan = tuning.diff_interval_fan(
        [tuning.lattice.point(vec) for vec in diff_vecs]
    )

    with pytest.raises(InvalidIndexMask):
        interval_fan.partial(mask)


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
    Test if partial_not function of interval fans works correctly
    """

    interval_fan = tuning.diff_interval_fan(
        [tuning.lattice.point(vec) for vec in diff_vecs]
    )
    result_interval_fan = tuning.diff_interval_fan(
        [tuning.lattice.point(vec) for vec in result_vecs]
    )

    assert interval_fan.partial_not(mask) == result_interval_fan


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
    Test if partial_not function of interval fans raises correct
    exception when invalid mask is given
    """

    interval_fan = tuning.diff_interval_fan(
        [tuning.lattice.point(vec) for vec in diff_vecs]
    )

    with pytest.raises(InvalidIndexMask):
        interval_fan.partial_not(mask)


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
    Test if partition function of interval fans works correctly
    """

    interval_fan = tuning.diff_interval_fan(
        [tuning.lattice.point(vec) for vec in diff_vecs]
    )

    positive = interval_fan.partial(mask)
    complement = interval_fan.partial_not(mask)

    assert interval_fan.partition(mask) == (positive, complement)


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
    Test if partition function of interval fans raises correct
    exception when invalid mask is given
    """

    interval_fan = tuning.diff_interval_fan(
        [tuning.lattice.point(vec) for vec in diff_vecs]
    )

    with pytest.raises(InvalidIndexMask):
        interval_fan.partition(mask)


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
    Test if 'in' operator works on interval fans
    """

    interval_fan = tuning.diff_interval_fan(
        [tuning.lattice.point(vec) for vec in diff_vecs]
    )

    for vec in diff_vecs:
        assert tuning.diff_interval(tuning.lattice.point(vec)) in interval_fan


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
    Test if 'not in' operator works on interval fans
    """

    interval_fan = tuning.diff_interval_fan(
        [tuning.lattice.point(vec) for vec in diff_vecs]
    )

    for vec in excl_vecs:
        assert tuning.diff_interval(
            tuning.lattice.point(vec)
        ) not in interval_fan


@pytest.mark.parametrize(
    'tuning, diff_vecs, repr_str',
    [
        (
            multigen_235,
            [(0, 0, 0), (-11, 7, 0), (-3, 2, 0), (-6, 4, 0)],
            'MultiGenPitchIntervalFan(['
            '(0, 0, 0), (-11, 7, 0), (-3, 2, 0), (-6, 4, 0)'
            '], G=(2, 3, 5))',
        ),
        (
            multigen_235,
            [(0, 1, 0), (-12, 7, 0), (-3, -2, 0), (-3, 3, 0)],
            'MultiGenPitchIntervalFan(['
            '(0, 1, 0), (-12, 7, 0), (-3, -2, 0), (-3, 3, 0)'
            '], G=(2, 3, 5))',
        ),
        (
            multigen_23,
            [(-11, 7), (-3, 2), (-6, 4), (-1, 1)],
            'MultiGenPitchIntervalFan(['
            '(-11, 7), (-3, 2), (-6, 4), (-1, 1)'
            '], G=(2, 3))',
        ),
        (
            multigen_weird,
            [(-11, 7, 2), (-3, 2, 1), (-6, 4, 1), (-1, 1, 1)],
            'MultiGenPitchIntervalFan(['
            '(-11, 7, 2), (-3, 2, 1), (-6, 4, 1), (-1, 1, 1)'
            '], G=(sqrt(2), 7, 11))',
        ),
    ]
)
def test_repr(tuning, diff_vecs, repr_str):
    """
    Test if repr() returns the right string
    """

    interval_fan = tuning.diff_interval_fan(
        [tuning.lattice.point(vec) for vec in diff_vecs]
    )

    assert repr(interval_fan) == repr_str


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

    interval_fan = tuning.diff_interval_fan(
        [tuning.lattice.point(vec) for vec in diff_vecs]
    )

    assert interval_fan.frequency_ratios == [
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

    interval_fan = tuning.diff_interval_fan(
        [tuning.lattice.point(vec) for vec in diff_vecs]
    )

    assert interval_fan.cents == [
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
    interval_fan = tuning.diff_interval_fan(pitch_diffs)
    assert interval_fan.pitch_diffs == pitch_diffs


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
    Test if 'addition' operator works on interval fans
    """

    interval_fan_a = tuning.diff_interval_fan(
        [tuning.lattice.point(vec) for vec in diff_vecs_a]
    )

    interval_fan_b = tuning.diff_interval_fan(
        [tuning.lattice.point(vec) for vec in diff_vecs_b]
    )

    result = tuning.diff_interval_fan(
        [tuning.lattice.point(vec) for vec in result_vecs]
    )

    assert interval_fan_a + interval_fan_b == result


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
    Test if inversion operation works on interval fans
    """

    interval_fan = tuning.diff_interval_fan(
        [tuning.lattice.point(vec) for vec in diff_vecs]
    )

    result = tuning.diff_interval_fan(
        [tuning.lattice.point(vec) for vec in result_vecs]
    )

    assert interval_fan.inversion() == result


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
    Test if 'scalar multiplication' works on interval fans
    """

    interval_fan = tuning.diff_interval_fan(
        [tuning.lattice.point(vec) for vec in diff_vecs]
    )

    result = tuning.diff_interval_fan(
        [tuning.lattice.point(vec) for vec in result_vecs]
    )

    assert scalar * interval_fan == result
    assert interval_fan * scalar == result


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

    interval_fan = tuning.diff_interval_fan(
        [tuning.lattice.point(vec) for vec in diff_vecs]
    )

    interval = tuning.diff_interval(
        tuning.lattice.point(diff_vec)
    )

    assert interval_fan.index(interval) == result


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

    interval_fan = tuning.diff_interval_fan(
        [tuning.lattice.point(vec) for vec in diff_vecs]
    )

    interval = tuning.diff_interval(
        tuning.lattice.point(diff_vec)
    )

    with pytest.raises(ValueError) as excinfo:
        interval_fan.index(interval)
    assert (
        excinfo.value.args[0] ==
        f'{interval} is not in fan'
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

    interval_fan = tuning.diff_interval_fan(
        [tuning.lattice.point(vec) for vec in diff_vecs]
    )

    interval = tuning.diff_interval(
        tuning.lattice.point(diff_vec)
    )

    assert interval_fan.index(interval, start) == result


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

    interval_fan = tuning.diff_interval_fan(
        [tuning.lattice.point(vec) for vec in diff_vecs]
    )

    interval = tuning.diff_interval(
        tuning.lattice.point(diff_vec)
    )

    with pytest.raises(ValueError) as excinfo:
        interval_fan.index(interval, start)
    assert (
        excinfo.value.args[0] ==
        f'{interval} is not in fan'
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

    interval_fan = tuning.diff_interval_fan(
        [tuning.lattice.point(vec) for vec in diff_vecs]
    )

    interval = tuning.diff_interval(
        tuning.lattice.point(diff_vec)
    )

    assert interval_fan.index(interval, start, stop) == result


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

    interval_fan = tuning.diff_interval_fan(
        [tuning.lattice.point(vec) for vec in diff_vecs]
    )

    interval = tuning.diff_interval(
        tuning.lattice.point(diff_vec)
    )

    with pytest.raises(ValueError) as excinfo:
        interval_fan.index(interval, start, stop)
    assert (
        excinfo.value.args[0] ==
        f'{interval} is not in fan'
    )


@pytest.mark.parametrize(
    'tuning, diff_vecs, pitch_vec, pitch_vecs',
    [
        (
            multigen_235,
            [(0, 0, 0), (-9, 3, 1), (-3, 2, 0), (-6, 4, 3)],
            (-11, 7, 1),
            [(-11, 7, 1), (-20, 10, 2), (-14, 9, 1), (-17, 11, 4)],
        ),
        (
            multigen_23,
            [(-11, 7), (-3, 2), (-6, -4), (-1, 1), (-6, -4)],
            (2, -1),
            [(-9, 6), (-1, 1), (-4, -5), (1, 0), (-4, -5)],
        ),
    ]
)
def test_to_scale(tuning, diff_vecs, pitch_vec, pitch_vecs):
    """
    Test if pitch interval fan can be converted into scale
    """

    interval_fan = tuning.diff_interval_fan(
        [tuning.lattice.point(vec) for vec in diff_vecs]
    )
    scale = tuning.index_scale(
        [tuning.lattice.point(vec) for vec in pitch_vecs]
    )
    pitch = tuning.pitch(
        tuning.lattice.point(pitch_vec)
    )

    assert interval_fan.to_scale(pitch) == scale
    assert pitch.scale(interval_fan) == scale


@pytest.mark.parametrize(
    'tuning, diff_vecs, pitch_vec, pitch_vecs',
    [
        (
            multigen_235,
            [(0, 1, 0), (-11, 7, 1), (-3, 2, 0), (-6, 4, 3)],
            (-11, 7, 1),
            [(-11, 8, 1), (-22, 14, 2), (-14, 9, 1), (-17, 11, 4)],
        ),
        (
            multigen_23,
            [(0, 0), (-3, 2), (-6, -4), (-1, 1), (-6, -4)],
            (-6, -4),
            [(-6, -4), (-9, -2), (-12, -8), (-7, -3), (-12, -8)],
        ),
    ]
)
def test_to_seq(tuning, diff_vecs, pitch_vec, pitch_vecs):
    """
    Test if pitch interval fan can be converted into pitch sequence
    """

    interval_fan = tuning.diff_interval_fan(
        [tuning.lattice.point(vec) for vec in diff_vecs]
    )
    seq = tuning.index_seq(
        [tuning.lattice.point(vec) for vec in pitch_vecs]
    )
    pitch = tuning.pitch(
        tuning.lattice.point(pitch_vec)
    )

    assert interval_fan.to_seq(pitch) == seq
    assert pitch.seq(interval_fan) == seq


@pytest.mark.parametrize(
    'source_tuning, source_vecs, target_tuning, target_diffs',
    [
        (
            multigen_235,
            [(-1, 1, 0), (-3, 1, 1), (-2, 2, 0)],
            EDOTuning(31),
            [18, 28, 36]
        ),
        (
            multigen_23,
            [(0, 0), (-6, 4), (-1, 1)],
            EDOTuning(12),
            [0, 4, 7]
        ),
    ]
)
def test_retune_closest_edo(
    source_tuning, source_vecs, target_tuning, target_diffs
):
    """
    Test if retune_closest method works correctly
    """

    interval_fan = source_tuning.diff_interval_fan(
        [source_tuning.lattice.point(vec) for vec in source_vecs]
    )

    retuned = interval_fan.retune_closest(target_tuning)
    assert retuned == target_tuning.diff_interval_fan(target_diffs)


def test_retune_closest_type_error():
    """
    Test if retune_closest method raises exception on 2+
    dimensional target tuning
    """

    diff_vecs = [(-1, 1, 0), (-3, 1, 1), (-2, 2, 0)]
    source_ifan = multigen_235.diff_interval_fan(
        [multigen_235.lattice.point(vec) for vec in diff_vecs]
    )

    with pytest.raises(TypeError):
        source_ifan.retune_closest(multigen_25)
