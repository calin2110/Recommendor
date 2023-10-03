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


def train_model():
    args = setup_args().parse_args()
    dataset = UnlabeledDataset(
        csv_file=args.csv_file,
        root_dir=args.data_folder,
        extension=args.extension
    )
    data_loader = DataLoader(dataset, batch_size=args.batch_size, shuffle=True)

    flattener_memory = []
    transform = Compose([
        PatchMasker(
            patch_width=args.patch_width,
            patch_height=args.patch_height,
            probability=args.patch_probability
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
        hidden_size=args.hidden_size,
        num_layers=args.num_layers,
        num_heads=args.num_heads,
        pre_transforms=transform,
        post_transforms=undo_transform,
        kernel_size=args.kernel_size,
        stride=args.stride,
        dropout_rate=args.dropout_rate
    )

    # optimizer = torch.optim.AdamW(params=model.parameters(), lr=hp.learning_rate)
    optimizer = torch.optim.Adam(params=model.parameters(), lr=args.learning_rate)
    loss_fn = torch.nn.MSELoss()
    scheduler = torch.optim.lr_scheduler.StepLR(
        optimizer=optimizer,
        step_size=args.scheduler_step_size,
        gamma=args.scheduler_gamma)

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(device)
    trainer = UnsupervisedTrainer(model=model, optimizer=optimizer, loss_fn=loss_fn, scheduler=scheduler, device=device)

    trainer.train(
        data_loader=data_loader,
        epochs=args.epochs,
        save_interval=args.save_interval
    )


if __name__ == '__main__':
    train_model()
