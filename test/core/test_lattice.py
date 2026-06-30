import pytest
from xenharmlib.core.frequencies import FrequencyRatio
from xenharmlib.core.lattice import Lattice


@pytest.mark.parametrize(
    'index',
    (
        (0, 0, 0, 0, 0),
        (0, 2, -1, 5, 0),
        (-1, -1, -2, -2, -3),
        (3, 4, 5, 9, 1),
    )
)
def test_contains_point(index):

    lattice_a = Lattice(
        (
            FrequencyRatio(2),
            FrequencyRatio(3),
            FrequencyRatio(5),
            FrequencyRatio(7),
            FrequencyRatio(41),
        )
    )
    lp_a = lattice_a.point(index)

    lattice_b = Lattice(
        (
            FrequencyRatio(3),
            FrequencyRatio(5),
            FrequencyRatio(7),
            FrequencyRatio(31),
            FrequencyRatio(41),
        )
    )
    lp_b = lattice_b.point(index)

    assert lattice_a.contains_point(lp_a)
    assert lattice_b.contains_point(lp_b)
    assert not lattice_a.contains_point(lp_b)
    assert not lattice_b.contains_point(lp_a)


@pytest.mark.parametrize(
    'lattice, repr_result',
    [
        (
            Lattice(
                (
                    FrequencyRatio(2),
                    FrequencyRatio(3),
                    FrequencyRatio(5),
                    FrequencyRatio(7),
                    FrequencyRatio(11),
                )
            ),
            'Lattice(2, 3, 5, 7, 11)'
        ),
        (
            Lattice(
                (
                    FrequencyRatio(2),
                    FrequencyRatio(3),
                    FrequencyRatio(5, 3),
                    FrequencyRatio(7),
                    FrequencyRatio(11),
                )
            ),
            'Lattice(2, 3, 5/3, 7, 11)'
        ),
    ]
)
def test_lattice_repr(lattice, repr_result):
    assert repr(lattice) == repr_result


def test_dim_mismatch():

    lattice = Lattice(
        (
            FrequencyRatio(2),
            FrequencyRatio(3),
            FrequencyRatio(5),
            FrequencyRatio(7),
            FrequencyRatio(29),
            FrequencyRatio(41),
        )
    )

    with pytest.raises(ValueError) as exc_info:
        lattice.point((1, 2, 3))
    assert exc_info.value.args[0] == (
        "Index vector dimensions must match base dimensions"
    )


@pytest.mark.parametrize(
    'lattice, index, repr_result',
    [
        (
            Lattice(
                (
                    FrequencyRatio(2),
                    FrequencyRatio(3),
                    FrequencyRatio(5),
                    FrequencyRatio(7),
                )
            ),
            (-1, 1, 0, 0),
            'LatticePoint(-1, 1, 0, 0)'
        ),
        (
            Lattice(
                (
                    FrequencyRatio(2),
                    FrequencyRatio(3),
                    FrequencyRatio(5),
                    FrequencyRatio(7),
                )
            ),
            (0, 1, 0, 0),
            'LatticePoint(0, 1, 0, 0)'
        ),
        (
            Lattice(
                (
                    FrequencyRatio(2),
                    FrequencyRatio(3),
                    FrequencyRatio(5),
                    FrequencyRatio(7),
                )
            ),
            (-1, 0, 0, 0),
            'LatticePoint(-1, 0, 0, 0)'
        ),
        (
            Lattice(
                (
                    FrequencyRatio(2),
                    FrequencyRatio(3),
                    FrequencyRatio(5),
                    FrequencyRatio(7),
                )
            ),
            (0, 0, 0, 0),
            'LatticePoint(0, 0, 0, 0)'
        ),
    ]
)
def test_lattice_point_repr(lattice, index, repr_result):
    point = lattice.point(index)
    assert repr(point) == repr_result


@pytest.mark.parametrize(
    'lattice, index, repr_result',
    [
        (
            Lattice(
                (
                    FrequencyRatio(2),
                    FrequencyRatio(3),
                    FrequencyRatio(5),
                    FrequencyRatio(7),
                )
            ),
            (-1, 1, 0, 0),
            '(-1, 1, 0, 0)'
        ),
        (
            Lattice(
                (
                    FrequencyRatio(2),
                    FrequencyRatio(3),
                    FrequencyRatio(5),
                    FrequencyRatio(7),
                )
            ),
            (0, 1, 0, 0),
            '(0, 1, 0, 0)'
        ),
        (
            Lattice(
                (
                    FrequencyRatio(2),
                    FrequencyRatio(3),
                    FrequencyRatio(5),
                    FrequencyRatio(7),
                )
            ),
            (-1, 0, 0, 0),
            '(-1, 0, 0, 0)'
        ),
        (
            Lattice(
                (
                    FrequencyRatio(2),
                    FrequencyRatio(3),
                    FrequencyRatio(5),
                    FrequencyRatio(7),
                )
            ),
            (0, 0, 0, 0),
            '(0, 0, 0, 0)'
        ),
    ]
)
def test_lattice_point_short_repr(lattice, index, repr_result):
    point = lattice.point(index)
    assert point.short_repr == repr_result


def test_hash_set():

    lattice_a = Lattice(
        (
            FrequencyRatio(2),
            FrequencyRatio(3),
            FrequencyRatio(5),
            FrequencyRatio(7),
            FrequencyRatio(29),
            FrequencyRatio(41),
        )
    )

    lp = lattice_a.point((0, 1, 2, 3, 4, 5))
    lp_same = lattice_a.point((0, 1, 2, 3, 4, 5))
    lp_different = lattice_a.point((2, 1, 2, 3, 4, 5))

    lattice_b = Lattice(
        (
            FrequencyRatio(2),
            FrequencyRatio(3),
            FrequencyRatio(5),
            FrequencyRatio(7),
            FrequencyRatio(31),
            FrequencyRatio(41),
        )
    )

    lp_same_diff_lattice = lattice_b.point((0, 1, 2, 3, 4, 5))

    assert set(
        [lp, lp_same, lp_same_diff_lattice, lp_different]
    ) == set(
        [lp, lp_different, lp_same_diff_lattice]
    )


def test_zero():

    lattice = Lattice(
        (
            FrequencyRatio(2),
            FrequencyRatio(3),
            FrequencyRatio(5),
            FrequencyRatio(7),
            FrequencyRatio(11),
        )
    )
    assert lattice.zero == lattice.point((0, 0, 0, 0, 0))


def test_add_different_lattice():

    lattice_a = Lattice(
        (
            FrequencyRatio(2),
            FrequencyRatio(3),
            FrequencyRatio(5),
            FrequencyRatio(7),
            FrequencyRatio(11),
        )
    )
    lattice_b = Lattice(
        (
            FrequencyRatio(2),
            FrequencyRatio(3),
            FrequencyRatio(5),
            FrequencyRatio(7),
            FrequencyRatio(17),
        )
    )

    with pytest.raises(TypeError) as exc_info:
        lattice_a.point((1, 2, 1, 0, 1)) + lattice_b.point((1, 3, 5, 5, -1))
    assert exc_info.value.args[0] == (
        "unsupported operator +: lattice points originate from "
        "different lattices"
    )


@pytest.mark.parametrize(
    'operand',
    [
        'foo',
        3,
        bool,
        3.12
    ]
)
def test_add_non_lattice_point_operand(operand):

    lattice = Lattice(
        (
            FrequencyRatio(2),
            FrequencyRatio(3),
            FrequencyRatio(5),
            FrequencyRatio(7),
            FrequencyRatio(11),
        )
    )

    with pytest.raises(TypeError) as exc_info:
        lattice.point((1, 2, 1, 0, 1)) + operand
    assert exc_info.value.args[0] == (
        f"unsupported operand type(s) for +: 'LatticePoint' and "
        f"'{type(operand).__name__}'"
    )

    with pytest.raises(TypeError) as exc_info:
        operand + lattice.point((1, 2, 1, 0, 1))
    assert exc_info.value.args[0] in {
        f"unsupported operand type(s) for +: 'LatticePoint' and "
        f"'{type(operand).__name__}'",
        f"unsupported operand type(s) for +: '{type(operand).__name__}' and "
        f"'LatticePoint'"
    }


@pytest.mark.parametrize(
    'tuple_a, tuple_b, tuple_r',
    [
        ((1, 9, 3, 5, 1), (-4, 1, -4, 11, 3), (-3, 10, -1, 16, 4)),
        ((0, 0, 0, 0, 0), (3, 9, 2, 1, -3), (3, 9, 2, 1, -3)),
    ]
)
def test_add(tuple_a, tuple_b, tuple_r):

    lattice = Lattice(
        (
            FrequencyRatio(2),
            FrequencyRatio(3),
            FrequencyRatio(5),
            FrequencyRatio(7),
            FrequencyRatio(11),
        )
    )

    a = lattice.point(tuple_a)
    b = lattice.point(tuple_b)
    r = lattice.point(tuple_r)

    assert a + b == r
    assert b + a == r


def test_sub_different_lattice():

    lattice_a = Lattice(
        (
            FrequencyRatio(2),
            FrequencyRatio(3),
            FrequencyRatio(5),
            FrequencyRatio(7),
            FrequencyRatio(11),
        )
    )
    lattice_b = Lattice(
        (
            FrequencyRatio(2),
            FrequencyRatio(3),
            FrequencyRatio(5),
            FrequencyRatio(7),
            FrequencyRatio(17),
        )
    )

    with pytest.raises(TypeError) as exc_info:
        lattice_a.point((1, 2, 1, 0, 1)) - lattice_b.point((1, 3, 5, 5, -1))
    assert exc_info.value.args[0] == (
        "unsupported operator -: lattice points originate from "
        "different lattices"
    )


@pytest.mark.parametrize(
    'operand',
    [
        'foo',
        3,
        bool,
        3.12
    ]
)
def test_sub_non_lattice_point_operand(operand):

    lattice = Lattice(
        (
            FrequencyRatio(2),
            FrequencyRatio(3),
            FrequencyRatio(5),
            FrequencyRatio(7),
            FrequencyRatio(11),
        )
    )

    with pytest.raises(TypeError) as exc_info:
        lattice.point((1, 2, 1, 0, 1)) - operand
    assert exc_info.value.args[0] == (
        f"unsupported operand type(s) for -: 'LatticePoint' and "
        f"'{type(operand).__name__}'"
    )

    with pytest.raises(TypeError) as exc_info:
        operand - lattice.point((1, 2, 1, 0, 1))
    assert exc_info.value.args[0] in {
        f"unsupported operand type(s) for -: 'LatticePoint' and "
        f"'{type(operand).__name__}'",
        f"unsupported operand type(s) for -: '{type(operand).__name__}' and "
        f"'LatticePoint'"
    }


@pytest.mark.parametrize(
    'tuple_a, tuple_b, tuple_r',
    [
        ((1, 9, 3, 5, 1), (-4, 1, -4, 11, 3), (5, 8, 7, -6, -2))
    ]
)
def test_sub(tuple_a, tuple_b, tuple_r):

    lattice = Lattice(
        (
            FrequencyRatio(2),
            FrequencyRatio(3),
            FrequencyRatio(5),
            FrequencyRatio(7),
            FrequencyRatio(11),
        )
    )

    a = lattice.point(tuple_a)
    b = lattice.point(tuple_b)
    r = lattice.point(tuple_r)

    assert a - b == r


def test_divmod_different_lattice():

    lattice_a = Lattice(
        (
            FrequencyRatio(2),
            FrequencyRatio(3),
            FrequencyRatio(5),
            FrequencyRatio(7),
            FrequencyRatio(11),
        )
    )
    lattice_b = Lattice(
        (
            FrequencyRatio(2),
            FrequencyRatio(3),
            FrequencyRatio(5),
            FrequencyRatio(7),
            FrequencyRatio(17),
        )
    )

    with pytest.raises(TypeError) as exc_info:
        divmod(
            lattice_a.point((1, 2, 1, 0, 1)), lattice_b.point((1, 3, 5, 5, -1))
        )
    assert exc_info.value.args[0] == (
        "unsupported operator __divmod__: lattice points originate from "
        "different lattices"
    )


@pytest.mark.parametrize(
    'operand',
    [
        'foo',
        3,
        bool,
        3.12
    ]
)
def test_divmod_non_lattice_point_operand(operand):

    lattice = Lattice(
        (
            FrequencyRatio(2),
            FrequencyRatio(3),
            FrequencyRatio(5),
            FrequencyRatio(7),
            FrequencyRatio(11),
        )
    )

    with pytest.raises(TypeError) as exc_info:
        divmod(lattice.point((1, 2, 1, 0, 1)), operand)
    assert exc_info.value.args[0] == (
        f"unsupported operand type(s) for __divmod__: 'LatticePoint' and "
        f"'{type(operand).__name__}'"
    )


def test_divmod_zerodiv_error():

    lattice = Lattice(
        (
            FrequencyRatio(2),
            FrequencyRatio(3),
            FrequencyRatio(5),
            FrequencyRatio(7),
            FrequencyRatio(11),
        )
    )

    with pytest.raises(ZeroDivisionError):
        divmod(lattice.point((1, 2, 3, 4, 5)), lattice.zero)


@pytest.mark.parametrize(
    'tuple_a, tuple_b, q, tuple_r',
    [
        ((0, 0, 0, 0, 0), (0, 0, 0, 0, 1), 0, (0, 0, 0, 0, 0)),
        ((8, 6, -2, 12, 18), (4, 3, -1, 6, 9), 2, (0, 0, 0, 0, 0)),
        ((8, 6, 0, 12, 18), (4, 3, -1, 6, 9), 2, (0, 0, 2, 0, 0)),
        ((80, 60, 0, 120, 180), (4, 3, -1, 6, 9), 20, (0, 0, 20, 0, 0)),
        ((6, 9, -3, 3, 0), (2, 3, -1, 1, 0), 3, (0, 0, 0, 0, 0)),
        ((6, 8, -3, 3, 0), (-2, -3, 1, -1, 0), -3, (0, -1, 0, 0, 0)),
        ((-5, -9, 3, -3, 0), (2, 3, -1, 1, 0), -3, (1, 0, 0, 0, 0)),
        ((-6, -9, 3, -3, 0), (-2, -2, 1, -1, 0), 3, (0, -3, 0, 0, 0)),
    ]
)
def test_divmod(tuple_a, tuple_b, q, tuple_r):

    lattice = Lattice(
        (
            FrequencyRatio(2),
            FrequencyRatio(3),
            FrequencyRatio(5),
            FrequencyRatio(7),
            FrequencyRatio(11),
        )
    )

    a = lattice.point(tuple_a)
    b = lattice.point(tuple_b)
    r = lattice.point(tuple_r)

    assert divmod(a, b) == (q, r)
    assert a == q * b + r


def test_mod_different_lattice():

    lattice_a = Lattice(
        (
            FrequencyRatio(2),
            FrequencyRatio(3),
            FrequencyRatio(5),
            FrequencyRatio(7),
            FrequencyRatio(11),
        )
    )
    lattice_b = Lattice(
        (
            FrequencyRatio(2),
            FrequencyRatio(3),
            FrequencyRatio(5),
            FrequencyRatio(7),
            FrequencyRatio(17),
        )
    )

    with pytest.raises(TypeError) as exc_info:
        lattice_a.point((1, 2, 1, 0, 1)) % lattice_b.point((1, 3, 5, 5, -1))
    assert exc_info.value.args[0] == (
        "unsupported operator %: lattice points originate from "
        "different lattices"
    )


@pytest.mark.parametrize(
    'operand',
    [
        'foo',
        3,
        bool,
        3.12
    ]
)
def test_mod_non_lattice_point_operand(operand):

    lattice = Lattice(
        (
            FrequencyRatio(2),
            FrequencyRatio(3),
            FrequencyRatio(5),
            FrequencyRatio(7),
            FrequencyRatio(11),
        )
    )

    with pytest.raises(TypeError) as exc_info:
        lattice.point((1, 2, 1, 0, 1)) % operand
    assert exc_info.value.args[0] == (
        f"unsupported operand type(s) for %: 'LatticePoint' and "
        f"'{type(operand).__name__}'"
    )

    with pytest.raises(TypeError) as exc_info:
        operand % lattice.point((1, 2, 1, 0, 1))


def test_mod_zerodiv_error():

    lattice = Lattice(
        (
            FrequencyRatio(2),
            FrequencyRatio(3),
            FrequencyRatio(5),
            FrequencyRatio(7),
            FrequencyRatio(11),
        )
    )

    with pytest.raises(ZeroDivisionError):
        lattice.point((1, 2, 3, 4, 5)) % lattice.zero


@pytest.mark.parametrize(
    'tuple_a, tuple_b, tuple_r',
    [
        ((8, 6, -2, 12, 18), (4, 3, -1, 6, 9), (0, 0, 0, 0, 0)),
        ((8, 6, 0, 12, 18), (4, 3, -1, 6, 9), (0, 0, 2, 0, 0)),
        ((80, 60, 0, 120, 180), (4, 3, -1, 6, 9), (0, 0, 20, 0, 0)),
        ((6, 9, -3, 3, 0), (2, 3, -1, 1, 0), (0, 0, 0, 0, 0)),
        ((6, 8, -3, 3, 0), (-2, -3, 1, -1, 0), (0, -1, 0, 0, 0)),
        ((-5, -9, 3, -3, 0), (2, 3, -1, 1, 0), (1, 0, 0, 0, 0)),
        ((-6, -9, 3, -3, 0), (-2, -2, 1, -1, 0), (0, -3, 0, 0, 0)),
    ]
)
def test_mod(tuple_a, tuple_b, tuple_r):

    lattice = Lattice(
        (
            FrequencyRatio(2),
            FrequencyRatio(3),
            FrequencyRatio(5),
            FrequencyRatio(7),
            FrequencyRatio(11),
        )
    )

    result = (lattice.point(tuple_a) % lattice.point(tuple_b))
    assert result == lattice.point(tuple_r)


def test_floordiv_different_lattice():

    lattice_a = Lattice(
        (
            FrequencyRatio(2),
            FrequencyRatio(3),
            FrequencyRatio(5),
            FrequencyRatio(7),
            FrequencyRatio(11),
        )
    )
    lattice_b = Lattice(
        (
            FrequencyRatio(2),
            FrequencyRatio(3),
            FrequencyRatio(5),
            FrequencyRatio(7),
            FrequencyRatio(17),
        )
    )

    with pytest.raises(TypeError) as exc_info:
        lattice_a.point((1, 2, 1, 0, 1)) // lattice_b.point((1, 3, 5, 5, -1))
    assert exc_info.value.args[0] == (
        "unsupported operator //: lattice points originate from "
        "different lattices"
    )


@pytest.mark.parametrize(
    'operand',
    [
        'foo',
        3,
        bool,
        3.12
    ]
)
def test_floordiv_non_lattice_point_operand(operand):

    lattice = Lattice(
        (
            FrequencyRatio(2),
            FrequencyRatio(3),
            FrequencyRatio(5),
            FrequencyRatio(7),
            FrequencyRatio(11),
        )
    )

    with pytest.raises(TypeError) as exc_info:
        lattice.point((1, 2, 1, 0, 1)) // operand
    assert exc_info.value.args[0] == (
        f"unsupported operand type(s) for //: 'LatticePoint' and "
        f"'{type(operand).__name__}'"
    )

    with pytest.raises(TypeError) as exc_info:
        operand // lattice.point((1, 2, 1, 0, 1))
    assert exc_info.value.args[0] in {
        f"unsupported operand type(s) for //: 'LatticePoint' and "
        f"'{type(operand).__name__}'",
        f"unsupported operand type(s) for //: '{type(operand).__name__}' and "
        f"'LatticePoint'"
    }


def test_floordiv_zerodiv_error():

    lattice = Lattice(
        (
            FrequencyRatio(2),
            FrequencyRatio(3),
            FrequencyRatio(5),
            FrequencyRatio(7),
            FrequencyRatio(11),
        )
    )

    with pytest.raises(ZeroDivisionError):
        lattice.point((1, 2, 3, 4, 5)) // lattice.zero


@pytest.mark.parametrize(
    'tuple_a, tuple_b, quotient',
    [
        ((8, 6, -2, 12, 18), (4, 3, -1, 6, 9), 2),
        ((8, 6, 0, 12, 18), (4, 3, -1, 6, 9), 2),
        ((80, 60, 0, 120, 180), (4, 3, -1, 6, 9), 20),
        ((6, 9, -3, 3, 0), (2, 3, -1, 1, 0), 3),
        ((6, 8, -3, 3, 0), (-2, -3, 1, -1, 0), -3),
        ((-5, -9, 3, -3, 0), (2, 3, -1, 1, 0), -3),
        ((-6, -9, 3, -3, 0), (-2, -2, 1, -1, 0), 3),
    ]
)
def test_floordiv(tuple_a, tuple_b, quotient):

    lattice = Lattice(
        (
            FrequencyRatio(2),
            FrequencyRatio(3),
            FrequencyRatio(5),
            FrequencyRatio(7),
            FrequencyRatio(11),
        )
    )

    result = (lattice.point(tuple_a) // lattice.point(tuple_b))
    assert result == quotient


def test_mul_lattice():

    lattice = Lattice(
        (
            FrequencyRatio(2),
            FrequencyRatio(3),
            FrequencyRatio(5),
            FrequencyRatio(7),
            FrequencyRatio(11),
        )
    )

    with pytest.raises(TypeError) as exc_info:
        lattice.point((1, 2, 1, 0, 1)) * lattice.point((1, 3, 5, 5, -1))
    assert exc_info.value.args[0] == (
        "unsupported operand type(s) for *: 'LatticePoint' and 'LatticePoint'"
    )


@pytest.mark.parametrize(
    'operand',
    [
        'foo',
        bool,
        3.12
    ]
)
def test_mul_other_incompatible_operand(operand):

    lattice = Lattice(
        (
            FrequencyRatio(2),
            FrequencyRatio(3),
            FrequencyRatio(5),
            FrequencyRatio(7),
            FrequencyRatio(11),
        )
    )

    with pytest.raises(TypeError) as exc_info:
        lattice.point((1, 2, 1, 0, 1)) * operand
    assert exc_info.value.args[0] == (
        f"unsupported operand type(s) for *: 'LatticePoint' and "
        f"'{type(operand).__name__}'"
    )

    with pytest.raises(TypeError) as exc_info:
        operand * lattice.point((1, 2, 1, 0, 1))
    assert exc_info.value.args[0] == (
        f"unsupported operand type(s) for *: 'LatticePoint' and "
        f"'{type(operand).__name__}'"
    )


@pytest.mark.parametrize(
    'tuple_in, scalar, tuple_r',
    [
        ((1, 9, 3, 5, 1), 1, (1, 9, 3, 5, 1)),
        ((1, 9, -3, 5, 1), 1, (1, 9, -3, 5, 1)),
        ((1, 9, -3, 5, 1), 10, (10, 90, -30, 50, 10)),
        ((1, 9, -3, 5, 1), 2, (2, 18, -6, 10, 2)),
        ((1, 9, -3, 5, 1), -2, (-2, -18, 6, -10, -2)),
        ((1, 9, -3, 5, 1), 0, (0, 0, 0, 0, 0)),
    ]
)
def test_mul(tuple_in, scalar, tuple_r):

    lattice = Lattice(
        (
            FrequencyRatio(2),
            FrequencyRatio(3),
            FrequencyRatio(5),
            FrequencyRatio(7),
            FrequencyRatio(11),
        )
    )

    assert scalar * lattice.point(tuple_in) == lattice.point(tuple_r)
    assert lattice.point(tuple_in) * scalar == lattice.point(tuple_r)


@pytest.mark.parametrize(
    'tuple_in, tuple_r',
    [
        ((1, 9, 3, 5, 1), (1, 9, 3, 5, 1)),
        ((-100, 4, 3, -2, 1), (100, -4, -3, 2, -1)),
        ((0, 0, 0, 0, 0), (0, 0, 0, 0, 0)),
    ]
)
def test_abs(tuple_in, tuple_r):

    lattice = Lattice(
        (
            FrequencyRatio(2),
            FrequencyRatio(3),
            FrequencyRatio(5),
            FrequencyRatio(7),
            FrequencyRatio(11),
        )
    )

    assert abs(lattice.point(tuple_in)) == lattice.point(tuple_r)


@pytest.mark.parametrize(
    'tuple_in, tuple_r',
    [
        ((1, 9, 3, 5, 1), (-1, -9, -3, -5, -1)),
        ((1, 4, 3, -2, 1), (-1, -4, -3, 2, -1)),
        ((0, 0, 0, 0, 0), (0, 0, 0, 0, 0)),
    ]
)
def test_neg(tuple_in, tuple_r):

    lattice = Lattice(
        (
            FrequencyRatio(2),
            FrequencyRatio(3),
            FrequencyRatio(5),
            FrequencyRatio(7),
            FrequencyRatio(11),
        )
    )

    assert lattice.point(tuple_r) == - lattice.point(tuple_in)
    assert - lattice.point(tuple_r) == lattice.point(tuple_in)


@pytest.mark.parametrize(
    'tuple_a, tuple_b, equal',
    [
        ((9, 2, 5, 6, 6), (9, 2, 5, 6, 6), True),
        ((1, 9, 3, 5, 1), (-4, 1, -4, 11, 3), False)
    ]
)
def test_eq_same_lattice(tuple_a, tuple_b, equal):

    lattice = Lattice(
        (
            FrequencyRatio(2),
            FrequencyRatio(3),
            FrequencyRatio(5),
            FrequencyRatio(7),
            FrequencyRatio(11),
        )
    )

    a = lattice.point(tuple_a)
    b = lattice.point(tuple_b)

    assert (a == b) is equal
    assert (b == a) is equal
    assert (hash(a) == hash(b)) is equal


def test_non_eq_different_lattice():

    lattice_a = Lattice(
        (
            FrequencyRatio(2),
            FrequencyRatio(3),
            FrequencyRatio(5),
            FrequencyRatio(7),
            FrequencyRatio(11),
        )
    )
    lattice_b = Lattice(
        (
            FrequencyRatio(2),
            FrequencyRatio(3),
            FrequencyRatio(5),
            FrequencyRatio(7),
            FrequencyRatio(17),
        )
    )
    assert lattice_a.point((1, 2, 3, 4, 5)) != lattice_b.point((1, 2, 3, 4, 5))


@pytest.mark.parametrize(
    'operand',
    [
        'foo',
        3,
        bool,
        3.12
    ]
)
def test_eq_non_lattice_point_operand(operand):

    lattice = Lattice(
        (
            FrequencyRatio(2),
            FrequencyRatio(3),
            FrequencyRatio(5),
            FrequencyRatio(7),
            FrequencyRatio(11),
        )
    )

    assert lattice.point((1, 2, 1, 0, 1)) != operand


def test_lt_different_lattice():

    lattice_a = Lattice(
        (
            FrequencyRatio(2),
            FrequencyRatio(3),
            FrequencyRatio(5),
            FrequencyRatio(7),
            FrequencyRatio(11),
        )
    )
    lattice_b = Lattice(
        (
            FrequencyRatio(2),
            FrequencyRatio(3),
            FrequencyRatio(5),
            FrequencyRatio(7),
            FrequencyRatio(17),
        )
    )

    with pytest.raises(TypeError) as exc_info:
        lattice_a.point((1, 2, 1, 0, 1)) < lattice_b.point((1, 3, 5, 5, -1))
    assert exc_info.value.args[0] == (
        "unsupported operator <: lattice points originate from "
        "different lattices"
    )

    with pytest.raises(TypeError) as exc_info:
        lattice_a.point((1, 2, 1, 0, 1)) <= lattice_b.point((1, 3, 5, 5, -1))
    assert exc_info.value.args[0] == (
        "unsupported operator <: lattice points originate from "
        "different lattices"
    )

    with pytest.raises(TypeError) as exc_info:
        lattice_a.point((1, 2, 1, 0, 1)) > lattice_b.point((1, 3, 5, 5, -1))
    assert exc_info.value.args[0] == (
        "unsupported operator <: lattice points originate from "
        "different lattices"
    )

    with pytest.raises(TypeError) as exc_info:
        lattice_a.point((1, 2, 1, 0, 1)) >= lattice_b.point((1, 3, 5, 5, -1))
    assert exc_info.value.args[0] == (
        "unsupported operator <: lattice points originate from "
        "different lattices"
    )


@pytest.mark.parametrize(
    'operand',
    [
        'foo',
        3,
        bool,
        3.12
    ]
)
def test_lt_gt_non_lattice_point_operand(operand):

    lattice = Lattice(
        (
            FrequencyRatio(2),
            FrequencyRatio(3),
            FrequencyRatio(5),
            FrequencyRatio(7),
            FrequencyRatio(11),
        )
    )

    with pytest.raises(TypeError) as exc_info:
        lattice.point((1, 2, 1, 0, 1)) < operand
    assert exc_info.value.args[0] == (
        f"unsupported operand type(s) for <: 'LatticePoint' and "
        f"'{type(operand).__name__}'"
    )

    with pytest.raises(TypeError) as exc_info:
        lattice.point((1, 2, 1, 0, 1)) <= operand
    assert exc_info.value.args[0] == (
        f"unsupported operand type(s) for <: 'LatticePoint' and "
        f"'{type(operand).__name__}'"
    )

    with pytest.raises(TypeError) as exc_info:
        lattice.point((1, 2, 1, 0, 1)) > operand
    assert exc_info.value.args[0] == (
        f"unsupported operand type(s) for <: 'LatticePoint' and "
        f"'{type(operand).__name__}'"
    )

    with pytest.raises(TypeError) as exc_info:
        lattice.point((1, 2, 1, 0, 1)) >= operand
    assert exc_info.value.args[0] == (
        f"unsupported operand type(s) for <: 'LatticePoint' and "
        f"'{type(operand).__name__}'"
    )

    with pytest.raises(TypeError) as exc_info:
        operand < lattice.point((1, 2, 1, 0, 1))
    assert exc_info.value.args[0] in {
        f"unsupported operand type(s) for <: 'LatticePoint' and "
        f"'{type(operand).__name__}'",
        f"unsupported operand type(s) for <: '{type(operand).__name__}' and "
        f"'LatticePoint'"
    }

    with pytest.raises(TypeError) as exc_info:
        operand <= lattice.point((1, 2, 1, 0, 1))
    assert exc_info.value.args[0] in {
        f"unsupported operand type(s) for <: 'LatticePoint' and "
        f"'{type(operand).__name__}'",
        f"unsupported operand type(s) for <=: '{type(operand).__name__}' and "
        f"'LatticePoint'"
    }

    with pytest.raises(TypeError) as exc_info:
        operand > lattice.point((1, 2, 1, 0, 1))
    assert exc_info.value.args[0] in {
        f"unsupported operand type(s) for <: 'LatticePoint' and "
        f"'{type(operand).__name__}'",
        f"unsupported operand type(s) for >: '{type(operand).__name__}' and "
        f"'LatticePoint'"
    }

    with pytest.raises(TypeError) as exc_info:
        operand >= lattice.point((1, 2, 1, 0, 1))
    assert exc_info.value.args[0] in {
        f"unsupported operand type(s) for <: 'LatticePoint' and "
        f"'{type(operand).__name__}'",
        f"unsupported operand type(s) for >=: '{type(operand).__name__}' and "
        f"'LatticePoint'"
    }


@pytest.mark.parametrize(
    'tuple_a, tuple_b, result',
    [
        ((0, 0, 0, 0, 0), (1, 0, 0, 0, 0), True),
        ((1, 0, 0, 0, 0), (0, 1, 0, 0, 0), True),
        ((2, 0, 0, 0, 0), (0, 1, 0, 0, 0), False),
        ((0, 0, -1, 0, 0), (0, -1, 0, 0, 0), True),
        ((1, 0, -1, 0, 0), (2, -1, 0, 0, 0), True),
        ((2, -1, 0, 0, 0), (1, -1, 0, 0, 0), False),
        ((2, -1, 0, 0, 4), (2, -1, 0, 0, 0), False),
    ]
)
def test_lt_gt(tuple_a, tuple_b, result):

    lattice = Lattice(
        (
            FrequencyRatio(2),
            FrequencyRatio(3),
            FrequencyRatio(5),
            FrequencyRatio(7),
            FrequencyRatio(11),
        )
    )

    assert (lattice.point(tuple_a) < lattice.point(tuple_b)) == result
    assert (lattice.point(tuple_a) <= lattice.point(tuple_b)) == result
    assert (lattice.point(tuple_b) > lattice.point(tuple_a)) == result
    assert (lattice.point(tuple_b) >= lattice.point(tuple_a)) == result
