import pytest
from xenharmlib import EDOTuning
from xenharmlib.notation.updown import UpDownNotation

# Technically we should really test all EDOs 5-72, but it
# takes a long, long time, so instead we put a couple of
# each sharpness
# ALL_EDO_DIVS = set(range(5, 73))
ALL_EDO_DIVS = {
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
PERFECT_EDO_DIVS = {7, 14, 21, 28, 35}
ABS_SHARP_1_EDO_DIVS = {5, 9, 12, 16, 19, 23, 26, 33, 40, 47}
IMPERFECT_EDO_DIVS = ALL_EDO_DIVS.difference(PERFECT_EDO_DIVS)
IMPERFECT_UPDOWN_EDO_DIVS = IMPERFECT_EDO_DIVS.difference(ABS_SHARP_1_EDO_DIVS)

IMPERFECT_EDOS = [
    UpDownNotation(EDOTuning(i)) for i in IMPERFECT_EDO_DIVS
]

IMPERFECT_UPDOWN_EDOS = [
    UpDownNotation(EDOTuning(i)) for i in IMPERFECT_UPDOWN_EDO_DIVS
]

PERFECT_EDOS = [UpDownNotation(EDOTuning(i)) for i in PERFECT_EDO_DIVS]

edo12 = EDOTuning(12)
n_edo12 = UpDownNotation(edo12)

edo24 = EDOTuning(24)
n_edo24 = UpDownNotation(edo24)

edo31 = EDOTuning(31)
n_edo31 = UpDownNotation(edo31)

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
    'n_edo',
    IMPERFECT_EDOS
)
def test_flat_sharp_interval_names_imperfect_edos(n_edo,
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

    note_a = n_edo.note(pc_symbol_a, bi_index_a)
    note_b = n_edo.note(pc_symbol_b, bi_index_b)

    with pytest.deprecated_call():
        interval = n_edo.note_interval(note_a, note_b)

    assert interval.shorthand_name == (ic_symbol, numeral)
    assert note_a.transpose(interval) == note_b

    interval = n_edo.interval(note_a, note_b)

    assert interval.shorthand_name == (ic_symbol, numeral)
    assert note_a.transpose(interval) == note_b

    interval = n_edo.shorthand_interval(ic_symbol, numeral)
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
    'n_edo',
    IMPERFECT_UPDOWN_EDOS
)
def test_up_down_interval_names_imperfect_edos(
    n_edo,
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

    note_a = n_edo.note(pc_symbol_a, bi_index_a)
    note_b = n_edo.note(pc_symbol_b, bi_index_b)

    with pytest.deprecated_call():
        interval = n_edo.note_interval(note_a, note_b)

    assert interval.shorthand_name == (ic_symbol, numeral)
    assert note_a.transpose(interval) == note_b

    interval = n_edo.interval(note_a, note_b)

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
    'n_edo',
    PERFECT_EDOS
)
def test_interval_names_perfect_edos(
    n_edo,
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

    note_a = n_edo.note(pc_symbol_a, bi_index_a)
    note_b = n_edo.note(pc_symbol_b, bi_index_b)

    with pytest.deprecated_call():
        interval = n_edo.note_interval(note_a, note_b)

    assert interval.shorthand_name == (ic_symbol, numeral)
    assert note_a.transpose(interval) == note_b

    interval = n_edo.interval(note_a, note_b)

    assert interval.shorthand_name == (ic_symbol, numeral)
    assert note_a.transpose(interval) == note_b

    interval = n_edo.shorthand_interval(ic_symbol, numeral)
    assert note_a.transpose(interval) == note_b


@pytest.mark.parametrize(
    'notation, pitch_diff',
    [
        (n_edo12, 3),
        (n_edo24, 0),
        (n_edo24, -3),
        (n_edo31, 40),
    ]
)
def test_diff_interval(notation, pitch_diff):

    created = notation.diff_interval(pitch_diff)
    note_a = notation.note('D', 2)
    note_b = note_a.transpose(pitch_diff)
    expected = note_a.interval(note_b)

    assert created == expected


@pytest.mark.parametrize(
    'n_edo',
    PERFECT_EDOS
)
@pytest.mark.parametrize(
    'shorthand_name, result_shorthand_name',
    (
        (('P', 3), ('P', 3)),
        (('P', 2), ('P', 2)),
        (('P', 1), ('P', 1)),
        (('vv', 1), ('^^', 1)),
        (('P', -9), ('P', 9)),
        (('P', -33), ('P', 33)),
        (('vv', -33), ('vv', 33)),
    )
)
def test_abs_perfect(n_edo, shorthand_name, result_shorthand_name):
    """
    Test if abs works for perfect EDOs
    """

    interval = n_edo.shorthand_interval(*shorthand_name)
    result_interval = n_edo.shorthand_interval(*result_shorthand_name)

    assert abs(interval) == result_interval


@pytest.mark.parametrize(
    'n_edo',
    PERFECT_EDOS
)
@pytest.mark.parametrize(
    'shorthand_name, result_shorthand_name',
    (
        (('P', 3), ('P', -3)),
        (('P', 2), ('P', -2)),
        (('^', 2), ('^', -2)),
        (('P', 1), ('P', 1)),
        (('vv', 1), ('^^', 1)),
        (('P', -9), ('P', 9)),
    )
)
def test_neg_perfect(n_edo, shorthand_name, result_shorthand_name):
    """
    Test if negation works for perfect EDOs
    """

    interval = n_edo.shorthand_interval(*shorthand_name)
    result_interval = n_edo.shorthand_interval(*result_shorthand_name)

    assert -interval == result_interval
    assert interval == -result_interval


@pytest.mark.parametrize(
    'n_edo',
    PERFECT_EDOS
)
@pytest.mark.parametrize(
    'shorthand_name_a, shorthand_name_b, result_shorthand_name',
    (
        (('P', 3), ('P', -3), ('P', 1)),
        (('P', 2), ('P', 5), ('P', 6)),
        (('P', -2), ('P', -3), ('P', -4)),
        (('P', 8), ('P', -9), ('P', -2)),
    )
)
def test_add_perfect(
    n_edo, shorthand_name_a, shorthand_name_b, result_shorthand_name
):
    """
    Test if addition works for perfect EDOs
    """

    interval_a = n_edo.shorthand_interval(*shorthand_name_a)
    interval_b = n_edo.shorthand_interval(*shorthand_name_b)
    result_interval = n_edo.shorthand_interval(*result_shorthand_name)

    assert interval_a + interval_b == result_interval
    assert (interval_a + interval_b).shorthand_name == result_shorthand_name
    assert interval_b + interval_a == result_interval
    assert (interval_b + interval_a).shorthand_name == result_shorthand_name


@pytest.mark.parametrize(
    'n_edo',
    PERFECT_EDOS
)
@pytest.mark.parametrize(
    'shorthand_name_a, shorthand_name_b, result_shorthand_name',
    (
        (('P', 3), ('P', -3), ('P', 5)),
        (('P', 2), ('P', 5), ('P', -4)),
        (('P', -2), ('P', 1), ('P', -2)),
        (('P', 8), ('P', -9), ('P', 16)),
    )
)
def test_sub_perfect(
    n_edo, shorthand_name_a, shorthand_name_b, result_shorthand_name
):
    """
    Test if subtraction works for perfect EDOs
    """

    interval_a = n_edo.shorthand_interval(*shorthand_name_a)
    interval_b = n_edo.shorthand_interval(*shorthand_name_b)
    result_interval = n_edo.shorthand_interval(*result_shorthand_name)

    assert interval_a - interval_b == result_interval
    assert (interval_a - interval_b).shorthand_name == result_shorthand_name
    assert -(interval_b - interval_a) == result_interval
    assert (-(interval_b - interval_a)).shorthand_name == result_shorthand_name


@pytest.mark.parametrize(
    'n_edo',
    PERFECT_EDOS
)
@pytest.mark.parametrize(
    'shorthand_name, scalar, result_shorthand_name',
    (
        (('P', 3), 2, ('P', 5)),
        (('^', 3), 2, ('^^', 5)),
        (('P', 2), 0, ('P', 1)),
        (('P', 1), 3, ('P', 1)),
        (('^', 1), -3, ('vvv', 1)),
        (('P', 1), -3, ('P', 1)),
        (('P', 2), -3, ('P', -4)),
        (('P', -2), 3, ('P', -4)),
        (('v', -2), 3, ('vvv', -4)),
    )
)
def test_mul_perfect(
    n_edo, shorthand_name, scalar, result_shorthand_name
):
    """
    Test if scalar multiplication works for perfect EDOs
    """

    interval = n_edo.shorthand_interval(*shorthand_name)
    result_interval = n_edo.shorthand_interval(*result_shorthand_name)

    assert interval * scalar == result_interval
    assert scalar * interval == result_interval


@pytest.mark.parametrize(
    'n_edo',
    PERFECT_EDOS
)
@pytest.mark.parametrize(
    'shorthand_name, sign',
    (
        (('P', 3), 1),
        (('^', 3), 1),
        (('P', 2), 1),
        (('P', 1), 0),
        (('^', 1), 1),
        (('v', 1), -1),
        (('P', 2), 1),
        (('P', -2), -1),
        (('v', -3), -1),
    )
)
def test_sign_perfect(
    n_edo, shorthand_name, sign
):
    """
    Test if sign property works for perfect EDOs
    """

    interval = n_edo.shorthand_interval(*shorthand_name)
    assert interval.sign == sign


@pytest.mark.parametrize(
    'n_edo',
    PERFECT_EDOS
)
@pytest.mark.parametrize(
    'shorthand_name, is_simple',
    (
        (('^^', 12), False),
        (('P', 12), False),
        (('P', 2), True),
        (('P', -2), True),
        (('P', -12), False),
        (('v', -12), False),
        (('v', 1), True),
    )
)
def test_simple_compound_perfect(
    n_edo, shorthand_name, is_simple
):
    """
    Test if is_simple and is_compound works for perfect EDOs
    """

    interval = n_edo.shorthand_interval(*shorthand_name)
    assert interval.is_simple == is_simple
    assert interval.is_compound != is_simple


@pytest.mark.parametrize(
    'n_edo',
    PERFECT_EDOS
)
@pytest.mark.parametrize(
    'shorthand_name, result_shorthand_name',
    (
        (('^^', 12), ('^^', 5)),
        (('P', 12), ('P', 5)),
        (('P', 2), ('P', 2)),
        (('P', -2), ('P', -2)),
        (('P', -12), ('P', -5)),
        (('v', -12), ('v', -5)),
        (('v', 1), ('v', 1)),
    )
)
def test_to_simple_perfect(
    n_edo, shorthand_name, result_shorthand_name
):
    """
    Test if to_simple works for perfect EDOs
    """

    interval = n_edo.shorthand_interval(*shorthand_name)
    result_interval = n_edo.shorthand_interval(*result_shorthand_name)

    assert interval.to_simple().is_notated_same(result_interval)


@pytest.mark.parametrize(
    'n_edo',
    PERFECT_EDOS
)
@pytest.mark.parametrize(
    'shorthand_name, result_shorthand_name',
    (
        (('P', 2), ('P', 7)),
        (('P', 12), ('P', -5)),
        (('^^', 12), ('^^', -5)),
        (('P', -2), ('P', 9)),
        (('P', -12), ('P', 19)),
        (('v', -12), ('v', 19)),
        (('v', 1), ('^', 8)),
    )
)
def test_inversion_perfect(
    n_edo, shorthand_name, result_shorthand_name
):
    """
    Test if inversion works for perfect EDOs
    """

    interval = n_edo.shorthand_interval(*shorthand_name)
    result_interval = n_edo.shorthand_interval(*result_shorthand_name)

    assert interval.inversion().is_notated_same(result_interval)


@pytest.mark.parametrize(
    'n_edo',
    PERFECT_EDOS
)
@pytest.mark.parametrize(
    'shorthand_name, result_shorthand_name',
    (
        (('P', 2), ('P', 2)),
        (('P', 12), ('P', 4)),
        (('^^', 12), ('vv', 4)),
        (('P', -2), ('P', 2)),
        (('P', -12), ('P', 4)),
        (('v', 1), ('^', 1)),
    )
)
def test_ic_normalized_ic_index_perfect(
    n_edo, shorthand_name, result_shorthand_name
):
    """
    Test if ic normalization and ic_index works for perfect EDOs
    """

    interval = n_edo.shorthand_interval(*shorthand_name)
    result_interval = n_edo.shorthand_interval(*result_shorthand_name)

    # we don't test on notational equality here, because there
    # are intervals (like A4 in 12-EDO) that have an inversion
    # with exactly the same pitch difference, so the result
    # depends on an implementation detail of which object is
    # chosen in the minimum function

    assert interval.ic_normalized() == result_interval
    assert interval.ic_index == result_interval.pitch_diff


@pytest.mark.parametrize(
    'n_edo',
    IMPERFECT_EDOS
)
@pytest.mark.parametrize(
    'shorthand_name, result_shorthand_name',
    (
        (('P', 5), ('P', 5)),
        (('P', -5), ('P', 5)),
        (('M', -3), ('M', 3)),
        (('P', 1), ('P', 1)),
        (('m', 3), ('m', 3)),
        (('m', -3), ('m', 3)),
        (('A', -5), ('A', 5)),
        (('dd', 12), ('dd', 12)),
        (('dd', -12), ('dd', 12)),
    )
)
def test_abs_imperfect(n_edo, shorthand_name, result_shorthand_name):
    """
    Test if abs works for imperfect EDOs
    """

    interval = n_edo.shorthand_interval(*shorthand_name)
    result_interval = n_edo.shorthand_interval(*result_shorthand_name)

    assert abs(interval) == result_interval


@pytest.mark.parametrize(
    'n_edo',
    IMPERFECT_EDOS
)
@pytest.mark.parametrize(
    'shorthand_name, result_shorthand_name',
    (
        (('P', 5), ('P', -5)),
        (('P', -5), ('P', 5)),
        (('M', -3), ('M', 3)),
        (('P', 1), ('P', 1)),
        (('m', 3), ('m', -3)),
        (('m', -3), ('m', 3)),
        (('A', -5), ('A', 5)),
        (('dd', 12), ('dd', -12)),
        (('dd', -12), ('dd', 12)),
    )
)
def test_neg_imperfect(n_edo, shorthand_name, result_shorthand_name):
    """
    Test if negation works for imperfect EDOs
    """

    interval = n_edo.shorthand_interval(*shorthand_name)
    result_interval = n_edo.shorthand_interval(*result_shorthand_name)

    assert -interval == result_interval
    assert interval == -result_interval


@pytest.mark.parametrize(
    'n_edo',
    IMPERFECT_EDOS
)
@pytest.mark.parametrize(
    'shorthand_name_a, shorthand_name_b, result_shorthand_name',
    (
        (('d', 9), ('P', 1), ('d', 9)),
        (('m', 3), ('m', -3), ('P', 1)),
        (('m', 3), ('M', 3), ('P', 5)),
        (('A', 5), ('M', 2), ('A', 6)),
        (('M', 3), ('A', 2), ('AA', 4)),
        (('P', 8), ('P', -12), ('P', -5)),
    )
)
def test_add_imperfect(
    n_edo, shorthand_name_a, shorthand_name_b, result_shorthand_name
):
    """
    Test if addition works for imperfect EDOs
    """

    interval_a = n_edo.shorthand_interval(*shorthand_name_a)
    interval_b = n_edo.shorthand_interval(*shorthand_name_b)
    result_interval = n_edo.shorthand_interval(*result_shorthand_name)

    assert interval_a + interval_b == result_interval
    assert (interval_a + interval_b).shorthand_name == result_shorthand_name
    assert interval_b + interval_a == result_interval
    assert (interval_b + interval_a).shorthand_name == result_shorthand_name


@pytest.mark.parametrize(
    'n_edo',
    IMPERFECT_EDOS
)
@pytest.mark.parametrize(
    'shorthand_name_a, shorthand_name_b, result_shorthand_name',
    (
        (('d', 9), ('P', 1), ('d', 9)),
        (('m', 3), ('m', -3), ('d', 5)),
        (('m', 3), ('M', 3), ('d', 1)),
        (('P', 8), ('m', 3), ('M', 6)),
        (('m', 3), ('P', 5), ('M', -3)),
        (('d', 3), ('P', 5), ('A', -3)),
    )
)
def test_sub_imperfect(
    n_edo, shorthand_name_a, shorthand_name_b, result_shorthand_name
):
    """
    Test if subtraction works for imperfect EDOs
    """

    interval_a = n_edo.shorthand_interval(*shorthand_name_a)
    interval_b = n_edo.shorthand_interval(*shorthand_name_b)
    result_interval = n_edo.shorthand_interval(*result_shorthand_name)

    assert interval_a - interval_b == result_interval
    assert (interval_a - interval_b).shorthand_name == result_shorthand_name
    assert -(interval_b - interval_a) == result_interval
    assert (-(interval_b - interval_a)).shorthand_name == result_shorthand_name


@pytest.mark.parametrize(
    'n_edo',
    IMPERFECT_EDOS
)
@pytest.mark.parametrize(
    'shorthand_name, scalar, result_shorthand_name',
    (
        (('P', 5), 2, ('M', 9)),
        (('M', 3), 2, ('A', 5)),
        (('m', 6), 1, ('m', 6)),
        (('m', 6), 0, ('P', 1)),
        (('A', 7), 0, ('P', 1)),
        (('m', 6), -1, ('m', -6)),
        (('P', 1), -3, ('P', 1)),
        (('P', 1), 33, ('P', 1)),
        (('P', 8), -2, ('P', -15)),
    )
)
def test_mul_imperfect(
    n_edo, shorthand_name, scalar, result_shorthand_name
):
    """
    Test if scalar multiplication works for imperfect EDOs
    """

    interval = n_edo.shorthand_interval(*shorthand_name)
    result_interval = n_edo.shorthand_interval(*result_shorthand_name)

    assert interval * scalar == result_interval
    assert scalar * interval == result_interval


@pytest.mark.parametrize(
    'n_edo',
    IMPERFECT_EDOS
)
@pytest.mark.parametrize(
    'shorthand_name, sign',
    (
        (('P', 4), 1),
        (('A', 12), 1),
        (('M', 6), 1),
        (('P', 1), 0),
        (('dd', 12), 1),
        (('M', -10), -1),
        (('P', -12), -1),
    )
)
def test_sign_imperfect(
    n_edo, shorthand_name, sign
):
    """
    Test if sign property works for imperfect EDOs
    """

    interval = n_edo.shorthand_interval(*shorthand_name)
    assert interval.sign == sign


@pytest.mark.parametrize(
    'n_edo',
    IMPERFECT_EDOS
)
@pytest.mark.parametrize(
    'shorthand_name, is_simple',
    (
        (('M', 9), False),
        (('P', 12), False),
        (('M', 2), True),
        (('m', -2), True),
        (('A', 12), False),
        (('P', 8), True),
        (('P', -8), True),
        (('M', 13), False),
        (('d', -3), True),
        (('P', -12), False),
    )
)
def test_simple_compound_imperfect(
    n_edo, shorthand_name, is_simple
):
    """
    Test if is_simple and is_compound works for imperfect EDOs
    """

    if n_edo.edo_category == 'supersharp' or n_edo.eq_diff < 12:
        return  # they are too weird to test this, sorry

    interval = n_edo.shorthand_interval(*shorthand_name)
    assert interval.is_simple == is_simple
    assert interval.is_compound != is_simple


@pytest.mark.parametrize(
    'n_edo',
    IMPERFECT_EDOS
)
@pytest.mark.parametrize(
    'shorthand_name, result_shorthand_name',
    (
        (('P', 12), ('P', 5)),
        (('P', -12), ('P', -5)),
        (('M', 2), ('M', 2)),
        (('m', -2), ('m', -2)),
        (('A', -12), ('A', -5)),
        (('dd', 12), ('dd', 5)),
        (('P', 8), ('P', 8)),
        (('P', -8), ('P', -8)),
    )
)
def test_to_simple_imperfect(
    n_edo, shorthand_name, result_shorthand_name
):
    """
    Test if to_simple works for imperfect EDOs
    """

    if n_edo.edo_category == 'supersharp' or n_edo.eq_diff < 12:
        return  # they are too weird to test this, sorry

    interval = n_edo.shorthand_interval(*shorthand_name)
    result_interval = n_edo.shorthand_interval(*result_shorthand_name)

    assert interval.to_simple().is_notated_same(result_interval)


@pytest.mark.parametrize(
    'n_edo',
    IMPERFECT_EDOS
)
@pytest.mark.parametrize(
    'shorthand_name, result_shorthand_name',
    (
        (('P', 12), ('P', -5)),
        (('P', -12), ('P', 19)),
        (('M', 2), ('m', 7)),
        (('m', -2), ('m', 9)),
        (('A', 4), ('d', 5)),
        (('dd', 3), ('AA', 6)),
        (('P', 8), ('P', 1)),
        (('P', 1), ('P', 8)),
    )
)
def test_inversion_imperfect(
    n_edo, shorthand_name, result_shorthand_name
):
    """
    Test if inversion works for imperfect EDOs
    """

    if n_edo.edo_category == 'supersharp' or n_edo.eq_diff < 12:
        return  # they are too weird to test this, sorry

    interval = n_edo.shorthand_interval(*shorthand_name)
    result_interval = n_edo.shorthand_interval(*result_shorthand_name)

    assert interval.inversion().is_notated_same(result_interval)


@pytest.mark.parametrize(
    'n_edo',
    IMPERFECT_EDOS
)
@pytest.mark.parametrize(
    'shorthand_name, result_shorthand_name',
    (
        (('P', 12), ('P', 4)),
        (('P', -12), ('P', 4)),
        (('M', 2), ('M', 2)),
        (('m', -2), ('m', 2)),
        (('dd', 4), ('dd', 4)),
        (('P', 8), ('P', 1)),
        (('P', 1), ('P', 1)),
    )
)
def test_ic_normalized_ic_index_imperfect(
    n_edo, shorthand_name, result_shorthand_name
):
    """
    Test if ic normalization and ic_index works for imperfect EDOs
    """

    if n_edo.edo_category == 'supersharp' or n_edo.eq_diff < 12:
        return  # they are too weird to test this, sorry

    interval = n_edo.shorthand_interval(*shorthand_name)
    result_interval = n_edo.shorthand_interval(*result_shorthand_name)

    # we don't test on notational equality here, because there
    # are intervals (like A4 in 12-EDO) that have an inversion
    # with exactly the same pitch difference, so the result
    # depends on an implementation detail of which object is
    # chosen in the minimum function

    assert interval.ic_normalized() == result_interval
    assert interval.ic_index == result_interval.pitch_diff


@pytest.mark.parametrize(
    'n_edo',
    IMPERFECT_UPDOWN_EDOS
)
@pytest.mark.parametrize(
    'shorthand_name, result_shorthand_name',
    (
        (('^', 5), ('^', 5)),
        (('vv', -5), ('vv', 5)),
        (('vM', -6), ('vM', 6)),
        (('vv', 1), ('^^', 1)),
        (('^m', 3), ('^m', 3)),
        (('vvvm', -9), ('vvvm', 9)),
        (('vA', -15), ('vA', 15)),
        (('^dd', 12), ('^dd', 12)),
        (('^^dd', -12), ('^^dd', 12)),
    )
)
def test_abs_imperfect_updown(n_edo, shorthand_name, result_shorthand_name):
    """
    Test if abs works for imperfect EDOs with ups/downs
    """

    interval = n_edo.shorthand_interval(*shorthand_name)
    result_interval = n_edo.shorthand_interval(*result_shorthand_name)

    assert abs(interval) == result_interval


@pytest.mark.parametrize(
    'n_edo',
    IMPERFECT_UPDOWN_EDOS
)
@pytest.mark.parametrize(
    'shorthand_name, result_shorthand_name',
    (
        (('^', 5), ('^', -5)),
        (('vv', -5), ('vv', 5)),
        (('vM', -6), ('vM', 6)),
        (('vv', 1), ('^^', -1)),
        (('^m', 3), ('^m', -3)),
        (('vvvm', -9), ('vvvm', 9)),
        (('vA', -15), ('vA', 15)),
        (('^dd', 12), ('^dd', -12)),
        (('^^dd', -12), ('^^dd', 12)),
    )
)
def test_neg_imperfect_updown(n_edo, shorthand_name, result_shorthand_name):
    """
    Test if negation works for imperfect EDOs with ups/downs
    """

    interval = n_edo.shorthand_interval(*shorthand_name)
    result_interval = n_edo.shorthand_interval(*result_shorthand_name)

    assert -interval == result_interval
    assert interval == -result_interval


@pytest.mark.parametrize(
    'n_edo',
    IMPERFECT_UPDOWN_EDOS
)
@pytest.mark.parametrize(
    'shorthand_name_a, shorthand_name_b, result_shorthand_name',
    (
        (('^^d', 9), ('P', 1), ('^^d', 9)),
        (('vm', 3), ('vm', -3), ('P', 1)),
        (('vm', 3), ('vvM', 3), ('vvv', 5)),
        (('^A', 5), ('vM', 2), ('A', 6)),
        (('vvM', 3), ('^A', 2), ('vAA', 4)),
        (('^', 8), ('v', -12), ('vv', -5)),
    )
)
def test_add_imperfect_updown(
    n_edo, shorthand_name_a, shorthand_name_b, result_shorthand_name
):
    """
    Test if addition works for imperfect EDOs with ups/downs
    """

    interval_a = n_edo.shorthand_interval(*shorthand_name_a)
    interval_b = n_edo.shorthand_interval(*shorthand_name_b)
    result_interval = n_edo.shorthand_interval(*result_shorthand_name)

    assert interval_a + interval_b == result_interval
    assert (interval_a + interval_b).shorthand_name == result_shorthand_name
    assert interval_b + interval_a == result_interval
    assert (interval_b + interval_a).shorthand_name == result_shorthand_name


@pytest.mark.parametrize(
    'n_edo',
    IMPERFECT_UPDOWN_EDOS
)
@pytest.mark.parametrize(
    'shorthand_name_a, shorthand_name_b, result_shorthand_name',
    (
        (('^d', 9), ('P', 1), ('^d', 9)),
        (('vvm', 3), ('vm', -3), ('vvvd', 5)),
        (('m', 3), ('^M', 3), ('vd', 1)),
        (('P', 8), ('^m', 3), ('vM', 6)),
        (('^m', 3), ('^^', 5), ('^M', -3)),
        (('d', 3), ('v', 5), ('vA', -3)),
    )
)
def test_sub_imperfect_updown(
    n_edo, shorthand_name_a, shorthand_name_b, result_shorthand_name
):
    """
    Test if subtraction works for imperfect EDOs with ups/downs
    """

    interval_a = n_edo.shorthand_interval(*shorthand_name_a)
    interval_b = n_edo.shorthand_interval(*shorthand_name_b)
    result_interval = n_edo.shorthand_interval(*result_shorthand_name)

    assert interval_a - interval_b == result_interval
    assert (interval_a - interval_b).shorthand_name == result_shorthand_name
    assert -(interval_b - interval_a) == result_interval
    assert (-(interval_b - interval_a)).shorthand_name == result_shorthand_name


@pytest.mark.parametrize(
    'n_edo',
    IMPERFECT_UPDOWN_EDOS
)
@pytest.mark.parametrize(
    'shorthand_name, scalar, result_shorthand_name',
    (
        (('vv', 5), 2, ('vvvvM', 9)),
        (('^M', 3), 2, ('^^A', 5)),
        (('^m', 6), 1, ('^m', 6)),
        (('^^m', 6), 0, ('P', 1)),
        (('vvA', 7), 0, ('P', 1)),
        (('vm', 6), -1, ('vm', -6)),
        (('^', 1), -3, ('vvv', 1)),
        (('^m', 3), -2, ('^^d', -5)),
    )
)
def test_mul_imperfect_updown(
    n_edo, shorthand_name, scalar, result_shorthand_name
):
    """
    Test if scalar multiplication works for imperfect EDOs with ups/downs
    """

    interval = n_edo.shorthand_interval(*shorthand_name)
    result_interval = n_edo.shorthand_interval(*result_shorthand_name)

    assert interval * scalar == result_interval
    assert scalar * interval == result_interval


@pytest.mark.parametrize(
    'n_edo',
    IMPERFECT_UPDOWN_EDOS
)
@pytest.mark.parametrize(
    'shorthand_name, sign',
    (
        (('^', 5), 1),
        (('vv', -5), -1),
        (('vM', -6), -1),
        (('vv', 1), -1),
        (('^m', 3), 1),
        (('vvvm', -9), -1),
        (('vA', -15), -1),
        (('^dd', 12), 1),
    )
)
def test_sign_imperfect_updown(
    n_edo, shorthand_name, sign
):
    """
    Test if sign property works for imperfect EDOs with ups/downs
    """

    interval = n_edo.shorthand_interval(*shorthand_name)
    assert interval.sign == sign


@pytest.mark.parametrize(
    'n_edo',
    IMPERFECT_UPDOWN_EDOS
)
@pytest.mark.parametrize(
    'shorthand_name, is_simple',
    (
        (('M', 9), False),
        (('^^M', 9), False),
        (('vM', 9), False),
        (('P', 12), False),
        (('vv', 12), False),
        (('M', 2), True),
        (('^M', 2), True),
        (('m', -2), True),
        (('^m', -2), True),
        (('A', 12), False),
        (('vvA', 12), False),
        (('P', 8), True),
        (('v', -8), True),
        (('vvM', 13), False),
        (('d', -3), True),
        (('^d', -3), True),
        (('P', -12), False),
        (('vv', -12), False),
    )
)
def test_simple_compound_imperfect_updown(
    n_edo, shorthand_name, is_simple
):
    """
    Test if is_simple and is_compound works for imperfect EDOs
    with ups and downs
    """

    if n_edo.edo_category == 'supersharp' or n_edo.eq_diff < 12:
        return  # they are too weird to test this, sorry

    interval = n_edo.shorthand_interval(*shorthand_name)
    assert interval.is_simple == is_simple
    assert interval.is_compound != is_simple


@pytest.mark.parametrize(
    'n_edo',
    IMPERFECT_UPDOWN_EDOS
)
@pytest.mark.parametrize(
    'shorthand_name, result_shorthand_name',
    (
        (('P', 12), ('P', 5)),
        (('^', 12), ('^', 5)),
        (('P', -12), ('P', -5)),
        (('vv', -12), ('vv', -5)),
        (('M', 2), ('M', 2)),
        (('^^M', 2), ('^^M', 2)),
        (('m', -2), ('m', -2)),
        (('vm', -2), ('vm', -2)),
        (('A', -12), ('A', -5)),
        (('vvA', -12), ('vvA', -5)),
        (('dd', 12), ('dd', 5)),
        (('^dd', 12), ('^dd', 5)),
        (('P', 8), ('P', 8)),
        (('^', 8), ('^', 1)),
        (('^', -8), ('v', 1)),
    )
)
def test_to_simple_imperfect_updown(
    n_edo, shorthand_name, result_shorthand_name
):
    """
    Test if to_simple works for imperfect EDOs with ups/downs
    """

    if n_edo.edo_category == 'supersharp' or n_edo.eq_diff < 12:
        return  # they are too weird to test this, sorry

    interval = n_edo.shorthand_interval(*shorthand_name)
    result_interval = n_edo.shorthand_interval(*result_shorthand_name)

    assert interval.to_simple().is_notated_same(result_interval)


@pytest.mark.parametrize(
    'n_edo',
    IMPERFECT_UPDOWN_EDOS
)
@pytest.mark.parametrize(
    'shorthand_name, result_shorthand_name',
    (
        (('P', 12), ('P', -5)),
        (('v', 12), ('v', -5)),
        (('P', -12), ('P', 19)),
        (('vvv', -12), ('vvv', 19)),
        (('M', 2), ('m', 7)),
        (('vM', 2), ('^m', 7)),
        (('m', -2), ('m', 9)),
        (('A', 4), ('d', 5)),
        (('^A', 4), ('vd', 5)),
        (('dd', 3), ('AA', 6)),
        (('^^dd', 3), ('vvAA', 6)),
        (('P', 8), ('P', 1)),
        (('v', 8), ('^', 1)),
        (('v', 1), ('^', 8)),
    )
)
def test_inversion_imperfect_updown(
    n_edo, shorthand_name, result_shorthand_name
):
    """
    Test if inversion works for imperfect EDOs with ups/downs
    """

    if n_edo.edo_category == 'supersharp' or n_edo.eq_diff < 12:
        return  # they are too weird to test this, sorry

    interval = n_edo.shorthand_interval(*shorthand_name)
    result_interval = n_edo.shorthand_interval(*result_shorthand_name)

    assert interval.inversion().is_notated_same(result_interval)


@pytest.mark.parametrize(
    'n_edo',
    IMPERFECT_UPDOWN_EDOS
)
@pytest.mark.parametrize(
    'shorthand_name, result_shorthand_name',
    (
        (('P', 12), ('P', 4)),
        (('v', 12), ('^', 4)),
        (('P', -12), ('P', 4)),
        (('v', -12), ('^', 4)),
        (('M', 2), ('M', 2)),
        (('vM', 2), ('vM', 2)),
        (('m', -2), ('m', 2)),
        (('^^m', -2), ('^^m', 2)),
        (('dd', 4), ('dd', 4)),
        (('v', 8), ('^', 1)),
        (('vv', 1), ('^^', 1)),
    )
)
def test_ic_normalized_ic_index_imperfect_updown(
    n_edo, shorthand_name, result_shorthand_name
):
    """
    Test if ic normalization and ic_index works for imperfect EDOs
    with ups/downs
    """

    if n_edo.edo_category == 'supersharp' or n_edo.eq_diff < 12:
        return  # they are too weird to test this, sorry

    interval = n_edo.shorthand_interval(*shorthand_name)
    result_interval = n_edo.shorthand_interval(*result_shorthand_name)

    # we don't test on notational equality here, because there
    # are intervals (like A4 in 12-EDO) that have an inversion
    # with exactly the same pitch difference, so the result
    # depends on an implementation detail of which object is
    # chosen in the minimum function

    assert interval.ic_normalized() == result_interval
    assert interval.ic_index == result_interval.pitch_diff
