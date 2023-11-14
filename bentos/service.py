import bentoml
import numpy as np
from bentoml.io import NumpyNdarray

mrunner = bentoml.mlflow.get("my_sklearn_model:6yamececgc576ycf").to_runner()

svc = bentoml.Service("iris_classifier_2", runners=[mrunner])


@svc.api(input=NumpyNdarray(), output=NumpyNdarray())
def classify(input_series: np.ndarray) -> np.ndarray:
    result = mrunner.predict.run(input_series)
    return result
