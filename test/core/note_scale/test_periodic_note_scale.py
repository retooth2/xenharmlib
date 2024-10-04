import pytest
from xenharmlib import EDOTuning
from xenharmlib import EDTuning
from xenharmlib import FrequencyRatio
from xenharmlib.core.note_scale import PeriodicNoteScale
from xenharmlib.exc import IncompatibleOriginContexts
from ..utils import make_nat_acc_test_notation

edo12 = EDOTuning(12)
n_edo12 = make_nat_acc_test_notation(edo12)
edo24 = EDOTuning(24)
n_edo24 = make_nat_acc_test_notation(edo24)
edo31 = EDOTuning(31)
n_edo31 = make_nat_acc_test_notation(edo31)
ed13_3 = EDTuning(13, FrequencyRatio(3))
n_ed13_3 = make_nat_acc_test_notation(ed13_3)


@pytest.mark.parametrize(
    'notation, input_pairs, result_pci',
    [
        (
            n_edo12,
            [('E', 1), ('B+', 5), ('D+', 0)],
            [7, 8, 3]
        ),
        (
            n_edo12,
            [('A', 2), ('B+', 0), ('C', 1)],
            [3, 4, 0]
        ),
        (
            n_edo24,
            [('A', 1), ('B+', 1), ('C', 1)],
            [0, 3, 4]
        ),
    ]
)
def test_pc_indices(notation, input_pairs, result_pci):
    """
    Test if pc_indices property is correct
    """
 
    scale = PeriodicNoteScale(
        notation, 
        [notation.note(*pair) for pair in input_pairs]
    )
 
    assert scale.pc_indices == result_pci


@pytest.mark.parametrize(
    'notation, input_pairs, result_pairs',
    [
        (
            n_edo12,
            [('A+', 0), ('B+', 0), ('D+', 0)],
            [('B+', 0), ('D+', 0), ('A+', 1)],
        ),
        (
            n_edo12,
            [('A+', 0), ('B+', 0), ('B-', 1)],
            [('B+', 0), ('B-', 1), ('A+', 2)],
        ),
        (
            n_edo24,
            [('A+', 0), ('B+', 1), ('C', 1)],
            [('B+', 1), ('C', 1), ('A+', 2)],
        ),
    ]
)
def test_rotated_up(notation, input_pairs, result_pairs):
    """
    Test if rotated_up operation works correctly
    """

    scale = PeriodicNoteScale(
        notation, 
        [notation.note(*pair) for pair in input_pairs]
    )

    rot_scale = scale.rotated_up()

    notes = list(rot_scale)
    assert notes == [notation.note(*pair) for pair in result_pairs]


@pytest.mark.parametrize(
    'notation, input_pairs, result_pairs',
    [
        (
            n_edo12,
            [('B+', 0), ('D+', 0), ('A+', 1)],
            [('A+', 0), ('B+', 0), ('D+', 0)],
        ),
        (
            n_edo12,
            [('B-', 0), ('A', 1), ('A+', 1)],
            [('A+', -1), ('B-', 0), ('A', 1)],
        ),
        (
            n_edo24,
            [('B+', 1), ('C', 1), ('D', 2)],
            [('D', 0), ('B+', 1), ('C', 1)],
        ),
    ]
)
def test_rotated_down(notation, input_pairs, result_pairs):
    """
    Test if rotated_up operation works correctly
    """

    scale = PeriodicNoteScale(
        notation, 
        [notation.note(*pair) for pair in input_pairs]
    )

    rot_scale = scale.rotated_down()

    notes = list(rot_scale)
    assert notes == [notation.note(*pair) for pair in result_pairs]


@pytest.mark.parametrize(
    'notation, input_pairs, order, result_pairs',
    [
        (
            n_edo12,
            [('A+', 0), ('B+', 0), ('D+', 0)],
            2,
            [('D+', 0), ('A+', 1), ('B+', 1)],
        ),
        (
            n_edo24,
            [('A+', 0), ('B+', 1), ('C', 1)],
            2,
            [('C', 1), ('A+', 2), ('B+', 2)],
        ),
        (
            n_edo12,
            [('A+', 0), ('B+', 0), ('D+', 0)],
            1,
            [('B+', 0), ('D+', 0), ('A+', 1)],
        ),
        (
            n_edo24,
            [('A+', 0), ('B+', 1), ('C', 1)],
            1,
            [('B+', 1), ('C', 1), ('A+', 2)],
        ),
        (
            n_edo31,
            [('A+', 0), ('B+', 1), ('C', 1)],
            0,
            [('A+', 0), ('B+', 1), ('C', 1)],
        ),
        (
            n_edo12,
            [('B+', 0), ('D+', 0), ('A+', 1)],
            -1,
            [('A+', 0), ('B+', 0), ('D+', 0)],
        ),
        (
            n_edo24,
            [('B+', 1), ('C', 1), ('D', 2)],
            -1,
            [('D', 0), ('B+', 1), ('C', 1)],
        ),
        (
            n_edo12,
            [('B+', 0), ('D+', 0), ('A+', 1)],
            -2,
            [('D+', -1), ('A+', 0), ('B+', 0)],
        ),
        (
            n_edo24,
            [('B+', 1), ('C', 1), ('D', 2)],
            -2,
            [('C', 0), ('D', 0), ('B+', 1)],
        ),
    ]
)
def test_rotation(notation, input_pairs, order, result_pairs):
    """
    Test if rotated_up operation works correctly
    """

    scale = PeriodicNoteScale(
        notation, 
        [notation.note(*pair) for pair in input_pairs]
    )

    rot_scale = scale.rotation(order)

    notes = list(rot_scale)
    assert notes == [notation.note(*pair) for pair in result_pairs]


@pytest.mark.parametrize(
    'notation, input_pairs_a, input_pairs_b, result_pairs',
    [
        (
            n_edo12,
            [('A+', 0), ('B+', 0), ('D+', 0)],
            [('A+', 0), ('C', 0), ('D+', 0)],
            [('A+', 0), ('B+', 0), ('C', 0), ('D+', 0)],
        ),
        (
            n_edo12,
            [('A+', 0), ('B+', 1), ('F', 2)],
            [('A+', 0), ('B+', 1), ('F', 2)],
            [('A+', 0), ('B+', 1), ('F', 2)],
        ),
        (
            n_edo24,
            [('A+', 0), ('B+', 1), ('F+', 2)],
            [('A', 0), ('B', 0), ('F', 2)],
            [('A', 0), ('A+', 0), ('B', 0), ('B+', 1), ('F', 2), ('F+', 2)],
        ),
        (
            n_edo24,
            [('A+', 0), ('B+', 1), ('F', 2)],
            [],
            [('A+', 0), ('B+', 1), ('F', 2)],
        ),
    ]
)
def test_union(notation, input_pairs_a, input_pairs_b, result_pairs):
    """
    Test if union operation works correctly
    """

    scale_a = PeriodicNoteScale(
        notation, 
        [notation.note(*pair) for pair in input_pairs_a]
    )

    scale_b = PeriodicNoteScale(
        notation, 
        [notation.note(*pair) for pair in input_pairs_b]
    )

    scale_c = scale_a.union(scale_b)
    assert len(scale_c) == len(result_pairs)
    notes = list(scale_c)
    assert notes == [notation.note(*pair) for pair in result_pairs]

    scale_c = scale_a | scale_b
    assert len(scale_c) == len(result_pairs)
    notes = list(scale_c)
    assert notes == [notation.note(*pair) for pair in result_pairs]


def test_union_incompatible_origin_contexts():
    """
    Test if union operation fails if scales originate from
    different notations
    """

    n_edo12_2 = make_nat_acc_test_notation(edo12)
    notations = n_edo12, n_edo24, n_edo31, n_edo12_2

    for i, notation_a in enumerate(notations):

        for notation_b in notations[i+1:]:

            scale_a = PeriodicNoteScale(
                notation_a
            )
            scale_b = PeriodicNoteScale(
                notation_b
            )

            with pytest.raises(IncompatibleOriginContexts):
                scale_a.union(scale_b)


@pytest.mark.parametrize(
    'notation, input_pairs_a, input_pairs_b, result_pairs',
    [
        (
            n_edo12,
            [('A+', 0), ('B+', 0), ('D+', 0)],
            [('A+', 0), ('C', 0), ('D+', 0)],
            [('A+', 0), ('D+', 0)],
        ),
        (
            n_edo12,
            [('A+', 0), ('B+', 0), ('D+', 0)],
            [('A+', 0), ('C', 0), ('E-', 0)],
            [('A+', 0), ('D+', 0)],
        ),
        (
            n_edo12,
            [('A+', 0), ('B+', 1), ('F', 2)],
            [('A+', 0), ('C-', 1), ('Ex', 2)],
            [('A+', 0), ('B+', 1), ('F', 2)],
        ),
        (
            n_edo24,
            [('A+', 0), ('B+', 1), ('F+', 2)],
            [('A', 0), ('B', 0), ('F', 2)],
            [],
        ),
        (
            n_edo24,
            [('A+', 0), ('B+', 1), ('F', 2)],
            [],
            [],
        ),
    ]
)
def test_intersection(notation, input_pairs_a, input_pairs_b, result_pairs):
    """
    Test if intersection operation works correctly
    """

    scale_a = PeriodicNoteScale(
        notation, 
        [notation.note(*pair) for pair in input_pairs_a]
    )

    scale_b = PeriodicNoteScale(
        notation, 
        [notation.note(*pair) for pair in input_pairs_b]
    )

    scale_c = scale_a.intersection(scale_b)
    assert len(scale_c) == len(result_pairs)
    notes = list(scale_c)
    assert notes == [notation.note(*pair) for pair in result_pairs]

    scale_c = scale_a & scale_b
    assert len(scale_c) == len(result_pairs)
    notes = list(scale_c)
    assert notes == [notation.note(*pair) for pair in result_pairs]


@pytest.mark.parametrize(
    'notation, input_pairs_a, input_pairs_b, result_pairs',
    [
        (
            n_edo12,
            [('A+', 0), ('B+', 0), ('D+', 0)],
            [('A+', 0), ('C', 0), ('D+', 0)],
            [('A+', 0), ('D+', 0)],
        ),
        (
            n_edo12,
            [('A+', 0), ('B+', 0), ('D+', 0)],
            [('A+', 0), ('C', 0), ('E-', 0)],
            [('A+', 0)],
        ),
        (
            n_edo12,
            [('A+', 0), ('B+', 1), ('F', 2)],
            [('A+', 0), ('C-', 1), ('Ex', 2)],
            [('A+', 0)],
        ),
        (
            n_edo24,
            [('A+', 0), ('B+', 1), ('F+', 2)],
            [('A', 0), ('B', 0), ('F', 2)],
            [],
        ),
        (
            n_edo24,
            [('A+', 0), ('B+', 1), ('F', 2)],
            [],
            [],
        ),
    ]
)
def test_note_intersection(
    notation,
    input_pairs_a,
    input_pairs_b,
    result_pairs
):
    """
    Test if note_intersection operation works correctly
    """

    scale_a = PeriodicNoteScale(
        notation,
        [notation.note(*pair) for pair in input_pairs_a]
    )

    scale_b = PeriodicNoteScale(
        notation,
        [notation.note(*pair) for pair in input_pairs_b]
    )

    scale_c = scale_a.note_intersection(scale_b)

    assert len(scale_c) == len(result_pairs)
    notes = list(scale_c)
    assert notes == [notation.note(*pair) for pair in result_pairs]


@pytest.mark.parametrize(
    'notation, input_pairs_a, input_pairs_b, result_pairs',
    [
        (
            n_edo12,
            [('A+', 0), ('B+', 0), ('D+', 1)],
            [('A+', 0), ('C', 0), ('D+', 0)],
            [('A+', 0), ('D+', 0), ('D+', 1)],
        ),
        (
            n_edo12,
            [('A+', 0), ('B+', 0), ('D+', 0)],
            [('A+', 0), ('C', 0), ('E-', 1)],
            [('A+', 0), ('D+', 0), ('E-', 1)],
        ),
        (
            n_edo12,
            [('A+', 0), ('B+', 1), ('F', 2)],
            [('A+', 1), ('C-', 2), ('Ex', 3)],
            [('A+', 0), ('A+', 1), ('B+', 1), ('C-', 2), ('F', 2), ('Ex', 3)],
        ),
        (
            n_edo24,
            [('A+', 0), ('B+', 1), ('F+', 2)],
            [('A', 0), ('B', 0), ('F', 2)],
            [],
        ),
        (
            n_edo24,
            [('A+', 0), ('B+', 1), ('F', 2)],
            [],
            [],
        ),
    ]
)
def test_intersection_ignore_bi_index(
    notation,
    input_pairs_a,
    input_pairs_b,
    result_pairs
):
    """
    Test if intersection operation works correctly
    on ignore_bi_index=True
    """

    scale_a = PeriodicNoteScale(
        notation, 
        [notation.note(*pair) for pair in input_pairs_a]
    )

    scale_b = PeriodicNoteScale(
        notation, 
        [notation.note(*pair) for pair in input_pairs_b]
    )

    scale_c = scale_a.intersection(scale_b, ignore_bi_index=True)

    assert len(scale_c) == len(result_pairs)
    notes = list(scale_c)
    assert notes == [notation.note(*pair) for pair in result_pairs]


@pytest.mark.parametrize(
    'notation, input_pairs_a, input_pairs_b, result_pairs',
    [
        (
            n_edo12,
            [('A+', 0), ('B+', 0), ('D+', 1)],
            [('A+', 0), ('C', 0), ('D+', 0)],
            [('A+', 0), ('D+', 0), ('D+', 1)],
        ),
        (
            n_edo12,
            [('A+', 0), ('B+', 0), ('D+', 0)],
            [('A+', 0), ('C', 0), ('E-', 0)],
            [('A+', 0)],
        ),
        (
            n_edo12,
            [('A+', 0), ('B+', 1), ('F', 2)],
            [('A+', 2), ('C-', 1), ('Ex', 2)],
            [('A+', 0), ('A+', 2)],
        ),
        (
            n_edo24,
            [('A+', 0), ('B+', 1), ('F+', 2)],
            [('A', 0), ('B', 0), ('F', 2)],
            [],
        ),
        (
            n_edo24,
            [('A+', 0), ('B+', 1), ('F', 2)],
            [],
            [],
        ),
    ]
)
def test_note_intersection_ignore_bi_index(
    notation,
    input_pairs_a,
    input_pairs_b,
    result_pairs
):
    """
    Test if note_intersection operation works correctly
    on ignore_bi_index=True
    """

    scale_a = PeriodicNoteScale(
        notation, 
        [notation.note(*pair) for pair in input_pairs_a]
    )

    scale_b = PeriodicNoteScale(
        notation, 
        [notation.note(*pair) for pair in input_pairs_b]
    )

    scale_c = scale_a.note_intersection(
        scale_b,
        ignore_bi_index=True
    )

    assert len(scale_c) == len(result_pairs)
    notes = list(scale_c)
    assert notes == [notation.note(*pair) for pair in result_pairs]


def test_intersection_incompatible_origin_contexts():
    """
    Test if intersection operation fails if scales originate from
    different notations
    """

    n_edo12_2 = make_nat_acc_test_notation(edo12)
    notations = n_edo12, n_edo24, n_edo31, n_edo12_2

    for i, notation_a in enumerate(notations):

        for notation_b in notations[i+1:]:

            scale_a = PeriodicNoteScale(
                notation_a
            )
            scale_b = PeriodicNoteScale(
                notation_b
            )

            with pytest.raises(IncompatibleOriginContexts):
                scale_a.intersection(scale_b)

            with pytest.raises(IncompatibleOriginContexts):
                scale_a & scale_b


def test_note_intersection_incompatible_origin_contexts():
    """
    Test if note_intersection operation fails if scales originate from
    different notations
    """

    n_edo12_2 = make_nat_acc_test_notation(edo12)
    notations = n_edo12, n_edo24, n_edo31, n_edo12_2

    for i, notation_a in enumerate(notations):

        for notation_b in notations[i+1:]:

            scale_a = PeriodicNoteScale(
                notation_a
            )
            scale_b = PeriodicNoteScale(
                notation_b
            )

            with pytest.raises(IncompatibleOriginContexts):
                scale_a.note_intersection(scale_b)


@pytest.mark.parametrize(
    'notation, input_pairs_a, input_pairs_b, result_pairs',
    [
        (
            n_edo12,
            [('A+', 0), ('B+', 0), ('D+', 0)],
            [('A+', 0), ('C', 0), ('D+', 0)],
            [('B+', 0)],
        ),
        (
            n_edo12,
            [('A+', 0), ('B+', 0), ('D+', 0)],
            [('A+', 0), ('C', 0), ('E-', 0)],
            [('B+', 0)],
        ),
        (
            n_edo12,
            [('A+', 0), ('B+', 1), ('F', 2)],
            [('A+', 0), ('C-', 1), ('Ex', 2)],
            [],
        ),
        (
            n_edo24,
            [('A+', 0), ('B+', 1), ('F+', 2)],
            [('A', 0), ('B', 0), ('F', 2)],
            [('A+', 0), ('B+', 1), ('F+', 2)],
        ),
        (
            n_edo24,
            [('A+', 0), ('B+', 1), ('F', 2)],
            [],
            [('A+', 0), ('B+', 1), ('F', 2)],
        ),
    ]
)
def test_difference(notation, input_pairs_a, input_pairs_b, result_pairs):
    """
    Test if difference operation works correctly
    """

    scale_a = PeriodicNoteScale(
        notation, 
        [notation.note(*pair) for pair in input_pairs_a]
    )

    scale_b = PeriodicNoteScale(
        notation, 
        [notation.note(*pair) for pair in input_pairs_b]
    )

    scale_c = scale_a.difference(scale_b)
    assert len(scale_c) == len(result_pairs)
    notes = list(scale_c)
    assert notes == [notation.note(*pair) for pair in result_pairs]

    scale_c = scale_a - scale_b
    assert len(scale_c) == len(result_pairs)
    notes = list(scale_c)
    assert notes == [notation.note(*pair) for pair in result_pairs]


@pytest.mark.parametrize(
    'notation, input_pairs_a, input_pairs_b, result_pairs',
    [
        (
            n_edo12,
            [('A+', 0), ('B+', 0), ('D+', 0)],
            [('A+', 0), ('C', 0), ('D+', 1)],
            [('B+', 0)],
        ),
        (
            n_edo12,
            [('A+', 0), ('B+', 0), ('D+', 0)],
            [('A+', 2), ('C', 0), ('E-', 1)],
            [('B+', 0)],
        ),
        (
            n_edo12,
            [('A+', 0), ('B+', 1), ('F', 2)],
            [('A+', 0), ('C-', 1), ('Ex', 2)],
            [],
        ),
        (
            n_edo24,
            [('A+', 0), ('B+', 1), ('F+', 2)],
            [('A', 0), ('B', 0), ('F', 2)],
            [('A+', 0), ('B+', 1), ('F+', 2)],
        ),
        (
            n_edo24,
            [('A+', 0), ('B+', 1), ('F', 2)],
            [],
            [('A+', 0), ('B+', 1), ('F', 2)],
        ),
    ]
)
def test_difference_ignore_bi_index(notation, input_pairs_a, input_pairs_b, result_pairs):
    """
    Test if difference operation works correctly
    on ignore_bi_index=True
    """

    scale_a = PeriodicNoteScale(
        notation, 
        [notation.note(*pair) for pair in input_pairs_a]
    )

    scale_b = PeriodicNoteScale(
        notation, 
        [notation.note(*pair) for pair in input_pairs_b]
    )

    scale_c = scale_a.difference(
        scale_b, ignore_bi_index=True
    )

    assert len(scale_c) == len(result_pairs)
    notes = list(scale_c)
    assert notes == [notation.note(*pair) for pair in result_pairs]


@pytest.mark.parametrize(
    'notation, input_pairs_a, input_pairs_b, result_pairs',
    [
        (
            n_edo12,
            [('A+', 0), ('B+', 0), ('D+', 0)],
            [('A+', 0), ('C', 0), ('D+', 0)],
            [('B+', 0)],
        ),
        (
            n_edo12,
            [('A+', 0), ('B+', 0), ('D+', 0)],
            [('A+', 0), ('C', 0), ('E-', 0)],
            [('B+', 0), ('D+', 0)],
        ),
        (
            n_edo12,
            [('A+', 0), ('B+', 1), ('F', 2)],
            [('A+', 0), ('C-', 1), ('Ex', 2)],
            [('B+', 1), ('F', 2)],
        ),
        (
            n_edo24,
            [('A+', 0), ('B+', 1), ('F+', 2)],
            [('A', 0), ('B', 0), ('F', 2)],
            [('A+', 0), ('B+', 1), ('F+', 2)],
        ),
        (
            n_edo24,
            [('A+', 0), ('B+', 1), ('F', 2)],
            [],
            [('A+', 0), ('B+', 1), ('F', 2)],
        ),
    ]
)
def test_note_difference(notation, input_pairs_a, input_pairs_b, result_pairs):
    """
    Test if note_difference operation works correctly
    """

    scale_a = PeriodicNoteScale(
        notation,
        [notation.note(*pair) for pair in input_pairs_a]
    )

    scale_b = PeriodicNoteScale(
        notation,
        [notation.note(*pair) for pair in input_pairs_b]
    )

    scale_c = scale_a.note_difference(scale_b)

    assert len(scale_c) == len(result_pairs)
    notes = list(scale_c)
    assert notes == [notation.note(*pair) for pair in result_pairs]


@pytest.mark.parametrize(
    'notation, input_pairs_a, input_pairs_b, result_pairs',
    [
        (
            n_edo12,
            [('A+', 0), ('B+', 0), ('D+', 0)],
            [('A+', 1), ('C', 0), ('D+', 1)],
            [('B+', 0)],
        ),
        (
            n_edo12,
            [('A+', 0), ('B+', 0), ('D+', 0)],
            [('A+', 1), ('C', 0), ('E-', 0)],
            [('B+', 0), ('D+', 0)],
        ),
        (
            n_edo12,
            [('A+', 2), ('B+', 1), ('F', 2)],
            [('A+', 0), ('C-', 1), ('Ex', 3)],
            [('B+', 1), ('F', 2)],
        ),
        (
            n_edo24,
            [('A+', 0), ('B+', 1), ('F+', 2)],
            [('A', 0), ('B', 0), ('F', 2)],
            [('A+', 0), ('B+', 1), ('F+', 2)],
        ),
        (
            n_edo24,
            [('A+', 0), ('B+', 1), ('F', 2)],
            [],
            [('A+', 0), ('B+', 1), ('F', 2)],
        ),
    ]
)
def test_note_difference_ignore_bi_index(
    notation,
    input_pairs_a,
    input_pairs_b,
    result_pairs
):
    """
    Test if difference operation works correctly
    on ignore_bi_index=True
    """

    scale_a = PeriodicNoteScale(
        notation, 
        [notation.note(*pair) for pair in input_pairs_a]
    )

    scale_b = PeriodicNoteScale(
        notation, 
        [notation.note(*pair) for pair in input_pairs_b]
    )

    scale_c = scale_a.note_difference(
        scale_b,
        ignore_bi_index=True
    )

    assert len(scale_c) == len(result_pairs)
    notes = list(scale_c)
    assert notes == [notation.note(*pair) for pair in result_pairs]


def test_difference_incompatible_origin_contexts():
    """
    Test if difference operation fails if scales originate from
    different notations
    """

    n_edo12_2 = make_nat_acc_test_notation(edo12)
    notations = n_edo12, n_edo24, n_edo31, n_edo12_2

    for i, notation_a in enumerate(notations):

        for notation_b in notations[i+1:]:

            scale_a = PeriodicNoteScale(
                notation_a
            )
            scale_b = PeriodicNoteScale(
                notation_b
            )

            with pytest.raises(IncompatibleOriginContexts):
                scale_a.difference(scale_b)

            with pytest.raises(IncompatibleOriginContexts):
                scale_a - scale_b


def test_note_difference_incompatible_origin_contexts():
    """
    Test if note_difference operation fails if scales originate from
    different notations
    """

    n_edo12_2 = make_nat_acc_test_notation(edo12)
    notations = n_edo12, n_edo24, n_edo31, n_edo12_2

    for i, notation_a in enumerate(notations):

        for notation_b in notations[i+1:]:

            scale_a = PeriodicNoteScale(
                notation_a
            )
            scale_b = PeriodicNoteScale(
                notation_b
            )

            with pytest.raises(IncompatibleOriginContexts):
                scale_a.note_difference(scale_b)


@pytest.mark.parametrize(
    'notation, input_pairs_a, input_pairs_b, result_pairs',
    [
        (
            n_edo12,
            [('A+', 0), ('B+', 0), ('D+', 0)],
            [('A+', 0), ('C', 0), ('D+', 0)],
            [('B+', 0), ('C', 0)],
        ),
        (
            n_edo12,
            [('A+', 0), ('B+', 1), ('F', 2)],
            [('A+', 0), ('B+', 1), ('F', 2)],
            [],
        ),
        (
            n_edo24,
            [('A+', 0), ('B+', 1), ('F+', 2)],
            [('A', 0), ('B', 0), ('F', 2)],
            [('A', 0), ('A+', 0), ('B', 0), ('B+', 1), ('F', 2), ('F+', 2)],
        ),
        (
            n_edo24,
            [('A+', 0), ('B+', 1), ('F', 2)],
            [],
            [('A+', 0), ('B+', 1), ('F', 2)],
        ),
    ]
)
def test_symmetric_difference(notation, input_pairs_a, input_pairs_b, result_pairs):
    """
    Test if symmetric_difference operation works correctly
    """

    scale_a = PeriodicNoteScale(
        notation, 
        [notation.note(*pair) for pair in input_pairs_a]
    )

    scale_b = PeriodicNoteScale(
        notation, 
        [notation.note(*pair) for pair in input_pairs_b]
    )

    scale_c = scale_a.symmetric_difference(scale_b)
    assert len(scale_c) == len(result_pairs)
    notes = list(scale_c)
    assert notes == [notation.note(*pair) for pair in result_pairs]

    scale_c = scale_a ^ scale_b
    assert len(scale_c) == len(result_pairs)
    notes = list(scale_c)
    assert notes == [notation.note(*pair) for pair in result_pairs]


@pytest.mark.parametrize(
    'notation, input_pairs_a, input_pairs_b, result_pairs',
    [
        (
            n_edo12,
            [('A+', 0), ('B+', 0), ('D+', 0)],
            [('A+', 1), ('C', 0), ('D+', 0)],
            [('B+', 0), ('C', 0)],
        ),
        (
            n_edo12,
            [('A+', 0), ('B+', 1), ('F', 2)],
            [('A+', 1), ('B+', 3), ('F', 5)],
            [],
        ),
        (
            n_edo24,
            [('A+', 0), ('B+', 1), ('F+', 2)],
            [('A', 1), ('B', 3), ('F', 2)],
            [('A+', 0), ('A', 1), ('B+', 1), ('F', 2), ('F+', 2), ('B', 3)],
        ),
        (
            n_edo24,
            [('A+', 0), ('B+', 1), ('F', 2)],
            [],
            [('A+', 0), ('B+', 1), ('F', 2)],
        ),
    ]
)
def test_symmetric_difference_ignore_bi_index(
    notation,
    input_pairs_a,
    input_pairs_b,
    result_pairs
):
    """
    Test if symmetric_difference operation works correctly
    on ignore_bi_index=True
    """

    scale_a = PeriodicNoteScale(
        notation, 
        [notation.note(*pair) for pair in input_pairs_a]
    )

    scale_b = PeriodicNoteScale(
        notation, 
        [notation.note(*pair) for pair in input_pairs_b]
    )

    scale_c = scale_a.symmetric_difference(scale_b, ignore_bi_index=True)

    assert len(scale_c) == len(result_pairs)
    notes = list(scale_c)
    assert notes == [notation.note(*pair) for pair in result_pairs]


def test_symmetric_difference_incompatible_origin_contexts():
    """
    Test if symmetric_difference operation fails if scales originate from
    different notations
    """

    n_edo12_2 = make_nat_acc_test_notation(edo12)
    notations = n_edo12, n_edo24, n_edo31, n_edo12_2

    for i, notation_a in enumerate(notations):

        for notation_b in notations[i+1:]:

            scale_a = PeriodicNoteScale(
                notation_a
            )
            scale_b = PeriodicNoteScale(
                notation_b
            )

            with pytest.raises(IncompatibleOriginContexts):
                scale_a.symmetric_difference(scale_b)

            with pytest.raises(IncompatibleOriginContexts):
                scale_a ^ scale_b


@pytest.mark.parametrize(
    'notation, input_pairs_a, input_pairs_b, expected',
    [
        (
            n_edo12,
            [('A+', 0), ('B+', 0), ('D+', 0)],
            [('A+', 0), ('C', 0), ('D+', 0)],
            False
        ),
        (
            n_edo12,
            [('A+', 0), ('B+', 0), ('D+', 0)],
            [('A+', 0), ('C', 0), ('E-', 0)],
            False
        ),
        (
            n_edo12,
            [('A+', 0), ('B+', 1), ('F', 2)],
            [('A+', 0), ('C-', 1), ('Ex', 2)],
            False
        ),
        (
            n_edo24,
            [('A+', 0), ('B+', 1), ('F+', 2)],
            [('A', 0), ('B', 0), ('F', 2)],
            True
        ),
        (
            n_edo24,
            [('A+', 0), ('B+', 1), ('F', 2)],
            [],
            True
        ),
    ]
)
def test_is_disjoint(notation, input_pairs_a, input_pairs_b, expected):
    """
    Test if is_disjoint operation works correctly
    """

    scale_a = PeriodicNoteScale(
        notation, 
        [notation.note(*pair) for pair in input_pairs_a]
    )

    scale_b = PeriodicNoteScale(
        notation, 
        [notation.note(*pair) for pair in input_pairs_b]
    )

    assert scale_a.is_disjoint(scale_b) == expected


@pytest.mark.parametrize(
    'notation, input_pairs_a, input_pairs_b, expected',
    [
        (
            n_edo12,
            [('A+', 0), ('B+', 0), ('D+', 0)],
            [('A+', 1), ('C', 0), ('D+', 0)],
            False
        ),
        (
            n_edo12,
            [('A+', 0), ('B+', 0), ('D+', 0)],
            [('A+', 0), ('C', 0), ('E-', 1)],
            False
        ),
        (
            n_edo12,
            [('A+', 0), ('B+', 1), ('F', 2)],
            [('A+', 0), ('C-', 1), ('Ex', 2)],
            False
        ),
        (
            n_edo24,
            [('A+', 0), ('B+', 1), ('F+', 2)],
            [('A', 0), ('B', 1), ('F', 2)],
            True
        ),
        (
            n_edo24,
            [('A+', 0), ('B+', 1), ('F', 2)],
            [],
            True
        ),
    ]
)
def test_is_disjoint_ignore_bi_index(notation, input_pairs_a, input_pairs_b, expected):
    """
    Test if is_disjoint operation works correctly
    on ignore_bi_index=True
    """

    scale_a = PeriodicNoteScale(
        notation, 
        [notation.note(*pair) for pair in input_pairs_a]
    )

    scale_b = PeriodicNoteScale(
        notation, 
        [notation.note(*pair) for pair in input_pairs_b]
    )

    assert scale_a.is_disjoint(scale_b, ignore_bi_index=True) == expected


@pytest.mark.parametrize(
    'notation, input_pairs_a, input_pairs_b, expected',
    [
        (
            n_edo12,
            [('A+', 0), ('B+', 0), ('D+', 0)],
            [('A+', 0), ('C', 0), ('D+', 0)],
            False
        ),
        (
            n_edo12,
            [('A+', 0), ('B+', 0), ('D+', 0)],
            [('A+', 0), ('C', 0), ('E-', 0)],
            False
        ),
        (
            n_edo12,
            [('A+', 0), ('B+', 1), ('F', 2)],
            [('A+', 0), ('C-', 1), ('Ex', 2)],
            False
        ),
        (
            n_edo24,
            [('A+', 0), ('B+', 1), ('F+', 2)],
            [('A', 0), ('B', 0), ('F', 2)],
            True
        ),
        (
            n_edo24,
            [('A+', 0), ('B+', 1), ('F', 2)],
            [],
            True
        ),
    ]
)
def test_is_notated_disjoint(notation, input_pairs_a, input_pairs_b, expected):
    """
    Test if is_notated_disjoint operation works correctly
    """

    scale_a = PeriodicNoteScale(
        notation, 
        [notation.note(*pair) for pair in input_pairs_a]
    )

    scale_b = PeriodicNoteScale(
        notation, 
        [notation.note(*pair) for pair in input_pairs_b]
    )

    assert scale_a.is_notated_disjoint(scale_b) == expected


@pytest.mark.parametrize(
    'notation, input_pairs_a, input_pairs_b, expected',
    [
        (
            n_edo12,
            [('A+', 0), ('B+', 0), ('D+', 0)],
            [('A+', 1), ('C', 0), ('D+', 0)],
            False
        ),
        (
            n_edo12,
            [('A+', 0), ('B+', 0), ('D+', 0)],
            [('A+', 0), ('C', 1), ('E-', 1)],
            False
        ),
        (
            n_edo12,
            [('A+', 0), ('B+', 1), ('F', 2)],
            [('A+', 2), ('C-', 1), ('Ex', 2)],
            False
        ),
        (
            n_edo24,
            [('A+', 0), ('B+', 1), ('F+', 2)],
            [('A', 1), ('B', 2), ('F', 3)],
            True
        ),
        (
            n_edo24,
            [('A+', 0), ('B+', 1), ('F', 2)],
            [],
            True
        ),
    ]
)
def test_is_notated_disjoint_ignore_bi_index(
    notation,
    input_pairs_a,
    input_pairs_b,
    expected
):
    """
    Test if is_notated_disjoint operation works correctly
    on ignore_bi_index=True
    """

    scale_a = PeriodicNoteScale(
        notation, 
        [notation.note(*pair) for pair in input_pairs_a]
    )

    scale_b = PeriodicNoteScale(
        notation, 
        [notation.note(*pair) for pair in input_pairs_b]
    )

    assert scale_a.is_notated_disjoint(
        scale_b,
        ignore_bi_index=True
    ) == expected


def test_is_disjoint_incompatible_origin_contexts():
    """
    Test if is_disjoint operation fails if scales originate from
    different notations
    """

    n_edo12_2 = make_nat_acc_test_notation(edo12)
    notations = n_edo12, n_edo24, n_edo31, n_edo12_2

    for i, notation_a in enumerate(notations):

        for notation_b in notations[i+1:]:

            scale_a = PeriodicNoteScale(
                notation_a
            )
            scale_b = PeriodicNoteScale(
                notation_b
            )

            with pytest.raises(IncompatibleOriginContexts):
                scale_a.is_disjoint(scale_b)


def test_is_notated_disjoint_incompatible_origin_contexts():
    """
    Test if is_notated_disjoint operation fails if scales originate from
    different notations
    """

    n_edo12_2 = make_nat_acc_test_notation(edo12)
    notations = n_edo12, n_edo24, n_edo31, n_edo12_2

    for i, notation_a in enumerate(notations):

        for notation_b in notations[i+1:]:

            scale_a = PeriodicNoteScale(
                notation_a
            )
            scale_b = PeriodicNoteScale(
                notation_b
            )

            with pytest.raises(IncompatibleOriginContexts):
                scale_a.is_notated_disjoint(scale_b)


@pytest.mark.parametrize(
    'notation, input_pairs_a, input_pairs_b, expected',
    [
        (
            n_edo12,
            [('A+', 0), ('D+', 0)],
            [('A+', 0), ('B+', 0), ('D+', 0)],
            True
        ),
        (
            n_edo12,
            [('A+', 0), ('E-', 0)],
            [('A+', 0), ('B+', 0), ('D+', 0)],
            True
        ),
        (
            n_edo12,
            [('A+', 0), ('B+', 1), ('F', 2)],
            [('A+', 0), ('C-', 1), ('Ex', 2)],
            True
        ),
        (
            n_edo24,
            [('A+', 0), ('B+', 1), ('F+', 2)],
            [('A', 0), ('B', 0), ('F', 2)],
            False
        ),
        (
            n_edo24,
            [],
            [('A+', 0), ('B+', 1), ('F', 2)],
            True
        ),
        (
            n_edo24,
            [('A+', 0), ('B+', 1), ('F', 2)],
            [],
            False
        ),
    ]
)
def test_is_subset(notation, input_pairs_a, input_pairs_b, expected):
    """
    Test if is_subset operation works correctly
    """

    scale_a = PeriodicNoteScale(
        notation, 
        [notation.note(*pair) for pair in input_pairs_a]
    )

    scale_b = PeriodicNoteScale(
        notation, 
        [notation.note(*pair) for pair in input_pairs_b]
    )

    assert scale_a.is_subset(scale_b) == expected


@pytest.mark.parametrize(
    'notation, input_pairs_a, input_pairs_b, expected',
    [
        (
            n_edo12,
            [('A+', 0), ('D+', 2)],
            [('A+', 1), ('B+', 0), ('D+', 0)],
            True
        ),
        (
            n_edo12,
            [('A+', 0), ('E-', 1)],
            [('A+', 0), ('B+', 1), ('D+', 0)],
            True
        ),
        (
            n_edo12,
            [('A+', 0), ('B+', 1), ('F', 2)],
            [('A+', 0), ('C-', 2), ('Ex', 2)],
            True
        ),
        (
            n_edo24,
            [('A+', 0), ('B+', 1), ('F+', 2)],
            [('A', 0), ('B', 0), ('F', 2)],
            False
        ),
        (
            n_edo24,
            [],
            [('A+', 0), ('B+', 1), ('F', 2)],
            True
        ),
        (
            n_edo24,
            [('A+', 0), ('B+', 1), ('F', 2)],
            [],
            False
        ),
    ]
)
def test_is_subset_ignore_bi_index(notation, input_pairs_a, input_pairs_b, expected):
    """
    Test if is_subset operation works correctly
    on ignore_bi_index=True
    """

    scale_a = PeriodicNoteScale(
        notation, 
        [notation.note(*pair) for pair in input_pairs_a]
    )

    scale_b = PeriodicNoteScale(
        notation, 
        [notation.note(*pair) for pair in input_pairs_b]
    )

    assert scale_a.is_subset(scale_b, ignore_bi_index=True) == expected


@pytest.mark.parametrize(
    'notation, input_pairs_a, input_pairs_b, expected',
    [
        (
            n_edo12,
            [('A+', 0), ('D+', 0)],
            [('A+', 0), ('B+', 0), ('D+', 0)],
            True
        ),
        (
            n_edo12,
            [('A+', 0), ('E-', 0)],
            [('A+', 0), ('B+', 0), ('D+', 0)],
            True
        ),
        (
            n_edo12,
            [('A+', 0), ('B+', 1), ('F', 2)],
            [('A+', 0), ('C-', 1), ('Ex', 2)],
            False
        ),
        (
            n_edo24,
            [('A+', 0), ('B+', 1), ('F+', 2)],
            [('A', 0), ('B', 0), ('F', 2)],
            False
        ),
        (
            n_edo24,
            [],
            [('A+', 0), ('B+', 1), ('F', 2)],
            True
        ),
        (
            n_edo24,
            [('A+', 0), ('B+', 1), ('F', 2)],
            [],
            False
        ),
    ]
)
def test_is_subset_proper(notation, input_pairs_a, input_pairs_b, expected):
    """
    Test if is_subset operation works correctly
    on proper=True
    """

    scale_a = PeriodicNoteScale(
        notation, 
        [notation.note(*pair) for pair in input_pairs_a]
    )

    scale_b = PeriodicNoteScale(
        notation, 
        [notation.note(*pair) for pair in input_pairs_b]
    )

    assert scale_a.is_subset(scale_b, proper=True) == expected


@pytest.mark.parametrize(
    'notation, input_pairs_a, input_pairs_b, expected',
    [
        (
            n_edo12,
            [('A+', 0), ('D+', 0)],
            [('A+', 0), ('B+', 1), ('D+', 0)],
            True
        ),
        (
            n_edo12,
            [('A+', 0), ('E-', 0)],
            [('A+', 2), ('B+', 0), ('D+', 3)],
            True
        ),
        (
            n_edo12,
            [('A+', 0), ('B+', 1), ('F', 2)],
            [('A+', 0), ('C-', 2), ('Ex', 2)],
            False
        ),
        (
            n_edo24,
            [('A+', 0), ('B+', 1), ('F+', 2)],
            [('A', 0), ('B', 0), ('F', 2)],
            False
        ),
        (
            n_edo24,
            [],
            [('A+', 0), ('B+', 1), ('F', 2)],
            True
        ),
        (
            n_edo24,
            [('A+', 0), ('B+', 1), ('F', 2)],
            [],
            False
        ),
    ]
)
def test_is_subset_proper_ignore_bi_index(notation, input_pairs_a, input_pairs_b, expected):
    """
    Test if is_subset operation works correctly
    on proper=True and ignore_bi_index=True
    """

    scale_a = PeriodicNoteScale(
        notation, 
        [notation.note(*pair) for pair in input_pairs_a]
    )

    scale_b = PeriodicNoteScale(
        notation, 
        [notation.note(*pair) for pair in input_pairs_b]
    )

    assert scale_a.is_subset(
        scale_b,
        ignore_bi_index=True,
        proper=True
    ) == expected


@pytest.mark.parametrize(
    'notation, input_pairs_a, input_pairs_b, expected',
    [
        (
            n_edo12,
            [('A+', 0), ('D+', 0)],
            [('A+', 0), ('B+', 0), ('D+', 0)],
            True
        ),
        (
            n_edo12,
            [('A+', 0), ('B+', 0), ('D+', 0)],
            [('A+', 0), ('B+', 0), ('D+', 0)],
            True
        ),
        (
            n_edo12,
            [('A+', 0), ('E-', 0)],
            [('A+', 0), ('B+', 0), ('D+', 0)],
            False
        ),
        (
            n_edo12,
            [('A+', 0), ('B+', 1), ('F', 2)],
            [('A+', 0), ('C-', 1), ('Ex', 2)],
            False
        ),
        (
            n_edo24,
            [('A+', 0), ('B+', 1), ('F+', 2)],
            [('A', 0), ('B', 0), ('F', 2)],
            False
        ),
        (
            n_edo24,
            [],
            [('A+', 0), ('B+', 1), ('F', 2)],
            True
        ),
        (
            n_edo24,
            [('A+', 0), ('B+', 1), ('F', 2)],
            [],
            False
        ),
    ]
)
def test_is_note_subset(notation, input_pairs_a, input_pairs_b, expected):
    """
    Test if is_note_subset operation works correctly
    """

    scale_a = PeriodicNoteScale(
        notation, 
        [notation.note(*pair) for pair in input_pairs_a]
    )

    scale_b = PeriodicNoteScale(
        notation, 
        [notation.note(*pair) for pair in input_pairs_b]
    )

    assert scale_a.is_note_subset(scale_b) == expected


@pytest.mark.parametrize(
    'notation, input_pairs_a, input_pairs_b, expected',
    [
        (
            n_edo12,
            [('A+', 0), ('D+', 0)],
            [('A+', 0), ('B+', 1), ('D+', 2)],
            True
        ),
        (
            n_edo12,
            [('A+', 0), ('B+', 0), ('D+', 0)],
            [('A+', 1), ('B+', 4), ('D+', 2)],
            True
        ),
        (
            n_edo12,
            [('A+', 0), ('E-', 0)],
            [('A+', 2), ('B+', 0), ('D+', 1)],
            False
        ),
        (
            n_edo12,
            [('A+', 0), ('B+', 1), ('F', 2)],
            [('A+', 1), ('C-', 1), ('Ex', 2)],
            False
        ),
        (
            n_edo24,
            [('A+', 0), ('B+', 1), ('F+', 2)],
            [('A', 3), ('B', 0), ('F', 2)],
            False
        ),
        (
            n_edo24,
            [],
            [('A+', 0), ('B+', 1), ('F', 2)],
            True
        ),
        (
            n_edo24,
            [('A+', 0), ('B+', 1), ('F', 2)],
            [],
            False
        ),
    ]
)
def test_is_note_subset_ignore_bi_index(
    notation,
    input_pairs_a,
    input_pairs_b,
    expected
):
    """
    Test if is_note_subset operation works correctly
    on ignore_bi_index=True
    """

    scale_a = PeriodicNoteScale(
        notation, 
        [notation.note(*pair) for pair in input_pairs_a]
    )

    scale_b = PeriodicNoteScale(
        notation, 
        [notation.note(*pair) for pair in input_pairs_b]
    )

    assert scale_a.is_note_subset(
        scale_b,
        ignore_bi_index=True
    ) == expected


@pytest.mark.parametrize(
    'notation, input_pairs_a, input_pairs_b, expected',
    [
        (
            n_edo12,
            [('A+', 0), ('D+', 0)],
            [('A+', 0), ('B+', 0), ('D+', 0)],
            True
        ),
        (
            n_edo12,
            [('A+', 0), ('B+', 0), ('D+', 0)],
            [('A+', 0), ('B+', 0), ('D+', 0)],
            False
        ),
        (
            n_edo12,
            [('A+', 0), ('E-', 0)],
            [('A+', 0), ('B+', 0), ('D+', 0)],
            False
        ),
        (
            n_edo12,
            [('A+', 0), ('B+', 1), ('F', 2)],
            [('A+', 0), ('C-', 1), ('Ex', 2)],
            False
        ),
        (
            n_edo24,
            [('A+', 0), ('B+', 1), ('F+', 2)],
            [('A', 0), ('B', 0), ('F', 2)],
            False
        ),
        (
            n_edo24,
            [],
            [('A+', 0), ('B+', 1), ('F', 2)],
            True
        ),
        (
            n_edo24,
            [('A+', 0), ('B+', 1), ('F', 2)],
            [],
            False
        ),
    ]
)
def test_is_note_subset_proper(
    notation,
    input_pairs_a,
    input_pairs_b,
    expected
):
    """
    Test if is_note_subset operation works correctly
    on proper=True
    """

    scale_a = PeriodicNoteScale(
        notation, 
        [notation.note(*pair) for pair in input_pairs_a]
    )

    scale_b = PeriodicNoteScale(
        notation, 
        [notation.note(*pair) for pair in input_pairs_b]
    )

    assert scale_a.is_note_subset(
        scale_b, 
        proper=True
    ) == expected


@pytest.mark.parametrize(
    'notation, input_pairs_a, input_pairs_b, expected',
    [
        (
            n_edo12,
            [('A+', 0), ('D+', 0)],
            [('A+', 1), ('B+', 0), ('D+', 0)],
            True
        ),
        (
            n_edo12,
            [('A+', 0), ('B+', 0), ('D+', 0)],
            [('A+', 0), ('B+', 2), ('D+', 0)],
            False
        ),
        (
            n_edo12,
            [('A+', 0), ('E-', 0)],
            [('A+', 1), ('B+', 2), ('D+', 0)],
            False
        ),
        (
            n_edo12,
            [('A+', 0), ('B+', 1), ('F', 2)],
            [('A+', 1), ('C-', 2), ('Ex', 2)],
            False
        ),
        (
            n_edo24,
            [('A+', 0), ('B+', 1), ('F+', 2)],
            [('A', 0), ('B', 0), ('F', 2)],
            False
        ),
        (
            n_edo24,
            [],
            [('A+', 0), ('B+', 1), ('F', 2)],
            True
        ),
        (
            n_edo24,
            [('A+', 0), ('B+', 1), ('F', 2)],
            [],
            False
        ),
    ]
)
def test_is_note_subset_proper_ignore_bi_index(
    notation,
    input_pairs_a,
    input_pairs_b,
    expected
):
    """
    Test if is_note_subset operation works correctly
    on proper=True and ignore_bi_index=True
    """

    scale_a = PeriodicNoteScale(
        notation, 
        [notation.note(*pair) for pair in input_pairs_a]
    )

    scale_b = PeriodicNoteScale(
        notation, 
        [notation.note(*pair) for pair in input_pairs_b]
    )

    assert scale_a.is_note_subset(
        scale_b, 
        proper=True,
        ignore_bi_index=True
    ) == expected


def test_is_subset_incompatible_origin_contexts():
    """
    Test if is_subset operation fails if scales originate from
    different notations
    """

    n_edo12_2 = make_nat_acc_test_notation(edo12)
    notations = n_edo12, n_edo24, n_edo31, n_edo12_2

    for i, notation_a in enumerate(notations):

        for notation_b in notations[i+1:]:

            scale_a = PeriodicNoteScale(
                notation_a
            )
            scale_b = PeriodicNoteScale(
                notation_b
            )

            with pytest.raises(IncompatibleOriginContexts):
                scale_a.is_subset(scale_b)


def test_is_note_subset_incompatible_origin_contexts():
    """
    Test if is_note_subset operation fails if scales originate from
    different notations
    """

    n_edo12_2 = make_nat_acc_test_notation(edo12)
    notations = n_edo12, n_edo24, n_edo31, n_edo12_2

    for i, notation_a in enumerate(notations):

        for notation_b in notations[i+1:]:

            scale_a = PeriodicNoteScale(
                notation_a
            )
            scale_b = PeriodicNoteScale(
                notation_b
            )

            with pytest.raises(IncompatibleOriginContexts):
                scale_a.is_note_subset(scale_b)


@pytest.mark.parametrize(
    'notation, input_pairs_a, input_pairs_b, expected',
    [
        (
            n_edo12,
            [('A+', 0), ('B+', 0), ('D+', 0)],
            [('A+', 0), ('D+', 0)],
            True
        ),
        (
            n_edo12,
            [('A+', 0), ('B+', 0), ('D+', 0)],
            [('A+', 0), ('E-', 0)],
            True
        ),
        (
            n_edo12,
            [('A+', 0), ('C-', 1), ('Ex', 2)],
            [('A+', 0), ('B+', 1), ('F', 2)],
            True
        ),
        (
            n_edo24,
            [('A', 0), ('B', 0), ('F', 2)],
            [('A+', 0), ('B+', 1), ('F+', 2)],
            False
        ),
        (
            n_edo24,
            [('A+', 0), ('B+', 1), ('F', 2)],
            [],
            True
        ),
        (
            n_edo24,
            [],
            [('A+', 0), ('B+', 1), ('F', 2)],
            False
        ),
    ]
)
def test_is_superset(notation, input_pairs_a, input_pairs_b, expected):
    """
    Test if is_superset operation works correctly
    """

    scale_a = PeriodicNoteScale(
        notation, 
        [notation.note(*pair) for pair in input_pairs_a]
    )

    scale_b = PeriodicNoteScale(
        notation, 
        [notation.note(*pair) for pair in input_pairs_b]
    )

    assert scale_a.is_superset(scale_b) == expected


@pytest.mark.parametrize(
    'notation, input_pairs_a, input_pairs_b, expected',
    [
        (
            n_edo12,
            [('A+', 1), ('B+', 0), ('D+', 0)],
            [('A+', 0), ('D+', 2)],
            True
        ),
        (
            n_edo12,
            [('A+', 0), ('B+', 1), ('D+', 0)],
            [('A+', 0), ('E-', 1)],
            True
        ),
        (
            n_edo12,
            [('A+', 0), ('C-', 2), ('Ex', 2)],
            [('A+', 0), ('B+', 1), ('F', 2)],
            True
        ),
        (
            n_edo24,
            [('A', 0), ('B', 0), ('F', 2)],
            [('A+', 0), ('B+', 1), ('F+', 2)],
            False
        ),
        (
            n_edo24,
            [('A+', 0), ('B+', 1), ('F', 2)],
            [],
            True
        ),
        (
            n_edo24,
            [],
            [('A+', 0), ('B+', 1), ('F', 2)],
            False
        ),
    ]
)
def test_is_superset_ignore_bi_index(notation, input_pairs_a, input_pairs_b, expected):
    """
    Test if is_superset operation works correctly
    on ignore_bi_index=True
    """

    scale_a = PeriodicNoteScale(
        notation, 
        [notation.note(*pair) for pair in input_pairs_a]
    )

    scale_b = PeriodicNoteScale(
        notation, 
        [notation.note(*pair) for pair in input_pairs_b]
    )

    assert scale_a.is_superset(
        scale_b,
        ignore_bi_index=True
    ) == expected


@pytest.mark.parametrize(
    'notation, input_pairs_a, input_pairs_b, expected',
    [
        (
            n_edo12,
            [('A+', 0), ('B+', 0), ('D+', 0)],
            [('A+', 0), ('D+', 0)],
            True
        ),
        (
            n_edo12,
            [('A+', 0), ('B+', 0), ('D+', 0)],
            [('A+', 0), ('E-', 0)],
            True
        ),
        (
            n_edo12,
            [('A+', 0), ('C-', 1), ('Ex', 2)],
            [('A+', 0), ('B+', 1), ('F', 2)],
            False
        ),
        (
            n_edo24,
            [('A', 0), ('B', 0), ('F', 2)],
            [('A+', 0), ('B+', 1), ('F+', 2)],
            False
        ),
        (
            n_edo24,
            [('A+', 0), ('B+', 1), ('F', 2)],
            [],
            True
        ),
        (
            n_edo24,
            [],
            [('A+', 0), ('B+', 1), ('F', 2)],
            False
        ),
    ]
)
def test_is_superset_proper(notation, input_pairs_a, input_pairs_b, expected):
    """
    Test if is_superset operation works correctly
    on proper=True
    """

    scale_a = PeriodicNoteScale(
        notation, 
        [notation.note(*pair) for pair in input_pairs_a]
    )

    scale_b = PeriodicNoteScale(
        notation, 
        [notation.note(*pair) for pair in input_pairs_b]
    )

    assert scale_a.is_superset(scale_b, proper=True) == expected


@pytest.mark.parametrize(
    'notation, input_pairs_a, input_pairs_b, expected',
    [
        (
            n_edo12,
            [('A+', 0), ('B+', 1), ('D+', 0)],
            [('A+', 0), ('D+', 0)],
            True
        ),
        (
            n_edo12,
            [('A+', 2), ('B+', 0), ('D+', 3)],
            [('A+', 0), ('E-', 0)],
            True
        ),
        (
            n_edo12,
            [('A+', 0), ('C-', 2), ('Ex', 2)],
            [('A+', 0), ('B+', 1), ('F', 2)],
            False
        ),
        (
            n_edo24,
            [('A', 0), ('B', 0), ('F', 2)],
            [('A+', 0), ('B+', 1), ('F+', 2)],
            False
        ),
        (
            n_edo24,
            [('A+', 0), ('B+', 1), ('F', 2)],
            [],
            True
        ),
        (
            n_edo24,
            [],
            [('A+', 0), ('B+', 1), ('F', 2)],
            False
        ),
    ]
)
def test_is_superset_proper_ignore_bi_index(notation, input_pairs_a, input_pairs_b, expected):
    """
    Test if is_superset operation works correctly
    on proper=True and ignore_bi_index=True
    """

    scale_a = PeriodicNoteScale(
        notation, 
        [notation.note(*pair) for pair in input_pairs_a]
    )

    scale_b = PeriodicNoteScale(
        notation, 
        [notation.note(*pair) for pair in input_pairs_b]
    )

    assert scale_a.is_superset(
        scale_b,
        ignore_bi_index=True,
        proper=True
    ) == expected


@pytest.mark.parametrize(
    'notation, input_pairs_a, input_pairs_b, expected',
    [
        (
            n_edo12,
            [('A+', 0), ('B+', 0), ('D+', 0)],
            [('A+', 0), ('D+', 0)],
            True
        ),
        (
            n_edo12,
            [('A+', 0), ('B+', 0), ('D+', 0)],
            [('A+', 0), ('B+', 0), ('D+', 0)],
            True
        ),
        (
            n_edo12,
            [('A+', 0), ('B+', 0), ('D+', 0)],
            [('A+', 0), ('E-', 0)],
            False
        ),
        (
            n_edo12,
            [('A+', 0), ('C-', 1), ('Ex', 2)],
            [('A+', 0), ('B+', 1), ('F', 2)],
            False
        ),
        (
            n_edo24,
            [('A', 0), ('B', 0), ('F', 2)],
            [('A+', 0), ('B+', 1), ('F+', 2)],
            False
        ),
        (
            n_edo24,
            [('A+', 0), ('B+', 1), ('F', 2)],
            [],
            True
        ),
        (
            n_edo24,
            [],
            [('A+', 0), ('B+', 1), ('F', 2)],
            False
        ),
    ]
)
def test_is_note_superset(notation, input_pairs_a, input_pairs_b, expected):
    """
    Test if is_note_superset operation works correctly
    """

    scale_a = PeriodicNoteScale(
        notation,
        [notation.note(*pair) for pair in input_pairs_a]
    )

    scale_b = PeriodicNoteScale(
        notation,
        [notation.note(*pair) for pair in input_pairs_b]
    )

    assert scale_a.is_note_superset(scale_b) == expected


@pytest.mark.parametrize(
    'notation, input_pairs_a, input_pairs_b, expected',
    [
        (
            n_edo12,
            [('A+', 0), ('B+', 1), ('D+', 2)],
            [('A+', 0), ('D+', 0)],
            True
        ),
        (
            n_edo12,
            [('A+', 1), ('B+', 4), ('D+', 2)],
            [('A+', 0), ('B+', 0), ('D+', 0)],
            True
        ),
        (
            n_edo12,
            [('A+', 2), ('B+', 0), ('D+', 1)],
            [('A+', 0), ('E-', 0)],
            False
        ),
        (
            n_edo12,
            [('A+', 1), ('C-', 1), ('Ex', 2)],
            [('A+', 0), ('B+', 1), ('F', 2)],
            False
        ),
        (
            n_edo24,
            [('A', 3), ('B', 0), ('F', 2)],
            [('A+', 0), ('B+', 1), ('F+', 2)],
            False
        ),
        (
            n_edo24,
            [('A+', 0), ('B+', 1), ('F', 2)],
            [],
            True
        ),
        (
            n_edo24,
            [],
            [('A+', 0), ('B+', 1), ('F', 2)],
            False
        ),
    ]
)
def test_is_note_superset_ignore_bi_index(
    notation,
    input_pairs_a,
    input_pairs_b,
    expected
):
    """
    Test if is_note_superset operation works correctly
    on ignore_bi_index=True
    """

    scale_a = PeriodicNoteScale(
        notation, 
        [notation.note(*pair) for pair in input_pairs_a]
    )

    scale_b = PeriodicNoteScale(
        notation, 
        [notation.note(*pair) for pair in input_pairs_b]
    )

    assert scale_a.is_note_superset(
        scale_b,
        ignore_bi_index=True
    ) == expected


@pytest.mark.parametrize(
    'notation, input_pairs_a, input_pairs_b, expected',
    [
        (
            n_edo12,
            [('A+', 0), ('B+', 0), ('D+', 0)],
            [('A+', 0), ('D+', 0)],
            True
        ),
        (
            n_edo12,
            [('A+', 0), ('B+', 0), ('D+', 0)],
            [('A+', 0), ('B+', 0), ('D+', 0)],
            False
        ),
        (
            n_edo12,
            [('A+', 0), ('B+', 0), ('D+', 0)],
            [('A+', 0), ('E-', 0)],
            False
        ),
        (
            n_edo12,
            [('A+', 0), ('C-', 1), ('Ex', 2)],
            [('A+', 0), ('B+', 1), ('F', 2)],
            False
        ),
        (
            n_edo24,
            [('A', 0), ('B', 0), ('F', 2)],
            [('A+', 0), ('B+', 1), ('F+', 2)],
            False
        ),
        (
            n_edo24,
            [('A+', 0), ('B+', 1), ('F', 2)],
            [],
            True
        ),
        (
            n_edo24,
            [],
            [('A+', 0), ('B+', 1), ('F', 2)],
            False
        ),
    ]
)
def test_is_note_superset_proper(
    notation,
    input_pairs_a,
    input_pairs_b,
    expected
):
    """
    Test if is_note_superset operation works correctly
    on proper=True
    """

    scale_a = PeriodicNoteScale(
        notation,
        [notation.note(*pair) for pair in input_pairs_a]
    )

    scale_b = PeriodicNoteScale(
        notation,
        [notation.note(*pair) for pair in input_pairs_b]
    )

    assert scale_a.is_note_superset(
        scale_b,
        proper=True
    ) == expected


@pytest.mark.parametrize(
    'notation, input_pairs_a, input_pairs_b, expected',
    [
        (
            n_edo12,
            [('A+', 1), ('B+', 0), ('D+', 0)],
            [('A+', 0), ('D+', 0)],
            True
        ),
        (
            n_edo12,
            [('A+', 0), ('B+', 2), ('D+', 0)],
            [('A+', 0), ('B+', 0), ('D+', 0)],
            False
        ),
        (
            n_edo12,
            [('A+', 1), ('B+', 2), ('D+', 0)],
            [('A+', 0), ('E-', 0)],
            False
        ),
        (
            n_edo12,
            [('A+', 1), ('C-', 2), ('Ex', 2)],
            [('A+', 0), ('B+', 1), ('F', 2)],
            False
        ),
        (
            n_edo24,
            [('A', 0), ('B', 0), ('F', 2)],
            [('A+', 0), ('B+', 1), ('F+', 2)],
            False
        ),
        (
            n_edo24,
            [('A+', 0), ('B+', 1), ('F', 2)],
            [],
            True
        ),
        (
            n_edo24,
            [],
            [('A+', 0), ('B+', 1), ('F', 2)],
            False
        ),
    ]
)
def test_is_note_superset_proper_ignore_bi_index(
    notation,
    input_pairs_a,
    input_pairs_b,
    expected
):
    """
    Test if is_superset operation works correctly
    on proper=True and ignore_bi_index=True
    """

    scale_a = PeriodicNoteScale(
        notation,
        [notation.note(*pair) for pair in input_pairs_a]
    )

    scale_b = PeriodicNoteScale(
        notation,
        [notation.note(*pair) for pair in input_pairs_b]
    )

    assert scale_a.is_note_superset(
        scale_b,
        proper=True,
        ignore_bi_index=True
    ) == expected


def test_is_superset_incompatible_origin_contexts():
    """
    Test if is_superset operation fails if scales originate from
    different notations
    """

    n_edo12_2 = make_nat_acc_test_notation(edo12)
    notations = n_edo12, n_edo24, n_edo31, n_edo12_2

    for i, notation_a in enumerate(notations):

        for notation_b in notations[i+1:]:

            scale_a = PeriodicNoteScale(
                notation_a
            )
            scale_b = PeriodicNoteScale(
                notation_b
            )

            with pytest.raises(IncompatibleOriginContexts):
                scale_a.is_superset(scale_b)


def test_is_note_superset_incompatible_origin_contexts():
    """
    Test if is_note_superset operation fails if scales originate from
    different notations
    """

    n_edo12_2 = make_nat_acc_test_notation(edo12)
    notations = n_edo12, n_edo24, n_edo31, n_edo12_2

    for i, notation_a in enumerate(notations):

        for notation_b in notations[i+1:]:

            scale_a = PeriodicNoteScale(
                notation_a
            )
            scale_b = PeriodicNoteScale(
                notation_b
            )

            with pytest.raises(IncompatibleOriginContexts):
                scale_a.is_note_superset(scale_b)


@pytest.mark.parametrize(
    'notation, input_pairs, result_pairs',
    [
        (
            n_edo12,
            [],
            [],
        ),
        (
            n_edo12,
            [('A+', 0), ('B+', 1), ('D+', 3)],
            [('A+', 0), ('B+', 0), ('D+', 0)],
        ),
        (
            n_edo12,
            [('C', 2), ('C+', 1), ('D+', 0)],
            [('C', 0), ('C+', 0), ('D+', 0)],
        ),
        (
            n_edo24,
            [('A+', 0), ('B+', 0), ('C', 0)],
            [('A+', 0), ('B+', 0), ('C', 0)],
        ),
    ]
)
def test_pcs_normalized(notation, input_pairs, result_pairs):
    """
    Test if pcs_normalized operation works correctly
    """

    input_scale = notation.scale(
        [notation.note(*pair) for pair in input_pairs]
    )

    result_scale = notation.scale(
        [notation.note(*pair) for pair in result_pairs]
    )

    n_scale = input_scale.pcs_normalized()
    assert n_scale.is_notated_same(result_scale)


@pytest.mark.parametrize(
    'notation, input_pairs, expected',
    [
        (
            n_edo12,
            [],
            True
        ),
        (
            n_edo12,
            [('A+', 0), ('B+', 1), ('D+', 3)],
            False
        ),
        (
            n_edo12,
            [('C', 2), ('C+', 1), ('D+', 0)],
            False
        ),
        (
            n_edo24,
            [('A+', 0), ('B+', 0), ('C', 0)],
            True
        ),
    ]
)
def test_is_pcs_normalized(notation, input_pairs, expected):
    """
    Test if is_pcs_normalized operation works correctly
    """

    input_scale = notation.scale(
        [notation.note(*pair) for pair in input_pairs]
    )

    assert input_scale.is_pcs_normalized == expected
