import pytest
import sympy as sp
from xenharmlib.core.frequencies import FrequencyRatio
from xenharmlib.core.multigen import MultiGenTuning


@pytest.mark.parametrize(
    'gen_ratios, period_vec, pitch_vec_a, pitch_vec_b, ratio',
    [
        (
            (FrequencyRatio(2), FrequencyRatio(3)),
            (1, 0),
            (0, 0),
            (0, 0),
            FrequencyRatio(1)
        ),
        (
            (FrequencyRatio(2), FrequencyRatio(3)),
            (1, 0),
            (-1, 1),
            (4, -5),
            FrequencyRatio(32, 729)
        ),
        (
            (
                FrequencyRatio(sp.Integer(2) ** sp.Rational(1, 2)),
                FrequencyRatio(11),
                FrequencyRatio(7)
            ),
            (1, 0, 0),
            (2, -1, -1),
            (2, -1, -1),
            FrequencyRatio(1)
        ),
        (
            (
                FrequencyRatio(sp.Integer(2) ** sp.Rational(1, 2)),
                FrequencyRatio(11),
                FrequencyRatio(7)
            ),
            (1, 0, 0),
            (4, -1, -1),
            (2, -1, -1),
            FrequencyRatio(1, 2)
        ),
    ]
)
def test_frequency_ratio(
    gen_ratios, period_vec, pitch_vec_a, pitch_vec_b, ratio
):

    tuning = MultiGenTuning(
        gen_ratios,
        period_vec
    )

    pitch_a = tuning.pitch(tuning.lattice.point(pitch_vec_a))
    pitch_b = tuning.pitch(tuning.lattice.point(pitch_vec_b))

    interval = tuning.interval(pitch_a, pitch_b)
    assert interval.frequency_ratio == ratio


@pytest.mark.parametrize(
    'gen_ratios, period_vec, pitch_vec_a, pitch_vec_b, interval_vec',
    [
        (
            (FrequencyRatio(2), FrequencyRatio(3)),
            (1, 0),
            (0, 0),
            (0, 0),
            (0, 0),
        ),
        (
            (FrequencyRatio(2), FrequencyRatio(3)),
            (1, 0),
            (-1, 1),
            (4, -5),
            (5, -6),
        ),
        (
            (
                FrequencyRatio(sp.Integer(2) ** sp.Rational(1, 2)),
                FrequencyRatio(11),
                FrequencyRatio(7)
            ),
            (1, 0, 0),
            (2, -1, -1),
            (2, -1, -1),
            (0, 0, 0),
        ),
        (
            (
                FrequencyRatio(sp.Integer(2) ** sp.Rational(1, 2)),
                FrequencyRatio(11),
                FrequencyRatio(7)
            ),
            (1, 0, 0),
            (4, -1, -1),
            (2, -1, -1),
            (-2, 0, 0),
        ),
    ]
)
def test_pitch_diff(
    gen_ratios, period_vec, pitch_vec_a, pitch_vec_b, interval_vec
):

    tuning = MultiGenTuning(
        gen_ratios,
        period_vec
    )

    pitch_a = tuning.pitch(tuning.lattice.point(pitch_vec_a))
    pitch_b = tuning.pitch(tuning.lattice.point(pitch_vec_b))

    interval = tuning.interval(pitch_a, pitch_b)
    assert interval.pitch_diff == tuning.lattice.point(interval_vec)


@pytest.mark.parametrize(
    'gen_ratios_a, period_vec_a, diff_vec_a,'
    'gen_ratios_b, period_vec_b, diff_vec_b',
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
    diff_vec_a,
    gen_ratios_b,
    period_vec_b,
    diff_vec_b
):

    tuning_a = MultiGenTuning(
        gen_ratios_a,
        period_vec_a
    )
    tuning_b = MultiGenTuning(
        gen_ratios_b,
        period_vec_b
    )

    interval_a = tuning_a.diff_interval(tuning_a.lattice.point(diff_vec_a))
    interval_b = tuning_b.diff_interval(tuning_b.lattice.point(diff_vec_b))

    assert interval_a < interval_b
    assert interval_a <= interval_b
    assert interval_b > interval_a
    assert interval_b >= interval_a
    assert interval_a != interval_b
    assert interval_b != interval_a


@pytest.mark.parametrize(
    'gen_ratios_a, period_vec_a, diff_vec_a,'
    'gen_ratios_b, period_vec_b, diff_vec_b',
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
    diff_vec_a,
    gen_ratios_b,
    period_vec_b,
    diff_vec_b
):

    tuning_a = MultiGenTuning(
        gen_ratios_a,
        period_vec_a
    )
    tuning_b = MultiGenTuning(
        gen_ratios_b,
        period_vec_b
    )

    interval_a = tuning_a.diff_interval(tuning_a.lattice.point(diff_vec_a))
    interval_b = tuning_b.diff_interval(tuning_b.lattice.point(diff_vec_b))

    assert interval_a == interval_b


@pytest.mark.parametrize(
    'gen_ratios, period_vec, pitch_vec_a, pitch_vec_b, cents',
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
            (1, 0),
            (0, 1),
            701.9550008654
        ),
        (
            (
                FrequencyRatio(2),
                FrequencyRatio(3),
                FrequencyRatio(5)
            ),
            (1, 0, 0),
            (2, -1, -1),
            (4, -2, -1),
            498.0449991346
        ),
        (
            (
                FrequencyRatio(sp.Integer(2) ** sp.Rational(1, 2)),
                FrequencyRatio(11),
                FrequencyRatio(7)
            ),
            (1, 0, 0),
            (2, -1, -1),
            (4, -1, -1),
            1200
        ),
    ]
)
def test_cents(
    gen_ratios, period_vec, pitch_vec_a, pitch_vec_b, cents
):

    tuning = MultiGenTuning(
        gen_ratios,
        period_vec
    )

    pitch_a = tuning.pitch(tuning.lattice.point(pitch_vec_a))
    pitch_b = tuning.pitch(tuning.lattice.point(pitch_vec_b))

    interval = tuning.interval(pitch_a, pitch_b)
    assert interval.cents == cents


@pytest.mark.parametrize(
    'gen_ratios, period_vec, pitch_vec_a, pitch_vec_b',
    [
        (
            (FrequencyRatio(2), FrequencyRatio(3)),
            (1, 0),
            (0, 0),
            (0, 0),
        ),
        (
            (FrequencyRatio(2), FrequencyRatio(3)),
            (1, 0),
            (-9, 2),
            (4, 1),
        ),
        (
            (
                FrequencyRatio(2),
                FrequencyRatio(3),
                FrequencyRatio(5)
            ),
            (1, 0, 1),
            (2, 6, 3),
            (1, 2, 7),
        ),
        (
            (
                FrequencyRatio(sp.Integer(2) ** sp.Rational(1, 2)),
                FrequencyRatio(11),
                FrequencyRatio(7)
            ),
            (1, 0, 0),
            (-2, 0, 0),
            (2, 0, 0),
        ),
    ]
)
def test_abs(gen_ratios, period_vec, pitch_vec_a, pitch_vec_b):
    """
    Test if abs() value of interval is implemented correctly
    """

    tuning = MultiGenTuning(
        gen_ratios,
        period_vec
    )

    pitch_a = tuning.pitch(tuning.lattice.point(pitch_vec_a))
    pitch_b = tuning.pitch(tuning.lattice.point(pitch_vec_b))

    interval_a = tuning.interval(
        pitch_a,
        pitch_b,
    )
    interval_b = tuning.interval(
        pitch_b,
        pitch_a,
    )
    assert abs(interval_a) == abs(interval_b)
    assert abs(interval_b) == interval_a


@pytest.mark.parametrize(
    'gen_ratios, period_vec, pitch_vec_a, pitch_vec_b',
    [
        (
            (FrequencyRatio(2), FrequencyRatio(3)),
            (1, 0),
            (0, 0),
            (0, 0),
        ),
        (
            (FrequencyRatio(2), FrequencyRatio(3)),
            (1, 0),
            (-9, 2),
            (4, 1),
        ),
        (
            (
                FrequencyRatio(2),
                FrequencyRatio(3),
                FrequencyRatio(5)
            ),
            (1, 0, 1),
            (2, 6, 3),
            (1, 2, 7),
        ),
        (
            (
                FrequencyRatio(sp.Integer(2) ** sp.Rational(1, 2)),
                FrequencyRatio(11),
                FrequencyRatio(7)
            ),
            (1, 0, 0),
            (-2, 0, 0),
            (2, 0, 0),
        ),
    ]
)
def test_neg(gen_ratios, period_vec, pitch_vec_a, pitch_vec_b):
    """
    Test if negation of interval is implemented correctly
    """

    tuning = MultiGenTuning(
        gen_ratios,
        period_vec
    )

    pitch_a = tuning.pitch(tuning.lattice.point(pitch_vec_a))
    pitch_b = tuning.pitch(tuning.lattice.point(pitch_vec_b))

    interval_a = tuning.interval(
        pitch_a,
        pitch_b,
    )
    interval_b = tuning.interval(
        pitch_b,
        pitch_a,
    )
    assert -interval_a == interval_b
    assert -interval_b == interval_a


@pytest.mark.parametrize(
    'gen_ratios, period_vec, diff_vec_a, diff_vec_b, result_vec',
    [
        (
            (FrequencyRatio(2), FrequencyRatio(3)),
            (1, 0),
            (0, 0),
            (0, 0),
            (0, 0),
        ),
        (
            (FrequencyRatio(2), FrequencyRatio(3)),
            (1, 0),
            (-9, 2),
            (4, 1),
            (-5, 3),
        ),
        (
            (
                FrequencyRatio(2),
                FrequencyRatio(3),
                FrequencyRatio(5)
            ),
            (1, 0, 1),
            (2, 6, 3),
            (1, 2, 7),
            (3, 8, 10),
        ),
        (
            (
                FrequencyRatio(sp.Integer(2) ** sp.Rational(1, 2)),
                FrequencyRatio(11),
                FrequencyRatio(7)
            ),
            (1, 0, 0),
            (-2, 0, 0),
            (2, 0, 0),
            (0, 0, 0),
        ),
    ]
)
def test_add(gen_ratios, period_vec, diff_vec_a, diff_vec_b, result_vec):
    """
    Test if addition of intervals is implemented correctly
    """

    tuning = MultiGenTuning(
        gen_ratios,
        period_vec
    )

    interval_a = tuning.diff_interval(tuning.lattice.point(diff_vec_a))
    interval_b = tuning.diff_interval(tuning.lattice.point(diff_vec_b))
    result_interval = tuning.diff_interval(
        tuning.lattice.point(result_vec)
    )

    assert interval_a + interval_b == result_interval
    assert interval_b + interval_a == result_interval


@pytest.mark.parametrize(
    'gen_ratios, period_vec, diff_vec_a, diff_vec_b, result_vec',
    [
        (
            (FrequencyRatio(2), FrequencyRatio(3)),
            (1, 0),
            (0, 0),
            (0, 0),
            (0, 0),
        ),
        (
            (FrequencyRatio(2), FrequencyRatio(3)),
            (1, 0),
            (-9, 2),
            (4, 1),
            (-13, 1),
        ),
        (
            (
                FrequencyRatio(2),
                FrequencyRatio(3),
                FrequencyRatio(5)
            ),
            (1, 0, 1),
            (2, 6, 3),
            (1, 2, 7),
            (1, 4, -4),
        ),
        (
            (
                FrequencyRatio(sp.Integer(2) ** sp.Rational(1, 2)),
                FrequencyRatio(11),
                FrequencyRatio(7)
            ),
            (1, 0, 0),
            (-2, 0, 0),
            (-2, 0, 0),
            (0, 0, 0),
        ),
    ]
)
def test_sub(gen_ratios, period_vec, diff_vec_a, diff_vec_b, result_vec):
    """
    Test if subtraction of intervals is implemented correctly
    """

    tuning = MultiGenTuning(
        gen_ratios,
        period_vec
    )

    interval_a = tuning.diff_interval(tuning.lattice.point(diff_vec_a))
    interval_b = tuning.diff_interval(tuning.lattice.point(diff_vec_b))
    result_interval = tuning.diff_interval(
        tuning.lattice.point(result_vec)
    )

    assert interval_a - interval_b == result_interval
    assert interval_b - interval_a == -result_interval


@pytest.mark.parametrize(
    'gen_ratios, period_vec, diff_vec, scalar, result_vec',
    [
        (
            (FrequencyRatio(2), FrequencyRatio(3)),
            (1, 0),
            (0, 0),
            5,
            (0, 0),
        ),
        (
            (FrequencyRatio(2), FrequencyRatio(3)),
            (1, 0),
            (-9, 2),
            2,
            (-18, 4),
        ),
        (
            (
                FrequencyRatio(2),
                FrequencyRatio(3),
                FrequencyRatio(5)
            ),
            (1, 0, 1),
            (2, 6, -3),
            -3,
            (-6, -18, 9),
        ),
        (
            (
                FrequencyRatio(sp.Integer(2) ** sp.Rational(1, 2)),
                FrequencyRatio(11),
                FrequencyRatio(7)
            ),
            (1, 0, 0),
            (-2, 9, 11),
            0,
            (0, 0, 0),
        ),
    ]
)
def test_mul(gen_ratios, period_vec, diff_vec, scalar, result_vec):
    """
    Test if scalar multiplication of intervals is implemented correctly
    """

    tuning = MultiGenTuning(
        gen_ratios,
        period_vec
    )

    interval = tuning.diff_interval(tuning.lattice.point(diff_vec))
    result_interval = tuning.diff_interval(
        tuning.lattice.point(result_vec)
    )

    assert interval * scalar == result_interval
    assert scalar * interval == result_interval


@pytest.mark.parametrize(
    'gen_ratios, period_vec, diff_vec, sign',
    [
        (
            (FrequencyRatio(2), FrequencyRatio(3)),
            (1, 0),
            (0, 0),
            0,
        ),
        (
            (FrequencyRatio(2), FrequencyRatio(3)),
            (1, 0),
            (-9, 2),
            -1,
        ),
        (
            (
                FrequencyRatio(2),
                FrequencyRatio(3),
                FrequencyRatio(5)
            ),
            (1, 0, 1),
            (2, 6, -3),
            1,
        ),
        (
            (
                FrequencyRatio(sp.Integer(2) ** sp.Rational(1, 2)),
                FrequencyRatio(11),
                FrequencyRatio(7)
            ),
            (1, 0, 0),
            (-2, 9, 11),
            1,
        ),
    ]
)
def test_sign(gen_ratios, period_vec, diff_vec, sign):
    """
    Test if sign property of intervals is implemented correctly
    """

    tuning = MultiGenTuning(
        gen_ratios,
        period_vec
    )

    interval = tuning.diff_interval(tuning.lattice.point(diff_vec))

    assert interval.sign == sign


@pytest.mark.parametrize(
    'gen_ratios, period_vec, diff_vec, str_repr',
    [
        (
            (FrequencyRatio(2), FrequencyRatio(3)),
            (1, 0),
            (0, 0),
            'MultiGenPitchInterval((0, 0), G=(2, 3))',
        ),
        (
            (FrequencyRatio(2), FrequencyRatio(3)),
            (0, 1),
            (-1, 1),
            'MultiGenPitchInterval((-1, 1), G=(2, 3))',
        ),
        (
            (
                FrequencyRatio(sp.Integer(2) ** sp.Rational(1, 2)),
                FrequencyRatio(11),
                FrequencyRatio(7)
            ),
            (1, 0, 0),
            (2, -1, -1),
            'MultiGenPitchInterval((2, -1, -1), G=(sqrt(2), 11, 7))',
        ),
    ]
)
def test_repr(gen_ratios, period_vec, diff_vec, str_repr):

    tuning = MultiGenTuning(
        gen_ratios,
        period_vec
    )

    pitch_diff = tuning.lattice.point(diff_vec)

    interval = tuning.diff_interval(pitch_diff)
    assert repr(interval) == str_repr


@pytest.mark.parametrize(
    'gen_ratios, period_vec, diff_vec, str_repr',
    [
        (
            (FrequencyRatio(2), FrequencyRatio(3)),
            (1, 0),
            (0, 0),
            '(0, 0)',
        ),
        (
            (FrequencyRatio(2), FrequencyRatio(3)),
            (0, 1),
            (-1, 1),
            '(-1, 1)',
        ),
        (
            (
                FrequencyRatio(sp.Integer(2) ** sp.Rational(1, 2)),
                FrequencyRatio(11),
                FrequencyRatio(7)
            ),
            (1, 0, 0),
            (2, -1, -1),
            '(2, -1, -1)',
        ),
    ]
)
def test_short_repr(gen_ratios, period_vec, diff_vec, str_repr):

    tuning = MultiGenTuning(
        gen_ratios,
        period_vec
    )

    pitch_diff = tuning.lattice.point(diff_vec)

    interval = tuning.diff_interval(pitch_diff)
    assert interval.short_repr == str_repr
