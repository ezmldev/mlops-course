# %%
"""Create training dataset"""

import csv
import datetime
import glob
import os
from pathlib import Path

import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB

data_files_dir = Path.cwd().parent / "data"
df = pd.read_csv(data_files_dir / "comments.csv")

print(f"Read total {len(df)} rows")
df.head(2)
# %%

vectorizer = CountVectorizer()
v_model = vectorizer.fit(df["content"])
X = v_model.transform(df["content"])
y = df["is_spam"]

# %%

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# %%

classifier = MultinomialNB()
classifier.fit(X_train, y_train)

y_pred = classifier.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

print(f"NB Accuracy: {accuracy}")

# %%
from sklearn.linear_model import LogisticRegression

classifier = LogisticRegression()
classifier.fit(X_train, y_train)

y_pred = classifier.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

print(f"LogReg Accuracy: {accuracy}")

# %%
from sklearn.ensemble import RandomForestClassifier

classifier = RandomForestClassifier(random_state=42)
classifier.fit(X_train, y_train)

y_pred = classifier.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

print(f"RF Accuracy: {accuracy}")
from sklearn.ensemble import RandomForestClassifier

# %%
from sklearn.model_selection import GridSearchCV

# Create a dictionary containing the hyperparameters and their possible values
param_grid = {
    "n_estimators": [10, 50, 100, 200],  # 200
    "max_depth": [None, 10, 20, 30],  # None
    "min_samples_split": [2, 5, 10],  # 2
}

# DEV to make it faster
param_grid = {
    "n_estimators": [200],  # 200
    "max_depth": [None, 10],  # None
    "min_samples_split": [2],  # 2
}

# Create a Random Forest classifier
rf = RandomForestClassifier(random_state=42)

# Create the grid search with cross-validation
classifier = GridSearchCV(
    estimator=rf, param_grid=param_grid, cv=3, n_jobs=-1, verbose=2
)
classifier.fit(X_train, y_train)
best_params = classifier.best_params_
print(best_params)

best_model = classifier.best_estimator_
y_pred = best_model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

print(f"Accuracy of best model: {accuracy}")

# %%

# %%
import mlflow

mlflow.set_experiment("youtube-spam")

with mlflow.start_run() as run:
    model_info = mlflow.sklearn.log_model(pipe, "spam_model")

print(model_info.artifact_path)
# %%

artifact_path = f"runs:/{run.info.run_id}/{model_info.artifact_path}"
print(artifact_path)

reloaded_model = mlflow.pyfunc.load_model(artifact_path)

# %%
message = "Come subscribe to my channel"
is_spam = reloaded_model.predict([message])
print(message + " spam? " + str(bool(is_spam)))

# %%
import shutil

shutil.rmtree(os.path.join(THIS_FOLDER, "model"), ignore_errors=True)

model_dir = os.path.join(THIS_FOLDER, "model")
pip_requirements = [
    "numpy==1.24.4",
    "pandas==1.5.3",
    "scikit-learn==1.2.2",
    "mlflow==2.5",
]


class ModelWithPreprocess(mlflow.pyfunc.PythonModel):
    def __init__(self, pipe_model):
        self.model = pipe_model

    def preprocess_input(self, payload):
        if (
            not isinstance(payload, dict)
            or "data" not in payload
            or not isinstance(payload["data"], str)
        ):
            raise TypeError(
                "Request payload must be a dict in " + '{"data": "message"} format',
            )
        return payload["data"]

    def predict(self, context, model_input):
        processed_model_input = self.preprocess_input(model_input.copy())
        # proba = self.model.predict_proba([processed_model_input][0])
        prediction = self.model.predict([processed_model_input])[0]
        # return {
        #    "prediction": prediction,
        #    "probability": float(proba[1]),
        # }
        return prediction


model_w_preprocess = ModelWithPreprocess(pipe)

mlflow.pyfunc.save_model(
    path=model_dir,
    python_model=model_w_preprocess,
    code_path=[os.path.join(THIS_FOLDER, "model_code")],
    pip_requirements=pip_requirements,
    metadata={
        "model_type": "spam_classifier",
        "model_name": "spam_model",
        "model_version": "v1",
        "model_description": "Spam classifier trained on YouTube comments",
        "trained_at": datetime.datetime.utcnow().isoformat(),
        "accuracy": accuracy,
    },
)

m2 = mlflow.pyfunc.load_model(model_dir)
print("Prediction: " + str(m2.predict({"data": "Come subscribe to my channel"})))
print(m2.metadata.metadata)
# %%
