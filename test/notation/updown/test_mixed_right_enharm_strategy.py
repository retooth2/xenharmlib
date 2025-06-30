import pytest
from xenharmlib import EDOTuning
from xenharmlib import UpDownNotation
from xenharmlib.notation.updown import MixedRightEnharmStrategy

NOTATIONS = {
    i: UpDownNotation(EDOTuning(i))
    for i in [5, 7, 9, 10, 11, 12, 14, 18, 28, 31]
}


@pytest.mark.parametrize(
    'divisions, pitch_index, note_pair',
    [
        # sharpness -2
        (11, 9, ('C#', 1)),
        (11, 10, ('Bb', 0)),
        (11, 5, ('F', 0)),
        (11, 4, ('Eb', 0)),
        # sharpness -1
        (9, 12, ('Eb', 1)),
        (9, 13, ('F', 1)),
        # sharpness 0
        (7, 16, ('E', 2)),
        (7, 7, ('C', 1)),
        (14, 5, ('vF', 0)),
        (28, 27, ('vC', 1)),
        # sharpness 1
        (5, 2, ('E', 0)),
        (5, 3, ('G', 0)),
        (12, 18, ('Gb', 1)),
        # sharpness 2
        (10, 17, ('vA', 1)),
        (10, 20, ('C', 2)),
        (31, 19 + (3*31), ('Abb', 3)),
        (31, 22 + (5*31), ('Gx', 5)),
        # supersharp
        (18, 7, ('F', 0)),
        (18, 8, ('E', 0)),
        (18, 9, ('^E', 0)),
        (18, 29, ('G', 1)),
        (18, 18, ('C', 1)),
        (18, 19, ('B', 0)),
    ]
)
def test_guess_note(divisions, pitch_index, note_pair):

    notation = NOTATIONS[divisions]
    tuning = notation.tuning
    strategy = MixedRightEnharmStrategy(notation)
    notation.enharm_strategy = strategy

    note = notation.guess_note(tuning.pitch(pitch_index))
    expected = notation.note(*note_pair)
    assert note.is_notated_same(expected)
    assert note.pitch_index == pitch_index


@pytest.mark.parametrize(
    'divisions, pitch_index_a, pitch_index_b, name',
    [
        # sharpness -2
        (11, 9, 10, ('A', -2)),
        (11, 5, 4, ('M', -2)),
        # sharpness -1
        (9, 12, 13, ('M', 2)),
        # sharpness 0
        (7, 7, 16, ('P', 10)),
        (14, 4, 5, ('v', 2)),
        (28, 27, 31, ('P', 2)),
        # sharpness 1
        (5, 2, 4, ('P', 4)),
        (5, 3, 7, ('M', 6)),
        (12, 1, 20, ('P', 12)),
        # sharpness 2
        (10, 17, 18, ('^', 1)),
        (10, 20, 39, ('v', 15)),
        (31, 10 + (3*31), 19 + (3*31), ('dd', 4)),
        (31, 9 + (3*31), 22 + (5*31), ('P', 18)),
        # supersharp
        (18, 7, 8, ('m', -2)),
        (18, 9, 28, ('vvm', 10)),
        (18, 18, 19, ('m', -2)),
    ]
)
def test_guess_note_interval(divisions,
                             pitch_index_a,
                             pitch_index_b,
                             name):

    notation = NOTATIONS[divisions]
    tuning = notation.tuning
    strategy = MixedRightEnharmStrategy(notation)
    notation.enharm_strategy = strategy

    pitch_a = tuning.pitch(pitch_index_a)
    pitch_b = tuning.pitch(pitch_index_b)
    pitch_interval = pitch_a.interval(pitch_b)

    note_interval = notation.guess_note_interval(pitch_interval)
    assert note_interval.shorthand_name == name
    assert note_interval.pitch_diff == (pitch_index_b - pitch_index_a)


@pytest.mark.parametrize(
    'divisions, pitch_indices, note_pairs',
    [
        # sharpness -2
        (
            11,
            [9, 10, 14, 17],
            [('C#', 1), ('Bb', 0), ('F#', 1), ('G', 1)],
        ),
        (
            11,
            [7, 8, 11, 15],
            [('A', 0), ('B', 0), ('C', 1), ('Eb', 1)],
        ),
        # sharpness -1
        (
            9,
            [0, 3, 6, 8, 11],
            [('C', 0), ('Eb', 0), ('A', 0), ('Bb', 0), ('E', 1)],
        ),
        (
            9,
            [2, 3, 7, 8, 14],
            [('E', 0), ('Eb', 0), ('B', 0), ('Bb', 0), ('G', 1)],
        ),
        # sharpness 0
        (
            7,
            [2, 3, 7, 8, 14],
            [('E', 0), ('F', 0), ('C', 1), ('D', 1), ('C', 2)],
        ),
        (
            14,
            [2, 4, 7, 9, 13],
            [('D', 0), ('E', 0), ('vG', 0), ('vA', 0), ('vC', 1)],
        ),
        # sharpness 1
        (
            5,
            [1, 3, 4, 6, 8, 11],
            [('D', 0), ('G', 0), ('A', 0), ('D', 1), ('G', 1), ('D', 2)],
        ),
        (
            12,
            [4, 6, 10, 11, 15, 19],
            [('E', 0), ('Gb', 0), ('Bb', 0), ('B', 0), ('Eb', 1), ('G', 1)],
        ),
        # sharpness 2
        (
            10,
            [2, 4, 5, 6, 10, 11],
            [('D', 0), ('E', 0), ('vG', 0), ('G', 0), ('C', 1), ('vD', 1)],
        ),
        (
            31,
            [4, 6, 13, 18, 22, 32],
            [('Cx', 0), ('Ebb', 0), ('F', 0), ('G', 0), ('Gx', 0), ('Dbb', 1)],
        ),
        (
            31,
            [0, 5, 12, 19, 20, 35],
            [('C', 0), ('D', 0), ('E#', 0), ('Abb', 0), ('G#', 0), ('Cx', 1)],
        ),
        # supersharp
        (
            18,
            [4, 6, 12, 19, 20, 30],
            [('D', 0), ('vF', 0), ('^G', 0), ('B', 0), ('^B', 0), ('^G', 1)],
        ),
    ]
)
def test_guess_note_scale(divisions, pitch_indices, note_pairs):

    notation = NOTATIONS[divisions]
    tuning = notation.tuning
    strategy = MixedRightEnharmStrategy(notation)
    notation.enharm_strategy = strategy

    note_scale = notation.guess_note_scale(
        tuning.scale(
            [tuning.pitch(pitch_index) for pitch_index in pitch_indices]
        )
    )
    expected = notation.scale(
        [notation.note(*note_pair) for note_pair in note_pairs]
    )
    assert note_scale.is_notated_same(expected)
    assert [p.pitch_index for p in note_scale.pitch_scale] == pitch_indices


@pytest.mark.parametrize(
    'divisions, note_pair_a, pitch_diff, note_pair_b',
    [
        # sharpness -2
        (11, ('D', 2), 9, ('Bb', 2)),
        (11, ('C#', 3), 2, ('C', 3)),
        # sharpness -1
        (9, ('G', 0), 3, ('Bb', 0)),
        # sharpness 0
        (7, ('G', 2), 10, ('C', 4)),
        (7, ('G', 2), -5, ('B', 1)),
        (14, ('E', 5), 1, ('vF', 5)),
        (28, ('F', 0), 6, ('vvA', 0)),
        # sharpness 1
        (5, ('E', 1), 1, ('G', 1)),
        (5, ('D', 4), 9, ('C', 6)),
        (12, ('D', 2), 13, ('Eb', 3)),
        (12, ('D', 2), -2, ('C', 2)),
        # sharpness 2
        (10, ('F#', 2), 3, ('vC', 3)),
        (10, ('A', 0), 2, ('C', 1)),
        (31, ('E', 2), 37, ('Gb', 3)),
        (31, ('^G', 1), 1, ('G#', 1)),
        # supersharp
        (18, ('D', 2), 1, ('^D', 2)),
        (18, ('D', 2), 3, ('F', 2)),
    ]
)
def test_note_transpose(divisions,
                        note_pair_a,
                        pitch_diff,
                        note_pair_b):

    notation = NOTATIONS[divisions]
    strategy = MixedRightEnharmStrategy(notation)
    notation.enharm_strategy = strategy

    note_a = notation.note(*note_pair_a)
    note_b = notation.note(*note_pair_b)
    assert note_a.transpose(pitch_diff).is_notated_same(note_b)
    assert note_b.pitch_index == note_a.pitch_index + pitch_diff


@pytest.mark.parametrize(
    'divisions, note_pairs_a, pitch_diff, note_pairs_b',
    [
        # sharpness -2
        (
            11,
            [('C#', 1), ('D', 1), ('G#', 1), ('A', 1)],
            5,
            [('F#', 1), ('G', 1), ('C#', 2), ('D', 2)],
        ),
        (
            11,
            [('A', 0), ('B', 0), ('C', 1), ('G#', 1)],
            10,
            [('G', 1), ('A', 1), ('Bb', 1), ('F#', 2)],
        ),
        # sharpness -1
        (
            9,
            [('Db', 0), ('F#', 0), ('G', 0), ('Cb', 1), ('E', 1)],
            8,
            [('D', 1), ('E', 1), ('F', 1), ('C', 2), ('D', 2)],
        ),
        (
            9,
            [('F#', 1), ('F', 1), ('C#', 2), ('C', 2), ('A', 2)],
            -10,
            [('E', 0), ('Eb', 0), ('B', 0), ('Bb', 0), ('G', 1)],
        ),
        # sharpness 0
        (
            7,
            [('E', 0), ('F', 0), ('C', 1), ('D', 1), ('C', 2)],
            3,
            [('A', 0), ('B', 0), ('F', 1), ('G', 1), ('F', 2)],
        ),
        (
            14,
            [('^D', 0), ('E', 0), ('vF', 0), ('^^G', 0), ('B', 0)],
            -1,
            [('D', 0), ('vE', 0), ('E', 0), ('vA', 0), ('vB', 0)],
        ),
        # sharpness 1
        (
            5,
            [('C', 0), ('Eb', 0), ('A', 0), ('G#', 1), ('D', 2)],
            8,
            [('G', 1), ('A', 1), ('E', 2), ('E', 3), ('A', 3)],
        ),
        (
            12,
            [('D', 1), ('E', 1), ('G#', 1), ('A', 1), ('C#', 2), ('F', 2)],
            -10,
            [('E', 0), ('Gb', 0), ('Bb', 0), ('B', 0), ('Eb', 1), ('G', 1)],
        ),
        # sharpness 2
        (
            10,
            [('D', 0), ('E', 0), ('^E', 0), ('G', 0), ('C', 1), ('^C', 1)],
            7,
            [('vC', 1), ('vD', 1), ('D', 1), ('vE', 1), ('vA', 1), ('A', 1)],
        ),
        (
            31,
            [('E', 0), ('F#', 0), ('A#', 0), ('B', 0), ('D#', 1), ('G', 1)],
            4,
            [('Gbb', 0), ('Abb', 0), ('Cb', 1),
             ('Dbb', 1), ('Fb', 1), ('Gx', 1)],
        ),
        (
            31,
            [('C', 0), ('D', 0), ('^^E', 0), ('^G', 0), ('G#', 0), ('^F', 1)],
            9,
            [('Dx', 0), ('Gbb', 0), ('Ab', 0), ('B', 0), ('Cb', 1), ('A', 1)],
        ),
        # supersharp
        (
            18,
            [('F#', 0), ('F', 0), ('B', 0), ('^D', 1), ('E', 1), ('C#', 2)],
            5,
            [('^G', 0), ('vC', 1), ('vF', 1),
             ('vG', 1), ('vvA', 1), ('vG', 2)],
        ),
    ]
)
def test_note_scale_transpose(
    divisions,
    note_pairs_a,
    pitch_diff,
    note_pairs_b
):

    notation = NOTATIONS[divisions]
    strategy = MixedRightEnharmStrategy(notation)
    notation.enharm_strategy = strategy

    scale_a = notation.scale(
        [notation.note(*note_pair) for note_pair in note_pairs_a]
    )
    scale_b = notation.scale(
        [notation.note(*note_pair) for note_pair in note_pairs_b]
    )
    assert scale_a.transpose(pitch_diff).is_notated_same(scale_b)

    for i, note_b in enumerate(scale_b):
        assert note_b.pitch_index == scale_a[i].pitch_index + pitch_diff


@pytest.mark.parametrize(
    'divisions, note_pairs_a, note_pairs_b',
    [
        # sharpness -2
        (
            11,
            [('C#', 1), ('D#', 1), ('F#', 1), ('G', 1)],
            [('C', 0), ('D', 0), ('E', 0), ('Eb', 0),
             ('F', 0), ('A', 0), ('B', 0)],
        ),
        (
            11,
            [('A', 0), ('B', 0), ('C', 1), ('G#', 1)],
            [('D', 0), ('E', 0), ('F#', 0), ('F', 0),
             ('G', 0), ('C#', 1), ('Bb', 0)],
        ),
        # sharpness -1
        (
            9,
            [('C', 0), ('F#', 0), ('A', 0), ('C#', 1), ('E', 1)],
            [('D', 0), ('F', 0), ('G', 0), ('B', 0)],
        ),
        (
            9,
            [('E', 0), ('F#', 0), ('B', 0), ('C#', 1), ('G', 1)],
            [('C', 0), ('D', 0), ('F', 0), ('A', 0)],
        ),
        # sharpness 0
        (
            7,
            [('E', 0), ('D', 1), ('C', 2)],
            [('F', 0), ('G', 0), ('A', 0), ('B', 0)],
        ),
        (
            14,
            [('D', 0), ('E', 0), ('vG', 0), ('vA', 0), ('vC', 0)],
            [('C', 0), ('vD', 0), ('vE', 0), ('vF', 0), ('F', 0),
             ('G', 0), ('A', 0), ('vB', 0), ('B', 0)],
        ),
        # sharpness 1
        (
            5,
            [('D', 1), ('G', 1), ('A', 2)],
            [('C', 0), ('E', 0)],
        ),
        (
            12,
            [('E', 0), ('F#', 3), ('A#', 0), ('B', 0), ('D#', 1), ('G', 1)],
            [('C', 0), ('Db', 0), ('D', 0), ('F', 0), ('Ab', 0), ('A', 0)],
        ),
        # sharpness 2
        (
            10,
            [('D', 0), ('E', 0), ('^E', 0), ('G', 0), ('C', 1), ('^C', 1)],
            [('vE', 0), ('vA', 0), ('A', 0), ('vC', 1)],
        ),
        (
            31,
            [('C', 0), ('Fx', 2), ('A#', 0), ('B#', 0), ('D', 1), ('Gx', 1)],
            [('Dbb', 0), ('C#', 0), ('Db', 0), ('Cx', 0), ('Ebb', 0),
             ('D#', 0), ('Eb', 0), ('Dx', 0), ('E', 0), ('Fb', 0),
             ('E#', 0), ('F', 0), ('Gbb', 0), ('F#', 0), ('Gb', 0),
             ('G', 0), ('Abb', 0), ('G#', 0), ('Ab', 0), ('A', 0),
             ('Bbb', 0), ('Bb', 0), ('Ax', 0), ('B', 0), ('Cb', 1)],
        ),
        # supersharp
        (
            18,
            [('F#', 0), ('F', 0), ('B', 0), ('^D', 1), ('E', 1), ('C#', 2)],
            [('C', 0), ('^B', -1), ('vD', 0), ('D', 0), ('vF', 0),
             ('^E', 0), ('vG', 0), ('G', 0), ('vvA', 0), ('vA', 0),
             ('A', 0), ('^A', 0), ('vC', 1)],
        ),
    ]
)
def test_note_scale_pcs_complement(
    divisions,
    note_pairs_a,
    note_pairs_b
):

    notation = NOTATIONS[divisions]
    strategy = MixedRightEnharmStrategy(notation)
    notation.enharm_strategy = strategy

    scale_a = notation.scale(
        [notation.note(*note_pair) for note_pair in note_pairs_a]
    )
    scale_b = notation.scale(
        [notation.note(*note_pair) for note_pair in note_pairs_b]
    )
    assert scale_a.pcs_complement().is_notated_same(scale_b)
