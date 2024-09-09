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
This module includes functions to render frequencies of objects
as sine waves and export them as wavfile
"""

import math
from typing import *
import numpy as np
import sounddevice as sd
from ..core.protocols import HasFrequency
from ..core.frequencies import Frequency
from scipy.io.wavfile import write as write_wav

DEFAULT_SAMPLE_RATE = 22050


def freq_to_raw_sine_audio(
    frequency: Frequency,
    duration: float = 0.5,
    sample_rate: int = DEFAULT_SAMPLE_RATE,
):
    """
    Returns a raw audio byte stream as a numpy array
    for a given frequency by using a generic sine wave

    :param frequency: The frequency of the sine wave
    :param duration: The duration in seconds
    :param sample_rate: The sample rate of the raw audio
        (optional, default is 22050)
    """

    _frequency = frequency.to_float()
    t = np.linspace(0, duration, math.ceil(sample_rate * duration))
    output = np.sin(2 * np.pi * _frequency * t)

    # generate fade in/out array (to remove the clicking
    # noise on frequency change)

    fade_in_t = min(100, len(output) // 100)
    fade_out_t = min(1000, len(output) // 10)

    volume = []

    for i in range(0, fade_in_t):
        volume.append(i / fade_in_t)

    volume.extend([1] * (len(output) - (fade_in_t + fade_out_t)))

    for i in range(0, fade_out_t):
        volume.append((fade_out_t - i - 1) / fade_out_t)

    output = output * np.array(volume)

    return output


def pitch_like_to_raw_sine_audio(
    pitch_like: HasFrequency,
    duration: float = 0.5,
    sample_rate: int = DEFAULT_SAMPLE_RATE,
):
    """
    Returns a raw audio byte stream as a numpy array
    for a given pitch-like object (e.g. a note or a
    pitch object) by using a generic sine wave

    :param pitch_like: An object with a frequency property
    :param duration: The duration in seconds
    :param sample_rate: The sample rate of the raw audio
        (optional, default is 22050)
    """

    return freq_to_raw_sine_audio(pitch_like.frequency, duration, sample_rate)


def tone_obj_to_raw_sine_audio(
    tone_obj: Frequency | HasFrequency,
    duration: float = 0.5,
    sample_rate: int = DEFAULT_SAMPLE_RATE,
):
    """
    Returns a raw audio byte stream as a numpy array
    for a given tone object (a frequency, note or pitch)
    by using a generic sine wave

    :param frequency: The frequency of the sinewave
    :param duration: The duration in seconds
    :param sample_rate: The sample rate of the raw audio
        (optional, default is 22050)
    """

    if isinstance(tone_obj, Frequency):
        return freq_to_raw_sine_audio(tone_obj, duration, sample_rate)

    elif isinstance(tone_obj, HasFrequency):
        return pitch_like_to_raw_sine_audio(tone_obj, duration, sample_rate)

    raise ValueError(
        'Tone object must be a frequency or have a frequency property'
    )


def concat_audio_chunks(chunks: List):
    """
    Concatenates a list of numpy arrays including
    raw audio data.

    :param chunks: A list of numpy arrays containing
        raw audio data
    """

    output = np.array(())

    for chunk in chunks:
        output = np.concatenate((output, chunk))

    return output


def mix_audio_chunks(chunks: List):
    """
    Mixes a list of numpy arrays including raw audio data.

    :param chunks: A list of numpy arrays containing
        raw audio data
    """

    size = max([chunk.size for chunk in chunks])

    output = np.zeros(size)

    for chunk in chunks:
        output += chunk

    # make sure max amplitude does not exceed 1

    if np.max(output) > abs(np.min(output)):
        output = output / np.max(output)
    else:
        output = output / -np.min(output)

    return output


def playable_to_raw_sine_audio(
    playable: (
        Iterable[HasFrequency] | HasFrequency | Iterable[Frequency] | Frequency
    ),
    duration: float = 0.5,
    play_as_chord: bool = False,
    sample_rate: int = DEFAULT_SAMPLE_RATE,
):
    """
    Returns a raw audio byte stream as a numpy array for
    a given playable object (a frequency, frequency list,
    note, pitch, note scale, pitch scale, note list, pitch
    list)

    :param playable: A playable object
    :param duration: (optional, default is 0.5) The number of
        seconds a single sound should be played
    :param sample_rate: The sample rate of the raw audio
        (optional, default is 22050)
    """

    if not isinstance(playable, Iterable):
        playable = [playable]

    chunks = []
    for tone_obj in playable:
        chunk = tone_obj_to_raw_sine_audio(tone_obj, duration, sample_rate)
        chunks.append(chunk)

    if play_as_chord:
        return mix_audio_chunks(chunks)

    return concat_audio_chunks(chunks)


def export_wav(
    filename: str,
    playable: (
        Iterable[HasFrequency] | HasFrequency | Iterable[Frequency] | Frequency
    ),
    duration: float = 0.5,
    play_as_chord: bool = False,
    sample_rate: int = DEFAULT_SAMPLE_RATE,
):
    """
    This function exports a playable object as a wav file

    :param filename: Target filename to export data to
    :param playable: The playable object. Can be a pitch, note,
        frequency, a list of the aforementioned - or a scale.
    :param duration: (optional, default is 0.5) The number of
        seconds a single sound should be played
    :param play_as_chord: (optional, default False). If set
        to True items in collections of playable objects will
        be mixed instead of put after another.
    :param sample_rate: (optional, default 22050) The sample
        rate of the output data
    """

    output = playable_to_raw_sine_audio(
        playable, duration, play_as_chord, sample_rate
    )

    scaled = np.int16(output / np.max(np.abs(output)) * 32767)
    write_wav(filename, sample_rate, scaled)
