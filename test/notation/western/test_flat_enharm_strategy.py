import pytest
from xenharmlib import WesternNotation
from xenharmlib.notation.western import FlatEnharmStrategy


def test_nat_index_order():

    notation = WesternNotation()
    tuning = notation.tuning
    strategy = FlatEnharmStrategy(notation)
    notation.enharm_strategy = strategy

    note_scale = notation.guess_note_scale(
        tuning.scale(tuning.pitch_range(0, 12))
    )

    for first, second in zip(note_scale, note_scale[1:]):
        assert first.nat_index <= second.nat_index


@pytest.mark.parametrize(
    'pitch_index, note_pair',
    [
        (18, ('Gb', 1)),
        (1, ('Db', 0)),
        (8, ('Ab', 0)),
    ]
)
def test_guess_note(pitch_index, note_pair):

    notation = WesternNotation()
    tuning = notation.tuning
    strategy = FlatEnharmStrategy(notation)
    notation.enharm_strategy = strategy

    note = notation.guess_note(tuning.pitch(pitch_index))
    expected = notation.note(*note_pair)
    assert note.is_notated_same(expected)
    assert note.pitch_index == pitch_index


@pytest.mark.parametrize(
    'pitch_index_a, pitch_index_b, name',
    [
        (1, 20, ('P', 12)),
        (0, 7, ('P', 5)),
        (0, 6, ('d', 5)),
    ]
)
def test_guess_note_interval(pitch_index_a,
                             pitch_index_b,
                             name):

    notation = WesternNotation()
    tuning = notation.tuning
    strategy = FlatEnharmStrategy(notation)
    notation.enharm_strategy = strategy

    pitch_diff = pitch_index_b - pitch_index_a
    pitch_a = tuning.pitch(pitch_index_a)
    pitch_b = tuning.pitch(pitch_index_b)
    pitch_interval = pitch_a.interval(pitch_b)

    note_interval_a = notation.guess_note_interval(pitch_interval)
    note_interval_b = notation.diff_interval(pitch_diff)

    assert note_interval_a.shorthand_name == name
    assert note_interval_a.pitch_diff == pitch_diff
    assert note_interval_b.shorthand_name == name
    assert note_interval_b.pitch_diff == pitch_diff


@pytest.mark.parametrize(
    'pitch_indices, note_pairs',
    [
        (
            [4, 6, 10, 11, 15, 19],
            [('E', 0), ('Gb', 0), ('Bb', 0), ('B', 0), ('Eb', 1), ('G', 1)],
        ),
    ]
)
def test_guess_note_scale(pitch_indices, note_pairs):

    notation = WesternNotation()
    tuning = notation.tuning
    strategy = FlatEnharmStrategy(notation)
    notation.enharm_strategy = strategy

    note_scale_a = notation.guess_note_scale(
        tuning.scale(
            [tuning.pitch(pitch_index) for pitch_index in pitch_indices]
        )
    )
    note_scale_b = notation.index_scale(pitch_indices)

    expected = notation.scale(
        [notation.note(*note_pair) for note_pair in note_pairs]
    )
    assert note_scale_a.is_notated_same(expected)
    assert note_scale_b.is_notated_same(expected)
    assert [p.pitch_index for p in note_scale_a.pitch_scale] == pitch_indices
    assert [p.pitch_index for p in note_scale_b.pitch_scale] == pitch_indices


@pytest.mark.parametrize(
    'pitch_diffs, sh_names',
    [
        (
            [4, 6, 4, 5, 10, 7],
            [('M', 3), ('d', 5), ('M', 3), ('P', 4), ('m', 7), ('P', 5)],
        ),
    ]
)
def test_guess_note_interval_seq(pitch_diffs, sh_names):

    notation = WesternNotation()
    tuning = notation.tuning
    strategy = FlatEnharmStrategy(notation)
    notation.enharm_strategy = strategy

    note_interval_seq_a = notation.guess_note_interval_seq(
        tuning.interval_seq(
            [tuning.diff_interval(pitch_diff) for pitch_diff in pitch_diffs]
        )
    )
    note_interval_seq_b = notation.diff_interval_seq(pitch_diffs)

    expected = notation.interval_seq(
        [notation.shorthand_interval(*sh_name) for sh_name in sh_names]
    )
    assert note_interval_seq_a.is_notated_same(expected)
    assert note_interval_seq_b.is_notated_same(expected)

    assert [i.pitch_diff for i in note_interval_seq_a] == pitch_diffs
    assert [i.pitch_diff for i in note_interval_seq_b] == pitch_diffs


@pytest.mark.parametrize(
    'pitch_diffs, sh_names',
    [
        (
            [0, 6, 4, 5, 10, 7],
            [('P', 1), ('d', 5), ('M', 3), ('P', 4), ('m', 7), ('P', 5)],
        ),
    ]
)
def test_guess_note_interval_fan(pitch_diffs, sh_names):

    notation = WesternNotation()
    tuning = notation.tuning
    strategy = FlatEnharmStrategy(notation)
    notation.enharm_strategy = strategy

    note_interval_fan_a = notation.guess_note_interval_fan(
        tuning.interval_fan(
            [tuning.diff_interval(pitch_diff) for pitch_diff in pitch_diffs]
        )
    )
    note_interval_fan_b = notation.diff_interval_fan(pitch_diffs)

    expected = notation.interval_fan(
        [notation.shorthand_interval(*sh_name) for sh_name in sh_names]
    )
    assert note_interval_fan_a.is_notated_same(expected)
    assert note_interval_fan_b.is_notated_same(expected)
    assert [i.pitch_diff for i in note_interval_fan_a] == pitch_diffs
    assert [i.pitch_diff for i in note_interval_fan_b] == pitch_diffs


@pytest.mark.parametrize(
    'pitch_indices, note_pairs',
    [
        (
            [4, 6, 10, 11, 15, 19],
            [('E', 0), ('Gb', 0), ('Bb', 0), ('B', 0), ('Eb', 1), ('G', 1)],
        ),
    ]
)
def test_guess_note_seq(pitch_indices, note_pairs):

    notation = WesternNotation()
    tuning = notation.tuning
    strategy = FlatEnharmStrategy(notation)
    notation.enharm_strategy = strategy

    note_seq_a = notation.guess_note_seq(
        tuning.seq(
            [tuning.pitch(pitch_index) for pitch_index in pitch_indices]
        )
    )
    note_seq_b = notation.index_seq(pitch_indices)

    expected = notation.seq(
        [notation.note(*note_pair) for note_pair in note_pairs]
    )
    assert note_seq_a.is_notated_same(expected)
    assert note_seq_b.is_notated_same(expected)
    assert [p.pitch_index for p in note_seq_a] == pitch_indices
    assert [p.pitch_index for p in note_seq_b] == pitch_indices


@pytest.mark.parametrize(
    'note_pair_a, pitch_diff, note_pair_b',
    [
        (('D', 2), 13, ('Eb', 3)),
        (('D', 2), -2, ('C', 2)),
    ]
)
def test_note_transpose(note_pair_a,
                        pitch_diff,
                        note_pair_b):

    notation = WesternNotation()
    strategy = FlatEnharmStrategy(notation)
    notation.enharm_strategy = strategy

    note_a = notation.note(*note_pair_a)
    note_b = notation.note(*note_pair_b)
    assert note_a.transpose(pitch_diff).is_notated_same(note_b)
    assert note_b.pitch_index == note_a.pitch_index + pitch_diff


@pytest.mark.parametrize(
    'note_pairs_a, pitch_diff, note_pairs_b',
    [
        (
            [('D', 1), ('E', 1), ('G#', 1), ('A', 1), ('C#', 2), ('F', 2)],
            -10,
            [('E', 0), ('Gb', 0), ('Bb', 0), ('B', 0), ('Eb', 1), ('G', 1)],
        ),
    ]
)
def test_note_scale_transpose(
    note_pairs_a,
    pitch_diff,
    note_pairs_b
):

    notation = WesternNotation()
    strategy = FlatEnharmStrategy(notation)
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
    'note_pairs_a, note_pairs_b',
    [
        (
            [('E', 0), ('F#', 3), ('A#', 0), ('B', 0), ('D#', 1), ('G', 1)],
            [('C', 0), ('Db', 0), ('D', 0), ('F', 0), ('Ab', 0), ('A', 0)],
        ),
    ]
)
def test_note_scale_pcs_complement(
    note_pairs_a,
    note_pairs_b
):

    notation = WesternNotation()
    strategy = FlatEnharmStrategy(notation)
    notation.enharm_strategy = strategy

    scale_a = notation.scale(
        [notation.note(*note_pair) for note_pair in note_pairs_a]
    )
    scale_b = notation.scale(
        [notation.note(*note_pair) for note_pair in note_pairs_b]
    )
    assert scale_a.pcs_complement().is_notated_same(scale_b)
