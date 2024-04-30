DOCKER_USERNAME ?= gdel
APPLICATION_NAME ?= staircase
BACK_NAME = ${DOCKER_USERNAME}/${APPLICATION_NAME}/back
FRONT_NAME = ${DOCKER_USERNAME}/${APPLICATION_NAME}/front

build:
	docker build --tag ${FRONT_NAME} -f Dockerfile_front .
	docker build --tag ${BACK_NAME} -f Dockerfile_back .

run:
	docker run --rm -p 5000:5000 -v $(pwd)/data:/app/data ${BACK_NAME} &
	docker run --rm -p 4200:4200 ${FRONT_NAME} &