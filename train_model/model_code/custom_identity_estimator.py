from typing import Any

from sklearn.base import BaseEstimator, TransformerMixin


class CustomIdentityEstimator(BaseEstimator, TransformerMixin):
    def fit(self, **args) -> "CustomIdentityEstimator":
        return self

    def transform(self, X: Any) -> Any:
        return X
