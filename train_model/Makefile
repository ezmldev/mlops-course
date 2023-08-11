build:
	docker build --target mlflow  -t ttl.sh/mlflow -t ghcr.io/lalyos/mlflow .
	docker build --target model-build  -t ttl.sh/mlflow-spam -t ghcr.io/$${GITHUB_REPOSITORY%/*}/mlflow-spam .
	docker build -t ttl.sh/spam-model -t ghcr.io/$${GITHUB_REPOSITORY%/*}/spam-model .


volume:
	docker run -v model:/model --rm ttl.sh/spam-model sh -c 'cp -r /volume-data/* /model'

run-volume: build volume
	docker run -d -p 5001:5001 -v model:/model ttl.sh/mlflow

run-embedded: build
	docker run -d -p 5001:5001 ttl.sh/mlflow-spam

test:
	curl   -H "content-type: application/json"   localhost:5001/invocations   -d '{"inputs": {"data": "subscribe my channel"}}'

clean:
	docker rm -f $(shell docker ps -qa) || true
	docker volume prune -f