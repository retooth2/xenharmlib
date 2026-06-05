import pytest
from xenharmlib.core.frequencies import FrequencyRatio
from xenharmlib.core.tunings import EDTuning
from xenharmlib.core.tunings import EDOTuning
from xenharmlib.core.pitch import PitchInterval
from xenharmlib.exc import IncompatibleOriginContexts

edo12 = EDTuning(12, FrequencyRatio(2))
edo24 = EDTuning(24, FrequencyRatio(2))
edo31 = EDTuning(31, FrequencyRatio(2))
ed13_3 = EDTuning(13, FrequencyRatio(3))


@pytest.mark.parametrize(
    'tuning, pitch_index_a, pitch_index_b, pitch_diff',
    [
        (edo31, 2, 8, 6),
        (edo31, 2, -8, -10),
        (edo12, -8, -2, 6),
        (edo24, -1, 26, 27),
    ]
)
def test_init_pitch_diff(tuning,
                         pitch_index_a,
                         pitch_index_b,
                         pitch_diff):
    """
    Test if pitch diff and ref pitch is calculated
    correctly when initializing an interval
    """

    with pytest.deprecated_call():
        interval = PitchInterval.from_pitches(
            tuning.pitch(pitch_index_a),
            tuning.pitch(pitch_index_b),
        )

    interval.ref_pitch == tuning.pitch(pitch_index_a)
    interval.pitch_diff == pitch_diff

    interval = PitchInterval.from_source_and_target(
        tuning.pitch(pitch_index_a),
        tuning.pitch(pitch_index_b),
    )

    interval.ref_pitch == tuning.pitch(pitch_index_a)
    interval.pitch_diff == pitch_diff


@pytest.mark.parametrize(
    'tuning_ab, pitch_index_a, pitch_index_b, '
    'tuning_cd, pitch_index_c, pitch_index_d, ',
    [
        (edo31,  2,  8, edo31,  1,  9),
        (edo31,  2,  8, edo12,  1,  4),
        (edo12,  2, -9, edo12,  2, -8),
    ]
)
def test_lt_gt(tuning_ab,
               pitch_index_a,
               pitch_index_b,
               tuning_cd,
               pitch_index_c,
               pitch_index_d):
    """
    Test if pitch intervals can be compared with lesser-than
    and greater-than relations and if lesser-than and
    greater-than also implies inequality
    """

    with pytest.deprecated_call():
        interval_ab = PitchInterval.from_pitches(
            tuning_ab.pitch(pitch_index_a),
            tuning_ab.pitch(pitch_index_b),
        )
    with pytest.deprecated_call():
        interval_cd = PitchInterval.from_pitches(
            tuning_cd.pitch(pitch_index_c),
            tuning_cd.pitch(pitch_index_d),
        )
    assert interval_ab < interval_cd
    assert interval_cd > interval_ab
    assert interval_ab != interval_cd
    assert interval_cd != interval_ab

    interval_ab = PitchInterval.from_source_and_target(
        tuning_ab.pitch(pitch_index_a),
        tuning_ab.pitch(pitch_index_b),
    )
    interval_cd = PitchInterval.from_source_and_target(
        tuning_cd.pitch(pitch_index_c),
        tuning_cd.pitch(pitch_index_d),
    )
    assert interval_ab < interval_cd
    assert interval_cd > interval_ab
    assert interval_ab != interval_cd
    assert interval_cd != interval_ab


@pytest.mark.parametrize(
    'tuning_ab, pitch_index_a, pitch_index_b, '
    'tuning_cd, pitch_index_c, pitch_index_d, ',
    [
        (edo31,  2,  8, edo31,  2,   8),
        (edo12, -1, -4, edo12, -1,  -4),
        (edo12,  2, -9, edo24,  4, -18),
    ]
)
def test_eq(tuning_ab,
            pitch_index_a,
            pitch_index_b,
            tuning_cd,
            pitch_index_c,
            pitch_index_d):
    """
    Test if two intervals are correctly recognized as
    equal if they have the same frequency ratio
    """

    with pytest.deprecated_call():
        interval_ab = PitchInterval.from_pitches(
            tuning_ab.pitch(pitch_index_a),
            tuning_ab.pitch(pitch_index_b),
        )
    with pytest.deprecated_call():
        interval_cd = PitchInterval.from_pitches(
            tuning_cd.pitch(pitch_index_c),
            tuning_cd.pitch(pitch_index_d),
        )
    assert interval_ab == interval_cd

    interval_ab = PitchInterval.from_source_and_target(
        tuning_ab.pitch(pitch_index_a),
        tuning_ab.pitch(pitch_index_b),
    )
    interval_cd = PitchInterval.from_source_and_target(
        tuning_cd.pitch(pitch_index_c),
        tuning_cd.pitch(pitch_index_d),
    )
    assert interval_ab == interval_cd


@pytest.mark.parametrize(
    'tuning, pitch_index_a, pitch_index_b',
    [
        (edo31,  2,  52),
        (edo12,  1,  9),
        (edo24,  2,  25),
    ]
)
def test_abs(tuning,
             pitch_index_a,
             pitch_index_b):
    """
    Test if abs() value of interval is implemented correctly
    """

    with pytest.deprecated_call():
        interval_a = PitchInterval.from_pitches(
            tuning.pitch(pitch_index_a),
            tuning.pitch(pitch_index_b),
        )
    with pytest.deprecated_call():
        interval_b = PitchInterval.from_pitches(
            tuning.pitch(pitch_index_b),
            tuning.pitch(pitch_index_a),
        )
    assert abs(interval_a) == abs(interval_b)
    assert abs(interval_b) == interval_a

    interval_a = PitchInterval.from_source_and_target(
        tuning.pitch(pitch_index_a),
        tuning.pitch(pitch_index_b),
    )
    interval_b = PitchInterval.from_source_and_target(
        tuning.pitch(pitch_index_b),
        tuning.pitch(pitch_index_a),
    )
    assert abs(interval_a) == abs(interval_b)
    assert abs(interval_b) == interval_a


@pytest.mark.parametrize(
    'tuning, pitch_index_a, pitch_index_b',
    [
        (edo31,  2,  52),
        (edo12,  1,  9),
        (edo24,  2,  25),
    ]
)
def test_neg(tuning,
             pitch_index_a,
             pitch_index_b):
    """
    Test if negative value of interval is implemented correctly
    """

    interval_a = PitchInterval.from_source_and_target(
        tuning.pitch(pitch_index_a),
        tuning.pitch(pitch_index_b),
    )
    interval_b = PitchInterval.from_source_and_target(
        tuning.pitch(pitch_index_b),
        tuning.pitch(pitch_index_a),
    )
    assert -interval_a == interval_b
    assert -interval_b == interval_a


@pytest.mark.parametrize(
    'tuning, pitch_diff_a, pitch_diff_b, result_pitch_diff',
    [
        (edo31,  18,  7, 25),
        (edo12,  16,  0, 16),
        (edo24,  -2,  12, 10),
    ]
)
def test_add(tuning,
             pitch_diff_a,
             pitch_diff_b,
             result_pitch_diff):
    """
    Test if addition on intervals is implemented correctly
    """

    interval_a = tuning.diff_interval(pitch_diff_a)
    interval_b = tuning.diff_interval(pitch_diff_b)
    result_interval = tuning.diff_interval(result_pitch_diff)
    assert interval_a + interval_b == result_interval
    assert interval_b + interval_a == result_interval


@pytest.mark.parametrize(
    'tuning, pitch_diff_a, pitch_diff_b, result_pitch_diff',
    [
        (edo31,  18,  7, 11),
        (edo12,  16,  0, 16),
        (edo12,  0,  3, -3),
        (edo24,  -2,  12, -14),
    ]
)
def test_sub(tuning,
             pitch_diff_a,
             pitch_diff_b,
             result_pitch_diff):
    """
    Test if subtraction on intervals is implemented correctly
    """

    interval_a = tuning.diff_interval(pitch_diff_a)
    interval_b = tuning.diff_interval(pitch_diff_b)
    result_interval = tuning.diff_interval(result_pitch_diff)
    assert interval_a - interval_b == result_interval
    assert interval_b - interval_a == -result_interval


@pytest.mark.parametrize(
    'tuning, pitch_diff, scalar, result_pitch_diff',
    [
        (edo31,  18,  3, 54),
        (edo12,  16,  0, 0),
        (edo12,  0,  3, 0),
        (edo24,  -2,  12, -24),
        (edo24,  9,  -2, -18),
    ]
)
def test_mul(tuning,
             pitch_diff,
             scalar,
             result_pitch_diff):
    """
    Test if scalar multiplication on intervals is implemented correctly
    """

    interval = tuning.diff_interval(pitch_diff)
    result_interval = tuning.diff_interval(result_pitch_diff)
    assert interval * scalar == result_interval
    assert scalar * interval == result_interval


@pytest.mark.parametrize(
    'tuning, pitch_diff, sign',
    [
        (edo31,  18,  1),
        (edo12,  16,  1),
        (edo12,  0,  0),
        (edo24,  -2,  -1),
        (edo24,  -9,  -1),
    ]
)
def test_sign(tuning,
              pitch_diff,
              sign):
    """
    Test if sign property on intervals is implemented correctly
    """

    interval = tuning.diff_interval(pitch_diff)
    assert interval.sign == sign


@pytest.mark.parametrize(
    'tuning, pitch_diff, is_simple',
    [
        (edo31,  18, True),
        (edo31,  -33, False),
        (edo12,  0, True),
        (edo12,  12, True),
        (edo12,  18, False),
        (edo12,  19, False),
        (edo24,  -24, True),
    ]
)
def test_simple_compound(tuning,
                         pitch_diff,
                         is_simple):
    """
    Test if simple and compound property on intervals is implemented correctly
    """

    interval = tuning.diff_interval(pitch_diff)
    assert interval.is_simple == is_simple
    assert interval.is_compound != is_simple


@pytest.mark.parametrize(
    'tuning, pitch_diff, result_pitch_diff',
    [
        (edo31,  18, 18),
        (edo31,  -33, -2),
        (edo12,  0, 0),
        (edo12,  18, 6),
        (edo12,  19, 7),
        (edo24,  -24, -24),
    ]
)
def test_to_simple(tuning,
                   pitch_diff,
                   result_pitch_diff):
    """
    Test if to_simple method on intervals is implemented correctly
    """

    interval = tuning.diff_interval(pitch_diff)
    result_interval = tuning.diff_interval(result_pitch_diff)
    assert interval.to_simple() == result_interval


@pytest.mark.parametrize(
    'tuning, pitch_diff, result_pitch_diff',
    [
        (edo31,  18, 13),
        (edo31,  -33, 64),
        (edo12,  0, 12),
        (edo12,  12, 0),
        (edo12,  18, -6),
        (edo12,  19, -7),
        (edo24,  12, 12),
    ]
)
def test_inversion(tuning,
                   pitch_diff,
                   result_pitch_diff):
    """
    Test if inversion method on intervals is implemented correctly
    """

    interval = tuning.diff_interval(pitch_diff)
    result_interval = tuning.diff_interval(result_pitch_diff)
    assert interval.inversion() == result_interval


@pytest.mark.parametrize(
    'tuning, pitch_diff, result_pitch_diff',
    [
        (edo31,  18, 13),
        (edo31,  -16, 15),
        (edo12,  0, 0),
        (edo12,  18, 6),
        (edo12,  19, 5),
        (edo24,  -22, 2),
    ]
)
def test_ic_normalized(tuning,
                       pitch_diff,
                       result_pitch_diff):
    """
    Test if ic normalization on intervals is implemented correctly
    """

    interval = tuning.diff_interval(pitch_diff)
    result_interval = tuning.diff_interval(result_pitch_diff)
    assert interval.ic_normalized() == result_interval


@pytest.mark.parametrize(
    'tuning, pitch_diff, ic_index',
    [
        (edo31,  18, 13),
        (edo31,  -16, 15),
        (edo12,  0, 0),
        (edo12,  18, 6),
        (edo12,  19, 5),
        (edo24,  -22, 2),
    ]
)
def test_ic_index(tuning,
                  pitch_diff,
                  ic_index):
    """
    Test if ic_index attribute on intervals is implemented correctly
    """

    interval = tuning.diff_interval(pitch_diff)
    assert interval.ic_index == ic_index


@pytest.mark.parametrize(
    'tuning, pitch_index_a, pitch_index_b, cents',
    [
        (edo12, 6, 8, 200),
        (edo12, 1, 9, 800),
        (edo24, 2, 3, 50),
    ]
)
def test_cents(tuning,
               pitch_index_a,
               pitch_index_b,
               cents):
    """
    Test if cent calculation works correctly
    """

    with pytest.deprecated_call():
        interval = PitchInterval.from_pitches(
            tuning.pitch(pitch_index_a),
            tuning.pitch(pitch_index_b),
        )
    assert interval.cents == cents

    interval = PitchInterval.from_source_and_target(
        tuning.pitch(pitch_index_a),
        tuning.pitch(pitch_index_b),
    )
    assert interval.cents == cents


def test_init_incompatible_origin_contexts():
    """
    Test if IncompatibleOriginContexts is raised when trying to form an
    interval from two pitches that originate from different tunings
    """

    edo12_2 = EDTuning(12, FrequencyRatio(2))

    with pytest.raises(IncompatibleOriginContexts):
        with pytest.deprecated_call():
            PitchInterval.from_pitches(
                edo12.pitch(0),
                edo12_2.pitch(0),
            )
    with pytest.raises(IncompatibleOriginContexts):
        PitchInterval.from_source_and_target(
            edo12.pitch(0),
            edo12_2.pitch(0),
        )


@pytest.mark.parametrize(
    'tuning, pitch_index_a, pitch_index_b, repr_result',
    [
        (EDOTuning(31), 2, 8, 'PitchInterval(6, 31-EDO)'),
        (EDOTuning(12), 2, -8, 'PitchInterval(-10, 12-EDO)'),
    ]
)
def test_repr(tuning,
              pitch_index_a,
              pitch_index_b,
              repr_result):
    """
    Test if pitch interval is represented correctly
    """

    with pytest.deprecated_call():
        interval = PitchInterval.from_pitches(
            tuning.pitch(pitch_index_a),
            tuning.pitch(pitch_index_b),
        )
    assert repr(interval) == repr_result

    interval = PitchInterval.from_source_and_target(
        tuning.pitch(pitch_index_a),
        tuning.pitch(pitch_index_b),
    )
    assert repr(interval) == repr_result
