import pytest

from xenharmlib import EDOTuning
from xenharmlib import UpDownNotation

edo12 = EDOTuning(12)
edo31 = EDOTuning(31)


@pytest.mark.parametrize(
    'divisions',
    [12, 19, 26, 33, 40, 47]
)
def test_init_notation_sharpness_1(divisions):

    tuning = EDOTuning(divisions)
    notation = UpDownNotation(tuning)

    assert notation.note('B#', 0).nat_bi_index == 0
    assert notation.note('B#', 0).natc_index == 6
    assert notation.note('B#', 0).acc_value == 1

    assert notation.note('Bx', 0).nat_bi_index == 0
    assert notation.note('Bx', 0).natc_index == 6
    assert notation.note('Bx', 0).acc_value == 2

    assert notation.note('C', 1).nat_bi_index == 1
    assert notation.note('C', 1).natc_index == 0
    assert notation.note('C', 1).acc_value == 0

    assert notation.note('Dbb', 1).nat_bi_index == 1
    assert notation.note('Dbb', 1).natc_index == 1
    assert notation.note('Dbb', 1).acc_value == -2

    assert notation.note('E#', 3).nat_bi_index == 3
    assert notation.note('E#', 3).natc_index == 2
    assert notation.note('E#', 3).acc_value == 1

    assert notation.note('Fb', 3).nat_bi_index == 3
    assert notation.note('Fb', 3).natc_index == 3
    assert notation.note('Fb', 3).acc_value == -1

    # weird cases

    assert notation.note('Dxxx', 1).nat_bi_index == 1
    assert notation.note('Dxxx', 1).natc_index == 1
    assert notation.note('Dxxx', 1).acc_value == 6

    assert notation.note('Dbbx', 1).nat_bi_index == 1
    assert notation.note('Dbbx', 1).natc_index == 1
    assert notation.note('Dbbx', 1).acc_value == 0

    assert notation.note('D#bb', 1).nat_bi_index == 1
    assert notation.note('D#bb', 1).natc_index == 1
    assert notation.note('D#bb', 1).acc_value == -1


def test_init_notation_edo12():

    notation = UpDownNotation(edo12)

    for natural_symbol in ['C', 'D', 'E', 'F', 'G', 'A', 'B']:
        note = notation.note(natural_symbol, 1)
        assert note.nat_pc_index == note.pc_index

    assert notation.note('B#', 0).nat_pc_index == 11
    assert notation.note('B#', 0).pc_index == 0
    assert not notation.note('B#', 0).is_notated_natural
    assert notation.note('B#', 0).is_enharmonic_natural

    assert notation.note('Cb', 1).nat_pc_index == 0
    assert notation.note('Cb', 1).pc_index == 11
    assert not notation.note('B#', 0).is_notated_natural
    assert notation.note('B#', 0).is_enharmonic_natural

    assert notation.note('G#', 1).nat_pc_index == 7
    assert notation.note('G#', 1).pc_index == 8
    assert not notation.note('G#', 0).is_notated_natural
    assert not notation.note('G#', 0).is_enharmonic_natural

    assert notation.note('A', 1).nat_pc_index == 9
    assert notation.note('A', 1).pc_index == 9
    assert notation.note('A', 0).is_notated_natural
    assert notation.note('A', 0).is_enharmonic_natural

    assert notation.note('E#', 1).nat_pc_index == 4
    assert notation.note('E#', 1).pc_index == 5
    assert not notation.note('E#', 1).is_notated_natural
    assert notation.note('E#', 1).is_enharmonic_natural


@pytest.mark.parametrize(
    'divisions',
    [17, 24, 31, 38, 45, 52]
)
def test_init_notation_sharpness_2(divisions):

    tuning = EDOTuning(divisions)
    notation = UpDownNotation(tuning)

    assert notation.note('vBb', 0).nat_bi_index == 0
    assert notation.note('vBb', 0).natc_index == 6
    assert notation.note('vBb', 0).acc_value == -3

    assert notation.note('Bb', 0).nat_bi_index == 0
    assert notation.note('Bb', 0).natc_index == 6
    assert notation.note('Bb', 0).acc_value == -2

    assert notation.note('vB', 0).nat_bi_index == 0
    assert notation.note('vB', 0).natc_index == 6
    assert notation.note('vB', 0).acc_value == -1

    assert notation.note('^B', 0).nat_bi_index == 0
    assert notation.note('^B', 0).natc_index == 6
    assert notation.note('^B', 0).acc_value == 1

    assert notation.note('B#', 0).nat_bi_index == 0
    assert notation.note('B#', 0).natc_index == 6
    assert notation.note('B#', 0).acc_value == 2

    assert notation.note('^B#', 0).nat_bi_index == 0
    assert notation.note('^B#', 0).natc_index == 6
    assert notation.note('^B#', 0).acc_value == 3

    assert notation.note('Bx', 0).nat_bi_index == 0
    assert notation.note('Bx', 0).natc_index == 6
    assert notation.note('Bx', 0).acc_value == 4

    assert notation.note('C', 1).nat_bi_index == 1
    assert notation.note('C', 1).natc_index == 0
    assert notation.note('C', 1).acc_value == 0

    assert notation.note('Dbb', 1).nat_bi_index == 1
    assert notation.note('Dbb', 1).natc_index == 1
    assert notation.note('Dbb', 1).acc_value == -4

    assert notation.note('E#', 3).nat_bi_index == 3
    assert notation.note('E#', 3).natc_index == 2
    assert notation.note('E#', 3).acc_value == 2

    assert notation.note('Fb', 3).nat_bi_index == 3
    assert notation.note('Fb', 3).natc_index == 3
    assert notation.note('Fb', 3).acc_value == -2

    # weird cases

    assert notation.note('Dxxx', 1).nat_bi_index == 1
    assert notation.note('Dxxx', 1).natc_index == 1
    assert notation.note('Dxxx', 1).acc_value == 12

    assert notation.note('Dbbx', 1).nat_bi_index == 1
    assert notation.note('Dbbx', 1).natc_index == 1
    assert notation.note('Dbbx', 1).acc_value == 0

    assert notation.note('^^D#b', 1).nat_bi_index == 1
    assert notation.note('^D#bb', 1).natc_index == 1
    assert notation.note('^D#bb', 1).acc_value == -1


def test_init_notation_edo31():

    notation = UpDownNotation(edo31)

    for natural_symbol in ['C', 'D', 'E', 'F', 'G', 'A', 'B']:
        note = notation.note(natural_symbol, 1)
        assert note.nat_pc_index == note.pc_index

    assert notation.note('^B', 0).nat_pc_index == 28
    assert notation.note('^B', 0).pc_index == 29
    assert not notation.note('^B', 0).is_notated_natural
    assert not notation.note('^B', 0).is_enharmonic_natural

    assert notation.note('B#', 0).nat_pc_index == 28
    assert notation.note('B#', 0).pc_index == 30
    assert not notation.note('B#', 0).is_notated_natural
    assert not notation.note('B#', 0).is_enharmonic_natural

    assert notation.note('^B#', 0).nat_pc_index == 28
    assert notation.note('^B#', 0).pc_index == 0
    assert not notation.note('^B#', 0).is_notated_natural
    assert notation.note('^B#', 0).is_enharmonic_natural

    assert notation.note('Gbb', 1).nat_pc_index == 18
    assert notation.note('Gbb', 1).pc_index == 14
    assert not notation.note('vGb', 0).is_notated_natural
    assert not notation.note('vGb', 0).is_enharmonic_natural

    assert notation.note('vGb', 1).nat_pc_index == 18
    assert notation.note('vGb', 1).pc_index == 15
    assert not notation.note('vGb', 0).is_notated_natural
    assert not notation.note('vGb', 0).is_enharmonic_natural

    assert notation.note('Gb', 1).nat_pc_index == 18
    assert notation.note('Gb', 1).pc_index == 16
    assert not notation.note('Gb', 0).is_notated_natural
    assert not notation.note('Gb', 0).is_enharmonic_natural

    assert notation.note('vG', 1).nat_pc_index == 18
    assert notation.note('vG', 1).pc_index == 17
    assert not notation.note('vG', 0).is_notated_natural
    assert not notation.note('vG', 0).is_enharmonic_natural

    assert notation.note('G', 1).nat_pc_index == 18
    assert notation.note('G', 1).pc_index == 18
    assert notation.note('G', 0).is_notated_natural
    assert notation.note('G', 0).is_enharmonic_natural


@pytest.mark.parametrize(
    'divisions',
    [22, 29, 36, 43, 50, 57, 64]
)
def test_init_notation_sharpness_3(divisions):

    tuning = EDOTuning(divisions)
    notation = UpDownNotation(tuning)

    assert notation.note('vBb', 0).nat_bi_index == 0
    assert notation.note('vBb', 0).natc_index == 6
    assert notation.note('vBb', 0).acc_value == -4

    assert notation.note('Bb', 0).nat_bi_index == 0
    assert notation.note('Bb', 0).natc_index == 6
    assert notation.note('Bb', 0).acc_value == -3

    assert notation.note('^Bb', 0).nat_bi_index == 0
    assert notation.note('^Bb', 0).natc_index == 6
    assert notation.note('^Bb', 0).acc_value == -2

    assert notation.note('vB', 0).nat_bi_index == 0
    assert notation.note('vB', 0).natc_index == 6
    assert notation.note('vB', 0).acc_value == -1

    assert notation.note('B', 0).nat_bi_index == 0
    assert notation.note('B', 0).natc_index == 6
    assert notation.note('B', 0).acc_value == 0

    assert notation.note('^B', 0).nat_bi_index == 0
    assert notation.note('^B', 0).natc_index == 6
    assert notation.note('^B', 0).acc_value == 1

    assert notation.note('vB#', 0).nat_bi_index == 0
    assert notation.note('vB#', 0).natc_index == 6
    assert notation.note('vB#', 0).acc_value == 2

    assert notation.note('B#', 0).nat_bi_index == 0
    assert notation.note('B#', 0).natc_index == 6
    assert notation.note('B#', 0).acc_value == 3

    assert notation.note('^C#', 1).nat_bi_index == 1
    assert notation.note('^C#', 1).natc_index == 0
    assert notation.note('^C#', 1).acc_value == 4

    assert notation.note('Dbb', 1).nat_bi_index == 1
    assert notation.note('Dbb', 1).natc_index == 1
    assert notation.note('Dbb', 1).acc_value == -6

    assert notation.note('Fx', 3).nat_bi_index == 3
    assert notation.note('Fx', 3).natc_index == 3
    assert notation.note('Fx', 3).acc_value == 6

    # weird cases

    assert notation.note('Dxxx', 1).nat_bi_index == 1
    assert notation.note('Dxxx', 1).natc_index == 1
    assert notation.note('Dxxx', 1).acc_value == 18

    assert notation.note('vDbbx', 1).nat_bi_index == 1
    assert notation.note('vDbbx', 1).natc_index == 1
    assert notation.note('vDbbx', 1).acc_value == -1

    assert notation.note('vv^D#bb', 1).nat_bi_index == 1
    assert notation.note('vv^D#bb', 1).natc_index == 1
    assert notation.note('vv^D#bb', 1).acc_value == -4
