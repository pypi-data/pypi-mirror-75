# -*- coding: utf-8 -*-
"""
    boris.cli
    ~~~~~~~~~

    A simple command line tool to upload your datasets to
    the WhatToLabel platform.

"""

import hydra

from boris.api import upload_embeddings_from_csv
from boris.api import upload_images_from_folder

from boris.cli._helpers import fix_input_path


def _upload_cli(cfg, is_cli_call=True):
    '''Upload your image dataset and/or embeddings to the WhatToLabel platform.

    Args:
        cfg['path_to_folder']: (str)
            Path to folder which holds images to upload
        cfg['path_to_embeddings']: (str)
            Path to csv file which holds embeddings to upload
        cfg['dataset_id']: (str) Dataset identifier on the platform
        cfg['token']: (str) Token which grants acces to the platform

    '''

    path_to_folder = cfg['path_to_folder']
    if path_to_folder and is_cli_call:
        path_to_folder = fix_input_path(cfg['path_to_folder'])

    path_to_embeddings = cfg['path_to_embeddings']
    if path_to_embeddings and is_cli_call:
        path_to_embeddings = fix_input_path(cfg['path_to_embeddings'])

    dataset_id = cfg['dataset_id']
    token = cfg['token']

    if not token:
        raise ValueError('token was not specified!')
    if not dataset_id:
        raise ValueError('dataset_id was not specified!')

    if path_to_folder:
        upload_images_from_folder(path_to_folder, dataset_id, token)

    if path_to_embeddings:
        upload_embeddings_from_csv(path_to_embeddings, dataset_id, token)


@hydra.main(config_path='config/config.yaml')
def upload_cli(cfg):
    '''Upload your image dataset and/or embeddings to the WhatToLabel platform.

    Args:
        cfg['path_to_folder']: (str)
            Path to folder which holds images to upload
        cfg['path_to_embeddings']: (str)
            Path to csv file which holds embeddings to upload
        cfg['dataset_id']: (str) Dataset identifier on the platform
        cfg['token']: (str) Token which grants acces to the platform

    '''
    _upload_cli(cfg)


def entry():
    upload_cli()
