SHELL := /usr/bin/env bash
DOCKER_OK := $(shell type -P docker)
PYTHON_VERSION := 3.8.2
REPO_HOST := local
VERSION := development
POETRY_RUNNER := docker run -u `id -u`:`id -g` -v `pwd`:/app --rm python-poetry:$(PYTHON_VERSION)

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

update: build_test_container
	@mkdir -p .cache
	@$(POETRY_RUNNER) poetry update

setup: build_test_container
	@echo '**************** Creating virtualenv *******************'
	@$(POETRY_RUNNER) poetry install --no-root
	@echo '*************** Installation Complete ******************'

setup_git_hooks: setup
	@echo '****** Setting up git hooks ******'
	@$(POETRY_RUNNER) poetry run pre-commit install

install: setup setup_git_hooks  ## Install a local development environment

typechecking: setup
	@$(POETRY_RUNNER) poetry run mypy ./task_helper

black: setup
	@$(POETRY_RUNNER) poetry run black ./task_helper

security_checks: setup
	@$(POETRY_RUNNER) poetry run safety check
	@$(POETRY_RUNNER) poetry run bandit -r ./task_helper --skip B303 --exclude ./task_helper/test_envoy_manager.py,./task_helper/test_environment_variables.py

test: setup typechecking  ## Run tests
	@find . -type f -name '*.pyc' -delete
	@$(POETRY_RUNNER) poetry run pytest ./task_helper

clean:  ## Delete virtualenv
	@rm -rf ./.venv
	@rm -rf ./.cache

build: setup test security_checks
	@$(POETRY_RUNNER) poetry export -f requirements.txt > ./requirements.txt --without-hashes
	@docker build --tag $(REPO_HOST)/ecs-appmesh-task-helper:$(VERSION) . 
	@rm -rf ./requirements.txt

push_image: ## Push the docker image to artifactory
	@docker push $(REPO_HOST)/ecs-appmesh-task-helper:$(VERSION)

push_latest: ## Push the latest tag to artifactory
	@docker tag $(REPO_HOST)/ecs-appmesh-task-helper:$(VERSION) $(REPO_HOST)/ecs-appmesh-task-helper:latest
	@docker push $(REPO_HOST)/ecs-appmesh-task-helper:latest

build_test_container:
	@docker build -t python-poetry:$(PYTHON_VERSION) -f poetry.Dockerfile .
