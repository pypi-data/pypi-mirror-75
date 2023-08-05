import torch
from .distance_miner import DistanceMiner


class PairwiseMiner(DistanceMiner):
    def __init__(self, cos=False, **kwargs):
        super().__init__(cos=cos, **kwargs)

    def forward(self, x1, x2):
        matrix = self.create_matrix(x1, x2)
        with torch.no_grad():
            if self.cos:
                idx = torch.argmax(matrix, dim=-1)
            else:
                idx = torch.argmin(matrix, dim=-1)
        x1 = torch.cat((x1, x1), dim=0)
        x2 = torch.cat((x2, x2[idx]), dim=0)
        labels = torch.cat((torch.ones(idx.size(0)), torch.zeros(idx.size(0))), dim=0)
        return x1, x2, labels
