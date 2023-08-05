import math
import torch
import torch.nn.functional as F
from .base_loss import BaseLoss


class PairwiseSoftmaxLoss(BaseLoss):
    def __init__(self, batch_size=None, s=20, **kwargs):
        super().__init__(**kwargs)
        if batch_size is None:
            self.s = s
        else:
            self.s = math.sqrt(2) * math.log(batch_size - 1)

    def cal_matric(self, x1, x2):
        x1 = F.normalize(x1, p=self.p, dim=-1)
        x2 = F.normalize(x2, p=self.p, dim=-1)
        x = torch.mm(x1, x2.T)
        x = torch.acos(torch.clamp(x, -1.0 + 1e-7, 1.0 - 1e-7))
        return x

    def scale(self, x):
        return x * self.s

    def add_margin(self, x):
        return torch.cos(x)

    def forward(self, x1, x2):
        x = self.cal_matric(x1, x2)
        x = self.add_margin(x)
        x = self.scale(x)
        x = torch.exp(x)
        x = x / x.sum(-1, keepdim=True)
        x = - torch.log(x)
        losses = torch.diag(x)
        return self.reducer(losses)
