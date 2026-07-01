import pytest
from xenharmlib import PrimeLimitTuning


@pytest.mark.parametrize(
    'limit, repr_str',
    [
        (3, 'PrimeLimitTuning(3-Limit)'),
        (11, 'PrimeLimitTuning(11-Limit)'),
        (31, 'PrimeLimitTuning(31-Limit)'),
    ]

)
def test_repr(limit, repr_str):
    assert repr(PrimeLimitTuning(limit)) == repr_str


@pytest.mark.parametrize(
    'limit, name_str',
    [
        (3, 'PrimeLimitTuning(3)'),
        (11, 'PrimeLimitTuning(11)'),
        (31, 'PrimeLimitTuning(31)'),
    ]

)
def test_name(limit, name_str):
    assert PrimeLimitTuning(limit).name == name_str


@pytest.mark.parametrize(
    'noprime', [-3, 0, 1, 4, 99, 10, 27, 100, 102]
)
def test_init_noprime(noprime):
    with pytest.raises(ValueError) as exc_info:
        PrimeLimitTuning(noprime)
    assert 'Given limit is not a prime number' in exc_info.value.args[0]
