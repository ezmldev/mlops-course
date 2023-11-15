DATA_URL=https://ez-public.s3.amazonaws.com/comments.csv python train_model.py 

MODEL_PATH=/workspaces/mlops-course/models/spam_classifier_prod pytest
