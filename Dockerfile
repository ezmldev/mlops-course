# cp Dockerfile /workspaces/mlops-course/mlartifacts/334997387425955836/Dockerfile
FROM python
ADD ./my_xgboost /model/my_xgboost
WORKDIR /model/my_xgboost
RUN pip install -r requirements.txt

CMD mlflow models serve -p 5001 -h 0.0.0.0 -m file:/model/my_xgboost/ --no-conda
