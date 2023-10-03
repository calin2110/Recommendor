import argparse
import configparser

import pandas as pd
import torch
from torchvision.transforms import Compose

from AudioDownloader import AudioDownloader
from AudioFilesDao import AudioFilesDao
from MusicClassifier import MusicClassifier
from MusicRecommender import MusicRecommender
from Server import Server
from SimilarityCalculator import SimilarityNormalCalculator
from SimilarityFilter import SimilarityFilter
from recommendor.interpreters.MelSpectrogramInterpreter import MelSpectrogramInterpreter
from recommendor.model.AudioTransformer import AudioTransformer
from recommendor.model.GenreClassifier import GenreClassifier
from recommendor.model.LearnableClustering import LearnableClustering
from recommendor.model.WeightableNorms import LpNorm
from recommendor.normalizers.MinMaxNormalizer import MinMaxNormalizer
from recommendor.transforms.Flattener import Flattener
from recommendor.transforms.Sequencer import Sequencer
from shared.CommutativePair import CommutativePair


def setup_interpreter(config):
    n_mels = config.getint('Interpreter', 'n_mels')
    hop_length = config.getint('Interpreter', 'hop_length')
    n_fft = config.getint('Interpreter', 'n_fft')
    return MelSpectrogramInterpreter(n_fft=n_fft, hop_length=hop_length, n_mels=n_mels)


def setup_normalizer(config):
    normalizer = MinMaxNormalizer()
    stats_file = config.get('Normalizer', 'stats_file')
    normalizer.load_stats(stats_file)
    return normalizer


def setup_encoder(config):
    sequence_length = config.getint('Transformer', 'sequence_length')
    input_width = config.getint('Transformer', 'input_width')
    input_height = config.getint('Transformer', 'input_height')
    hidden_size = config.getint('Transformer', 'transformer_hidden_size')
    num_layers = config.getint('Transformer', 'transformer_layers')
    num_heads = config.getint('Transformer', 'transformer_heads')
    kernel_size = config.getint('Transformer', 'kernel_size')
    stride = config.getint('Transformer', 'stride')
    model_file = config.get('Transformer', 'transformer_path')

    flattener_memory = []
    transform = Compose([
        Flattener(memory=flattener_memory),
        Sequencer(sequence_length=sequence_length),
    ])

    model = AudioTransformer(
        input_width=input_width,
        input_height=input_height,
        hidden_size=hidden_size,
        num_layers=num_layers,
        num_heads=num_heads,
        pre_transforms=transform,
        post_transforms=None,
        kernel_size=kernel_size,
        stride=stride,
        dropout_rate=0
    )
    model.load(model_file)
    return model


def setup_genre_classifier(config):
    in_features = config.getint('GenreClassifier', 'classifier_in_features')
    hidden_size = config.getint('GenreClassifier', 'classifier_units')
    hidden_layers = config.getint('GenreClassifier', 'classifier_layers')
    out_features = config.getint('GenreClassifier', 'classifier_out_features')
    model_file = config.get('GenreClassifier', 'classifier_path')

    model = GenreClassifier(
        in_features=in_features,
        hidden_size=hidden_size,
        dropout_rate=0,
        hidden_layers=hidden_layers,
        out_features=out_features
    )
    model.load(model_file)
    return model


def setup_genres(config):
    genres_file = config.get('Genres', 'genres_file')
    genre_column = config.get('Genres', 'genre_column')
    df = pd.read_csv(genres_file)
    tags = [tag for tag in df[genre_column]]
    tags = sorted(set(tags))

    genres = {}
    subgenres = {}
    for idx, genre in enumerate(tags):
        genres[idx] = genre
        subgenres[idx] = {}

        subgenres_template = config.get('Genres', 'subgenres_template_csv')
        subgenres_template = subgenres_template.format(genre)
        subgenres_df = pd.read_csv(subgenres_template)
        subgenre_column = config.get('Genres', 'subgenre_column')
        subtags = [tag for tag in subgenres_df[subgenre_column]]
        subtags = sorted(set(subtags))
        for subtag_idx, subtag in enumerate(subtags):
            subgenres[idx][subtag_idx] = subtag

    return genres, subgenres


def setup_args():
    args = argparse.ArgumentParser()
    args.add_argument('--config-file', type=str, default='../models/RecommendorSetup.properties')
    return args.parse_args()


def setup_subgenre_classifiers(config, genre_list, subgenre_list):
    learnable_clusterings = {}
    for key in genre_list:
        value = genre_list[key]
        folder = config.get('SubgenreClassifiers', 'subgenres_folder')
        template = f'{folder}/{value}'
        input_size = config.getint('SubgenreClassifiers', 'subgenres_in_features')
        p = config.getfloat('SubgenreClassifiers', 'p')
        norm_fn = LpNorm(p=p)

        tags_tensor = torch.tensor(list(subgenre_list[key].keys()))
        learnable_clustering = LearnableClustering(norm_fn=norm_fn, num_features=input_size,
                                                   tags=tags_tensor)
        learnable_clustering.load(template)
        learnable_clusterings[key] = learnable_clustering
    return learnable_clusterings


def run():
    config_file = setup_args().config_file
    config = configparser.ConfigParser()
    config.read(config_file)
    interpreter = setup_interpreter(config)
    print('Interpreter loaded')
    normalizer = setup_normalizer(config)
    print('Normalizer loaded')
    encoder = setup_encoder(config)
    print('Encoder loaded')
    genre_classifier = setup_genre_classifier(config)
    print('Genre classifier loaded')
    genre_list, subgenre_list = setup_genres(config)
    print('Genres loaded')
    subgenre_classifiers = setup_subgenre_classifiers(config, genre_list, subgenre_list)
    print('Subgenre classifiers loaded')

    classifier = MusicClassifier(
        interpreter=interpreter,
        normalizer=normalizer,
        encoder=encoder,
        genre_classifier=genre_classifier,
        subgenre_classifiers=subgenre_classifiers,
        genre_list=genre_list,
        subgenre_list=subgenre_list
    )
    downloader = AudioDownloader()
    dao = AudioFilesDao()
    similarity_calculator = SimilarityNormalCalculator()
    similarity_filter = SimilarityFilter()
    recommender = MusicRecommender(audio_downloader=downloader,
                                   music_classifier=classifier,
                                   similarity_calculator=similarity_calculator,
                                   similarity_filter=similarity_filter,
                                   audio_files_dao=dao
                                   )
    server = Server(music_recommender=recommender, similarity_calculator=similarity_calculator)
    print('Server listening!')
    server.run()


if __name__ == "__main__":
    run()
