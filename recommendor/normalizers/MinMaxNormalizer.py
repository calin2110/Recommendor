import pickle

import numpy as np

from exceptions.NormalizerException import NormalizerException
from normalizers.Normalizer import Normalizer


class MinMaxNormalizer(Normalizer):
    def __init__(self, eps=1e-7):
        super().__init__()
        self.__eps = eps
        self.__min = None
        self.__max = None

    def __call__(self, data):
        if len(data.shape) == 3:
            if self.__min is not None or self.__max is not None:
                raise NormalizerException('Population already given')

            lines = data.shape[1]
            x_data = [np.concatenate(data[:, j, :]) for j in range(lines)]

            self.__min = np.min(x_data, axis=1)
            self.__max = np.max(x_data, axis=1)
            return (data - self.__min[:, np.newaxis]) / (
                        self.__max[:, np.newaxis] - self.__min[:, np.newaxis] + self.__eps)

        if len(data.shape) == 2:
            if self.__min is None or self.__max is None:
                raise NormalizerException('Population not previously given')
            return (data - self.__min[:, np.newaxis]) / (
                    self.__max[:, np.newaxis] - self.__min[:, np.newaxis] + self.__eps)

        raise NormalizerException('Invalid data shape')

    def save_stats(self, file):
        stats = np.array([self.__min, self.__max])
        np.save(file, stats)

    def load_stats(self, file):
        stats = np.load(file)
        self.__min = stats[0]
        self.__max = stats[1]
