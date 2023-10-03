from normalizers.Normalizer import Normalizer


class NoNormalizer(Normalizer):
    def __init__(self):
        super().__init__()

    def __call__(self, data):
        return data

    def save_stats(self, path):
        pass

    def load_stats(self, path):
        pass
