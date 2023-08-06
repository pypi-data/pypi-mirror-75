import librosa
import numpy as np
import random

from kolibri.features import Features


class AudioPreprocessor(Features):
    """
    Loads and clean audio files
"""

    name = "audio_preprocessor"

    provides = ["audio_features"]

    requires = []

    defaults = {
        "envolope": True,  # compute the envolop and apply threshold

        # remove accents during the preprocessing step
        "threshold": 20,
        "sample_rate": 16000,
        "envolop": True,
        "delta_time": 1,
        "downsample": True,
        "split": True,
        "random_start": True
    }

    @classmethod
    def required_packages(cls):
        return ["librosa"]

    def __init__(self, component_config):
        """Construct a new count vectorizer using the sklearn framework."""

        super(AudioPreprocessor, self).__init__(component_config)

    def fit_transform(self, X, y):

        return self.transform(X)

    def transform(self, X):
        Xt = np.empty((len(X), 1, int(self.component_config["sample_rate"] * self.component_config["delta_time"])),
                      dtype=np.float32)

        for i, x in enumerate(X):
            if self.component_config["downsample"]:
                wav, rate = librosa.load(x, sr=self.component_config["sample_rate"])
            else:
                wav, rate = librosa.load(x)

            intervals = librosa.effects.split(wav, top_db=self.component_config["threshold"])
            wav_output = []

            wav_len = int(self.component_config["sample_rate"] * self.component_config["delta_time"])

            for sliced in intervals:
                wav_output.extend(wav[sliced[0]:sliced[1]])

            if len(wav_output) > wav_len:
                l = len(wav_output) - wav_len
                r = 0
                if self.component_config["random_start"]:
                    r = random.randint(0, l)
                wav_output = wav_output[r:wav_len + r]
            else:
                wav_output.extend(np.zeros(shape=[wav_len - len(wav_output)], dtype=np.float32))
            Xt[i,] = np.array(wav_output).reshape(1, -1)
        return Xt

    def get_info(self):
        return 'audio cleaner'
