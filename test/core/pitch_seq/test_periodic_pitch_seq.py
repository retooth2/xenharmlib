import pytest
from xenharmlib.core.frequencies import FrequencyRatio
from xenharmlib.core.tunings import EDTuning
from xenharmlib.core.pitch_seq import PeriodicPitchSeq
from xenharmlib.exc import IncompatibleOriginContexts

edo12 = EDTuning(12, FrequencyRatio(2))
edo24 = EDTuning(24, FrequencyRatio(2))
edo31 = EDTuning(31, FrequencyRatio(2))
ed13_3 = EDTuning(13, FrequencyRatio(3))


@pytest.mark.parametrize(
    'tuning, pi_list, n_pi_list, bi_diff',
    [
        (edo12, [7, 13, 19, 24], [7+24, 13+24, 19+24, 24+24], 2),
        (edo12, [9, 12, 14, 15], [9, 12, 14, 15], 0),
        (edo31, [13, 39, 48, 65], [13-31, 39-31, 48-31, 65-31], -1)
    ]
)
def test_transpose_bi_index(tuning, pi_list, n_pi_list, bi_diff):
    """
    Test if transpose_bi_index method works correctly
    """

    seq = tuning.index_seq(pi_list)
    expected = tuning.index_seq(n_pi_list)
    assert seq.transpose_bi_index(bi_diff) == expected


@pytest.mark.parametrize(
    'tuning, pitch_indices, pc_indices',
    [
        (edo12, [3, 5, 9, 15, 19, 20], [3, 5, 9, 3, 7, 8]),
        (edo31, [19, 20, 36, 51, 58], [19, 20, 5, 20, 27]),
    ]
)
def test_pc_indices(tuning, pitch_indices, pc_indices):
    """
    Test if pc_indices property works correctly
    """

    pitches = [
        tuning.pitch(pi) for pi in pitch_indices
    ]

    seq = tuning.seq(pitches)
    assert seq.pc_indices == pc_indices


@pytest.mark.parametrize(
    'tuning, input_pi_a, input_pi_b, expected',
    [
        (edo12, [5, 7, 8], [5, 7, 8], True),
        (edo12, [5, 7, 8], [5, 7, 20], True),
        (edo12, [8, 7], [5, 8, 19], False),
        (edo12, [5, 8, 7], [5, 8], False),
        (edo24, [1, 11, 12], [25, 35, 36], True),
        (edo31, [3, 11, 64], [1, 9, 12], False),
        (edo12, [2, 6, 9], [6, 9, 14], False),
        (ed13_3, [3, 11, 20], [], False),
        (ed13_3, [], [3, 11, 20], False),
    ]
)
def test_is_equivalent(tuning, input_pi_a, input_pi_b, expected):
    """
    Test if is_equivalent method works correctly
    """

    seq_a = PeriodicPitchSeq(
        tuning,
        [tuning.pitch(pi) for pi in input_pi_a]
    )

    seq_b = PeriodicPitchSeq(
        tuning,
        [tuning.pitch(pi) for pi in input_pi_b]
    )

    assert seq_a.is_equivalent(seq_b) == expected


@pytest.mark.parametrize(
    'tuning_a, input_pi_a, tuning_b, input_pi_b, expected',
    [
        (edo12, [0, 4, 7], edo24, [0, 8, 14], True),
        (edo12, [5, 8, 7], edo24, [10, 16, 14], True),
        (edo12, [5, 8, 7], edo24, [34, 40, 38], True),
        (edo12, [5, 8, 7], edo24, [38, 40, 58], False),
        (edo12, [8, 7], edo24, [34, 38, 19], False),
        (edo12, [8, 7], edo31, [34, 38, 19], False),
    ]
)
def test_is_equivalent_different_tunings(
    tuning_a, input_pi_a, tuning_b, input_pi_b, expected
):
    """
    Test if is_equivalent method works correctly
    if sequences are from different tunings with
    same equivalency interval
    """

    seq_a = PeriodicPitchSeq(
        tuning_a,
        [tuning_a.pitch(pi) for pi in input_pi_a]
    )

    seq_b = PeriodicPitchSeq(
        tuning_b,
        [tuning_b.pitch(pi) for pi in input_pi_b]
    )

    assert seq_a.is_equivalent(seq_b) == expected


def test_is_equivalent_incompatible_origin_contexts():
    """
    Test if is_equivalent method fails
    if sequences are from tunings with
    different equivalency interval
    """

    ed12_3 = EDTuning(12, FrequencyRatio(3))
    tunings = edo12, edo24, edo31

    for tuning in tunings:

        seq_a = PeriodicPitchSeq(tuning)
        seq_b = PeriodicPitchSeq(ed12_3)

        with pytest.raises(IncompatibleOriginContexts) as exc_info:
            seq_a.is_equivalent(seq_b)

        assert exc_info.value.args[0] == (
            'Equivalency can only be tested for sequences from tunings '
            'with the same equivalency interval'
        )
