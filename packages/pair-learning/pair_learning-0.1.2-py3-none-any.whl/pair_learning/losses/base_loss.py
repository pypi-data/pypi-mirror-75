import torch.nn as nn
from ..reducers import MeanReducer


class BaseLoss(nn.Module):
    """
    Args:
        p: The exponent value in the norm formulation.
    """
    def __init__(self, p=2, reducer=None, **kwargs):
        super().__init__(**kwargs)
        self.p = p
        self.reducer = self.get_reducer() if reducer is None else reducer

    def forward(self, x1, x2):
        raise NotImplementedError

    def get_reducer(self):
        return MeanReducer()