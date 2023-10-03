import torch
from torch.utils.data import DataLoader

from model.LabeledDataset import LabeledDataset
from model.LearnableClustering import LearnableClustering
from model.LearnableClusteringTrainer import LearnableClusteringTrainer
from model.WeightableNorms import LpNorm
from runners.shared import setup_args


def setup_specific_args():
    args = setup_args()
    args.add_argument('--label-column', type=str, default='specific genre', help='The column in the csv file that contains the labels')
    args.add_argument('--genre-file-template', type=str, default='../../tags/{}_out_genres.csv', help='The template for the file that contains the genres')
    args.add_argument('--current-genre', type=str, required=True, help='The genre that is being trained')
    args.add_argument('--p', type=int, default=2, help='The p value for the norm function')
    args.add_argument('--num-features', type=int, default=128, help='The number of features in the data')
    return args


def train():
    args = setup_specific_args().parse_args()
    if args.p < 1:
        raise ValueError('p must be greater than or equal to 1')
    norm_used = LpNorm(args.p)

    train_dataset = LabeledDataset(
        csv_file=args.genre_file_template.format(args.current_genre),
        root_dir=args.data_folder,
        extension=args.extension,
        dataset_type=0,
        label_column=args.label_column
    )
    learnable_clustering = LearnableClustering(norm_fn=norm_used, tags=train_dataset.tags, num_features=args.num_features)

    train_size = len(train_dataset)
    train_loader = DataLoader(train_dataset, batch_size=train_size, shuffle=False)

    # fit the data
    batch, labels = next(iter(train_loader))
    learnable_clustering.fit(batch, labels)

    train_loader = DataLoader(train_dataset, batch_size=args.batch_size, shuffle=True)

    validation_dataset = LabeledDataset(
        csv_file=args.genre_file_template.format(args.current_genre),
        root_dir=args.data_folder,
        extension=args.extension,
        dataset_type=1,
        label_column=args.label_column
    )
    validation_loader = DataLoader(validation_dataset, batch_size=args.batch_size, shuffle=True)

    test_dataset = LabeledDataset(
        csv_file=args.genre_file_template.format(args.current_genre),
        root_dir=args.data_folder,
        extension=args.extension,
        dataset_type=2,
        label_column=args.label_column
    )
    test_loader = DataLoader(test_dataset, batch_size=args.batch_size, shuffle=True)

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    optimizer = torch.optim.Adam(learnable_clustering.parameters(), lr=args.learning_rate)
    scheduler = torch.optim.lr_scheduler.StepLR(
        optimizer=optimizer,
        step_size=args.scheduler_step_size,
        gamma=args.scheduler_gamma
    )

    learnable_clustering_training = LearnableClusteringTrainer(
        model=learnable_clustering,
        train_loader=train_loader,
        validation_loader=validation_loader,
        test_loader=test_loader,
        device=device,
        loss_fn=torch.nn.CrossEntropyLoss(),
        optimizer=optimizer,
        scheduler=scheduler
    )

    learnable_clustering_training.train(epochs=args.epochs, save_interval=args.save_interval, genre=args.current_genre)


if __name__ == '__main__':
    train()
