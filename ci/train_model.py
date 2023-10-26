import datetime
import logging
from pathlib import Path

import pandas as pd

import mlflow
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
import pandas as pd
from mlflow.models import ModelSignature, infer_signature
from mlflow.types.schema import ColSpec, Schema
import os
import shutil
from warnings import simplefilter
simplefilter(action="ignore", category=FutureWarning)

if "MODEL_PATH" in os.environ:
    model_path = os.environ["MODEL_PATH"]
    spam_data_file = Path("/data/comments.csv")
else:
    model_path = Path(__file__).parent.parent / "models" / "spam_classifier_prod"
    spam_data_file = Path(__file__).parent.parent / "data" / "comments.csv"

if not spam_data_file.exists():
    logging.error(f"Can't find {spam_data_file}")
    raise SystemExit(1)

df = pd.read_csv(spam_data_file)

print(f"Loaded {len(df)} rows from {spam_data_file}")
print(f"Trainig model...")

# Initialize Random Forest model with best parameters
best_params = {"max_depth": None, "min_samples_split": 2, "n_estimators": 200}

X = df[["content"]]
y = df["is_spam"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

count_vectorizer = CountVectorizer()
rf = RandomForestClassifier(random_state=42, **best_params)

col_trans = ColumnTransformer(
    transformers=[
        (
            "text to features",
            count_vectorizer,
            "content",
        )  # Apply CountVectorizer directly to the 'text' column
    ],
    remainder="drop",
)

pipe = Pipeline([("Preprocess", col_trans), ("RandomForest", rf)])
pipe.fit(X_train, y_train)
y_pred = pipe.predict(X_test)

accuracy = float(accuracy_score(y_test, y_pred))

print("Creating model artifact...")

pip_requirements = [
    "scikit-learn==1.2.2",
    "mlflow==2.7.1",
]

# Option 1: Manually construct the signature object
input_schema = Schema(
    [
        ColSpec("string", "content"),
    ]
)
output_schema = Schema([ColSpec("double", "is_spam")])
signature = ModelSignature(inputs=input_schema, outputs=output_schema)

content_df = pd.DataFrame(
    {
        "content": [
            "Click this link and subscribe to my channel!",
            "This is the best ever video about MLflow!",
        ]
    }
)


shutil.rmtree(model_path, ignore_errors=True)

mlflow.sklearn.save_model(
    pipe,
    path=model_path,
    input_example=content_df,
    pip_requirements=pip_requirements,
    signature=signature,
    metadata={
        "model_name": "Spam Classifier",
        "model_description": "Spam classifier trained on YouTube comments",
        "model_version": "1.0.0",
        "trained_at": datetime.datetime.utcnow().isoformat(),
        "accuracy": accuracy,
    },
)

print(f"Model saved to {model_path}")