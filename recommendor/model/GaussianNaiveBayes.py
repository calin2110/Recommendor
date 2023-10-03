import numpy as np
import torch
from scipy.stats import norm


class GaussianNaiveBayes:
    def __init__(self, error=1e-10):
        self.means = None
        self.stds = None
        self.class_probs = None
        self.classes = None
        self.error = error

    def fit(self, X, y):
        self.classes = np.unique(y)
        num_features = X.shape[1]
        self.means = np.zeros((len(self.classes), num_features))
        self.stds = np.zeros((len(self.classes), num_features))
        self.class_probs = np.zeros(len(self.classes))
        for clazz in self.classes:
            X_c = []
            for idx, x in enumerate(X):
                if y[idx] == clazz:
                    X_c.append(x)
            X_c = torch.stack(X_c).numpy()
            self.class_probs[clazz] = len(X_c) / len(X)
            self.means[clazz, :] = np.mean(X_c, axis=0)
            self.stds[clazz, :] = np.std(X_c, axis=0) + self.error

    def predict(self, X):
        probabilities = []
        for data_item in X:
            class_probs = []
            for idx, label in enumerate(self.classes):
                prior = np.log(self.class_probs[idx])
                likelihood = np.prod(norm.pdf(data_item, self.means[idx], self.stds[idx]))
                posterior = prior * likelihood
                class_probs.append(posterior)
            class_probs /= (np.sum(class_probs) + self.error)
            probabilities.append(class_probs)
        return probabilities
