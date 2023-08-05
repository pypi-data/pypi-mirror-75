from .base_reducer import BaseReducer
import torch


class ThresholdReducer(BaseReducer):
    def __init__(self, threshold, **kwargs):
        super().__init__(**kwargs)
        self.threshold = threshold

    def forward(self, losses):
        valid_idx = losses > self.threshold
        if torch.sum(valid_idx):
            loss = torch.mean(losses[valid_idx])
        else:
            loss = torch.mean(losses) * 0
        return loss