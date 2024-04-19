import pytest

from xenharmlib import EDOTuning
from xenharmlib.exc import UnknownNoteSymbol
from xenharmlib.exc import IncompatibleNotations
from xenharmlib.exc import InvalidGenerator
from ..utils import make_nat_acc_test_notation

edo12 = EDOTuning(12)
edo24 = EDOTuning(24)
edo31 = EDOTuning(31)

n_edo12 = make_nat_acc_test_notation(edo12)
n_edo24 = make_nat_acc_test_notation(edo24)
n_edo31 = make_nat_acc_test_notation(edo31)

@pytest.mark.parametrize(
    'notation, pc_symbol, nat_bi_index, pitch_index',
    [
        (n_edo12, 'Bx+', 0, 5),
        (n_edo12, 'Bx+', 1, 17),
        (n_edo31, 'D--', 0, 4),
        (n_edo31, 'D--', 2, 66),
        (n_edo31, 'A--', 0, -2),
    ]
)
def test_note_pitch_index(notation, pc_symbol, nat_bi_index, pitch_index):
    """
    Test if pitch index of note is returned correctly
    """

    note = notation.note(pc_symbol, nat_bi_index)
    assert note.pitch_index == pitch_index


@pytest.mark.parametrize(
    'notation, pc_symbol, nat_bi_index, pc_index',
    [
        (n_edo12, 'Bx+', 0, 5),
        (n_edo12, 'Bx++', 1, 6),
        (n_edo31, 'D--', 0, 4),
        (n_edo31, 'D--.', 2, 2),
        (n_edo31, 'A--', 0, 29),
    ]
)
def test_note_pc_index(notation, pc_symbol, nat_bi_index, pc_index):
    """
    Test if pitch class index of note is returned correctly
    """

    note = notation.note(pc_symbol, nat_bi_index)
    assert note.pc_index == pc_index


@pytest.mark.parametrize(
    'notation, pc_symbol, nat_bi_index, bi_index',
    [
        (n_edo12, 'F++', 0, 1),
        (n_edo12, 'Bx++', 1, 1),
        (n_edo31, 'D--', 0, 0),
        (n_edo31, 'A--.', 2, 1),
        (n_edo31, 'A--', 0, -1),
    ]
)
def test_note_bi_index(notation, pc_symbol, nat_bi_index, bi_index):
    """
    Test if base interval index of note is returned correctly
    """

    note = notation.note(pc_symbol, nat_bi_index)
    assert note.bi_index == bi_index


@pytest.mark.parametrize(
    'notation, pc_symbol, nat_bi_index, nat_index',
    [
        (n_edo12, 'Bx+', 0, 1),
        (n_edo12, 'Bx+', 1, 7),
        (n_edo31, 'D--', 0, 3),
        (n_edo31, 'D--', 2, 35),
        (n_edo12, 'F', -2, -7),
    ]
)
def test_note_nat_index(notation, pc_symbol, nat_bi_index, nat_index):
    """
    Test if natural index of note is returned correctly
    """

    note = notation.note(pc_symbol, nat_bi_index)
    assert note.nat_index == nat_index


@pytest.mark.parametrize(
    'notation, pc_symbol, nat_bi_index, natc_index',
    [
        (n_edo12, 'Bx+', 0, 1),
        (n_edo12, 'Bx+', 1, 1),
        (n_edo31, 'D--', 0, 3),
        (n_edo31, 'D--', 2, 3),
        (n_edo12, 'F', -2, 5),
    ]
)
def test_note_natc_index(notation, pc_symbol, nat_bi_index, natc_index):
    """
    Test if natural class index of note is returned correctly
    """

    note = notation.note(pc_symbol, nat_bi_index)
    assert note.natc_index == natc_index


@pytest.mark.parametrize(
    'notation, pc_symbol, nat_bi_index, nat_pitch_index',
    [
        (n_edo12, 'Bx+', 0, 2),
        (n_edo12, 'Bx+', 1, 14),
        (n_edo31, 'D--', 0, 6),
        (n_edo31, 'D--', 2, 68),
        (n_edo12, 'F', -2, -14),
    ]
)
def test_note_nat_pitch_index(
    notation,
    pc_symbol,
    nat_bi_index,
    nat_pitch_index
):
    """
    Test if natural pitch index of note is returned correctly
    """

    note = notation.note(pc_symbol, nat_bi_index)
    assert note.nat_pitch_index == nat_pitch_index


@pytest.mark.parametrize(
    'notation, pc_symbol, nat_bi_index, nat_pc_index',
    [
        (n_edo12, 'Bx+', 0, 2),
        (n_edo12, 'Bx+', 1, 2),
        (n_edo31, 'D--', 0, 6),
        (n_edo31, 'D--', 2, 6),
        (n_edo12, 'F', -2, 10),
    ]
)
def test_note_nat_pc_index(
    notation,
    pc_symbol,
    nat_bi_index,
    nat_pc_index
):
    """
    Test if natural pitch class index of note is returned correctly
    """

    note = notation.note(pc_symbol, nat_bi_index)
    assert note.nat_pc_index == nat_pc_index


@pytest.mark.parametrize(
    'notation, pc_symbol, nat_bi_index, natc_symbol',
    [
        (n_edo12, 'Bx+', 0,  'B'),
        (n_edo12, 'Bx+', 1,  'B'),
        (n_edo31, 'F--', 0,  'F'),
        (n_edo31, 'G+-', 2,  'G'),
        (n_edo31, 'K+-', -1, 'K'),
    ]
)
def test_note_natc_symbol(
    notation,
    pc_symbol,
    nat_bi_index,
    natc_symbol
):
    """
    Test if natural class symbol of note is returned correctly
    """

    note = notation.note(pc_symbol, nat_bi_index)
    assert note.natc_symbol == natc_symbol


@pytest.mark.parametrize(
    'notation, pc_symbol, nat_bi_index, acc_symbol',
    [
        (n_edo12, 'Bx+',    0, 'x+'),
        (n_edo12, 'Bx+',    1, 'x+'),
        (n_edo31, 'F.-..',  0, '.-..'),
        (n_edo31, 'G+-',    2, '+-'),
        (n_edo31, 'B++',   -1, '++'),
    ]
)
def test_note_acc_symbol(
    notation,
    pc_symbol,
    nat_bi_index,
    acc_symbol
):
    """
    Test if accidental symbol of note is returned correctly
    """

    note = notation.note(pc_symbol, nat_bi_index)
    assert note.acc_symbol == acc_symbol


@pytest.mark.parametrize(
    'notation, pc_symbol, nat_bi_index',
    [
        (n_edo12, 'Bx+',    0),
        (n_edo12, 'Bx+',    1),
        (n_edo31, 'F.-..',  2),
        (n_edo31, 'G+-',    2),
        (n_edo31, 'G+-',   -2),
    ]
)
def test_note_pc_symbol(
    notation,
    pc_symbol,
    nat_bi_index
):
    """
    Test if pitch class symbol of note is returned correctly
    """

    note = notation.note(pc_symbol, nat_bi_index)
    assert note.pc_symbol == pc_symbol


@pytest.mark.parametrize(
    'notation, pc_symbol, nat_bi_index, acc_value',
    [
        (n_edo12, 'Bx+',   0,  3),
        (n_edo12, 'Bx+.',  1,  1),
        (n_edo31, 'F',     0,  0),
        (n_edo31, 'G.-',   2, -3),
        (n_edo31, 'A.-',  -1, -3),
    ]
)
def test_note_acc_value(
    notation,
    pc_symbol,
    nat_bi_index,
    acc_value
):
    """
    Test if accidental value of note is returned correctly
    """

    note = notation.note(pc_symbol, nat_bi_index)
    assert note.acc_value == acc_value


@pytest.mark.parametrize(
    'notation, pc_symbol, nat_bi_index, acc_direction',
    [
        (n_edo12, 'Bx+',   0,  1),
        (n_edo12, 'Bx+.',  1,  1),
        (n_edo31, 'F',     0,  0),
        (n_edo31, 'G.-',   2, -1),
        (n_edo31, 'C.-',  -3, -1),
    ]
)
def test_note_acc_direction(
    notation,
    pc_symbol,
    nat_bi_index,
    acc_direction
):
    """
    Test if accidental direction of note is returned correctly
    """

    note = notation.note(pc_symbol, nat_bi_index)
    assert note.acc_direction == acc_direction


@pytest.mark.parametrize(
    'notation, pc_symbol, nat_bi_index',
    [
        (n_edo12, 'Kx+',  0),
        (n_edo12, '?x+.', 1),
        (n_edo31, 'Z',    0),
        (n_edo31, '(.-',  2),
        (n_edo31, '.-',  -1),
    ]
)
def test_note_invalid_natural(notation, pc_symbol, nat_bi_index):
    """
    Test if UnknownNoteSymbol is raised if an invalid natural
    class symbol is given in the note builder method
    """

    with pytest.raises(UnknownNoteSymbol):
        notation.note(pc_symbol, nat_bi_index)


@pytest.mark.parametrize(
    'notation, pc_symbol, nat_bi_index',
    [
        (n_edo12, 'Axb+',  0),
        (n_edo12, 'Ax_+.', 1),
        (n_edo31, 'A()',   0),
        (n_edo31, 'A.?-',  2),
        (n_edo31, 'B..q', -1),
    ]
)
def test_note_invalid_acc(notation, pc_symbol, nat_bi_index):
    """
    Test if UnknownNoteSymbol is raised if an invalid accidental
    symbol is given in the note builder method
    """

    with pytest.raises(UnknownNoteSymbol):
        notation.note(pc_symbol, nat_bi_index)


@pytest.mark.parametrize(
    'notation_a, pc_symbol_a, nat_bi_index_a, '
    'notation_b, pc_symbol_b, nat_bi_index_b',
    [
        (n_edo12, 'B+',   0, n_edo12, 'F',     0),
        (n_edo12, 'Bx+',  0, n_edo12, 'F',     1),
        (n_edo12, 'Cx+',  1, n_edo12, 'Cx++',  1),
        (n_edo12, 'Bx+',  1, n_edo12, 'Cx+',   1),
        (n_edo31, 'D--',  0, n_edo31, 'K',     0),
        (n_edo31, 'D',    2, n_edo12, 'D',     2),
        (n_edo12, 'B',    2, n_edo31, 'D',     2),
        (n_edo12, 'B',   -1, n_edo31, 'A',     0),
        (n_edo12, 'B',   -2, n_edo31, 'F',    -1),
    ]
)
def test_note_lt(
    notation_a,
    pc_symbol_a,
    nat_bi_index_a,
    notation_b,
    pc_symbol_b,
    nat_bi_index_b,
):
    """
    Test if notes can be compared with lesser-than and greater-than
    relations and that lesser-than and greater-than imply inequality
    """

    note_a = notation_a.note(pc_symbol_a, nat_bi_index_a)
    note_b = notation_b.note(pc_symbol_b, nat_bi_index_b)
    assert note_a < note_b
    assert note_b > note_a
    assert note_a != note_b
    assert note_b != note_a


@pytest.mark.parametrize(
    'notation_a, pc_symbol_a, nat_bi_index_a, '
    'notation_b, pc_symbol_b, nat_bi_index_b',
    [
        (n_edo12, 'B+',   0, n_edo12, 'B+',  0),
        (n_edo12, 'Bx',   0, n_edo12, 'C',   0),
        (n_edo12, 'B',    0, n_edo24, 'C',   0),
        (n_edo12, 'C--',  1, n_edo12, 'B',   1),
        (n_edo12, 'B--', -1, n_edo12, 'A',  -1),
    ]
)
def test_note_eq(
    notation_a,
    pc_symbol_a,
    nat_bi_index_a,
    notation_b,
    pc_symbol_b,
    nat_bi_index_b,
):
    """
    Test if notes can be compared with equality sign
    (positive test)
    """

    note_a = notation_a.note(pc_symbol_a, nat_bi_index_a)
    note_b = notation_b.note(pc_symbol_b, nat_bi_index_b)
    assert note_a == note_b
    assert note_b == note_a


@pytest.mark.parametrize(
    'not_a_note',
    ['abc', 1, 1.6, set(), dict()]
)
def test_note_default_not_eq(not_a_note):
    """
    Test if equality test of notes returns False if a random
    object is given instead of a note or pitch
    """

    note = n_edo12.note('B+', 0)
    assert note != not_a_note
    assert not_a_note != note


@pytest.mark.parametrize(
    'notation, pc_symbol, nat_bi_index, '
    'tuning, pitch_index',
    [
        (n_edo12, 'B+',   0, edo12, 10),
        (n_edo12, 'Bx+',  0, edo12, 10),
        (n_edo12, 'Cx+',  1, edo12, 23),
        (n_edo12, 'Bx+',  1, edo12, 26),
        (n_edo31, 'D--',  0, edo31, 90),
        (n_edo31, 'D',    2, edo12, 64),
        (n_edo12, 'B',    2, edo31, 79),
        (n_edo12, 'B',   -1, edo31, 79),
        (n_edo12, 'B',   -1, edo31, -1),
    ]
)
def test_note_lt_pitch(
    notation,
    pc_symbol,
    nat_bi_index,
    tuning,
    pitch_index
):
    """
    Test if notes can be compared with lesser-than and greater-than
    relations to pitches and that lesser-than and greater-than imply
    inequality
    """

    note = notation.note(pc_symbol, nat_bi_index)
    pitch = tuning.pitch(pitch_index)
    assert note < pitch
    assert pitch > note
    assert note != pitch
    assert pitch != note


@pytest.mark.parametrize(
    'notation, pc_symbol, nat_bi_index, '
    'tuning, pitch_index',
    [
        (n_edo12, 'B',    0, edo12, 2),
        (n_edo12, 'Bx',   1, edo12, 16),
        (n_edo12, 'C',    1, edo24, (4+12)*2),
        (n_edo31, 'D--',  1, edo31, 6-2+31),
        (n_edo31, 'D--', -1, edo31, 6-2-31),
    ]
)
def test_note_eq_pitch(
    notation,
    pc_symbol,
    nat_bi_index,
    tuning,
    pitch_index
):
    """
    Test if notes and pitches can be compared with equality sign
    """

    note = notation.note(pc_symbol, nat_bi_index)
    pitch = tuning.pitch(pitch_index)
    assert note == pitch
    assert pitch == note


@pytest.mark.parametrize(
    'notation_a, pc_symbol_a, nat_bi_index_a, '
    'notation_b, pc_symbol_b, nat_bi_index_b',
    [
        (n_edo12, 'B+',   0, n_edo12, 'B+',  1),
        (n_edo12, 'Bx',   0, n_edo12, 'C',   2),
        (n_edo12, 'B',    0, n_edo24, 'C',   3),
        (n_edo12, 'C--',  1, n_edo12, 'B',   9),
        (n_edo12, 'B--', -1, n_edo12, 'A',   0),
    ]
)
def test_note_is_equivalent(
    notation_a,
    pc_symbol_a,
    nat_bi_index_a,
    notation_b,
    pc_symbol_b,
    nat_bi_index_b,
):
    """
    Test if notes can be compared with is_equivalent test
    (positive test)
    """

    note_a = notation_a.note(pc_symbol_a, nat_bi_index_a)
    note_b = notation_b.note(pc_symbol_b, nat_bi_index_b)
    assert note_a.is_equivalent(note_b)
    assert note_b.is_equivalent(note_a)


@pytest.mark.parametrize(
    'notation_a, pc_symbol_a, nat_bi_index_a, '
    'notation_b, pc_symbol_b, nat_bi_index_b',
    [
        (n_edo12, 'B+',   0, n_edo12, 'B',   1),
        (n_edo12, 'Bx',   0, n_edo12, 'C+',  2),
        (n_edo12, 'B',    0, n_edo24, 'A',   3),
        (n_edo12, 'C--',  1, n_edo12, 'C',   9),
        (n_edo12, 'B--', -1, n_edo12, 'B',   0),
    ]
)
def test_note_is_equivalent_neg(
    notation_a,
    pc_symbol_a,
    nat_bi_index_a,
    notation_b,
    pc_symbol_b,
    nat_bi_index_b,
):
    """
    Test if notes can be compared with is_equivalent test
    (negative test)
    """

    note_a = notation_a.note(pc_symbol_a, nat_bi_index_a)
    note_b = notation_b.note(pc_symbol_b, nat_bi_index_b)
    assert not note_a.is_equivalent(note_b)
    assert not note_b.is_equivalent(note_a)


@pytest.mark.parametrize(
    'notation, pc_symbol, nat_bi_index, '
    'tuning, pitch_index',
    [
        (n_edo12, 'B',    0, edo12, 2),
        (n_edo12, 'Bx',   1, edo12, 12+16),
        (n_edo12, 'C',    1, edo24, 24+(4+12)*2),
        (n_edo31, 'D--',  1, edo31, 31+6-2+31),
        (n_edo31, 'D--', -1, edo31, 6-2-31-31),
    ]
)
def test_note_is_equivalent_pitch(
    notation,
    pc_symbol,
    nat_bi_index,
    tuning,
    pitch_index
):
    """
    Test if notes can be compared with pitches using
    is_equivalent test (positive test)
    """

    note = notation.note(pc_symbol, nat_bi_index)
    pitch = tuning.pitch(pitch_index)
    assert note.is_equivalent(pitch)
    assert pitch.is_equivalent(note)


@pytest.mark.parametrize(
    'notation, pc_symbol, nat_bi_index, '
    'tuning, pitch_index',
    [
        (n_edo12, 'B',    0, edo12, 1),
        (n_edo12, 'Bx',   1, edo12, 2),
        (n_edo12, 'C',    1, edo24, 55),
        (n_edo31, 'D--',  1, edo31, 31),
        (n_edo31, 'D--', -1, edo31, 62),
    ]
)
def test_note_is_equivalent_pitch_neg(
    notation,
    pc_symbol,
    nat_bi_index,
    tuning,
    pitch_index
):
    """
    Test if notes can be compared with pitches using
    is_equivalent test (negative test)
    """

    note = notation.note(pc_symbol, nat_bi_index)
    pitch = tuning.pitch(pitch_index)
    assert not note.is_equivalent(pitch)
    assert not pitch.is_equivalent(note)


@pytest.mark.parametrize(
    'notation, pc_symbol, nat_bi_index, expected',
    [
        (n_edo12, 'B',    0, True),
        (n_edo12, 'Bx',   1, False),
        (n_edo31, 'C',    1, True),
        (n_edo31, 'D--',  1, False),
        (n_edo31, 'D--', -1, False),
        (n_edo31, 'D',   -2, True),
    ]
)
def test_note_is_notated_natural(
    notation,
    pc_symbol,
    nat_bi_index,
    expected
):
    """
    Test if is_notated_natural property works correctly
    """

    note = notation.note(pc_symbol, nat_bi_index)
    assert note.is_notated_natural == expected


@pytest.mark.parametrize(
    'notation, pc_symbol, nat_bi_index, expected',
    [
        (n_edo12, 'B',    0, True),
        (n_edo12, 'Bx',   1, True),
        (n_edo12, 'B++',  1, True),
        (n_edo31, 'C-',   1, False),
        (n_edo31, 'C--',  1, True),
        (n_edo12, 'A--', -1, True),
    ]
)
def test_note_is_enharmonic_natural(
    notation,
    pc_symbol,
    nat_bi_index,
    expected
):
    """
    Test if is_enharmonic_natural property works correctly
    """

    note = notation.note(pc_symbol, nat_bi_index)
    assert note.is_enharmonic_natural == expected


@pytest.mark.parametrize(
    'notation, pc_symbol, nat_bi_index, expected',
    [
        (n_edo12, 'B',    0, 'NatAccNote(B, 0, 12-EDO)'),
        (n_edo12, 'Bx',   1, 'NatAccNote(Bx, 1, 12-EDO)'),
        (n_edo12, 'B++',  3, 'NatAccNote(B++, 3, 12-EDO)'),
        (n_edo31, 'C-',   2, 'NatAccNote(C-, 2, 31-EDO)'),
        (n_edo31, 'C--',  1, 'NatAccNote(C--, 1, 31-EDO)'),
        (n_edo12, 'A--', -1, 'NatAccNote(A--, -1, 12-EDO)'),
    ]
)
def test_note_repr(
    notation,
    pc_symbol,
    nat_bi_index,
    expected
):
    """
    Test if repr() function works correctly on notes
    """

    note = notation.note(pc_symbol, nat_bi_index)
    assert repr(note) == expected


@pytest.mark.parametrize(
    'notation, pc_symbol, nat_bi_index, '
    'gen_pc_symbol, gen_nat_bi_index, '
    'gen_index',
    [
        (n_edo12, 'B+',  0, 'D+',  0, 9),
        (n_edo12, 'Bx+', 1, 'C+',  0, 1),
        (n_edo12, 'B',   1, 'C+',  1, 10),
        (n_edo31, 'A',   0, 'B',  0, 0),
        (n_edo31, 'D--', 0, 'K',  0, 25),
    ]
)
def test_note_get_generator_index(
    notation,
    pc_symbol,
    nat_bi_index,
    gen_pc_symbol,
    gen_nat_bi_index,
    gen_index
):
    """
    Test if get_generator_index function returns correct results
    """

    note = notation.note(pc_symbol, nat_bi_index)
    generator = notation.note(gen_pc_symbol, gen_nat_bi_index)
    assert note.get_generator_index(generator) == gen_index


@pytest.mark.parametrize(
    'notation, pc_symbol, nat_bi_index, '
    'gen_pc_symbol, gen_nat_bi_index, ',
    [
        (n_edo12, 'B+',  0, 'D+',  0),
        (n_edo12, 'Bx+', 1, 'C+',  0),
        (n_edo12, 'B',   1, 'C+',  1),
        (n_edo31, 'A',   0, 'B',   0),
        (n_edo31, 'D--', 0, 'K',   0),
    ]
)
def test_note_get_generator_index_diff_notation(
    notation,
    pc_symbol,
    nat_bi_index,
    gen_pc_symbol,
    gen_nat_bi_index
):
    """
    Test if get_generator_index function fails if note and generator
    note are from different notations
    """

    diff_notation = make_nat_acc_test_notation(edo31)

    note = notation.note(pc_symbol, nat_bi_index)
    generator = diff_notation.note(gen_pc_symbol, gen_nat_bi_index)

    with pytest.raises(IncompatibleNotations):
        note.get_generator_index(generator)


@pytest.mark.parametrize(
    'notation, pc_symbol, nat_bi_index, '
    'gen_pc_symbol, gen_nat_bi_index, '
    'gen_index',
    [
        (n_edo12, 'B+',  0, 'B+',  0,  9),
        (n_edo12, 'Bx+', 1, 'B+',  0,  1),
        (n_edo12, 'B',   1, 'B',   1, 10),
        (n_edo24, 'B',   1, 'B',   1,  1),
    ]
)
def test_note_get_generator_index_invalid_generator(
    notation,
    pc_symbol,
    nat_bi_index,
    gen_pc_symbol,
    gen_nat_bi_index,
    gen_index
):
    """
    Test if get_generator_index function fails if given generator
    note is not in fact a generator
    """

    note = notation.note(pc_symbol, nat_bi_index)
    generator = notation.note(gen_pc_symbol, gen_nat_bi_index)

    with pytest.raises(InvalidGenerator):
        note.get_generator_index(generator)


@pytest.mark.parametrize(
    'notation, pc_symbol_a, nat_bi_index_a, '
    'pc_symbol_b, nat_bi_index_b, ',
    [
        (n_edo12, 'B+',  0, 'B+',  0),
        (n_edo12, 'Bx+', 0, 'Bx+', 0),
        (n_edo12, 'A',   0, 'A',   0),
    ]
)
def test_note_is_notated_same(
    notation,
    pc_symbol_a,
    nat_bi_index_a,
    pc_symbol_b,
    nat_bi_index_b,
):
    """
    Test if notes can be compared with is_notated_same
    relation (positive test)
    """

    note_a = notation.note(pc_symbol_a, nat_bi_index_a)
    note_b = notation.note(pc_symbol_b, nat_bi_index_b)
    assert note_a.is_notated_same(note_b)


@pytest.mark.parametrize(
    'notation, pc_symbol_a, nat_bi_index_a, '
    'pc_symbol_b, nat_bi_index_b, ',
    [
        (n_edo12, 'B+',  0, 'B+',  0),
        (n_edo12, 'Bx+', 0, 'Bx+', 0),
        (n_edo12, 'A',   0, 'A',   0),
    ]
)
def test_note_is_notated_same_diff_notation(
    notation,
    pc_symbol_a,
    nat_bi_index_a,
    pc_symbol_b,
    nat_bi_index_b,
):
    """
    Test if is_notated_same relation test fails if the
    two notes are from different notations
    """

    diff_notation = make_nat_acc_test_notation(edo12)

    note_a = notation.note(pc_symbol_a, nat_bi_index_a)
    note_b = diff_notation.note(pc_symbol_b, nat_bi_index_b)

    with pytest.raises(IncompatibleNotations):
        note_a.is_notated_same(note_b)


@pytest.mark.parametrize(
    'notation, pc_symbol_a, nat_bi_index_a, '
    'pc_symbol_b, nat_bi_index_b, ',
    [
        (n_edo12, 'B+',  0, 'Ax+', 0),
        (n_edo12, 'Bx+', 0, 'Bx+', 1),
        (n_edo12, 'A',   0, 'Cx',  0),
    ]
)
def test_note_is_notated_same_neg(
    notation,
    pc_symbol_a,
    nat_bi_index_a,
    pc_symbol_b,
    nat_bi_index_b,
):
    """
    Test if notes can be compared with is_notated_same
    relation (negative test)
    """

    note_a = notation.note(pc_symbol_a, nat_bi_index_a)
    note_b = notation.note(pc_symbol_b, nat_bi_index_b)
    assert not note_a.is_notated_same(note_b)


@pytest.mark.parametrize(
    'notation, pc_symbol_a, nat_bi_index_a, '
    'pc_symbol_b, nat_bi_index_b, ',
    [
        (n_edo12, 'B+',  0, 'B+',  0),
        (n_edo12, 'Bx+', 0, 'Bx+', 1),
        (n_edo12, 'A',   0, 'A',   3),
    ]
)
def test_note_is_notated_equivalent(
    notation,
    pc_symbol_a,
    nat_bi_index_a,
    pc_symbol_b,
    nat_bi_index_b,
):
    """
    Test if notes can be compared with is_notated_equivalent
    relation (positive test)
    """

    note_a = notation.note(pc_symbol_a, nat_bi_index_a)
    note_b = notation.note(pc_symbol_b, nat_bi_index_b)
    assert note_a.is_notated_equivalent(note_b)


@pytest.mark.parametrize(
    'notation, pc_symbol_a, nat_bi_index_a, '
    'pc_symbol_b, nat_bi_index_b, ',
    [
        (n_edo12, 'B+',  0, 'B+',  0),
        (n_edo12, 'Bx+', 0, 'Bx+', 1),
        (n_edo12, 'A',   0, 'A',   3),
    ]
)
def test_note_is_notated_equivalent_diff_notation(
    notation,
    pc_symbol_a,
    nat_bi_index_a,
    pc_symbol_b,
    nat_bi_index_b,
):
    """
    Test if is_notated_equivalent relation test fails if the
    two notes are from different notations
    """

    diff_notation = make_nat_acc_test_notation(edo12)

    note_a = notation.note(pc_symbol_a, nat_bi_index_a)
    note_b = diff_notation.note(pc_symbol_b, nat_bi_index_b)

    with pytest.raises(IncompatibleNotations):
        note_a.is_notated_equivalent(note_b)


@pytest.mark.parametrize(
    'notation, pc_symbol_a, nat_bi_index_a, '
    'pc_symbol_b, nat_bi_index_b, ',
    [
        (n_edo12, 'B+',  0, 'Ax+', 0),
        (n_edo12, 'Bx+', 0, 'B+',  1),
        (n_edo12, 'A',   0, 'Cx',  0),
    ]
)
def test_note_is_notated_equivalent_neg(
    notation,
    pc_symbol_a,
    nat_bi_index_a,
    pc_symbol_b,
    nat_bi_index_b,
):
    """
    Test if notes can be compared with is_notated_equivalent
    relation (negative test)
    """

    note_a = notation.note(pc_symbol_a, nat_bi_index_a)
    note_b = notation.note(pc_symbol_b, nat_bi_index_b)
    assert not note_a.is_notated_equivalent(note_b)