import pytest
from xenharmlib.core.frequencies import FrequencyRatio
from xenharmlib.core.tunings import EDTuning
from xenharmlib.core.tunings import EDOTuning
from xenharmlib.core.pitch import PitchInterval
from xenharmlib.exc import IncompatibleTunings

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

    interval = PitchInterval.from_pitches(
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

    interval_ab = PitchInterval.from_pitches(
        tuning_ab.pitch(pitch_index_a),
        tuning_ab.pitch(pitch_index_b),
    )
    interval_cd = PitchInterval.from_pitches(
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

    interval_ab = PitchInterval.from_pitches(
        tuning_ab.pitch(pitch_index_a),
        tuning_ab.pitch(pitch_index_b),
    )
    interval_cd = PitchInterval.from_pitches(
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

    interval_a = PitchInterval.from_pitches(
        tuning.pitch(pitch_index_a),
        tuning.pitch(pitch_index_b),
    )
    interval_b = PitchInterval.from_pitches(
        tuning.pitch(pitch_index_b),
        tuning.pitch(pitch_index_a),
    )
    assert abs(interval_a) == abs(interval_b)
    assert abs(interval_b) == interval_a


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

    interval = PitchInterval.from_pitches(
        tuning.pitch(pitch_index_a),
        tuning.pitch(pitch_index_b),
    )
    assert interval.cents == cents


def test_init_incompatible_tunings():
    """
    Test if IncompatibleTunings is raised when trying to form an
    interval from two pitches that originate from different tunings
    """

    edo12_2 = EDTuning(12, FrequencyRatio(2))

    with pytest.raises(IncompatibleTunings):
        PitchInterval.from_pitches(
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

    interval = PitchInterval.from_pitches(
        tuning.pitch(pitch_index_a),
        tuning.pitch(pitch_index_b),
    )

    assert repr(interval) == repr_result
