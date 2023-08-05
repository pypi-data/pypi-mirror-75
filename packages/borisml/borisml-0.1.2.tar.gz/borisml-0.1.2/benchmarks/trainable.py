import pytorch_lightning.core.lightning as lightning


class Trainable(lightning.LightningModule):

    def __init__(self,
                 model,
                 criterion,
                 optimizer,
                 dataloader,
                 scheduler=None):

        super(Trainable, self).__init__()
        self.model = model
        self.criterion = criterion
        self.optimizer = optimizer
        self.dataloader = dataloader
        self.scheduler = scheduler

    def forward(self, x):
        return self.model(x)

    def training_step(self, batch, batch_idx):
        x, y, _ = batch
        y_hat = self(x)
        loss_ = self.criterion(y_hat, y)
        tensorboard_logs = {'train_loss': loss_}
        return {'loss': loss_, 'log': tensorboard_logs}

    def configure_optimizers(self):
        if self.scheduler is None:
            return self.optimizer
        else:
            return [self.optimizer], [self.scheduler]

    def train_dataloader(self):
        return self.dataloader
