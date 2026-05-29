import pytest
from xenharmlib import EDOTuning
from xenharmlib.exc import IncompatibleOriginContexts
from xenharmlib.exc import InvalidGenerator
from xenharmlib.core.notes import NatAccNoteInterval
from ..utils import make_nat_acc_test_notation

edo12 = EDOTuning(12)
edo24 = EDOTuning(24)
edo31 = EDOTuning(31)

n_edo12 = make_nat_acc_test_notation(edo12)
n_edo24 = make_nat_acc_test_notation(edo24)
n_edo31 = make_nat_acc_test_notation(edo31)

@pytest.mark.parametrize(
    'notation, pc_symbol_a, nat_bi_index_a, pc_symbol_b, '
    'nat_bi_index_b, pitch_diff',
    [
        (n_edo12, 'Bx+', 0, 'F', 0, 5),
        (n_edo12, 'Bx+', 1, 'F', 0, -7),
        (n_edo12, 'Cx+', 1, 'Cx+', 1, 0),
        (n_edo31, 'D--', 0, 'Kx', 0, 18),
        (n_edo31, 'D--', 2, 'K+', 1, -14),
    ]
)
def test_note_interval_pitch_diff(
    notation,
    pc_symbol_a,
    nat_bi_index_a,
    pc_symbol_b,
    nat_bi_index_b,
    pitch_diff
):
    """
    Test if pitch difference is returned correctly
    """

    note_a = notation.note(pc_symbol_a, nat_bi_index_a)
    note_b = notation.note(pc_symbol_b, nat_bi_index_b)

    with pytest.deprecated_call():
        interval = notation.note_interval(note_a, note_b)
    assert interval.pitch_diff == pitch_diff

    interval = notation.interval(note_a, note_b)
    assert interval.pitch_diff == pitch_diff


@pytest.mark.parametrize(
    'notation, pc_symbol_a, nat_bi_index_a, pc_symbol_b, '
    'nat_bi_index_b, nat_diff',
    [
        (n_edo12, 'Bx+', 0, 'F', 0, 4),
        (n_edo12, 'Bx+', 1, 'F', 0, -2),
        (n_edo12, 'Cx+', 1, 'Cx+', 1, 0),
        (n_edo31, 'D--', 0, 'Kx', 0, 7),
        (n_edo31, 'D--', 2, 'K+', 1, -9),
    ]
)
def test_note_interval_nat_diff(
    notation,
    pc_symbol_a,
    nat_bi_index_a,
    pc_symbol_b,
    nat_bi_index_b,
    nat_diff
):
    """
    Test if natural difference is returned correctly
    """

    note_a = notation.note(pc_symbol_a, nat_bi_index_a)
    note_b = notation.note(pc_symbol_b, nat_bi_index_b)

    with pytest.deprecated_call():
        interval = notation.note_interval(note_a, note_b)
    assert interval.nat_diff == nat_diff

    interval = notation.interval(note_a, note_b)
    assert interval.nat_diff == nat_diff


@pytest.mark.parametrize(
    'notation, pc_symbol_a, nat_bi_index_a, pc_symbol_b, '
    'nat_bi_index_b, symbol',
    [
        (n_edo12, 'B+', 0, 'F', 0, '-F'),
        (n_edo12, 'Bx+', 1, 'F', 0, '+++F'),
        (n_edo12, 'Cx+', 1, 'Cx+', 1, 'F'),
        (n_edo12, 'Bx+', 1, 'Cx+', 1, 'C'),
        (n_edo31, 'D--', 0, 'K', 0, '++C'),
        (n_edo31, 'D-', 2, 'K', 1, '--C'),
    ]
)
def test_note_interval_symbol(
    notation,
    pc_symbol_a,
    nat_bi_index_a,
    pc_symbol_b,
    nat_bi_index_b,
    symbol
):
    """
    Test if interval symbol is returned correctly
    """

    note_a = notation.note(pc_symbol_a, nat_bi_index_a)
    note_b = notation.note(pc_symbol_b, nat_bi_index_b)

    with pytest.deprecated_call():
        interval = notation.note_interval(note_a, note_b)
    assert interval.symbol == symbol

    interval = notation.interval(note_a, note_b)
    assert interval.symbol == symbol


@pytest.mark.parametrize(
    'notation, pc_symbol_a, nat_bi_index_a, pc_symbol_b, '
    'nat_bi_index_b, number',
    [
        (n_edo12, 'B+', 0, 'F', 0, 5),
        (n_edo12, 'Bx+', 1, 'F', 0, -3),
        (n_edo12, 'Cx+', 1, 'Cx+', 1, 1),
        (n_edo12, 'Bx+', 1, 'Cx+', 1, 2),
        (n_edo31, 'D--', 0, 'K', 0, 8),
        (n_edo31, 'D-', 2, 'P', 1, -5),
    ]
)
def test_note_interval_number(
    notation,
    pc_symbol_a,
    nat_bi_index_a,
    pc_symbol_b,
    nat_bi_index_b,
    number
):
    """
    Test if interval number is returned correctly
    """

    note_a = notation.note(pc_symbol_a, nat_bi_index_a)
    note_b = notation.note(pc_symbol_b, nat_bi_index_b)

    with pytest.deprecated_call():
        interval = notation.note_interval(note_a, note_b)
    assert interval.number == number

    interval = notation.interval(note_a, note_b)
    assert interval.number == number


@pytest.mark.parametrize(
    'notation, pc_symbol_a, nat_bi_index_a, pc_symbol_b, '
    'nat_bi_index_b, shorthand_name',
    [
        (n_edo12, 'B+', 0, 'F', 0, ('-F', 5)),
        (n_edo12, 'Bx+', 1, 'F', 0, ('+++F', -3)),
        (n_edo12, 'Cx+', 1, 'Cx+', 1, ('F', 1)),
        (n_edo12, 'Bx+', 1, 'Cx+', 1, ('C', 2)),
        (n_edo31, 'D--', 0, 'K', 0, ('++C', 8)),
        (n_edo31, 'D-', 2, 'P', 1, ('--F', -5)),
    ]
)
def test_note_interval_shorthand(
    notation,
    pc_symbol_a,
    nat_bi_index_a,
    pc_symbol_b,
    nat_bi_index_b,
    shorthand_name
):
    """
    Test if shorthand names are generated correctly and that
    note intervals can be created from shorthand names
    """

    note_a = notation.note(pc_symbol_a, nat_bi_index_a)
    note_b = notation.note(pc_symbol_b, nat_bi_index_b)

    with pytest.deprecated_call():
        interval1 = notation.note_interval(note_a, note_b)
    assert interval1.shorthand_name == shorthand_name

    interval1 = notation.interval(note_a, note_b)
    assert interval1.shorthand_name == shorthand_name

    interval2 = notation.shorthand_interval(*shorthand_name)
    assert interval1 == interval2

    assert note_a.interval(note_b) == interval1
    assert note_a.interval(note_b) == interval2


@pytest.mark.parametrize(
    'notation_ab, pc_symbol_a, nat_bi_index_a, '
    'pc_symbol_b, nat_bi_index_b, '
    'notation_cd, pc_symbol_c, nat_bi_index_c, '
    'pc_symbol_d, nat_bi_index_d, ',
    [
        (n_edo12, 'B+',  0, 'F',   0, n_edo12, 'B', 3, 'F',  3),
        (n_edo12, 'Bx+', 1, 'F-',  0, n_edo12, 'B', 1, 'F',  0),
        (n_edo31, 'A',   0, 'B',   0, n_edo12, 'A', 0, 'B',  0),
        (n_edo12, 'B',   1, 'C',   1, n_edo12, 'B', 3, 'C+', 3),
        (n_edo31, 'D--', 0, 'K',   0, n_edo12, 'F', 3, 'F',  5),
    ]
)
def test_note_interval_lt(
    notation_ab,
    pc_symbol_a,
    nat_bi_index_a,
    pc_symbol_b,
    nat_bi_index_b,
    notation_cd,
    pc_symbol_c,
    nat_bi_index_c,
    pc_symbol_d,
    nat_bi_index_d,
):
    """
    Test if note intervals can be compared to one another using the
    greater-than and lesser-than relations and that greater-than
    and lesser-than imply inequality
    """

    note_a = notation_ab.note(pc_symbol_a, nat_bi_index_a)
    note_b = notation_ab.note(pc_symbol_b, nat_bi_index_b)
    interval_ab = note_a.interval(note_b)

    note_c = notation_cd.note(pc_symbol_c, nat_bi_index_c)
    note_d = notation_cd.note(pc_symbol_d, nat_bi_index_d)
    interval_cd = note_c.interval(note_d)

    assert interval_ab < interval_cd
    assert interval_cd > interval_ab
    assert interval_ab != interval_cd
    assert interval_cd != interval_ab


@pytest.mark.parametrize(
    'notation_ab, pc_symbol_a, nat_bi_index_a, '
    'pc_symbol_b, nat_bi_index_b, '
    'notation_cd, pc_symbol_c, nat_bi_index_c, '
    'pc_symbol_d, nat_bi_index_d, ',
    [
        (n_edo12, 'B+',  0, 'F',   0, n_edo12, 'B+',  0, 'F',  0),
        (n_edo12, 'Bx+', 1, 'F-',  0, n_edo12, 'Bx+', 1, 'F-', 0),
        (n_edo12, 'A',   0, 'B',   0, n_edo24, 'A',   0, 'C',  0),
    ]
)
def test_note_interval_eq(
    notation_ab,
    pc_symbol_a,
    nat_bi_index_a,
    pc_symbol_b,
    nat_bi_index_b,
    notation_cd,
    pc_symbol_c,
    nat_bi_index_c,
    pc_symbol_d,
    nat_bi_index_d,
):
    """
    Test if note intervals can be compared using the equality sign
    """

    note_a = notation_ab.note(pc_symbol_a, nat_bi_index_a)
    note_b = notation_ab.note(pc_symbol_b, nat_bi_index_b)
    interval_ab = note_a.interval(note_b)

    note_c = notation_cd.note(pc_symbol_c, nat_bi_index_c)
    note_d = notation_cd.note(pc_symbol_d, nat_bi_index_d)
    interval_cd = note_c.interval(note_d)

    assert interval_ab == interval_cd
    assert interval_cd == interval_ab


@pytest.mark.parametrize(
    'not_an_interval',
    ['abc', 1, 1.6, set(), dict()]
)
def test_note_interval_default_not_eq(not_an_interval):
    """
    Test if note intervals != unfitting objects
    """

    interval = n_edo12.note('B+', 0).interval(n_edo12.note('C', 2))
    assert interval != not_an_interval
    assert not_an_interval != interval


@pytest.mark.parametrize(
    'notation, pc_symbol_a, nat_bi_index_a, '
    'pc_symbol_b, nat_bi_index_b, '
    'tuning, pitch_index_a, pitch_index_b',
    [
        (n_edo12, 'B+',  0, 'F',   0, edo12, 12,  24),
        (n_edo12, 'Bx+', 1, 'F-',  0, edo12, 24, 20),
        (n_edo31, 'A',   0, 'B',   0, edo12, 0, 3),
        (n_edo12, 'B',   1, 'C',   1, edo12, 10, 15),
        (n_edo31, 'D--', 0, 'K',   0, edo12, 3, 18),
    ]
)
def test_note_interval_lt_pitch(
    notation,
    pc_symbol_a,
    nat_bi_index_a,
    pc_symbol_b,
    nat_bi_index_b,
    tuning,
    pitch_index_a,
    pitch_index_b,
):
    """
    Test if note intervals can be compared to pitch intervals using
    the greater-than and lesser-than relations and that greater-than
    and lesser-than imply inequality
    """

    note_a = notation.note(pc_symbol_a, nat_bi_index_a)
    note_b = notation.note(pc_symbol_b, nat_bi_index_b)
    interval_ab = note_a.interval(note_b)

    pitch_a = tuning.pitch(pitch_index_a)
    pitch_b = tuning.pitch(pitch_index_b)
    interval_cd = pitch_a.interval(pitch_b)

    assert interval_ab < interval_cd
    assert interval_ab != interval_cd
    assert interval_cd != interval_ab


@pytest.mark.parametrize(
    'notation, pc_symbol_a, nat_bi_index_a, '
    'pc_symbol_b, nat_bi_index_b, '
    'tuning, pitch_index_a, pitch_index_b',
    [
        (n_edo12, 'B+',  0, 'F',   0, edo12, 12, 19),
        (n_edo12, 'Bx+', 1, 'F-',  0, edo12, 24, 16),
        (n_edo31, 'A',   0, 'B',   0, edo31, 0, 2),
        (n_edo12, 'B',   1, 'C',   1, edo24, 10, 14),
        (n_edo31, 'D--', 0, 'K',   0, edo31, 3, 19),
    ]
)
def test_note_interval_eq_pitch(
    notation,
    pc_symbol_a,
    nat_bi_index_a,
    pc_symbol_b,
    nat_bi_index_b,
    tuning,
    pitch_index_a,
    pitch_index_b,
):
    """
    Test if note intervals can be compared to pitch intervals
    using the equality sign
    """

    note_a = notation.note(pc_symbol_a, nat_bi_index_a)
    note_b = notation.note(pc_symbol_b, nat_bi_index_b)
    interval_ab = note_a.interval(note_b)

    pitch_a = tuning.pitch(pitch_index_a)
    pitch_b = tuning.pitch(pitch_index_b)
    interval_cd = pitch_a.interval(pitch_b)

    assert interval_ab == interval_cd
    assert interval_cd == interval_ab


@pytest.mark.parametrize(
    'notation, pc_symbol_a, nat_bi_index_a, '
    'pc_symbol_b, nat_bi_index_b, ',
    [
        (n_edo12, 'B+',  0, 'F',  0),
        (n_edo12, 'Bx+', 0, 'F-', 2),
        (n_edo12, 'A',   0, 'B',  0),
    ]
)
def test_note_interval_eq_abs(
    notation,
    pc_symbol_a,
    nat_bi_index_a,
    pc_symbol_b,
    nat_bi_index_b,
):
    """
    Test if mirrored note intervals are equal under abs()
    """

    note_a = notation.note(pc_symbol_a, nat_bi_index_a)
    note_b = notation.note(pc_symbol_b, nat_bi_index_b)
    interval_ab = note_a.interval(note_b)
    interval_ba = note_b.interval(note_a)

    assert interval_ab != interval_ba
    assert abs(interval_ab) == abs(interval_ba)
    assert abs(interval_ba) == interval_ab


@pytest.mark.parametrize(
    'notation, pc_symbol_a, nat_bi_index_a, '
    'pc_symbol_b, nat_bi_index_b, ',
    [
        (n_edo12, 'B+',  0, 'F',  0),
        (n_edo12, 'Bx+', 0, 'F-', 2),
        (n_edo12, 'A',   0, 'B',  0),
    ]
)
def test_note_interval_neg(
    notation,
    pc_symbol_a,
    nat_bi_index_a,
    pc_symbol_b,
    nat_bi_index_b,
):
    """
    Test if negation works correctly
    """

    note_a = notation.note(pc_symbol_a, nat_bi_index_a)
    note_b = notation.note(pc_symbol_b, nat_bi_index_b)
    interval_ab = note_a.interval(note_b)
    interval_ba = note_b.interval(note_a)

    assert -interval_ab == interval_ba
    assert -interval_ba == interval_ab


@pytest.mark.parametrize(
    'notation, shorthand_name_a, shorthand_name_b, result_shorthand_name',
    [
        (n_edo12, ('+C', 4), ('F', 1), ('+C', 4)),
        (n_edo12, ('+C', 4), ('+C', -2), ('F', 3)),
        (n_edo12, ('+C', 4), ('++C', -2), ('-F', 3)),
        (n_edo12, ('F', 3), ('C', 4), ('C', 6)),
    ]
)
def test_note_interval_add(
    notation,
    shorthand_name_a,
    shorthand_name_b,
    result_shorthand_name,
):
    """
    Test if addition works correctly
    """

    interval_a = notation.shorthand_interval(*shorthand_name_a)
    interval_b = notation.shorthand_interval(*shorthand_name_b)
    result_interval = notation.shorthand_interval(*result_shorthand_name)

    assert interval_a + interval_b == result_interval
    assert interval_b + interval_a == result_interval
    assert (interval_b + interval_a).shorthand_name == result_shorthand_name
    assert (interval_a + interval_b).shorthand_name == result_shorthand_name


@pytest.mark.parametrize(
    'notation, shorthand_name_a, shorthand_name_b, result_shorthand_name',
    [
        (n_edo12, ('+C', 4), ('F', 1), ('+C', 4)),
        (n_edo12, ('+C', 4), ('+C', -2), ('++F', 5)),
        (n_edo12, ('+C', 4), ('+C', 2), ('F', 3)),
        (n_edo12, ('F', 13), ('C', 4), ('C', 10)),
        (n_edo12, ('C', 2), ('C', 4), ('F', -3)),
    ]
)
def test_note_interval_sub(
    notation,
    shorthand_name_a,
    shorthand_name_b,
    result_shorthand_name,
):
    """
    Test if subtraction works correctly
    """

    interval_a = notation.shorthand_interval(*shorthand_name_a)
    interval_b = notation.shorthand_interval(*shorthand_name_b)
    result_interval = notation.shorthand_interval(*result_shorthand_name)

    assert interval_a - interval_b == result_interval
    assert interval_b - interval_a == -result_interval
    assert (interval_a - interval_b).shorthand_name == result_shorthand_name
    assert (-(interval_b - interval_a)).shorthand_name == result_shorthand_name


@pytest.mark.parametrize(
    'notation, shorthand_name, scalar, result_shorthand_name',
    [
        (n_edo12, ('+C', 4), 0, ('F', 1)),
        (n_edo12, ('+C', 4), -2, ('++F', -7)),
        (n_edo12, ('-F', 3), 3, ('---F', 7)),
        (n_edo12, ('F', 1), 3, ('F', 1)),
    ]
)
def test_note_interval_mul(
    notation,
    shorthand_name,
    scalar,
    result_shorthand_name,
):
    """
    Test if subtraction works correctly
    """

    interval = notation.shorthand_interval(*shorthand_name)
    result_interval = notation.shorthand_interval(*result_shorthand_name)

    assert interval * scalar == result_interval
    assert scalar * interval == result_interval
    assert (interval * scalar).shorthand_name == result_shorthand_name
    assert (scalar * interval).shorthand_name == result_shorthand_name


@pytest.mark.parametrize(
    'notation, shorthand_name, sign',
    [
        (n_edo12, ('+C', 4), 1),
        (n_edo12, ('+C', 4), 1),
        (n_edo12, ('-F', -3), -1),
        (n_edo12, ('F', 1), 0),
    ]
)
def test_note_interval_sign(
    notation,
    shorthand_name,
    sign,
):
    """
    Test if sign property works correctly
    """

    interval = notation.shorthand_interval(*shorthand_name)
    assert interval.sign == sign


@pytest.mark.parametrize(
    'notation, pc_symbol_a, nat_bi_index_a, '
    'pc_symbol_b, nat_bi_index_b, '
    'tuning, pitch_index_a, pitch_index_b',
    [
        (n_edo12, 'B+',  0, 'F',   0, edo12, 19, 12),
        (n_edo12, 'Bx+', 1, 'F-',  0, edo12, 16, 24),
        (n_edo31, 'A',   0, 'B',   0, edo31, 2, 0),
        (n_edo12, 'B',   1, 'C',   1, edo24, 14, 10),
        (n_edo31, 'D--', 0, 'K',   0, edo31, 19, 3),
    ]
)
def test_note_interval_eq_pitch_abs(
    notation,
    pc_symbol_a,
    nat_bi_index_a,
    pc_symbol_b,
    nat_bi_index_b,
    tuning,
    pitch_index_a,
    pitch_index_b,
):
    """
    Test if note intervals are equal under abs() with their
    mirrored pitch intervals
    """

    note_a = notation.note(pc_symbol_a, nat_bi_index_a)
    note_b = notation.note(pc_symbol_b, nat_bi_index_b)
    interval_ab = note_a.interval(note_b)

    pitch_a = tuning.pitch(pitch_index_a)
    pitch_b = tuning.pitch(pitch_index_b)
    interval_cd = pitch_a.interval(pitch_b)

    assert abs(interval_ab) == abs(interval_cd)
    assert abs(interval_cd) == abs(interval_ab)


@pytest.mark.parametrize(
    'notation, pc_symbol_a, nat_bi_index_a, '
    'pc_symbol_b, nat_bi_index_b, '
    'gen_pc_symbol, gen_nat_bi_index, gen_dist',
    [
        (n_edo12, 'B+',  0, 'F',   0, 'D+', 0, 1),
        (n_edo12, 'B+',  1, 'F',   0, 'D+', 0, 1),
        (n_edo12, 'A',   0, 'B',   2, 'D+', 0, 2),
        (n_edo12, 'A',   1, 'C',   1, 'D+', 0, 4),
        (n_edo31, 'D--', 0, 'K',   0, 'C+', 0, 3),
    ]
)
def test_note_interval_get_generator_distance(
    notation,
    pc_symbol_a,
    nat_bi_index_a,
    pc_symbol_b,
    nat_bi_index_b,
    gen_pc_symbol,
    gen_nat_bi_index,
    gen_dist
):
    """
    Test if get_generator_distance works correctly
    """

    note_a = notation.note(pc_symbol_a, nat_bi_index_a)
    note_b = notation.note(pc_symbol_b, nat_bi_index_b)
    interval_ab = note_a.interval(note_b)

    assert interval_ab.get_generator_distance(
        notation.note(gen_pc_symbol, gen_nat_bi_index)
    ) == gen_dist


@pytest.mark.parametrize(
    'notation, pc_symbol_a, nat_bi_index_a, '
    'pc_symbol_b, nat_bi_index_b, '
    'gen_pc_symbol, gen_nat_bi_index',
    [
        (n_edo12, 'B+',  0, 'F',   0, 'B', 0),
        (n_edo12, 'B+',  1, 'F',   0, 'D', 0),
        (n_edo12, 'A',   0, 'B',   2, 'B+', 0),
    ]
)
def test_note_interval_get_generator_distance_invalid_generator(
    notation,
    pc_symbol_a,
    nat_bi_index_a,
    pc_symbol_b,
    nat_bi_index_b,
    gen_pc_symbol,
    gen_nat_bi_index
):
    """
    Test if get_generator_distance fails if generator note
    is not in fact a generator
    """

    note_a = notation.note(pc_symbol_a, nat_bi_index_a)
    note_b = notation.note(pc_symbol_b, nat_bi_index_b)
    interval_ab = note_a.interval(note_b)

    with pytest.raises(InvalidGenerator):
        interval_ab.get_generator_distance(
            notation.note(gen_pc_symbol, gen_nat_bi_index)
        )


def test_get_generator_distance_incompatible_origin_contexts():
    """
    Test if get_generator_distance fails if interval and generator
    note are from different notations
    """

    interval = n_edo12.note('A', 3).interval(
        n_edo12.note('F', 0)
    )
    gen_note = n_edo31.note('A', 0)

    with pytest.raises(IncompatibleOriginContexts):
        interval.get_generator_distance(gen_note)


@pytest.mark.parametrize(
    'notation, '
    'pc_symbol_a, nat_bi_index_a, '
    'pc_symbol_b, nat_bi_index_b, '
    'expected',
    [
        (n_edo12, 'B',    0, 'E', 2, 'MyNatAccNoteInterval(C, 16, 12-EDO)'),
        (n_edo12, 'Bx',   1, 'E', 2, 'MyNatAccNoteInterval(--C, 10, 12-EDO)'),
        (n_edo12, 'B++',  3, 'E', 2, 'MyNatAccNoteInterval(++C, -4, 12-EDO)'),
        (n_edo31, 'C-',   2, 'E', 2, 'MyNatAccNoteInterval(+F, 3, 31-EDO)'),
        (n_edo31, 'C--',  1, 'E', 2, 'MyNatAccNoteInterval(++F, 19, 31-EDO)'),
        (n_edo12, 'A--', -1, 'E', 2, 'MyNatAccNoteInterval(++F, 23, 12-EDO)'),
    ]
)
def test_note_repr(
    notation,
    pc_symbol_a,
    nat_bi_index_a,
    pc_symbol_b,
    nat_bi_index_b,
    expected
):
    """
    Test if repr() of note intervals works correctly
    """

    note_a = notation.note(pc_symbol_a, nat_bi_index_a)
    note_b = notation.note(pc_symbol_b, nat_bi_index_b)
    interval = note_a.interval(note_b)

    assert repr(interval) == expected


def test_from_notes_incompatible_origin_contexts():
    """
    Test if from_notes method raises correct error
    when notes are from different notations
    """

    note_a = n_edo12.note('A', 0)
    note_b = n_edo24.note('B', 1)

    with pytest.raises(IncompatibleOriginContexts):
        with pytest.deprecated_call():
            NatAccNoteInterval.from_notes(note_a, note_b)
