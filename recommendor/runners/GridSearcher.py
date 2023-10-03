import itertools
import os
import random

import torch
from torch.utils.data import DataLoader
from torchvision.transforms import Compose

from model.AudioTransformer import AudioTransformer
from model.UnlabeledDataset import UnlabeledDataset
from model.UnsupervisedTrainer import UnsupervisedTrainer
from runners.shared import setup_args
from transforms.Flattener import Flattener, UndoFlattener
from transforms.PatchMasker import PatchMasker
from transforms.Sequencer import Sequencer, UndoSequencer


def grid_search():
    strides = [1, 2, 3]
    kernel_sizes = [1, 3, 5]
    patch_widths = [32, 64]
    patch_heights = [32, 64]
    patch_probabilities = [0.01, 0.05, 0.1]
    hidden_sizes = [256, 512, 1024]
    num_layers = [4, 8]
    dropout_rates = [0.2, 0.5, 0.7]
    learning_rates = [0.01, 0.001, 0.005]

    combinations = itertools.product(strides, kernel_sizes, patch_widths, patch_heights, patch_probabilities,
                                     hidden_sizes, num_layers, dropout_rates, learning_rates)
    combinations = list(combinations)
    random.shuffle(combinations)

    args = setup_args().parse_args()

    running_epochs = 100
    for combination in combinations:
        stride, kernel_size, patch_width, patch_height, patch_probability, hidden_size, num_layer, dropout_rate, learning_rate = combination

        dataset = UnlabeledDataset(
            csv_file=args.csv_file,
            root_dir=args.data_folder,
            extension=args.extension
        )
        data_loader = DataLoader(dataset, batch_size=args.batch_size, shuffle=True)

        flattener_memory = []
        transform = Compose([
            PatchMasker(
                patch_width=patch_width,
                patch_height=patch_height,
                probability=patch_probability
            ),
            Flattener(memory=flattener_memory),
            Sequencer(sequence_length=args.sequence_length),
        ])

        undo_transform = Compose([
            UndoSequencer(),
            UndoFlattener(memory=flattener_memory, original_shape=(args.input_height, args.input_width))
        ])

        model = AudioTransformer(
            input_width=args.input_width,
            input_height=args.input_height,
            hidden_size=hidden_size,
            num_layers=num_layer,
            num_heads=args.num_heads,
            pre_transforms=transform,
            post_transforms=undo_transform,
            kernel_size=kernel_size,
            stride=stride,
            dropout_rate=dropout_rate
        )

        optimizer = torch.optim.Adam(params=model.parameters(), lr=learning_rate)
        loss_fn = torch.nn.MSELoss()
        scheduler = torch.optim.lr_scheduler.StepLR(
            optimizer=optimizer,
            step_size=args.scheduler_step_size,
            gamma=args.scheduler_gamma)
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        print(device)

        trainer = UnsupervisedTrainer(model=model, optimizer=optimizer, loss_fn=loss_fn,
                                      scheduler=scheduler, device=device)

        plot_dir = 'plots'
        plot_file = 'plot'
        plot_file += f'_str_{stride}'
        plot_file += f'_ker_{kernel_size}'
        plot_file += f'_pw_{patch_width}'
        plot_file += f'_ph_{patch_height}'
        plot_file += f'_pp_{patch_probability}'
        plot_file += f'_hs_{hidden_size}'
        plot_file += f'_nl_{num_layer}'
        plot_file += f'_dr_{dropout_rate}'
        plot_file += f'_lr_{learning_rate}'
        plot_file += '.png'
        trainer.train_grid_search(data_loader=data_loader, epochs=running_epochs, plot_file=os.path.join(plot_dir, plot_file))


if __name__ == '__main__':
    grid_search()
