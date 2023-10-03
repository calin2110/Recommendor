import torch
from matplotlib import pyplot as plt

from model.GenreClassifier import GenreClassifier


class GenreClassifierTrainer(object):
    def __init__(self, model: GenreClassifier, train_loader, validation_loader, test_loader, device, loss_fn, optimizer, scheduler=None):
        self.model = model.to(device)
        self.device = device
        self.loss_fn = loss_fn
        self.optimizer = optimizer
        self.scheduler = scheduler
        self.train_loader = train_loader
        self.validate_loader = validation_loader
        self.test_loader = test_loader
        self.losses = []

    def train(self, epochs, filename=None, save_interval=None):
        self.losses = []
        for epoch in range(epochs):
            self.model.train()
            total_loss = 0
            batches = 0
            for batch, labels in self.train_loader:
                batch = batch.to(self.device)
                num_tags = len(torch.unique(self.train_loader.dataset.tags))
                labels = torch.eye(num_tags)[labels].to(self.device)
                self.optimizer.zero_grad()
                output = self.model(batch)

                loss = self.loss_fn(output, labels)
                loss.backward()

                self.optimizer.step()
                total_loss += loss.item()
                batches += 1
            if self.scheduler is not None:
                self.scheduler.step()
            current_loss = total_loss / batches
            self.losses.append(current_loss)
            print(f"Epoch {epoch} average: loss: {current_loss}")
            self.validate()
            if save_interval is not None and (epoch + 1) % save_interval == 0:
                self.model.save(f'../checkpoints/classifier_{epoch}.pt')
        self.test()
        plt.clf()
        x_axis = range(len(self.losses))
        ax = plt.gca()
        ax.set_ylim([0, 2.3])
        plt.plot(x_axis, self.losses)
        if filename is not None:
            plt.savefig(filename)
        else:
            plt.show()

    def validate(self):
        average_loss, accuracy = self.__evaluate(self.validate_loader)
        print(f"Validation average: loss: {average_loss}")
        print(f"Validation accuracy: {accuracy}")

    def test(self):
        average_loss, accuracy = self.__evaluate(self.test_loader)
        print(f"Test average: loss: {average_loss}")
        print(f"Test accuracy: {accuracy}")

    def __evaluate(self, data_loader):
        self.model.eval()
        total_loss = 0
        batches = 0

        correct = 0
        total = 0
        for batch, labels in data_loader:
            batch = batch.to(self.device)
            output = self.model(batch)
            predicted_classes = torch.argmax(output, dim=1)
            for i, label in enumerate(labels):
                if label == predicted_classes[i]:
                    correct += 1

            total += labels.size(0)
            num_tags = len(torch.unique(self.validate_loader.dataset.tags))
            labels = torch.eye(num_tags)[labels].to(self.device)
            loss = self.loss_fn(output, labels)
            total_loss += loss.item()
            batches += 1
        average_loss = total_loss / batches
        accuracy = correct / total
        return average_loss, accuracy
