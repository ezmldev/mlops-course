import logging
from pathlib import Path

import pandas as pd

from .helper_functions import *

# Set up logging
logging.root.setLevel(logging.INFO)

# Make sure pandas has doesn't truncate the output
pd.set_option("display.max_colwidth", None)
pd.options.display.max_rows = 4000

# Make sure we don't get any deprecation warnings from mlflow
from warnings import simplefilter

simplefilter(action="ignore", category=FutureWarning)
simplefilter(action="ignore", category=UserWarning)
