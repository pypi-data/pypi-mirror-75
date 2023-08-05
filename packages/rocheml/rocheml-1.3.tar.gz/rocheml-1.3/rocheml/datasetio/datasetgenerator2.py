from skimage.io import imread
from skimage.transform import resize
import numpy as np
import math
import h5py
from tensorflow.keras.utils import Sequence

# Here, `x_set` is list of path to the images
# and `y_set` are the associated classes.


class DatasetGemeratpr2(Sequence):
    def __init__(self, db_file_path, dataset_name, x_key, y_key, batch_size,
                 preprocessors):
        self.db = h5py.File(db_file_path, "r")
        self.dataset = self.db[dataset_name]
        self.x_key = x_key
        self.y_key = y_key
        self.batch_size = batch_size
        self.preprocessors = preprocessors

    def __len__(self):
        return math.ceil(self.dataset.shape[0] / self.batch_size)

    def __getitem__(self, idx):
        batch_x = self.dataset[idx * self.batch_size:(idx + 1) *
                               self.batch_size][self.x_key]
        batch_y = self.dataset[idx * self.batch_size:(idx + 1) *
                               self.batch_size][self.y_key]

        # TODO: See Trey Hunner's way of making this prettier with a list comprehension
        batch_x_pp = []
        for x in batch_x:
            for pp in preprocessors:
                x = pp.preprocess(x)
            batch_x_pp.append(x)

        return np.array([
            resize(imread(file_name), (200, 200)) for file_name in batch_x
        ]), np.array(batch_y)
