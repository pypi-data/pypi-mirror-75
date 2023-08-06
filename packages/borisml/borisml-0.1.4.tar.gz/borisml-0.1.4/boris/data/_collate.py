""" Collate Functions """

import torch
import torch.nn as nn

import torchvision.transforms as transforms
from boris.transforms import GaussianBlur


class BaseCollateFunction(nn.Module):
    """ Base class for collate callables.

    """

    def __init__(self, transform):
        """ Constructor

        Args:
            transform: (torchvision.transforms.Compose)

        """
        super(BaseCollateFunction, self).__init__()
        self.transform = transform

    def forward(self, batch):
        """ Upon call

            Args:
                batch: List[(img, target, fname)]

            Returns:
                image_batch: Transformed images in batch form
                target_batch: Targets in batch form
                fnames: List of filenames for samples in batch
        """
        batch_a = torch.cat(
            [self.transform(item[0]).unsqueeze_(0) for item in batch], 0
        )
        batch_b = torch.cat(
            [self.transform(item[0]).unsqueeze_(0) for item in batch], 0
        )
        labels = torch.tensor([item[1] for item in batch]).long()
        fnames = [item[2] for item in batch]
        return (torch.cat((batch_a, batch_b), 0),
                torch.cat((labels, labels), 0),
                fnames)


class ImageCollateFunction(BaseCollateFunction):
    """ Image collate function for self-supervised learning

    """

    def __init__(self, input_size=32, cj_prob=0.8, cj_bright=0.7,
                 cj_contrast=0.7, cj_sat=0.7, cj_hue=0.2, min_scale=0.08,
                 random_gray_scale=0.2, kernel_size=0.1):
        """ Constructor

        Args:
            input_size: (int) Dimensions of the input image
            cj_prob: (float) Probability that color jitter is applied
            cj_bright: (float) How much to jigger brightness
            cj_contrast: (float) How much to jigger constrast
            cj_sat: (float) How much to jigger saturation
            cj_hue: (float) How much to jigger hue
            min_scale: (float) Minimum size of the randomized crop
            random_gray_scale: (float) Probability of grayscale
            kernel_size: (float) Sigma of gaussian blur is \
                kernel_size * input_size

        """
        color_jitter = transforms.ColorJitter(
            cj_bright, cj_contrast, cj_sat, cj_hue
        )
        transform = transforms.Compose(
            [transforms.RandomResizedCrop(size=input_size,
                                          scale=(min_scale, 1.0)),
             transforms.RandomHorizontalFlip(),
             transforms.RandomApply([color_jitter], p=cj_prob),
             transforms.RandomGrayscale(p=random_gray_scale),
             GaussianBlur(kernel_size=int(kernel_size * input_size)),
             transforms.ToTensor(),
             transforms.Normalize(
                mean=[0.485, 0.456, 0.406],
                std=[0.229, 0.224, 0.225]),
             ]
        )
        super(ImageCollateFunction, self).__init__(transform)
