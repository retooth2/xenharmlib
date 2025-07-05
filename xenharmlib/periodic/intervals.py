# This file is part of xenharmlib.
#
# xenharmlib is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# xenharmlib is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with xenharmlib. If not, see <https://www.gnu.org/licenses/>.

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
    UpDownNoteInterval(m, 2, 12-EDO)

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

