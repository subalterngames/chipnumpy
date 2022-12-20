# Chipnumpy

**Chipnumpy is a module for creating simple "chiptune" style audio waveforms using numpy.** 

This module can be thought of as an extension of [chippy](https://github.com/benmoran56/chippy), though not really a fork because most of the code has been rewritten.

The waveforms in `chipnumpy` are the same as those in `chippy`. The difference is that `chipnumpy` uses numpy as its generator, which is significantly faster.

# API

## Synthesizer

Start to generate audio by creating a Synthesizer:

```python
from chipnumpy.synthesizer import Synthesizer

s = Synthesizer()
```

You can optionally set the random seed: `s = Synthesizer(seed=0)`. This is used when generating noise waveforms; it can be useful if you want to recreate noise waveforms with the same seed.

To generate a sine waveform:

```python
from chipnumpy.synthesizer import Synthesizer

s = Synthesizer()
data = s.sine(frequency=293.66, amplitude=0.5, length=1.1)
```

- `frequency` is the frequency in Hz.
- `amplitude` controls the volume and is clamped to be between 0 and 1.
- `length` is the duration of the waveform in seconds.
- The returned `data` is an int16 byte array.

To generate a **triangle waveform**: `data = s.triangle(293.66, 0.5, 1.1)`

To generate a **sawtooth waveform**: `data = s.sawtooth(293.66, 0.5, 1.1)`

To generate a **pulse waveform**: `data = s.pulse(293.66, 0.5, 1.1)` You can optionally set the duty cycle parameter, which controls the length of the pulse (must be between 1 and 100): `s.pulse(293.66, 0.5, 1.1, duty_cycle=50)`.

To generate a **sawtooth waveform**: `data = s.sawtooth(293.66, 0.5, 1.1)`

To generate a **noise waveform** with the same syntax: `data = s.noise(293.66, 0.5, 1.1)` This uses random values; see above for how to seed the random number generator.

To convert data to wav data (i.e. to add a wav header): `wav = s.to_wav(data)`

To convert data to wav data and write to disk: `s.write(data, path)` where `data` is an int16 byte array and `path` is either a string or a `Path`.

