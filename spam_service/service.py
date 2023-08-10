import os

import mlflow
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware


class MLService:
    def __init__(self, model):
        self.model = model

        self.app = FastAPI()
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

        @self.app.get("/")
        async def model_info():
            return self.model.metadata._metadata

        @self.app.post("/invocations/")
        async def invocations(payload: dict):
            if (
                not isinstance(payload, dict)
                or "data" not in payload
                or not isinstance(str, payload["data"])
            ):
                raise HTTPException(
                    status_code=400,
                    detail="Request payload must be a dict in "
                    + '{"data": "message"} format',
                )
            return int(self.model.predict(payload["data"])[0])


if __name__ == "__main__":
    pyfunc_model = mlflow.pyfunc.load_model(os.environ["MODEL_PATH"])
    ml_service = MLService(pyfunc_model)

    uvicorn.run(ml_service.app, port=5000, log_level="info")
