import pytest
from xenharmlib.core.frequencies import FrequencyRatio
from xenharmlib import EDTuning
from xenharmlib.tuning.ed import EDPitch
from xenharmlib.exc import IncompatibleOriginContexts
from xenharmlib.exc import InvalidGenerator

edo12 = EDTuning(12, FrequencyRatio(2))
edo17 = EDTuning(17, FrequencyRatio(2))
edo24 = EDTuning(24, FrequencyRatio(2))
edo31 = EDTuning(31, FrequencyRatio(2))
ed13_3 = EDTuning(13, FrequencyRatio(3))
ed17_3 = EDTuning(17, FrequencyRatio(3))


@pytest.mark.parametrize(
    'tuning, pitch_index, exp_pc, exp_bi',
    [
        (edo31, 12, 12, 0),
        (edo31, 32, 1, 1),
        (edo31, -1, 30, -1),
        (edo12, -13, 11, -2),
        (edo24, 48, 0, 2),
        (edo24, -49, 23, -3),
    ]
)
def test_pitch_periodic_indices(tuning, pitch_index, exp_pc, exp_bi):
    """
    Test if pitch class index and base interval index
    are calculated correctly from pitch index
    """

    pitch = tuning.pitch(pitch_index)
    assert pitch.pc_index == exp_pc
    assert pitch.bi_index == exp_bi


@pytest.mark.parametrize(
    'tuning, pitch_index, diff, exp_result',
    [
        (edo31, 12, 2, 74),
        (edo31, 12, -2, -50),
        (edo12, 12, -1, 0),
        (ed13_3, 12, 1, 25),
    ]
)
def test_transpose_bi_index(tuning, pitch_index, diff, exp_result):
    """
    Test if method transpose_bi_index works correctly
    """

    pitch = tuning.pitch(pitch_index)
    transposed = pitch.transpose_bi_index(diff)
    assert transposed.pitch_index == exp_result


@pytest.mark.parametrize(
    'tuning, pitch_index, diff, new_index',
    [
        (edo12, 7, 10, 17),
        (edo17, 7, -3, 4),
        (ed17_3, 19, 3, 22),
        (edo12, -7, 10, 3),
    ]
)
def test_transpose_int(tuning, pitch_index, diff, new_index):
    """
    Test if transpose method with an integer parameter
    works correctly
    """

    pitch = tuning.pitch(pitch_index)
    transposed = pitch.transpose(diff)
    assert type(pitch) is EDPitch
    assert type(transposed) is EDPitch
    assert transposed.pitch_index == new_index


@pytest.mark.parametrize(
    'tuning, pitch_index, diff, new_index',
    [
        (edo12, 7, 10, 17),
        (edo17, 7, -3, 4),
        (ed17_3, 19, 3, 22),
        (edo12, -9, 13, 4),
    ]
)
def test_transpose_interval(tuning, pitch_index, diff, new_index):
    """
    Test if transpose method with a pitch interval parameter
    works correctly
    """

    pitch_a = tuning.pitch(pitch_index)
    pitch_b = tuning.pitch(pitch_index + diff)
    interval = pitch_a.interval(pitch_b)
    transposed = pitch_a.transpose(interval)
    assert type(pitch_a) is EDPitch
    assert type(pitch_b) is EDPitch
    assert transposed.pitch_index == pitch_b.pitch_index
    assert transposed.pitch_index == new_index


@pytest.mark.parametrize(
    'pitch, gen_pitch, gen_index',
    [
        (edo12.pitch(0), edo12.pitch(7), 0),
        (edo12.pitch(6), edo12.pitch(7), 6),
        (edo12.pitch(3), edo12.pitch(7), 9),
        (edo12.pitch(3), edo12.pitch(5), 3),
        (edo12.pitch(3), edo12.pitch(5+12), 3),
        (edo31.pitch(9), edo31.pitch(1), 9),
        (edo31.pitch(5), edo31.pitch(9), 4),
        (ed13_3.pitch(8), ed13_3.pitch(7), 3),
        (edo12.pitch(-10), edo12.pitch(7), 2),
    ]
)
def test_get_generator_index(pitch, gen_pitch, gen_index):
    """
    Test if get_generator_index works correctly
    """

    result = pitch.get_generator_index(gen_pitch)
    assert result == gen_index


def test_get_generator_index_invalid_generator():
    """
    Test if get_generator_index raises InvalidGenerator if
    given parameter is not a generator pitch
    """

    pitch = edo12.pitch(8)
    with pytest.raises(InvalidGenerator):
        pitch.get_generator_index(
            edo12.pitch(4)
        )


@pytest.mark.parametrize(
    'pitch',
    [
        edo12.pitch(0),
        edo12.pitch(7),
        edo12.pitch(23),
        edo31.pitch(0),
        edo31.pitch(18),
        edo31.pitch(32),
        edo31.pitch(-9),
    ]
)
def test_pcs_normalized(pitch):
    """
    Test if pcs_normalized method works correctly
    """

    expected = pitch.tuning.pitch(pitch.pc_index)
    assert pitch.pcs_normalized() == expected


@pytest.mark.parametrize(
    'pitch_a, pitch_b',
    [
        (edo12.pitch(0), edo31.pitch(0)),
        (edo12.pitch(24), edo31.pitch(62)),
        (edo12.pitch(7), edo31.pitch(18)),
        (edo12.pitch(7), ed13_3.pitch(5)),
        (edo12.pitch(-7), ed13_3.pitch(-5)),
    ]
)
def test_retune(pitch_a, pitch_b):
    """
    Test if retune method works correctly
    """

    assert pitch_a.retune(pitch_b.tuning) == pitch_b
    assert pitch_b.retune(pitch_a.tuning) == pitch_a


@pytest.mark.parametrize(
    'pitch_a, pitch_b',
    [
        (edo12.pitch(0), edo12.pitch(6)),
        (edo12.pitch(9), edo12.pitch(18)),
        (edo31.pitch(18), edo31.pitch(19)),
        (edo31.pitch(18), edo12.pitch(7)),
        (edo12.pitch(7), ed13_3.pitch(5)),
        (edo12.pitch(-7), ed13_3.pitch(5)),
        (edo12.pitch(-7), ed13_3.pitch(-2)),
        (edo12.pitch(-7), edo12.pitch(-6)),
    ]
)
def test_lt_gt(pitch_a, pitch_b):
    """
    Test if pitches can be compared with lesser-than
    and greater-than relations and if lesser-than and
    greater-than also implies inequality
    """

    assert pitch_a < pitch_b
    assert pitch_b > pitch_a
    assert pitch_a != pitch_b
    assert pitch_b != pitch_a


@pytest.mark.parametrize(
    'pitch_a, pitch_b',
    [
        (edo12.pitch(0), edo12.pitch(0)),
        (edo31.pitch(9), edo31.pitch(9)),
        (edo12.pitch(3), edo24.pitch(6)),
        (edo12.pitch(19), edo24.pitch(38)),
        (edo12.pitch(-13), edo24.pitch(-26)),
    ]
)
def test_eq(pitch_a, pitch_b):
    """
    Test if two pitches are correctly recognized as
    equal if they have the same frequency
    """
    assert pitch_a == pitch_b


@pytest.mark.parametrize(
    'pitch_a, pitch_b',
    [
        (edo12.pitch(3), edo12.pitch(3)),
        (edo31.pitch(9), edo31.pitch(40)),
        (edo24.pitch(3), edo24.pitch(51)),
        (edo12.pitch(2), edo24.pitch(52)),
    ]
)
def test_is_equivalent(pitch_a, pitch_b):
    """
    Test if two pitches are correctly recognized as
    equivalent if their frequency is the same under
    base interval normalization
    """
    assert pitch_a.is_equivalent(pitch_b)


@pytest.mark.parametrize(
    'pitch_a, pitch_b',
    [
        (edo12.pitch(3), edo12.pitch(4)),
        (edo31.pitch(9), edo31.pitch(43)),
        (edo24.pitch(3), edo24.pitch(59)),
    ]
)
def test_is_not_equivalent(pitch_a, pitch_b):
    """
    Test if two pitches are correctly recognized as
    not equivalent if their frequency is not the same under
    base interval normalization
    """
    assert not pitch_a.is_equivalent(pitch_b)


@pytest.mark.parametrize(
    'pitch_b',
    [
        edo12.pitch(3),
        edo31.pitch(0),
        ed13_3.pitch(7),
    ]
)
def test_get_generator_index_incompatible_origin_contexts(pitch_b):
    """
    Test if IncompatibleOriginContexts is raised while calling
    get_generator_index when generator pitch is from a different
    tuning context
    """

    edo12_2 = EDTuning(12, FrequencyRatio(2))
    pitch_a = edo12_2.pitch(0)

    with pytest.raises(IncompatibleOriginContexts):
        pitch_a.get_generator_index(pitch_b)


@pytest.mark.parametrize(
    'index_a, index_b',
    [
        (9, 2),
        (8, 4),
        (1, 0),
        (-10, 2),
    ]
)
def test_arithmetic(index_a, index_b):
    """
    Test if pitch addition/substraction and scalar
    multiplication works correctly
    """

    sum_result = index_a + index_b
    diff_result = index_a - index_b
    mul_result = index_a * index_b

    pitch_a = edo12.pitch(index_a)
    pitch_b = edo12.pitch(index_b)

    sum_pitch = (pitch_a + pitch_b)
    diff_pitch = (pitch_a - pitch_b)
    mul_pitch = index_a * pitch_b
    rmul_pitch = pitch_b * index_a

    assert sum_pitch.pitch_index == edo12.pitch(sum_result).pitch_index
    assert diff_pitch.pitch_index == edo12.pitch(diff_result).pitch_index
    assert mul_pitch == rmul_pitch
    assert mul_pitch.pitch_index == edo12.pitch(mul_result).pitch_index


@pytest.mark.parametrize(
    'index_a, index_b',
    [
        (9, 2),
        (8, 4),
        (1, 0),
        (-9, 2),
    ]
)
def test_arithmetic_incompatible_origin_contexts(index_a, index_b):
    """
    Test if IncompatibleOriginContexts is raised when addition
    and substraction is done with pitches from different
    tuning contexts
    """

    edo12_2 = EDTuning(12, FrequencyRatio(2))
    pitch_a = edo12.pitch(index_a)
    pitch_b = edo12_2.pitch(index_b)

    with pytest.raises(IncompatibleOriginContexts):
        pitch_a - pitch_b

    with pytest.raises(IncompatibleOriginContexts):
        pitch_a + pitch_b
