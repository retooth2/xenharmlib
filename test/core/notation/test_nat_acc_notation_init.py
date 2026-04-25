import pytest
from xenharmlib import EDOTuning
from xenharmlib.exc import InvalidAccidentalValue
from xenharmlib.exc import InvalidNaturalDiffClassIndex
from xenharmlib.core.notation import NatAccNotation
from xenharmlib.core.notation import IncompleteNotation
from xenharmlib.core.symbols import SymbolArithmetic
from xenharmlib.core.symbols import AmbiguousSymbol


def test_append_natural_ambiguous_symbol():

    tuning = EDOTuning(12)
    notation = NatAccNotation(tuning, acc_weights=(1,))

    notation.append_natural('C', 3)

    with pytest.raises(AmbiguousSymbol):
        notation.append_natural('C', 5)


def test_get_acc_symbol_invalid_accidental_value():

    tuning = EDOTuning(12)
    notation = NatAccNotation(tuning, acc_weights=(1,))

    arith = SymbolArithmetic()
    arith.add_symbol('#', (1,))
    notation.acc_symbol_code = arith

    with pytest.raises(InvalidAccidentalValue):
        notation.get_acc_symbol((-1,))


def test_set_interval_symbol_code_invalid_nat_diffc():

    tuning = EDOTuning(12)
    notation = NatAccNotation(tuning, acc_weights=(1,))

    notation.append_natural('C', 3)

    arith = SymbolArithmetic()
    arith.add_symbol('X', (1,))

    with pytest.raises(InvalidNaturalDiffClassIndex):
        notation.set_interval_symbol_code(1, arith)


def test_get_interval_symbol_incomplete_notation():

    tuning = EDOTuning(12)
    notation = NatAccNotation(tuning, acc_weights=(1,))

    notation.append_natural('C', 3)
    notation.append_natural('D', 5)
    notation.append_natural('E', 6)

    with pytest.raises(IncompleteNotation):
        notation.get_interval_symbol(2, (1,))


def test_acc_symbol_code_incomplete_notation():

    tuning = EDOTuning(12)
    notation = NatAccNotation(tuning, acc_weights=(1,))

    with pytest.raises(IncompleteNotation):
        notation.acc_symbol_code
