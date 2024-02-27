# Note: using --name allows us to set a container name, so that we can easily
# remove it later :¬)

CONTAINER_NAME=fastapi-first-test-project-container
IMAGE_NAME=fastapi-first-test-project

up:
	docker run -d -p 127.0.0.1:8000:80 --name $(CONTAINER_NAME) $(IMAGE_NAME)

down:
	docker rm -f $(CONTAINER_NAME)