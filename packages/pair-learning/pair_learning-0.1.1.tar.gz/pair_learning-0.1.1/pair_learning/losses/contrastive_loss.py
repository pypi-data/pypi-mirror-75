import torch.nn.functional as F
from torch.nn import CosineSimilarity, PairwiseDistance
from .base_loss import BaseLoss
from ..miners import PairwiseMiner


class ContrastiveLoss(BaseLoss):
    """
    Contrastive loss using either euclidean distance or cosine similarity.
    Args:
        cos: If True, will use cosine similarity. Otherwise, euclidean distance will
             be used.
        pos_margin: The distance (or similarity) over (under) which positive pairs
                    will contribute to the loss.
        neg_margin: The distance (or similarity) under (over) which negative pairs
                    will contribute to the loss.
        power: Each pair's loss will be raised to this power.
    """
    def __init__(self, cos=False, pos_margin=0, neg_margin=1, power=2, miner=None, **kwargs):
        super().__init__(**kwargs)
        self.cos = cos
        self.pos_margin = pos_margin
        self.neg_margin = neg_margin
        self.power = power
        self.miner = miner if miner is not None else PairwiseMiner(cos=cos)
        if self.cos:
            self.metric = CosineSimilarity(dim=-1)
        else:
            self.metric = PairwiseDistance(p=self.p)

    def forward(self, x1, x2, labels=None):
        if labels is None:
            x1, x2, labels = self.miner(x1, x2)
        dist = self.metric(x1, x2)
        labels = labels.float()
        if self.cos:
            losses = labels / self.power * (F.relu(self.pos_margin - dist) ** self.power)
            losses += (1 - labels) / self.power * (F.relu(dist - self.neg_margin) ** self.power)
        else:
            losses = labels / self.power * (F.relu(dist - self.pos_margin) ** self.power)
            losses += (1 - labels) / self.power * (F.relu(self.neg_margin - dist) ** self.power)
        return self.reducer(losses)
