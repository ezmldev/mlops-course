from typing import Any

import mlflow
from sklearn.pipeline import Pipeline


class ModelWithPreprocess(mlflow.pyfunc.PythonModel):
    def __init__(self, pipe_model: Pipeline) -> None:
        self.model = pipe_model

    def preprocess_input(self, payload: dict) -> str:
        if not isinstance(payload, dict) or "data" not in payload:
            raise TypeError(
                "Request payload must be a dict in " + '{"data": "message"} format',
            )
        return str(payload["data"])

    def predict(
        self, context: mlflow.pyfunc.PythonModelContext, model_input: dict[str, Any]
    ) -> int:
        processed_model_input = self.preprocess_input(model_input.copy())
        prediction = int(self.model.predict([processed_model_input])[0])
        return prediction
