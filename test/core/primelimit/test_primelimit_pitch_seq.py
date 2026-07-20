import pytest
from xenharmlib import FrequencyRatio
from xenharmlib import PrimeLimitTuning


@pytest.mark.parametrize(
    'tuning, lp_vecs, repr_str',
    [
        (
            PrimeLimitTuning(5),
            [(-2, 0, 1), (1, -2, 1), (-2, 0, 1), (-1, 1, 0)],
            'PrimeLimitPitchSeq([5/4, 10/9, 5/4, 3/2], 5-Limit)'
        ),
        (
            PrimeLimitTuning(5),
            [(0, 0, 0), (-2, 0, 1), (0, -1, 0), (2, -1, 0)],
            'PrimeLimitPitchSeq([1, 5/4, 1/3, 4/3], 5-Limit)'
        ),
        (
            PrimeLimitTuning(7),
            [(1, -2, 1, 0), (-2, 0, 1, 0), (-2, 0, 0, 1)],
            'PrimeLimitPitchSeq([10/9, 5/4, 7/4], 7-Limit)'
        ),
        (
            PrimeLimitTuning(3),
            [(1, -2), (-2, 0), (-1, 1)],
            'PrimeLimitPitchSeq([2/9, 1/4, 3/2], 3-Limit)'
        ),
        (
            PrimeLimitTuning(31),
            [],
            'PrimeLimitPitchSeq([], 31-Limit)'
        ),
    ]
)
def test_repr(tuning, lp_vecs, repr_str):
    assert repr(
        tuning.index_seq(
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
            [(2, -1, 0), (2, -1, 0), (0, 0, 0), (-2, 0, 1), (2, -1, 0)],
        ),
        (
            PrimeLimitTuning(7),
            [(1, -2, 1, 0), (1, 0, -1, 1), (-2, 0, 1, 0), (-2, 0, 0, 1)],
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
    assert tuning.index_seq(
        [tuning.lattice.point(lp_vec) for lp_vec in lp_vecs]
    ).monzos == lp_vecs


def test_ratio_seq_no_param():
    iseq = PrimeLimitTuning(5).ratio_seq()
    assert len(iseq) == 0
    assert iseq.pitch_indices == []


@pytest.mark.parametrize(
    'tuning, ratios',
    [
        (
            PrimeLimitTuning(5),
            [
                FrequencyRatio(10, 9),
                FrequencyRatio(3, 2),
                FrequencyRatio(5, 4),
                FrequencyRatio(3, 2),
                FrequencyRatio(3, 2),
            ]
        ),
        (
            PrimeLimitTuning(5),
            [
                FrequencyRatio(2, 3),
                FrequencyRatio(5, 4),
                FrequencyRatio(4, 3),
                FrequencyRatio(2, 3),
                FrequencyRatio(2, 3),
            ]
        ),
        (
            PrimeLimitTuning(7),
            [
                FrequencyRatio(10, 9),
                FrequencyRatio(5, 4),
                FrequencyRatio(5, 4),
                FrequencyRatio(7, 4),
            ]
        ),
        (
            PrimeLimitTuning(3),
            [
                FrequencyRatio(1, 4),
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
def test_ratio_seq(tuning, ratios):
    seq = tuning.ratio_seq(ratios)
    assert [
        tuning.zero_element.interval(pitch).frequency_ratio
        for pitch in seq
    ] == ratios


@pytest.mark.parametrize(
    'tuning, ratios',
    [
        (
            PrimeLimitTuning(5),
            [
                FrequencyRatio(3, 2),
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
                FrequencyRatio(5, 8),
                FrequencyRatio(5, 2),
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
                FrequencyRatio(3, 2),
            ]
        ),
    ]
)
def test_ratio_seq_limit_violated(tuning, ratios):

    with pytest.raises(ValueError) as exc_info:
        tuning.ratio_seq(ratios)
    assert 'surpasses prime limit' in exc_info.value.args[0]


@pytest.mark.parametrize(
    'tuning, ratio_strs, ratios',
    [
        (
            PrimeLimitTuning(5),
            ['3', '10/9', '5/4', '3/2'],
            [
                FrequencyRatio(3),
                FrequencyRatio(10, 9),
                FrequencyRatio(5, 4),
                FrequencyRatio(3, 2),
            ]
        ),
        (
            PrimeLimitTuning(5),
            ['1', '5/4', '4/3', '3/4', '3/4'],
            [
                FrequencyRatio(1, 1),
                FrequencyRatio(5, 4),
                FrequencyRatio(4, 3),
                FrequencyRatio(3, 4),
                FrequencyRatio(3, 4),
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
def test_rs_seq(tuning, ratio_strs, ratios):
    seq = tuning.rs_seq(ratio_strs)
    assert [
        tuning.zero_element.interval(pitch).frequency_ratio
        for pitch in seq
    ] == ratios


def test_rs_seq_no_param():
    iseq = PrimeLimitTuning(5).rs_seq()
    assert len(iseq) == 0
    assert iseq.pitch_indices == []


@pytest.mark.parametrize(
    'tuning, ratio_strs',
    [
        (
            PrimeLimitTuning(5),
            ['10/9', '55/40', '3/2'],
        ),
        (
            PrimeLimitTuning(5),
            ['2', '5/4', '7/5', '1/2'],
        ),
        (
            PrimeLimitTuning(7),
            ['7/4', '110/97', '5/4', '7/4'],
        ),
        (
            PrimeLimitTuning(3),
            ['2/9', '8/31', '3/2'],
        ),
    ]
)
def test_rs_seq_limit_violated(tuning, ratio_strs):

    with pytest.raises(ValueError) as exc_info:
        tuning.rs_seq(ratio_strs)
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
def test_rs_seq_bogus(tuning, ratio_strs):

    with pytest.raises(ValueError) as exc_info:
        tuning.rs_seq(ratio_strs)
    assert 'is not a valid ratio string expression' in exc_info.value.args[0]
