import pytest
from xenharmlib import FrequencyRatio
from xenharmlib import PrimeLimitTuning


@pytest.mark.parametrize(
    'tuning, lp_vec, repr_str',
    [
        (PrimeLimitTuning(5), (-1, 0, 1), 'PrimeLimitPitch(5/2, 5-Limit)'),
        (PrimeLimitTuning(5), (-2, 1, 0), 'PrimeLimitPitch(3/4, 5-Limit)'),
        (PrimeLimitTuning(7), (-2, 1, 0, 1), 'PrimeLimitPitch(21/4, 7-Limit)'),
        (PrimeLimitTuning(3), (-6, 4), 'PrimeLimitPitch(81/64, 3-Limit)'),
    ]

)
def test_repr(tuning, lp_vec, repr_str):
    assert repr(tuning.pitch(tuning.lattice.point(lp_vec))) == repr_str


@pytest.mark.parametrize(
    'tuning, lp_vec, repr_str',
    [
        (PrimeLimitTuning(5), (1, 0, 0), '2'),
        (PrimeLimitTuning(5), (-1, 0, 1), '5/2'),
        (PrimeLimitTuning(5), (-2, 1, 0), '3/4'),
        (PrimeLimitTuning(7), (-2, 1, 0, 1), '21/4'),
        (PrimeLimitTuning(3), (-6, 4), '81/64'),
        (PrimeLimitTuning(3), (0, 1), '3'),
    ]

)
def test_short_repr(tuning, lp_vec, repr_str):
    assert tuning.pitch(tuning.lattice.point(lp_vec)).short_repr == repr_str


@pytest.mark.parametrize(
    'tuning, lp_vec, repr_str',
    [
        (PrimeLimitTuning(5), (1, 0, 0), '1'),
        (PrimeLimitTuning(5), (-1, 0, 1), '5/4'),
        (PrimeLimitTuning(5), (-2, 1, 0), '3/2'),
        (PrimeLimitTuning(7), (-2, 1, 0, 1), '21/16'),
        (PrimeLimitTuning(3), (-6, 4), '81/64'),
        (PrimeLimitTuning(3), (0, 1), '3/2'),
    ]

)
def test_pc_short_repr(tuning, lp_vec, repr_str):
    assert tuning.pitch(tuning.lattice.point(lp_vec)).pc_short_repr == repr_str


@pytest.mark.parametrize(
    'tuning, lp_vec',
    [
        (PrimeLimitTuning(5), (-1, 0, 1)),
        (PrimeLimitTuning(5), (-2, 1, 0)),
        (PrimeLimitTuning(7), (-2, 1, 0, 1)),
        (PrimeLimitTuning(3), (-6, 4)),
    ]

)
def test_monzo(tuning, lp_vec):
    assert tuning.pitch(tuning.lattice.point(lp_vec)).monzo == lp_vec


@pytest.mark.parametrize(
    'tuning, ratio',
    [
        (PrimeLimitTuning(5), FrequencyRatio(5, 4)),
        (PrimeLimitTuning(5), FrequencyRatio(10, 9)),
        (PrimeLimitTuning(7), FrequencyRatio(7, 4)),
        (PrimeLimitTuning(11), FrequencyRatio(10, 11)),
        (PrimeLimitTuning(3), FrequencyRatio(9, 8)),
        (PrimeLimitTuning(3), FrequencyRatio(8, 9)),
    ]
)
def test_ratio_pitch(tuning, ratio):
    pitch = tuning.ratio_pitch(ratio)
    assert tuning.zero_element.interval(pitch).frequency_ratio == ratio


@pytest.mark.parametrize(
    'tuning, ratio',
    [
        (PrimeLimitTuning(5), FrequencyRatio(7, 4)),
        (PrimeLimitTuning(5), FrequencyRatio(14, 9)),
        (PrimeLimitTuning(7), FrequencyRatio(11, 12)),
        (PrimeLimitTuning(11), FrequencyRatio(31, 30)),
        (PrimeLimitTuning(3), FrequencyRatio(10, 8)),
        (PrimeLimitTuning(3), FrequencyRatio(8, 10)),
    ]
)
def test_ratio_pitch_limit_violated(tuning, ratio):

    with pytest.raises(ValueError) as exc_info:
        tuning.ratio_pitch(ratio)
    assert 'surpasses prime limit' in exc_info.value.args[0]


@pytest.mark.parametrize(
    'tuning, ratio_str, ratio',
    [
        (PrimeLimitTuning(5), '5/4', FrequencyRatio(5, 4)),
        (PrimeLimitTuning(5), '10/9', FrequencyRatio(10, 9)),
        (PrimeLimitTuning(7), '7/4', FrequencyRatio(7, 4)),
        (PrimeLimitTuning(7), '3', FrequencyRatio(3)),
        (PrimeLimitTuning(7), '3/1', FrequencyRatio(3)),
        (PrimeLimitTuning(11), '10/11', FrequencyRatio(10, 11)),
        (PrimeLimitTuning(3), '9/8', FrequencyRatio(9, 8)),
        (PrimeLimitTuning(3), '8/9', FrequencyRatio(8, 9)),
    ]
)
def test_rs_pitch(tuning, ratio_str, ratio):
    pitch = tuning.rs_pitch(ratio_str)
    assert tuning.zero_element.interval(pitch).frequency_ratio == ratio


@pytest.mark.parametrize(
    'tuning, ratio_str',
    [
        (PrimeLimitTuning(5), '11/10'),
        (PrimeLimitTuning(5), '7'),
        (PrimeLimitTuning(7), '10/11'),
        (PrimeLimitTuning(7), '31/30'),
        (PrimeLimitTuning(7), '7/23'),
        (PrimeLimitTuning(11), '23/10'),
        (PrimeLimitTuning(3), '5/8'),
        (PrimeLimitTuning(3), '10/9'),
    ]
)
def test_rs_pitch_limit_violated(tuning, ratio_str):

    with pytest.raises(ValueError) as exc_info:
        tuning.rs_pitch(ratio_str)
    assert 'surpasses prime limit' in exc_info.value.args[0]


@pytest.mark.parametrize(
    'tuning, ratio_str',
    [
        (PrimeLimitTuning(5), '11/10/7'),
        (PrimeLimitTuning(5), '7.0'),
        (PrimeLimitTuning(7), 3),
        (PrimeLimitTuning(7), '8/b'),
        (PrimeLimitTuning(7), 'a/23'),
        (PrimeLimitTuning(11), '23.xx/10'),
        (PrimeLimitTuning(3), '5/8**?'),
        (PrimeLimitTuning(3), '10/9/7/9/10/6'),
    ]
)
def test_rs_pitch_bogus(tuning, ratio_str):

    with pytest.raises(ValueError) as exc_info:
        tuning.rs_pitch(ratio_str)
    assert str(ratio_str) in exc_info.value.args[0]
    assert 'is not a valid ratio string expression' in exc_info.value.args[0]
