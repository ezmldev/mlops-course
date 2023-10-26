import logging
import sys
from pathlib import Path
from typing import Optional

import mlflow
import pandas as pd
import requests
from IPython.display import Image, display
from termcolor import colored

# Have a global variable for the project root directory
PROJECT_ROOT_DIR = Path(__file__).parent.parent

# Set up MLflow defaults for the course
MLFLOW_EXPERIMENT_NAME = "Spam Detection"


def mlflow_connect() -> Optional[mlflow.entities.experiment.Experiment]:
    """
    Connect to the MLflow server on localhost and create an experiment if it doesn't exist.
    """

    try:
        requests.get("http://localhost:5000", timeout=1)
        print(
            colored("OK", "green")
            + f" - mlflow server is up and running. Setting Tracking URI to http://localhost:5000. Setting Experiment to '{MLFLOW_EXPERIMENT_NAME}'",
            file=sys.stderr,
        )
        mlflow.set_tracking_uri("http://localhost:5000")
        return mlflow.set_experiment(MLFLOW_EXPERIMENT_NAME)
    except Exception:
        print(
            colored(f"The MLflow server is not running.", "red")
            + f"\nPlease run '{PROJECT_ROOT_DIR}/start_mlflow_native.sh' in the Terminal.",
            file=sys.stderr,
        )
        print(
            "Once MLflow is running, make sure you open http://localhost:5000/ in a browser.",
            file=sys.stderr,
        )
        display(
            Image(
                filename=f"{PROJECT_ROOT_DIR}/course_helpers/images/mlflow_open_port.png",
                width=300,
            )
        )
        return None


def load_dataset() -> pd.DataFrame:
    """
    Loads the spam dataset from the data directory.
    """
    spam_data_file = Path(__file__).parent.parent / "data" / "comments.csv"
    if not spam_data_file.exists():
        logging.error(f"Can't find {spam_data_file}")
        raise SystemExit(1)

    df = pd.read_csv(spam_data_file)

    logging.info(f"Loaded {len(df)} rows from {spam_data_file}. First three records:")
    display(df.head(3))
    return df
