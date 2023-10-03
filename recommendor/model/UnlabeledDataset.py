import os

import numpy as np
import pandas as pd
from torch.utils.data import Dataset


class UnlabeledDataset(Dataset):
    def __init__(self, root_dir, csv_file, extension):
        super().__init__()
        self.root_dir = root_dir
        self.csv_file = csv_file
        self.extension = extension
        self.files = [os.path.join(root_dir, path[:-4] + '.' + extension) for path in pd.read_csv(csv_file)['filename']]

    def __getitem__(self, index):
        return np.load(self.files[index])

    def __len__(self):
        return len(self.files)
