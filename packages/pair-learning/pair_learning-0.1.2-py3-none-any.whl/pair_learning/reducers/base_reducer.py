import torch.nn as nn


class BaseReducer(nn.Module):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def forward(self):
        raise NotImplementedError