""" BorisDataset """

import os
from typing import List

import torch.utils.data as data
import torchvision.datasets as datasets

from boris.data._helpers import _load_dataset
from boris.data._helpers import DatasetFolder


class BorisDataset(data.Dataset):
    """ Provides a uniform data interface for the embedding models.

    """

    def __init__(self, root='',
                 name='cifar10',
                 train=True,
                 download=True,
                 transform=None,
                 from_folder=''):
        """ Constructor

        Args:
            root: (str) Directory where dataset is stored
            name: (str) Name of the dataset (e.g. cifar10, cifar100)
            train: (bool) Use the training set
            download: (bool) Download the dataset
            transform: (torchvision.transforms.Compose) image transformations
            from_folder: (str) Path to directory holding the images to load.

        Raises:
            ValueError: If the specified dataset doesn't exist

        """

        super(BorisDataset, self).__init__()
        self.dataset = _load_dataset(
            root, name, train, download, transform, from_folder
        )
        self.root_folder = None
        if from_folder:
            self.root_folder = from_folder

    def get_filenames(self) -> List[str]:
        """Returns a list of filenames
        """
        list_of_filenames = []
        for index in range(len(self)):
            fname = self._get_filename_by_index(index)
            list_of_filenames.append(fname)
        return list_of_filenames

    def _get_filename_by_index(self, index) -> str:
        """Returns filename based on index
        """
        if isinstance(self.dataset, datasets.ImageFolder):
            full_path = self.dataset.imgs[index][0]
            return os.path.relpath(full_path, self.root_folder)
        elif isinstance(self.dataset, DatasetFolder):
            full_path = self.dataset.samples[index][0]
            return os.path.relpath(full_path, self.root_folder)
        else:
            return str(index)

    def __getitem__(self, index):
        """ Get item at index. Supports torchvision.ImageFolder datasets and
            all dataset which return the tuple (sample, target).

        Args:
         - index:   index of the queried item

        Returns:
         - sample:  sample at queried index
         - target:  class_index of target class, 0 if there is no target
         - fname:   filename of the sample, str(index) if there is no filename

        """
        fname = self._get_filename_by_index(index)
        sample, target = self.dataset.__getitem__(index)
        return sample, target, fname

    def __len__(self):
        """ Length of the dataset
        """
        return len(self.dataset)

    def __add__(self, other):
        """ Add element to dataset
        """
        raise NotImplementedError()
