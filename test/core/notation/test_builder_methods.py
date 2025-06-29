import pytest
from xenharmlib import EDOTuning
from xenharmlib.exc import IncompatibleOriginContexts
from xenharmlib.exc import UnknownNoteSymbol
from ..utils import make_nat_acc_test_notation

edo12 = EDOTuning(12)
n_edo12 = make_nat_acc_test_notation(edo12)
edo24 = EDOTuning(24)
n_edo24 = make_nat_acc_test_notation(edo24)

# TODO: builder methods should also be
# properly unit tested


def test_note_interval_incompatible_origin_contexts():

    note_a = n_edo12.note('A', 0)
    note_b = n_edo12.note('B', 0)

    with pytest.raises(IncompatibleOriginContexts):
        with pytest.deprecated_call():
            n_edo24.note_interval(note_a, note_b)

    with pytest.raises(IncompatibleOriginContexts):
        n_edo24.interval(note_a, note_b)


def test_note_scale_incompatible_origin_contexts():

    note_a = n_edo12.note('A', 0)
    note_b = n_edo12.note('B', 0)
    note_c = n_edo24.note('B', 0)

    with pytest.raises(IncompatibleOriginContexts):
        with pytest.deprecated_call():
            n_edo12.note_scale(
                [note_a, note_b, note_c]
            )

    with pytest.raises(IncompatibleOriginContexts):
        n_edo12.scale(
            [note_a, note_b, note_c]
        )


def test_natural_scale():

    with pytest.deprecated_call():
        natural_scale = n_edo12.note_scale(
            [n_edo12.note(s, 0) for s in ['A', 'B', 'C', 'D', 'E', 'F']]
        )

    assert n_edo12.natural_scale().is_notated_same(natural_scale)

    natural_scale = n_edo12.scale(
        [n_edo12.note(s, 0) for s in ['A', 'B', 'C', 'D', 'E', 'F']]
    )

    assert n_edo12.natural_scale().is_notated_same(natural_scale)


@pytest.mark.parametrize(
    'notation, pc_symbols, expected_pairs',
    [
        (
            n_edo12,
            [],
            []
        ),
        (
            n_edo12,
            ['E'],
            [('E', 0)]
        ),
        (
            n_edo12,
            ['E', 'F+', 'A', 'C'],
            [('E', 0), ('F+', 0), ('A', 1), ('C', 1)]
        ),
        (
            n_edo12,
            ['C-', 'F+', 'A', 'C'],
            [('C-', 0), ('F+', 0), ('A', 1), ('C', 1)]
        ),
        (
            n_edo24,
            ['E', 'E', 'E', 'E'],
            [('E', 0), ('E', 1), ('E', 2), ('E', 3)]
        ),
        (
            n_edo24,
            ['A', 'B', 'C', 'E'],
            [('A', 0), ('B', 0), ('C', 0), ('E', 0)]
        ),
    ]
)
def test_pc_scale(notation, pc_symbols, expected_pairs):

    scale = notation.pc_scale(pc_symbols)
    expected = notation.scale(
        [notation.note(*pair) for pair in expected_pairs]
    )

    assert scale.is_notated_same(expected)


@pytest.mark.parametrize(
    'notation, pc_symbols, root_nat_bi_index, expected_pairs',
    [
        (
            n_edo12,
            ['E', 'F+', 'A', 'C'],
            2,
            [('E', 2), ('F+', 2), ('A', 3), ('C', 3)]
        ),
        (
            n_edo24,
            ['E', 'E', 'E', 'E'],
            5,
            [('E', 5), ('E', 6), ('E', 7), ('E', 8)]
        )
    ]
)
def test_pc_scale_root_nat_bi_index(
    notation, pc_symbols, root_nat_bi_index, expected_pairs
):

    scale = notation.pc_scale(pc_symbols, root_nat_bi_index)
    expected = notation.scale(
        [notation.note(*pair) for pair in expected_pairs]
    )

    assert scale.is_notated_same(expected)


@pytest.mark.parametrize(
    'notation, pc_symbols',
    [
        (
            n_edo12,
            ['X']
        ),
        (
            n_edo12,
            ['E', 'F+', 'X', 'C'],
        ),
        (
            n_edo24,
            ['E', 'E', 'E', 'X+']
        ),
    ]
)
def test_pc_scale_unknown_note_symbol(notation, pc_symbols):

    with pytest.raises(UnknownNoteSymbol):
        notation.pc_scale(pc_symbols)
