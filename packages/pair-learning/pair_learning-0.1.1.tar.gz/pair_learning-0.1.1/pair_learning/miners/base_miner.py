import torch.nn as nn


class BaseMiner(nn.Module):
    """
    Args:
        p: The exponent value in the norm formulation.
    """
    def __init__(self, p=2, **kwargs):
        super().__init__(**kwargs)
        self.p = p

    def forward(self, x1, x2):
        raise NotImplementedError