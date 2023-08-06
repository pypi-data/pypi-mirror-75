import unittest

import numpy as np
import torch

from boris.sampling import sample


class TestSampler(unittest.TestCase):

    def create_state(self, n, d, device='cpu'):
        embeddings = torch.from_numpy(np.random.rand(n, d)).float().to(device)
        n_data = len(embeddings)
        selected = torch.from_numpy(np.zeros(n_data)).bool().to(device)
        state = (n_data, selected, embeddings, None)
        return state

    def test_all_samplers_cpu(self):
        STRATEGIES = ('bit', 'random', 'coreset')
        N_SAMPLES = (1e1, 1e2, 1e3)
        DIMENSION = (2, 16, 32)
        N_OUTPUT = int(1e1)

        for strategy in STRATEGIES:
            for n in N_SAMPLES:
                for d in DIMENSION:
                    n = int(n)
                    state = self.create_state(n, d, 'cpu')
                    new_state, sscores = sample(N_OUTPUT, state, strategy)

                    n_data, selected, embeddings, scores = new_state

                    self.assertIsInstance(n_data, int)
                    self.assertIsInstance(selected, torch.BoolTensor)
                    self.assertIsInstance(embeddings, torch.FloatTensor)
                    self.assertEqual(n_data, len(embeddings))
                    self.assertEqual(n_data, n)
                    self.assertTrue(torch.max(sscores).item() <= 1.0)
                    self.assertTrue(torch.min(sscores).item() >= 0.0)

    def test_bit_sampler_too_large_embedding(self):
        embeddings = torch.from_numpy(np.random.rand(10, 65)).float()
        n_data = len(embeddings)
        selected = torch.from_numpy(np.zeros(n_data)).bool()
        state = (n_data, selected, embeddings, None)

        with self.assertRaises(ValueError):
            new_state, sscores = sample(5, state, 'bit')
