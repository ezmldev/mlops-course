FROM python:alpine as mlflow

RUN apk add bash curl py3-scikit-learn py3-pandas py3-numpy py3-pyarrow py3-matplotlib
ENV PYTHONPATH=/usr/lib/python3.11/site-packages/
RUN pip install mlflow


# cp -r ./mlruns/827003277591383190/89608b2de76040cbbc9d971ddd88d222/artifacts/spam_model  .
#ADD spam_model /model

COPY start.sh /
RUN chmod 755 /start.sh

VOLUME /model
ENV MODEL_URI=file:/model/
EXPOSE 5001
CMD [ "/start.sh" ]

FROM mlflow as model-build
COPY data /app/data
COPY model_code *.py /app/model_code
COPY *.py /app/
WORKDIR /app
RUN python preprocess_data.py
ENV TMP=krumpli-v2

FROM busybox as model
COPY --from=model-build /app/model /volume-data


