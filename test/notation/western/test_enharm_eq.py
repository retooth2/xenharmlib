from itertools import combinations
import pytest
from xenharmlib.notation.western import WesternNotation


@pytest.mark.parametrize(
    'enharmonics',
    [
        [('D', 0), ('Ebb', 0)],
        [('D#', 0), ('Eb', 0), ('Fbb', 0)],
        [('Dx', 0), ('E', 0), ('Fb', 0)],
        [('E#', 0), ('F', 0)],
        [('E#', 0), ('F', 0)],
    ]
)
def test_enharm_eq(enharmonics):
    """
    Test enharmonic equivalencies of notes in western notation
    """

    notation = WesternNotation()

    for note_pair_a, note_pair_b in combinations(enharmonics, 2):
        note_a = notation.note(*note_pair_a)
        note_b = notation.note(*note_pair_b)
        assert note_a == note_b
        assert note_b == note_a
