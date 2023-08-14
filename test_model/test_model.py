import os

import mlflow
import pytest

PROJECT_ROOT_DIR = os.path.dirname(os.path.dirname(__file__))


@pytest.fixture(scope="session")
def model():
    return mlflow.pyfunc.load_model(os.path.join(PROJECT_ROOT_DIR, "models"))


def test_predictions(model):
    assert model.predict({"data": "Subscribe to my channel!"}) == 1
    assert model.predict({"data": "This video is great!"}) == 0


def test_accuracy_baseline(model):
    accuracy_baseline = 0.9
    model_accuracy = float(model.metadata.metadata["accuracy"])
    assert (
        model_accuracy >= accuracy_baseline
    ), f"Model accuracy ({model_accuracy}) is lower than baseline ({accuracy_baseline})"
