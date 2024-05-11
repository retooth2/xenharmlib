import pytest
from xenharmlib import EDOTuning
from xenharmlib.notation.updown import UpDownNotation

# Technically we should really test all EDOs 5-72, but it
# takes a long, long time, so instead we put a couple of
# each sharpness
# ALL_EDOS = set(range(5, 73))
ALL_EDOS = {
    6, 7, 8, 13, 14, 18, 21, 28, 35,
    5, 9, 12, 33,
    10, 11, 38,
    20, 34, 62,
    25, 53, 60,
    30, 37, 44, 72,
    49, 56, 63,
    61,
    66,
    71
}
PERFECT_EDOS = {7, 14, 21, 28, 35}
ABS_SHARP_1_EDOS = {5, 9, 12, 16, 19, 23, 26, 33, 40, 47}
IMPERFECT_EDOS = ALL_EDOS.difference(PERFECT_EDOS)
IMPERFECT_UPDOWN_EDOS = IMPERFECT_EDOS.difference(ABS_SHARP_1_EDOS)


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


def invariant_source_target_note(testcase_list, acc_symbol):
    """
    Modifies the source and target note in a test case list
    with the same additional accidentals to check that the
    interval name result is still the same.
    """

    acc_head = ''
    acc_tail = ''

    for letter in acc_symbol:
        if letter in {'v', '^'}:
            acc_head += letter
        else:
            acc_tail += letter

    new_testcase_list = []
    for testcase in testcase_list:
        pc_s_a, bi_i_a, pc_s_b, bi_i_b, ic_s, n = testcase
        new_testcase_list.append(
            (
                acc_head + pc_s_a + acc_tail,
                bi_i_a,
                acc_head + pc_s_b + acc_tail,
                bi_i_b,
                ic_s,
                n
            )
        )
    return new_testcase_list


def invariant_updown(testcase_list, acc_symbol):
    """
    Modifies the target note and the interval name in a test
    case list with the same up/down accidentals (or reverted
    accidentals in a downwards interval) to check that the
    result is still valid.
    """

    new_testcase_list = []

    for testcase in testcase_list:

        pc_s_a, bi_i_a, pc_s_b, bi_i_b, ic_s, n = testcase

        # P interval logic does not work as '^P' or 'vP'
        # but simply '^' and 'v'
        if ic_s == 'P':
            ic_s = ''

        if n < 0:
            # on negative intervals adding ^ to the target note
            # results in a v in the interval name
            int_acc_symbol = ''
            for letter in acc_symbol:
                if letter == '^':
                    int_acc_symbol += 'v'
                if letter == 'v':
                    int_acc_symbol += '^'
        else:
            # on positive intervals ups/downs get added in the
            # same way to note names and interval names
            int_acc_symbol = acc_symbol

        new_testcase_list.append(
            (
                pc_s_a,
                bi_i_a,
                acc_symbol + pc_s_b,
                bi_i_b,
                int_acc_symbol + ic_s,
                n
            )
        )
    return new_testcase_list


@pytest.mark.parametrize(
    'pc_symbol_a, bi_index_a, pc_symbol_b, bi_index_b, ic_symbol, numeral',
    TESTCASE_LIST_STD_C +
    TESTCASE_LIST_STD_C_NEG +
    TESTCASE_LIST_CROSSOVER_FLAT_D +
    TESTCASE_LIST_CROSSOVER_SHARP_D +
    TESTCASE_LIST_MULTI_BI_B +
    TESTCASE_LIST_MULTI_BI_B_NEG +
    invariant_source_target_note(TESTCASE_LIST_STD_C, 'b') +
    invariant_source_target_note(TESTCASE_LIST_STD_C, '#') +
    invariant_source_target_note(TESTCASE_LIST_STD_C, 'x')
)
@pytest.mark.parametrize(
    'edo_divisions',
    IMPERFECT_EDOS
)
def test_flat_sharp_interval_names_imperfect_edos(edo_divisions,
                                                  pc_symbol_a,
                                                  bi_index_a,
                                                  pc_symbol_b,
                                                  bi_index_b,
                                                  ic_symbol,
                                                  numeral):
    """
    Test that notes with flat and sharps result in the
    correct interval name
    """

    edo12 = EDOTuning(edo_divisions)
    n_edo12 = UpDownNotation(edo12)
    note_a = n_edo12.note(pc_symbol_a, bi_index_a)
    note_b = n_edo12.note(pc_symbol_b, bi_index_b)

    interval = n_edo12.note_interval(note_a, note_b)

    assert interval.shorthand_name == (ic_symbol, numeral)
    assert note_a.transpose(interval) == note_b

    interval = n_edo12.shorthand_interval(ic_symbol, numeral)
    assert note_a.transpose(interval) == note_b


@pytest.mark.parametrize(
    'pc_symbol_a, bi_index_a, pc_symbol_b, bi_index_b, ic_symbol, numeral',
    invariant_source_target_note(TESTCASE_LIST_STD_C, 'v') +
    invariant_source_target_note(TESTCASE_LIST_STD_C, 'vv') +
    invariant_source_target_note(TESTCASE_LIST_STD_C, '^') +
    invariant_source_target_note(TESTCASE_LIST_STD_C, '^^') +
    invariant_source_target_note(TESTCASE_LIST_STD_C, 'b^') +
    invariant_source_target_note(TESTCASE_LIST_STD_C, '#^') +
    invariant_source_target_note(TESTCASE_LIST_STD_C, 'x^') +
    invariant_source_target_note(TESTCASE_LIST_STD_C, 'bv') +
    invariant_source_target_note(TESTCASE_LIST_STD_C, '#v') +
    invariant_source_target_note(TESTCASE_LIST_STD_C, 'xv') +
    invariant_updown(TESTCASE_LIST_STD_C, '^^^') +
    invariant_updown(TESTCASE_LIST_STD_C, '^^') +
    invariant_updown(TESTCASE_LIST_STD_C, '^') +
    invariant_updown(TESTCASE_LIST_STD_C, 'v') +
    invariant_updown(TESTCASE_LIST_STD_C, 'vv') +
    invariant_updown(TESTCASE_LIST_STD_C, 'vvv') +
    invariant_updown(TESTCASE_LIST_STD_C_NEG, '^^^') +
    invariant_updown(TESTCASE_LIST_STD_C_NEG, '^^') +
    invariant_updown(TESTCASE_LIST_STD_C_NEG, '^') +
    invariant_updown(TESTCASE_LIST_STD_C_NEG, 'v') +
    invariant_updown(TESTCASE_LIST_STD_C_NEG, 'vv') +
    invariant_updown(TESTCASE_LIST_STD_C_NEG, 'vvv') +
    invariant_updown(TESTCASE_LIST_CROSSOVER_FLAT_D, '^^^') +
    invariant_updown(TESTCASE_LIST_CROSSOVER_FLAT_D, '^^') +
    invariant_updown(TESTCASE_LIST_CROSSOVER_FLAT_D, '^') +
    invariant_updown(TESTCASE_LIST_CROSSOVER_FLAT_D, 'v') +
    invariant_updown(TESTCASE_LIST_CROSSOVER_FLAT_D, 'vv') +
    invariant_updown(TESTCASE_LIST_CROSSOVER_FLAT_D, 'vvv') +
    invariant_updown(TESTCASE_LIST_CROSSOVER_SHARP_D, '^^^') +
    invariant_updown(TESTCASE_LIST_CROSSOVER_SHARP_D, '^^') +
    invariant_updown(TESTCASE_LIST_CROSSOVER_SHARP_D, '^') +
    invariant_updown(TESTCASE_LIST_CROSSOVER_SHARP_D, 'v') +
    invariant_updown(TESTCASE_LIST_CROSSOVER_SHARP_D, 'vv') +
    invariant_updown(TESTCASE_LIST_CROSSOVER_SHARP_D, 'vvv') +
    invariant_updown(TESTCASE_LIST_MULTI_BI_B, '^^^') +
    invariant_updown(TESTCASE_LIST_MULTI_BI_B, '^^') +
    invariant_updown(TESTCASE_LIST_MULTI_BI_B, '^') +
    invariant_updown(TESTCASE_LIST_MULTI_BI_B, 'v') +
    invariant_updown(TESTCASE_LIST_MULTI_BI_B, 'vv') +
    invariant_updown(TESTCASE_LIST_MULTI_BI_B, 'vvv') +
    invariant_updown(TESTCASE_LIST_MULTI_BI_B_NEG, '^^^') +
    invariant_updown(TESTCASE_LIST_MULTI_BI_B_NEG, '^^') +
    invariant_updown(TESTCASE_LIST_MULTI_BI_B_NEG, '^') +
    invariant_updown(TESTCASE_LIST_MULTI_BI_B_NEG, 'v') +
    invariant_updown(TESTCASE_LIST_MULTI_BI_B_NEG, 'vv') +
    invariant_updown(TESTCASE_LIST_MULTI_BI_B_NEG, 'vvv')
)
@pytest.mark.parametrize(
    'edo_divisions',
    IMPERFECT_UPDOWN_EDOS
)
def test_up_down_interval_names_imperfect_edos(
    edo_divisions,
    pc_symbol_a,
    bi_index_a,
    pc_symbol_b,
    bi_index_b,
    ic_symbol,
    numeral
):
    """
    Test if ups and downs are applied correctly
    to imperfect EDOs that have abs(sharpness) != 1
    """

    edo = EDOTuning(edo_divisions)

    n_edo = UpDownNotation(edo)

    note_a = n_edo.note(pc_symbol_a, bi_index_a)
    note_b = n_edo.note(pc_symbol_b, bi_index_b)

    interval = n_edo.note_interval(note_a, note_b)

    assert interval.shorthand_name == (ic_symbol, numeral)
    assert note_a.transpose(interval) == note_b

    interval = n_edo.shorthand_interval(ic_symbol, numeral)
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
    'pc_symbol_a, bi_index_a, pc_symbol_b, bi_index_b, ic_symbol, numeral',
    TESTCASE_LIST_PERFECT_C +
    invariant_updown(TESTCASE_LIST_PERFECT_C, 'vvv') +
    invariant_updown(TESTCASE_LIST_PERFECT_C, 'vv') +
    invariant_updown(TESTCASE_LIST_PERFECT_C, 'v') +
    invariant_updown(TESTCASE_LIST_PERFECT_C, '^') +
    invariant_updown(TESTCASE_LIST_PERFECT_C, '^^') +
    invariant_updown(TESTCASE_LIST_PERFECT_C_NEG, '^^^') +
    invariant_updown(TESTCASE_LIST_PERFECT_C_NEG, 'vvv') +
    invariant_updown(TESTCASE_LIST_PERFECT_C_NEG, 'vv') +
    invariant_updown(TESTCASE_LIST_PERFECT_C_NEG, 'v') +
    invariant_updown(TESTCASE_LIST_PERFECT_C_NEG, '^') +
    invariant_updown(TESTCASE_LIST_PERFECT_C_NEG, '^^') +
    invariant_updown(TESTCASE_LIST_PERFECT_C_NEG, '^^^')
)
@pytest.mark.parametrize(
    'edo_divisions',
    PERFECT_EDOS
)
def test_interval_names_perfect_edos(
    edo_divisions,
    pc_symbol_a,
    bi_index_a,
    pc_symbol_b,
    bi_index_b,
    ic_symbol,
    numeral
):
    """
    Test if ups and downs are applied correctly
    to perfect EDOs (those without sharps and flats)
    """

    edo = EDOTuning(edo_divisions)

    n_edo = UpDownNotation(edo)

    note_a = n_edo.note(pc_symbol_a, bi_index_a)
    note_b = n_edo.note(pc_symbol_b, bi_index_b)

    interval = n_edo.note_interval(note_a, note_b)

    assert interval.shorthand_name == (ic_symbol, numeral)
    assert note_a.transpose(interval) == note_b

    interval = n_edo.shorthand_interval(ic_symbol, numeral)
    assert note_a.transpose(interval) == note_b
