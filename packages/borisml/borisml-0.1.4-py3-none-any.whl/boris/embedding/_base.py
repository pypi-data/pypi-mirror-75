""" BaseEmbeddings """

import copy

import pytorch_lightning as pl
import pytorch_lightning.core.lightning as lightning
import torch.nn as nn


class BaseEmbedding(lightning.LightningModule):
    """ All trainable embeddings must inherit from BaseEmbedding.

    """

    def __init__(self, model, criterion, optimizer, dataloader):
        """ Constructor

        Args:
            model: (torch.nn.Module)
            criterion: (torch.nn.Module)
            optimizer: (torch.optim.Optimizer)
            dataloader: (torch.utils.data.DataLoader)

        """

        super(BaseEmbedding, self).__init__()
        self.model = model
        self.criterion = criterion
        self.optimizer = optimizer
        self.dataloader = dataloader
        self.checkpoint = None

    def forward(self, x):
        return self.model(x)

    def training_step(self, batch, batch_idx):
        x, y, _ = batch
        y_hat = self(x)
        loss = self.criterion(y_hat, y)
        tensorboard_logs = {'train_loss': loss}
        return {'loss': loss, 'log': tensorboard_logs}

    def configure_optimizers(self):
        return self.optimizer

    def train_dataloader(self):
        return self.dataloader

    def train_embedding(self, **kwargs):
        """ Train the model on the provided dataset.

        Args:
            **kwargs: pylightning_trainer arguments, examples include:
                min_epochs: (int) Minimum number of epochs to train
                max_epochs: (int) Maximum number of epochs to train
                gpus: (int) number of gpus to use

        Returns:
            A trained encoder, ready for embedding datasets.

        """
        trainer = pl.Trainer(**kwargs)
        trainer.fit(self)

        checkpoint_cb = trainer.checkpoint_callback
        try:
            self.checkpoint = checkpoint_cb.kth_best_model
        except:
            print('Warning: "kth_best_model" was deprecated. \
                    Using "kth_best_model_path" instead.')
            self.checkpoint = checkpoint_cb.kth_best_model_path

        return self

    def recycle(self, new_output_dim, layer=None):
        """Build a copy of the embedding model with a new output layer

        Args:
            new_output_dim: (int)
            layer: (int)

        Returns:
            Copy of the embedding model with new output layer
        """

        layer = -1 if layer is None else layer

        modules = []
        for module in self.model.features:
            module_copy = copy.deepcopy(module)
            modules.append(module_copy)

        output_dim = None
        if isinstance(modules[-1], nn.AdaptiveAvgPool2d):
            output_dim = modules[-2].out_channels
        elif isinstance(modules[-1], nn.Linear):
            output_dim = modules[-1].out_features
        else:
            msg = 'Could not determine output_size. Last layer is {}'
            msg = msg.format(type(modules[-1]))
            raise NotImplementedError(msg)

        modules.append(nn.Flatten())
        modules.append(nn.Linear(output_dim, new_output_dim))
        return nn.Sequential(*modules)

    def embed(self, *args, **kwargs):
        """Must be implemented by classes which inherit from BaseEmbedding.

        """
        raise NotImplementedError()
