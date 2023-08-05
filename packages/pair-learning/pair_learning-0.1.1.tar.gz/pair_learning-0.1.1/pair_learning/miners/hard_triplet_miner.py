import torch
import torch.nn.functional as F
from .distance_miner import DistanceMiner


class HardTripletMiner(DistanceMiner):
    def __init__(self, cos=True, **kwargs):
        super().__init__(cos=cos, **kwargs)

    def forward(self, x, pos):
        matrix = self.create_matrix(x, pos)
        with torch.no_grad():
            if self.cos:
                idx = torch.argmax(matrix, dim=-1)
            else:
                idx = torch.argmin(matrix, dim=-1)
            neg = pos[idx]
        return x, pos, neg