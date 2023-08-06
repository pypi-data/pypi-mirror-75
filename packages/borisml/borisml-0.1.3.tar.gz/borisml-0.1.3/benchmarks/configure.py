import torch
import torch.nn as nn

import pytorch_lightning as pl
import torchvision

import boris

from trainable import Trainable
from evaluatable import Evaluatable

from helpers import calculate_class_weights

import metrics


def configure_criterion(cfg, dataloader):

    if cfg['criterion']['name'] == 'cross-entropy':
        weight = calculate_class_weights(dataloader, cfg['num_classes'])
        return nn.CrossEntropyLoss(weight=weight)
    else:
        raise NotImplementedError()


def configure_dataloader(cfg, dataset, state=None, train=True):

    if train and state is not None:
        _, selected, _, _ = state
        sampler = torch.utils.data.SubsetRandomSampler(
            selected.nonzero()
        )
    else:
        sampler = None

    if train:
        dataloader = torch.utils.data.DataLoader(
            dataset,
            shuffle=True if sampler is None else False,
            batch_size=cfg['training']['batch_size'],
            sampler=sampler
        )
    else:
        dataloader = torch.utils.data.DataLoader(
            dataset,
            batch_size=cfg['evaluation']['batch_size'],
            num_workers=8
        )

    return dataloader


def configure_dataset(cfg, transform, train=True):

    if train:
        dataset_cfg = cfg['training']['data']
    else:
        dataset_cfg = cfg['evaluation']['data']

    dataset = boris.data.BorisDataset(**dataset_cfg, transform=transform)
    return dataset


def configure_embedding(cfg, data_cfg, transform_cfg):

    if 'resnet' in cfg['model']['name']:
        model = boris.models.ResNetSimCLR(**cfg['model'])
    else:
        raise NotImplementedError()

    criterion = boris.loss.NTXentLoss(**cfg['criterion'])
    optimizer = torch.optim.SGD(model.parameters(), **cfg['optimizer'])

    dataset = boris.data.BorisDataset(**data_cfg)

    collate_fn = boris.data.ImageCollateFunction(**cfg['collate'])
    dataloader = torch.utils.data.DataLoader(dataset,
                                             **cfg['loader'],
                                             collate_fn=collate_fn)

    embed_transform = torchvision.transforms.Compose([
        torchvision.transforms.Resize((transform_cfg['input_size'])),
        torchvision.transforms.ToTensor(),
        torchvision.transforms.Normalize(
            mean=[0.485, 0.456, 0.406],
            std=[0.229, 0.224, 0.225])
        ])
    embed_dataset = boris.data.BorisDataset(**data_cfg,
                                            transform=embed_transform)

    embedding_model = boris.embedding.SelfSupervisedEmbedding(
        model, criterion, optimizer, dataloader
    )
    return embedding_model, torch.utils.data.DataLoader(embed_dataset,
                                                        batch_size=100)


def configure_model(cfg):

    if 'resnet' in cfg['model']['name']:
        model = boris.models.ResNetGenerator(
            width=cfg['model']['width'],
            num_classes=cfg['num_classes']
        )
    else:
        raise NotImplementedError()

    return model


def configure_optimizer(cfg, model):

    if cfg['optimizer']['name'] == 'sgd':
        optimizer = torch.optim.SGD(
            model.parameters(),
            lr=cfg['optimizer']['lr'],
            weight_decay=cfg['optimizer']['weight_decay']
        )
    elif cfg['optimizer']['name'] == 'adam':
        optimizer = torch.optim.Adam(
            model.parameters(),
            lr=cfg['optimizer']['lr'],
            weight_decay=cfg['optimizer']['weight_decay']
        )
    else:
        raise NotImplementedError()

    return optimizer


def configure_scheduler(cfg, optimizer):
    if 'lr_decay' in cfg['optimizer']:
        lr_decay_step = cfg['optimizer']['lr_decay']
        scheduler = torch.optim.lr_scheduler.MultiStepLR(
            optimizer, milestones=lr_decay_step
        )
    else:
        scheduler = None
    return scheduler


def configure_transform(cfg, train=True):

    if train:
        transform_cfg = cfg['training']['transform']
    else:
        transform_cfg = cfg['evaluation']['transform']

    transforms = []

    if transform_cfg['input_size'] > 0:
        transforms.append(
            torchvision.transforms.Resize((transform_cfg['input_size']))
        )

    if 'flip' in transform_cfg.keys() and transform_cfg['flip']:
        transforms.append(
            torchvision.transforms.RandomHorizontalFlip()
        )

    transforms.append(torchvision.transforms.ToTensor())

    if 'normalize' in transform_cfg.keys() and transform_cfg['normalize']:
        transforms.append(
            torchvision.transforms.Normalize(
                mean=[0.485, 0.456, 0.406],
                std=[0.229, 0.224, 0.225]
            )
        )

    return torchvision.transforms.Compose(transforms)


def configure_trainable(cfg, state, device=None):

    model = configure_model(cfg)
    optimizer = configure_optimizer(cfg, model)
    scheduler = configure_scheduler(cfg, optimizer)

    transform = configure_transform(cfg, train=True)
    dataset = configure_dataset(cfg, transform, train=True)
    dataloader = configure_dataloader(cfg, dataset, state=state, train=True)
    criterion = configure_criterion(cfg, dataloader)

    trainable = Trainable(model, criterion, optimizer, dataloader, scheduler)
    trainer = pl.Trainer(**cfg['training']['trainer'])

    return trainable, trainer


def configure_evaluatable(cfg):

    num_classes = cfg['num_classes']

    transform = configure_transform(cfg, train=False)
    dataset = configure_dataset(cfg, transform, train=False)
    dataloader = configure_dataloader(cfg, dataset, train=False)
    eval_metrics = []
    for metric in cfg['evaluation']['metrics']:

        # classification
        if metric == 'classification-per-class-accuracy':
            eval_metric = [
                metrics.ClassificationPerClassAccuracy(i, num_classes)
                for i in range(num_classes)
            ]
        elif metric == 'classification-top-1-accuracy':
            eval_metric = [metrics.ClassificationTop1Accuracy()]
        elif metric == 'classification-top-5-accuracy':
            eval_metric = [metrics.ClassificationTop5Accuracy()]
        elif metric == 'classification-mean-precision':
            eval_metric = [metrics.ClassificationMeanPrecision(num_classes)]
        elif metric == 'classification-mean-recall':
            eval_metric = [metrics.ClassificationMeanRecall(num_classes)]
        # other
        elif metric == 'segmentation-TODO':
            raise NotImplementedError()
        # none of the above
        else:
            raise ValueError('Illegal metric: {}'.format(eval_metric))

        eval_metrics = eval_metrics + eval_metric

    evaluatable = Evaluatable(dataloader, eval_metrics)
    return evaluatable
