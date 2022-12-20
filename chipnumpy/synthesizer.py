from typing import Tuple, Union
from pathlib import Path
from struct import pack
import numpy as np
from chipnumpy.constants import FRAMERATE, AMPLITUDE_SCALE, NUM_CHANNELS, NUM_BITS


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
                         FRAMERATE * NUM_BITS // 8,
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

    def sine(self, frequency: float, amplitude: float, length: float) -> bytes:
        """
        :param frequency: The frequency in Hz.
        :param amplitude: The amplitude (0 to 1).
        :param length: The length in seconds.

        :return A sine waveform.
        """

        return Synthesizer._to_bytes(Synthesizer._sine(frequency=frequency, amplitude=amplitude),
                                     length=length)

    def triangle(self, frequency: float, amplitude: float, length: float) -> bytes:
        """
        :param frequency: The frequency in Hz.
        :param amplitude: The amplitude (0 to 1).
        :param length: The length in seconds.

        :return A triangle waveform.
        """

        return Synthesizer._to_bytes(Synthesizer._triangle(frequency=frequency, amplitude=amplitude),
                                     length=length)

    def sawtooth(self, frequency: float, amplitude: float, length: float) -> bytes:
        """
        :param frequency: The frequency in Hz.
        :param amplitude: The amplitude (0 to 1).
        :param length: The length in seconds.

        :return A sawtooth waveform.
        """

        return Synthesizer._to_bytes(Synthesizer._sawtooth(frequency=frequency, amplitude=amplitude),
                                     length=length)

    def pulse(self, frequency: float, amplitude: float, length: float, duty_cycle: int = 50) -> bytes:
        """
        :param frequency: The frequency in Hz.
        :param amplitude: The amplitude (0 to 1).
        :param length: The length in seconds.
        :param duty_cycle: An integer that controls length of each pulse. Must be between 1 and 100.

        :return A pulse waveform.
        """

        return Synthesizer._to_bytes(Synthesizer._pulse(frequency=frequency, amplitude=amplitude, duty_cycle=duty_cycle),
                                     length=length)

    def noise(self, frequency: float, amplitude: float, length: float) -> bytes:
        """
        :param frequency: The frequency in Hz.
        :param amplitude: The amplitude (0 to 1).
        :param length: The length in seconds.

        :return A noise waveform using random values between -1 and 1.
        """

        return Synthesizer._to_bytes(self._noise(frequency=frequency, amplitude=amplitude),
                                     length=length)

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
        return Synthesizer.HEADER + data

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
    def _sine(frequency: float, amplitude: float) -> np.ndarray:
        """
        Generate a sine waveform.

        :param frequency: The frequency in Hz.
        :param amplitude: The amplitude (0 to 1).

        :return: A numpy sine waveform.
        """

        period, amplitude, arr = Synthesizer._start(frequency=frequency, amplitude=amplitude)
        # Get the range and convert to float64.
        arr: np.ndarray = np.arange(0, period).astype(np.float64)
        # Apply a sine.
        np.sin(2 * np.pi * frequency * (arr % period) / FRAMERATE, out=arr)
        # Multiply by the amplitude.
        np.multiply(arr, amplitude, out=arr)
        return arr

    @staticmethod
    def _triangle(frequency: float, amplitude: float) -> np.ndarray:
        """
        Generate a triangle waveform.

        :param frequency: The frequency in Hz.
        :param amplitude: The amplitude (0 to 1).

        :return: A numpy triangle waveform.
        """

        period, amplitude, arr = Synthesizer._start(frequency=frequency, amplitude=amplitude)
        half_period: float = period / 2
        return (amplitude / half_period) * (half_period - np.abs(arr % period - half_period) * 2 - 1)

    @staticmethod
    def _sawtooth(frequency: float, amplitude: float) -> np.ndarray:
        """
        Generate a sawtooth waveform.

        :param frequency: The frequency in Hz.
        :param amplitude: The amplitude (0 to 1).

        :return: A numpy sawtooth waveform.
        """

        period, amplitude, arr = Synthesizer._start(frequency=frequency, amplitude=amplitude)
        return amplitude * (frequency * (arr % period / FRAMERATE) * 2 - 1)

    @staticmethod
    def _pulse(frequency: float, amplitude: float, duty_cycle: int = 50) -> np.ndarray:
        """
        Generate a pulse waveform.

        :param frequency: The frequency in Hz.
        :param amplitude: The amplitude (0 to 1).
        :param duty_cycle: An integer that controls length of each pulse. Must be between 1 and 100.

        :return: A numpy pulse waveform.
        """

        period, amplitude, arr = Synthesizer._start(frequency=frequency, amplitude=amplitude)
        duty_cycle = int(duty_cycle * period / 100)
        return amplitude * ((arr < duty_cycle).astype(int) * 2 - 1)

    def _noise(self, frequency: float, amplitude: float) -> np.ndarray:
        """
        Generate a noise waveform using random values between -1 and 1.

        :param frequency: The frequency in Hz.
        :param amplitude: The amplitude (0 to 1).

        :return: A numpy noise waveform.
        """

        period = int(FRAMERATE / frequency)
        arr = self._rng.uniform(-1, 1, size=period)
        np.multiply(arr, amplitude, out=arr)
        return arr

    @staticmethod
    def _start(frequency: float, amplitude: float) -> Tuple[int, float, np.ndarray]:
        """
        Generate data used by most waveform types.

        :param frequency: The frequency in Hz.
        :param amplitude: The amplitude (0 to 1).

        :return: Tuple: The period as an int, the amplitude clamped between 0 and 1, and a numpy array of length `period`.
        """

        period = int(FRAMERATE / frequency)
        return period, 0 if amplitude < 0 else 1 if amplitude > 1 else amplitude, np.arange(0, period).astype(np.float64)
