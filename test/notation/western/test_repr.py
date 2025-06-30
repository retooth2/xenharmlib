from xenharmlib import WesternNotation


def test_note_repr():

    notation = WesternNotation()
    assert repr(notation.note('B#', 0)) == 'WesternNote(B#, 0)'
    assert repr(notation.note('C', 4)) == 'WesternNote(C, 4)'


def test_interval_repr():

    notation = WesternNotation()

    i1 = notation.shorthand_interval('A', 3)
    assert repr(i1) == 'WesternNoteInterval(A, 3)'

    i2 = notation.shorthand_interval('M', -2)
    assert repr(i2) == 'WesternNoteInterval(M, -2)'


def test_scale_repr():

    notation = WesternNotation()

    scale = notation.pc_scale(['C', 'E', 'F'], 3)
    assert repr(scale) == 'WesternNoteScale([C3, E3, F3])'

    scale = notation.scale(
        [
            notation.note('F#', 2),
            notation.note('A', 2),
            notation.note('C', 3)
        ]
    )
    assert repr(scale) == 'WesternNoteScale([F#2, A2, C3])'


def test_interval_seq_repr():

    notation = WesternNotation()

    iseq = notation.interval_seq(
        [
            notation.shorthand_interval('A', 2),
            notation.shorthand_interval('P', 4)
        ]
    )
    assert repr(iseq) == 'WesternNoteIntervalSeq([A2, P4])'
