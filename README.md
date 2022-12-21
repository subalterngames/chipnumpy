# Chipnumpy

**Chipnumpy is a module for creating simple chiptune style audio waveforms using numpy.** 

Chipnumpy was inspired by [chippy](https://github.com/benmoran56/chippy). It has a similar API and generates the same types of waveforms. Unlike chippy, chipnumpy uses numpy, which makes it significantly faster.

To install:

```bash
pip3 install chipnumpy
```

For example implementation, see `examples/c_scale.py` (requires pygame to play the audio).

# Synthesizer API

## The constructor

Start to generate audio by creating a Synthesizer:

```python
from chipnumpy.synthesizer import Synthesizer

s = Synthesizer()
```

You can optionally set the random seed: `s = Synthesizer(seed=0)`. This is used when generating noise waveforms; it can be useful if you want to recreate noise waveforms with the same seed.

## Generate a sine waveform

```python
from chipnumpy.synthesizer import Synthesizer

s = Synthesizer()
data = s.sine(note=293.66, amplitude=0.5, length=1.1)
```

`note` is either a frequency in Hz, or a string representing a note + octave:

```python
from chipnumpy.synthesizer import Synthesizer

s = Synthesizer()
data = s.sine(note="C5", amplitude=0.5, length=1.1)
```

`amplitude` controls the volume and is clamped to be between 0 and 1.

`length` is the duration of the waveform in seconds.

The returned `data` is an int16 byte array.

## Generate other waveforms

To generate a **triangle waveform**: `data = s.triangle("C5", 0.5, 1.1)`

To generate a **sawtooth waveform**: `data = s.sawtooth("C5", 0.5, 1.1)`

To generate a **pulse waveform**: `data = s.pulse("C5", 0.5, 1.1)` You can optionally set the duty cycle parameter, which controls the length of the pulse (must be between 1 and 100): `s.pulse("C5", 0.5, 1.1, duty_cycle=50)`.

To generate a **sawtooth waveform**: `data = s.sawtooth("C5", 0.5, 1.1)`

To generate a **noise waveform** with the same syntax: `data = s.noise("C5", 0.5, 1.1)` This uses random values; see above for how to seed the random number generator.

## Generate and write wav data

To convert data to wav data (i.e. to add a wav header): `wav = s.to_wav(data)`

To convert data to wav data and write to disk: `s.write(data, path)` where `data` is an int16 byte array and `path` is either a string or a `Path`.
