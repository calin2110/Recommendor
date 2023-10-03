import os

import torch
from torch.utils.data import DataLoader

from shared import load_transformer
from model.UnlabeledDataset import UnlabeledDataset
from model.UnsupervisedTrainer import UnsupervisedTrainer
from runners.shared import setup_args


def setup_specific_args():
    args = setup_args()
    args.add_argument('--transformer-model', type=str, help='The model to specialize', required=True)
    return args


def specialize_model():
    args = setup_specific_args().parse_args()
    dataset = UnlabeledDataset(
        csv_file=args.csv_file,
        root_dir=args.data_folder,
        extension=args.extension
    )
    data_loader = DataLoader(dataset, batch_size=args.batch_size, shuffle=True)

    model = load_transformer(args.transformer_model)

    optimizer = torch.optim.Adam(params=model.parameters(), lr=args.learning_rate)
    loss_fn = torch.nn.MSELoss()
    scheduler = torch.optim.lr_scheduler.StepLR(
        optimizer=optimizer,
        step_size=args.scheduler_step_size,
        gamma=args.scheduler_gamma
    )

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(device)
    trainer = UnsupervisedTrainer(model=model, optimizer=optimizer, loss_fn=loss_fn, scheduler=scheduler, device=device)
    trainer.train(
        data_loader=data_loader,
        epochs=args.epochs,
        save_interval=args.save_interval
    )


if __name__ == '__main__':
    specialize_model()
