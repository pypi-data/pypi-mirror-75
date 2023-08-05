import torch
import torch.nn.functional as F
from .base_miner import BaseMiner
from ..utils import pairwise_distance


class DistanceMiner(BaseMiner):
    def __init__(self, cos=False, **kwargs):
        super().__init__(**kwargs)
        self.cos = cos

    def create_matrix(self, x1, x2):
        with torch.no_grad():
            if self.cos:
                x1 = F.normalize(x1, p=self.p, dim=-1)
                x2 = F.normalize(x2, p=self.p, dim=-1)
                matrix = torch.mm(x1, x2.T)
                matrix = matrix - 2 * torch.eye(matrix.size(0))
            else:
                matrix = pairwise_distance(x1, x2)
                one_hot = torch.eye(matrix.size(0))
                penalty = float('inf') * torch.ones_like(matrix)
                matrix = torch.where(one_hot == 1, penalty, matrix)
        return matrix

    def forward(self, x1, x2):
        raise NotImplementedError
