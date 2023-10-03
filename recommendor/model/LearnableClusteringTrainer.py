import torch


class LearnableClusteringTrainer(object):
    def __init__(self, model, train_loader, validation_loader, test_loader, device, loss_fn, optimizer, scheduler=None):
        self.model = model.to(device)
        self.train_loader = train_loader
        self.validate_loader = validation_loader
        self.test_loader = test_loader
        self.device = device
        self.loss_fn = loss_fn
        self.optimizer = optimizer
        self.scheduler = scheduler
        self.losses = []

    def train(self, epochs, save_interval, genre):
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
            if (epoch + 1) % save_interval == 0:
                self.model.save(f"../checkpoints/learnable_clustering_{genre}_{epoch}.pt")
            self.validate()
        self.test()

    def test(self):
        self.model.eval()
        test_loss = self.__evaluate(self.test_loader)
        print(f"Test average: loss: {test_loss}")

    def validate(self):
        self.model.eval()
        validate_loss = self.__evaluate(self.validate_loader)
        print(f"Validation average: loss: {validate_loss}")

    def __evaluate(self, loader):
        total_loss = 0
        batches = 0
        for batch, label in loader:
            batch = batch.to(self.device)
            label = label.to(self.device)
            output = self.model(batch)
            loss = self.loss_fn(output, label)
            total_loss += loss.item()
            batches += 1
        return total_loss / batches
