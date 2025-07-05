import pytest
from xenharmlib import EDOTuning
from xenharmlib import UpDownNotation
from xenharmlib import setc

edo12 = EDOTuning(12)
n_edo12 = UpDownNotation(edo12)


@pytest.mark.parametrize(
    'tuning, input_scale_pi, output_scale_pi, output_pci',
    [
        # no tie break necessary
        (
            edo12,
            [1, 5, 7, 10],
            [5, 7, 10, 13],
            [5, 7, 10, 1]
        ),
        # standard tie break possible + different
        # results between rahn and forte method
        (
            edo12,
            [2, 3, 7, 11],
            [11, 14, 15, 19],
            [11, 2, 3, 7],
        ),
        (
            edo12,
            [11, 14, 15, 19],
            [11, 14, 15, 19],
            [11, 2, 3, 7],
        ),
        (
            edo12,
            [14, 15, 19, 23],
            [11, 14, 15, 19],
            [11, 2, 3, 7],
        ),
        # lexicographic tie break necessary
        (
            edo12,
            [0, 1, 4, 5, 8, 9],
            [0, 1, 4, 5, 8, 9],
            [0, 1, 4, 5, 8, 9],
        ),
        (
            edo12,
            [1, 4, 5, 8, 9, 12],
            [0, 1, 4, 5, 8, 9],
            [0, 1, 4, 5, 8, 9],
        ),
    ]
)
def test_nf_forte_pitch(
    tuning, input_scale_pi, output_scale_pi, output_pci
):
    """
    Test if nf_forte works on the pitch layer
    """

    input_scale = tuning.index_scale(input_scale_pi)
    output_scale = tuning.index_scale(output_scale_pi)

    n_scale = setc.nf_forte(input_scale)
    assert n_scale == output_scale
    assert n_scale.pc_indices == output_pci


def test_nf_forte_non_period_normalized():
    """
    Test if nf_forte fails on non-period normalized scales
    """

    scale = edo12.index_scale([0, 2, 4, 6, 9, 11, 13])

    with pytest.raises(ValueError) as exc_info:
        setc.nf_forte(scale)

    assert exc_info.value.args[0] == (
        'nf_forte is only defined on period normalized scales'
    )

    scale = n_edo12.pc_scale(['C', 'D', 'F', 'G', 'A', 'B', 'C'])

    with pytest.raises(ValueError) as exc_info:
        setc.nf_forte(scale)

    assert exc_info.value.args[0] == (
        'nf_forte is only defined on period normalized scales'
    )


@pytest.mark.parametrize(
    'tuning, input_scale_pi, output_scale_pi, output_pci',
    [
        # no tie break necessary
        (
            edo12,
            [1, 5, 7, 10],
            [5, 7, 10, 13],
            [5, 7, 10, 1]
        ),
        # standard tie break possible + different
        # results between rahn and forte method
        (
            edo12,
            [2, 3, 7, 11],
            [11, 14, 15, 19],
            [11, 2, 3, 7]
        ),
        (
            edo12,
            [14, 15, 19, 23],
            [11, 14, 15, 19],
            [11, 2, 3, 7]
        ),
        (
            # lexicographic tie break necessary
            edo12,
            [0, 1, 4, 5, 8, 9],
            [0, 1, 4, 5, 8, 9],
            [0, 1, 4, 5, 8, 9],
        ),
        (
            edo12,
            [1, 4, 5, 8, 9, 12],
            [0, 1, 4, 5, 8, 9],
            [0, 1, 4, 5, 8, 9],
        ),
    ]
)
def test_nf_rahn_pitch(
    tuning, input_scale_pi, output_scale_pi, output_pci
):
    """
    Test if nf_rahn works on the pitch layer
    """

    input_scale = tuning.index_scale(input_scale_pi)
    output_scale = tuning.index_scale(output_scale_pi)

    n_scale = setc.nf_rahn(input_scale)
    assert n_scale == output_scale
    assert n_scale.pc_indices == output_pci


def test_nf_rahn_non_period_normalized():
    """
    Test if nf_rahn fails on non-period normalized scales
    """

    scale = edo12.index_scale([0, 2, 4, 6, 9, 11, 13])

    with pytest.raises(ValueError) as exc_info:
        setc.nf_rahn(scale)

    assert exc_info.value.args[0] == (
        'nf_rahn is only defined on period normalized scales'
    )

    scale = n_edo12.pc_scale(['C', 'D', 'F', 'G', 'A', 'B', 'C'])

    with pytest.raises(ValueError) as exc_info:
        setc.nf_rahn(scale)

    assert exc_info.value.args[0] == (
        'nf_rahn is only defined on period normalized scales'
    )
