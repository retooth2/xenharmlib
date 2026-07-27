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
        multigen_23, multigen_257, multigen_weird
    ]
)
def test_init_empty(tuning):
    """
    Test if seq can be created by omitting pitches parameter
    """

    seq = tuning.seq()

    assert len(seq) == 0
    pitches = list(seq)
    assert pitches == []


def test_init_incompatible_origin_contexts():
    """
    Test if correct exception is raised when pitch from
    different origin context is given to constructor
    """

    with pytest.raises(IncompatibleOriginContexts):
        multigen_257.seq(
            [multigen_235.pitch(multigen_235.lattice.point((0, 0, 0)))]
        )

    with pytest.raises(IncompatibleOriginContexts):
        multigen_weird.seq(
            [multigen_235.pitch(multigen_235.lattice.point((0, 0, 0)))]
        )


def test_eq():
    """
    Test if seq equalities and inequalities work correctly
    """

    seq_a = multigen_23.index_seq(
        [multigen_23.lattice.point(vec) for vec in [(0, 0), (-11, 7), (-3, 2)]]
    )
    seq_b = multigen_23.index_seq(
        [multigen_23.lattice.point(vec) for vec in [(0, 0), (-11, 7), (-3, 2)]]
    )
    seq_c = multigen_23.index_seq(
        [
            multigen_23.lattice.point(vec) for vec in [
                (0, 0), (-11, 7), (-3, 2), (-6, 4)
            ]
        ]
    )

    seq_d = multigen_25.index_seq(
        [multigen_25.lattice.point(vec) for vec in [(0, 0), (-11, 7), (-3, 2)]]
    )
    seq_e = multigen_235.index_seq(
        [
            multigen_235.lattice.point(vec) for vec in [
                (0, 0, 0), (-11, 7, 0), (-3, 2, 0),
            ]
        ]
    )

    assert seq_a == seq_a
    assert seq_a == seq_b
    assert seq_a == seq_e
    assert seq_a != seq_c
    assert seq_a != seq_d

    assert hash(seq_a) == hash(seq_a)
    assert hash(seq_a) == hash(seq_b)
    assert hash(seq_a) == hash(seq_e)
    assert hash(seq_a) != hash(seq_c)
    assert hash(seq_a) != hash(seq_d)

    assert 'XYZ' != seq_a
    assert 3 != seq_a
    assert seq_a != 'XYZ'
    assert seq_a != 3


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

    seq = tuning.index_seq(
        [tuning.lattice.point(vec) for vec in pitch_vecs]
    )

    for i, vec in enumerate(pitch_vecs):
        assert seq[i] == tuning.pitch(tuning.lattice.point(vec))


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
    Test if slicing of seqs works correctly
    """

    seq = tuning.index_seq(
        [tuning.lattice.point(vec) for vec in pitch_vecs]
    )

    for i, vec in enumerate(pitch_vecs):
        assert seq[i] == tuning.pitch(tuning.lattice.point(vec))

    seq = tuning.index_seq(
        [tuning.lattice.point(vec) for vec in pitch_vecs]
    )
    seq_b = tuning.index_seq(
        [tuning.lattice.point(vec) for vec in result_vecs]
    )
    assert seq[start:stop] == seq_b


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
    Test if slicing of seqs works correctly when
    stop parameter is omitted
    """

    seq = tuning.index_seq(
        [tuning.lattice.point(vec) for vec in pitch_vecs]
    )

    for i, vec in enumerate(pitch_vecs):
        assert seq[i] == tuning.pitch(tuning.lattice.point(vec))

    seq = tuning.index_seq(
        [tuning.lattice.point(vec) for vec in pitch_vecs]
    )
    seq_b = tuning.index_seq(
        [tuning.lattice.point(vec) for vec in result_vecs]
    )
    assert seq[start:] == seq_b


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
    Test if slicing of seqs works correctly when
    start parameter is omitted
    """

    seq = tuning.index_seq(
        [tuning.lattice.point(vec) for vec in pitch_vecs]
    )

    for i, vec in enumerate(pitch_vecs):
        assert seq[i] == tuning.pitch(tuning.lattice.point(vec))

    seq = tuning.index_seq(
        [tuning.lattice.point(vec) for vec in pitch_vecs]
    )
    seq_b = tuning.index_seq(
        [tuning.lattice.point(vec) for vec in result_vecs]
    )
    assert seq[:stop] == seq_b


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
    Test if partial function of seqs works correctly
    """

    seq = tuning.index_seq(
        [tuning.lattice.point(vec) for vec in pitch_vecs]
    )

    for i, vec in enumerate(pitch_vecs):
        assert seq[i] == tuning.pitch(tuning.lattice.point(vec))

    seq = tuning.index_seq(
        [tuning.lattice.point(vec) for vec in pitch_vecs]
    )
    seq_b = tuning.index_seq(
        [tuning.lattice.point(vec) for vec in result_vecs]
    )
    assert seq.partial(mask) == seq_b


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
    Test if partial function of seqs raises correct exception
    when invalid mask is given
    """

    seq = tuning.index_seq(
        [tuning.lattice.point(vec) for vec in pitch_vecs]
    )

    with pytest.raises(InvalidIndexMask):
        seq.partial(mask)


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
    Test if partial_not function of seqs works correctly
    """

    seq = tuning.index_seq(
        [tuning.lattice.point(vec) for vec in pitch_vecs]
    )

    for i, vec in enumerate(pitch_vecs):
        assert seq[i] == tuning.pitch(tuning.lattice.point(vec))

    seq = tuning.index_seq(
        [tuning.lattice.point(vec) for vec in pitch_vecs]
    )
    seq_b = tuning.index_seq(
        [tuning.lattice.point(vec) for vec in result_vecs]
    )
    assert seq.partial_not(mask) == seq_b


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
    Test if partial_not function of seqs raises correct exception
    when invalid mask is given
    """

    seq = tuning.index_seq(
        [tuning.lattice.point(vec) for vec in pitch_vecs]
    )

    with pytest.raises(InvalidIndexMask):
        seq.partial_not(mask)


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
    Test if partition function of seqs works correctly
    """

    seq = tuning.index_seq(
        [tuning.lattice.point(vec) for vec in pitch_vecs]
    )

    for i, vec in enumerate(pitch_vecs):
        assert seq[i] == tuning.pitch(tuning.lattice.point(vec))

    positive = seq.partial(mask)
    complement = seq.partial_not(mask)

    assert seq.partition(mask) == (positive, complement)


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
    Test if partition function of seqs raises correct exception
    when invalid mask is given
    """

    seq = tuning.index_seq(
        [tuning.lattice.point(vec) for vec in pitch_vecs]
    )

    with pytest.raises(InvalidIndexMask):
        seq.partition(mask)


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

    seq = tuning.index_seq(
        [tuning.lattice.point(vec) for vec in pitch_vecs]
    )

    for vec in pitch_vecs:
        assert tuning.pitch(tuning.lattice.point(vec)) in seq


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

    seq = tuning.index_seq(
        [tuning.lattice.point(vec) for vec in pitch_vecs]
    )

    for vec in excl_vecs:
        assert tuning.pitch(tuning.lattice.point(vec)) not in seq


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

    seq = tuning.index_seq(
        [tuning.lattice.point(vec) for vec in pitch_vecs]
    )

    for vec in diff_vecs:
        assert tuning.diff_interval(tuning.lattice.point(vec)) in seq


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

    seq = tuning.index_seq(
        [tuning.lattice.point(vec) for vec in pitch_vecs]
    )

    for vec in diff_vecs:
        assert tuning.diff_interval(tuning.lattice.point(vec)) not in seq


@pytest.mark.parametrize(
    'tuning, pitch_vecs, repr_str',
    [
        (
            multigen_235,
            [(0, 0, 0), (-11, 7, 0), (-3, 2, 0), (-6, 4, 0)],
            'MultiGenPitchSeq([(0, 0, 0), (-11, 7, 0), (-3, 2, 0), '
            '(-6, 4, 0)], G=(2, 3, 5))',
        ),
        (
            multigen_23,
            [(-11, 7), (-3, 2), (-6, 4), (-1, 1)],
            'MultiGenPitchSeq([(-11, 7), (-3, 2), (-6, 4), (-1, 1)], '
            'G=(2, 3))'
        ),
    ]
)
def test_repr(tuning, pitch_vecs, repr_str):
    """
    Test if repr() returns the right string for seq
    """

    seq = tuning.index_seq(
        [tuning.lattice.point(vec) for vec in pitch_vecs]
    )

    assert repr(seq) == repr_str


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

    seq = tuning.index_seq(
        [tuning.lattice.point(vec) for vec in pitch_vecs]
    )

    assert seq.frequencies == [
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

    seq = tuning.index_seq(
        [tuning.lattice.point(vec) for vec in pitch_vecs]
    )

    assert seq.pitch_indices == [
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

    seq = tuning.index_seq(
        [tuning.lattice.point(vec) for vec in pitch_vecs]
    )
    interval = tuning.diff_interval(tuning.lattice.point(diff_vec))
    expected_seq = tuning.index_seq(
        [tuning.lattice.point(vec) for vec in result_vecs]
    )

    transposed = seq.transpose(interval)
    assert transposed == expected_seq


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

    seq = tuning.index_seq(
        [tuning.lattice.point(vec) for vec in pitch_vecs]
    )
    expected_seq = tuning.index_seq(
        [tuning.lattice.point(vec) for vec in result_vecs]
    )

    pitch_diff = tuning.lattice.point(diff_vec)
    transposed = seq.transpose(pitch_diff)
    assert transposed == expected_seq


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

    seq = source_tuning.index_seq(
        [source_tuning.lattice.point(vec) for vec in source_vecs]
    )

    retuned = seq.retune_closest(target_tuning)
    assert retuned == target_tuning.index_seq(target_indices)


def test_retune_closest_type_error():
    """
    Test if retune_closest method raises exception on 2+
    dimensional target tuning
    """

    pitch_vecs = [(-1, 1, 0), (-3, 1, 1), (-2, 2, 0)]
    source_seq = multigen_235.index_seq(
        [multigen_235.lattice.point(vec) for vec in pitch_vecs]
    )

    with pytest.raises(TypeError):
        source_seq.retune_closest(multigen_25)


@pytest.mark.parametrize(
    'tuning, pitch_vecs_subseq, pitch_vecs_superseq, index',
    [
        (
            multigen_235,
            [(-11, 7, 0), (-3, 2, 0)],
            [(0, 0, 0), (-11, 7, 0), (-3, 2, 0), (-5, 4, 0)],
            1
        ),
        (
            multigen_23,
            [(-11, 7), (-3, 2), (-6, 4), (-1, 1)],
            [(-11, 7), (-3, 2), (-6, 4), (-1, 1)],
            0
        ),
        (
            multigen_weird,
            [(10, 0, 2)],
            [(-2, 0, 2), (-1, 0, 3), (10, 0, 2)],
            2
        ),
    ]
)
def test_subseq_index(
    tuning, pitch_vecs_subseq, pitch_vecs_superseq, index
):
    """
    Test if subseq_index operation works correctly
    """

    superseq = tuning.index_seq(
        [tuning.lattice.point(vec) for vec in pitch_vecs_superseq]
    )
    subseq = tuning.index_seq(
        [tuning.lattice.point(vec) for vec in pitch_vecs_subseq]
    )

    assert superseq.subseq_index(subseq) == index


@pytest.mark.parametrize(
    'tuning, pitch_vecs_subseq, pitch_vecs_superseq',
    [
        (
            multigen_235,
            [],
            [(0, 0, 0), (-11, 7, 0), (-3, 2, 0), (-5, 4, 0)],
        ),
        (
            multigen_23,
            [],
            [(-11, 7), (-3, 2), (-6, 4), (-1, 1)],
        ),
    ]
)
def test_subseq_index_empty_param(
    tuning, pitch_vecs_subseq, pitch_vecs_superseq
):
    """
    Test if subseq_index operation works correctly
    if parameter is an empty seq
    """

    superseq = tuning.index_seq(
        [tuning.lattice.point(vec) for vec in pitch_vecs_superseq]
    )
    subseq = tuning.index_seq(
        [tuning.lattice.point(vec) for vec in pitch_vecs_subseq]
    )

    with pytest.raises(ValueError) as exc_info:
        superseq.subseq_index(subseq)

    assert exc_info.value.args[0] == (
        'subseq_index is undefined on empty sequence parameter'
    )


@pytest.mark.parametrize(
    'tuning, pitch_vecs_subseq, pitch_vecs_superseq',
    [
        (
            multigen_235,
            [(-5, 4, 1)],
            [(0, 0, 0), (-11, 7, 0), (-3, 2, 0), (-5, 4, 0)],
        ),
        (
            multigen_23,
            [(-11, 7), (-3, 3)],
            [(-11, 7), (-3, 2), (-6, 4), (-1, 1)],
        ),
    ]
)
def test_subseq_index_not_a_subseq(
    tuning, pitch_vecs_subseq, pitch_vecs_superseq
):
    """
    Test if subseq_index operation works correctly
    if parameter is an empty seq
    """

    superseq = tuning.index_seq(
        [tuning.lattice.point(vec) for vec in pitch_vecs_superseq]
    )
    subseq = tuning.index_seq(
        [tuning.lattice.point(vec) for vec in pitch_vecs_subseq]
    )

    with pytest.raises(ValueError) as exc_info:
        superseq.subseq_index(subseq)

    assert exc_info.value.args[0] == 'Given sequence is not a subsequence'


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
def test_is_subseq(
    tuning, pitch_vecs_a, pitch_vecs_b, expected
):
    """
    Test if is_subseq operation works correctly
    """

    seq_a = tuning.index_seq(
        [tuning.lattice.point(vec) for vec in pitch_vecs_a]
    )
    seq_b = tuning.index_seq(
        [tuning.lattice.point(vec) for vec in pitch_vecs_b]
    )

    assert seq_a.is_subseq(seq_b) is expected


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
def test_is_subseq_proper(
    tuning, pitch_vecs_a, pitch_vecs_b, expected
):
    """
    Test if is_subseq operation works correctly
    with proper=True
    """

    seq_a = tuning.index_seq(
        [tuning.lattice.point(vec) for vec in pitch_vecs_a]
    )
    seq_b = tuning.index_seq(
        [tuning.lattice.point(vec) for vec in pitch_vecs_b]
    )

    assert seq_a.is_subseq(seq_b, proper=True) is expected


def test_is_subseq_cross_origin():
    """
    Test if is_subseq works across origin contexts
    """

    seq_a = multigen_235.index_seq(
        [
            multigen_235.lattice.point((0, 1, -1)),
            multigen_235.lattice.point((2, 1, -1)),
            multigen_235.lattice.point((-2, 3, 0)),
            multigen_235.lattice.point((-4, 1, 0)),
            multigen_235.lattice.point((0, 1, -1)),
            multigen_235.lattice.point((1, 1, -1)),
        ]
    )
    seq_b = multigen_23.index_seq(
        [
            multigen_23.lattice.point((-2, 3)),
            multigen_23.lattice.point((-4, 1)),
        ]
    )
    seq_c = multigen_23.index_seq(
        [
            multigen_23.lattice.point((-1, 3)),
            multigen_23.lattice.point((-4, 1)),
        ]
    )

    assert seq_b.is_subseq(seq_a)
    assert not seq_c.is_subseq(seq_a)


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
def test_is_superseq(
    tuning, pitch_vecs_a, pitch_vecs_b, expected
):
    """
    Test if is_superseq operation works correctly
    """

    seq_a = tuning.index_seq(
        [tuning.lattice.point(vec) for vec in pitch_vecs_a]
    )
    seq_b = tuning.index_seq(
        [tuning.lattice.point(vec) for vec in pitch_vecs_b]
    )

    assert seq_a.is_superseq(seq_b) is expected


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
def test_is_superseq_proper(
    tuning, pitch_vecs_a, pitch_vecs_b, expected
):
    """
    Test if is_superseq operation works correctly
    """

    seq_a = tuning.index_seq(
        [tuning.lattice.point(vec) for vec in pitch_vecs_a]
    )
    seq_b = tuning.index_seq(
        [tuning.lattice.point(vec) for vec in pitch_vecs_b]
    )

    assert seq_a.is_superseq(seq_b, proper=True) is expected


def test_is_superseq_cross_origin():
    """
    Test if is_superseq operation works cross origin
    """

    seq_a = multigen_235.index_seq(
        [
            multigen_235.lattice.point((0, 1, -1)),
            multigen_235.lattice.point((2, 1, -1)),
            multigen_235.lattice.point((-2, 3, 0)),
            multigen_235.lattice.point((-4, 1, 0)),
            multigen_235.lattice.point((0, 1, -1)),
            multigen_235.lattice.point((1, 1, -1)),
        ]
    )
    seq_b = multigen_23.index_seq(
        [
            multigen_23.lattice.point((-2, 3)),
            multigen_23.lattice.point((-4, 1)),
        ]
    )
    seq_c = multigen_23.index_seq(
        [
            multigen_23.lattice.point((-1, 3)),
            multigen_23.lattice.point((-4, 1)),
        ]
    )

    assert seq_a.is_superseq(seq_b)
    assert not seq_a.is_superseq(seq_c)


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

    seq = tuning.index_seq(
        [tuning.lattice.point(vec) for vec in pitch_vecs]
    )
    result = tuning.index_seq(
        [tuning.lattice.point(vec) for vec in result_vecs]
    )

    assert seq.zero_normalized() == result


def test_zero_normalized_value_error():
    """
    Test if zero_normalized raises ValueError if seq is empty
    """

    input_seq = multigen_23.seq()
    with pytest.raises(ValueError) as excinfo:
        input_seq.zero_normalized()
    assert (
        excinfo.value.args[0] ==
        'zero_normalized is not defined on empty sequence'
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

    seq = tuning.index_seq(
        [tuning.lattice.point(vec) for vec in pitch_vecs]
    )

    assert seq.is_zero_normalized is result


def test_is_zero_normalized_value_error():
    """
    Test if is_zero_normalized raises ValueError if seq is empty
    """

    input_seq = multigen_235.seq()
    with pytest.raises(ValueError) as excinfo:
        input_seq.is_zero_normalized
    assert (
        excinfo.value.args[0] ==
        'is_zero_normalized is not defined on empty sequence'
    )


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
    Test if transpose_bi_index method of seqs works correctly
    """

    seq = tuning.index_seq(
        [tuning.lattice.point(vec) for vec in pitch_vecs]
    )
    result_seq = tuning.index_seq(
        [tuning.lattice.point(vec) for vec in result_vecs]
    )

    assert seq.transpose_bi_index(bi_diff) == result_seq


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
            [(0, 1, -1), (1, -2, 1), (2, -1, -1), (1, -1, 0)],
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
            [(4, -2, 0), (4, -1, -1), (2, -1, -1), (3, 0, -1)],
            False
        ),
        (
            multigen_235,
            [(0, -2, 0), (0, -1, -1), (1, -1, 0)],
            [(4, -2, 0), (4, -1, -1), (2, -1, -1), (3, 0, -1)],
            False
        ),
    ]
)
def test_is_equivalent(tuning, pitch_vecs_a, pitch_vecs_b, expected):
    """
    Test if is_equivalent property works correctly
    """

    seq_a = tuning.index_seq(
        [tuning.lattice.point(vec) for vec in pitch_vecs_a]
    )
    seq_b = tuning.index_seq(
        [tuning.lattice.point(vec) for vec in pitch_vecs_b]
    )

    assert seq_a.is_equivalent(seq_b) is expected


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
            [(4, -2), (4, -1), (2, -1), (3, 1)],
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
def test_is_equivalent_different_tunings(
    tuning_a, pitch_vecs_a, tuning_b, pitch_vecs_b, expected
):
    """
    Test if is_equivalent property works correctly
    if seqs are from different tunings with
    same equivalency interval
    """

    seq_a = tuning_a.index_seq(
        [tuning_a.lattice.point(vec) for vec in pitch_vecs_a]
    )
    seq_b = tuning_b.index_seq(
        [tuning_b.lattice.point(vec) for vec in pitch_vecs_b]
    )

    assert seq_a.is_equivalent(seq_b) is expected


def test_is_equivalent_incompatible_origin_contexts():
    """
    Test if is_equivalent operation fails if seqs originate from
    incompatible tunings
    """

    ed13_3 = EDTuning(13, FrequencyRatio(3))
    tunings = multigen_23, multigen_weird, ed13_3

    for i, tuning_a in enumerate(tunings):

        for tuning_b in tunings[i+1:]:

            seq_a = tuning_a.seq()
            seq_b = tuning_b.seq()

            with pytest.raises(IncompatibleOriginContexts):
                seq_a.is_equivalent(seq_b)


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

    seq = tuning.seq(
        [tuning.pitch(tuning.lattice.point(vec)) for vec in input_vecs]
    )
    iseq = tuning.diff_interval_seq(
        [tuning.lattice.point(vec) for vec in result_vecs]
    )
    assert seq.to_interval_seq() == iseq


@pytest.mark.parametrize(
    'tuning, pitch_vecs, pitch_vec, result',
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
def test_index(tuning, pitch_vecs, pitch_vec, result):
    """
    Test if index method works correctly
    """

    seq = tuning.index_seq(
        [tuning.lattice.point(vec) for vec in pitch_vecs]
    )

    pitch = tuning.pitch(
        tuning.lattice.point(pitch_vec)
    )

    assert seq.index(pitch) == result


@pytest.mark.parametrize(
    'tuning, pitch_vecs, pitch_vec',
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
def test_index_value_error(tuning, pitch_vecs, pitch_vec):
    """
    Test if index raises ValueError if pitch was not found
    """

    seq = tuning.index_seq(
        [tuning.lattice.point(vec) for vec in pitch_vecs]
    )

    pitch = tuning.pitch(
        tuning.lattice.point(pitch_vec)
    )

    with pytest.raises(ValueError) as excinfo:
        seq.index(pitch)
    assert (
        excinfo.value.args[0] ==
        f'{pitch} is not in sequence'
    )


@pytest.mark.parametrize(
    'tuning, pitch_vecs, pitch_vec, start, result',
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
def test_index_start(tuning, pitch_vecs, pitch_vec, start, result):
    """
    Test if index method works correctly
    with start parameter
    """

    seq = tuning.index_seq(
        [tuning.lattice.point(vec) for vec in pitch_vecs]
    )

    pitch = tuning.pitch(
        tuning.lattice.point(pitch_vec)
    )

    assert seq.index(pitch, start) == result


@pytest.mark.parametrize(
    'tuning, pitch_vecs, pitch_vec, start',
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
def test_index_start_value_error(tuning, pitch_vecs, pitch_vec, start):
    """
    Test if index raises ValueError if pitch was not found
    after a given start value
    """

    seq = tuning.index_seq(
        [tuning.lattice.point(vec) for vec in pitch_vecs]
    )

    pitch = tuning.pitch(
        tuning.lattice.point(pitch_vec)
    )

    with pytest.raises(ValueError) as excinfo:
        seq.index(pitch, start)
    assert (
        excinfo.value.args[0] ==
        f'{pitch} is not in sequence'
    )


@pytest.mark.parametrize(
    'tuning, pitch_vecs, pitch_vec, start, stop, result',
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
def test_index_start_stop(tuning, pitch_vecs, pitch_vec, start, stop, result):
    """
    Test if pitch can be found with index and
    a given start and stop parameter
    """

    seq = tuning.index_seq(
        [tuning.lattice.point(vec) for vec in pitch_vecs]
    )

    pitch = tuning.pitch(
        tuning.lattice.point(pitch_vec)
    )

    assert seq.index(pitch, start, stop) == result


@pytest.mark.parametrize(
    'tuning, pitch_vecs, pitch_vec, start, stop',
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
    tuning, pitch_vecs, pitch_vec, start, stop
):
    """
    Test if pitch can be found with index and
    a given start and stop parameter
    """

    seq = tuning.index_seq(
        [tuning.lattice.point(vec) for vec in pitch_vecs]
    )

    pitch = tuning.pitch(
        tuning.lattice.point(pitch_vec)
    )

    with pytest.raises(ValueError) as excinfo:
        seq.index(pitch, start, stop)
    assert (
        excinfo.value.args[0] ==
        f'{pitch} is not in sequence'
    )


@pytest.mark.parametrize(
    'tuning, pitch_vecs_a, pitch_vecs_b, result_vecs',
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
def test_concatenation(tuning, pitch_vecs_a, pitch_vecs_b, result_vecs):
    """
    Test if 'concatenation' operator works on sequences
    """

    seq_a = tuning.index_seq(
        [tuning.lattice.point(vec) for vec in pitch_vecs_a]
    )

    seq_b = tuning.index_seq(
        [tuning.lattice.point(vec) for vec in pitch_vecs_b]
    )

    result = tuning.index_seq(
        [tuning.lattice.point(vec) for vec in result_vecs]
    )

    assert seq_a + seq_b == result


@pytest.mark.parametrize(
    'tuning, pitch_vecs, scalar, result_vecs',
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
def test_scalar_multiplication(tuning, pitch_vecs, scalar, result_vecs):
    """
    Test if 'scalar multiplication' works on sequences
    """

    seq = tuning.index_seq(
        [tuning.lattice.point(vec) for vec in pitch_vecs]
    )

    result = tuning.index_seq(
        [tuning.lattice.point(vec) for vec in result_vecs]
    )

    assert scalar * seq == result
    assert seq * scalar == result


@pytest.mark.parametrize(
    'tuning, pitch_vecs, new_pitch_vec, result_vecs',
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
def test_with_element(tuning, pitch_vecs, new_pitch_vec, result_vecs):
    """
    Test if with_element works
    """

    seq = tuning.seq(
        [tuning.pitch(tuning.lattice.point(index))
         for index in pitch_vecs]
    )

    seq = seq.with_element(
        tuning.pitch(tuning.lattice.point(new_pitch_vec))
    )

    assert len(seq) == len(result_vecs)
    pitches = list(seq)
    assert pitches == [
        tuning.pitch(tuning.lattice.point(index))
        for index in result_vecs
    ]


@pytest.mark.parametrize(
    'tuning, pitch_vecs, new_pitch_vec, insert_pos, result_vecs',
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
def test_with_element_insert_pos(
    tuning, pitch_vecs, new_pitch_vec, insert_pos, result_vecs
):
    """
    Test if with_element works
    """

    seq = tuning.seq(
        [tuning.pitch(tuning.lattice.point(index))
         for index in pitch_vecs]
    )

    seq = seq.with_element(
        tuning.pitch(tuning.lattice.point(new_pitch_vec)),
        insert_pos
    )

    assert len(seq) == len(result_vecs)
    pitches = list(seq)
    assert pitches == [
        tuning.pitch(tuning.lattice.point(index))
        for index in result_vecs
    ]


def test_with_element_incompatible_origin_contexts():
    """
    Test if with_element raises IncompatibleOriginContexts if argument
    originates from a different tuning
    """

    edo12_2 = EDTuning(12, FrequencyRatio(2))
    tunings = edo12_2, multigen_weird, multigen_235, multigen_25

    for i, tuning_a in enumerate(tunings):

        for tuning_b in tunings[i+1:]:

            seq = tuning_a.seq()

            with pytest.raises(IncompatibleOriginContexts):
                seq.with_element(
                    tuning_b.pitch(
                        tuning_b.zero_index
                    )
                )


@pytest.mark.parametrize(
    'tuning, pitch_vecs, result_vecs',
    [
        (
            multigen_235,
            [(0, 0, 0), (-11, 7, 0), (-3, 2, 0), (-6, 4, 0)],
            [(-6, 4, 0), (-3, 2, 0), (-11, 7, 0), (0, 0, 0)],
        ),
        (
            multigen_weird,
            [(0, 1, 0), (-1, 0, 1), (0, 1, 0)],
            [(0, 1, 0), (-1, 0, 1), (0, 1, 0)],
        ),
        (
            multigen_23,
            [(-11, 7), (-3, 2), (-6, 4), (-1, 1)],
            [(-1, 1), (-6, 4), (-3, 2), (-11, 7)],
        ),
        (
            multigen_23,
            [],
            [],
        ),
    ]
)
def test_retrograde(tuning, pitch_vecs, result_vecs):
    """
    Test if retrograde method works on sequences
    """

    seq = tuning.index_seq(
        [tuning.lattice.point(vec) for vec in pitch_vecs]
    )

    result = tuning.index_seq(
        [tuning.lattice.point(vec) for vec in result_vecs]
    )

    assert seq.retrograde() == result


@pytest.mark.parametrize(
    'tuning, pitch_vecs, result_vecs',
    [
        (
            multigen_235,
            [(0, 0, 0), (-11, 7, 0), (-5, 2, 0), (-6, 4, 1)],
            [(0, 0, 0), (11, -7, 0), (5, -2, 0), (6, -4, -1)],
        ),
        (
            multigen_weird,
            [(0, 1, 0), (-1, 0, 1), (0, 1, 0)],
            [(0, 1, 0), (1, 2, -1), (0, 1, 0)],
        ),
        (
            multigen_23,
            [(-11, 7), (-3, 2), (-6, 4), (-1, 1)],
            [(-11, 7), (-19, 12), (-16, 10), (-21, 13)],
        ),
        (
            multigen_23,
            [],
            [],
        ),
    ]
)
def test_inversion(tuning, pitch_vecs, result_vecs):
    """
    Test if inversion method works on sequences
    """

    seq = tuning.index_seq(
        [tuning.lattice.point(vec) for vec in pitch_vecs]
    )

    result = tuning.index_seq(
        [tuning.lattice.point(vec) for vec in result_vecs]
    )

    assert seq.inversion() == result


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

    seq = tuning.seq(
        [tuning.pitch(tuning.lattice.point(vec)) for vec in input_vecs]
    )
    ifan = tuning.diff_interval_fan(
        [tuning.lattice.point(vec) for vec in result_vecs]
    )
    assert seq.to_interval_fan() == ifan


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

    seq = tuning.seq(
        [tuning.pitch(tuning.lattice.point(vec)) for vec in input_vecs]
    )
    ifan = tuning.diff_interval_fan(
        [tuning.lattice.point(vec) for vec in result_vecs]
    )

    ref = tuning.vec_pitch(ref_pi)
    assert seq.to_interval_fan(ref) == ifan


def test_to_interval_fan_incompatible_origin_context():
    """
    Test if to_interval_fan method raises correct error
    when giving incompatible reference parameter
    """

    seq = multigen_235.seq(
        [
            multigen_235.pitch(multigen_235.lattice.point(vec))
            for vec in [(0, 0, 0), (1, 2, 3)]
         ]
    )

    ref = multigen_23.vec_pitch((1, 2))

    with pytest.raises(IncompatibleOriginContexts) as excinfo:
        seq.to_interval_fan(ref)
    assert (
        excinfo.value.args[0] ==
        f'The ref parameter {ref} does not originate from context '
        f'{seq.origin_context}. Cannot construct interval fan.'
    )
