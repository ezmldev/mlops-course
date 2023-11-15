GITHUB_REPOSITORY_OWNER ?= ezmldev
build:
	docker build -t ghcr.io/$(GITHUB_REPOSITORY_OWNER)/ezmodel-spam .
	docker build --target serving-with-model  -t ghcr.io/$(GITHUB_REPOSITORY_OWNER)/ezserving-spam .

volume:
	docker volume rm model 2>/dev/null || true
	docker run -v model:/model --rm ghcr.io/$(GITHUB_REPOSITORY_OWNER)/ezmodel-spam sh -c 'cp -r /volume-data/* /model'

run-volume: build volume
	docker run -d -p 6000:5000 -v model:/model ghcr.io/ezmldev/serving-api:1.2

run-embedded: build
	docker run -d -p 6000:5000 ghcr.io/$(GITHUB_REPOSITORY_OWNER)/ezserving-spam

test:
	curl -H "content-type: application/json"   localhost:6000/invocations/   -d '{"content": "subscribe my channel"}'
	@echo

clean:
	docker rm -f $(shell docker ps -qa) || true
	docker volume prune -f