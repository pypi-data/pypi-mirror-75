import torch
import numpy as np

"""
def _evaluate(dataloader, model, metric, device=None):

    with torch.no_grad():
        for batch, target, _ in dataloader:

            batch = batch.to(device)
            target = target.to(device)

            output = model(batch)
            # metric automatically updates all necessary
            # numbers and statistics
            metric(output, target, len(dataloader))

    return metric
"""


def _evaluate(dataloader, model, metrics, device=None):

    with torch.no_grad():
        for batch, target, _ in dataloader:

            batch = batch.to(device)
            target = target.to(device)

            output = model(batch)

            for i, metric in enumerate(metrics):
                metric(output, target, len(dataloader))
                assert np.power(metric.result - metrics[i].result, 2) < 1e-5

    return metrics


class Evaluatable(object):

    def __init__(self, dataloader, eval_metrics):
        self.dataloader = dataloader
        self.eval_metrics = eval_metrics

    def evaluate(self, trainable, device=None):
        """Evaluate trainable with different metrics.

        """
        self.eval_metrics = _evaluate(
            self.dataloader, trainable, self.eval_metrics, device=device
        )
