from typing import Tuple, Union
from pathlib import Path
from struct import pack
import numpy as np
from chipnumpy.constants import FRAMERATE, AMPLITUDE_SCALE, NUM_CHANNELS, NUM_BITS, NOTES, OCTAVES


class Synthesizer:
    """
    Abstract base class for synthesizers.
    """

    HEADER: bytes = pack('<4sI8sIHHIIHH4sI',
                         b"RIFF",
                         0,
                         b"WAVEfmt ",
                         NUM_BITS,
                         1,
                         NUM_CHANNELS,
                         FRAMERATE,
                         FRAMERATE * NUM_CHANNELS * NUM_BITS // 8,
                         NUM_CHANNELS * NUM_BITS // 8,
                         NUM_BITS,
                         b"data",
                         0)

    def __init__(self, seed: float = None):
        """
        :param seed: The random seed. This is used only in `noise()`. If None, the seed is random.
        """

        if seed is None:
            self._rng: np.random.RandomState = np.random.RandomState()
        else:
            self._rng = np.random.RandomState(seed)

    def sine(self, note: Union[str, float], amplitude: float, length: float) -> bytes:
        """
        :param note: Either a note expressed as a note + octave string, e.g. `"F#4"`, or the frequency in Hz as a float.
        :param amplitude: The amplitude (0 to 1).
        :param length: The length in seconds.

        :return A sine waveform.
        """

        return Synthesizer._to_bytes(Synthesizer._sine(note=note, amplitude=amplitude), length=length)

    def triangle(self, note: Union[str, float], amplitude: float, length: float) -> bytes:
        """
        :param note: Either a note expressed as a note + octave string, e.g. `"F#4"`, or the frequency in Hz as a float.
        :param amplitude: The amplitude (0 to 1).
        :param length: The length in seconds.

        :return A triangle waveform.
        """

        return Synthesizer._to_bytes(Synthesizer._triangle(note=note, amplitude=amplitude), length=length)

    def sawtooth(self, note: Union[str, float], amplitude: float, length: float) -> bytes:
        """
        :param note: Either a note expressed as a note + octave string, e.g. `"F#4"`, or the frequency in Hz as a float.
        :param amplitude: The amplitude (0 to 1).
        :param length: The length in seconds.

        :return A sawtooth waveform.
        """

        return Synthesizer._to_bytes(Synthesizer._sawtooth(note=note, amplitude=amplitude), length=length)

    def pulse(self, note: Union[str, float], amplitude: float, length: float, duty_cycle: int = 50) -> bytes:
        """
        :param note: Either a note expressed as a note + octave string, e.g. `"F#4"`, or the frequency in Hz as a float.
        :param amplitude: The amplitude (0 to 1).
        :param length: The length in seconds.
        :param duty_cycle: An integer that controls length of each pulse. Must be between 1 and 100.

        :return A pulse waveform.
        """

        return Synthesizer._to_bytes(Synthesizer._pulse(note=note, amplitude=amplitude, duty_cycle=duty_cycle), length=length)

    def noise(self, note: Union[str, float], amplitude: float, length: float) -> bytes:
        """
        :param note: Either a note expressed as a note + octave string, e.g. `"F#4"`, or the frequency in Hz as a float.
        :param amplitude: The amplitude (0 to 1).
        :param length: The length in seconds.

        :return A noise waveform using random values between -1 and 1.
        """

        return Synthesizer._to_bytes(self._noise(note=note, amplitude=amplitude), length=length)

    @staticmethod
    def to_wav(data: bytes) -> bytes:
        """
        Add a RIFF standard Wave header to raw PCM data.

        :param data: Raw PCM data as a byte array.

        :return: A fully formed Wave object with correct file header, ready to be saved to disk or used directly.
        """

        length: int = len(data)
        # Set the file length.
        Synthesizer.HEADER[4:8] = pack('<I', length + 36)
        # Set the data length.
        Synthesizer.HEADER[-4:] = pack('<I', length)
        wav = bytearray()
        wav.extend(Synthesizer.HEADER)
        wav.extend(data)
        return bytes(wav)

    @staticmethod
    def write(data: bytes, path: Union[str, Path]) -> None:
        """
        Add a RIFF Wave header to raw PCM data, and save to disk.

        :param data: Raw PCM data as a byte array.
        :param path: The path to the output file as either a string or a `Path`.
        """

        # Get a `Path` object.
        if isinstance(path, str):
            p = Path(path).resolve()
        elif isinstance(path, Path):
            p = path.resolve()
        else:
            raise Exception(f"Invalid path: {path}")
        # Create the directory.
        if not p.parent.exists():
            p.parent.mkdir(parents=True)
        # Write the data.
        p.write_bytes(data)

    @staticmethod
    def _to_bytes(arr: np.ndarray, length: float) -> bytes:
        """
        :param arr: A float64 numpy array.
        :param length: The length of the waveform.

        :return: A byte array of int16 wav data.
        """

        # Get the empty samples array.
        samples: np.ndarray = np.zeros(shape=int(FRAMERATE * length), dtype=np.int16)
        # Get a chunk of int16s.
        int16s: np.ndarray = (arr * AMPLITUDE_SCALE).astype(np.int16)
        # Drop in the samples.
        i = 0
        while i < samples.shape[0]:
            if i + int16s.shape[0] > samples.shape[0]:
                samples[i:] = int16s[:samples.shape[0] - i]
            else:
                samples[i: i + int16s.shape[0]] = int16s
            i += int16s.shape[0]
        return samples.tobytes()

    @staticmethod
    def _sine(note: Union[str, float], amplitude: float) -> np.ndarray:
        """
        Generate a sine waveform.

        :param note: Either a note expressed as a note + octave string, e.g. `"F#4"`, or the frequency in Hz as a float.
        :param amplitude: The amplitude (0 to 1).

        :return: A numpy sine waveform.
        """

        frequency, period, amplitude, arr = Synthesizer._start(note=note, amplitude=amplitude)
        # Get the range and convert to float64.
        arr: np.ndarray = np.arange(0, period).astype(np.float64)
        # Apply a sine.
        np.sin(2 * np.pi * frequency * (arr % period) / FRAMERATE, out=arr)
        # Multiply by the amplitude.
        np.multiply(arr, amplitude, out=arr)
        return arr

    @staticmethod
    def _triangle(note: Union[str, float], amplitude: float) -> np.ndarray:
        """
        Generate a triangle waveform.

        :param note: Either a note expressed as a note + octave string, e.g. `"F#4"`, or a frequency in Hz as a float.
        :param amplitude: The amplitude (0 to 1).

        :return: A numpy triangle waveform.
        """

        frequency, period, amplitude, arr = Synthesizer._start(note=note, amplitude=amplitude)
        half_period: float = period / 2
        return (amplitude / half_period) * (half_period - np.abs(arr % period - half_period) * 2 - 1)

    @staticmethod
    def _sawtooth(note: Union[str, float], amplitude: float) -> np.ndarray:
        """
        Generate a sawtooth waveform.

        :param note: Either a note expressed as a note + octave string, e.g. `"F#4"`, or a frequency in Hz as a float.
        :param amplitude: The amplitude (0 to 1).

        :return: A numpy sawtooth waveform.
        """

        frequency, period, amplitude, arr = Synthesizer._start(note=note, amplitude=amplitude)
        return amplitude * (frequency * (arr % period / FRAMERATE) * 2 - 1)

    @staticmethod
    def _pulse(note: Union[str, float], amplitude: float, duty_cycle: int = 50) -> np.ndarray:
        """
        Generate a pulse waveform.

        :param note: Either a note expressed as a note + octave string, e.g. `"F#4"`, or a frequency in Hz as a float.
        :param amplitude: The amplitude (0 to 1).
        :param duty_cycle: An integer that controls length of each pulse. Must be between 1 and 100.

        :return: A numpy pulse waveform.
        """

        frequency, period, amplitude, arr = Synthesizer._start(note=note, amplitude=amplitude)
        duty_cycle = int(duty_cycle * period / 100)
        return amplitude * ((arr < duty_cycle).astype(int) * 2 - 1)

    def _noise(self, note: Union[str, float], amplitude: float) -> np.ndarray:
        """
        Generate a noise waveform using random values between -1 and 1.

        :param note: Either a note expressed as a note + octave string, e.g. `"F#4"`, or a frequency in Hz as a float.
        :param amplitude: The amplitude (0 to 1).

        :return: A numpy noise waveform.
        """

        frequency: float = Synthesizer._get_frequency(note=note)
        period: int = int(FRAMERATE / frequency)
        arr: np.ndarray = self._rng.uniform(-1, 1, size=period)
        np.multiply(arr, amplitude, out=arr)
        return arr

    @staticmethod
    def _get_frequency(note: Union[str, float]) -> float:
        """
        :param note: Either a note expressed as a note + octave string, e.g. `"F#4"`, or a frequency in Hz as a float.

        :return: A frequency in Hz as a float.
        """

        if isinstance(note, str):
            return NOTES[note[:-1]] * OCTAVES[int(note[-1])]
        elif isinstance(note, float):
            return note
        else:
            raise Exception(f"Invalid note: {note}")

    @staticmethod
    def _start(note: Union[str, float], amplitude: float) -> Tuple[float, int, float, np.ndarray]:
        """
        Generate data used by most waveform types.

        :param note: Either a note expressed as a note + octave string, e.g. `"F#4"`, or a frequency in Hz as a float.
        :param amplitude: The amplitude (0 to 1).

        :return: Tuple: The frequency in Hz, the period as an int, the clamped amplitude, and a numpy array of length `period`.
        """

        frequency: float = Synthesizer._get_frequency(note=note)
        period: int = int(FRAMERATE / frequency)
        return frequency, period, 0 if amplitude < 0 else 1 if amplitude > 1 else amplitude, np.arange(0, period).astype(np.float64)
