build:
	docker build -t ghcr.io/$${GITHUB_REPOSITORY%/*}/model-spam .

volume:
	docker volume rm model 2>/dev/null || true
	docker run -v model:/model --rm ghcr.io/$${GITHUB_REPOSITORY%/*}/model-spam sh -c 'cp -r /volume-data/* /model'

run-volume: build volume
	docker run -d -p 5000:5000 -v model:/model ghcr.io/ezmldev/model-serving:v1.0

run-embedded: build
	docker run -d -p 5000:5000 ttl.sh/mlflow-spam

test:
	curl   -H "content-type: application/json"   localhost:5000/invocations/   -d '{"data": "subscribe my channel"}'

clean:
	docker rm -f $(shell docker ps -qa) || true
	docker volume prune -f