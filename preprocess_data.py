"""
Dataset: http://archive.ics.uci.edu/dataset/380/youtube+spam+collection
"""
# %%
"""Create training dataset"""

import csv
import glob
import os

import pandas

THIS_FOLDER = os.path.dirname(__file__)
csv_files = glob.glob(os.path.join(THIS_FOLDER, "data", "*.csv"))
# %%
data = []

for f in csv_files:
    with open(f, newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            data.append({"content": row["CONTENT"], "is_spam": row["CLASS"]})

print(f"Total {len(data)} rows")
# %%

df = pandas.DataFrame(data)

from sklearn.feature_extraction.text import CountVectorizer

vectorizer = CountVectorizer()
v_model = vectorizer.fit(df["content"])
X = v_model.transform(df["content"])
y = df["is_spam"]

# %%
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
# %%
from sklearn.naive_bayes import MultinomialNB

classifier = MultinomialNB()
classifier.fit(X_train, y_train)

from sklearn.metrics import accuracy_score

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
from sklearn.pipeline import Pipeline

pipe = Pipeline([("count_vectorizer", v_model), ("rf", best_model)])
messages = [
    "I love this video!",
    "Come subscribe to my channel",
    "If you want to see more videos like this, check out this video",
    "This is the funniest video in the world!",
]

predictions = pipe.predict(messages)

for t in zip(messages, predictions):
    print(t)


# %%
import mlflow

mlflow.set_experiment("youtube-spam")

with mlflow.start_run():
    mlflow.sklearn.log_model(pipe, "spam_model")
