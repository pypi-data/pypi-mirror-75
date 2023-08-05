from .threshold_reducer import ThresholdReducer


class MeanNonZeroReducer(ThresholdReducer):
    def __init__(self, **kwargs):
        super().__init__(threshold=0, **kwargs)