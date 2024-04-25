from typing import *
import sounddevice as sd
from .export.audio import playable_to_raw_sine_audio
from .export.audio import DEFAULT_SAMPLE_RATE
from .core.protocols import HasFrequency
from .core.frequencies import Frequency


def play(
    playable: Iterable[HasFrequency] | 
              HasFrequency |
              Iterable[Frequency] |
              Frequency,
    duration: float = 0.5,
    play_as_chord: bool = False,
    sample_rate: int = DEFAULT_SAMPLE_RATE
):
    """
    Renders an object into a sine wave sound and plays it

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
        playable,
        duration,
        play_as_chord,
        sample_rate
    )
    sd.play(
        output,
        samplerate=sample_rate,
        blocking=True
    )
