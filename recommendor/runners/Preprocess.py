import argparse
import os
import time

from Preprocessor import Preprocessor
from interpreters.MelSpectrogramInterpreter import MelSpectrogramInterpreter
from normalizers.MinMaxNormalizer import MinMaxNormalizer
from normalizers.NoNormalizer import NoNormalizer
from normalizers.ZScoreNormalizer import ZScoreNormalizer
from runners.shared import load_transformer


def setup_args():
    parser = argparse.ArgumentParser(description='Preprocesses the data')
    parser.add_argument('--n-fft', type=int, default=2048, help='The number of FFTs to use')
    parser.add_argument('--hop-length', type=int, default=512, help='The hop length to use')
    parser.add_argument('--n-mels', type=int, default=128, help='The number of mel bins to use')
    parser.add_argument('--normalizer', type=str, default='minmax', help='The normalizer to use')
    parser.add_argument('--timer', type=bool, default=True, help='Whether to time the preprocessing')
    parser.add_argument('--genres-path', type=str, default=os.path.join('..', '..', 'tags', 'out_genres.csv'), help='The path to the genres csv file')
    parser.add_argument('--audio-folder', type=str, default=os.path.join('..', '..', 'data'), help='The path to the audio folder')
    parser.add_argument('--save-folder', type=str, help='The path to the save folder', required=True)
    parser.add_argument('--stats-file', type=str, help='The path to the stats file', required=True)
    parser.add_argument('--thread-count', type=int, default=7, help='The number of threads to use')
    return parser


def get_normalizer(normalizer):
    if normalizer == 'minmax':
        return MinMaxNormalizer()
    if normalizer == 'zscore':
        return ZScoreNormalizer()
    if normalizer == 'none':
        return NoNormalizer()
    raise ValueError(f'Unknown normalizer {normalizer}')


def preprocess_data():
    args = setup_args().parse_args()
    interpreter = MelSpectrogramInterpreter(n_fft=args.n_fft, hop_length=args.hop_length, n_mels=args.n_mels)

    preprocessor = Preprocessor(normalizer=get_normalizer(args.normalizer), interpreter=interpreter)

    start = None
    if args.timer:
        start = time.time()
        print(f'Started timer at f{start}')
    preprocessor.preprocess_population(
        genres_path=args.genres_path,
        audio_folder=args.audio_folder,
        save_folder=args.save_folder,
        stats_file=args.stats_file,
        thread_count=args.thread_count
    )

    if args.timer:
        end = time.time()
        print(f'Ended timer at {end}')
        print('Preprocessing took {} seconds'.format(end - start))


if __name__ == "__main__":
    preprocess_data()
