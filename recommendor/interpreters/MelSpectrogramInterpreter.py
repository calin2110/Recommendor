import librosa
import numpy as np

from interpreters.AudioFileInterpreter import AudioFileInterpreter


class MelSpectrogramInterpreter(AudioFileInterpreter):
    def __init__(self, n_fft, hop_length, n_mels):
        super().__init__()
        self.__n_fft = n_fft
        self.__hop_length = hop_length
        self.__n_mels = n_mels

    def __call__(self, srate, data) -> np.ndarray:
        S = librosa.feature.melspectrogram(
            y=data,
            sr=srate,
            n_fft=self.__n_fft,
            hop_length=self.__hop_length,
            n_mels=self.__n_mels
        )
        S_to_db = librosa.power_to_db(S, ref=np.max)
        return S_to_db

    def extension(self) -> str:
        return 'mel'
