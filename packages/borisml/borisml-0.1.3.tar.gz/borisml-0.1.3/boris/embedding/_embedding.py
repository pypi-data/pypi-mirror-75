""" Embeddings """

import time

import torch
from boris import is_prefetch_generator_available
from boris.embedding._base import BaseEmbedding
from tqdm import tqdm

if is_prefetch_generator_available():
    from prefetch_generator import BackgroundGenerator


class SelfSupervisedEmbedding(BaseEmbedding):
    """ Self-supervised embedding based on contrastive multiview coding.
        (https://arxiv.org/abs/1906.05849)

    """

    def __init__(self, model, criterion, optimizer, dataloader):
        """ Constructor

        Args:
            model: (torch.nn.Module)
            criterion: (torch.nn.Module)
            optimizer: (torch.optim.Optimizer)
            dataloader: (torch.utils.data.DataLoader)

        """

        super(SelfSupervisedEmbedding, self).__init__(
            model, criterion, optimizer, dataloader
        )

    def embed(self, dataloader, caching=False, normalize=False, device=None):
        """ Embed data in vector space

        Args:
            dataloader: (torch.utils.data.DataLoader)
            caching: (bool) TODO
            normalize: (bool) Normalize embeddings to unit length

        """

        # TODO: Caching
        if caching:
            pass
            return None, None

        self.model.eval()
        embeddings, labels, fnames = None, None, []

        if is_prefetch_generator_available():
            pbar = tqdm(BackgroundGenerator(dataloader, max_prefetch=3),
                        total=len(dataloader))
        else:
            pbar = tqdm(dataloader, total=len(dataloader))

        start_time = time.time()
        with torch.no_grad():

            for (img, label, fname) in pbar:

                img = img.to(device)
                label = label.to(device)

                fnames += [*fname]

                batch_size = img.shape[0]
                prepare_time = time.time()

                emb = self.model.features(img)
                emb = emb.detach().reshape(batch_size, -1)

                if embeddings is None:
                    embeddings = emb
                else:
                    embeddings = torch.cat((embeddings, emb), 0)

                if labels is None:
                    labels = label
                else:
                    labels = torch.cat((labels, label), 0)

                process_time = time.time()

                pbar.set_description("Compute efficiency: {:.2f}".format(
                    process_time / (process_time + prepare_time)))

            embeddings = embeddings.cpu().numpy()
            labels = labels.cpu().numpy()

        return embeddings, labels, fnames


class VAEEmbedding(BaseEmbedding):
    """ Unsupervised embedding based on variational auto-encoders.

    """

    def embed(self, dataloader):
        """ TODO

        """
        raise NotImplementedError("This site is under construction...")
