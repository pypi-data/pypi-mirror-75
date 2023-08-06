# -*- coding: utf-8 -*-
"""
    boris-cli
    ~~~~~~~~~

    A simple command line tool to train a state-of-the-art
    self-supervised model on your image dataset.

"""

import hydra
import warnings

from boris.data import ImageCollateFunction
from boris.data import BorisDataset
from boris.embedding import SelfSupervisedEmbedding
from boris.loss import NTXentLoss
from boris.models import ResNetSimCLR

from boris.cli._helpers import _is_url
from boris.cli._helpers import _model_zoo
from boris.cli._helpers import fix_input_path
from boris.cli._helpers import filter_state_dict

import torch


def _train_cli(cfg, is_cli_call=True):
    """Train a self-supervised model on the image dataset of your choice.

    Args:
        cfg[data]: (str)
            Name of the dataset (to download use cifar10 or cifar100)
        cfg[root]: (str) Directory where the dataset should be stored
        cfg[download]: (bool) Whether to download the dataset
        cfg[from_folder]: (str)
            If specified, the dataset is loaded from the folder

    Returns:
        checkpoint: (str) Path to checkpoint of the best model during training

    """

    data = cfg['data']
    download = cfg['download']

    root = cfg['root']
    if root and is_cli_call:
        root = fix_input_path(root)

    from_folder = cfg['from_folder']
    if from_folder and is_cli_call:
        from_folder = fix_input_path(from_folder)

    if 'seed' in cfg.keys():
        seed = cfg['seed']
        torch.manual_seed(seed)
        torch.cuda.manual_seed(seed)
        torch.backends.cudnn.deterministic = True
        torch.backends.cudnn.benchmark = False

    if torch.cuda.is_available():
        device = 'cuda'
    elif cfg['trainer'] and cfg['trainer']['gpus']:
        device = 'cpu'
        cfg['trainer']['gpus'] = 0

    if cfg['loader']['batch_size'] < 64:
        msg = 'Training a self-supervised model with a small batch size: {}! '
        msg = msg.format(cfg['loader']['batch_size'])
        msg += 'Small batch size may harm embedding quality. '
        msg += 'You can specify the batch size via the loader key-word: '
        msg += 'loader.batch_size=BSZ'
        warnings.warn(msg)

    model = ResNetSimCLR(**cfg['model'])
    checkpoint = cfg['checkpoint']
    if cfg['pre_trained'] and not checkpoint:
        # if checkpoint wasn't specified explicitly and pre_trained is True
        # try to load the checkpoint from the model zoo
        checkpoint, key = _model_zoo(cfg['model'])
        if not checkpoint:
            msg = 'Cannot download checkpoint for key {} '.format(key)
            msg += 'because it does not exist! '
            msg += 'Model will be trained from scratch.'
            warnings.warn(msg)
    elif checkpoint:
        checkpoint = fix_input_path(checkpoint) if is_cli_call else checkpoint
    
    if checkpoint:
        # load the PyTorch state dictionary and map it to the current device
        # then, remove the model. prefix which is caused by the pytorch-lightning
        # checkpoint saver and load the model from the "filtered" state dict
        # this approach is compatible with pytorch_lightning 0.7.1 - 0.8.4 (latest)
        if _is_url(checkpoint):
            state_dict = torch.hub.load_state_dict_from_url(
                checkpoint, map_location=device
            )['state_dict']
        else:
            state_dict = torch.load(
                checkpoint, map_location=device
            )['state_dict']
        state_dict = filter_state_dict(state_dict)
        model.load_state_dict(state_dict)
        
    criterion = NTXentLoss(**cfg['criterion'])
    optimizer = torch.optim.SGD(model.parameters(), **cfg['optimizer'])

    dataset = BorisDataset(root,
                           name=data, train=True, download=download,
                           from_folder=from_folder)

    collate_fn = ImageCollateFunction(**cfg['collate'])
    dataloader = torch.utils.data.DataLoader(dataset,
                                             **cfg['loader'],
                                             collate_fn=collate_fn)

    encoder = SelfSupervisedEmbedding(model, criterion, optimizer, dataloader)
    encoder = encoder.train_embedding(**cfg['trainer'])

    print('Best model is stored at: %s' % (encoder.checkpoint))
    return encoder.checkpoint


@hydra.main(config_path="config/config.yaml", strict=False)
def train_cli(cfg):
    """Train a self-supervised model on the image dataset of your choice.

    Args:
        cfg[data]: (str)
            Name of the dataset (to download use cifar10 or cifar100)
        cfg[root]: (str) Directory where the dataset should be stored
        cfg[download]: (bool) Whether to download the dataset
        cfg[from_folder]: (str)
            If specified, the dataset is loaded from the folder

    Returns:
        checkpoint: (str) Path to checkpoint of the best model during training

    """

    return _train_cli(cfg)


def entry():
    train_cli()
