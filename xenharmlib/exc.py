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

"""
This module includes all exceptions that must be handled
by the user of the library
"""


class IncompatibleOriginContexts(Exception):
    """
    Gets raised whenever two or more objects are not
    compatible because they are based on different
    orgin contexts
    """
    pass


class UnfittingNotation(Exception):
    """
    Gets raised on construction of notations when a
    property of the tuning prohibits the use of the
    specific notation
    """

    pass


class UnknownNoteSymbol(Exception):
    """
    Gets raised on construction of notes if a provided
    symbol was not recognized by the notation
    """


class InvalidFrequency(Exception):
    """
    Gets raised when a frequency argument does not
    adhere to a certain restriction, for example if
    it is out of bounds of a predefined limit
    """


class InvalidPitchIndex(Exception):
    """
    Gets raised when a pitch index does not adhere
    to a certain restriction, for example if it is
    out of bounds of a predefined limit
    """


class InvalidPitchClassIndex(Exception):
    """
    Gets raised when a pitch class index does not
    adhere to a certain restriction, for example if
    it is out of bounds of a predefined limit
    """


class InvalidBaseIntervalIndex(Exception):
    """
    Gets raised when a base interval index does not
    adhere to a certain restriction, for example if
    it is out of bounds of a predefined limit
    """


class InvalidGenerator(Exception):
    """
    Gets raised when a given pitch or pitch-like
    argument is not a generator in respect to the
    tuning
    """


class InvalidNaturalIndex(Exception):
    """
    Gets raised when a natural index does not adhere
    to a certain restriction, for example if it is
    out of bounds of a predefined limit
    """


class InvalidAccidentalValue(Exception):
    """
    Gets raised when an accidental value is not
    allowed in a notation
    """


class InvalidNaturalDiffClassIndex(Exception):
    """
    Gets raised when a natural diff class index does not
    adhere to a certain restriction, for example if it is
    out of bounds of a predefined limit
    """


class InvalidIntervalNumber(Exception):
    """
    Gets raised when an interval number is not valid
    """


class InvalidIndexMask(Exception):
    """
    Gets raised when an index mask expression is invalid
    """
