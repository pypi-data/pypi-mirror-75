import numpy as np
import torch

import unittest

from boris.transforms import GaussianBlur


class TestGaussianBlur(unittest.TestCase):

    def test_on_np_array(self):
        m, M = 0.1, 2.0
        for w in range(1, 100):
            for h in range(1, 100):
                gb = GaussianBlur(int(0.1 * w), min=m, max=M)
                sample = np.random.randn(w, h)
                gb(sample)

    def test_on_torch_tensor(self):
        m, M = 0.1, 2.0
        for w in range(1, 100):
            for h in range(1, 100):
                gb = GaussianBlur(int(0.1 * w), min=m, max=M)
                sample = torch.randn(w, h)
                gb(sample)
