import argparse
import configparser

import torch
from torchvision.transforms import Compose

from model.AudioTransformer import AudioTransformer
from transforms.Flattener import Flattener, UndoFlattener
from transforms.PatchMasker import PatchMasker
from transforms.Sequencer import Sequencer, UndoSequencer


def setup_args():
    parser = argparse.ArgumentParser(description='Setup arguments for different purposes')
    parser.add_argument('--batch-size', type=int, default=256, help='The batch size')
    parser.add_argument('--patch-width', type=int, default=64, help='The width of the patches')
    parser.add_argument('--patch-height', type=int, default=32, help='The height of the patches')
    parser.add_argument('--patch-probability', type=float, default=0.1, help='The probability of a patch being masked')
    parser.add_argument('--sequence-length', type=int, default=1, help='The length of the sequence')
    parser.add_argument('--kernel-size', type=int, default=5, help='The kernel size of the transformer')
    parser.add_argument('--stride', type=int, default=3, help='The stride of the transformer')
    parser.add_argument('--hidden-size', type=int, default=256, help='The hidden size of the transformer')
    parser.add_argument('--dropout-rate', type=float, default=0.7, help='The dropout rate of the transformer')
    parser.add_argument('--num-layers', type=int, default=4, help='The number of layers in the transformer')
    parser.add_argument('--num-heads', type=int, default=8, help='The number of heads in the transformer')
    parser.add_argument('--input-height', type=int, default=128, help='The height of the input')
    parser.add_argument('--input-width', type=int, default=1292, help='The width of the input')
    parser.add_argument('--learning-rate', type=float, default=0.001, help='The learning rate')
    parser.add_argument('--scheduler-step-size', type=int, default=500, help='The step size of the scheduler')
    parser.add_argument('--scheduler-gamma', type=float, default=0.1, help='The gamma of the scheduler')
    parser.add_argument('--save-interval', type=int, default=500, help='The interval at which to save the model')
    parser.add_argument('--epochs', type=int, default=2000, help='The number of epochs to train for')
    parser.add_argument('--extension', type=str, default='mel.npy', help='The extension of the data files')
    parser.add_argument('--data-folder', type=str, help='The folder where the data is located', required=True)
    parser.add_argument('--csv-file', type=str, default='../../tags/out_genres.csv', help='The csv file containing labeled data')
    return parser


def load_transformer(properties_file, patch_probability=None, device=torch.device('cpu')):
    config = configparser.ConfigParser()
    config.read(properties_file)
    patch_width = config.getint('Patch', 'patch_width')
    patch_height = config.getint('Patch', 'patch_height')

    if patch_probability is None:
        patch_probability = config.getfloat('Patch', 'patch_probability')

    sequence_length = config.getint('Sequencer', 'sequence_length')
    input_width = config.getint('Input', 'input_width')
    input_height = config.getint('Input', 'input_height')
    hidden_size = config.getint('Transformer', 'hidden_size')
    num_layers = config.getint('Transformer', 'num_layers')
    num_heads = config.getint('Transformer', 'num_heads')
    kernel_size = config.getint('Convolution', 'kernel_size')
    stride = config.getint('Convolution', 'stride')
    dropout_rate = config.getfloat('Transformer', 'dropout_rate')
    model_file = config.get('Transformer', 'path')

    flattener_memory = []
    transform = Compose([
        PatchMasker(
            patch_width=patch_width,
            patch_height=patch_height,
            probability=patch_probability
        ),
        Flattener(memory=flattener_memory),
        Sequencer(sequence_length=sequence_length),
    ])
    undo_transform = Compose([
        UndoSequencer(),
        UndoFlattener(memory=flattener_memory,
                      original_shape=(input_height, input_width))
    ])

    model = AudioTransformer(
        input_width=input_width,
        input_height=input_height,
        hidden_size=hidden_size,
        num_layers=num_layers,
        num_heads=num_heads,
        pre_transforms=transform,
        post_transforms=undo_transform,
        kernel_size=kernel_size,
        stride=stride,
        dropout_rate=dropout_rate
    )
    model.load(model_file, device=device)
    return model
