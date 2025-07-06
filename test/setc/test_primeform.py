import pytest
from xenharmlib import EDOTuning
from xenharmlib import UpDownNotation
from xenharmlib import setc

edo12 = EDOTuning(12)
n_edo12 = UpDownNotation(edo12)


@pytest.mark.parametrize(
    'transposition', range(0, 12)
)
@pytest.mark.parametrize(
    'inverted', [True, False]
)
@pytest.mark.parametrize(
    'tuning, input_scale_pi, output_scale_pi, output_pci',
    [
        # difference between rahn and forte
        (
            edo12,
            [0, 1, 3, 7, 8],
            [0, 1, 3, 7, 8],
            [0, 1, 3, 7, 8]
        ),
        (
            edo12,
            [0, 1, 2, 4, 7, 8, 9],
            [0, 1, 2, 4, 7, 8, 9],
            [0, 1, 2, 4, 7, 8, 9]
        ),
        (
            edo12,
            [0, 1, 2, 4, 5, 7, 9, 10],
            [0, 1, 2, 4, 5, 7, 9, 10],
            [0, 1, 2, 4, 5, 7, 9, 10]
        ),
        # no difference between rahn and forte
        (
            edo12,
            [1, 5, 7, 10],
            [0, 2, 5, 8],
            [0, 2, 5, 8]
        ),
        (
            edo12,
            [2, 3, 7, 11],
            [0, 1, 4, 8],
            [0, 1, 4, 8]
        ),
        (
            edo12,
            [11, 14, 15, 19],
            [0, 1, 4, 8],
            [0, 1, 4, 8]
        ),
        (
            edo12,
            [14, 15, 19, 23],
            [0, 1, 4, 8],
            [0, 1, 4, 8]
        ),
        (
            edo12,
            [0, 1, 4, 5, 8, 9],
            [0, 1, 4, 5, 8, 9],
            [0, 1, 4, 5, 8, 9]
        ),
        (
            edo12,
            [1, 4, 5, 8, 9, 12],
            [0, 1, 4, 5, 8, 9],
            [0, 1, 4, 5, 8, 9]
        ),
    ]
)
def test_primeform_forte_pitch(
    tuning,
    input_scale_pi,
    output_scale_pi,
    output_pci,
    transposition,
    inverted
):
    """
    Test if primeform_forte works on the pitch layer
    """

    input_scale = tuning.index_scale(input_scale_pi)
    output_scale = tuning.index_scale(output_scale_pi)

    # primeforms must be idempotent under rotation,
    # inversion and transposition

    for order in range(0, len(input_scale)):

        input_scale = input_scale.rotation(order)

        if inverted:
            input_scale = input_scale.reflection()

        input_scale = input_scale.transpose(transposition)

        n_scale = setc.primeform_forte(input_scale)
        assert n_scale == output_scale
        assert n_scale.pc_indices == output_pci


def test_primeform_forte_non_period_normalized():
    """
    Test if primeform_forte fails on non-period normalized scales
    """

    scale = edo12.index_scale([0, 2, 4, 6, 9, 11, 13])

    with pytest.raises(ValueError) as exc_info:
        setc.primeform_forte(scale)

    assert exc_info.value.args[0] == (
        'primeform_forte is only defined on period normalized scales'
    )

    scale = n_edo12.pc_scale(['C', 'D', 'F', 'G', 'A', 'B', 'C'])

    with pytest.raises(ValueError) as exc_info:
        setc.primeform_forte(scale)

    assert exc_info.value.args[0] == (
        'primeform_forte is only defined on period normalized scales'
    )


@pytest.mark.parametrize(
    'transposition', range(0, 12)
)
@pytest.mark.parametrize(
    'inverted', [True, False]
)
@pytest.mark.parametrize(
    'tuning, input_scale_pi, output_scale_pi, output_pci',
    [
        # difference between rahn and forte
        (
            edo12,
            [0, 1, 3, 7, 8],
            [0, 1, 5, 6, 8],
            [0, 1, 5, 6, 8]
        ),
        (
            edo12,
            [0, 1, 2, 4, 7, 8, 9],
            [0, 1, 2, 5, 6, 7, 9],
            [0, 1, 2, 5, 6, 7, 9],
        ),
        (
            edo12,
            [0, 1, 2, 4, 5, 7, 9, 10],
            [0, 1, 3, 4, 5, 7, 8, 10],
            [0, 1, 3, 4, 5, 7, 8, 10]
        ),
        # no difference between rahn and forte
        (
            edo12,
            [1, 5, 7, 10],
            [0, 2, 5, 8],
            [0, 2, 5, 8]
        ),
        (
            edo12,
            [0, 1, 2, 3, 5, 8, 9],
            [0, 1, 4, 5, 6, 7, 9],
            [0, 1, 4, 5, 6, 7, 9],
        ),
        (
            edo12,
            [12, 13, 14, 15, 17, 20, 21],
            [0, 1, 4, 5, 6, 7, 9],
            [0, 1, 4, 5, 6, 7, 9],
        ),
        (
            edo12,
            [0, 1, 4, 5, 6, 7, 9],
            [0, 1, 4, 5, 6, 7, 9],
            [0, 1, 4, 5, 6, 7, 9],
        ),
        (
            edo12,
            [0, 1, 4, 5, 8, 9],
            [0, 1, 4, 5, 8, 9],
            [0, 1, 4, 5, 8, 9]
        ),
        (
            edo12,
            [1, 4, 5, 8, 9, 12],
            [0, 1, 4, 5, 8, 9],
            [0, 1, 4, 5, 8, 9]
        ),
    ]
)
def test_primeform_rahn_pitch(
    tuning,
    input_scale_pi,
    output_scale_pi,
    output_pci,
    inverted,
    transposition
):
    """
    Test if primeform_rahn works on the pitch layer
    """

    input_scale = tuning.index_scale(input_scale_pi)
    output_scale = tuning.index_scale(output_scale_pi)

    # primeforms must be idempotent under rotation,
    # inversion and transposition

    for order in range(0, len(input_scale)):

        input_scale = input_scale.rotation(order)

        if inverted:
            input_scale = input_scale.reflection()

        input_scale = input_scale.transpose(transposition)

        n_scale = setc.primeform_rahn(input_scale)
        assert n_scale == output_scale
        assert n_scale.pc_indices == output_pci


def test_primeform_rahn_non_period_normalized():
    """
    Test if primeform_rahn fails on non-period normalized scales
    """

    scale = edo12.index_scale([0, 2, 4, 6, 9, 11, 13])

    with pytest.raises(ValueError) as exc_info:
        setc.primeform_rahn(scale)

    assert exc_info.value.args[0] == (
        'primeform_rahn is only defined on period normalized scales'
    )

    scale = n_edo12.pc_scale(['C', 'D', 'F', 'G', 'A', 'B', 'C'])

    with pytest.raises(ValueError) as exc_info:
        setc.primeform_rahn(scale)

    assert exc_info.value.args[0] == (
        'primeform_rahn is only defined on period normalized scales'
    )
