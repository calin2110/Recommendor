import os

import numpy as np
import pandas as pd
import torch
from torch.utils.data import Dataset


class LabeledDataset(Dataset):
    def __init__(self, root_dir, csv_file, extension, dataset_type, label_column):
        super().__init__()
        self.root_dir = root_dir
        self.csv_file = csv_file
        self.extension = extension
        df = pd.read_csv(csv_file)
        filtered_df = df[df['type'] == dataset_type]
        self.files = [os.path.join(root_dir, path[:-4] + '.' + extension) for path in filtered_df['filename']]
        self.tags = [tag for tag in filtered_df[label_column]]
        possible_tags = set(self.tags)
        possible_tags = sorted(possible_tags)
        self.tags = [possible_tags.index(tag) for tag in self.tags]
        self.tags = torch.tensor(self.tags)

    def __getitem__(self, index):
        return np.load(self.files[index]), self.tags[index]

    def __len__(self):
        return len(self.files)
