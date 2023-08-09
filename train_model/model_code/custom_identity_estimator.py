from sklearn.base import BaseEstimator, TransformerMixin


class CustomIdentityEstimator(BaseEstimator, TransformerMixin):
    def fit(self, **args):
        return self

    def transform(self, X):
        return X
