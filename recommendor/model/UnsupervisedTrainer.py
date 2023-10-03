import os

from model.AudioTransformer import AudioTransformer

import matplotlib.pyplot as plt


class UnsupervisedTrainer(object):
    def __init__(self, model: AudioTransformer, device, optimizer, loss_fn, scheduler=None):
        self.device = device
        self.model = model.to(device)
        self.optimizer = optimizer
        self.loss_fn = loss_fn
        self.scheduler = scheduler
        self.losses = []

    def train_grid_search(self, data_loader, epochs, plot_file):
        self.model.train()
        losses = []
        for epoch in range(epochs):
            total_loss = 0
            batches = 0

            for batch in data_loader:
                batch = batch.to(self.device)
                self.optimizer.zero_grad()
                output = self.model(batch)
                loss = self.loss_fn(output, batch)
                loss.backward()
                total_loss += loss.item()
                batches += 1
                self.optimizer.step()
            if self.scheduler is not None:
                self.scheduler.step()
            losses.append(total_loss / batches)
            print(f"Epoch {epoch} average: loss: {total_loss / batches}")

        plt.clf()
        x_axis = range(len(losses))
        ax = plt.gca()
        ax.set_ylim([0, 0.04])
        plt.plot(x_axis, losses)
        plt.savefig(plot_file)

    def train(self, data_loader, epochs, save_interval):
        self.model.train()
        for epoch in range(epochs):
            total_loss = 0
            batches = 0

            for batch in data_loader:
                batch = batch.to(self.device)
                self.optimizer.zero_grad()
                output = self.model(batch)
                loss = self.loss_fn(output, batch)
                loss.backward()
                total_loss += loss.item()
                batches += 1
                self.optimizer.step()
            if self.scheduler is not None:
                self.scheduler.step()

            if (epoch + 1) % save_interval == 0:
                self.model.save(
                    os.path.join('checkpoints', f'model_{epoch}.pt')
                )
            self.losses.append(total_loss / batches)
            print(f"Epoch {epoch} average: loss: {total_loss / batches}")

        plt.clf()
        x_axis = range(len(self.losses))
        ax = plt.gca()
        ax.set_ylim([0, 0.04])
        plt.plot(x_axis, self.losses)
        plt.show()
