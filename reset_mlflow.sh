#!/usr/bin/env bash

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

# Stop any running MLflow server
echo "Stopping any running MLflow server"
killall mlflow 2>/dev/null

# Remove any existing MLflow data
echo "Removing any existing MLflow data"
rm -rf ./.mlflow_data
mkdir -p ./.mlflow_data/artifacts

echo "DONE"
echo
echo "You can now start MLflow by running: ${SCRIPT_DIR}/start_mlflow_native.sh"
echo "Once MLflow is running, open a browser to http://localhost:5000 by clicking the popup in the lower right corner of VSCode."