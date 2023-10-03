import librosa
import torch

from SubgenrePdf import SubgenrePdf
from recommendor.interpreters.MelSpectrogramInterpreter import MelSpectrogramInterpreter
from recommendor.model.AudioTransformer import AudioTransformer
from recommendor.model.GenreClassifier import GenreClassifier
from recommendor.model.LearnableClustering import LearnableClustering
from recommendor.normalizers.MinMaxNormalizer import MinMaxNormalizer
import torch.nn.functional as F


class MusicClassifier:
    def __init__(
            self,
            interpreter: MelSpectrogramInterpreter,
            normalizer: MinMaxNormalizer,
            encoder: AudioTransformer,
            genre_classifier: GenreClassifier,
            subgenre_classifiers: dict[int, LearnableClustering],
            genre_list: dict[int, str],
            subgenre_list: dict[int, dict[int, str]]
    ):
        self.interpreter = interpreter
        self.normalizer = normalizer
        self.encoder = encoder
        self.genre_classifier = genre_classifier
        self.subgenre_classifiers = subgenre_classifiers
        self.subgenre_list = subgenre_list
        self.genre_list = genre_list

        # freeze the params of all models
        for param in encoder.parameters():
            param.requires_grad = False
        for param in genre_classifier.parameters():
            param.requires_grad = False
        for subgenre_classifier in subgenre_classifiers.values():
            for param in subgenre_classifier.parameters():
                param.requires_grad = False

    def __limit_pdf(self, subgenre_pdf: SubgenrePdf, limit: int) -> SubgenrePdf:
        if limit == -1 or limit >= len(subgenre_pdf.get_keys()):
            return subgenre_pdf
        sorted_pdf = sorted(subgenre_pdf.get_items(), key=lambda x: x[1], reverse=True)
        sorted_pdf = sorted_pdf[:limit]

        saved_values = [prob[1] for prob in sorted_pdf]
        total_sum = sum(saved_values)
        new_pdf = {}
        for key, value in sorted_pdf:
            new_pdf[key] = value / total_sum
        return SubgenrePdf(genre=subgenre_pdf.get_genre(), pdf=new_pdf)

    def __classify(self, filepath: str) -> SubgenrePdf:
        loaded_data, sr = librosa.load(filepath)
        interpreted = self.interpreter(srate=sr, data=loaded_data)
        normalized = self.normalizer(data=interpreted)

        data = torch.tensor(normalized)
        data = self.split(data, (128, 1292))
        encoded_data = self.encoder.encode(data)
        encoded_data = encoded_data.squeeze(0)
        genre_vector = self.genre_classifier(inputs=encoded_data)
        # add the batches, then take the argmax
        added_genre_vector = torch.sum(genre_vector, dim=0)
        genre = torch.argmax(added_genre_vector).item()

        subgenre_probabilities = self.subgenre_classifiers[genre](encoded_data)
        subgenre_probabilities = torch.mean(subgenre_probabilities, dim=0)
        # average it out before creating the PDF
        pdf = {}

        for idx, probability in enumerate(subgenre_probabilities):
            subgenre_name = self.subgenre_list[genre][idx]
            pdf[subgenre_name] = probability.item()

        genre = self.genre_list[genre].upper()
        genre = genre.replace('-', '_')
        return SubgenrePdf(genre=genre, pdf=pdf)

    # data is a numpy array of the size [selected_height, width]
    # split it in several arrays of the size [selected_height, selected_width]
    # if width < selected_width, pad the data with zeros on the right
    def split(self, data, selected_shape):
        height, width = data.shape
        selected_height, selected_width = selected_shape
        assert height == selected_height

        parts = []
        if width < selected_width:
            data = F.pad(data, (0, selected_width - width), value=0)
            parts.append(data)

        else:
            num_parts = width // selected_width if width % selected_width == 0 else width // selected_width + 1
            parts = []
            for i in range(num_parts):
                start = i * selected_width
                end = min((i + 1) * selected_width, width)
                if start == end:
                    continue

                if end - start < selected_width:
                    start = end - selected_width
                part = data[:, start:end]
                parts.append(part)
        return torch.stack(parts)

    def get_pdf(self, limit, file) -> SubgenrePdf:
        # classify and limit the pdf
        subgenre_pdf = self.__classify(file)
        subgenre_pdf = self.__limit_pdf(subgenre_pdf, limit)
        return subgenre_pdf
