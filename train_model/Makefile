build:
	docker build --target mlflow  -t ttl.sh/mlflow -t ghcr.io/lalyos/mlflow .
	docker build --target model-build  -t ttl.sh/mlflow-spam -t ghcr.io/lalyos/mlflow-spam .
	docker build -t ttl.sh/spam-model -t ghcr.io/lalyos/spam-model .

volume:
	docker run -v model:/model --rm ttl.sh/spam-model sh -c 'cp -r /volume-data/* /model'

run-volume: build volume
	docker run -d -p 5001:5001 -v model:/model ttl.sh/mlflow

run-embedded: build
	docker run -d -p 5001:5001 -e MLFLOW_MODEL_URI=file:/app/model/ ttl.sh/mlflow-spam

test:
	curl   -H "content-type: application/json"   localhost:5001/invocations   -d '{"inputs": ["subscribe my channel","this was great"]}'

clean:
	docker rm -f $(shell docker ps -qa) || true
	docker volume prune -f