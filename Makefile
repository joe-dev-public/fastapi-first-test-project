# Note: using --name allows us to set a container name, so that we can easily
# remove it later :¬)

CONTAINER_NAME=fastapi-first-test-project-container
IMAGE_NAME=fastapi-first-test-project

build:
	docker build -t $(IMAGE_NAME) .

# Bind mount to watch code files and live-reload (local dev only)
# Todo: something like src="$(shell pwd)./app" might better?
# Todo: use env vars to check for dev vs prod (vs test), etc.
# Todo: use docker-compose instead! ;¬)
up:
	docker run -d -p 127.0.0.1:8000:80 --network some-network --network-alias fastapi-server --mount type=bind,src=./app,target=/code/app --name $(CONTAINER_NAME) $(IMAGE_NAME)

down:
	docker rm -f $(CONTAINER_NAME)

bash:
	docker exec -it $(CONTAINER_NAME) bash

logs:
	docker logs $(CONTAINER_NAME)