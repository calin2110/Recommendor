import itertools
import random

import torch
from torch.utils.data import DataLoader
import numpy as np
from matplotlib import pyplot as plt
from sklearn.metrics import confusion_matrix
from model.GenreClassifier import GenreClassifier
from model.GenreClassifierTrainer import GenreClassifierTrainer
from model.LabeledDataset import LabeledDataset
from runners.shared import load_transformer, setup_args


def setup_specific_args():
    args = setup_args()
    args.add_argument('--classifier-file', type=str, default='../checkpoints/classifier_199.pt',
                      help='The file where the classifier is saved')
    args.add_argument('--label-column', type=str, default='general genre',
                      help='The column in the csv file that contains the labels')
    args.add_argument('--hidden-layers', type=int, default=1, help='The number of hidden layers')
    args.add_argument('--weight-decay', type=float, default=1e-4, help='The weight decay for L2 Regularization')
    args.add_argument('--in-features', type=int, default=128, help='The number of input features')
    args.add_argument('--out-features', type=int, default=10, help='The number of output features')
    return args


def check_similarity():
    args = setup_specific_args().parse_args()
    dataset = LabeledDataset(
        csv_file=args.csv_file,
        root_dir=args.data_folder,
        extension=args.extension,
        dataset_type=0,
        label_column=args.label_column
    )
    data_loader = DataLoader(dataset, batch_size=args.batch_size, shuffle=True)
    model = load_transformer(args.transformer_file)
    for batch, tags in data_loader:
        for i, image in enumerate(batch):
            image = image.unsqueeze(0)
            image = model.encode(image)
            image = image.squeeze(0)
            print(image)
            for j, image2 in enumerate(batch):
                if i != j:
                    image2 = image2.unsqueeze(0)
                    image2 = model.encode(image2)
                    image2 = image2.squeeze(0)
                    # print(torch.cosine_similarity(image, image2))
                    print(torch.cdist(image, image2))
        print(batch[0].shape)
        print(batch[1].shape)
        break


def grid_search_params():
    args = setup_specific_args().parse_args()
    train_dataset = LabeledDataset(
        csv_file=args.csv_file,
        root_dir=args.data_folder,
        extension=args.extension,
        dataset_type=0,
        label_column=args.label_column
    )
    train_loader = DataLoader(train_dataset, batch_size=args.batch_size, shuffle=True)

    validation_dataset = LabeledDataset(
        csv_file=args.csv_file,
        root_dir=args.data_folder,
        extension=args.extension,
        dataset_type=1,
        label_column=args.label_column
    )
    validation_loader = DataLoader(validation_dataset, batch_size=args.batch_size, shuffle=True)

    test_dataset = LabeledDataset(
        csv_file=args.csv_file,
        root_dir=args.data_folder,
        extension=args.extension,
        dataset_type=2,
        label_column=args.label_column
    )
    test_loader = DataLoader(test_dataset, batch_size=args.batch_size, shuffle=True)

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(device)

    dropout_rates = [0, 0.5, 0.7]
    hidden_sizes = [16, 64, 128, 256, 512]
    hidden_layers = [1, 2, 3, 4]
    learning_rates = [1e-2, 1e-3, 1e-4, 1e-5]
    weight_decays = [1e-2, 1e-3, 1e-4, 1e-5]

    combinations = itertools.product(dropout_rates, hidden_sizes, hidden_layers, learning_rates, weight_decays)
    combinations = list(combinations)
    random.shuffle(combinations)
    for dropout_rate, hidden_size, hidden_layer, learning_rate, weight_decay in combinations:
        model = GenreClassifier(
            in_features=args.in_features,
            hidden_size=hidden_size,
            dropout_rate=dropout_rate,
            hidden_layers=hidden_layer,
            out_features=args.out_features
        )

        optimizer = torch.optim.Adam(params=model.parameters(), lr=learning_rate, weight_decay=weight_decay)

        loss_fn = torch.nn.CrossEntropyLoss()
        scheduler = torch.optim.lr_scheduler.StepLR(
            optimizer=optimizer,
            step_size=args.scheduler_step_size,
            gamma=args.scheduler_gamma
        )

        trainer = GenreClassifierTrainer(
            model=model,
            device=device,
            loss_fn=loss_fn,
            optimizer=optimizer,
            scheduler=scheduler,
            train_loader=train_loader,
            validation_loader=validation_loader,
            test_loader=test_loader
        )
        filename = f'../plots/model_{dropout_rate}_{hidden_size}_{hidden_layer}_{learning_rate}_{weight_decay}.png'
        trainer.train(epochs=200, filename=filename)


def train_classifier():
    args = setup_specific_args().parse_args()
    train_dataset = LabeledDataset(
        csv_file=args.csv_file,
        root_dir=args.data_folder,
        extension=args.extension,
        dataset_type=0,
        label_column=args.label_column
    )
    train_loader = DataLoader(train_dataset, batch_size=args.batch_size, shuffle=True)

    validation_dataset = LabeledDataset(
        csv_file=args.csv_file,
        root_dir=args.data_folder,
        extension=args.extension,
        dataset_type=1,
        label_column=args.label_column
    )
    validation_loader = DataLoader(validation_dataset, batch_size=args.batch_size, shuffle=True)

    test_dataset = LabeledDataset(
        csv_file=args.csv_file,
        root_dir=args.data_folder,
        extension=args.extension,
        dataset_type=2,
        label_column=args.label_column
    )
    test_loader = DataLoader(test_dataset, batch_size=args.batch_size, shuffle=True)

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(device)

    model = GenreClassifier(
        in_features=args.in_features,
        hidden_size=args.hidden_size,
        dropout_rate=args.dropout_rate,
        hidden_layers=args.hidden_layers,
        out_features=args.out_features
    )
    print(args.learning_rate)
    optimizer = torch.optim.Adam(params=model.parameters(), lr=args.learning_rate, weight_decay=args.weight_decay)

    loss_fn = torch.nn.CrossEntropyLoss()
    scheduler = torch.optim.lr_scheduler.StepLR(
        optimizer=optimizer,
        step_size=args.scheduler_step_size,
        gamma=args.scheduler_gamma
    )

    trainer = GenreClassifierTrainer(
        model=model,
        device=device,
        loss_fn=loss_fn,
        optimizer=optimizer,
        scheduler=scheduler,
        train_loader=train_loader,
        validation_loader=validation_loader,
        test_loader=test_loader
    )
    trainer.train(epochs=args.epochs, save_interval=args.save_interval)


def print_confusion_matrix():
    args = setup_specific_args().parse_args()
    train_dataset = LabeledDataset(
        csv_file=args.csv_file,
        root_dir=args.data_folder,
        extension=args.extension,
        dataset_type=0,
        label_column=args.label_column
    )
    train_loader = DataLoader(train_dataset, batch_size=256, shuffle=True)
    test_dataset = LabeledDataset(
        csv_file=args.csv_file,
        root_dir=args.data_folder,
        extension=args.extension,
        dataset_type=1,
        label_column=args.label_column
    )
    test_loader = DataLoader(test_dataset, batch_size=256)
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(device)

    model = GenreClassifier(
        in_features=args.in_features,
        hidden_size=args.hidden_size,
        dropout_rate=args.dropout_rate,
        hidden_layers=args.hidden_layers,
        out_features=args.out_features
    )

    model.load(args.classifier_file, device=device)
    model.eval()
    predicted_labels = []
    actual_labels = []
    for batch, labels in test_loader:
        output = model(batch)
        predicted_classes = torch.argmax(output, dim=1)
        for i, label in enumerate(labels):
            predicted_label = predicted_classes[i]
            predicted_labels.append(predicted_label.item())
            actual_label = label.item()
            actual_labels.append(actual_label)
    cm = confusion_matrix(actual_labels, predicted_labels)
    print(cm)
    # Plot the confusion matrix as a heatmap
    fig = plt.figure(figsize=(8, 7))
    plt.imshow(cm, interpolation='nearest', cmap=plt.cm.Blues)
    plt.title('Confusion Matrix')
    plt.colorbar()
    tick_marks = np.arange(10)
    tags = ['blues', 'classical', 'country', 'disco', 'hip-hop', 'jazz', 'metal', 'pop', 'reggae', 'rock']
    plt.xticks(tick_marks, tags, rotation=90)
    plt.yticks(tick_marks, tags)
    plt.xlabel('Predicted Label')
    plt.ylabel('True Label')
    plt.show()


if __name__ == '__main__':
    print_confusion_matrix()
