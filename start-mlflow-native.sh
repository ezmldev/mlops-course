mlflow server \
    --backend-store-uri sqlite:///.mlflow_data/mlflow.db \
    --default-artifact-root ./.mlflow_data/artifacts \
    --host 0.0.0.0 \
    --port 5000