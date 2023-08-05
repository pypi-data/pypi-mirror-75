from .base_reducer import BaseReducer
import torch


class MeanReducer(BaseReducer):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def forward(self, losses):
        return torch.mean(losses)