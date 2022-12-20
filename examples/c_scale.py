from time import sleep
import pygame.mixer
from chipnumpy.synthesizer import Synthesizer

length = 0.5
amplitude = 0.1
data = bytearray()
synthesizer = Synthesizer()
for note in ["C4", "D4", "E4", "F4", "G4", "A4", "B4", "C5"]:
    data.extend(synthesizer.sawtooth(note=note, amplitude=amplitude, length=length))
pygame.mixer.init()
sound = pygame.mixer.Sound(data)
sound.play()
sleep(sound.get_length())
