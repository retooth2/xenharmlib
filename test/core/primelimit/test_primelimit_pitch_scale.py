import pytest
from xenharmlib import FrequencyRatio
from xenharmlib import PrimeLimitTuning


@pytest.mark.parametrize(
    'tuning, lp_vecs, repr_str',
    [
        (
            PrimeLimitTuning(5),
            [(1, -2, 1), (-2, 0, 1), (-1, 1, 0)],
            'PrimeLimitPitchScale([10/9, 5/4, 3/2], 5-Limit)'
        ),
        (
            PrimeLimitTuning(5),
            [(0, 0, 0), (-2, 0, 1), (2, -1, 0)],
            'PrimeLimitPitchScale([1, 5/4, 4/3], 5-Limit)'
        ),
        (
            PrimeLimitTuning(7),
            [(1, -2, 1, 0), (-2, 0, 1, 0), (-2, 0, 0, 1)],
            'PrimeLimitPitchScale([10/9, 5/4, 7/4], 7-Limit)'
        ),
        (
            PrimeLimitTuning(3),
            [(1, -2), (-2, 0), (-1, 1)],
            'PrimeLimitPitchScale([2/9, 1/4, 3/2], 3-Limit)'
        ),
        (
            PrimeLimitTuning(31),
            [],
            'PrimeLimitPitchScale([], 31-Limit)'
        ),
    ]
)
def test_repr(tuning, lp_vecs, repr_str):
    assert repr(
        tuning.index_scale(
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
    assert tuning.index_scale(
        [tuning.lattice.point(lp_vec) for lp_vec in lp_vecs]
    ).monzos == lp_vecs


def test_ratio_scale_no_param():
    scale = PrimeLimitTuning(5).ratio_scale()
    assert len(scale) == 0
    assert scale.pitch_indices == []


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
def test_ratio_scale(tuning, ratios):
    scale = tuning.ratio_scale(ratios)
    assert [
        tuning.zero_element.interval(pitch).frequency_ratio
        for pitch in scale
    ] == ratios


def test_ratio_pc_scale_no_param():
    scale = PrimeLimitTuning(5).ratio_pc_scale()
    assert len(scale) == 0
    assert scale.pitch_indices == []


@pytest.mark.parametrize(
    'tuning, input_ratios, result_ratios',
    [
        (
            PrimeLimitTuning(5),
            [
                FrequencyRatio(3, 2),
                FrequencyRatio(1, 1),
                FrequencyRatio(5, 4),
            ],
            [
                FrequencyRatio(3, 2),
                FrequencyRatio(2, 1),
                FrequencyRatio(5, 2),
            ]
        ),
        (
            PrimeLimitTuning(5),
            [
                FrequencyRatio(5, 4),
                FrequencyRatio(4, 3),
                FrequencyRatio(25, 16),
                FrequencyRatio(1, 1),
            ],
            [
                FrequencyRatio(5, 4),
                FrequencyRatio(4, 3),
                FrequencyRatio(25, 16),
                FrequencyRatio(2, 1),
            ]
        ),
        (
            PrimeLimitTuning(7),
            [
                FrequencyRatio(5, 4),
                FrequencyRatio(7, 4),
                FrequencyRatio(10, 9),
            ],
            [
                FrequencyRatio(5, 4),
                FrequencyRatio(7, 4),
                FrequencyRatio(20, 9),
            ]
        ),
        (
            PrimeLimitTuning(3),
            [
                FrequencyRatio(3, 2),
                FrequencyRatio(128, 81),
                FrequencyRatio(9, 8),
                FrequencyRatio(32, 27)
            ],
            [
                FrequencyRatio(3, 2),
                FrequencyRatio(128, 81),
                FrequencyRatio(9, 4),
                FrequencyRatio(64, 27)
            ],
        ),
        (
            PrimeLimitTuning(31),
            [],
            [],
        ),
    ]
)
def test_ratio_pc_scale(tuning, input_ratios, result_ratios):
    scale = tuning.ratio_pc_scale(input_ratios)
    assert [
        tuning.zero_element.interval(pitch).frequency_ratio
        for pitch in scale
    ] == result_ratios


@pytest.mark.parametrize(
    'tuning, input_ratios, root_bi_index, result_ratios',
    [
        (
            PrimeLimitTuning(5),
            [
                FrequencyRatio(3, 2),
                FrequencyRatio(1, 1),
                FrequencyRatio(5, 4),
            ],
            2,
            [
                FrequencyRatio(6),
                FrequencyRatio(8),
                FrequencyRatio(10),
            ]
        ),
        (
            PrimeLimitTuning(5),
            [
                FrequencyRatio(5, 4),
                FrequencyRatio(4, 3),
                FrequencyRatio(25, 16),
                FrequencyRatio(1, 1),
            ],
            0,
            [
                FrequencyRatio(5, 4),
                FrequencyRatio(4, 3),
                FrequencyRatio(25, 16),
                FrequencyRatio(2, 1),
            ]
        ),
        (
            PrimeLimitTuning(7),
            [
                FrequencyRatio(5, 4),
                FrequencyRatio(7, 4),
                FrequencyRatio(10, 9),
            ],
            3,
            [
                FrequencyRatio(10),
                FrequencyRatio(14),
                FrequencyRatio(160, 9),
            ]
        ),
        (
            PrimeLimitTuning(3),
            [
                FrequencyRatio(3, 2),
                FrequencyRatio(128, 81),
                FrequencyRatio(9, 8),
                FrequencyRatio(32, 27)
            ],
            -1,
            [
                FrequencyRatio(3, 4),
                FrequencyRatio(128, 162),
                FrequencyRatio(9, 8),
                FrequencyRatio(64, 54)
            ],
        ),
        (
            PrimeLimitTuning(31),
            [],
            3,
            [],
        ),
    ]
)
def test_ratio_pc_scale_root_bi_index(
    tuning, input_ratios, root_bi_index, result_ratios
):
    scale = tuning.ratio_pc_scale(input_ratios, root_bi_index)
    assert [
        tuning.zero_element.interval(pitch).frequency_ratio
        for pitch in scale
    ] == result_ratios


@pytest.mark.parametrize(
    'tuning, input_ratios',
    [
        (
            PrimeLimitTuning(5),
            [
                FrequencyRatio(3, 2),
                FrequencyRatio(1, 1),
                FrequencyRatio(7, 4),
            ],
        ),
        (
            PrimeLimitTuning(5),
            [
                FrequencyRatio(5, 4),
                FrequencyRatio(4, 3),
                FrequencyRatio(25, 16),
                FrequencyRatio(7, 4),
            ],
        ),
        (
            PrimeLimitTuning(7),
            [
                FrequencyRatio(12, 11),
                FrequencyRatio(5, 4),
                FrequencyRatio(10, 9),
            ],
        ),
        (
            PrimeLimitTuning(3),
            [
                FrequencyRatio(31, 22),
                FrequencyRatio(128, 81),
                FrequencyRatio(9, 8),
                FrequencyRatio(32, 27)
            ],
        ),
    ]
)
def test_ratio_pc_scale_limit_violated(tuning, input_ratios):
    with pytest.raises(ValueError) as exc_info:
        tuning.ratio_pc_scale(input_ratios)
    assert 'surpasses prime limit' in exc_info.value.args[0]


@pytest.mark.parametrize(
    'tuning, input_ratios',
    [
        (
            PrimeLimitTuning(5),
            [
                FrequencyRatio(3, 2),
                FrequencyRatio(1, 1),
                FrequencyRatio(5, 2),
            ],
        ),
        (
            PrimeLimitTuning(5),
            [
                FrequencyRatio(5, 4),
                FrequencyRatio(4, 3),
                FrequencyRatio(25, 16),
                FrequencyRatio(2),
            ],
        ),
        (
            PrimeLimitTuning(7),
            [
                FrequencyRatio(12, 5),
                FrequencyRatio(5, 4),
                FrequencyRatio(10, 9),
            ],
        ),
        (
            PrimeLimitTuning(3),
            [
                FrequencyRatio(3),
                FrequencyRatio(128, 81),
                FrequencyRatio(9, 8),
                FrequencyRatio(32, 27)
            ],
        ),
    ]
)
def test_ratio_pc_scale_non_pc_ratio(tuning, input_ratios):
    with pytest.raises(ValueError) as exc_info:
        tuning.ratio_pc_scale(input_ratios)
    assert 'must all be between 1 and 2' in exc_info.value.args[0]


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
def test_ratio_scale_limit_violated(tuning, ratios):

    with pytest.raises(ValueError) as exc_info:
        tuning.ratio_scale(ratios)
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
def test_rs_scale(tuning, ratio_strs, ratios):
    scale = tuning.rs_scale(ratio_strs)
    assert [
        tuning.zero_element.interval(pitch).frequency_ratio
        for pitch in scale
    ] == ratios


def test_rs_scale_no_param():
    scale = PrimeLimitTuning(5).rs_scale()
    assert len(scale) == 0
    assert scale.pitch_indices == []


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
def test_rs_scale_limit_violated(tuning, ratio_strs):

    with pytest.raises(ValueError) as exc_info:
        tuning.rs_scale(ratio_strs)
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
def test_rs_scale_bogus(tuning, ratio_strs):

    with pytest.raises(ValueError) as exc_info:
        tuning.rs_scale(ratio_strs)
    assert 'is not a valid ratio string expression' in exc_info.value.args[0]


@pytest.mark.parametrize(
    'tuning, input_ratio_strs, result_ratios',
    [
        (
            PrimeLimitTuning(5),
            ['3/2', '1', '5/4'],
            [
                FrequencyRatio(3, 2),
                FrequencyRatio(2, 1),
                FrequencyRatio(5, 2),
            ]
        ),
        (
            PrimeLimitTuning(5),
            ['5/4', '4/3', '25/16', '1/1'],
            [
                FrequencyRatio(5, 4),
                FrequencyRatio(4, 3),
                FrequencyRatio(25, 16),
                FrequencyRatio(2, 1),
            ]
        ),
        (
            PrimeLimitTuning(7),
            ['5/4', '7/4', '10/9'],
            [
                FrequencyRatio(5, 4),
                FrequencyRatio(7, 4),
                FrequencyRatio(20, 9),
            ]
        ),
        (
            PrimeLimitTuning(3),
            ['3/2', '128/81', '9/8', '32/27'],
            [
                FrequencyRatio(3, 2),
                FrequencyRatio(128, 81),
                FrequencyRatio(9, 4),
                FrequencyRatio(64, 27)
            ],
        ),
        (
            PrimeLimitTuning(31),
            [],
            [],
        ),
    ]
)
def test_rs_pc_scale(tuning, input_ratio_strs, result_ratios):
    scale = tuning.rs_pc_scale(input_ratio_strs)
    assert [
        tuning.zero_element.interval(pitch).frequency_ratio
        for pitch in scale
    ] == result_ratios


def test_rs_pc_scale_no_param():
    scale = PrimeLimitTuning(5).rs_pc_scale()
    assert len(scale) == 0
    assert scale.pitch_indices == []


@pytest.mark.parametrize(
    'tuning, input_ratio_strs, root_bi_index, result_ratios',
    [
        (
            PrimeLimitTuning(5),
            ['3/2', '1/1', '5/4'],
            2,
            [
                FrequencyRatio(6),
                FrequencyRatio(8),
                FrequencyRatio(10),
            ]
        ),
        (
            PrimeLimitTuning(5),
            ['5/4', '4/3', '25/16', '1/1'],
            0,
            [
                FrequencyRatio(5, 4),
                FrequencyRatio(4, 3),
                FrequencyRatio(25, 16),
                FrequencyRatio(2, 1),
            ]
        ),
        (
            PrimeLimitTuning(7),
            ['5/4', '7/4', '10/9'],
            3,
            [
                FrequencyRatio(10),
                FrequencyRatio(14),
                FrequencyRatio(160, 9),
            ]
        ),
        (
            PrimeLimitTuning(3),
            ['3/2', '128/81', '9/8', '32/27'],
            -1,
            [
                FrequencyRatio(3, 4),
                FrequencyRatio(128, 162),
                FrequencyRatio(9, 8),
                FrequencyRatio(64, 54)
            ],
        ),
        (
            PrimeLimitTuning(31),
            [],
            3,
            [],
        ),
    ]
)
def test_rs_pc_scale_root_bi_index(
    tuning, input_ratio_strs, root_bi_index, result_ratios
):
    scale = tuning.rs_pc_scale(input_ratio_strs, root_bi_index)
    assert [
        tuning.zero_element.interval(pitch).frequency_ratio
        for pitch in scale
    ] == result_ratios


@pytest.mark.parametrize(
    'tuning, input_ratio_strs',
    [
        (
            PrimeLimitTuning(5),
            ['3/2', '1/1', '7/4'],
        ),
        (
            PrimeLimitTuning(5),
            ['5/4', '4/3', '25/16', '7/4'],
        ),
        (
            PrimeLimitTuning(7),
            ['12/11', '5/4', '10/9'],
        ),
        (
            PrimeLimitTuning(3),
            ['31/22', '128/81', '9/8', '32/27'],
        ),
    ]
)
def test_rs_pc_scale_limit_violated(tuning, input_ratio_strs):
    with pytest.raises(ValueError) as exc_info:
        tuning.rs_pc_scale(input_ratio_strs)
    assert 'surpasses prime limit' in exc_info.value.args[0]


@pytest.mark.parametrize(
    'tuning, input_ratio_strs',
    [
        (
            PrimeLimitTuning(5),
            ['3/2', '2', '7/4'],
        ),
        (
            PrimeLimitTuning(5),
            ['5/4', '8/3', '25/16', '7/4'],
        ),
        (
            PrimeLimitTuning(7),
            ['4/7', '5/4', '10/9'],
        ),
        (
            PrimeLimitTuning(3),
            ['3/2', '128/81', '8/9', '32/27'],
        ),
    ]
)
def test_rs_pc_scale_non_pc_ratio(tuning, input_ratio_strs):
    with pytest.raises(ValueError) as exc_info:
        tuning.rs_pc_scale(input_ratio_strs)
    assert 'must all be between 1 and 2' in exc_info.value.args[0]


@pytest.mark.parametrize(
    'tuning, input_ratio_strs',
    [
        (
            PrimeLimitTuning(5),
            ['3/2', '1/1', '7/4', '1/'],
        ),
        (
            PrimeLimitTuning(5),
            ['5/4', '4/3', '25/16/3', '7/4'],
        ),
        (
            PrimeLimitTuning(7),
            ['12/11', 3, '5/4', '10/9'],
        ),
        (
            PrimeLimitTuning(3),
            ['31/22', 'foo', '128/81', '9/8', '32/27'],
        ),
    ]
)
def test_rs_pc_scale_bogus(tuning, input_ratio_strs):
    with pytest.raises(ValueError) as exc_info:
        tuning.rs_pc_scale(input_ratio_strs)
    assert 'is not a valid ratio string expression' in exc_info.value.args[0]
