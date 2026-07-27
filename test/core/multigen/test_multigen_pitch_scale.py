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
    'tuning, input_vecs, result_vecs',
    [
        (
            multigen_23,
            [(1, -1), (1, 0), (-1, 1)],
            [(1, -1), (-1, 1), (1, 0)]
        ),
        (
            multigen_257,
            [(0, 0, 1), (0, 1, 0), (0, 1, 0), (1, 0, 0)],
            [(1, 0, 0), (0, 1, 0), (0, 0, 1)],
        ),
        (
            multigen_257,
            [(0, 0, 1), (0, 2, 0), (5, 0, 0)],
            [(0, 0, 1), (0, 2, 0), (5, 0, 0)],
        ),
        (
            multigen_weird,
            [(0, 0, 1), (0, 2, 0), (11, 0, 0)],
            [(0, 0, 1), (11, 0, 0), (0, 2, 0)],
        ),
    ]
)
def test_sort_on_init(tuning, input_vecs, result_vecs):
    """
    Test if pitches get sorted correctly on scale init
    """

    scale = tuning.scale(
        [tuning.pitch(tuning.lattice.point(vec)) for vec in input_vecs]
    )
    assert len(scale) == len(result_vecs)
    pitches = list(scale)
    assert pitches == [
        tuning.pitch(tuning.lattice.point(vec)) for vec in result_vecs
    ]


@pytest.mark.parametrize(
    'tuning',
    [
        multigen_23, multigen_257, multigen_weird
    ]
)
def test_init_empty(tuning):
    """
    Test if scale can be created by omitting pitches parameter
    """

    scale = tuning.scale()

    assert len(scale) == 0
    pitches = list(scale)
    assert pitches == []


@pytest.mark.parametrize(
    'tuning, input_vecs, pitch_vec, result_vecs',
    [
        (
            multigen_23,
            [(1, -1), (-1, 1), (1, 0)],
            (0, 0),
            [(1, -1), (0, 0), (-1, 1), (1, 0)]
        ),
        (
            multigen_257,
            [(1, 0, 0), (0, 1, 0), (0, 0, 1)],
            (0, -1, 0),
            [(0, -1, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1)],
        ),
        (
            multigen_257,
            [(1, 0, 0), (0, 1, 0), (0, 0, 1)],
            (0, 1, 0),
            [(1, 0, 0), (0, 1, 0), (0, 0, 1)],
        ),
        (
            multigen_257,
            [(0, 0, 1), (0, 2, 0), (5, 0, 0)],
            (4, 0, 0),
            [(0, 0, 1), (4, 0, 0), (0, 2, 0), (5, 0, 0)],
        ),
        (
            multigen_weird,
            [(0, 0, 1), (11, 0, 0), (0, 2, 0)],
            (0, 0, 0),
            [(0, 0, 0), (0, 0, 1), (11, 0, 0), (0, 2, 0)],
        ),
    ]
)
def test_with_element(tuning, input_vecs, pitch_vec, result_vecs):
    """
    Test if with_element correctly insorts new pitch
    """

    scale = tuning.scale(
        [tuning.pitch(tuning.lattice.point(vec)) for vec in input_vecs]
    )

    scale = scale.with_element(
        tuning.pitch(tuning.lattice.point(pitch_vec))
    )

    assert len(scale) == len(result_vecs)
    pitches = list(scale)
    assert pitches == [
        tuning.pitch(tuning.lattice.point(vec)) for vec in result_vecs
    ]


def test_eq():
    """
    Test if scale equalities and inequalities work correctly
    """

    scale_a = multigen_23.index_scale(
        [multigen_23.lattice.point(vec) for vec in [(0, 0), (-11, 7), (-3, 2)]]
    )
    scale_b = multigen_23.index_scale(
        [multigen_23.lattice.point(vec) for vec in [(0, 0), (-11, 7), (-3, 2)]]
    )
    scale_c = multigen_23.index_scale(
        [
            multigen_23.lattice.point(vec) for vec in [
                (0, 0), (-11, 7), (-3, 2), (-6, 4)
            ]
        ]
    )

    scale_d = multigen_25.index_scale(
        [multigen_25.lattice.point(vec) for vec in [(0, 0), (-11, 7), (-3, 2)]]
    )
    scale_e = multigen_235.index_scale(
        [
            multigen_235.lattice.point(vec) for vec in [
                (0, 0, 0), (-11, 7, 0), (-3, 2, 0),
            ]
        ]
    )

    assert scale_a == scale_a
    assert scale_a == scale_b
    assert scale_a == scale_e
    assert scale_a != scale_c
    assert scale_a != scale_d

    assert hash(scale_a) == hash(scale_a)
    assert hash(scale_a) == hash(scale_b)
    assert hash(scale_a) == hash(scale_e)
    assert hash(scale_a) != hash(scale_c)
    assert hash(scale_a) != hash(scale_d)

    assert 'XYZ' != scale_a
    assert 3 != scale_a
    assert scale_a != 'XYZ'
    assert scale_a != 3


@pytest.mark.parametrize(
    'tuning, pitch_vecs',
    [
        (multigen_235, [(0, 0, 0), (-11, 7, 0), (-3, 2, 0), (-6, 4, 0)]),
        (multigen_23, [(-11, 7), (-3, 2), (-6, 4), (-1, 1)]),
        (multigen_weird, [(-1, 0, 0), (0, 0, 1), (11, 0, 0), (0, 2, 0)]),
    ]
)
def test_getitem(tuning, pitch_vecs):
    """
    Test if fetching single pitch items works correctly
    """

    scale = tuning.index_scale(
        [tuning.lattice.point(vec) for vec in pitch_vecs]
    )

    for i, vec in enumerate(pitch_vecs):
        assert scale[i] == tuning.pitch(tuning.lattice.point(vec))


@pytest.mark.parametrize(
    'tuning, pitch_vecs, start, stop, result_vecs',
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
def test_getitem_slice(tuning, pitch_vecs, start, stop, result_vecs):
    """
    Test if slicing of scales works correctly
    """

    scale = tuning.index_scale(
        [tuning.lattice.point(vec) for vec in pitch_vecs]
    )

    for i, vec in enumerate(pitch_vecs):
        assert scale[i] == tuning.pitch(tuning.lattice.point(vec))

    scale = tuning.index_scale(
        [tuning.lattice.point(vec) for vec in pitch_vecs]
    )
    scale_b = tuning.index_scale(
        [tuning.lattice.point(vec) for vec in result_vecs]
    )
    assert scale[start:stop] == scale_b


@pytest.mark.parametrize(
    'tuning, pitch_vecs, start, result_vecs',
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
def test_getitem_slice_omit_stop(tuning, pitch_vecs, start, result_vecs):
    """
    Test if slicing of scales works correctly when
    stop parameter is omitted
    """

    scale = tuning.index_scale(
        [tuning.lattice.point(vec) for vec in pitch_vecs]
    )

    for i, vec in enumerate(pitch_vecs):
        assert scale[i] == tuning.pitch(tuning.lattice.point(vec))

    scale = tuning.index_scale(
        [tuning.lattice.point(vec) for vec in pitch_vecs]
    )
    scale_b = tuning.index_scale(
        [tuning.lattice.point(vec) for vec in result_vecs]
    )
    assert scale[start:] == scale_b


@pytest.mark.parametrize(
    'tuning, pitch_vecs, stop, result_vecs',
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
def test_getitem_slice_omit_start(tuning, pitch_vecs, stop, result_vecs):
    """
    Test if slicing of scales works correctly when
    start parameter is omitted
    """

    scale = tuning.index_scale(
        [tuning.lattice.point(vec) for vec in pitch_vecs]
    )

    for i, vec in enumerate(pitch_vecs):
        assert scale[i] == tuning.pitch(tuning.lattice.point(vec))

    scale = tuning.index_scale(
        [tuning.lattice.point(vec) for vec in pitch_vecs]
    )
    scale_b = tuning.index_scale(
        [tuning.lattice.point(vec) for vec in result_vecs]
    )
    assert scale[:stop] == scale_b


@pytest.mark.parametrize(
    'tuning, pitch_vecs, mask, result_vecs',
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
def test_partial(tuning, pitch_vecs, mask, result_vecs):
    """
    Test if partial function of scales works correctly
    """

    scale = tuning.index_scale(
        [tuning.lattice.point(vec) for vec in pitch_vecs]
    )

    for i, vec in enumerate(pitch_vecs):
        assert scale[i] == tuning.pitch(tuning.lattice.point(vec))

    scale = tuning.index_scale(
        [tuning.lattice.point(vec) for vec in pitch_vecs]
    )
    scale_b = tuning.index_scale(
        [tuning.lattice.point(vec) for vec in result_vecs]
    )
    assert scale.partial(mask) == scale_b


@pytest.mark.parametrize(
    'tuning, pitch_vecs, mask',
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
def test_partial_invalid_mask(tuning, pitch_vecs, mask):
    """
    Test if partial function of scales raises correct exception
    when invalid mask is given
    """

    scale = tuning.index_scale(
        [tuning.lattice.point(vec) for vec in pitch_vecs]
    )

    with pytest.raises(InvalidIndexMask):
        scale.partial(mask)


@pytest.mark.parametrize(
    'tuning, pitch_vecs, mask, result_vecs',
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
def test_partial_not(tuning, pitch_vecs, mask, result_vecs):
    """
    Test if partial_not function of scales works correctly
    """

    scale = tuning.index_scale(
        [tuning.lattice.point(vec) for vec in pitch_vecs]
    )

    for i, vec in enumerate(pitch_vecs):
        assert scale[i] == tuning.pitch(tuning.lattice.point(vec))

    scale = tuning.index_scale(
        [tuning.lattice.point(vec) for vec in pitch_vecs]
    )
    scale_b = tuning.index_scale(
        [tuning.lattice.point(vec) for vec in result_vecs]
    )
    assert scale.partial_not(mask) == scale_b


@pytest.mark.parametrize(
    'tuning, pitch_vecs, mask',
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
def test_partial_not_invalid_mask(tuning, pitch_vecs, mask):
    """
    Test if partial_not function of scales raises correct exception
    when invalid mask is given
    """

    scale = tuning.index_scale(
        [tuning.lattice.point(vec) for vec in pitch_vecs]
    )

    with pytest.raises(InvalidIndexMask):
        scale.partial_not(mask)


@pytest.mark.parametrize(
    'tuning, pitch_vecs, mask',
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
def test_partition(tuning, pitch_vecs, mask):
    """
    Test if partition function of scales works correctly
    """

    scale = tuning.index_scale(
        [tuning.lattice.point(vec) for vec in pitch_vecs]
    )

    for i, vec in enumerate(pitch_vecs):
        assert scale[i] == tuning.pitch(tuning.lattice.point(vec))

    positive = scale.partial(mask)
    complement = scale.partial_not(mask)

    assert scale.partition(mask) == (positive, complement)


@pytest.mark.parametrize(
    'tuning, pitch_vecs, mask',
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
def test_partition_invalid_mask(tuning, pitch_vecs, mask):
    """
    Test if partition function of scales raises correct exception
    when invalid mask is given
    """

    scale = tuning.index_scale(
        [tuning.lattice.point(vec) for vec in pitch_vecs]
    )

    with pytest.raises(InvalidIndexMask):
        scale.partition(mask)


@pytest.mark.parametrize(
    'tuning, pitch_vecs',
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
def test_in_operator_pitch(tuning, pitch_vecs):
    """
    Test if 'in' operator works on single pitches
    """

    scale = tuning.index_scale(
        [tuning.lattice.point(vec) for vec in pitch_vecs]
    )

    for vec in pitch_vecs:
        assert tuning.pitch(tuning.lattice.point(vec)) in scale


@pytest.mark.parametrize(
    'tuning, pitch_vecs, excl_vecs',
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
def test_not_in_operator_pitch(tuning, pitch_vecs, excl_vecs):
    """
    Test if 'not in' operator works on single pitches
    """

    scale = tuning.index_scale(
        [tuning.lattice.point(vec) for vec in pitch_vecs]
    )

    for vec in excl_vecs:
        assert tuning.pitch(tuning.lattice.point(vec)) not in scale


@pytest.mark.parametrize(
    'tuning, pitch_vecs, diff_vecs',
    [
        (
            multigen_235,
            [(0, 0, 0), (-11, 7, 0), (-3, 2, 0), (-6, 4, 0)],
            [(-11, 7, 0), (-3, 2, 0), (-6, 4, 0), (8, -5, 0), (-3, 2, 0)],
        ),
        (
            multigen_23,
            [(-11, 7), (-3, 2), (-6, 4), (-1, 1)],
            [(8, -5), (2, -1), (5, -3), (-5, 3)]
        ),
    ]
)
def test_in_operator_interval(tuning, pitch_vecs, diff_vecs):
    """
    Test if 'in' operator works on intervals
    """

    scale = tuning.index_scale(
        [tuning.lattice.point(vec) for vec in pitch_vecs]
    )

    for vec in diff_vecs:
        assert tuning.diff_interval(tuning.lattice.point(vec)) in scale


@pytest.mark.parametrize(
    'tuning, pitch_vecs, diff_vecs',
    [
        (
            multigen_235,
            [(0, 0, 0), (-11, 7, 0), (-3, 2, 0), (-6, 4, 0)],
            [(-10, 7, 0), (-2, 2, 0), (-5, 4, 1), (8, -5, -2), (-3, 2, 3)],
        ),
        (
            multigen_23,
            [(-11, 7), (-3, 2), (-6, 4), (-1, 1)],
            [(8, 5), (2, 1), (-5, 4)]
        ),
    ]
)
def test_not_in_operator_interval(tuning, pitch_vecs, diff_vecs):
    """
    Test if 'not in' operator works on intervals
    """

    scale = tuning.index_scale(
        [tuning.lattice.point(vec) for vec in pitch_vecs]
    )

    for vec in diff_vecs:
        assert tuning.diff_interval(tuning.lattice.point(vec)) not in scale


@pytest.mark.parametrize(
    'tuning, pitch_vecs, repr_str',
    [
        (
            multigen_235,
            [(0, 0, 0), (-11, 7, 0), (-3, 2, 0), (-6, 4, 0)],
            'MultiGenPitchScale([(0, 0, 0), (-11, 7, 0), (-3, 2, 0), '
            '(-6, 4, 0)], G=(2, 3, 5))',
        ),
        (
            multigen_23,
            [(-11, 7), (-3, 2), (-6, 4), (-1, 1)],
            'MultiGenPitchScale([(-11, 7), (-3, 2), (-6, 4), (-1, 1)], '
            'G=(2, 3))'
        ),
    ]
)
def test_repr(tuning, pitch_vecs, repr_str):
    """
    Test if repr() returns the right string for scale
    """

    scale = tuning.index_scale(
        [tuning.lattice.point(vec) for vec in pitch_vecs]
    )

    assert repr(scale) == repr_str


@pytest.mark.parametrize(
    'tuning, pitch_vecs',
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
def test_frequencies(tuning, pitch_vecs):
    """
    Test if frequencies property works correctly
    """

    scale = tuning.index_scale(
        [tuning.lattice.point(vec) for vec in pitch_vecs]
    )

    assert scale.frequencies == [
        tuning.pitch(tuning.lattice.point(vec)).frequency for vec in pitch_vecs
    ]


@pytest.mark.parametrize(
    'tuning, pitch_vecs',
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
def test_pitch_indices(tuning, pitch_vecs):
    """
    Test if pitch_indices property works correctly
    """

    scale = tuning.index_scale(
        [tuning.lattice.point(vec) for vec in pitch_vecs]
    )

    assert scale.pitch_indices == [
        tuning.lattice.point(vec) for vec in pitch_vecs
    ]


@pytest.mark.parametrize(
    'tuning, pitch_vecs, diff_vec, result_vecs',
    [
        (
            multigen_235,
            [(0, 0, 0), (-11, 7, 0), (-3, 2, 0), (-6, 4, 0)],
            (2, 0, 1),
            [(2, 0, 1), (-9, 7, 1), (-1, 2, 1), (-4, 4, 1)],
        ),
        (
            multigen_23,
            [(-11, 7), (-3, 2), (-6, 4), (-1, 1)],
            (1, -2),
            [(-10, 5), (-2, 0), (-5, 2), (0, -1)],
        ),
        (
            multigen_weird,
            [(-1, 0, 0), (0, 0, 1), (11, 0, 0), (0, 2, 0)],
            (-1, 0, 2),
            [(-2, 0, 2), (-1, 0, 3), (10, 0, 2), (-1, 2, 2)],
        ),
    ]
)
def test_transpose_interval(
    tuning, pitch_vecs, diff_vec, result_vecs
):

    scale = tuning.index_scale(
        [tuning.lattice.point(vec) for vec in pitch_vecs]
    )
    interval = tuning.diff_interval(tuning.lattice.point(diff_vec))
    expected_scale = tuning.index_scale(
        [tuning.lattice.point(vec) for vec in result_vecs]
    )

    transposed = scale.transpose(interval)
    assert transposed == expected_scale


@pytest.mark.parametrize(
    'tuning, pitch_vecs, diff_vec, result_vecs',
    [
        (
            multigen_235,
            [(0, 0, 0), (-11, 7, 0), (-3, 2, 0), (-6, 4, 0)],
            (2, 0, 1),
            [(2, 0, 1), (-9, 7, 1), (-1, 2, 1), (-4, 4, 1)],
        ),
        (
            multigen_23,
            [(-11, 7), (-3, 2), (-6, 4), (-1, 1)],
            (1, -2),
            [(-10, 5), (-2, 0), (-5, 2), (0, -1)],
        ),
        (
            multigen_weird,
            [(-1, 0, 0), (0, 0, 1), (11, 0, 0), (0, 2, 0)],
            (-1, 0, 2),
            [(-2, 0, 2), (-1, 0, 3), (10, 0, 2), (-1, 2, 2)],
        ),
    ]
)
def test_transpose_index(
    tuning, pitch_vecs, diff_vec, result_vecs
):

    scale = tuning.index_scale(
        [tuning.lattice.point(vec) for vec in pitch_vecs]
    )
    expected_scale = tuning.index_scale(
        [tuning.lattice.point(vec) for vec in result_vecs]
    )

    pitch_diff = tuning.lattice.point(diff_vec)
    transposed = scale.transpose(pitch_diff)
    assert transposed == expected_scale


@pytest.mark.parametrize(
    'tuning, pitch_vecs, axis_vec, result_vecs',
    [
        (
            multigen_235,
            [(0, 0, 0), (-11, 7, 0), (-3, 2, 0), (-6, 4, 0)],
            (0, 0, 0),
            [(0, 0, 0), (11, -7, 0), (3, -2, 0), (6, -4, 0)],
        ),
        (
            multigen_23,
            [(-11, 7), (-3, 2), (-6, 4), (-1, 1)],
            (1, -2),
            [(13, -11), (5, -6), (8, -8), (3, -5)],
        ),
        (
            multigen_weird,
            [(-1, 0, 0), (0, 0, 1), (11, 0, 0), (0, 2, 0)],
            (-1, 0, 2),
            [(-1, 0, 4), (-2, 0, 3), (-13, 0, 4), (-2, -2, 4)],
        ),
    ]
)
def test_reflection(
    tuning, pitch_vecs, axis_vec, result_vecs
):

    scale = tuning.index_scale(
        [tuning.lattice.point(vec) for vec in pitch_vecs]
    )
    expected_scale = tuning.index_scale(
        [tuning.lattice.point(vec) for vec in result_vecs]
    )

    axis = tuning.pitch(tuning.lattice.point(axis_vec))
    reflected = scale.reflection(axis)
    assert reflected == expected_scale


@pytest.mark.parametrize(
    'tuning, pitch_vecs, result_vecs',
    [
        (
            multigen_235,
            [(0, 0, 0), (-11, 7, 0), (-3, 2, 0), (-6, 4, 0)],
            [(0, 0, 0), (11, -7, 0), (3, -2, 0), (6, -4, 0)],
        ),
        (
            multigen_23,
            [(-11, 7), (-3, 2), (-6, 4), (-1, 1)],
            [(11, -7), (3, -2), (6, -4), (1, -1)],
        ),
        (
            multigen_weird,
            [(-1, 0, 0), (0, 0, 1), (11, 0, 0), (0, 2, 0)],
            [(1, 0, 0), (0, 0, -1), (-11, 0, 0), (0, -2, 0)],
        ),
    ]
)
def test_reflection_without_param(
    tuning, pitch_vecs, result_vecs
):

    scale = tuning.index_scale(
        [tuning.lattice.point(vec) for vec in pitch_vecs]
    )
    expected_scale = tuning.index_scale(
        [tuning.lattice.point(vec) for vec in result_vecs]
    )

    reflected = scale.reflection()
    assert reflected == expected_scale


@pytest.mark.parametrize(
    'source_tuning, source_vecs, target_tuning, target_indices',
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
    source_tuning, source_vecs, target_tuning, target_indices
):
    """
    Test if retune_closest method works correctly
    """

    scale = source_tuning.index_scale(
        [source_tuning.lattice.point(vec) for vec in source_vecs]
    )

    with pytest.deprecated_call():
        retuned = scale.retune(target_tuning)

    assert retuned == target_tuning.index_scale(target_indices)

    retuned = scale.retune_closest(target_tuning)
    assert retuned == target_tuning.index_scale(target_indices)


def test_retune_closest_type_error():
    """
    Test if retune_closest method raises exception
    on 2+ dimensional target tuning
    """

    pitch_vecs = [(-1, 1, 0), (-3, 1, 1), (-2, 2, 0)]
    source_scale = multigen_235.index_scale(
        [multigen_235.lattice.point(vec) for vec in pitch_vecs]
    )

    with pytest.raises(TypeError):
        with pytest.deprecated_call():
            source_scale.retune(multigen_25)

    with pytest.raises(TypeError):
        source_scale.retune_closest(multigen_25)


@pytest.mark.parametrize(
    'tuning, pitch_vecs_a, pitch_vecs_b, result_vecs',
    [
        (
            multigen_235,
            [(0, 0, 0), (-11, 7, 0), (-3, 2, 0), (-6, 4, 0)],
            [(0, 0, 0), (-11, 7, 0), (-3, 2, 0), (-5, 4, 0)],
            [(0, 0, 0), (-11, 7, 0), (-3, 2, 0), (-6, 4, 0), (-5, 4, 0)],
        ),
        (
            multigen_23,
            [(-11, 7), (-3, 2), (-6, 4), (-1, 1)],
            [(-11, 7), (-3, 2), (-6, 4), (-1, 1)],
            [(-11, 7), (-3, 2), (-6, 4), (-1, 1)],
        ),
        (
            multigen_weird,
            [(-1, 0, 0), (0, 0, 1), (11, 0, 0)],
            [(-2, 0, 2), (-1, 0, 3), (10, 0, 2)],
            [(-1, 0, 0), (0, 0, 1), (11, 0, 0),
             (-2, 0, 2), (-1, 0, 3), (10, 0, 2)],
        ),
        (
            multigen_23,
            [(-11, 7), (-3, 2), (-6, 4), (-1, 1)],
            [],
            [(-11, 7), (-3, 2), (-6, 4), (-1, 1)],
        ),
    ]
)
def test_union(
    tuning, pitch_vecs_a, pitch_vecs_b, result_vecs
):
    """
    Test if union operation works correctly
    """

    scale_a = tuning.index_scale(
        [tuning.lattice.point(vec) for vec in pitch_vecs_a]
    )
    scale_b = tuning.index_scale(
        [tuning.lattice.point(vec) for vec in pitch_vecs_b]
    )
    expected_scale = tuning.index_scale(
        [tuning.lattice.point(vec) for vec in result_vecs]
    )

    scale_c = scale_a.union(scale_b)
    assert len(scale_c) == len(result_vecs)
    assert scale_c == expected_scale

    scale_c = scale_a | scale_b
    assert len(scale_c) == len(result_vecs)
    assert scale_c == expected_scale

    scale_c = scale_b.union(scale_a)
    assert len(scale_c) == len(result_vecs)
    assert scale_c == expected_scale

    scale_c = scale_b | scale_a
    assert len(scale_c) == len(result_vecs)
    assert scale_c == expected_scale


def test_union_incompatible_origin_contexts():
    """
    Test if union operation fails if scales originate from
    different tunings
    """

    ed13_3 = EDTuning(13, FrequencyRatio(3))
    tunings = multigen_23, multigen_25, multigen_weird, ed13_3

    for i, tuning_a in enumerate(tunings):

        for tuning_b in tunings[i+1:]:

            scale_a = tuning_a.scale()
            scale_b = tuning_b.scale()

            with pytest.raises(IncompatibleOriginContexts):
                scale_a.union(scale_b)

            with pytest.raises(IncompatibleOriginContexts):
                scale_a | scale_b


@pytest.mark.parametrize(
    'tuning, pitch_vecs_a, pitch_vecs_b, result_vecs',
    [
        (
            multigen_235,
            [(0, 0, 0), (-11, 7, 0), (-3, 2, 0), (-6, 4, 0)],
            [(0, 0, 0), (-11, 7, 0), (-3, 2, 0), (-5, 4, 0)],
            [(0, 0, 0), (-11, 7, 0), (-3, 2, 0)],
        ),
        (
            multigen_23,
            [(-11, 7), (-3, 2), (-6, 4), (-1, 1)],
            [(-11, 7), (-3, 2), (-6, 4), (-1, 1)],
            [(-11, 7), (-3, 2), (-6, 4), (-1, 1)],
        ),
        (
            multigen_weird,
            [(-1, 0, 0), (0, 0, 1), (11, 0, 0)],
            [(-2, 0, 2), (-1, 0, 3), (10, 0, 2)],
            []
        ),
        (
            multigen_23,
            [(-11, 7), (-3, 2), (-6, 4), (-1, 1)],
            [],
            [],
        ),
    ]
)
def test_intersection(
    tuning, pitch_vecs_a, pitch_vecs_b, result_vecs
):
    """
    Test if intersection operation works correctly
    """

    scale_a = tuning.index_scale(
        [tuning.lattice.point(vec) for vec in pitch_vecs_a]
    )
    scale_b = tuning.index_scale(
        [tuning.lattice.point(vec) for vec in pitch_vecs_b]
    )
    expected_scale = tuning.index_scale(
        [tuning.lattice.point(vec) for vec in result_vecs]
    )

    scale_c = scale_a.intersection(scale_b)
    assert len(scale_c) == len(result_vecs)
    assert scale_c == expected_scale

    scale_c = scale_a & scale_b
    assert len(scale_c) == len(result_vecs)
    assert scale_c == expected_scale

    scale_c = scale_b.intersection(scale_a)
    assert len(scale_c) == len(result_vecs)
    assert scale_c == expected_scale

    scale_c = scale_b & scale_a
    assert len(scale_c) == len(result_vecs)
    assert scale_c == expected_scale


@pytest.mark.parametrize(
    'tuning, pitch_vecs_a, pitch_vecs_b, result_vecs',
    [
        (
            multigen_235,
            [(0, 0, 0), (-11, 7, 0), (-3, 2, 0), (-6, 4, 0)],
            [(0, 0, 0), (-11, 7, 0), (-3, 2, 0), (-5, 4, 0)],
            [(0, 0, 0), (-11, 7, 0), (-3, 2, 0), (-5, 4, 0), (-6, 4, 0)],
        ),
        (
            multigen_235,
            [(0, 0, 0), (-11, 7, 0), (-3, 2, 0), (-10, 7, 0)],
            [(0, 0, 0), (-11, 7, 0), (-3, 2, 0)],
            [(0, 0, 0), (-11, 7, 0), (-3, 2, 0), (-10, 7, 0)],
        ),
        (
            multigen_23,
            [(-11, 7), (-3, 2), (-6, 4), (-1, 1)],
            [(-11, 7), (-3, 2), (-6, 4), (-1, 1)],
            [(-11, 7), (-3, 2), (-6, 4), (-1, 1)],
        ),
        (
            multigen_weird,
            [(-1, 0, 0), (0, 0, 1), (11, 0, 0), (-1, 1, 3)],
            [(-2, 0, 2), (-1, 0, 3), (10, 0, 2)],
            [(-1, 0, 3), (-1, 1, 3)]
        ),
        (
            multigen_23,
            [(-11, 7), (-3, 2), (-6, 4), (-1, 1)],
            [],
            [],
        ),
    ]
)
def test_intersection_ignore_bi_index(
    tuning, pitch_vecs_a, pitch_vecs_b, result_vecs
):
    """
    Test if intersection operation works correctly
    with ignore_bi_index = True
    """

    scale_a = tuning.index_scale(
        [tuning.lattice.point(vec) for vec in pitch_vecs_a]
    )
    scale_b = tuning.index_scale(
        [tuning.lattice.point(vec) for vec in pitch_vecs_b]
    )
    expected_scale = tuning.index_scale(
        [tuning.lattice.point(vec) for vec in result_vecs]
    )

    scale_c = scale_a.intersection(scale_b, ignore_bi_index=True)
    assert len(scale_c) == len(result_vecs)
    assert scale_c == expected_scale

    scale_c = scale_b.intersection(scale_a, ignore_bi_index=True)
    assert len(scale_c) == len(result_vecs)
    assert scale_c == expected_scale


def test_intersection_incompatible_origin_contexts():
    """
    Test if intersection operation fails if scales originate from
    different tunings
    """

    ed13_3 = EDTuning(13, FrequencyRatio(3))
    tunings = multigen_23, multigen_25, multigen_weird, ed13_3

    for i, tuning_a in enumerate(tunings):

        for tuning_b in tunings[i+1:]:

            scale_a = tuning_a.scale()
            scale_b = tuning_b.scale()

            with pytest.raises(IncompatibleOriginContexts):
                scale_a.intersection(scale_b)

            with pytest.raises(IncompatibleOriginContexts):
                scale_a & scale_b


@pytest.mark.parametrize(
    'tuning, pitch_vecs_a, pitch_vecs_b, result_vecs',
    [
        (
            multigen_235,
            [(0, 0, 0), (-11, 7, 0), (-3, 2, 0), (-6, 4, 0)],
            [(0, 0, 0), (-11, 7, 0), (-3, 2, 0), (-5, 4, 0)],
            [(-6, 4, 0)],
        ),
        (
            multigen_23,
            [(-11, 7), (-3, 2), (-6, 4), (-1, 1)],
            [(-11, 7), (-3, 2), (-6, 4), (-1, 1)],
            [],
        ),
        (
            multigen_weird,
            [(-1, 0, 0), (0, 0, 1), (11, 0, 0)],
            [(-2, 0, 2), (-1, 0, 3), (10, 0, 2)],
            [(-1, 0, 0), (0, 0, 1), (11, 0, 0)],
        ),
        (
            multigen_23,
            [(-11, 7), (-3, 2), (-6, 4), (-1, 1)],
            [],
            [(-11, 7), (-3, 2), (-6, 4), (-1, 1)],
        ),
    ]
)
def test_difference(
    tuning, pitch_vecs_a, pitch_vecs_b, result_vecs
):
    """
    Test if difference operation works correctly
    """

    scale_a = tuning.index_scale(
        [tuning.lattice.point(vec) for vec in pitch_vecs_a]
    )
    scale_b = tuning.index_scale(
        [tuning.lattice.point(vec) for vec in pitch_vecs_b]
    )
    expected_scale = tuning.index_scale(
        [tuning.lattice.point(vec) for vec in result_vecs]
    )

    scale_c = scale_a.difference(scale_b)
    assert len(scale_c) == len(result_vecs)
    assert scale_c == expected_scale

    scale_c = scale_a - scale_b
    assert len(scale_c) == len(result_vecs)
    assert scale_c == expected_scale


@pytest.mark.parametrize(
    'tuning, pitch_vecs_a, pitch_vecs_b, result_vecs',
    [
        (
            multigen_235,
            [(0, 0, 0), (-11, 7, 0), (-3, 2, 0), (-6, 4, 0)],
            [(0, 0, 0), (-11, 7, 0), (-3, 2, 0), (-5, 4, 0)],
            [],
        ),
        (
            multigen_23,
            [(-11, 7), (-3, 2), (-6, 4), (-1, 1)],
            [(-11, 7), (-3, 2), (-6, 4), (-1, 1)],
            [],
        ),
        (
            multigen_weird,
            [(-1, 0, 0), (0, 0, 1), (11, 0, 0)],
            [(-2, 0, 2), (-1, 0, 3), (10, 0, 2), (0, 1, 1)],
            [(-1, 0, 0), (11, 0, 0)],
        ),
        (
            multigen_23,
            [(-11, 7), (-3, 2), (-6, 4), (-1, 1)],
            [],
            [(-11, 7), (-3, 2), (-6, 4), (-1, 1)],
        ),
    ]
)
def test_difference_ignore_bi_index(
    tuning, pitch_vecs_a, pitch_vecs_b, result_vecs
):
    """
    Test if difference operation works correctly
    with ignore_bi_index = True
    """

    scale_a = tuning.index_scale(
        [tuning.lattice.point(vec) for vec in pitch_vecs_a]
    )
    scale_b = tuning.index_scale(
        [tuning.lattice.point(vec) for vec in pitch_vecs_b]
    )
    expected_scale = tuning.index_scale(
        [tuning.lattice.point(vec) for vec in result_vecs]
    )

    scale_c = scale_a.difference(scale_b, ignore_bi_index=True)
    assert len(scale_c) == len(result_vecs)
    assert scale_c == expected_scale


def test_difference_incompatible_origin_contexts():
    """
    Test if difference operation fails if scales originate from
    different tunings
    """

    ed13_3 = EDTuning(13, FrequencyRatio(3))
    tunings = multigen_23, multigen_25, multigen_weird, ed13_3

    for i, tuning_a in enumerate(tunings):

        for tuning_b in tunings[i+1:]:

            scale_a = tuning_a.scale()
            scale_b = tuning_b.scale()

            with pytest.raises(IncompatibleOriginContexts):
                scale_a.difference(scale_b)

            with pytest.raises(IncompatibleOriginContexts):
                scale_a - scale_b


@pytest.mark.parametrize(
    'tuning, pitch_vecs_a, pitch_vecs_b, result_vecs',
    [
        (
            multigen_235,
            [(0, 0, 0), (-11, 7, 0), (-3, 2, 0), (-6, 4, 0)],
            [(0, 0, 0), (-11, 7, 0), (-3, 2, 0), (-5, 4, 0)],
            [(-6, 4, 0), (-5, 4, 0)],
        ),
        (
            multigen_23,
            [(-11, 7), (-3, 2), (-6, 4), (-1, 1)],
            [(-11, 7), (-3, 2), (-6, 4), (-1, 1)],
            [],
        ),
        (
            multigen_weird,
            [(-1, 0, 0), (0, 0, 1), (11, 0, 0)],
            [(-2, 0, 2), (-1, 0, 3), (10, 0, 2)],
            [(-1, 0, 0), (0, 0, 1), (11, 0, 0),
             (-2, 0, 2), (-1, 0, 3), (10, 0, 2)],
        ),
        (
            multigen_23,
            [(-11, 7), (-3, 2), (-6, 4), (-1, 1)],
            [],
            [(-11, 7), (-3, 2), (-6, 4), (-1, 1)],
        ),
    ]
)
def test_symmetric_difference(
    tuning, pitch_vecs_a, pitch_vecs_b, result_vecs
):
    """
    Test if symmetric_difference operation works correctly
    """

    scale_a = tuning.index_scale(
        [tuning.lattice.point(vec) for vec in pitch_vecs_a]
    )
    scale_b = tuning.index_scale(
        [tuning.lattice.point(vec) for vec in pitch_vecs_b]
    )
    expected_scale = tuning.index_scale(
        [tuning.lattice.point(vec) for vec in result_vecs]
    )

    scale_c = scale_a.symmetric_difference(scale_b)
    assert len(scale_c) == len(result_vecs)
    assert scale_c == expected_scale

    scale_c = scale_a ^ scale_b
    assert len(scale_c) == len(result_vecs)
    assert scale_c == expected_scale

    scale_c = scale_b.symmetric_difference(scale_a)
    assert len(scale_c) == len(result_vecs)
    assert scale_c == expected_scale

    scale_c = scale_b ^ scale_a
    assert len(scale_c) == len(result_vecs)
    assert scale_c == expected_scale


@pytest.mark.parametrize(
    'tuning, pitch_vecs_a, pitch_vecs_b, result_vecs',
    [
        (
            multigen_235,
            [(0, 0, 0), (-11, 7, 0), (-3, 2, 0), (-6, 4, 0)],
            [(0, 0, 0), (-11, 7, 0), (-3, 2, 0), (-5, 4, 0)],
            [],
        ),
        (
            multigen_23,
            [(-11, 7), (-3, 2), (-6, 4), (-1, 1)],
            [(-11, 7), (-3, 2), (-6, 4), (-1, 1)],
            [],
        ),
        (
            multigen_weird,
            [(-1, 0, 0), (0, 0, 1), (11, 0, 0), (-1, 4, 3)],
            [(-2, 0, 2), (-1, 0, 3), (10, 0, 2)],
            [(-1, 0, 0), (0, 0, 1), (11, 0, 0),
             (-2, 0, 2), (10, 0, 2)],
        ),
        (
            multigen_23,
            [(-11, 7), (-3, 2), (-6, 4), (-1, 1)],
            [],
            [(-11, 7), (-3, 2), (-6, 4), (-1, 1)],
        ),
    ]
)
def test_symmetric_difference_ignore_bi_index(
    tuning, pitch_vecs_a, pitch_vecs_b, result_vecs
):
    """
    Test if symmetric_difference operation works correctly
    with ignore_bi_index=True
    """

    scale_a = tuning.index_scale(
        [tuning.lattice.point(vec) for vec in pitch_vecs_a]
    )
    scale_b = tuning.index_scale(
        [tuning.lattice.point(vec) for vec in pitch_vecs_b]
    )
    expected_scale = tuning.index_scale(
        [tuning.lattice.point(vec) for vec in result_vecs]
    )

    scale_c = scale_a.symmetric_difference(scale_b, ignore_bi_index=True)
    assert len(scale_c) == len(result_vecs)
    assert scale_c == expected_scale

    scale_c = scale_b.symmetric_difference(scale_a, ignore_bi_index=True)
    assert len(scale_c) == len(result_vecs)
    assert scale_c == expected_scale


def test_symmetric_difference_incompatible_origin_contexts():
    """
    Test if symmetric_difference operation fails if scales originate
    from different tunings
    """

    ed13_3 = EDTuning(13, FrequencyRatio(3))
    tunings = multigen_23, multigen_25, multigen_weird, ed13_3

    for i, tuning_a in enumerate(tunings):

        for tuning_b in tunings[i+1:]:

            scale_a = tuning_a.scale()
            scale_b = tuning_b.scale()

            with pytest.raises(IncompatibleOriginContexts):
                scale_a.symmetric_difference(scale_b)

            with pytest.raises(IncompatibleOriginContexts):
                scale_a ^ scale_b


@pytest.mark.parametrize(
    'tuning, pitch_vecs_a, pitch_vecs_b, expected',
    [
        (
            multigen_235,
            [(0, 0, 0), (-11, 7, 0), (-3, 2, 0), (-6, 4, 0)],
            [(0, 0, 0), (-11, 7, 0), (-3, 2, 0), (-5, 4, 0)],
            False
        ),
        (
            multigen_23,
            [(-11, 7), (-3, 2), (-6, 4), (-1, 1)],
            [(-11, 7), (-3, 2), (-6, 4), (-1, 1)],
            False
        ),
        (
            multigen_weird,
            [(-1, 0, 0), (0, 0, 1), (11, 0, 0)],
            [(-2, 0, 2), (-1, 0, 3), (10, 0, 2)],
            True
        ),
        (
            multigen_23,
            [(-11, 7), (-3, 2), (-6, 4), (-1, 1)],
            [],
            True
        ),
    ]
)
def test_is_disjoint(
    tuning, pitch_vecs_a, pitch_vecs_b, expected
):
    """
    Test if is_disjoint operation works correctly
    """

    scale_a = tuning.index_scale(
        [tuning.lattice.point(vec) for vec in pitch_vecs_a]
    )
    scale_b = tuning.index_scale(
        [tuning.lattice.point(vec) for vec in pitch_vecs_b]
    )

    assert scale_a.is_disjoint(scale_b) is expected
    assert scale_b.is_disjoint(scale_a) is expected


@pytest.mark.parametrize(
    'tuning, pitch_vecs_a, pitch_vecs_b, expected',
    [
        (
            multigen_235,
            [(0, 0, 0), (-11, 7, 0), (-3, 2, 0), (-6, 4, 0)],
            [(0, 0, 0), (-11, 7, 0), (-3, 2, 0), (-5, 4, 0)],
            False
        ),
        (
            multigen_23,
            [(-11, 7), (-3, 2), (-6, 4), (-1, 1)],
            [(-11, 7), (-3, 2), (-6, 4), (-1, 1)],
            False
        ),
        (
            multigen_weird,
            [(-1, 0, 0), (0, 0, 1), (11, 0, 0)],
            [(-2, 0, 2), (-1, 0, 3), (10, 0, 2), (11, 9, 0)],
            False
        ),
        (
            multigen_23,
            [(-11, 7), (-3, 2), (-6, 4), (-1, 1)],
            [(-4, 2)],
            False
        ),
        (
            multigen_23,
            [(-11, 7), (-3, 2), (-6, 4), (-1, 1)],
            [],
            True
        ),
    ]
)
def test_is_disjoint_ignore_bi_index(
    tuning, pitch_vecs_a, pitch_vecs_b, expected
):
    """
    Test if is_disjoint operation works correctly
    with ignore_bi_index = True
    """

    scale_a = tuning.index_scale(
        [tuning.lattice.point(vec) for vec in pitch_vecs_a]
    )
    scale_b = tuning.index_scale(
        [tuning.lattice.point(vec) for vec in pitch_vecs_b]
    )

    assert scale_a.is_disjoint(scale_b, ignore_bi_index=True) is expected
    assert scale_b.is_disjoint(scale_a, ignore_bi_index=True) is expected


def test_is_disjoint_incompatible_origin_contexts():
    """
    Test if is_disjoint operation fails if scales originate
    from different tunings
    """

    ed13_3 = EDTuning(13, FrequencyRatio(3))
    tunings = multigen_23, multigen_25, multigen_weird, ed13_3

    for i, tuning_a in enumerate(tunings):

        for tuning_b in tunings[i+1:]:

            scale_a = tuning_a.scale()
            scale_b = tuning_b.scale()

            with pytest.raises(IncompatibleOriginContexts):
                scale_a.is_disjoint(scale_b)


@pytest.mark.parametrize(
    'tuning, pitch_vecs_a, pitch_vecs_b, expected',
    [
        (
            multigen_235,
            [(0, 0, 0), (-11, 7, 0), (-3, 2, 0)],
            [(0, 0, 0), (-11, 7, 0), (-3, 2, 0), (-5, 4, 0)],
            True
        ),
        (
            multigen_235,
            [(0, 0, 0), (-11, 7, 0), (-4, 2, 0)],
            [(0, 0, 0), (-11, 7, 0), (-3, 2, 0), (-5, 4, 0)],
            False
        ),
        (
            multigen_23,
            [(-11, 7), (-3, 2), (-6, 4), (-1, 1)],
            [(-11, 7), (-3, 2), (-6, 4), (-1, 1)],
            True
        ),
        (
            multigen_weird,
            [],
            [(-2, 0, 2), (-1, 0, 3), (10, 0, 2)],
            True
        ),
        (
            multigen_23,
            [(-11, 7), (-3, 2), (-6, 4), (-1, 1)],
            [],
            False
        ),
    ]
)
def test_is_subset(
    tuning, pitch_vecs_a, pitch_vecs_b, expected
):
    """
    Test if is_subset operation works correctly
    """

    scale_a = tuning.index_scale(
        [tuning.lattice.point(vec) for vec in pitch_vecs_a]
    )
    scale_b = tuning.index_scale(
        [tuning.lattice.point(vec) for vec in pitch_vecs_b]
    )

    assert scale_a.is_subset(scale_b) is expected


@pytest.mark.parametrize(
    'tuning, pitch_vecs_a, pitch_vecs_b, expected',
    [
        (
            multigen_235,
            [(0, 0, 0), (-11, 7, 0), (-3, 2, 0)],
            [(0, 0, 0), (-11, 7, 0), (-3, 2, 0), (-5, 4, 0)],
            True
        ),
        (
            multigen_235,
            [(0, 0, 0), (-11, 7, 0), (-4, 2, 0)],
            [(0, 0, 0), (-11, 7, 0), (-3, 2, 0), (-5, 4, 0)],
            True
        ),
        (
            multigen_23,
            [(-11, 7), (-3, 2), (-6, 4), (-1, 1)],
            [(-11, 7), (-3, 2), (-6, 4), (-1, 1)],
            True
        ),
        (
            multigen_weird,
            [],
            [(-2, 0, 2), (-1, 0, 3), (10, 0, 2)],
            True
        ),
        (
            multigen_weird,
            [(10, 9, 2)],
            [(-2, 0, 2), (-1, 0, 3), (10, 0, 2)],
            True
        ),
        (
            multigen_23,
            [(-11, 7), (-3, 2), (-6, 4), (-1, 1)],
            [],
            False
        ),
    ]
)
def test_is_subset_ignore_bi_index(
    tuning, pitch_vecs_a, pitch_vecs_b, expected
):
    """
    Test if is_subset operation works correctly
    with ignore_bi_index = True
    """

    scale_a = tuning.index_scale(
        [tuning.lattice.point(vec) for vec in pitch_vecs_a]
    )
    scale_b = tuning.index_scale(
        [tuning.lattice.point(vec) for vec in pitch_vecs_b]
    )

    assert scale_a.is_subset(scale_b, ignore_bi_index=True) is expected


@pytest.mark.parametrize(
    'tuning, pitch_vecs_a, pitch_vecs_b, expected',
    [
        (
            multigen_235,
            [(0, 0, 0), (-11, 7, 0), (-3, 2, 0)],
            [(0, 0, 0), (-11, 7, 0), (-3, 2, 0), (-5, 4, 0)],
            True
        ),
        (
            multigen_235,
            [(0, 0, 0), (-11, 7, 0), (-4, 2, 0)],
            [(0, 0, 0), (-11, 7, 0), (-3, 2, 0), (-5, 4, 0)],
            False
        ),
        (
            multigen_23,
            [(-11, 7), (-3, 2), (-6, 4), (-1, 1)],
            [(-11, 7), (-3, 2), (-6, 4), (-1, 1)],
            False
        ),
        (
            multigen_weird,
            [],
            [(-2, 0, 2), (-1, 0, 3), (10, 0, 2)],
            True
        ),
        (
            multigen_23,
            [(-11, 7), (-3, 2), (-6, 4), (-1, 1)],
            [],
            False
        ),
    ]
)
def test_is_subset_proper(
    tuning, pitch_vecs_a, pitch_vecs_b, expected
):
    """
    Test if is_subset operation works correctly
    with proper=True
    """

    scale_a = tuning.index_scale(
        [tuning.lattice.point(vec) for vec in pitch_vecs_a]
    )
    scale_b = tuning.index_scale(
        [tuning.lattice.point(vec) for vec in pitch_vecs_b]
    )

    assert scale_a.is_subset(scale_b, proper=True) is expected


@pytest.mark.parametrize(
    'tuning, pitch_vecs_a, pitch_vecs_b, expected',
    [
        (
            multigen_235,
            [(0, 0, 0), (-11, 7, 0), (-3, 2, 0)],
            [(0, 0, 0), (-11, 7, 0), (-3, 2, 0), (-5, 4, 0)],
            True
        ),
        (
            multigen_235,
            [(0, 0, 0), (-11, 7, 0), (-4, 2, 0)],
            [(0, 0, 0), (-11, 7, 0), (-3, 2, 0), (-5, 4, 0)],
            True
        ),
        (
            multigen_23,
            [(-11, 7), (-3, 2), (-6, 4), (-1, 1)],
            [(-11, 7), (-3, 2), (-6, 4), (-1, 1)],
            False
        ),
        (
            multigen_23,
            [(-11, 7), (-3, 2), (-6, 4), (-1, 1)],
            [(-11, 7), (-3, 2), (-6, 4), (-1, 1), (-2, 1)],
            False
        ),
        (
            multigen_weird,
            [],
            [(-2, 0, 2), (-1, 0, 3), (10, 0, 2)],
            True
        ),
        (
            multigen_23,
            [(-11, 7), (-3, 2), (-6, 4), (-1, 1)],
            [],
            False
        ),
    ]
)
def test_is_subset_proper_ignore_bi_index(
    tuning, pitch_vecs_a, pitch_vecs_b, expected
):
    """
    Test if is_subset operation works correctly
    with proper=True and ignore_bi_index=True
    """

    scale_a = tuning.index_scale(
        [tuning.lattice.point(vec) for vec in pitch_vecs_a]
    )
    scale_b = tuning.index_scale(
        [tuning.lattice.point(vec) for vec in pitch_vecs_b]
    )

    assert scale_a.is_subset(
        scale_b, proper=True, ignore_bi_index=True
    ) is expected


def test_is_subset_incompatible_origin_contexts():
    """
    Test if is_subset operation fails if scales originate
    from different tunings
    """

    ed13_3 = EDTuning(13, FrequencyRatio(3))
    tunings = multigen_23, multigen_25, multigen_weird, ed13_3

    for i, tuning_a in enumerate(tunings):

        for tuning_b in tunings[i+1:]:

            scale_a = tuning_a.scale()
            scale_b = tuning_b.scale()

            with pytest.raises(IncompatibleOriginContexts):
                scale_a.is_subset(scale_b)

            with pytest.raises(IncompatibleOriginContexts):
                scale_a.is_subset(scale_b, proper=True)


@pytest.mark.parametrize(
    'tuning, pitch_vecs_a, pitch_vecs_b, expected',
    [
        (
            multigen_235,
            [(0, 0, 0), (-11, 7, 0), (-3, 2, 0), (-5, 4, 0)],
            [(0, 0, 0), (-11, 7, 0), (-3, 2, 0)],
            True
        ),
        (
            multigen_235,
            [(0, 0, 0), (-11, 7, 0), (-3, 2, 0), (-5, 4, 0)],
            [(0, 0, 0), (-11, 7, 0), (-4, 2, 0)],
            False
        ),
        (
            multigen_23,
            [(-11, 7), (-3, 2), (-6, 4), (-1, 1)],
            [(-11, 7), (-3, 2), (-6, 4), (-1, 1)],
            True
        ),
        (
            multigen_weird,
            [(-2, 0, 2), (-1, 0, 3), (10, 0, 2)],
            [],
            True
        ),
        (
            multigen_23,
            [],
            [(-11, 7), (-3, 2), (-6, 4), (-1, 1)],
            False
        ),
    ]
)
def test_is_superset(
    tuning, pitch_vecs_a, pitch_vecs_b, expected
):
    """
    Test if is_superset operation works correctly
    """

    scale_a = tuning.index_scale(
        [tuning.lattice.point(vec) for vec in pitch_vecs_a]
    )
    scale_b = tuning.index_scale(
        [tuning.lattice.point(vec) for vec in pitch_vecs_b]
    )

    assert scale_a.is_superset(scale_b) is expected


@pytest.mark.parametrize(
    'tuning, pitch_vecs_a, pitch_vecs_b, expected',
    [
        (
            multigen_235,
            [(0, 0, 0), (-11, 7, 0), (-3, 2, 0), (-5, 4, 0)],
            [(0, 0, 0), (-11, 7, 0), (-3, 2, 0)],
            True
        ),
        (
            multigen_235,
            [(0, 0, 0), (-11, 7, 0), (-3, 2, 0), (-5, 4, 0)],
            [(0, 0, 0), (-11, 7, 0), (-4, 2, 0)],
            True
        ),
        (
            multigen_23,
            [(-11, 7), (-3, 2), (-6, 4), (-1, 1)],
            [(-11, 7), (-3, 2), (-6, 4), (-1, 1)],
            True
        ),
        (
            multigen_weird,
            [(-2, 0, 2), (-1, 0, 3), (10, 0, 2)],
            [],
            True
        ),
        (
            multigen_weird,
            [(-2, 0, 2), (-1, 0, 3), (10, 0, 2)],
            [(10, 9, 2)],
            True
        ),
        (
            multigen_23,
            [],
            [(-11, 7), (-3, 2), (-6, 4), (-1, 1)],
            False
        ),
    ]
)
def test_is_superset_ignore_bi_index(
    tuning, pitch_vecs_a, pitch_vecs_b, expected
):
    """
    Test if is_superset operation works correctly
    with ignore_bi_index = True
    """

    scale_a = tuning.index_scale(
        [tuning.lattice.point(vec) for vec in pitch_vecs_a]
    )
    scale_b = tuning.index_scale(
        [tuning.lattice.point(vec) for vec in pitch_vecs_b]
    )

    assert scale_a.is_superset(scale_b, ignore_bi_index=True) is expected


@pytest.mark.parametrize(
    'tuning, pitch_vecs_a, pitch_vecs_b, expected',
    [
        (
            multigen_235,
            [(0, 0, 0), (-11, 7, 0), (-3, 2, 0), (-5, 4, 0)],
            [(0, 0, 0), (-11, 7, 0), (-3, 2, 0)],
            True
        ),
        (
            multigen_235,
            [(0, 0, 0), (-11, 7, 0), (-3, 2, 0), (-5, 4, 0)],
            [(0, 0, 0), (-11, 7, 0), (-4, 2, 0)],
            False
        ),
        (
            multigen_23,
            [(-11, 7), (-3, 2), (-6, 4), (-1, 1)],
            [(-11, 7), (-3, 2), (-6, 4), (-1, 1)],
            False
        ),
        (
            multigen_weird,
            [(-2, 0, 2), (-1, 0, 3), (10, 0, 2)],
            [],
            True
        ),
        (
            multigen_23,
            [],
            [(-11, 7), (-3, 2), (-6, 4), (-1, 1)],
            False
        ),
    ]
)
def test_is_superset_proper(
    tuning, pitch_vecs_a, pitch_vecs_b, expected
):
    """
    Test if is_superset operation works correctly
    """

    scale_a = tuning.index_scale(
        [tuning.lattice.point(vec) for vec in pitch_vecs_a]
    )
    scale_b = tuning.index_scale(
        [tuning.lattice.point(vec) for vec in pitch_vecs_b]
    )

    assert scale_a.is_superset(scale_b, proper=True) is expected


@pytest.mark.parametrize(
    'tuning, pitch_vecs_a, pitch_vecs_b, expected',
    [
        (
            multigen_235,
            [(0, 0, 0), (-11, 7, 0), (-3, 2, 0), (-5, 4, 0)],
            [(0, 0, 0), (-11, 7, 0), (-3, 2, 0)],
            True
        ),
        (
            multigen_235,
            [(0, 0, 0), (-11, 7, 0), (-3, 2, 0), (-5, 4, 0)],
            [(0, 0, 0), (-11, 7, 0), (-4, 2, 0)],
            True
        ),
        (
            multigen_23,
            [(-11, 7), (-3, 2), (-6, 4), (-1, 1)],
            [(-11, 7), (-3, 2), (-6, 4), (-1, 1)],
            False
        ),
        (
            multigen_23,
            [(-11, 7), (-3, 2), (-6, 4), (-1, 1), (-2, 1)],
            [(-11, 7), (-3, 2), (-6, 4), (-1, 1)],
            False
        ),
        (
            multigen_weird,
            [(-2, 0, 2), (-1, 0, 3), (10, 0, 2)],
            [],
            True
        ),
        (
            multigen_23,
            [],
            [(-11, 7), (-3, 2), (-6, 4), (-1, 1)],
            False
        ),
    ]
)
def test_is_superset_proper_ignore_bi_index(
    tuning, pitch_vecs_a, pitch_vecs_b, expected
):
    """
    Test if is_superset operation works correctly
    with proper=True and ignore_bi_index=True
    """

    scale_a = tuning.index_scale(
        [tuning.lattice.point(vec) for vec in pitch_vecs_a]
    )
    scale_b = tuning.index_scale(
        [tuning.lattice.point(vec) for vec in pitch_vecs_b]
    )

    assert scale_a.is_superset(
        scale_b, proper=True, ignore_bi_index=True
    ) is expected


def test_is_superset_incompatible_origin_contexts():
    """
    Test if is_superset operation fails if scales originate
    from different tunings
    """

    ed13_3 = EDTuning(13, FrequencyRatio(3))
    tunings = multigen_23, multigen_25, multigen_weird, ed13_3

    for i, tuning_a in enumerate(tunings):

        for tuning_b in tunings[i+1:]:

            scale_a = tuning_a.scale()
            scale_b = tuning_b.scale()

            with pytest.raises(IncompatibleOriginContexts):
                scale_a.is_superset(scale_b)

            with pytest.raises(IncompatibleOriginContexts):
                scale_a.is_superset(scale_b, proper=True)


@pytest.mark.parametrize(
    'tuning, pitch_vecs, result_vecs',
    [
        (
            multigen_235,
            [(0, 0, 0), (-11, 7, 0), (-3, 2, 0), (-5, 4, 0)],
            [(0, 0, 0), (-11, 7, 0), (-3, 2, 0), (-5, 4, 0)],
        ),
        (
            multigen_235,
            [(2, 1, -4), (-9, 8, -4), (-1, 3, -4), (-3, 5, -4)],
            [(0, 0, 0), (-11, 7, 0), (-3, 2, 0), (-5, 4, 0)],
        ),
        (
            multigen_235,
            [(-1, 0, 2), (-12, 7, 2), (-4, 2, 2), (-6, 4, 2)],
            [(0, 0, 0), (-11, 7, 0), (-3, 2, 0), (-5, 4, 0)],
        ),
        (
            multigen_weird,
            [(-2, 0, 2), (-1, 0, 3), (10, 0, 2)],
            [(0, 0, 0), (1, 0, 1), (12, 0, 0)],
        ),
    ]
)
def test_zero_normalized(
    tuning, pitch_vecs, result_vecs
):
    """
    Test if zero_normalized works correctly
    """

    scale = tuning.index_scale(
        [tuning.lattice.point(vec) for vec in pitch_vecs]
    )
    result = tuning.index_scale(
        [tuning.lattice.point(vec) for vec in result_vecs]
    )

    assert scale.zero_normalized() == result


def test_zero_normalized_value_error():
    """
    Test if zero_normalized raises ValueError if scale is empty
    """

    input_scale = multigen_23.scale()
    with pytest.raises(ValueError) as excinfo:
        input_scale.zero_normalized()
    assert (
        excinfo.value.args[0] ==
        'zero_normalized is not defined on empty scale'
    )


@pytest.mark.parametrize(
    'tuning, pitch_vecs, result',
    [
        (
            multigen_235,
            [(2, 1, -4), (-9, 8, -4), (-1, 3, -4), (-3, 5, -4)],
            False
        ),
        (
            multigen_235,
            [(0, 0, 0), (-11, 7, 0), (-3, 2, 0), (-5, 4, 0)],
            True
        ),
        (
            multigen_235,
            [(-1, 0, 2), (-12, 7, 2), (-4, 2, 2), (-6, 4, 2)],
            False
        ),
        (
            multigen_235,
            [(0, 0, 0), (-11, 7, 0), (-3, 2, 0), (-5, 4, 0)],
            True
        ),
    ]
)
def test_is_zero_normalized(
    tuning, pitch_vecs, result
):
    """
    Test if is_zero_normalized works correctly
    """

    scale = tuning.index_scale(
        [tuning.lattice.point(vec) for vec in pitch_vecs]
    )

    assert scale.is_zero_normalized is result


def test_is_zero_normalized_value_error():
    """
    Test if is_zero_normalized raises ValueError if scale is empty
    """

    input_scale = multigen_235.scale()
    with pytest.raises(ValueError) as excinfo:
        input_scale.is_zero_normalized
    assert (
        excinfo.value.args[0] ==
        'is_zero_normalized is not defined on empty scale'
    )


@pytest.mark.parametrize(
    'tuning, pitch_vecs, source_index, target_index, result_vec',
    [
        (
            multigen_235,
            [(0, 0, 0), (-11, 7, 0), (-3, 2, 0), (-6, 4, 0)],
            0, 2,
            (-3, 2, 0)
        ),
        (
            multigen_23,
            [(-11, 7), (-3, 2), (-6, 4), (-1, 1)],
            1, 3,
            (2, -1)
        ),
        (
            multigen_weird,
            [(-1, 0, 0), (0, 0, 1), (11, 0, 0), (0, 2, 0)],
            1, -1,
            (0, 2, -1)
        ),
        (
            multigen_weird,
            [(-1, 0, 0), (0, 0, 1), (11, 0, 0), (0, 2, 0)],
            -4, -1,
            (1, 2, 0)
        ),
    ]
)
def test_spec_interval(
    tuning, pitch_vecs, source_index, target_index, result_vec
):
    """
    Test if spec_interval method of scales works correctly
    """

    scale = tuning.index_scale(
        [tuning.lattice.point(vec) for vec in pitch_vecs]
    )

    interval = tuning.diff_interval(
        tuning.lattice.point(result_vec)
    )

    assert scale.spec_interval(source_index, target_index) == interval


@pytest.mark.parametrize(
    'tuning, pitch_vecs, bi_diff, result_vecs',
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
            4,
            [(-7, 7), (1, 2), (-2, 4), (3, 1)],
        ),
        (
            multigen_weird,
            [(-1, 0, 0), (0, 0, 1), (11, 0, 0), (0, 2, 0)],
            -2,
            [(-1, -2, 0), (0, -2, 1), (11, -2, 0), (0, 0, 0)],
        ),
        (
            multigen_weird,
            [(-1, 0, 0), (0, 0, 1), (11, 0, 0), (0, 2, 0)],
            3,
            [(-1, 3, 0), (0, 3, 1), (11, 3, 0), (0, 5, 0)],
        ),
    ]
)
def test_transpose_bi_index(
    tuning, pitch_vecs, bi_diff, result_vecs
):
    """
    Test if transpose_bi_index method of scales works correctly
    """

    scale = tuning.index_scale(
        [tuning.lattice.point(vec) for vec in pitch_vecs]
    )
    result_scale = tuning.index_scale(
        [tuning.lattice.point(vec) for vec in result_vecs]
    )

    assert scale.transpose_bi_index(bi_diff) == result_scale


@pytest.mark.parametrize(
    'tuning, pitch_vecs, result_vecs',
    [
        (
            multigen_235,
            [(0, 0, 0), (-11, 7, 0), (-3, 2, 0), (-6, 4, 0)],
            [(0, 0, 0), (-11, 7, 0), (-3, 2, 0), (-6, 4, 0)],
        ),
        (
            multigen_23,
            [(-7, 7), (1, 2), (-2, 4), (3, 1)],
            [(-11, 7), (-3, 2), (-6, 4), (-1, 1)],
        ),
    ]
)
def test_pcs_normalized(
    tuning, pitch_vecs, result_vecs
):
    """
    Test if pcs_normalized method of scales works correctly
    """

    scale = tuning.index_scale(
        [tuning.lattice.point(vec) for vec in pitch_vecs]
    )
    result_scale = tuning.index_scale(
        [tuning.lattice.point(vec) for vec in result_vecs]
    )

    assert scale.pcs_normalized() == result_scale


@pytest.mark.parametrize(
    'tuning, pitch_vecs, expected',
    [
        (
            multigen_235,
            [(0, 0, 0), (-11, 7, 0), (-3, 2, 0), (-6, 4, 0)],
            True
        ),
        (
            multigen_23,
            [(-7, 7), (1, 2), (-2, 4), (3, 1)],
            False,
        ),
        (
            multigen_23,
            [(-11, 7), (-3, 2), (-6, 4), (-1, 1)],
            True
        ),
    ]
)
def test_is_pcs_normalized(
    tuning, pitch_vecs, expected
):
    """
    Test if is_pcs_normalized method of scales works correctly
    """

    scale = tuning.index_scale(
        [tuning.lattice.point(vec) for vec in pitch_vecs]
    )

    assert scale.is_pcs_normalized == expected


@pytest.mark.parametrize(
    'tuning, pitch_vecs, result_vecs',
    [
        (
            multigen_235,
            [(0, 0, 0), (-2, 0, 1), (-1, 1, 0), (-3, 1, 1)],
            [(0, 0, 0), (-2, 0, 1), (-1, 1, 0), (-3, 1, 1)],
        ),
        (
            multigen_235,
            [(0, 0, 0), (-2, 0, 1), (-1, 1, 0), (-3, 1, 1), (1, 0, 0)],
            [(0, 0, 0), (-2, 0, 1), (-1, 1, 0), (-3, 1, 1)],
        ),
        (
            multigen_235,
            [(0, 0, 0), (-2, 0, 1), (-1, 1, 0), (-3, 1, 1), (2, 1, -1)],
            [(0, 0, 0), (-2, 0, 1), (-1, 1, 0), (-3, 1, 1), (1, 1, -1)],
        ),
        (
            multigen_235,
            [(1, 2, 3), (-1, 2, 4), (0, 3, 3), (-2, 3, 4), (3, 3, 2)],
            [(1, 2, 3), (-1, 2, 4), (0, 3, 3), (-2, 3, 4), (2, 3, 2)],
        ),
        (
            multigen_23,
            [(0, 0), (-6, 4), (-1, 1), (-7, 5), (6, -3)],
            [(0, 0), (-6, 4), (-1, 1), (-7, 5), (5, -3)],
        ),
        (
            multigen_23,
            [(0, 0), (-6, 4), (-1, 1), (-7, 5), (6, -3), (-5, 4)],
            [(0, 0), (-6, 4), (-1, 1), (-7, 5), (5, -3)],
        ),
    ]
)
def test_period_normalized(
    tuning, pitch_vecs, result_vecs
):
    """
    Test if period_normalized method of scales works correctly
    """

    scale = tuning.index_scale(
        [tuning.lattice.point(vec) for vec in pitch_vecs]
    )
    result_scale = tuning.index_scale(
        [tuning.lattice.point(vec) for vec in result_vecs]
    )

    assert scale.period_normalized() == result_scale


def test_period_normalized_value_error():
    """
    Test if period_normalized raises ValueError if scale is empty
    """

    input_scale = multigen_235.scale()
    with pytest.raises(ValueError) as excinfo:
        input_scale.period_normalized()
    assert (
        excinfo.value.args[0] ==
        'period_normalized is not defined on empty scale'
    )


@pytest.mark.parametrize(
    'tuning, pitch_vecs, expected',
    [
        (
            multigen_235,
            [(0, 0, 0), (-2, 0, 1), (-1, 1, 0), (-3, 1, 1), (2, 1, -1)],
            False
        ),
        (
            multigen_235,
            [(0, 0, 0), (-2, 0, 1), (-1, 1, 0), (-3, 1, 1), (1, 1, -1)],
            True
        ),
        (
            multigen_235,
            [(1, 2, 3), (-1, 2, 4), (0, 3, 3), (-2, 3, 4), (3, 3, 2)],
            False
        ),
        (
            multigen_235,
            [(1, 2, 3), (-1, 2, 4), (0, 3, 3), (-2, 3, 4), (2, 3, 2)],
            True
        ),
        (
            multigen_23,
            [(0, 0), (-6, 4), (-1, 1), (-7, 5), (6, -3)],
            False
        ),
        (
            multigen_23,
            [(0, 0), (-6, 4), (-1, 1), (-7, 5), (5, -3)],
            True
        ),
        (
            multigen_23,
            [(0, 0), (-6, 4), (-1, 1), (-7, 5), (6, -3), (-5, 4)],
            False
        ),
        (
            multigen_23,
            [(0, 0), (-6, 4), (-1, 1), (-7, 5), (5, -3)],
            True
        ),
    ]
)
def test_is_period_normalized(
    tuning, pitch_vecs, expected
):
    """
    Test if is_period_normalized method of scales works correctly
    """

    scale = tuning.index_scale(
        [tuning.lattice.point(vec) for vec in pitch_vecs]
    )

    assert scale.is_period_normalized == expected


def test_is_period_normalized_value_error():
    """
    Test if is_period_normalized raises ValueError if scale is empty
    """

    input_scale = multigen_235.scale()
    with pytest.raises(ValueError) as excinfo:
        input_scale.is_period_normalized
    assert (
        excinfo.value.args[0] ==
        'is_period_normalized is not defined on empty scale'
    )


@pytest.mark.parametrize(
    'tuning, pitch_vecs, result_vecs',
    [
        (
            multigen_235,
            [(0, 0, 0), (-2, 0, 1), (-1, 1, 0), (-3, 1, 1), (2, 1, -1)],
            [(0, 0, 0), (-2, 0, 1), (-1, 1, 0),
             (-3, 1, 1), (1, 1, -1), (1, 0, 0)],
        ),
        (
            multigen_235,
            [(1, 2, 3), (-1, 2, 4), (0, 3, 3), (-2, 3, 4), (3, 3, 2)],
            [(1, 2, 3), (-1, 2, 4), (0, 3, 3),
             (-2, 3, 4), (2, 3, 2), (2, 2, 3)],
        ),
        (
            multigen_23,
            [(0, 0), (-6, 4), (-1, 1), (-7, 5), (6, -3)],
            [(0, 0), (-6, 4), (-1, 1), (-7, 5), (5, -3), (1, 0)],
        ),
        (
            multigen_23,
            [(0, 0), (-6, 4), (-1, 1), (-7, 5), (6, -3), (-5, 4)],
            [(0, 0), (-6, 4), (-1, 1), (-7, 5), (5, -3), (1, 0)],
        ),
    ]
)
def test_plusone_normalized(
    tuning, pitch_vecs, result_vecs
):
    """
    Test if plusone_normalized method of scales works correctly
    """

    scale = tuning.index_scale(
        [tuning.lattice.point(vec) for vec in pitch_vecs]
    )
    result_scale = tuning.index_scale(
        [tuning.lattice.point(vec) for vec in result_vecs]
    )

    assert scale.plusone_normalized() == result_scale


def test_plusone_normalized_value_error():
    """
    Test if plusone_normalized raises ValueError if scale is empty
    """

    input_scale = multigen_weird.scale()
    with pytest.raises(ValueError) as excinfo:
        input_scale.plusone_normalized()
    assert (
        excinfo.value.args[0] ==
        'plusone_normalized is not defined on empty scale'
    )


@pytest.mark.parametrize(
    'tuning, pitch_vecs, expected',
    [
        (
            multigen_235,
            [(0, 0, 0), (-2, 0, 1), (-1, 1, 0), (-3, 1, 1), (2, 1, -1)],
            False
        ),
        (
            multigen_235,
            [(0, 0, 0), (-2, 0, 1), (-1, 1, 0),
             (-3, 1, 1), (1, 1, -1), (1, 0, 0)],
            True
        ),
        (
            multigen_235,
            [(1, 2, 3), (-1, 2, 4), (0, 3, 3), (-2, 3, 4), (3, 3, 2)],
            False
        ),
        (
            multigen_235,
            [(1, 2, 3), (-1, 2, 4), (0, 3, 3),
             (-2, 3, 4), (2, 3, 2), (2, 2, 3)],
            True
        ),
        (
            multigen_23,
            [(0, 0), (-6, 4), (-1, 1), (-7, 5), (6, -3)],
            False
        ),
        (
            multigen_23,
            [(0, 0), (-6, 4), (-1, 1), (-7, 5), (5, -3), (1, 0)],
            True
        ),
        (
            multigen_23,
            [(0, 0), (-6, 4), (-1, 1), (-7, 5), (6, -3), (-5, 4)],
            False
        ),
        (
            multigen_23,
            [(0, 0), (-6, 4), (-1, 1), (-7, 5), (5, -3), (1, 0)],
            True
        ),
    ]
)
def test_is_plusone_normalized(
    tuning, pitch_vecs, expected
):
    """
    Test if is_plusone_normalized method of scales works correctly
    """

    scale = tuning.index_scale(
        [tuning.lattice.point(vec) for vec in pitch_vecs]
    )

    assert scale.is_plusone_normalized == expected


def test_is_plusone_normalized_value_error():
    """
    Test if is_plusone_normalized raises ValueError if scale is empty
    """

    input_scale = multigen_23.scale()
    with pytest.raises(ValueError) as excinfo:
        input_scale.is_plusone_normalized
    assert (
        excinfo.value.args[0] ==
        'is_plusone_normalized is not defined on empty scale'
    )


@pytest.mark.parametrize(
    'tuning, pitch_vecs, result_vecs',
    [
        (
            multigen_235,
            [(0, 0, 0), (-2, 0, 1), (-1, 1, 0), (-3, 1, 1)],
            [(0, 0, 0), (-2, 0, 1), (-1, 1, 0), (-3, 1, 1)],
        ),
        (
            multigen_235,
            [(0, 0, 0), (-2, 0, 1), (-1, 1, 0), (-3, 1, 1), (2, 1, -1)],
            [(0, 0, 0), (-2, 0, 1), (-1, 1, 0), (-3, 1, 1), (1, 1, -1)],
        ),
        (
            multigen_235,
            [(1, 2, 3), (-1, 2, 4), (0, 3, 3), (-2, 3, 4), (3, 3, 2)],
            [(0, 0, 0), (-2, 0, 1), (-1, 1, 0), (-3, 1, 1), (1, 1, -1)],
        ),
        (
            multigen_23,
            [(0, 2), (-6, 6), (-1, 3), (-7, 7), (6, -1)],
            [(0, 0), (-6, 4), (-1, 1), (-7, 5), (5, -3)],
        ),
        (
            multigen_23,
            [(2, 1), (-4, 5), (1, 2), (-5, 6), (8, -2), (-3, 5)],
            [(0, 0), (-6, 4), (-1, 1), (-7, 5), (5, -3)],
        ),
    ]
)
def test_zp_normalized(
    tuning, pitch_vecs, result_vecs
):
    """
    Test if zp_normalized method of scales works correctly
    """

    scale = tuning.index_scale(
        [tuning.lattice.point(vec) for vec in pitch_vecs]
    )
    result_scale = tuning.index_scale(
        [tuning.lattice.point(vec) for vec in result_vecs]
    )

    assert scale.zp_normalized() == result_scale


def test_zp_normalized_value_error():
    """
    Test if zp_normalized raises ValueError if scale is empty
    """

    input_scale = multigen_weird.scale()
    with pytest.raises(ValueError) as excinfo:
        input_scale.zp_normalized()
    assert (
        excinfo.value.args[0] ==
        'zp_normalized is not defined on empty scale'
    )


@pytest.mark.parametrize(
    'tuning, pitch_vecs, expected',
    [
        (
            multigen_235,
            [(0, 0, 0), (-2, 0, 1), (-1, 1, 0), (-3, 1, 1), (2, 1, -1)],
            False
        ),
        (
            multigen_235,
            [(0, 0, 0), (-2, 0, 1), (-1, 1, 0), (-3, 1, 1), (1, 1, -1)],
            True
        ),
        (
            multigen_235,
            [(1, 2, 3), (-1, 2, 4), (0, 3, 3), (-2, 3, 4), (3, 3, 2)],
            False
        ),
        (
            multigen_235,
            [(0, 0, 0), (-2, 0, 1), (-1, 1, 0), (-3, 1, 1), (1, 1, -1)],
            True
        ),
        (
            multigen_23,
            [(0, 2), (-6, 6), (-1, 3), (-7, 7), (6, -1)],
            False
        ),
        (
            multigen_23,
            [(0, 0), (-6, 4), (-1, 1), (-7, 5), (5, -3)],
            True
        ),
        (
            multigen_23,
            [(2, 1), (-4, 5), (1, 2), (-5, 6), (8, -2), (-3, 5)],
            False
        ),
        (
            multigen_23,
            [(0, 0), (-6, 4), (-1, 1), (-7, 5), (5, -3)],
            True
        ),
    ]
)
def test_is_zp_normalized(
    tuning, pitch_vecs, expected
):
    """
    Test if is_zp_normalized method of scales works correctly
    """

    scale = tuning.index_scale(
        [tuning.lattice.point(vec) for vec in pitch_vecs]
    )

    assert scale.is_zp_normalized == expected


def test_is_zp_normalized_value_error():
    """
    Test if is_zp_normalized raises ValueError if scale is empty
    """

    input_scale = multigen_23.scale()
    with pytest.raises(ValueError) as excinfo:
        input_scale.is_zp_normalized
    assert (
        excinfo.value.args[0] ==
        'is_zp_normalized is not defined on empty scale'
    )


@pytest.mark.parametrize(
    'tuning, pitch_vecs, result_vecs',
    [
        (
            multigen_235,
            [(0, 0, 0), (1, 1, -1), (-2, 0, 1), (-1, 1, 0), (-3, 1, 1)],
            [(1, 1, -1), (-2, 0, 1), (-1, 1, 0), (-3, 1, 1), (1, 0, 0)],
        ),
        (
            multigen_235,
            [(1, 2, 3), (2, 3, 2), (-1, 2, 4), (0, 3, 3), (-2, 3, 4)],
            [(2, 3, 2), (-1, 2, 4), (0, 3, 3), (-2, 3, 4), (2, 2, 3)],
        ),
        (
            multigen_23,
            [(-1, 0), (4, -3), (-7, 4), (-2, 1), (-8, 5)],
            [(4, -3), (-7, 4), (-2, 1), (-8, 5), (0, 0)],
        ),
        (
            multigen_23,
            [(-1, 0), (4, -3), (-7, 4), (-2, 1), (-8, 5), (-6, 4)],
            [(4, -3), (-7, 4), (-2, 1), (-8, 5), (-6, 4), (1, 0)],
        ),
        (
            multigen_23,
            [(0, -3), (5, -6), (-6, 1), (-1, -2), (-7, 2)],
            [(5, -6), (-6, 1), (-1, -2), (-7, 2), (1, -3)],
        ),
    ]
)
def test_rotated_up(
    tuning, pitch_vecs, result_vecs
):
    """
    Test if rotated_up method of scales works correctly
    """

    scale = tuning.index_scale(
        [tuning.lattice.point(vec) for vec in pitch_vecs]
    )
    result_scale = tuning.index_scale(
        [tuning.lattice.point(vec) for vec in result_vecs]
    )

    assert scale.rotated_up() == result_scale


@pytest.mark.parametrize(
    'tuning, pitch_vecs, result_vecs',
    [
        (
            multigen_235,
            [(1, 1, -1), (-2, 0, 1), (-1, 1, 0), (-3, 1, 1), (1, 0, 0)],
            [(0, 0, 0), (1, 1, -1), (-2, 0, 1), (-1, 1, 0), (-3, 1, 1)],
        ),
        (
            multigen_235,
            [(2, 3, 2), (-1, 2, 4), (0, 3, 3), (-2, 3, 4), (2, 2, 3)],
            [(1, 2, 3), (2, 3, 2), (-1, 2, 4), (0, 3, 3), (-2, 3, 4)],
        ),
        (
            multigen_23,
            [(4, -3), (-7, 4), (-2, 1), (-8, 5), (0, 0)],
            [(-1, 0), (4, -3), (-7, 4), (-2, 1), (-8, 5)],
        ),
        (
            multigen_23,
            [(4, -3), (-7, 4), (-2, 1), (-8, 5), (-6, 4), (1, 0)],
            [(-1, 0), (4, -3), (-7, 4), (-2, 1), (-8, 5), (-6, 4)],
        ),
        (
            multigen_23,
            [(5, -6), (-6, 1), (-1, -2), (-7, 2), (1, -3)],
            [(0, -3), (5, -6), (-6, 1), (-1, -2), (-7, 2)],
        ),
    ]
)
def test_rotated_down(
    tuning, pitch_vecs, result_vecs
):
    """
    Test if rotated_down method of scales works correctly
    """

    scale = tuning.index_scale(
        [tuning.lattice.point(vec) for vec in pitch_vecs]
    )
    result_scale = tuning.index_scale(
        [tuning.lattice.point(vec) for vec in result_vecs]
    )

    assert scale.rotated_down() == result_scale


@pytest.mark.parametrize(
    'tuning, pitch_vecs, order, result_vecs',
    [
        (
            multigen_235,
            [(0, 0, 0), (1, 1, -1), (-1, 1, 0), (0, 2, -1)],
            0,
            [(0, 0, 0), (1, 1, -1), (-1, 1, 0), (0, 2, -1)],
        ),
        (
            multigen_235,
            [(0, -2, 0), (1, -1, -1), (-1, -1, 0), (0, 0, -1)],
            -1,
            [(-1, 0, -1), (0, -2, 0), (1, -1, -1), (-1, -1, 0)],
        ),
        (
            multigen_235,
            [(-1, 0, -1), (0, -2, 0), (1, -1, -1), (-1, -1, 0)],
            3,
            [(-1, -1, 0), (0, 0, -1), (1, -2, 0), (2, -1, -1)],
        ),
        (
            multigen_23,
            [(4, -3), (-7, 4), (-2, 1), (-8, 5), (-6, 4), (1, 0)],
            -2,
            [(-8, 4), (-1, 0), (4, -3), (-7, 4), (-2, 1), (-8, 5)],
        ),
        (
            multigen_23,
            [(5, -6), (-6, 1), (-1, -2), (-7, 2), (1, -3)],
            -1,
            [(0, -3), (5, -6), (-6, 1), (-1, -2), (-7, 2)],
        ),
    ]
)
def test_rotation(
    tuning, pitch_vecs, order, result_vecs
):
    """
    Test if rotation method of scales works correctly
    """

    scale = tuning.index_scale(
        [tuning.lattice.point(vec) for vec in pitch_vecs]
    )

    result_scale = tuning.index_scale(
        [tuning.lattice.point(vec) for vec in result_vecs]
    )

    assert scale.rotation(order) == result_scale


@pytest.mark.parametrize(
    'tuning, pitch_vecs, pc_vecs',
    [
        (
            multigen_235,
            [(0, 0, 0), (1, 1, -1), (-1, 1, 0), (0, 2, -1)],
            [(0, 0, 0), (1, 1, -1), (-1, 1, 0), (0, 2, -1)],
        ),
        (
            multigen_235,
            [(0, -2, 0), (1, -1, -1), (-1, -1, 0), (0, 0, -1)],
            [(4, -2, 0), (4, -1, -1), (2, -1, 0), (3, 0, -1)],
        ),
        (
            multigen_235,
            [(-1, 0, -1), (0, -2, 0), (1, -1, -1), (-1, -1, 0)],
            [(3, 0, -1), (4, -2, 0), (4, -1, -1), (2, -1, 0)],
        ),
        (
            multigen_23,
            [(4, -3), (-7, 4), (-2, 1), (-8, 5), (-6, 4), (1, 0)],
            [(5, -3), (-6, 4), (-1, 1), (-7, 5), (-6, 4), (0, 0)],
        ),
    ]
)
def test_pc_indices(tuning, pitch_vecs, pc_vecs):
    """
    Test if pc_indices property works correctly
    """

    scale = tuning.index_scale(
        [tuning.lattice.point(vec) for vec in pitch_vecs]
    )

    assert scale.pc_indices == [
        tuning.lattice.point(vec) for vec in pc_vecs
    ]


@pytest.mark.parametrize(
    'tuning, pitch_vecs_a, pitch_vecs_b, result_vecs',
    [
        (
            multigen_235,
            [(0, 0, 0), (1, 1, -1), (-1, 1, 0), (0, 2, -1)],
            [(0, -2, 0), (1, -1, -1), (-1, -1, 0), (0, 0, -1)],
            []
        ),
        (
            multigen_235,
            [(0, -2, 0), (1, -1, -1), (-1, -1, 0), (0, 0, -1)],
            [(3, -2, 0), (0, -1, -1), (1, -1, 0), (-1, 0, -1)],
            [(4, -2, 0), (4, -1, -1), (2, -1, 0), (3, 0, -1)],
        ),
        (
            multigen_235,
            [(-1, 0, -1), (0, -2, 0), (1, -1, -1), (-1, -1, 0)],
            [(0, 1, -1), (3, -2, 0), (0, -1, 0), (0, -1, 0)],
            [(4, -2, 0), (2, -1, 0)]
        ),
    ]
)
def test_pcs_intersection(
    tuning, pitch_vecs_a, pitch_vecs_b, result_vecs
):
    """
    Test if pcs_intersection method of scales works correctly
    """

    scale_a = tuning.index_scale(
        [tuning.lattice.point(vec) for vec in pitch_vecs_a]
    )
    scale_b = tuning.index_scale(
        [tuning.lattice.point(vec) for vec in pitch_vecs_b]
    )
    result_scale = tuning.index_scale(
        [tuning.lattice.point(vec) for vec in result_vecs]
    )

    assert scale_a.pcs_intersection(scale_b) == result_scale


def test_pcs_intersection_incompatible_origin_contexts():
    """
    Test if pcs_intersection operation fails if scales originate from
    different tunings
    """

    ed13_3 = EDTuning(13, FrequencyRatio(3))
    tunings = multigen_23, multigen_25, multigen_weird, ed13_3

    for i, tuning_a in enumerate(tunings):

        for tuning_b in tunings[i+1:]:

            scale_a = tuning_a.scale()
            scale_b = tuning_b.scale()

            with pytest.raises(IncompatibleOriginContexts):
                scale_a.pcs_intersection(scale_b)


@pytest.mark.parametrize(
    'tuning, pitch_vecs_a, pitch_vecs_b, expected',
    [
        (
            multigen_235,
            [(2, 0, 0), (1, 1, -1), (0, 1, 0), (2, 2, -1)],
            [(0, 0, 0), (1, 1, -1), (-1, 1, 0), (0, 2, -1)],
            True
        ),
        (
            multigen_235,
            [(0, -2, 0), (0, -1, -1), (1, -1, 0), (1, 0, -1)],
            [(4, -2, 0), (4, -1, -1), (2, -1, 0), (3, 0, -1)],
            True
        ),
        (
            multigen_235,
            [(-1, 1, -1), (0, -2, 0), (1, -1, -1), (-1, -1, 0)],
            [(3, 0, -1), (4, -2, 0), (4, -1, -1), (2, -1, 0)],
            False
        ),
        (
            multigen_23,
            [(4, -3), (-7, 4), (-2, 1), (-8, 4), (-6, 4), (1, 0)],
            [(5, -3), (-6, 4), (-1, 1), (-7, 5), (-6, 4), (0, 0)],
            False
        ),
    ]
)
def test_is_set_equivalent(tuning, pitch_vecs_a, pitch_vecs_b, expected):
    """
    Test if is_set_equivalent property works correctly
    """

    scale_a = tuning.index_scale(
        [tuning.lattice.point(vec) for vec in pitch_vecs_a]
    )
    scale_b = tuning.index_scale(
        [tuning.lattice.point(vec) for vec in pitch_vecs_b]
    )

    assert scale_a.is_set_equivalent(scale_b) is expected


@pytest.mark.parametrize(
    'tuning_a, pitch_vecs_a, tuning_b, pitch_vecs_b, expected',
    [
        (
            multigen_235,
            [(2, 0, 0), (1, 1, 0), (0, 1, 0), (2, 2, 0)],
            multigen_23,
            [(0, 0), (1, 1), (-1, 1), (0, 2)],
            True
        ),
        (
            multigen_235,
            [(0, -2, 0), (0, -1, 0), (1, -1, 0), (1, 0, 0)],
            multigen_23,
            [(4, -2), (4, -1), (2, -1), (3, 0)],
            True
        ),
        (
            multigen_235,
            [(-1, 1, 0), (0, -2, 0), (1, -1, 0), (-1, -1, 0)],
            multigen_23,
            [(3, 0), (4, -2), (4, -1), (2, -1)],
            False
        ),
    ]
)
def test_is_set_equivalent_different_tunings(
    tuning_a, pitch_vecs_a, tuning_b, pitch_vecs_b, expected
):
    """
    Test if is_set_equivalent property works correctly
    if scales are from different tunings with
    same equivalency interval
    """

    scale_a = tuning_a.index_scale(
        [tuning_a.lattice.point(vec) for vec in pitch_vecs_a]
    )
    scale_b = tuning_b.index_scale(
        [tuning_b.lattice.point(vec) for vec in pitch_vecs_b]
    )

    assert scale_a.is_set_equivalent(scale_b) is expected


def test_is_set_equivalent_incompatible_origin_contexts():
    """
    Test if is_set_equivalent operation fails if scales originate from
    incompatible tunings
    """

    ed13_3 = EDTuning(13, FrequencyRatio(3))
    tunings = multigen_23, multigen_weird, ed13_3

    for i, tuning_a in enumerate(tunings):

        for tuning_b in tunings[i+1:]:

            scale_a = tuning_a.scale()
            scale_b = tuning_b.scale()

            with pytest.raises(IncompatibleOriginContexts):
                scale_a.is_set_equivalent(scale_b)


@pytest.mark.parametrize(
    'tuning, pitch_vecs_a, pitch_vecs_b, expected',
    [
        (
            multigen_235,
            [(2, 0, 0), (1, 1, -1), (0, 1, 0), (2, 2, -1)],
            [(3, 0, 0), (2, 1, -1), (1, 1, 0), (3, 2, -1)],
            True
        ),
        (
            multigen_235,
            [(0, -2, 0), (0, -1, -1), (1, -1, 0), (1, 0, -1)],
            [(-2, -2, 0), (-2, -1, -1), (-1, -1, 0), (-1, 0, -1)],
            True
        ),
        (
            multigen_235,
            [(-1, 1, -1), (0, -2, 0), (1, -1, -1), (-1, -1, 0)],
            [(4, 1, -1), (1, -2, 0), (6, -1, -1), (4, -1, 0)],
            True
        ),
        (
            multigen_235,
            [(-1, 1, -1), (0, -2, 0), (1, -1, -1), (-1, -1, 0)],
            [(0, 1, -1), (1, -2, 0), (2, -1, -1), (1, -1, 0)],
            False
        ),
        (
            multigen_23,
            [(4, -3), (-7, 4), (-2, 1), (-8, 4), (-6, 4), (1, 0)],
            [(2, -3), (-9, 4), (-4, 1), (-10, 4), (-8, 4), (-1, 0)],
            True
        ),
        (
            multigen_235,
            [(0, -2, 0), (0, -1, -1), (1, -1, 0), (1, 0, -1)],
            [(4, -2, 0), (4, -1, -1), (2, -1, 0), (3, 0, -1)],
            False
        ),
    ]
)
def test_is_seq_equivalent(tuning, pitch_vecs_a, pitch_vecs_b, expected):
    """
    Test if is_seq_equivalent property works correctly
    """

    scale_a = tuning.index_scale(
        [tuning.lattice.point(vec) for vec in pitch_vecs_a]
    )
    scale_b = tuning.index_scale(
        [tuning.lattice.point(vec) for vec in pitch_vecs_b]
    )

    assert scale_a.is_seq_equivalent(scale_b) is expected


@pytest.mark.parametrize(
    'tuning_a, pitch_vecs_a, tuning_b, pitch_vecs_b, expected',
    [
        (
            multigen_235,
            [(2, 0, 0), (1, 1, 0), (0, 1, 0), (2, 2, 0)],
            multigen_23,
            [(0, 0), (-1, 1), (-2, 1), (0, 2)],
            True
        ),
        (
            multigen_235,
            [(0, -2, 0), (0, -1, 0), (1, -1, 0), (1, 0, 0)],
            multigen_23,
            [(4, -2), (4, -1), (5, -1), (5, 0)],
            True
        ),
        (
            multigen_235,
            [(0, -2, 0), (0, -1, 0), (1, -1, 0), (1, 0, 0)],
            multigen_23,
            [(4, -2), (4, -1), (2, -1), (3, 0)],
            False
        ),
        (
            multigen_235,
            [(-1, 1, 0), (0, -2, 0), (1, -1, 0), (-1, -1, 0)],
            multigen_23,
            [(3, 0), (4, -2), (4, -1), (2, -1)],
            False
        ),
    ]
)
def test_is_seq_equivalent_different_tunings(
    tuning_a, pitch_vecs_a, tuning_b, pitch_vecs_b, expected
):
    """
    Test if is_seq_equivalent property works correctly
    if scales are from different tunings with
    same equivalency interval
    """

    scale_a = tuning_a.index_scale(
        [tuning_a.lattice.point(vec) for vec in pitch_vecs_a]
    )
    scale_b = tuning_b.index_scale(
        [tuning_b.lattice.point(vec) for vec in pitch_vecs_b]
    )

    assert scale_a.is_seq_equivalent(scale_b) is expected


def test_is_seq_equivalent_incompatible_origin_contexts():
    """
    Test if is_seq_equivalent operation fails if scales originate from
    incompatible tunings
    """

    ed13_3 = EDTuning(13, FrequencyRatio(3))
    tunings = multigen_23, multigen_weird, ed13_3

    for i, tuning_a in enumerate(tunings):

        for tuning_b in tunings[i+1:]:

            scale_a = tuning_a.scale()
            scale_b = tuning_b.scale()

            with pytest.raises(IncompatibleOriginContexts):
                scale_a.is_seq_equivalent(scale_b)


@pytest.mark.parametrize(
    'tuning, input_vecs, result_vecs',
    [
        (
            multigen_235,
            [(0, 0, 0), (1, 1, -1), (-2, 0, 1)],
            [(1, 1, -1), (-3, -1, 2)],
        ),
        (
            multigen_235,
            [(1, 2, 3), (2, 3, 2), (-1, 2, 4), (0, 3, 3), (-2, 3, 4)],
            [(1, 1, -1), (-3, -1, 2), (1, 1, -1), (-2, 0, 1)],
        ),
        (
            multigen_23,
            [],
            [],
        ),
    ]
)
def test_to_interval_seq(tuning, input_vecs, result_vecs):
    """
    Test if to_interval_seq works correctly
    """

    scale = tuning.scale(
        [tuning.pitch(tuning.lattice.point(vec)) for vec in input_vecs]
    )
    iseq = tuning.diff_interval_seq(
        [tuning.lattice.point(vec) for vec in result_vecs]
    )
    assert scale.to_interval_seq() == iseq


@pytest.mark.parametrize(
    'tuning, input_vecs, result_vecs',
    [
        (
            multigen_235,
            [(0, 0, 0), (1, 1, -1), (-2, 0, 1)],
            [(0, 0, 0), (1, 1, -1), (-2, 0, 1)],
        ),
        (
            multigen_235,
            [(1, 2, 3), (2, 3, 2), (-1, 2, 4), (0, 3, 3), (-2, 3, 4)],
            [(0, 0, 0), (1, 1, -1), (-2, 0, 1), (-1, 1, 0), (-3, 1, 1)],
        ),
        (
            multigen_23,
            [],
            [],
        ),
    ]
)
def test_to_interval_fan_no_param(tuning, input_vecs, result_vecs):
    """
    Test if to_interval_fan works correctly
    without giving a ref parameter
    """

    scale = tuning.scale(
        [tuning.pitch(tuning.lattice.point(vec)) for vec in input_vecs]
    )
    ifan = tuning.diff_interval_fan(
        [tuning.lattice.point(vec) for vec in result_vecs]
    )
    assert scale.to_interval_fan() == ifan


@pytest.mark.parametrize(
    'tuning, input_vecs, ref_pi, result_vecs',
    [
        (
            multigen_235,
            [(0, 0, 0), (1, 1, -1), (-2, 0, 1)],
            (0, 0, 0),
            [(0, 0, 0), (1, 1, -1), (-2, 0, 1)],
        ),
        (
            multigen_235,
            [(1, 2, 3), (2, 3, 2), (-1, 2, 4), (0, 3, 3), (-2, 3, 4)],
            (1, 2, 3),
            [(0, 0, 0), (1, 1, -1), (-2, 0, 1), (-1, 1, 0), (-3, 1, 1)],
        ),
        (
            multigen_235,
            [(1, 2, 3), (2, 3, 2), (-1, 2, 4), (0, 3, 3), (-2, 3, 4)],
            (-1, 1, 0),
            [(2, 1, 3), (3, 2, 2), (0, 1, 4), (1, 2, 3), (-1, 2, 4)],
        ),
        (
            multigen_23,
            [],
            (0, 1),
            [],
        ),
    ]
)
def test_to_interval_fan_reference_param(
    tuning, input_vecs, ref_pi, result_vecs
):
    """
    Test if to_interval_fan works correctly
    with giving reference parameter
    """

    scale = tuning.scale(
        [tuning.pitch(tuning.lattice.point(vec)) for vec in input_vecs]
    )
    ifan = tuning.diff_interval_fan(
        [tuning.lattice.point(vec) for vec in result_vecs]
    )

    ref = tuning.vec_pitch(ref_pi)
    assert scale.to_interval_fan(ref) == ifan


def test_to_interval_fan_incompatible_origin_context():
    """
    Test if to_interval_fan method raises correct error
    when giving incompatible reference parameter
    """

    scale = multigen_235.vec_scale(
        [(0, 0, 0), (1, 2, 3)]
    )

    ref = multigen_23.vec_pitch((1, 2))

    with pytest.raises(IncompatibleOriginContexts) as excinfo:
        scale.to_interval_fan(ref)
    assert (
        excinfo.value.args[0] ==
        f'The ref parameter {ref} does not originate from context '
        f'{scale.origin_context}. Cannot construct interval fan.'
    )
