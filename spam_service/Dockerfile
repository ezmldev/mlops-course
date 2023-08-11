ARG MODEL_IMG=ghcr.io/zoltanctoth/spam-model

FROM ghcr.io/zoltanctoth/mlflow AS serving-api
COPY requirements.txt /app/
WORKDIR /app
RUN pip install -r requirements.txt
COPY *.py /app/
ENV MODEL_PATH=/model
CMD [ "python", "service.py" ]

FROM ${MODEL_IMG} as model

FROM serving-api
COPY --from=model /volume-data /model