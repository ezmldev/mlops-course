#!/usr/bin/env bash

set -x
exec mlflow models serve -p ${PORT:-5001} -h 0.0.0.0 -m ${MODEL_URI} --no-conda