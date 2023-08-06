from .set_type_predictor import SetTypePredictor
from ..datasets import load_nan
from .simple_type import SimpleTypePredictor
import pandas as pd


class NaNType(SimpleTypePredictor):

    def __init__(self):
        super().__init__()
        self._predictor = SetTypePredictor(load_nan())

    def validate(self, candidate, **kwargs) -> bool:
        """Return boolean representing if given candidate is a NaN."""
        return self._predictor.validate(candidate) or pd.isna(candidate)
