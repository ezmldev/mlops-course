import os

import mlflow
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


class SpamService:
    def __init__(self, spam_model):
        self.spam_model = spam_model

        self.app = FastAPI()
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

        @self.app.post("/invocations/")
        async def root(payload: dict):
            return int(self.spam_model.predict(payload["data"])[0])


if __name__ == "__main__":
    spam_model = mlflow.pyfunc.load_model(os.environ["MODEL_PATH"])
    spam_service = SpamService(spam_model)

    uvicorn.run(spam_service.app, port=5000, log_level="info")
