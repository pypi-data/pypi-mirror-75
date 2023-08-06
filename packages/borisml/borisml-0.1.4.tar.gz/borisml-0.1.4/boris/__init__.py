""" Deep Learning Package for Python

boris is a Python module for self-supervised active learning.

"""

try:
    import pytorch_lightning
except ImportError:
    _lightning_available = False
else:
    _lightning_available = True

try:
    import cv2
except ImportError:
    _opencv_available = False
else:
    _opencv_available = True

try:
    import prefetch_generator
except ImportError:
    _prefetch_generator_available = False
else:
    _prefetch_generator_available = True


def is_lightning_available():
    return _lightning_available


def is_opencv_available():
    return _opencv_available


def is_prefetch_generator_available():
    return _prefetch_generator_available


if is_lightning_available():
    from ._one_liners import train_model_and_get_image_features
    from ._one_liners import train_self_supervised_model
    from ._one_liners import get_image_features

__version__ = '0.1.4'
