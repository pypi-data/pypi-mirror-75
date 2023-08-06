import torch

from helpers import confusion_matrix


class BaseMetric(object):

    def __init__(self, identifier):
        self._identifier = identifier
        self._result = None

    @property
    def identifier(self):
        return self._identifier

    @property
    def result(self):
        return self._result.detach().cpu().item()

    @result.setter
    def result(self, value):
        if self._result is None:
            self._result = value
        else:
            self._result += value


class ClassificationTop1Accuracy(BaseMetric):

    def __init__(self):
        super(ClassificationTop1Accuracy, self).__init__(
            'classification-top-1-accuracy'
        )

    def __call__(self, output, target, N):
        _, argmax = output.max(-1)
        self.result = (argmax == target).float().mean() / N


class ClassificationTop5Accuracy(BaseMetric):

    def __init__(self):
        super(ClassificationTop5Accuracy, self).__init__(
             'classification-top-5-accuracy'
        )

    def __call__(self, output, target, N):
        _, argsort = torch.sort(output, -1, descending=True)
        accuracy = torch.zeros(len(output)).to(output.device)
        for i in range(5):
            accuracy += (argsort[:, i] == target)
        self.result = accuracy.mean() / N


class ClassificationMeanPrecision(BaseMetric):

    def __init__(self, n_classes):
        super(ClassificationMeanPrecision, self).__init__(
            'classification-mean-precision'
        )
        self.n_classes = n_classes

    def __call__(self, output, target, N):
        C = confusion_matrix(output, target, self.n_classes)
        precision = torch.diag(C) / torch.sum(C, 0)
        precision[precision != precision] = 0.
        self.result = precision.mean() / N


class ClassificationMeanRecall(BaseMetric):

    def __init__(self, n_classes):
        super(ClassificationMeanRecall, self).__init__(
            'classification-mean-recall'
        )
        self.n_classes = n_classes

    def __call__(self, output, target, N):
        C = confusion_matrix(output, target, self.n_classes)
        recall = torch.diag(C) / torch.sum(C, 1)
        recall[recall != recall] = 0.
        self.result = recall.mean() / N


class ClassificationPerClassAccuracy(BaseMetric):

    def __init__(self, class_id, n_classes):
        super(ClassificationPerClassAccuracy, self).__init__(
            'classification-per-class-accuracy-' + str(class_id)
        )
        self.class_id = class_id
        self.n_classes = n_classes

    def __call__(self, output, target, N):
        C = confusion_matrix(output, target, self.n_classes)
        C = C / C.sum(axis=1)[:, None]
        C[C != C] = 0.
        self.result = torch.diag(C)[self.class_id] / N
