import os


import pandas as pd

from itertools import islice
from typing import List

from boris.api._communication import create_initial_tag
from boris.api._communication import get_presigned_upload_url
from boris.api._communication import upload_file_with_signed_url
from boris.api._communication import upload_embedding
from boris.api._communication import get_samples
from boris.data import BorisDataset
from boris.utils import pandas_to_dict

import tqdm
import warnings
from concurrent.futures import ThreadPoolExecutor

MAXIMUM_DATASET_SIZE = 10_000


def upload_embeddings_from_csv(path_to_embeddings: str,
                               dataset_id: str,
                               token: str,
                               max_upload: int = 512):
    """Uploads embeddings from a csv file to the cloud solution

    Args:
        path_to_embeddings: Path to csv file containing embeddings
        dataset_id: The unique identifier for the dataset
        token: Token for authentication

    Raises:
        RuntimeError if there is an error during the upload
        of a batch of embeddings
    """
    df = pd.read_csv(path_to_embeddings)
    data = pandas_to_dict(df)

    for embedding in data['embeddings']:
        embedding['fileName'] = os.path.basename(embedding['fileName'])

    data['token'] = token
    data['datasetId'] = dataset_id

    def _upload_single_batch(batch, append=False):
        batch['append'] = int(append)
        upload_embedding(batch)

    n_embeddings = len(data['embeddings'])
    n_batches = n_embeddings // max_upload
    n_batches = n_batches + 1 if n_embeddings % max_upload else n_batches

    embedding_batches = [None] * n_batches
    for i in range(n_batches):
        left = i*max_upload
        right = min((i + 1) * max_upload, n_embeddings)
        batch = data.copy()
        batch['embeddings'] = data['embeddings'][left:right]
        embedding_batches[i] = batch

    pbar = tqdm.tqdm(unit='embs', total=n_embeddings)
    for i, batch in enumerate(embedding_batches):
        _upload_single_batch(batch, append=i > 0)
        pbar.update(len(batch['embeddings']))


def upload_images_from_folder(path_to_folder: str,
                              dataset_id: str,
                              token: str,
                              max_workers: int = 8,
                              max_requests: int = 8):
    """Uploads images from a directory to the cloud solution

    Args:
        path_to_folder: Path to the folder containing the images
        dataset_id: The unique identifier for the dataset
        token: Token for authentication

    """

    bds = BorisDataset(from_folder=path_to_folder)
    fnames = bds.get_filenames()

    if len(fnames) > MAXIMUM_DATASET_SIZE:
        msg = f'Your dataset has {len(fnames)} samples which'
        msg += f'is more than the allowed maximum of {MAXIMUM_DATASET_SIZE}'
        raise ValueError(msg)

    def _upload_single_image(fname):

        success = True
        # try to get signed url
        try:
            basename = fname
            signed_url = get_presigned_upload_url(
                basename, dataset_id, token
            )
        except RuntimeError:
            success = False

        # try to upload image
        try:
            if success:
                full_fname = os.path.join(path_to_folder, fname)
                upload_file_with_signed_url(full_fname, signed_url)
        except RuntimeError:
            success = False

        return success

    n_batches = len(fnames) // max_requests
    n_batches = n_batches + 1 if len(fnames) % max_requests else n_batches
    fname_batches = [
        list(islice(fnames, i * max_requests, (i + 1) * max_requests))
        for i in range(n_batches)
    ]

    chunksize = max(max_requests // max_workers, 1)
    executor = ThreadPoolExecutor(max_workers=max_workers)

    pbar = tqdm.tqdm(unit='imgs', total=len(fnames))
    for i, batch in enumerate(fname_batches):
        mapped = executor.map(_upload_single_image, batch, chunksize=chunksize)
        mapped = list(mapped)
        if not all(mapped):
            msg = 'Warning: Unsuccessful upload(s) in batch {}! '.format(i)
            msg += 'This could cause problems when uploading embeddings.'
            msg += 'Failed at file: {}'.format(mapped.index(False))
            warnings.warn(msg)
        pbar.update(len(batch))
    create_initial_tag(dataset_id, token)


def upload_metadata_from_json(path_to_embeddings: str,
                              dataset_id: str,
                              token: str):
    pass


def get_samples_by_tag(tag_name: str,
                       dataset_id: str,
                       token: str,
                       mode: str = 'list',
                       filenames: List[str] = None):
    """Get the files associated with a given tag and dataset

    Args:
        tag_name: Name of the tag to query
        dataset_id: The unique identifier of the dataset
        token: Token for authentication
        mode: Return type, must be in ["list", "mask", "indices"]
        filenames: List of all filenames

    Returns:
        Either list of filenames, binary mask, or list of indices
        specifying the samples in the requested tag

    Raises: ValueError, RuntimeError

    """

    if mode == 'mask' and filenames is None:
        msg = f'Argument filenames must not be None for mode "{mode}"!'
        raise ValueError(msg)
    if mode == 'indices' and filenames is None:
        msg = f'Argument filenames must not be None for mode "{mode}"!'
        raise ValueError(msg)

    samples = get_samples(dataset_id, token, tag_name=tag_name)

    if mode == 'list':
        return samples

    if mode == 'mask':
        mask = [1 if f in set(samples) else 0 for f in filenames]
        if sum(mask) != len(samples):
            msg = 'Error during mapping from samples to filenames: '
            msg += f'sum(mask) != len(samples) with lengths '
            msg += f'{sum(mask)} and {len(samples)}'
            raise RuntimeError(msg)
        return mask

    if mode == 'indices':
        indices = [i for i in range(len(filenames))]
        indices = filter(lambda i: filenames[i] in set(samples), indices)
        indices = list(indices)
        if len(indices) != len(samples):
            msg = 'Error during mapping from samples to filenames: '
            msg += f'len(indices) != len(samples) with lengths '
            msg += f'{len(indices)} and {len(samples)}.'
            raise RuntimeError(msg)
        return indices

    msg = f'Got illegal mode "{mode}"! '
    msg += 'Must be in ["list", "mask", "indices"]'
    raise ValueError(msg)
