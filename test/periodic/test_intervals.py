import pytest
from xenharmlib import EDOTuning
from xenharmlib import UpDownNotation
from xenharmlib import periodic

edo12 = EDOTuning(12)
n_edo12 = UpDownNotation(edo12)
edo24 = EDOTuning(24)
n_edo24 = UpDownNotation(edo24)
edo31 = EDOTuning(31)
n_edo31 = UpDownNotation(edo31)


@pytest.mark.parametrize(
    'tuning, input_pi, source_index, target_index, diff',
    [
        (edo12, [3, 5, 7, 8, 10], 0, 2, 4),
        (edo12, [5, 7, 8, 9, 11], 2, -1, -9),
        (edo31, [10, 19, 23, 24, 26], 3, 8, 31),
        (edo31, [0, 12, 16, 19, 22, 30], 1, 5, 18),
    ]
)
def test_spec_interval_pitch(
    tuning, 
    input_pi,
    source_index,
    target_index,
    diff
):
    """
    Test if spec_interval works correctly on pitch layer
    """

    input_scale = tuning.index_scale(input_pi)
    expected = tuning.diff_interval(diff)
    assert periodic.spec_interval(
        input_scale, source_index, target_index
    ) == expected


@pytest.mark.parametrize(
    'notation, scale_pc, source_index, target_index, interval_pair',
    [
        (
            n_edo12,
            ['C', 'D', 'E', 'F', 'A', 'Bb'],
            2, 3,
            ('m', 2)
        ),
        (
            n_edo24,
            ['C#', 'D', 'vE', 'F#', 'A', 'vBb'],
            3, 6,
            ('P', 5)
        ),
        (
            n_edo31,
            ['C', 'D', 'E', 'F', 'A', 'Bb'],
            1, -2,
            ('P', -4)
        )
    ]
)
def test_spec_interval_note(
    notation,
    scale_pc,
    source_index,
    target_index,
    interval_pair
):
    """
    Test if spec_interval works correctly on note layer
    """

    input_scale = notation.pc_scale(scale_pc)
    expected = notation.shorthand_interval(*interval_pair)
    assert periodic.spec_interval(
        input_scale, source_index, target_index
    ) == expected


def test_spec_interval_non_period_normalized():
    """
    Test if spec_interval raises ValueError if scale is not
    period normalized
    """

    scale = n_edo31.pc_scale(['C', 'E', 'G', 'B', 'D', 'F'])

    with pytest.raises(ValueError) as exc_info:
        periodic.spec_interval(scale, 1, 2)

    assert exc_info.value.args[0] == (
        'spec_interval is only defined on period normalized scales'
    )
