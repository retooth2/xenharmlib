from xenharmlib.core.notation import NatAccNotation
from xenharmlib.core.symbols import SymbolSumArithmetic
from xenharmlib.core.symbols import SymbolSumArithmeticSet

def make_nat_acc_test_notation(tuning):
    """
    Creates a very generic and meaningless natural/accidental
    notation that classifies every second note of the tuning
    as a natural and adds four accidentals: the + alters one
    step upwards, the x alters two steps upwards, the - one
    step downwards, the . two steps downwards.

    Naturals are just named alphabetically A=0, B=2, etc

    For interval notation we say there are two types of intervals
    in the system: FUNKY and CRINGE. Every natural with an even
    natural index is considered FUNKY, every natural with an odd
    natural index is considered CRINGE. Funky intervals are notated
    'F', '+F', '-F', '++F' while cringe intervals are notated 'C',
    '+C', '-C', '--C'
    """

    ALPHABET = [chr(x) for x in range(65, 65+26)]

    notation = NatAccNotation(tuning)

    for nat_pc_index in range(0, len(tuning), 2):
        symbol = ALPHABET.pop(0)
        notation.set_natc_symbol(nat_pc_index, symbol)

    acc_arith = SymbolSumArithmetic(allow_empty=True)
    acc_arith.add_symbol('+', 1)
    acc_arith.add_symbol('x', 2)
    acc_arith.add_symbol('-', -1)
    acc_arith.add_symbol('.', -2)

    notation.acc_symbol_code = acc_arith

    funky_upper = SymbolSumArithmetic()
    funky_upper.add_symbol('F', 0, min_occurence=1, max_occurence=1)
    funky_upper.add_symbol('+', 1)
    funky_lower = SymbolSumArithmetic()
    funky_lower.add_symbol('F', 0, min_occurence=1, max_occurence=1)
    funky_lower.add_symbol('-', -1)
    funky = SymbolSumArithmeticSet([funky_upper, funky_lower])

    cringe_upper = SymbolSumArithmetic()
    cringe_upper.add_symbol('C', 0, min_occurence=1, max_occurence=1)
    cringe_upper.add_symbol('+', 1)
    cringe_lower = SymbolSumArithmetic()
    cringe_lower.add_symbol('C', 0, min_occurence=1, max_occurence=1)
    cringe_lower.add_symbol('-', -1)
    cringe = SymbolSumArithmeticSet([cringe_upper, cringe_lower])

    for nat_diffc in range(0, len(tuning) // 2):
        if nat_diffc % 2 == 0:
            notation.set_interval_symbol_code(
                nat_diffc, funky
            )
        else:
            notation.set_interval_symbol_code(
                nat_diffc, cringe
            )

    return notation