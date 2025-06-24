from .utils import scale_element
from ..core.scale import PeriodicScale
from ..core.interval import Interval


def spec_interval(
    scale: PeriodicScale,
    source_index: int,
    target_index: int
) -> Interval:
    """
    Returns the specific interval for a generic interval
    of the periodic extension of the scale.

    >>> from xenharmlib import EDOTuning
    >>> from xenharmlib import UpDownNotation
    >>> from xenharmlib import periodic
    >>>
    >>> edo12 = EDOTuning(12)
    >>> n_edo12 = UpDownNotation(edo12)
    >>>
    >>> c_maj = n_edo12.pc_scale(['C', 'D', 'E', 'F', 'G', 'A', 'B'])
    >>> periodic.spec_interval(c_maj, 6, 7)
    UpDownNoteInterval(m2, 12-EDO)

    :param scale: A period normalized scale
    :param source_index: Periodic source index for the interval
    :param target_index: Periodic target index for the interval
    """

    if not scale.is_period_normalized:
        raise ValueError(
            'spec_interval is only defined on period normalized scales'
        )

    source = scale_element(scale, source_index)
    target = scale_element(scale, target_index)
    return source.interval(target)

