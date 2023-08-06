""" boris.cli

    The boris.cli module provides a console interface
    for training self-supervised models, embedding,
    and filtering datasets

"""

from boris import is_lightning_available

if is_lightning_available():
    from .train_cli import train_cli
    from .embed_cli import embed_cli
    from .boris_cli import boris_cli

from .upload_cli import upload_cli
