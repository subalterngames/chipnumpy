from typing import Dict, List

# The sample framerate.
FRAMERATE: int = 44100
# Default for 16-bit audio.
AMPLITUDE_SCALE: int = 32767
# The number of channels. Currently, only 1 is supported.
NUM_CHANNELS: int = 1
# The number of bits. This is used for wav data.
NUM_BITS: int = 16
# Notes and frequencies. Source: https://github.com/benmoran56/chippy/blob/master/chippy/mmlparser.py
NOTES: Dict[str, float] = {"C": 261.63,
                           "C#": 277.183,
                           "D": 293.66,
                           "D#": 311.127,
                           "E": 329.63,
                           "F": 349.23,
                           "F#": 369.994,
                           "G": 392.00,
                           "G#": 415.305,
                           "A": 440.00,
                           "A#": 466.164,
                           "B": 493.88}
# A list of notes.
NOTES_LIST: List[str] = list(NOTES.keys())
# Octave multipliers. Source: https://github.com/benmoran56/chippy/blob/master/chippy/mmlparser.py
OCTAVES: Dict[int, float] = {0: 0.06,
                             1: 0.12,
                             2: 0.25,
                             3: 0.5,
                             4: 1,
                             5: 2,
                             6: 4,
                             7: 8,
                             8: 16}
