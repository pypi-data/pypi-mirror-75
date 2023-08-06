""" ResNet for Self-Supervised Learning """

import torch.nn as nn
import torch.nn.functional as F


class BasicBlock(nn.Module):
    """ ResNet Basic Block

    """
    expansion = 1

    def __init__(self, in_planes, planes, stride=1):
        """ Constructor

        Args:
            in_planes: (int) Number of input channels
            planes: (int) Number of channels
            stride: (int) Stride of the first convolutional
        """

        super(BasicBlock, self).__init__()

        self.conv1 = nn.Conv2d(in_planes,
                               planes,
                               kernel_size=3,
                               stride=stride,
                               padding=1,
                               bias=False)
        self.bn1 = nn.BatchNorm2d(planes)

        self.conv2 = nn.Conv2d(planes,
                               planes,
                               kernel_size=3,
                               stride=1,
                               padding=1,
                               bias=False)
        self.bn2 = nn.BatchNorm2d(planes)

        self.shortcut = nn.Sequential()
        if stride != 1 or in_planes != self.expansion*planes:
            self.shortcut = nn.Sequential(
                nn.Conv2d(in_planes,
                          self.expansion*planes,
                          kernel_size=1,
                          stride=stride,
                          bias=False),
                nn.BatchNorm2d(self.expansion*planes)
            )

    def forward(self, x):
        """ Forward pass through basic ResNet block

        Args:
            x: (Tensor) bsz x channels x W x H

        Returns:
            out: (Tensor) bsz x channels x W x H
        """

        out = self.conv1(x)
        out = self.bn1(out)
        out = F.relu(out)

        out = self.conv2(out)
        out = self.bn2(out)

        out += self.shortcut(x)
        out = F.relu(out)

        return out


class Bottleneck(nn.Module):
    """ ResNet Bottleneck block

    """
    expansion = 4

    def __init__(self, in_planes, planes, stride=1):
        """ Constructor

        Args:
            in_planes: (int) Number of input channels
            planes: (int) Number of intermediate channels
            stride: (int) Stride of first convolutional
        """

        super(Bottleneck, self).__init__()

        self.conv1 = nn.Conv2d(in_planes, planes, kernel_size=1, bias=False)
        self.bn1 = nn.BatchNorm2d(planes)

        self.conv2 = nn.Conv2d(planes,
                               planes,
                               kernel_size=3,
                               stride=stride,
                               padding=1,
                               bias=False)
        self.bn2 = nn.BatchNorm2d(planes)

        self.conv3 = nn.Conv2d(planes,
                               self.expansion*planes,
                               kernel_size=1,
                               bias=False)
        self.bn3 = nn.BatchNorm2d(self.expansion*planes)

        self.shortcut = nn.Sequential()
        if stride != 1 or in_planes != self.expansion*planes:
            self.shortcut = nn.Sequential(
                nn.Conv2d(in_planes,
                          self.expansion*planes,
                          kernel_size=1,
                          stride=stride,
                          bias=False),
                nn.BatchNorm2d(self.expansion*planes)
            )

    def forward(self, x):
        """ Forward pass through bottleneck ResNet block

        Args:
            x: (Tensor) bsz x channels x W x H

        Returns:
            out: (Tensor) bsz x (expansion*channels) x W x H
        """

        out = self.conv1(x)
        out = self.bn1(out)
        out = F.relu(out)

        out = self.conv2(out)
        out = self.bn2(out)
        out = F.relu(out)

        out = self.conv3(out)
        out = self.bn3(out)

        out += self.shortcut(x)
        out = F.relu(out)

        return out


class ResNet(nn.Module):
    """ ResNet

    Reference:
        [1] Kaiming He, Xiangyu Zhang, Shaoqing Ren, Jian Sun
        Deep Residual Learning for Image Recognition. arXiv:1512.03385
    """

    def __init__(self,
                 block=BasicBlock,
                 layers=[2, 2, 2, 2],
                 num_classes=10,
                 width=1):
        """ Constructor

        Args:
            block: (nn.Module) ResNet building block type
            layers: (List[int]) Blocks per layer
            num_classes: (int) Number of class for final softmax
            width: (int) Multiplier for ResNet width

        """

        super(ResNet, self).__init__()
        self.in_planes = int(64 * width)

        self.base = int(64 * width)

        self.conv1 = nn.Conv2d(3,
                               self.base,
                               kernel_size=3,
                               stride=1,
                               padding=1,
                               bias=False)
        self.bn1 = nn.BatchNorm2d(self.base)
        self.layer1 = self._make_layer(block, self.base, layers[0], stride=1)
        self.layer2 = self._make_layer(block, self.base*2, layers[1], stride=2)
        self.layer3 = self._make_layer(block, self.base*4, layers[2], stride=2)
        self.layer4 = self._make_layer(block, self.base*8, layers[3], stride=2)
        self.linear = nn.Linear(self.base*8*block.expansion, num_classes)

    def _make_layer(self, block, planes, layers, stride):
        strides = [stride] + [1]*(layers-1)
        layers = []
        for stride in strides:
            layers.append(block(self.in_planes, planes, stride))
            self.in_planes = planes * block.expansion
        return nn.Sequential(*layers)

    def forward(self, x):
        out = F.relu(self.bn1(self.conv1(x)))
        out = self.layer1(out)
        out = self.layer2(out)
        out = self.layer3(out)
        out = self.layer4(out)
        out = F.avg_pool2d(out, 4)
        out = out.view(out.size(0), -1)
        out = self.linear(out)
        return out


def ResNetGenerator(name='resnet-18', width=1, num_classes=10):
    """ Builds and returns the specified ResNet

    Args:
        name: (str) ResNet version from resnet-{9, 18, 34, 50, 101, 152}

    Returns:
        ResNet as nn.Module
    """

    model_params = {
        'resnet-9': {'block': BasicBlock, 'layers': [1, 1, 1, 1]},
        'resnet-18': {'block': BasicBlock, 'layers': [2, 2, 2, 2]},
        'resnet-34': {'block': BasicBlock, 'layers': [3, 4, 6, 3]},
        'resnet-50': {'block': Bottleneck, 'layers': [3, 4, 6, 3]},
        'resnet-101': {'block': Bottleneck, 'layers': [3, 4, 23, 3]},
        'resnet-152': {'block': Bottleneck, 'layers': [3, 8, 36, 3]},
    }

    if name not in model_params.keys():
        raise ValueError('Illegal name: {%s}. \
        Try resnet-9, resnet-18, resnet-34, resnet-50, resnet-101, resnet-152.' % (name))

    return ResNet(**model_params[name], width=width, num_classes=10)


class ResNetSimCLR(nn.Module):
    """ Self-supervised model with ResNet architecture

    """

    def __init__(self, name='resnet-18', width=1, num_ftrs=16, out_dim=128):
        """ Constructor

        Args:
            name: (str) ResNet version from resnet-{9, 18, 34, 50, 101, 152}
            num_ftrs: (int) Embedding dimension
            out_dim: (int) Output dimension

        """

        self.num_ftrs = num_ftrs
        self.out_dim = out_dim

        super(ResNetSimCLR, self).__init__()
        resnet = ResNetGenerator(name=name, width=width)

        last_conv_channels = list(resnet.children())[-1].in_features

        self.features = nn.Sequential(
            nn.BatchNorm2d(3),
            *list(resnet.children())[:-1],
            nn.Conv2d(last_conv_channels, num_ftrs, 1),
            nn.AdaptiveAvgPool2d(1)
        )

        self.projection_head = nn.Sequential(
            nn.Linear(num_ftrs, num_ftrs),
            nn.ReLU(),
            nn.Linear(num_ftrs, out_dim)
        )

    def forward(self, x):
        """ Forward pass through ResNetSimCLR

        Args:
            x: (tensor) bsz x channels x W x H

        Returns:
            embeddings: (tensor) bsz x n_features
        """
        # embed images in feature space
        emb = self.features(x)
        emb = emb.squeeze()

        # return projection to TODO
        return self.projection_head(emb)
