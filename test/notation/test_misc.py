import pytest
from xenharmlib.exc import IncompatibleOriginContexts
from xenharmlib import WesternNotation
from xenharmlib import UpDownNotation
from xenharmlib import EDOTuning


@pytest.mark.parametrize(
    'notation, pitch',
    [
        (WesternNotation(), EDOTuning(31).pitch(3)),
        (UpDownNotation(EDOTuning(24)), EDOTuning(31).pitch(3)),
    ]
)
def test_guess_note_incompatible(notation, pitch):

    with pytest.raises(IncompatibleOriginContexts) as exc_info:
        notation.guess_note(pitch)

    assert exc_info.value.args[0] == (
        'Pitch must originate from the tuning that this notation is build upon'
    )


@pytest.mark.parametrize(
    'notation, interval',
    [
        (WesternNotation(), EDOTuning(31).diff_interval(3)),
        (UpDownNotation(EDOTuning(24)), EDOTuning(31).diff_interval(3)),
    ]
)
def test_guess_note_interval_incompatible(notation, interval):

    with pytest.raises(IncompatibleOriginContexts) as exc_info:
        notation.guess_note_interval(interval)

    assert exc_info.value.args[0] == (
        'Pitch interval must originate from the tuning that this '
        'notation is build upon'
    )


@pytest.mark.parametrize(
    'notation, scale',
    [
        (WesternNotation(), EDOTuning(31).index_scale([1, 4, 6])),
        (UpDownNotation(EDOTuning(24)), EDOTuning(31).index_scale([2, 3, 4])),
    ]
)
def test_guess_note_scale_incompatible(notation, scale):

    with pytest.raises(IncompatibleOriginContexts) as exc_info:
        notation.guess_note_scale(scale)

    assert exc_info.value.args[0] == (
        'Pitch scale must originate from the tuning that this '
        'notation is build upon'
    )


@pytest.mark.parametrize(
    'notation, interval_seq',
    [
        (WesternNotation(), EDOTuning(31).diff_interval_seq([1, 4, 6])),
        (
            UpDownNotation(EDOTuning(24)),
            EDOTuning(31).diff_interval_seq([2, 3, 4])
        ),
    ]
)
def test_guess_note_interval_seq_incompatible(notation, interval_seq):

    with pytest.raises(IncompatibleOriginContexts) as exc_info:
        notation.guess_note_interval_seq(interval_seq)

    assert exc_info.value.args[0] == (
        'Pitch interval sequence must originate from the tuning that this '
        'notation is build upon'
    )


@pytest.mark.parametrize(
    'notation, interval_fan',
    [
        (WesternNotation(), EDOTuning(31).diff_interval_fan([1, 4, 6])),
        (
            UpDownNotation(EDOTuning(24)),
            EDOTuning(31).diff_interval_fan([2, 3, 4])
        ),
    ]
)
def test_guess_note_interval_fan_incompatible(notation, interval_fan):

    with pytest.raises(IncompatibleOriginContexts) as exc_info:
        notation.guess_note_interval_fan(interval_fan)

    assert exc_info.value.args[0] == (
        'Pitch interval fan must originate from the tuning that this '
        'notation is build upon'
    )


@pytest.mark.parametrize(
    'notation, seq',
    [
        (WesternNotation(), EDOTuning(31).index_seq([1, 4, 6])),
        (UpDownNotation(EDOTuning(24)), EDOTuning(31).index_seq([2, 3, 4])),
    ]
)
def test_guess_note_seq_incompatible(notation, seq):

    with pytest.raises(IncompatibleOriginContexts) as exc_info:
        notation.guess_note_seq(seq)

    assert exc_info.value.args[0] == (
        'Pitch sequence must originate from the tuning that this '
        'notation is build upon'
    )


@pytest.mark.parametrize(
    'notation, sum_vec, diff_vec',
    [
        (WesternNotation(), (3,), (3,)),
        (WesternNotation(), (0,), (0,)),
        (WesternNotation(), (-1,), (-1,)),
        (UpDownNotation(EDOTuning(12)), (-1,), (-1,)),
        (UpDownNotation(EDOTuning(24)), (2, -1), (4, -1)),
        (UpDownNotation(EDOTuning(31)), (-2, -1), (-4, -1)),
    ]
)
def test_acc_sum_vector_to_acc_diff_vector(notation, sum_vec, diff_vec):
    assert notation.acc_sum_vector_to_acc_diff_vector(sum_vec) == diff_vec


def test_acc_sum_vector_to_acc_diff_vector_wrong_dim():

    notation = WesternNotation()

    with pytest.raises(ValueError) as exc_info:
        notation.acc_sum_vector_to_acc_diff_vector((1, 2, 3))
    assert '(should be 1)' in exc_info.value.args[0]


@pytest.mark.parametrize(
    'notation, sum_vec, diff_vec',
    [
        (WesternNotation(), (3,), (3,)),
        (WesternNotation(), (0,), (0,)),
        (WesternNotation(), (-1,), (-1,)),
        (UpDownNotation(EDOTuning(12)), (-1,), (-1,)),
        (UpDownNotation(EDOTuning(24)), (2, -1), (4, -1)),
        (UpDownNotation(EDOTuning(31)), (-2, -1), (-4, -1)),
    ]
)
def test_acc_diff_vector_to_acc_sum_vector(notation, sum_vec, diff_vec):
    assert notation.acc_diff_vector_to_acc_sum_vector(diff_vec) == sum_vec


def test_acc_diff_vector_to_acc_sum_vector_wrong_dim():

    notation = WesternNotation()

    with pytest.raises(ValueError) as exc_info:
        notation.acc_diff_vector_to_acc_sum_vector((1, 2, 3))
    assert '(should be 1)' in exc_info.value.args[0]


@pytest.mark.parametrize(
    'notation, diff_vec',
    [
        (UpDownNotation(EDOTuning(24)), (3, -1)),
        (UpDownNotation(EDOTuning(31)), (-9, -1)),
    ]
)
def test_acc_diff_vector_to_acc_sum_vector_not_in_image(
    notation, diff_vec
):

    with pytest.raises(ValueError) as exc_info:
        notation.acc_diff_vector_to_acc_sum_vector(diff_vec)
    assert 'is not in the image' in exc_info.value.args[0]
