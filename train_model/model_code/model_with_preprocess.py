import mlflow


class ModelWithPreprocess(mlflow.pyfunc.PythonModel):
    def __init__(self, pipe_model):
        self.model = pipe_model

    def preprocess_input(self, payload: dict) -> str:
        if (
            not isinstance(payload, dict)
            or "data" not in payload
            or not isinstance(payload["data"], str)
        ):
            raise TypeError(
                "Request payload must be a dict in " + '{"data": "message"} format',
            )
        return payload["data"]

    def predict(self, context, model_input: str) -> int:
        processed_model_input = self.preprocess_input(model_input.copy())
        prediction = self.model.predict([processed_model_input])[0]
        return prediction
