import logging
import sys
from pathlib import Path
from warnings import simplefilter

import mlflow
import pandas as pd
import requests
from IPython.display import Image, display


def mlflow_connect() -> mlflow.entities.experiment.Experiment:
    """
    Connect to the MLflow server on localhost and create an experiment if it doesn't exist.
    """

    try:
        requests.get("http://localhost:5000", timeout=1)
        logging.info(
            f"OK - mlflow server is up and running. Setting Tracking URI to http://localhost:5000. Setting Experiment to '{MLFLOW_EXPERIMENT_NAME}'"
        )
        mlflow.set_tracking_uri("http://localhost:5000")
        return mlflow.set_experiment(MLFLOW_EXPERIMENT_NAME)
    except requests.exceptions.RequestException:
        logging.warning(
            f"MLflow server is not running. Please run '{PROJECT_ROOT_DIR}/start_mlflow_native.sh' in a terminal.",
            file=sys.stderr,
        )
        logging.info(
            "Once MLflow is running, make sure you open http://localhost:5000/ in a browser.",
            file=sys.stderr,
        )
        display(
            Image(
                filename=f"{PROJECT_ROOT_DIR}/course_helpers/images/mlflow_open_port.png",
                width=300,
            )
        )
        sys.exit(1)


def load_dataset():
    """
    Loads the spam dataset from the data directory.
    """
    spam_data_file = Path.cwd().parent / "data" / "comments.csv"
    if not spam_data_file.exists():
        logging.error(f"Can't find {spam_data_file}")
        raise SystemExit(1)

    df = pd.read_csv(spam_data_file)

    logging.info(f"Loaded {len(df)} rows from {spam_data_file}")
    display(df.head(10))
    return df
