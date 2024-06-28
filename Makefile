# This Makefile is for local development builds
# Jenkins produces builds for each push to git using the Jenkinsfile
SHELL := /usr/bin/env bash

build: lint test
	./batect requirements
	docker build -t 419929493928.dkr.ecr.eu-west-2.amazonaws.com/ecs-appmesh-task-helper:local .

debug:
	./batect shell

lint: 
	./batect format
	./batect lint

test:
	./batect test

.PHONY: build debug lint test