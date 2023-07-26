SHELL := /usr/bin/env bash
DOCKER_OK := $(shell type -P docker)
REPO_HOST := local
VERSION := development

default: help

help: ## The help text you're reading
	@grep --no-filename -E '^[a-zA-Z1-9_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
.PHONY: help

check_docker:
	@echo '********** Checking for docker installation *********'
    ifeq ('$(DOCKER_OK)','')
	    $(error package 'docker' not found!)
    else
	    @echo Found docker!
    endif

update:
	@mkdir -p .cache
	@poetry update

setup:
	@echo '**************** Creating virtualenv *******************'
	@pip install --index-url https://artefacts.tax.service.gov.uk/artifactory/api/pypi/pips/simple/ --upgrade poetry
	@poetry install
	@echo '*************** Installation Complete ******************'

install: setup  ## Install a local development environment

typechecking: setup
	@poetry run mypy ./task_helper

black: setup
	@poetry run black ./task_helper

security_checks: setup
	@poetry run bandit -r ./task_helper --skip B303 --exclude ./task_helper/test_envoy_manager.py,./task_helper/test_environment_variables.py,./task_helper/test_application_health_check.py

test: setup typechecking  ## Run tests
	@find . -type f -name '*.pyc' -delete
	@poetry run pytest ./task_helper

clean:  ## Delete virtualenv
	@rm -rf ./.venv
	@rm -rf ./.cache

build: setup test security_checks
	@poetry export -f requirements.txt > ./requirements.txt --without-hashes
	echo ${VERSION}
	@docker build --tag $(REPO_HOST)/ecs-appmesh-task-helper:$(VERSION) .
	@rm -rf ./requirements.txt

push_image: ## Push the docker image to artifactory
	echo $(cat .version)
	@docker push $(REPO_HOST)/ecs-appmesh-task-helper:$(VERSION)

push_latest: ## Push the latest tag to artifactory
	@docker tag $(REPO_HOST)/ecs-appmesh-task-helper:$(VERSION) $(REPO_HOST)/ecs-appmesh-task-helper:latest
	@docker push $(REPO_HOST)/ecs-appmesh-task-helper:latest

push_experimental: ## Push the experimental tag to artifactory
	@docker tag $(REPO_HOST)/ecs-appmesh-task-helper:$(VERSION) $(REPO_HOST)/ecs-appmesh-task-helper:experimental
	@docker push $(REPO_HOST)/ecs-appmesh-task-helper:experimental
