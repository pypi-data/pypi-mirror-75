# -*- coding: utf-8 -*-
"""
    boris.cli
    ~~~~~~~~~

    A simple command line tool to embed your image dataset with
    state-of-the-art technology.

"""

import hydra

from boris.cli.train_cli import _train_cli
from boris.cli.embed_cli import _embed_cli


def _boris_cli(cfg, is_cli_call=True):
    """Train a self-supervised model and use it to embed your dataset

    Args:
        see train_cli.py, embed_cli.py or
        https://www.notion.so/whattolabel/WhatToLabel-Documentation-28e645f5564a453e807d0a384a4e6ea7

    """

    cfg['loader']['shuffle'] = True
    cfg['loader']['drop_last'] = True
    checkpoint = _train_cli(cfg, is_cli_call)

    cfg['loader']['shuffle'] = False
    cfg['loader']['drop_last'] = False
    cfg['checkpoint'] = checkpoint

    return _embed_cli(cfg, is_cli_call)


@hydra.main(config_path="config/config.yaml", strict=False)
def boris_cli(cfg):
    """Train a self-supervised model and use it to embed your dataset

    Args:
        see train_cli.py, embed_cli.py or
        https://www.notion.so/whattolabel/WhatToLabel-Documentation-28e645f5564a453e807d0a384a4e6ea7

    """
    return _boris_cli(cfg)


def entry():
    boris_cli()
