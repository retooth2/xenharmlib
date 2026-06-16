import operator
import sympy as sp
import pytest
from xenharmlib import EDTuning
from xenharmlib import EDOTuning
from xenharmlib.exc import IncompatibleOriginContexts
from xenharmlib.core.utils import componentwise
from xenharmlib.core.utils import scalar_op
from xenharmlib.core.frequencies import Hz440C0
from xenharmlib.core.frequencies import FrequencyRatio
from xenharmlib.core.multigen import MultiGenTuning


def test_hash_set():

    tuning = MultiGenTuning(
        (FrequencyRatio(2), FrequencyRatio(3)),
        (1, 0)
    )

    test_set = set(
        [
            tuning.pitch(tuning.lattice.point((1, 0))),
            tuning.pitch(tuning.lattice.point((2, 4))),
            tuning.pitch(tuning.lattice.point((3, 1))),
            tuning.pitch(tuning.lattice.point((2, 4))),
        ]
    )

    assert len(test_set) == 3
    assert test_set == set(
        [
            tuning.pitch(tuning.lattice.point((1, 0))),
            tuning.pitch(tuning.lattice.point((2, 4))),
            tuning.pitch(tuning.lattice.point((3, 1))),
        ]
    )


@pytest.mark.parametrize(
    'gen_ratios, period_vec, pitch_vec_a, pitch_vec_b, pitch_diff_vec',
    [
        (
            (FrequencyRatio(2), FrequencyRatio(3)),
            (0, 1),
            (0, 0),
            (0, 0),
            (0, 0),
        ),
        (
            (FrequencyRatio(2), FrequencyRatio(3)),
            (1, 0),
            (0, 1),
            (9, 11),
            (9, 10),
        ),
        (
            (FrequencyRatio(2), FrequencyRatio(3), FrequencyRatio(7)),
            (1, 0, 0),
            (5, 1, 0),
            (0, 0, 0),
            (-5, -1, 0),
        ),
        (
            (
                FrequencyRatio(sp.Integer(2) ** sp.Rational(1, 2)),
                FrequencyRatio(11),
                FrequencyRatio(7)
            ),
            (1, 1, 0),
            (-2, 1, 1),
            (-2, 4, 0),
            (0, 3, -1),
        ),
    ]
)
def test_interval(
    gen_ratios, period_vec, pitch_vec_a, pitch_vec_b, pitch_diff_vec
):

    tuning = MultiGenTuning(
        gen_ratios,
        period_vec
    )

    pitch_index_a = tuning.lattice.point(pitch_vec_a)
    pitch_index_b = tuning.lattice.point(pitch_vec_b)
    pitch_a = tuning.pitch(pitch_index_a)
    pitch_b = tuning.pitch(pitch_index_b)

    result_interval = pitch_a.interval(pitch_b)

    pitch_diff = tuning.lattice.point(pitch_diff_vec)
    expected_interval = tuning.diff_interval(pitch_diff)

    assert result_interval == expected_interval
    assert result_interval.pitch_diff == expected_interval.pitch_diff


@pytest.mark.parametrize(
    'gen_ratios_a, period_vec_a, pitch_vec_a,'
    'gen_ratios_b, period_vec_b, pitch_vec_b',
    [
        (
            (FrequencyRatio(2), FrequencyRatio(3)),
            (1, 0),
            (0, 0),
            (FrequencyRatio(2), FrequencyRatio(3)),
            (1, 0),
            (0, 1),
        ),
        (
            (FrequencyRatio(2), FrequencyRatio(3)),
            (1, 0),
            (4, 1),
            (FrequencyRatio(2), FrequencyRatio(5)),
            (1, 0),
            (2, 2),
        ),
        (
            (FrequencyRatio(2), FrequencyRatio(3), FrequencyRatio(5)),
            (1, 0, 0),
            (4, 1, 1),
            (FrequencyRatio(2), FrequencyRatio(5)),
            (1, 0),
            (4, 2),
        ),
        (
            (FrequencyRatio(2), FrequencyRatio(3), FrequencyRatio(5)),
            (1, 0, 0),
            (-2, 0, 1),
            (FrequencyRatio(2), FrequencyRatio(3)),
            (1, 0),
            (-1, 2),
        ),
    ]
)
def test_lt_gt(
    gen_ratios_a,
    period_vec_a,
    pitch_vec_a,
    gen_ratios_b,
    period_vec_b,
    pitch_vec_b
):

    tuning_a = MultiGenTuning(
        gen_ratios_a,
        period_vec_a
    )
    tuning_b = MultiGenTuning(
        gen_ratios_b,
        period_vec_b
    )

    pitch_a = tuning_a.pitch(tuning_a.lattice.point(pitch_vec_a))
    pitch_b = tuning_b.pitch(tuning_b.lattice.point(pitch_vec_b))

    assert pitch_a < pitch_b
    assert pitch_a <= pitch_b
    assert pitch_b > pitch_a
    assert pitch_b >= pitch_a
    assert pitch_a != pitch_b
    assert pitch_b != pitch_a


@pytest.mark.parametrize(
    'gen_ratios_a, period_vec_a, pitch_vec_a,'
    'gen_ratios_b, period_vec_b, pitch_vec_b',
    [
        (
            (FrequencyRatio(2), FrequencyRatio(3)),
            (1, 0),
            (0, 2),
            (FrequencyRatio(2), FrequencyRatio(9)),
            (1, 0),
            (0, 1),
        ),
        (
            (FrequencyRatio(2), FrequencyRatio(3)),
            (1, 0),
            (1, 1),
            (FrequencyRatio(2), FrequencyRatio(6)),
            (1, 0),
            (0, 1),
        ),
        (
            (FrequencyRatio(2), FrequencyRatio(3), FrequencyRatio(5)),
            (1, 0, 0),
            (4, 0, 1),
            (FrequencyRatio(2), FrequencyRatio(5)),
            (1, 0),
            (4, 1),
        ),
        (
            (FrequencyRatio(2), FrequencyRatio(3), FrequencyRatio(5)),
            (1, 0, 0),
            (-2, 1, 0),
            (FrequencyRatio(2), FrequencyRatio(3)),
            (1, 0),
            (-2, 1),
        ),
    ]
)
def test_eq(
    gen_ratios_a,
    period_vec_a,
    pitch_vec_a,
    gen_ratios_b,
    period_vec_b,
    pitch_vec_b
):

    tuning_a = MultiGenTuning(
        gen_ratios_a,
        period_vec_a
    )
    tuning_b = MultiGenTuning(
        gen_ratios_b,
        period_vec_b
    )

    pitch_a = tuning_a.pitch(tuning_a.lattice.point(pitch_vec_a))
    pitch_b = tuning_b.pitch(tuning_b.lattice.point(pitch_vec_b))

    assert pitch_a == pitch_b
    assert hash(pitch_a) == hash(pitch_b)


@pytest.mark.parametrize(
    'gen_ratios, period_vec, pitch_vec_a, pitch_vec_b',
    [
        (
            (FrequencyRatio(2), FrequencyRatio(3)),
            (1, 0),
            (0, 2),
            (1, 0),
        ),
        (
            (FrequencyRatio(2), FrequencyRatio(3)),
            (1, 0),
            (1, 1),
            (9, 1),
        ),
        (
            (FrequencyRatio(2), FrequencyRatio(3), FrequencyRatio(5)),
            (1, 0, 0),
            (4, 0, 1),
            (4, -1, 7),
        ),
        (
            (FrequencyRatio(2), FrequencyRatio(3), FrequencyRatio(5)),
            (1, 0, 0),
            (-2, 1, 0),
            (0, 0, 0),
        ),
    ]
)
def test_add_sub(gen_ratios, period_vec, pitch_vec_a, pitch_vec_b):

    sum_result = componentwise(
        operator.add,
        pitch_vec_a,
        pitch_vec_b
    )
    diff_result = componentwise(
        operator.sub,
        pitch_vec_a,
        pitch_vec_b
    )

    tuning = MultiGenTuning(
        gen_ratios,
        period_vec
    )

    pitch_a = tuning.pitch(tuning.lattice.point(pitch_vec_a))
    pitch_b = tuning.pitch(tuning.lattice.point(pitch_vec_b))

    sum_pitch = (pitch_a + pitch_b)
    diff_pitch = (pitch_a - pitch_b)

    assert sum_pitch.pitch_index == tuning.pitch(
        tuning.lattice.point(sum_result)
    ).pitch_index

    assert diff_pitch.pitch_index == tuning.pitch(
        tuning.lattice.point(diff_result)
    ).pitch_index


def test_add_sub_incompatible_origin_contexts():

    # __add__ / __sub__ checks for "a is b"
    # object identity so even different
    # tunings with same configuration fail

    tuning_a = MultiGenTuning(
        (FrequencyRatio(3), FrequencyRatio(5)),
        (1, 0)
    )

    tuning_b = MultiGenTuning(
        (FrequencyRatio(3), FrequencyRatio(5)),
        (1, 0)
    )

    pitch_a = tuning_a.pitch(tuning_a.lattice.point((0, 1)))
    pitch_b = tuning_b.pitch(tuning_b.lattice.point((0, 1)))

    with pytest.raises(IncompatibleOriginContexts):
        pitch_a - pitch_b

    with pytest.raises(IncompatibleOriginContexts):
        pitch_a + pitch_b


@pytest.mark.parametrize(
    'gen_ratios, period_vec, pitch_vec, scalar',
    [
        (
            (FrequencyRatio(2), FrequencyRatio(3)),
            (1, 0),
            (0, 2),
            3
        ),
        (
            (FrequencyRatio(2), FrequencyRatio(3)),
            (1, 0),
            (1, 1),
            -3
        ),
        (
            (FrequencyRatio(2), FrequencyRatio(3), FrequencyRatio(5)),
            (1, 0, 0),
            (4, 0, 1),
            0
        ),
        (
            (FrequencyRatio(2), FrequencyRatio(3), FrequencyRatio(5)),
            (1, 0, 0),
            (-2, 1, 0),
            -11
        ),
    ]
)
def test_mul(gen_ratios, period_vec, pitch_vec, scalar):

    mul_result = scalar_op(
        operator.mul,
        pitch_vec,
        scalar
    )

    tuning = MultiGenTuning(
        gen_ratios,
        period_vec
    )

    pitch = tuning.pitch(tuning.lattice.point(pitch_vec))

    mul_pitch = pitch * scalar
    rmul_pitch = scalar * pitch

    assert mul_pitch.pitch_index == tuning.pitch(
        tuning.lattice.point(mul_result)
    ).pitch_index

    assert rmul_pitch.pitch_index == tuning.pitch(
        tuning.lattice.point(mul_result)
    ).pitch_index


@pytest.mark.parametrize(
    'gen_ratios, period_vec, pitch_vec, frequency',
    [
        (
            (FrequencyRatio(2), FrequencyRatio(3)),
            (1, 0),
            (0, 0),
            Hz440C0
        ),
        (
            (FrequencyRatio(2), FrequencyRatio(3)),
            (1, 0),
            (-1, 1),
            Hz440C0 * FrequencyRatio(3, 2)
        ),
        (
            (
                FrequencyRatio(sp.Integer(2) ** sp.Rational(1, 2)),
                FrequencyRatio(11),
                FrequencyRatio(7)
            ),
            (1, 0, 0),
            (2, -1, -1),
            Hz440C0 * FrequencyRatio(2, 77)
        ),
    ]
)
def test_frequency(gen_ratios, period_vec, pitch_vec, frequency):

    tuning = MultiGenTuning(
        gen_ratios,
        period_vec
    )

    pitch = tuning.pitch(tuning.lattice.point(pitch_vec))
    assert pitch.frequency == frequency


@pytest.mark.parametrize(
    'gen_ratios, period_vec, pitch_vec',
    [
        (
            (FrequencyRatio(2), FrequencyRatio(3)),
            (1, 0),
            (0, 0),
        ),
        (
            (FrequencyRatio(2), FrequencyRatio(3)),
            (1, 0),
            (-1, 1),
        ),
        (
            (
                FrequencyRatio(sp.Integer(2) ** sp.Rational(1, 2)),
                FrequencyRatio(11),
                FrequencyRatio(7)
            ),
            (1, 0, 0),
            (2, -1, -1),
        ),
    ]
)
def test_pitch_index(gen_ratios, period_vec, pitch_vec):

    tuning = MultiGenTuning(
        gen_ratios,
        period_vec
    )

    input_pi = tuning.lattice.point(pitch_vec)
    pitch = tuning.pitch(input_pi)
    assert pitch.pitch_index == input_pi


@pytest.mark.parametrize(
    'gen_ratios, period_vec, pitch_vec, pc_index_vec, bi_index',
    [
        (
            (FrequencyRatio(2), FrequencyRatio(3)),
            (1, 0),
            (0, 0),
            (0, 0),
            0
        ),
        (
            (FrequencyRatio(2), FrequencyRatio(3)),
            (1, 0),
            (0, 1),
            (-1, 1),
            1
        ),
        (
            (FrequencyRatio(2), FrequencyRatio(3)),
            (1, 0),
            (5, 1),
            (-1, 1),
            6
        ),
        (
            (
                FrequencyRatio(sp.Integer(2) ** sp.Rational(1, 2)),
                FrequencyRatio(11),
                FrequencyRatio(7)
            ),
            (1, 0, 0),
            (2, 1, 1),
            (-12, 1, 1),
            14
        ),
    ]
)
def test_pc_index_bi_index(
    gen_ratios, period_vec, pitch_vec, pc_index_vec, bi_index
):

    tuning = MultiGenTuning(
        gen_ratios,
        period_vec
    )

    pitch_index = tuning.lattice.point(pitch_vec)
    pc_index = tuning.lattice.point(pc_index_vec)

    pitch = tuning.pitch(pitch_index)
    assert pitch.pc_index == pc_index
    assert pitch.bi_index == bi_index
    assert pitch.pc_index + (
        pitch.bi_index * tuning.period_length
    ) == pitch_index


@pytest.mark.parametrize(
    'gen_ratios, period_vec, pitch_vec, str_repr',
    [
        (
            (FrequencyRatio(2), FrequencyRatio(3)),
            (1, 0),
            (0, 0),
            'MultiGenPitch((0, 0), G=(2, 3))',
        ),
        (
            (FrequencyRatio(2), FrequencyRatio(3)),
            (0, 1),
            (-1, 1),
            'MultiGenPitch((-1, 1), G=(2, 3))',
        ),
        (
            (
                FrequencyRatio(sp.Integer(2) ** sp.Rational(1, 2)),
                FrequencyRatio(11),
                FrequencyRatio(7)
            ),
            (1, 0, 0),
            (2, -1, -1),
            'MultiGenPitch((2, -1, -1), G=(sqrt(2), 11, 7))',
        ),
    ]
)
def test_pitch_repr(gen_ratios, period_vec, pitch_vec, str_repr):

    tuning = MultiGenTuning(
        gen_ratios,
        period_vec
    )

    pitch_index = tuning.lattice.point(pitch_vec)

    pitch = tuning.pitch(pitch_index)
    assert repr(pitch) == str_repr


@pytest.mark.parametrize(
    'gen_ratios, period_vec, pitch_vec, str_repr',
    [
        (
            (FrequencyRatio(2), FrequencyRatio(3)),
            (1, 0),
            (0, 0),
            '(0, 0)',
        ),
        (
            (FrequencyRatio(2), FrequencyRatio(3)),
            (1, 0),
            (0, 1),
            '(0, 1)',
        ),
        (
            (
                FrequencyRatio(sp.Integer(2) ** sp.Rational(1, 2)),
                FrequencyRatio(11),
                FrequencyRatio(7)
            ),
            (1, 0, 0),
            (2, 1, 1),
            '(2, 1, 1)',
        ),
    ]
)
def test_pitch_short_repr(gen_ratios, period_vec, pitch_vec, str_repr):

    tuning = MultiGenTuning(
        gen_ratios,
        period_vec
    )

    pitch_index = tuning.lattice.point(pitch_vec)

    pitch = tuning.pitch(pitch_index)
    assert pitch.short_repr == str_repr


@pytest.mark.parametrize(
    'gen_ratios, period_vec, pitch_vec, axis_vec, result_vec',
    [
        (
            (FrequencyRatio(2), FrequencyRatio(3)),
            (0, 1),
            (0, 0),
            (0, 0),
            (0, 0),
        ),
        (
            (FrequencyRatio(2), FrequencyRatio(3)),
            (1, 0),
            (4, -9),
            (0, 0),
            (-4, 9),
        ),
        (
            (FrequencyRatio(2), FrequencyRatio(3), FrequencyRatio(7)),
            (1, 0, 0),
            (5, 1, 0),
            (9, 1, 1),
            (13, 1, 2),
        ),
        (
            (
                FrequencyRatio(sp.Integer(2) ** sp.Rational(1, 2)),
                FrequencyRatio(11),
                FrequencyRatio(7)
            ),
            (1, 1, 0),
            (-2, 1, 1),
            (0, 3, -1),
            (2, 5, -3),
        ),
    ]
)
def test_reflection(
    gen_ratios, period_vec, pitch_vec, axis_vec, result_vec
):

    tuning = MultiGenTuning(
        gen_ratios,
        period_vec
    )

    pitch_index = tuning.lattice.point(pitch_vec)
    pitch = tuning.pitch(pitch_index)
    axis_index = tuning.lattice.point(axis_vec)
    axis = tuning.pitch(axis_index)
    result_index = tuning.lattice.point(result_vec)
    result = tuning.pitch(result_index)

    reflected = pitch.reflection(axis)
    assert reflected == result
    assert reflected.pitch_index == result.pitch_index


@pytest.mark.parametrize(
    'gen_ratios, period_vec, pitch_vec, result_vec',
    [
        (
            (FrequencyRatio(2), FrequencyRatio(3)),
            (0, 1),
            (0, 0),
            (0, 0),
        ),
        (
            (FrequencyRatio(2), FrequencyRatio(3)),
            (1, 0),
            (4, -9),
            (-4, 9),
        ),
        (
            (FrequencyRatio(2), FrequencyRatio(3), FrequencyRatio(7)),
            (1, 0, 0),
            (5, 1, 0),
            (-5, -1, 0),
        ),
        (
            (
                FrequencyRatio(sp.Integer(2) ** sp.Rational(1, 2)),
                FrequencyRatio(11),
                FrequencyRatio(7)
            ),
            (1, 1, 0),
            (-2, 1, 1),
            (2, -1, -1),
        ),
    ]
)
def test_reflection_default_axis(
    gen_ratios, period_vec, pitch_vec, result_vec
):

    tuning = MultiGenTuning(
        gen_ratios,
        period_vec
    )

    pitch_index = tuning.lattice.point(pitch_vec)
    pitch = tuning.pitch(pitch_index)
    result_index = tuning.lattice.point(result_vec)
    result = tuning.pitch(result_index)

    reflected = pitch.reflection()
    assert reflected == result
    assert reflected.pitch_index == result.pitch_index


@pytest.mark.parametrize(
    'gen_ratios, period_vec, pitch_vec, interval_vecs, result_vecs',
    [
        (
            (FrequencyRatio(2), FrequencyRatio(3)),
            (0, 1),
            (0, 0),
            [(-4, 2), (-3, 2), (-1, 1)],
            [(0, 0), (-4, 2), (-7, 4), (-8, 5)],
        ),
        (
            (FrequencyRatio(2), FrequencyRatio(3)),
            (1, 0),
            (4, -9),
            [(-4, 2), (-3, 2), (-1, 1), (1, 0), (1, 1)],
            [(4, -9), (0, -7), (-3, -5), (-4, -4), (-3, -4), (-2, -3)],
        ),
        (
            (FrequencyRatio(2), FrequencyRatio(3), FrequencyRatio(7)),
            (1, 0, 0),
            (5, 1, 0),
            [(-4, 3, 0), (-4, 3, 0), (-4, 3, 0), (-7, 3, 1)],
            [(5, 1, 0), (1, 4, 0), (-3, 7, 0), (-7, 10, 0), (-14, 13, 1)],
        ),
        (
            (
                FrequencyRatio(sp.Integer(2) ** sp.Rational(1, 2)),
                FrequencyRatio(11),
                FrequencyRatio(7)
            ),
            (1, 1, 0),
            (-2, 1, 1),
            [(-7, 3, 1), (-1, 1, 0), (-4, 3, 0)],
            [(-2, 1, 1), (-9, 4, 2), (-10, 5, 2), (-14, 8, 2)],
        ),
    ]
)
def test_scale(
    gen_ratios, period_vec, pitch_vec, interval_vecs, result_vecs
):

    tuning = MultiGenTuning(
        gen_ratios,
        period_vec
    )

    pitch_index = tuning.lattice.point(pitch_vec)
    pitch = tuning.pitch(pitch_index)

    interval_seq = tuning.interval_seq(
        [tuning.diff_interval(tuning.lattice.point(vec)) for vec in interval_vecs]
    )
    result_scale = tuning.scale(
        [tuning.pitch(tuning.lattice.point(vec)) for vec in result_vecs]
    )

    assert pitch.scale(interval_seq) == result_scale


@pytest.mark.parametrize(
    'gen_ratios, period_vec, pitch_vec, str_repr',
    [
        (
            (FrequencyRatio(2), FrequencyRatio(3)),
            (1, 0),
            (0, 0),
            '(0, 0)',
        ),
        (
            (FrequencyRatio(2), FrequencyRatio(3)),
            (1, 0),
            (0, 1),
            '(-1, 1)',
        ),
        (
            (
                FrequencyRatio(sp.Integer(2) ** sp.Rational(1, 2)),
                FrequencyRatio(11),
                FrequencyRatio(7)
            ),
            (1, 0, 0),
            (2, 1, 1),
            '(-12, 1, 1)',
        ),
    ]
)
def test_pitch_pc_short_repr(gen_ratios, period_vec, pitch_vec, str_repr):

    tuning = MultiGenTuning(
        gen_ratios,
        period_vec
    )

    pitch_index = tuning.lattice.point(pitch_vec)

    pitch = tuning.pitch(pitch_index)
    assert pitch.pc_short_repr == str_repr


@pytest.mark.parametrize(
    'gen_ratios, period_vec, pitch_vec, pitch_diff_vec, result_vec',
    [
        (
            (FrequencyRatio(2), FrequencyRatio(3)),
            (0, 1),
            (0, 0),
            (0, 0),
            (0, 0),
        ),
        (
            (FrequencyRatio(2), FrequencyRatio(3)),
            (1, 0),
            (0, 1),
            (9, 10),
            (9, 11),
        ),
        (
            (FrequencyRatio(2), FrequencyRatio(3), FrequencyRatio(7)),
            (1, 0, 0),
            (5, 1, 0),
            (-5, -1, 0),
            (0, 0, 0),
        ),
        (
            (
                FrequencyRatio(sp.Integer(2) ** sp.Rational(1, 2)),
                FrequencyRatio(11),
                FrequencyRatio(7)
            ),
            (1, 1, 0),
            (-2, 1, 1),
            (0, 3, -1),
            (-2, 4, 0),
        ),
    ]
)
def test_transpose_interval(
    gen_ratios, period_vec, pitch_vec, pitch_diff_vec, result_vec
):

    tuning = MultiGenTuning(
        gen_ratios,
        period_vec
    )

    pitch_index = tuning.lattice.point(pitch_vec)
    pitch_diff = tuning.lattice.point(pitch_diff_vec)

    pitch = tuning.pitch(pitch_index)
    interval = tuning.diff_interval(pitch_diff)

    transposed = pitch.transpose(interval)
    assert transposed.pitch_index == tuning.lattice.point(result_vec)


@pytest.mark.parametrize(
    'gen_ratios, period_vec, pitch_vec, pitch_diff_vec, result_vec',
    [
        (
            (FrequencyRatio(2), FrequencyRatio(3)),
            (0, 1),
            (0, 0),
            (0, 0),
            (0, 0),
        ),
        (
            (FrequencyRatio(2), FrequencyRatio(3)),
            (1, 0),
            (0, 1),
            (9, 10),
            (9, 11),
        ),
        (
            (FrequencyRatio(2), FrequencyRatio(3), FrequencyRatio(7)),
            (1, 0, 0),
            (5, 1, 0),
            (-5, -1, 0),
            (0, 0, 0),
        ),
        (
            (
                FrequencyRatio(sp.Integer(2) ** sp.Rational(1, 2)),
                FrequencyRatio(11),
                FrequencyRatio(7)
            ),
            (1, 1, 0),
            (-2, 1, 1),
            (0, 3, -1),
            (-2, 4, 0),
        ),
    ]
)
def test_transpose_index(
    gen_ratios, period_vec, pitch_vec, pitch_diff_vec, result_vec
):

    tuning = MultiGenTuning(
        gen_ratios,
        period_vec
    )

    pitch_index = tuning.lattice.point(pitch_vec)
    pitch_diff = tuning.lattice.point(pitch_diff_vec)

    pitch = tuning.pitch(pitch_index)

    transposed = pitch.transpose(pitch_diff)
    assert transposed.pitch_index == tuning.lattice.point(result_vec)


@pytest.mark.parametrize(
    'source_tuning, source_vec, target_tuning, target_index',
    [
        (
            MultiGenTuning((FrequencyRatio(2), FrequencyRatio(3)), (1, 0)),
            (-1, 1),
            EDOTuning(31),
            18
        ),
        (
            MultiGenTuning((FrequencyRatio(2), FrequencyRatio(3)), (1, 0)),
            (2, -1),
            EDOTuning(12),
            5
        ),
    ]
)
def test_retune_edo(source_tuning, source_vec, target_tuning, target_index):

    source_index = source_tuning.lattice.point(source_vec)
    source_pitch = source_tuning.pitch(source_index)

    target_pitch = source_pitch.retune(target_tuning)
    assert target_pitch.pitch_index == target_index


def test_retune_incompatible_origin_context():

    tuning_a = MultiGenTuning((FrequencyRatio(2), FrequencyRatio(3)), (1, 0))
    tuning_b = MultiGenTuning((FrequencyRatio(2), FrequencyRatio(5)), (1, 0))
    source_pitch = tuning_a.pitch(tuning_a.lattice.point((2, 1)))

    with pytest.raises(IncompatibleOriginContexts):
        source_pitch.retune(tuning_b)


@pytest.mark.parametrize(
    'gen_ratios, period_vec, pitch_vec, bi_index, result_vec',
    [
        (
            (FrequencyRatio(2), FrequencyRatio(3)),
            (0, 1),
            (0, 0),
            9,
            (0, 9),
        ),
        (
            (FrequencyRatio(2), FrequencyRatio(3)),
            (1, 0),
            (0, 1),
            -3,
            (-3, 1),
        ),
        (
            (FrequencyRatio(2), FrequencyRatio(3), FrequencyRatio(7)),
            (1, 0, 0),
            (5, 1, 0),
            0,
            (5, 1, 0),
        ),
        (
            (
                FrequencyRatio(sp.Integer(2) ** sp.Rational(1, 2)),
                FrequencyRatio(11),
                FrequencyRatio(7)
            ),
            (1, 1, 0),
            (2, 1, 1),
            7,
            (9, 8, 1),
        ),
    ]
)
def test_transpose_bi_index(
    gen_ratios, period_vec, pitch_vec, bi_index, result_vec
):

    tuning = MultiGenTuning(
        gen_ratios,
        period_vec
    )

    pitch_index = tuning.lattice.point(pitch_vec)
    pitch = tuning.pitch(pitch_index)

    transposed = pitch.transpose_bi_index(bi_index)
    assert transposed.pitch_index == tuning.lattice.point(result_vec)


@pytest.mark.parametrize(
    'gen_ratios, period_vec, pitch_vec, norm_vec',
    [
        (
            (FrequencyRatio(2), FrequencyRatio(3)),
            (0, 1),
            (0, 9),
            (0, 0),
        ),
        (
            (FrequencyRatio(2), FrequencyRatio(3)),
            (1, 0),
            (-3, 1),
            (-1, 1),
        ),
        (
            (FrequencyRatio(2), FrequencyRatio(3), FrequencyRatio(7)),
            (1, 0, 0),
            (5, 1, 0),
            (-1, 1, 0),
        ),
        (
            (
                FrequencyRatio(sp.Integer(2) ** sp.Rational(1, 2)),
                FrequencyRatio(11),
                FrequencyRatio(7)
            ),
            (1, 1, 0),
            (9, 8, 1),
            (1, 0, 1),
        ),
    ]
)
def test_pcs_normalized(
    gen_ratios, period_vec, pitch_vec, norm_vec
):

    tuning = MultiGenTuning(
        gen_ratios,
        period_vec
    )

    pitch_index = tuning.lattice.point(pitch_vec)
    pitch = tuning.pitch(pitch_index)

    normalized = pitch.pcs_normalized()
    assert normalized.pitch_index == tuning.lattice.point(norm_vec)


@pytest.mark.parametrize(
    'gen_ratios, period_vec, pitch_a_vec, pitch_b_vec, is_eq',
    [
        (
            (FrequencyRatio(2), FrequencyRatio(3)),
            (0, 1),
            (0, 0),
            (0, 9),
            True
        ),
        (
            (FrequencyRatio(2), FrequencyRatio(3)),
            (1, 0),
            (0, 1),
            (-3, 1),
            True
        ),
        (
            (FrequencyRatio(2), FrequencyRatio(3), FrequencyRatio(7)),
            (1, 0, 0),
            (5, 1, 0),
            (5, 1, 0),
            True
        ),
        (
            (FrequencyRatio(2), FrequencyRatio(3), FrequencyRatio(7)),
            (1, 0, 0),
            (5, 0, 0),
            (5, 1, 0),
            False
        ),
        (
            (
                FrequencyRatio(sp.Integer(2) ** sp.Rational(1, 2)),
                FrequencyRatio(11),
                FrequencyRatio(7)
            ),
            (1, 1, 0),
            (2, 1, 1),
            (9, 8, 1),
            True
        ),
        (
            (
                FrequencyRatio(sp.Integer(2) ** sp.Rational(1, 2)),
                FrequencyRatio(11),
                FrequencyRatio(7)
            ),
            (1, 1, 0),
            (2, 1, 1),
            (10, 8, 1),
            False
        ),
    ]
)
def test_is_equivalent(
    gen_ratios, period_vec, pitch_a_vec, pitch_b_vec, is_eq
):

    tuning = MultiGenTuning(
        gen_ratios,
        period_vec
    )

    pitch_a_index = tuning.lattice.point(pitch_a_vec)
    pitch_a = tuning.pitch(pitch_a_index)
    pitch_b_index = tuning.lattice.point(pitch_b_vec)
    pitch_b = tuning.pitch(pitch_b_index)

    assert (pitch_a.is_equivalent(pitch_b)) is is_eq


@pytest.mark.parametrize(
    'gen_ratios, period_vec, pitch_vec, edo_pitch',
    [
        (
            (FrequencyRatio(2), FrequencyRatio(3)),
            (0, 1),
            (0, 0),
            EDTuning(13, FrequencyRatio(3)).pitch(13),
        ),
        (
            (FrequencyRatio(2), FrequencyRatio(3)),
            (1, 0),
            (3, 0),
            EDOTuning(12).pitch(0),
        ),
    ]
)
def test_is_equivalent_cross_tuning(
    gen_ratios, period_vec, pitch_vec, edo_pitch
):

    tuning = MultiGenTuning(
        gen_ratios,
        period_vec
    )

    pitch_index = tuning.lattice.point(pitch_vec)
    pitch = tuning.pitch(pitch_index)

    assert pitch.is_equivalent(edo_pitch)
