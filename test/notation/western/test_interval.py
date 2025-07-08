import pytest
from xenharmlib.notation.western import WesternNotation


TESTCASE_LIST_STD_C = [
    ('C',     1, 'Cbb',   1, 'dd',     1),
    ('C',     1, 'Cb',    1, 'd',      1),
    ('C',     1, 'C',     1, 'P',      1),
    ('C',     1, 'C#',    1, 'A',      1),
    ('C',     1, 'Cx',    1, 'AA',     1),
    ('C',     1, 'Dbbb',  1, 'dd',     2),
    ('C',     1, 'Dbb',   1, 'd',      2),
    ('C',     1, 'Db',    1, 'm',      2),
    ('C',     1, 'D',     1, 'M',      2),
    ('C',     1, 'D#',    1, 'A',      2),
    ('C',     1, 'Dx',    1, 'AA',     2),
    ('C',     1, 'Ebbb',  1, 'dd',     3),
    ('C',     1, 'Ebb',   1, 'd',      3),
    ('C',     1, 'Eb',    1, 'm',      3),
    ('C',     1, 'E',     1, 'M',      3),
    ('C',     1, 'E#',    1, 'A',      3),
    ('C',     1, 'Ex',    1, 'AA',     3),
    ('C',     1, 'Fbb',   1, 'dd',     4),
    ('C',     1, 'Fb',    1, 'd',      4),
    ('C',     1, 'F',     1, 'P',      4),
    ('C',     1, 'F#',    1, 'A',      4),
    ('C',     1, 'Fx',    1, 'AA',     4),
    ('C',     1, 'Gbb',   1, 'dd',     5),
    ('C',     1, 'Gb',    1, 'd',      5),
    ('C',     1, 'G',     1, 'P',      5),
    ('C',     1, 'G#',    1, 'A',      5),
    ('C',     1, 'Gx',    1, 'AA',     5),
    ('C',     1, 'Abbb',  1, 'dd',     6),
    ('C',     1, 'Abb',   1, 'd',      6),
    ('C',     1, 'Ab',    1, 'm',      6),
    ('C',     1, 'A',     1, 'M',      6),
    ('C',     1, 'A#',    1, 'A',      6),
    ('C',     1, 'Ax',    1, 'AA',     6),
    ('C',     1, 'Bbbb',  1, 'dd',     7),
    ('C',     1, 'Bbb',   1, 'd',      7),
    ('C',     1, 'Bb',    1, 'm',      7),
    ('C',     1, 'B',     1, 'M',      7),
    ('C',     1, 'B#',    1, 'A',      7),
    ('C',     1, 'Bx',    1, 'AA',     7),
]

# Note: there are equalities of (d, 1) and (A, -1), (d, -1) and (A, 1)
# (AA, 1) and (dd, -1), etc. The algorithm uses the negative form in
# all cases EXCEPT unison, which is always positive 1. This is a choice
# to avoid weird ambiguities like (P, 1) = (P, -1). It is also imho the
# most intuitive way, for example Cbb -- (AA, 1) --> C makes much more
# sense than Cbb --> (dd, -1) --> C

TESTCASE_LIST_STD_C_NEG = [
    ('Cbb',   1, 'C',     1, 'AA',     1),
    ('Cb',    1, 'C',     1, 'A',      1),
    ('C',     1, 'C',     1, 'P',      1),
    ('C#',    1, 'C',     1, 'd',      1),
    ('Cx',    1, 'C',     1, 'dd',     1),
    ('Dbbb',  1, 'C',     1, 'dd',    -2),
    ('Dbb',   1, 'C',     1, 'd',     -2),
    ('Db',    1, 'C',     1, 'm',     -2),
    ('D',     1, 'C',     1, 'M',     -2),
    ('D#',    1, 'C',     1, 'A',     -2),
    ('Dx',    1, 'C',     1, 'AA',    -2),
    ('Ebbb',  1, 'C',     1, 'dd',    -3),
    ('Ebb',   1, 'C',     1, 'd',     -3),
    ('Eb',    1, 'C',     1, 'm',     -3),
    ('E',     1, 'C',     1, 'M',     -3),
    ('E#',    1, 'C',     1, 'A',     -3),
    ('Ex',    1, 'C',     1, 'AA',    -3),
    ('Fbb',   1, 'C',     1, 'dd',    -4),
    ('Fb',    1, 'C',     1, 'd',     -4),
    ('F',     1, 'C',     1, 'P',     -4),
    ('F#',    1, 'C',     1, 'A',     -4),
    ('Fx',    1, 'C',     1, 'AA',    -4),
    ('Gbb',   1, 'C',     1, 'dd',    -5),
    ('Gb',    1, 'C',     1, 'd',     -5),
    ('G',     1, 'C',     1, 'P',     -5),
    ('G#',    1, 'C',     1, 'A',     -5),
    ('Gx',    1, 'C',     1, 'AA',    -5),
    ('Abbb',  1, 'C',     1, 'dd',    -6),
    ('Abb',   1, 'C',     1, 'd',     -6),
    ('Ab',    1, 'C',     1, 'm',     -6),
    ('A',     1, 'C',     1, 'M',     -6),
    ('A#',    1, 'C',     1, 'A',     -6),
    ('Ax',    1, 'C',     1, 'AA',    -6),
    ('Bbbb',  1, 'C',     1, 'dd',    -7),
    ('Bbb',   1, 'C',     1, 'd',     -7),
    ('Bb',    1, 'C',     1, 'm',     -7),
    ('B',     1, 'C',     1, 'M',     -7),
    ('B#',    1, 'C',     1, 'A',     -7),
    ('Bx',    1, 'C',     1, 'AA',    -7),
]

# a list of intervals in key D where the second note has an accidental value
# which makes it 'cross over' the pitch index of the source, for example in
# 12-EDO the interval (D-0, Ebbb-0) in which the pitch index of D-0 is 2 while
# the pitch index of Ebbb is 1.

TESTCASE_LIST_CROSSOVER_FLAT_D = [
    ('D',          1, 'Ebbb',      1, 'dd',          2),
    ('D',          1, 'Ebbbb',     1, 'ddd',         2),
    ('D',          1, 'Ebbbbb',    1, 'dddd',        2),
    ('D',          1, 'Fbbbb',     1, 'dddd',        3),
    ('D',          1, 'Fbbbbb',    1, 'ddddd',       3),
    ('D',          1, 'Gbbbb',     1, 'dddd',        4),
    ('D',          1, 'Gbbbbb',    1, 'ddddd',       4),
    ('D',          1, 'Abbbbbb',   1, 'dddddd',      5),
    ('D',          1, 'Abbbbbbb',  1, 'ddddddd',     5),
]

TESTCASE_LIST_CROSSOVER_SHARP_D = [
    ('D###',       1, 'E',         1, 'dd',          2),
    ('D####',      1, 'E',         1, 'ddd',         2),
    ('D#####',     1, 'E',         1, 'dddd',        2),
    ('D####',      1, 'F',         1, 'dddd',        3),
    ('D#####',     1, 'F',         1, 'ddddd',       3),
    ('D######',    1, 'F',         1, 'dddddd',      3),
]

TESTCASE_LIST_MULTI_BI_B = [
    ('B',          1, 'C#',         2, 'M',          2),
    ('B',          1, 'F#',         3, 'P',         12),
    ('B',          1, 'Fx',         4, 'A',         19),
    ('B',          1, 'F',          5, 'd',         26),
    ('B',          1, 'Fb',         5, 'dd',        26),
    ('B',          1, 'E',          5, 'P',         25),
]

TESTCASE_LIST_MULTI_BI_B_NEG = [
    ('C#',         2, 'B',          1, 'M',         -2),
    ('F#',         3, 'B',          1, 'P',        -12),
    ('Fx',         4, 'B',          1, 'A',        -19),
    ('F',          5, 'B',          1, 'd',        -26),
    ('Fb',         5, 'B',          1, 'dd',       -26),
    ('E',          5, 'B',          1, 'P',        -25),
]


@pytest.mark.parametrize(
    'pc_symbol_a, bi_index_a, pc_symbol_b, bi_index_b, ic_symbol, numeral',
    TESTCASE_LIST_STD_C +
    TESTCASE_LIST_STD_C_NEG +
    TESTCASE_LIST_CROSSOVER_FLAT_D +
    TESTCASE_LIST_CROSSOVER_SHARP_D +
    TESTCASE_LIST_MULTI_BI_B +
    TESTCASE_LIST_MULTI_BI_B_NEG
)
def test_flat_sharp_interval_names_imperfect_edos(pc_symbol_a,
                                                  bi_index_a,
                                                  pc_symbol_b,
                                                  bi_index_b,
                                                  ic_symbol,
                                                  numeral):
    """
    Test that notes with flat and sharps result in the
    correct interval name
    """

    notation = WesternNotation()

    note_a = notation.note(pc_symbol_a, bi_index_a)
    note_b = notation.note(pc_symbol_b, bi_index_b)

    with pytest.deprecated_call():
        interval = notation.note_interval(note_a, note_b)

    assert interval.shorthand_name == (ic_symbol, numeral)
    assert note_a.transpose(interval) == note_b

    interval = notation.interval(note_a, note_b)

    assert interval.shorthand_name == (ic_symbol, numeral)
    assert note_a.transpose(interval) == note_b

    interval = notation.shorthand_interval(ic_symbol, numeral)
    assert note_a.transpose(interval) == note_b


TESTCASE_LIST_PERFECT_C = [
    ('C',     1, 'C',     1, 'P',      1),
    ('C',     1, 'D',     1, 'P',      2),
    ('C',     1, 'E',     1, 'P',      3),
    ('C',     1, 'F',     1, 'P',      4),
    ('C',     1, 'G',     1, 'P',      5),
    ('C',     1, 'A',     1, 'P',      6),
    ('C',     1, 'B',     1, 'P',      7),
    ('C',     1, 'C',     2, 'P',      8),
    ('C',     1, 'D',     2, 'P',      9),
    ('C',     1, 'E',     2, 'P',     10),
    ('C',     1, 'F',     2, 'P',     11),
    ('C',     1, 'G',     2, 'P',     12),
]


TESTCASE_LIST_PERFECT_C_NEG = [
    ('D',     1, 'C',     1, 'P',     -2),
    ('E',     1, 'C',     1, 'P',     -3),
    ('F',     1, 'C',     1, 'P',     -4),
    ('G',     1, 'C',     1, 'P',     -5),
    ('A',     1, 'C',     1, 'P',     -6),
    ('B',     1, 'C',     1, 'P',     -7),
    ('C',     2, 'C',     1, 'P',     -8),
    ('D',     2, 'C',     1, 'P',     -9),
    ('E',     2, 'C',     1, 'P',    -10),
    ('F',     2, 'C',     1, 'P',    -11),
    ('G',     2, 'C',     1, 'P',    -12),
]


@pytest.mark.parametrize(
    'pitch_diff',
    [3, 0, -3, 40]
)
def test_diff_interval(pitch_diff):

    notation = WesternNotation()

    created = notation.diff_interval(pitch_diff)
    note_a = notation.note('D', 2)
    note_b = note_a.transpose(pitch_diff)
    expected = note_a.interval(note_b)

    assert created == expected
