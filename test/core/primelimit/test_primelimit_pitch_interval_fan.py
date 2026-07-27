import pytest
from xenharmlib import FrequencyRatio
from xenharmlib import PrimeLimitTuning


@pytest.mark.parametrize(
    'tuning, lp_vecs, repr_str',
    [
        (
            PrimeLimitTuning(5),
            [(1, -2, 1), (-2, 0, 1), (-1, 1, 0)],
            'PrimeLimitPitchIntervalFan([10/9, 5/4, 3/2], 5-Limit)'
        ),
        (
            PrimeLimitTuning(5),
            [(0, 0, 0), (-2, 0, 1), (2, -1, 0)],
            'PrimeLimitPitchIntervalFan([1, 5/4, 4/3], 5-Limit)'
        ),
        (
            PrimeLimitTuning(7),
            [(1, -2, 1, 0), (-2, 0, 1, 0), (-2, 0, 0, 1)],
            'PrimeLimitPitchIntervalFan([10/9, 5/4, 7/4], 7-Limit)'
        ),
        (
            PrimeLimitTuning(3),
            [(1, -2), (-2, 0), (-1, 1)],
            'PrimeLimitPitchIntervalFan([2/9, 1/4, 3/2], 3-Limit)'
        ),
        (
            PrimeLimitTuning(31),
            [],
            'PrimeLimitPitchIntervalFan([], 31-Limit)'
        ),
    ]
)
def test_repr(tuning, lp_vecs, repr_str):
    assert repr(
        tuning.diff_interval_fan(
            [tuning.lattice.point(lp_vec) for lp_vec in lp_vecs]
        )
    ) == repr_str


@pytest.mark.parametrize(
    'tuning, lp_vecs',
    [
        (
            PrimeLimitTuning(5),
            [(1, -2, 1), (-2, 0, 1), (-1, 1, 0)],
        ),
        (
            PrimeLimitTuning(5),
            [(0, 0, 0), (-2, 0, 1), (2, -1, 0)],
        ),
        (
            PrimeLimitTuning(7),
            [(1, -2, 1, 0), (-2, 0, 1, 0), (-2, 0, 0, 1)],
        ),
        (
            PrimeLimitTuning(3),
            [(1, -2), (-2, 0), (-1, 1)],
        ),
        (
            PrimeLimitTuning(31),
            [],
        ),
    ]
)
def test_monzos(tuning, lp_vecs):
    assert tuning.diff_interval_fan(
        [tuning.lattice.point(lp_vec) for lp_vec in lp_vecs]
    ).monzos == lp_vecs


def test_ratio_interval_fan_no_param():
    ifan = PrimeLimitTuning(5).ratio_interval_fan()
    assert len(ifan) == 0
    assert ifan.pitch_diffs == []


@pytest.mark.parametrize(
    'tuning, ratios',
    [
        (
            PrimeLimitTuning(5),
            [
                FrequencyRatio(10, 9),
                FrequencyRatio(5, 4),
                FrequencyRatio(3, 2),
            ]
        ),
        (
            PrimeLimitTuning(5),
            [
                FrequencyRatio(1, 1),
                FrequencyRatio(5, 4),
                FrequencyRatio(4, 3),
            ]
        ),
        (
            PrimeLimitTuning(7),
            [
                FrequencyRatio(10, 9),
                FrequencyRatio(5, 4),
                FrequencyRatio(7, 4),
            ]
        ),
        (
            PrimeLimitTuning(3),
            [
                FrequencyRatio(2, 9),
                FrequencyRatio(1, 4),
                FrequencyRatio(3, 2),
            ]
        ),
        (
            PrimeLimitTuning(31),
            [],
        ),
    ]
)
def test_ratio_interval_fan(tuning, ratios):
    ifan = tuning.ratio_interval_fan(ratios)
    assert [interval.frequency_ratio for interval in ifan] == ratios


@pytest.mark.parametrize(
    'tuning, ratios',
    [
        (
            PrimeLimitTuning(5),
            [
                FrequencyRatio(10, 9),
                FrequencyRatio(7, 8),
                FrequencyRatio(3, 2),
            ]
        ),
        (
            PrimeLimitTuning(5),
            [
                FrequencyRatio(1, 1),
                FrequencyRatio(5, 4),
                FrequencyRatio(31, 20),
            ]
        ),
        (
            PrimeLimitTuning(7),
            [
                FrequencyRatio(10, 9),
                FrequencyRatio(5, 4),
                FrequencyRatio(77, 40),
            ]
        ),
        (
            PrimeLimitTuning(3),
            [
                FrequencyRatio(9, 5),
                FrequencyRatio(3, 2),
            ]
        ),
    ]
)
def test_ratio_interval_fan_limit_violated(tuning, ratios):

    with pytest.raises(ValueError) as exc_info:
        tuning.ratio_interval_fan(ratios)
    assert 'surpasses prime limit' in exc_info.value.args[0]


@pytest.mark.parametrize(
    'tuning, ratio_strs, ratios',
    [
        (
            PrimeLimitTuning(5),
            ['10/9', '5/4', '3/2'],
            [
                FrequencyRatio(10, 9),
                FrequencyRatio(5, 4),
                FrequencyRatio(3, 2),
            ]
        ),
        (
            PrimeLimitTuning(5),
            ['1', '5/4', '4/3'],
            [
                FrequencyRatio(1, 1),
                FrequencyRatio(5, 4),
                FrequencyRatio(4, 3),
            ]
        ),
        (
            PrimeLimitTuning(7),
            ['10/9', '5/4', '7/4'],
            [
                FrequencyRatio(10, 9),
                FrequencyRatio(5, 4),
                FrequencyRatio(7, 4),
            ]
        ),
        (
            PrimeLimitTuning(3),
            ['2/9', '1/4', '3/2'],
            [
                FrequencyRatio(2, 9),
                FrequencyRatio(1, 4),
                FrequencyRatio(3, 2),
            ]
        ),
        (
            PrimeLimitTuning(31),
            [],
            []
        ),
    ]
)
def test_rs_interval_fan(tuning, ratio_strs, ratios):
    ifan = tuning.rs_interval_fan(ratio_strs)
    assert [
        interval.frequency_ratio for interval in ifan
    ] == ratios


def test_rs_interval_fan_no_param():
    ifan = PrimeLimitTuning(5).rs_interval_fan()
    assert len(ifan) == 0
    assert ifan.pitch_diffs == []


@pytest.mark.parametrize(
    'tuning, ratio_strs',
    [
        (
            PrimeLimitTuning(5),
            ['10/9', '55/40', '3/2'],
        ),
        (
            PrimeLimitTuning(5),
            ['1', '5/4', '7/5'],
        ),
        (
            PrimeLimitTuning(7),
            ['110/97', '5/4', '7/4'],
        ),
        (
            PrimeLimitTuning(3),
            ['2/9', '8/31', '3/2'],
        ),
    ]
)
def test_rs_interval_fan_limit_violated(tuning, ratio_strs):

    with pytest.raises(ValueError) as exc_info:
        tuning.rs_interval_fan(ratio_strs)
    assert 'surpasses prime limit' in exc_info.value.args[0]


@pytest.mark.parametrize(
    'tuning, ratio_strs',
    [
        (
            PrimeLimitTuning(5),
            ['10/9', '5/4/4', '3/2'],
        ),
        (
            PrimeLimitTuning(5),
            ['1', '5/4', 'a/21'],
        ),
        (
            PrimeLimitTuning(7),
            ['foo/', '5/4', '??'],
        ),
        (
            PrimeLimitTuning(7),
            ['foo/', '5/4', 3],
        ),
        (
            PrimeLimitTuning(3),
            ['3/', '8/31', '3/2'],
        ),
    ]
)
def test_rs_interval_fan_bogus(tuning, ratio_strs):

    with pytest.raises(ValueError) as exc_info:
        tuning.rs_interval_fan(ratio_strs)
    assert 'is not a valid ratio string expression' in exc_info.value.args[0]


@pytest.mark.parametrize(
    'tuning, expr, ratios',
    [
        (
            PrimeLimitTuning(5),
            '4:5:6',
            [
                FrequencyRatio(1),
                FrequencyRatio(5, 4),
                FrequencyRatio(3, 2),
            ]
        ),
        (
            PrimeLimitTuning(5),
            '3:4:9:25:30',
            [
                FrequencyRatio(1),
                FrequencyRatio(4, 3),
                FrequencyRatio(3),
                FrequencyRatio(25, 3),
                FrequencyRatio(10),
            ]
        ),
        (
            PrimeLimitTuning(7),
            '7:4:8:5',
            [
                FrequencyRatio(1),
                FrequencyRatio(4, 7),
                FrequencyRatio(8, 7),
                FrequencyRatio(5, 7),
            ]
        ),
    ]
)
def test_ec_interval_fan(tuning, expr, ratios):
    ifan = tuning.ec_interval_fan(expr)
    assert [
        interval.frequency_ratio for interval in ifan
    ] == ratios
    assert ifan.to_ec_expr() == expr


@pytest.mark.parametrize(
    'tuning, expr',
    [
        (
            PrimeLimitTuning(5),
            '4',
        ),
        (
            PrimeLimitTuning(5),
            '3:3.4',
        ),
        (
            PrimeLimitTuning(7),
            'abc',
        ),
        (
            PrimeLimitTuning(7),
            '5:9:x:a:10',
        ),
    ]
)
def test_ec_interval_fan_bogus(tuning, expr):

    with pytest.raises(ValueError) as exc_info:
        tuning.ec_interval_fan(expr)
    assert 'Invalid expression' in exc_info.value.args[0]


@pytest.mark.parametrize(
    'tuning, expr',
    [
        (
            PrimeLimitTuning(5),
            '4:5:6:7',
        ),
        (
            PrimeLimitTuning(5),
            '3:4:8:11',
        ),
        (
            PrimeLimitTuning(7),
            '6:7:10:11:12',
        ),
        (
            PrimeLimitTuning(11),
            '20:24:31',
        ),
    ]
)
def test_ec_interval_fan_limit_violated(tuning, expr):

    with pytest.raises(ValueError) as exc_info:
        tuning.ec_interval_fan(expr)
    assert 'surpasses prime limit' in exc_info.value.args[0]


def test_invalid_interval_fans_for_ec():

    tuning = PrimeLimitTuning(11)

    with pytest.raises(ValueError) as exc_info:
        tuning.rs_interval_fan(['5/4']).to_ec_expr()
    assert 'must have at least length 2' in exc_info.value.args[0]

    with pytest.raises(ValueError) as exc_info:
        tuning.rs_interval_fan(['5/4', '5/2']).to_ec_expr()
    assert 'must start with 1/1 ratio' in exc_info.value.args[0]
