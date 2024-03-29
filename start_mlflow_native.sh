#!/usr/bin/env bash
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

echo "Starting MLflow server on port 5000"
echo Once MLflow is running, open a browser to http://localhost:5000 by clicking the popup in the lower right corner of VSCode:
imgcat "${SCRIPT_DIR}/course_helpers/images/mlflow_open_port.png"

mlflow server \
    --backend-store-uri sqlite:///.mlflow_data/mlflow.db \
    --default-artifact-root ./.mlflow_data/artifacts \
    --host 0.0.0.0 \
    --port 5000
    --workers 1
