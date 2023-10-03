import numpy as np
import torch
from torch import nn

from model.WeightableNorms import WeightableNorm


class LearnableClustering(nn.Module):
    def __init__(self, norm_fn: WeightableNorm, tags, num_features):
        super(LearnableClustering, self).__init__()
        self.norm_fn = norm_fn
        self.tags = torch.unique(tags)
        self.weights = nn.Parameter(torch.Tensor(1, num_features))
        nn.init.xavier_uniform_(self.weights)
        self.centers = None
        self.output_layer = nn.Softmax(dim=1)

    def fit(self, points, tags):
        self.centers = torch.zeros((len(self.tags), points.shape[1]))
        for i, tag in enumerate(self.tags):
            tag_points = points[tags == tag]
            center = torch.mean(tag_points, dim=0)
            self.centers[i] = center

    def forward(self, data):
        if self.centers is None:
            raise Exception("Centers not computed, please call fit first!")

        result = self.norm_fn(data, self.centers, self.weights)
        result = self.output_layer(result)
        return result

    def save(self, path):
        np.save(path + '_centers.npy', self.centers.detach().numpy())
        torch.save(self.state_dict(), f'{path}_weights.pt')

    def load(self, path):
        self.load_state_dict(torch.load(f'{path}_weights.pt'))
        self.centers = torch.from_numpy(np.load(path + '_centers.npy'))
