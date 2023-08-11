FROM ghcr.io/ezmlops/mlflow:v1.0 as model-build
COPY data /app/data
COPY model_code *.py /app/model_code/
COPY *.py /app/
WORKDIR /app
ENV MODEL_PATH=/app/model
RUN python train_model.py
ENV MLFLOW_MODEL_URI=file:/app/model/

FROM busybox as model
COPY --from=model-build /app/model /volume-data
