from .set_type_predictor import SetTypePredictor
from .simple_type import SimpleTypePredictor
from ..datasets import load_country_codes


class CountryCodeType(SimpleTypePredictor):

    def __init__(self):
        super().__init__()
        self._predictor = SetTypePredictor(
            load_country_codes(), normalize_values=True)

    def validate(self, candidate, **kwargs) -> bool:
        """Return boolean representing if given candidate is a valid country code."""
        return self._predictor.validate(candidate)
