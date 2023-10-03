import numpy as np

from interpreters.AudioFileInterpreter import AudioFileInterpreter


class MFCCsInterpreter(AudioFileInterpreter):
    def __init__(self):
        super().__init__()

    def __call__(self, srate, data) -> np.ndarray:
        pass

    def extension(self) -> str:
        return 'mfccs'

