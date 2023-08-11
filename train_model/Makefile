build:
	docker build --target model-build  -t ttl.sh/mlflow-spam -t ghcr.io/$${GITHUB_REPOSITORY%/*}/mlflow-spam .
	docker build -t ttl.sh/spam-model -t ghcr.io/$${GITHUB_REPOSITORY%/*}/spam-model .

volume:
	docker volume rm model
	docker run -v model:/model --rm ttl.sh/spam-model sh -c 'cp -r /volume-data/* /model'

run-volume: build volume
	docker run -d -p 5000:5000 -v model:/model ghcr.io/ezmlops/mlflow:v1.0

run-embedded: build
	docker run -d -p 5000:5000 ttl.sh/mlflow-spam

test:
	curl   -H "content-type: application/json"   localhost:5000/invocations   -d '{"inputs": {"data": "subscribe my channel"}}'

clean:
	docker rm -f $(shell docker ps -qa) || true
	docker volume prune -f