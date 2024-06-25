# This Makefile is for local development builds
# Jenkins produces builds for each push to git using the Jenkinsfile
SHELL := /usr/bin/env bash

all: ecs-appmesh-task-helper

LOCAL_TAG:=local
GIT_TAG:=$(shell git describe --dirty=+WIP-${USER}-$(shell date "+%Y-%m-%dT%H:%M:%S%z") --always)

ecs-appmesh-task-helper:
	./batect requirements
	docker build -t 419929493928.dkr.ecr.eu-west-2.amazonaws.com/ecs-appmesh-task-helper:$(LOCAL_TAG) .

test: ecs-appmesh-task-helper
	./batect test

debug: ecs-appmesh-task-helper
	./batect shell

lint: 
	./batect lint

.PHONY: ecs-appmesh-task-helper lint