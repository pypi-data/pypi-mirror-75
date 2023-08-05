import math
import torch
from .margin_softmax_loss import MarginSoftmaxLoss


class AdaptiveSoftmaxLoss(MarginSoftmaxLoss):
    def __init__(self, batch_size, **kwargs):
        super().__init__(**kwargs)
        self.b = torch.tensor(0).float()
        self.t = torch.tensor(0).float()
        self.s = torch.tensor(math.sqrt(2) * math.log(batch_size - 1)).float()

    def scale(self, x):
        if self.training:
            with torch.no_grad():
                theta = torch.acos(torch.clamp(x, -1.0 + 1e-7, 1.0 - 1e-7))
                one_hot = torch.eye(x.size(0))
                self.b = torch.where(one_hot == 1, torch.zeros_like(x), torch.exp(x * self.s))
                self.b = torch.sum(self.b) / x.size(0)
                self.t = torch.median(theta[one_hot == 1])
                self.s = torch.log(self.b) / \
                    torch.cos(torch.min(math.pi / 4 * torch.ones_like(self.t), self.t))
        return x * self.s
