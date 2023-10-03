import torch
from torch import nn


class GenreClassifier(nn.Module):
    def __init__(self, in_features=256, dropout_rate=0.7, out_features=10, hidden_layers=2, hidden_size=64):
        super(GenreClassifier, self).__init__()

        layers = []
        in_features = in_features

        # multiplicity = 1
        for i in range(hidden_layers):
            layers.append(nn.Linear(in_features, hidden_size))
            layers.append(nn.GELU())
            layers.append(nn.Dropout(dropout_rate))
            in_features = hidden_size
            hidden_size //= 2
            # multiplicity *= 2
        self.hidden_layers = nn.Sequential(*layers)
        self.output_layer = nn.Linear(in_features, out_features)
        self.classifier = nn.Softmax(dim=1)

    def forward(self, inputs):
        output = self.hidden_layers(inputs)
        output = self.output_layer(output)
        return self.classifier(output)

    def save(self, path):
        torch.save(self.state_dict(), path)

    def load(self, path, device=torch.device('cpu')):
        self.load_state_dict(torch.load(path, map_location=device))
