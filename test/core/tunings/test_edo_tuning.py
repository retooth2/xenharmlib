import pytest
from xenharmlib.core.tunings import EDOTuning

edo12 = EDOTuning('12-EDO', 12)
edo24 = EDOTuning('24-EDO', 24)
edo57 = EDOTuning('57-EDO', 57)
edo72 = EDOTuning('72-EDO', 72)

@pytest.mark.parametrize(
    'tuning, ring_number',
    [
        (edo12, 1),
        (edo24, 2),
        (edo57, 3),
        (edo72, 6),
    ]
)
def test_ring_number_fifth(tuning, ring_number):
    assert tuning.get_ring_number() == ring_number


@pytest.mark.parametrize(
    'divisions, sharpness',
    [
        (11, -2),
        (9, -1),
        (21, 0),
        (12, 1),
        (24, 2),
        (36, 3),
        (20, 4),
        (32, 5),
        (44, 6),
        (63, 7),
        (61, 8),
        (66, 9),
        (71, 10),
    ]
)
def test_sharpness(divisions, sharpness):
    tuning = EDOTuning('X', divisions)
    assert tuning.sharpness == sharpness


@pytest.mark.parametrize(
    'divisions',
    [
        8, 7, 12, 24, 31, 48
    ]
)
def test_repr(divisions):
    tuning = EDOTuning(f'{divisions}-EDO', divisions)
    assert repr(tuning) == f'EDOTuning({divisions}-EDO, {divisions})'