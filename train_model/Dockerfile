FROM python:alpine as mlflow

RUN apk add bash curl py3-scikit-learn py3-pandas py3-numpy py3-pyarrow py3-matplotlib
ENV PYTHONPATH=/usr/lib/python3.11/site-packages/
RUN pip install mlflow

COPY start.sh /
RUN chmod 755 /start.sh

VOLUME /model
ENV MLFLOW_MODEL_URI=file:/model/
EXPOSE 5001
CMD [ "/start.sh" ]

FROM mlflow as model-build
COPY data /app/data
COPY model_code *.py /app/model_code
COPY *.py /app/
WORKDIR /app
ENV MODEL_PATH=/app/model
RUN python train_model.py
ENV MLFLOW_MODEL_URI=file:/app/model/

FROM busybox as model
COPY --from=model-build /app/model /volume-data


