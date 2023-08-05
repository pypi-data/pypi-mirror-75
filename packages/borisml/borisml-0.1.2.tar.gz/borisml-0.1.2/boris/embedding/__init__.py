""" boris.embedding

    The boris.embedding module provides trainable self-supervised
    embedding strategies.

"""

from boris import is_lightning_available

if is_lightning_available():
    from ._base import BaseEmbedding
    from ._embedding import SelfSupervisedEmbedding
