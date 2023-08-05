from ..image import augment
from . import augments as augtool
import random
from .noise_composer import NoiseData
import librosa
import numpy as np
import soundfile

class Augment (augment.Augment):
    def __init__ (self, sr = 16000, noise_source_dir = None, difficulty = 1.0):
        self.sr = sr
        self._difficulty = difficulty
        self._random_multipliers = []
        self._life_noisy_maker = noise_source_dir and NoiseData (noise_source_dir, sr) or None

        self._augmentation_ranges = {  # (easy, hard)
            'color': (0.01, 0.1),
            'speed': (0.02, 0.2),
            'pitch': (0.1, 2.0),
            'ambient': (0.01, 0.5),
            'lap': (0.0, 0.0),
        }

    def write (self, path, y):
        with open (path, 'wb') as f:
            soundfile.write (f, y, self.sr)

    def __call__ (self, y, save_path = None):
        if isinstance (y, str):
            y, _ = librosa.load (y, sr = self.sr)

        noise_gain = self.noisy_value_from_type ('color')
        if noise_gain:
            if y.shape [0] % 2 == 1:
                y = y [:-1] # make even
            noise = augtool.gen_noise (random.choice (augtool.COLORS), y.shape [0])
            if random.randrange (3) == 0:
                # double noise
                noise += augtool.gen_noise (random.choice (augtool.COLORS), y.shape [0])
                noise /= 2
            y = (y * (1.0 - noise_gain)) + ((noise * noise_gain).astype ("float32"))

        pitch_shfit = self.noisy_value_from_type ('color')
        if pitch_shfit:
            y = librosa.effects.pitch_shift (y, self.sr, pitch_shfit * random.choice ([1, -1]), bins_per_octave = 12)

        speed = self.noisy_value_from_type ('speed')
        if speed:
            y = librosa.effects.time_stretch (y, 1.0 + (speed * random.choice ([1, -1])))

        if self._life_noisy_maker:
            ambient = self.noisy_value_from_type ('ambient')
            y = self._life_noisy_maker.synthesis (y, ambient)

        save_path and self.write (save_path, y)
        return y
