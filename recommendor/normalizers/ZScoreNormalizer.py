import numpy as np

from exceptions.NormalizerException import NormalizerException
from normalizers.Normalizer import Normalizer


class ZScoreNormalizer(Normalizer):
    def __init__(self, eps=1e-7):
        super().__init__()
        self.__eps = eps
        self.__mean = None
        self.__std = None

    def __call__(self, data) -> np.ndarray:
        if len(data.shape) == 3:
            if self.__mean is not None or self.__std is not None:
                raise NormalizerException('Population already given')

            lines = data.shape[1]
            x_data = [np.concatenate(data[:, j, :]) for j in range(lines)]

            self.__mean = np.mean(x_data, axis=1)
            self.__std = np.std(x_data, axis=1)

            return (data - self.__mean[:, np.newaxis]) / (self.__std[:, np.newaxis] + self.__eps)

        if len(data.shape) == 2:
            if self.__mean is None or self.__std is None:
                raise NormalizerException('Population not previously given')

            return (data - self.__mean[:, np.newaxis]) / (self.__std[:, np.newaxis] + self.__eps)

        raise NormalizerException('Invalid data shape')

    def save_stats(self, file):
        stats = np.array([self.__mean, self.__std])
        np.save(file, stats)

    def load_stats(self, file):
        stats = np.load(file)
        self.__mean = stats[0]
        self.__std = stats[1]
