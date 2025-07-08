import pytest
from xenharmlib.notation.western import WesternNotation


@pytest.mark.parametrize(
    'note_pair, pitch_index',
    [
        (('C',  0),   0),
        (('C#', 0),   1),
        (('Db', 0),   1),
        (('D',  0),   2),
        (('D#', 0),   3),
        (('Eb', 0),   3),
        (('E',  0),   4),
        (('F',  0),   5),
        (('F#', 0),   6),
        (('Gb', 0),   6),
        (('G',  0),   7),
        (('G#', 0),   8),
        (('Ab', 0),   8),
        (('A',  0),   9),
        (('A#', 0),  10),
        (('Bb', 0),  10),
        (('B',  0),  11),
        (('C',  1),  12),
    ]
)
def test_note_pitch_index(note_pair, pitch_index):
    """
    Test if pitch indices get calculated correctly
    """
    notation = WesternNotation()
    note = notation.note(*note_pair)
    assert note.pitch_index == pitch_index


def test_note_properties():

    notation = WesternNotation()

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
