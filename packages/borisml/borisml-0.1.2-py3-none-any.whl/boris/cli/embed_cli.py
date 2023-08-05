# -*- coding: utf-8 -*-
"""
    boris.cli
    ~~~~~~~~~

    A simple command line tool to embed your image dataset using
    a pretrained state-of-the-art, self-supervised model.

"""

import os

import hydra
import torch
import torchvision

from boris.data import BorisDataset
from boris.embedding import SelfSupervisedEmbedding
from boris.models import ResNetSimCLR
from boris.utils import embeddings_to_pandas

from boris.cli._helpers import _is_url
from boris.cli._helpers import _model_zoo
from boris.cli._helpers import fix_input_path
from boris.cli._helpers import filter_state_dict


def _embed_cli(cfg, is_cli_call=True):
    """Use the trained self-supervised model to embed samples from your dataset.

    Args:
        cfg[data]: (str) Name of the dataset
        cfg[root]: (str) Directory where the dataset should be stored
        cfg[checkpoint]: (str) Path to the lightning checkpoint
        cfg[download]: (bool) Whether to download the dataset
        cfg[from_folder]: (str) If specified, the dataset is loaded \
            from the folder

    Returns:
        embeddings: (np.ndarray) A d-dimensional embedding \
            for each data sample
        labels: (np.ndarray) Data labels, 0 if there are no labels
        filenames: (List[str]) File name of each data sample
    """

    data = cfg['data']
    checkpoint = cfg['checkpoint']
    download = cfg['download']

    root = cfg['root']
    if root and is_cli_call:
        root = fix_input_path(root)

    from_folder = cfg['from_folder']
    if from_folder and is_cli_call:
        from_folder = fix_input_path(from_folder)

    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False

    if torch.cuda.is_available():
        device = torch.device('cuda')
    else:
        device = torch.device('cpu')

    model = ResNetSimCLR(**cfg['model']).to(device)

    transform = torchvision.transforms.Compose([
        torchvision.transforms.Resize((cfg['collate']['input_size'],
                                       cfg['collate']['input_size'])),
        torchvision.transforms.ToTensor(),
        torchvision.transforms.Normalize(
            mean=[0.485, 0.456, 0.406],
            std=[0.229, 0.224, 0.225])
    ])

    dataset = BorisDataset(root,
                           name=data, train=True, download=download,
                           from_folder=from_folder, transform=transform)

    cfg['loader']['drop_last'] = False
    cfg['loader']['shuffle'] = False
    dataloader = torch.utils.data.DataLoader(dataset, **cfg['loader'])

    # load the PyTorch state dictionary and map it to the current device
    # then, remove the model. prefix which is caused by the pytorch-lightning
    # checkpoint saver and load the model from the "filtered" state dict
    # this approach is compatible with pytorch_lightning 0.7.1 - 0.8.4 (latest)
    if not checkpoint:
        checkpoint, key = _model_zoo(cfg['model'])
        if not checkpoint:
            msg = 'Cannot download checkpoint for key {} '.format(key)
            msg += 'because it does not exist!'
            raise RuntimeError(msg)
        state_dict = torch.hub.load_state_dict_from_url(
            checkpoint, map_location=device
        )['state_dict']
    else:
        checkpoint = fix_input_path(checkpoint) if is_cli_call else checkpoint
        state_dict = torch.load(
            checkpoint, map_location=device
        )['state_dict']
    state_dict = filter_state_dict(state_dict)
    model.load_state_dict(state_dict)
    encoder = SelfSupervisedEmbedding(model, None, None, None)

    embeddings, labels, filenames = encoder.embed(dataloader, device=device)

    df = embeddings_to_pandas(embeddings, labels, filenames)
    path = os.path.join(os.getcwd(), 'embeddings.csv')
    df.to_csv(path, index=False)
    print('Embeddings are stored at %s' % (path))

    return embeddings, labels, filenames


@hydra.main(config_path='config/config.yaml', strict=False)
def embed_cli(cfg):
    """Use the trained self-supervised model to embed samples from your dataset.

    Args:
        cfg[data]: (str) Name of the dataset
        cfg[root]: (str) Directory where the dataset should be stored
        cfg[checkpoint]: (str) Path to the lightning checkpoint
        cfg[download]: (bool) Whether to download the dataset
        cfg[from_folder]: (str) If specified, the dataset is loaded \
            from the folder

    Returns:
        embeddings: (np.ndarray) A d-dimensional embedding \
            for each data sample
        labels: (np.ndarray) Data labels, 0 if there are no labels
        filenames: (List[str]) File name of each data sample
    """

    return _embed_cli(cfg)


def entry():
    embed_cli()
