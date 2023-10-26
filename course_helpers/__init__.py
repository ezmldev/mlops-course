import logging
from pathlib import Path
from warnings import simplefilter

import pandas as pd

from .helper_functions import *

# Set up logging
logging.root.setLevel(logging.INFO)

# Make sure pandas has doesn't truncate the output
pd.set_option("display.max_colwidth", None)
pd.options.display.max_rows = 4000

# Make sure we don't get any deprecation warnings from scikit-learn and mlflow
simplefilter(action="ignore", category=FutureWarning)

# Have a global variable for the project root directory
PROJECT_ROOT_DIR = Path(__file__).parent.parent

# Set up MLflow defaults for the course
MLFLOW_EXPERIMENT_NAME = "Spam Detection"
