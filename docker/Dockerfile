FROM ghcr.io/ezmldev/mlflow:v2.6.0 as model-build
COPY train_model.py /app/
WORKDIR /app
ENV MODEL_PATH=/app/model
ENV DATA_URL=https://ez-public.s3.amazonaws.com/comments.csv
RUN python train_model.py

FROM model-build as test
COPY tests /app/tests
RUN apk add py3-pytest-asyncio-pyc
RUN python -m pytest -v

FROM ghcr.io/ezmldev/serving-api:v1.1.0 as serving-with-model
COPY --from=model-build /app/model /app/model
ENV MODEL_PATH=/app/model

FROM busybox as model
COPY --from=model-build /app/model /volume-data
