from boris.cli.train_cli import _train_cli
from boris.cli.embed_cli import _embed_cli
from boris.cli.boris_cli import _boris_cli
import boris.cli as cli

import yaml
import os


def _get_config_path(config_path):
    """Find path to yaml config file

    Args:
        config_path: (str) Path to config.yaml file

    Returns:
        Path to config.yaml if specified else default config.yaml

    Raises:
        ValueError if the config_path is not None but doesn't exist

    """
    if config_path is None:
        dirname = os.path.dirname(cli.__file__)
        config_path = os.path.join(dirname, 'config/config.yaml')
    if not os.path.exists(config_path):
        raise ValueError("Config path {} does not exist!".format(config_path))

    return config_path


def _load_config_file(config_path):
    """Load a yaml config file

    Args:
        config_path: (str) Path to config.yaml file

    Returns:
        Dictionary with configs from config.yaml

    """
    Loader = yaml.FullLoader
    with open(config_path, 'r') as config_file:
        cfg = yaml.load(config_file, Loader=Loader)

    return cfg


def _add_kwargs(cfg, kwargs):
    """Add keyword arguments to config

    Args:
        cfg: (dict) Dictionary of configs from config.yaml
        kwargs: (dict) Dictionary of keyword arguments

    Returns:
        Union of cfg and kwargs

    """
    for key, item in kwargs.items():
        if isinstance(item, dict):
            if key in cfg:
                cfg[key] = _add_kwargs(cfg[key], item)
            else:
                cfg[key] = item
        else:
            cfg[key] = item

    return cfg


def train_model_and_get_image_features(config_path: str = None, **kwargs):
    """Train a self-supervised model and use it to embed images

    Args:
        config_path: Path to config.yaml
        **kwargs: Keyword arguments to overwrite configs

    Returns:
        (embeddings, labels, filenames)

    """
    config_path = _get_config_path(config_path)
    config_args = _load_config_file(config_path)
    config_args = _add_kwargs(config_args, kwargs)

    return _boris_cli(config_args, is_cli_call=False)


def train_self_supervised_model(config_path: str = None, **kwargs):
    """Train a self-supervised model

    Args:
        config_path: Path to config.yaml
        **kwargs: Keyword arguments to overwrite configs

    Returns:
        Path to embedding-checkpoint

    """
    config_path = _get_config_path(config_path)
    config_args = _load_config_file(config_path)
    config_args = _add_kwargs(config_args, kwargs)

    return _train_cli(config_args, is_cli_call=False)


def get_image_features(checkpoint: str, config_path: str = None, **kwargs):
    """Embed images with a self-supervised model.

    Args:
        config_path: Path to config.yaml
        **kwargs: Keyword arguments to overwrite configs

    Returns:
        (embeddings, labels, filenames):

    """
    config_path = _get_config_path(config_path)
    config_args = _load_config_file(config_path)
    config_args = _add_kwargs(config_args, kwargs)

    config_args['checkpoint'] = checkpoint

    return _embed_cli(config_args, is_cli_call=False)
