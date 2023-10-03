import torch


class WeightableNorm:
    def __init__(self):
        pass

    def __call__(self, data, centers, weights):
        pass


class LpNorm(WeightableNorm):
    def __init__(self, p):
        super(LpNorm, self).__init__()
        self.p = p

    def __call__(self, data, centers, weights):
        batch_size, data_size = data.shape
        num_labels, center_data_size = centers.shape
        assert data_size == center_data_size, f"Data size {data_size} and center data size {center_data_size} must be equal!"

        data_expanded = data.unsqueeze(1).expand(batch_size, num_labels, data_size)
        centers_expanded = centers.unsqueeze(0).expand(batch_size, num_labels, data_size)
        result = torch.abs(data_expanded - centers_expanded) ** self.p
        weights_expanded = (weights ** self.p).unsqueeze(0).expand_as(data_expanded)
        result = torch.mul(result, weights_expanded)
        result = torch.sum(result, dim=2)
        result = torch.pow(result, 1 / self.p)
        return result
