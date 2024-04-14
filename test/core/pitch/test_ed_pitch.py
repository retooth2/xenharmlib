import pytest
from xenharmlib.core.frequencies import Frequency
from xenharmlib.core.tunings import EDTuning
from xenharmlib.core.pitch import EDPitch
from xenharmlib.exc import IncompatibleTunings
from xenharmlib.exc import InvalidPitchIndex
from xenharmlib.exc import InvalidPitchClassIndex
from xenharmlib.exc import InvalidBaseIntervalIndex
from xenharmlib.exc import InvalidGenerator

edo12 = EDTuning(12, Frequency(2))
edo24 = EDTuning(24, Frequency(2))
edo31 = EDTuning(31, Frequency(2))
ed13_3 = EDTuning(13, Frequency(3))


def test_pitch_periodic_indices():

    pitch = EDPitch(edo31, 12)
    assert pitch.pc_index == 12
    assert pitch.bi_index == 0

    pitch = EDPitch(edo31, 32)
    assert pitch.pc_index == 1
    assert pitch.bi_index == 1

    pitch = EDPitch(edo31, -1)
    assert pitch.pc_index == 30
    assert pitch.bi_index == -1


def test_transpose_bi_index():

    pitch = EDPitch(edo31, 41)
    assert pitch.pc_index == 10
    assert pitch.bi_index == 1

    transposed = pitch.transpose_bi_index(2)
    assert transposed.pitch_index == 103


@pytest.mark.parametrize(
    'tuning, pitch_index, diff, new_index',
    [
        (
            EDTuning(12, Frequency(2)),
            7, 10, 17
        ),
        (
            EDTuning(17, Frequency(2)),
            7, -3, 4
        ),
        (
            EDTuning(17, Frequency(3)),
            19, 3, 22
        ),
        (
            EDTuning(12, Frequency(2)),
            -7, 10, 3
        ),
    ]
)
def test_transpose_int(tuning, pitch_index, diff, new_index):
    pitch = tuning.pitch(pitch_index)
    transposed = pitch.transpose(diff)
    assert type(pitch) is EDPitch
    assert type(transposed) is EDPitch
    assert transposed.pitch_index == new_index


@pytest.mark.parametrize(
    'tuning, pitch_index, diff, new_index',
    [
        (
            EDTuning(12, Frequency(2)),
            7, 10, 17
        ),
        (
            EDTuning(17, Frequency(2)),
            7, -3, 4
        ),
        (
            EDTuning(17, Frequency(3)),
            19, 3, 22
        ),
        (
            EDTuning(12, Frequency(2)),
            -9, 13, 4
        ),
    ]
)
def test_transpose_interval(tuning, pitch_index, diff, new_index):
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
        (EDPitch(edo12, 0), EDPitch(edo12, 7), 0),
        (EDPitch(edo12, 6), EDPitch(edo12, 7), 6),
        (EDPitch(edo12, 3), EDPitch(edo12, 7), 9),
        (EDPitch(edo12, 3), EDPitch(edo12, 5), 3),
        (EDPitch(edo12, 3), EDPitch(edo12, 5+12), 3),
        (EDPitch(edo31, 9), EDPitch(edo31, 1), 9),
        (EDPitch(edo31, 5), EDPitch(edo31, 9), 4),
        (EDPitch(ed13_3, 8), EDPitch(ed13_3, 7), 3),
        (EDPitch(edo12, -10), EDPitch(edo12, 7), 2),
    ]
)
def test_get_generator_index(pitch, gen_pitch, gen_index):
    result = pitch.get_generator_index(gen_pitch)
    assert result == gen_index


def test_get_generator_index_invalid_generator():
    pitch = EDPitch(edo12, 8)

    with pytest.raises(InvalidGenerator):
        pitch.get_generator_index(
            EDPitch(edo12, 4)
        )


@pytest.mark.parametrize(
    'pitch',
    [
        EDPitch(edo12, 0),
        EDPitch(edo12, 7),
        EDPitch(edo12, 23),
        EDPitch(edo31, 0),
        EDPitch(edo31, 18),
        EDPitch(edo31, 32),
        EDPitch(edo31, -9),
    ]
)
def test_get_bi_normalized(pitch):
    expected = EDPitch(pitch.tuning, pitch.pc_index)
    assert pitch.get_bi_normalized() == expected


@pytest.mark.parametrize(
    'pitch_a, pitch_b',
    [
        (EDPitch(edo12, 0), EDPitch(edo31, 0)),
        (EDPitch(edo12, 24), EDPitch(edo31, 62)),
        (EDPitch(edo12, 7), EDPitch(edo31, 18)),
        (EDPitch(edo12, 7), EDPitch(ed13_3, 5)),
        (EDPitch(edo12, -7), EDPitch(ed13_3, -5)),
    ]
)
def test_retune(pitch_a, pitch_b):
    assert pitch_a.retune(pitch_b.tuning) == pitch_b
    assert pitch_b.retune(pitch_a.tuning) == pitch_a


@pytest.mark.parametrize(
    'pitch_a, pitch_b',
    [
        (EDPitch(edo12, 0), EDPitch(edo12, 6)),
        (EDPitch(edo12, 9), EDPitch(edo12, 18)),
        (EDPitch(edo31, 18), EDPitch(edo31, 19)),
        (EDPitch(edo31, 18), EDPitch(edo12, 7)),
        (EDPitch(edo12, 7), EDPitch(ed13_3, 5)),
        (EDPitch(edo12, -7), EDPitch(ed13_3, 5)),
        (EDPitch(edo12, -7), EDPitch(ed13_3, -2)),
        (EDPitch(edo12, -7), EDPitch(edo12, -6)),
    ]
)
def test_lt_gt(pitch_a, pitch_b):
    assert pitch_a < pitch_b
    assert pitch_b > pitch_a


@pytest.mark.parametrize(
    'pitch_a, pitch_b',
    [
        (EDPitch(edo12, 0), EDPitch(edo12, 0)),
        (EDPitch(edo31, 9), EDPitch(edo31, 9)),
        (EDPitch(edo12, 3), EDPitch(edo24, 6)),
        (EDPitch(edo12, 19), EDPitch(edo24, 38)),
        (EDPitch(edo12, -13), EDPitch(edo24, -26)),
    ]
)
def test_eq(pitch_a, pitch_b):
    assert pitch_a == pitch_b


@pytest.mark.parametrize(
    'pitch_a, pitch_b',
    [
        (EDPitch(edo12, 3), EDPitch(edo12, 3)),
        (EDPitch(edo31, 9), EDPitch(edo31, 40)),
        (EDPitch(edo24, 3), EDPitch(edo24, 51)),
    ]
)
def test_is_equivalent(pitch_a, pitch_b):
    assert pitch_a.is_equivalent(pitch_b)


@pytest.mark.parametrize(
    'pitch_a, pitch_b',
    [
        (EDPitch(edo12, 3), EDPitch(edo12, 4)),
        (EDPitch(edo31, 9), EDPitch(edo31, 43)),
        (EDPitch(edo24, 3), EDPitch(edo24, 59)),
    ]
)
def test_is_not_equivalent(pitch_a, pitch_b):
    assert not pitch_a.is_equivalent(pitch_b)


@pytest.mark.parametrize(
    'pitch_b',
    [
        EDPitch(edo31, 0),
        EDPitch(ed13_3, 7),
    ]
)
def test_incompatible_tunings(pitch_b):

    edo12_2 = EDTuning(12, Frequency(2))
    pitch_a = EDPitch(edo12_2, 0)

    with pytest.raises(IncompatibleTunings):
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

    sum_result = index_a + index_b
    diff_result = index_a - index_b
    mul_result = index_a * index_b

    pitch_a = EDPitch(edo12, index_a)
    pitch_b = EDPitch(edo12, index_b)

    sum_pitch = (pitch_a + pitch_b)
    diff_pitch = (pitch_a - pitch_b)
    mul_pitch = index_a * pitch_b
    rmul_pitch = pitch_b * index_a

    assert sum_pitch.pitch_index == EDPitch(
        edo12, sum_result
    ).pitch_index
    assert diff_pitch.pitch_index == EDPitch(
        edo12, diff_result
    ).pitch_index
    assert mul_pitch == rmul_pitch
    assert mul_pitch.pitch_index == EDPitch(
        edo12, mul_result
    ).pitch_index


@pytest.mark.parametrize(
    'index_a, index_b',
    [
        (9, 2),
        (8, 4),
        (1, 0),
        (-9, 2),
    ]
)
def test_arithmetic_incompatible_tunings(index_a, index_b):

    edo12_2 = EDTuning(12, Frequency(2))
    pitch_a = EDPitch(edo12, index_a)
    pitch_b = EDPitch(edo12_2, index_b)

    with pytest.raises(IncompatibleTunings):
        pitch_a - pitch_b

    with pytest.raises(IncompatibleTunings):
        pitch_a + pitch_b