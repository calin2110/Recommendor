import argparse
import os

import numpy as np
import pandas as pd
import torch

from runners.shared import load_transformer


def setup_args():
    parser = argparse.ArgumentParser(description='Encodes the data using a transformer model')
    parser.add_argument('--setup-file', type=str, default='../checkpoints/Transformer3Setup.properties')
    parser.add_argument('--tags-file', type=str, default='../../tags/out_genres.csv')
    parser.add_argument('--initial-extension', type=str, default='.wav')
    parser.add_argument('--extension', type=str, default='.mel.npy')
    parser.add_argument('--unencoded-data-folder', type=str, default='../data/minmax-mel-data')
    parser.add_argument('--encoded-data-folder', type=str, default='../data/encoded-data')
    return parser


def encode_existing_data():
    args = setup_args().parse_args()
    model = load_transformer(args.setup_file, patch_probability=0)
    files = pd.read_csv(args.tags_file)['filename'].tolist()
    for file in files:
        file = file.replace(args.initial_extension, args.extension)
        norm_data = np.load(os.path.join(args.unencoded_data_folder, file))
        norm_data = np.expand_dims(norm_data, axis=0)
        norm_data = torch.from_numpy(norm_data)
        # desequence and take the vector
        encoded_data = model.encode(norm_data)[0][0]
        np.save(os.path.join(args.encoded_data_folder, file), encoded_data.detach().numpy())


if __name__ == '__main__':
    encode_existing_data()
