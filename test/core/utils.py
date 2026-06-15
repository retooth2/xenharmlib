from xenharmlib.core.notes import NatAccNote
from xenharmlib.core.notes import NatAccNoteInterval
from xenharmlib.core.note_scale import NatAccNoteScale
from xenharmlib.core.note_interval_seq import NatAccNoteIntervalSeq
from xenharmlib.core.note_interval_fan import NatAccNoteIntervalFan
from xenharmlib.core.note_seq import NatAccNoteSeq
from xenharmlib.core.notes import SDPeriodicNoteMixin
from xenharmlib.core.notes import SDPeriodicNoteIntervalMixin
from xenharmlib.core.notation import NatAccNotation
from xenharmlib.core.symbols import SymbolArithmetic
from xenharmlib.core.symbols import SymbolArithmeticSet


class MyNatAccNote(NatAccNote[int], SDPeriodicNoteMixin):
    pass


class MyNatAccNoteInterval(
    NatAccNoteInterval[int, MyNatAccNote], SDPeriodicNoteIntervalMixin
):
    pass


class MyNatAccNoteScale(NatAccNoteScale[int, MyNatAccNote]):
    pass


class MyNatAccNoteIntervalSeq(NatAccNoteIntervalSeq[int, MyNatAccNote]):
    pass


class MyNatAccNoteIntervalFan(NatAccNoteIntervalFan[int, MyNatAccNote]):
    pass


class MyNatAccNoteSeq(NatAccNoteSeq[int, MyNatAccNote]):
    pass


class MyNatAccNotation(NatAccNotation[int]):

    def __init__(
        self,
        tuning,
        acc_weights,
        note_cls=MyNatAccNote,
        note_interval_cls=MyNatAccNoteInterval,
        note_scale_cls=MyNatAccNoteScale,
        note_interval_seq_cls=MyNatAccNoteIntervalSeq,
        note_interval_fan_cls=MyNatAccNoteIntervalFan,
        note_seq_cls=MyNatAccNoteSeq,
    ):

        super().__init__(
            tuning,
            acc_weights,
            note_cls=MyNatAccNote,
            note_interval_cls=MyNatAccNoteInterval,
            note_scale_cls=NatAccNoteScale,
            note_interval_seq_cls=NatAccNoteIntervalSeq,
            note_interval_fan_cls=MyNatAccNoteIntervalFan,
            note_seq_cls=MyNatAccNoteSeq,
        )

    @property
    def zero_index(self):
        return 0


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

    notation = MyNatAccNotation(tuning, acc_weights=(1,))

    for nat_pc_index in range(0, tuning.period_length, 2):
        natc_symbol = ALPHABET.pop(0)
        notation.append_natural(natc_symbol, nat_pc_index)

    acc_arith = SymbolArithmetic(allow_empty=True)
    acc_arith.add_symbol('+', (1,))
    acc_arith.add_symbol('x', (2,))
    acc_arith.add_symbol('-', (-1,))
    acc_arith.add_symbol('.', (-2,))

    notation.acc_symbol_code = acc_arith

    funky_upper = SymbolArithmetic()
    funky_upper.add_symbol(
        'F', (0,), min_occurence=1, max_occurence=1, position=1
    )
    funky_upper.add_symbol('+', (1,), position=0)
    funky_lower = SymbolArithmetic()
    funky_lower.add_symbol(
        'F', (0,), min_occurence=1, max_occurence=1, position=1
    )
    funky_lower.add_symbol('-', (-1,), position=0)
    funky = SymbolArithmeticSet()
    funky.add_arithmetic(funky_upper)
    funky.add_arithmetic(funky_lower)

    cringe_upper = SymbolArithmetic()
    cringe_upper.add_symbol(
        'C', (0,), min_occurence=1, max_occurence=1, position=1
    )
    cringe_upper.add_symbol('+', (1,), position=0)
    cringe_lower = SymbolArithmetic()
    cringe_lower.add_symbol(
        'C', (0,), min_occurence=1, max_occurence=1, position=1
    )
    cringe_lower.add_symbol('-', (-1,), position=0)
    cringe = SymbolArithmeticSet()
    cringe.add_arithmetic(cringe_upper)
    cringe.add_arithmetic(cringe_lower)

    for nat_diffc in range(0, tuning.period_length // 2):
        if nat_diffc % 2 == 0:
            notation.set_interval_symbol_code(
                nat_diffc, funky
            )
        else:
            notation.set_interval_symbol_code(
                nat_diffc, cringe
            )

    return notation
