import torch.nn.functional as F
from torch.nn import CosineSimilarity, PairwiseDistance
from .base_loss import BaseLoss
from ..miners import HardTripletMiner


class TripletLoss(BaseLoss):
    """
    Args:
        cos: If True, will use cosine similarity. Otherwise, euclidean distance will
             be used.
        margin: The desired difference between the anchor-positive distance and the
                anchor-negative distance.
    """
    def __init__(self, cos=True, margin=0.05, miner=None, **kwargs):
        super().__init__(**kwargs)
        self.cos = cos
        self.margin = margin
        self.miner = miner if miner is not None else HardTripletMiner(cos=cos)
        if self.cos:
            self.metric = CosineSimilarity(dim=-1)
        else:
            self.metric = PairwiseDistance(p=self.p)

    def forward(self, x, pos, neg=None):
        if neg is None:
            x, pos, neg = self.miner(x, pos)
        pos_dist = self.metric(x, pos)
        neg_dist = self.metric(x, neg)
        diff = pos_dist - neg_dist
        if self.cos:
            diff *= -1
        losses = F.relu(diff + self.margin)
        return self.reducer(losses)