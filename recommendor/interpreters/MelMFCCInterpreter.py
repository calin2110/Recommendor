import numpy as np

from interpreters.AudioFileInterpreter import AudioFileInterpreter


class MelMFCCInterpreter(AudioFileInterpreter):
    def __init__(self, n_fft, hop_length, n_mels):
        super().__init__()
        self.__n_fft = n_fft
        self.__hop_length = hop_length
        self.__n_mels = n_mels

    def __call__(self, srate, data) -> np.ndarray:
        pass

    def extension(self) -> str:
        return 'mmfccs'
