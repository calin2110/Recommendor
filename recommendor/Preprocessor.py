import concurrent.futures as cf
import os
import threading

import librosa
import numpy as np
import pandas as pd

from interpreters.AudioFileInterpreter import AudioFileInterpreter
from normalizers.Normalizer import Normalizer


def print_safe(text, lock):
    lock.acquire()
    print(text)
    lock.release()


class Preprocessor:
    def __init__(self, interpreter: AudioFileInterpreter, normalizer: Normalizer):
        self.__interpreter = interpreter
        self.__normalizer = normalizer

    def load_normalizer(self, file):
        self.__normalizer.load_stats(file)

    def save_normalizer(self, file):
        self.__normalizer.save_stats(file)

    def preprocess_file(self, interpreted_items, file_paths, file_to_process, index, audio_folder, print_lock):
        path = os.path.join(audio_folder, file_to_process)
        data, sr = librosa.load(path)
        # print_safe(f'Interpreting {file_to_process}', print_lock)
        current = self.__interpreter(sr, data)
        # print_safe(f'Interpreted {file_to_process}', print_lock)
        if current.shape[0] != 128:
            raise Exception('Inconsistent shape')
        interpreted_items[index] = current
        file_paths[index] = file_to_process

    def save_preprocessed_file(self, file_path, normalized_value, save_folder):
        path = f'{file_path[:-4]}.{self.__interpreter.extension()}'
        path = os.path.join(save_folder, path)
        np.save(path, normalized_value)

    def preprocess_population(
            self,
            genres_path,
            audio_folder,
            save_folder,
            stats_file,
            thread_count=os.cpu_count()
    ):
        # open genres_path as a CSV file
        files = pd.read_csv(genres_path)['filename'].tolist()
        interpreted_items = [None for _ in files]
        file_paths = [None for _ in files]

        with cf.ThreadPoolExecutor(max_workers=thread_count) as executor:
            futures = []
            print_lock = threading.Lock()
            for i, file in enumerate(files):
                futures.append(
                    executor.submit(
                        self.preprocess_file,
                        interpreted_items,
                        file_paths,
                        file,
                        i,
                        audio_folder,
                        print_lock
                    )
                )

            cf.wait(futures)

            interpreted_items = np.array(interpreted_items)
            normalized = self.__normalizer(interpreted_items)

            futures = []
            for i, path in enumerate(file_paths):
                futures.append(
                    executor.submit(
                        self.save_preprocessed_file,
                        path,
                        normalized[i],
                        save_folder
                    )
                )

                cf.wait(futures)

            self.__normalizer.save_stats(stats_file)
