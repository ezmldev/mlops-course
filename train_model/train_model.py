"""Create training dataset"""

import csv
import datetime
import glob
import logging
import os
import shutil

import mlflow
import pandas
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import accuracy_score
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.pipeline import Pipeline

from model_code.custom_identity_estimator import CustomIdentityEstimator
from model_code.model_with_preprocess import ModelWithPreprocess

logging.root.setLevel(logging.INFO)

THIS_DIR = os.path.dirname(__file__)
PROJECT_ROOT_DIR = os.path.dirname(THIS_DIR)

csv_files = glob.glob(os.path.join(THIS_DIR, "data", "*.csv"))

data = []
for f in csv_files:
    with open(f, newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            data.append({"content": row["CONTENT"], "is_spam": row["CLASS"]})

logging.info(f"Training model on {len(data)} rows")

df = pandas.DataFrame(data)


vectorizer = CountVectorizer()
v_model = vectorizer.fit(df["content"])
X = v_model.transform(df["content"])
y = df["is_spam"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

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

rf = RandomForestClassifier(random_state=42)
classifier = GridSearchCV(
    estimator=rf, param_grid=param_grid, cv=3, n_jobs=-1, verbose=2
)
classifier.fit(X_train, y_train)
best_params = classifier.best_params_
logging.info(f"Best Random Forest Parameters: {best_params}")

best_model = classifier.best_estimator_
y_pred = best_model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
logging.info(f"Accuracy of best model: {accuracy}")


pipe = Pipeline(
    [
        ("identity", CustomIdentityEstimator().fit()),
        ("count_vectorizer", v_model),
        ("rf", best_model),
    ]
)

if "MODEL_PATH" in os.environ:
    model_path = os.environ["MODEL_PATH"]
else:
    model_path = os.path.join(PROJECT_ROOT_DIR, "models")
shutil.rmtree(model_path, ignore_errors=True)

pip_requirements = [
    "numpy==1.24.4",
    "pandas==1.5.3",
    "scikit-learn==1.2.2",
    "mlflow==2.5",
]


model_w_preprocess = ModelWithPreprocess(pipe)

mlflow.pyfunc.save_model(
    path=model_path,
    python_model=model_w_preprocess,
    code_path=[os.path.join(THIS_DIR, "model_code")],
    pip_requirements=pip_requirements,
    metadata={
        "model_type": "Random Forest",
        "model_name": "spam_classifier",
        "model_description": "Spam classifier trained on YouTube comments",
        "model_version": "1.0.0",
        "trained_at": datetime.datetime.utcnow().isoformat(),
        "accuracy": str(accuracy),
    },
)

logging.info(f"Model saved to {model_path}")
