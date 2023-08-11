import os

import mlflow
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

THIS_DIR = os.path.dirname(__file__)
PROJECT_ROOT_DIR = os.path.dirname(THIS_DIR)


class MLService:
    def __init__(self, model):
        self.model = model

        self.app = FastAPI(
            title=model.metadata.metadata["model_name"],
            version=model.metadata.metadata["model_version"],
            description=model.metadata.metadata["model_description"],
        )
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

        @self.app.get("/metadata")
        async def metadata():
            return self.model.metadata._metadata

        @self.app.post("/invocations/")
        async def invocations(payload: dict):
            try:
                return int(self.model.predict([payload["data"]])[0])
            except Exception as e:
                raise HTTPException(
                    status_code=400,
                    detail=str(e),
                )


if __name__ == "__main__":
    pyfunc_model = mlflow.pyfunc.load_model(os.environ["MODEL_PATH"])
    ml_service = MLService(pyfunc_model)

    uvicorn.run(ml_service.app, port=5000, log_level="info")
