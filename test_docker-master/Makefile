MAKEFILE := $(FIRSTWORD $(makefile_list))
SECOND_ARG := $(word 2, $(MAKECMDGOALS))

export DOCKER_IMAGE_TAG := local_dev_env:latest

export RUN_IN_DOCKER_WITH_DISK_AND_NETWORKING :=\
docker run \
--rm \
--network none \
-v `pwd`:/app

export RUN_IN_DOCKER :=\
docker run \
--rm \
--network none \
-v `pwd`:/app:ro \
-v `pwd` /test_reports:app/test_reports:rw

.DEFAULT:
		@exit 0

.PHONY: build
build: ## Builds docker image
		docker build build \
		--platform linux/amd64 \
		--tag $(DOCKER_IMAGE_TAG)

.PHONY: shell
shell: build ## Runs interactive shell
	docker run --rm -it -v `pwd`:/app $(DOCKER_IMAGE_TAG) /bin/bash
