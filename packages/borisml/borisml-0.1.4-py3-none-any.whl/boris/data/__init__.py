""" boris.data

    The boris.data module provides a dataset wrapper
    and useful collate functions for self-supervised learning
    (see torch.utils.data.DataLoader for details on collate_fn)

"""

from ._dataset import BorisDataset
from ._collate import BaseCollateFunction
from ._collate import ImageCollateFunction
