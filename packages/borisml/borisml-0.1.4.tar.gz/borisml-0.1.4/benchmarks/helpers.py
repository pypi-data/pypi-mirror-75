import numpy as np
import torch

import yaml


def init_seed(seed):
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed(seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False


def load_config_file(config_path):
    Loader = yaml.FullLoader
    with open(config_path, 'r') as config_file:
        cfg = yaml.load(config_file, Loader=Loader)
    return cfg


def count_samples_per_class(dataloader, num_classes):
    labels = []
    for batch, target, _ in dataloader:
        labels.extend(target.cpu().numpy())
    return [labels.count(i) for i in range(num_classes)]


def calculate_class_weights(dataloader, num_classes):
    n_samples_per_class = count_samples_per_class(dataloader, num_classes)
    max_samples_per_class = max(n_samples_per_class)
    weight = [max_samples_per_class / x for x in n_samples_per_class]
    return torch.FloatTensor(weight)


def confusion_matrix(output, target, n_classes):

    _, argmax = output.max(-1)
    cm = torch.zeros((n_classes, n_classes))
    for yhat, y in zip(argmax, target):
        cm[y, yhat] += 1

    return cm
