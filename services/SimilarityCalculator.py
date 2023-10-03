import os
import pickle

from threading import Lock

from shared.CommutativePair import CommutativePair
from SubgenrePdf import SubgenrePdf


GENRES = ['BLUES', 'CLASSICAL', 'COUNTRY', 'DISCO', 'HIP_HOP', 'JAZZ', 'METAL', 'POP', 'REGGAE', 'ROCK']


class SimilarityNormalCalculator:
    def __init__(self):
        super().__init__()
        self.matrices = {}
        self.lock = Lock()
        self.load()

    def load(self):
        self.lock.acquire()
        for genre in GENRES:
            with open(os.path.join('matrices', f'{genre}_matrix.fmm'), 'rb') as file:
                self.matrices[genre] = pickle.load(file)
        self.lock.release()

    def calculate_similarity(self, pdf: SubgenrePdf) -> dict[str, float]:
        self.lock.acquire()
        matrix = self.matrices[pdf.get_genre()]
        self.lock.release()

        subgenres = pdf.get_keys()
        probabilities = {}
        for subgenre in subgenres:
            probabilities[subgenre] = 0
        for subgenre1 in subgenres:
            current_probability = pdf.get_value(subgenre1)

            for subgenre2 in subgenres:
                pair = CommutativePair(subgenre1, subgenre2)
                probabilities[subgenre2] += current_probability * matrix[pair]

        return probabilities


