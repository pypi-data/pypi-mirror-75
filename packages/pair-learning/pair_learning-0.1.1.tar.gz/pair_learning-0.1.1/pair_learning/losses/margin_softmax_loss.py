import torch
from .pairwise_softmax_loss import PairwiseSoftmaxLoss


class MarginSoftmaxLoss(PairwiseSoftmaxLoss):
    def __init__(self, batch_size=None, s=20, m1=1, m2=0, m3=0, **kwargs):
        super().__init__(batch_size=batch_size, s=s, **kwargs)
        self.m1 = m1
        self.m2 = m2
        self.m3 = m3

    def add_margin(self, x):
        one_hot = torch.eye(x.size(0))
        x = torch.where(one_hot == 1, self.m1 * x, x)
        x = x + self.m2 * one_hot
        x = torch.cos(x) - self.m3 * one_hot
        return x
