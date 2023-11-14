# %%

import bentoml

bentoml.mlflow.import_model("my_sklearn_model", model_uri="../spam_pipeline_model")

# %%
import mlflow

pyfunc_model: mlflow.pyfunc.PyFuncModel = bentoml.mlflow.load_model(
    "my_sklearn_model:latest"
)

# %%
import pandas as pd

content_df = pd.DataFrame(
    {
        "content": [
            "Click this link and subscribe to my channel!",
            "This is the best ever video about MLflow!",
        ]
    }
)

runner = bentoml.mlflow.get("my_sklearn_model:latest").to_runner()
runner.init_local()
runner.predict.run(input_data=content_df)

# %%
pipe = mlflow.sklearn.load_model("../spam_pipeline_model")
saved_model = bentoml.sklearn.save_model("my_bento_model", pipe)
