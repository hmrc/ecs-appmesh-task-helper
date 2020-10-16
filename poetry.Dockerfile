FROM python:3.8.2-slim

ENV POETRY_VIRTUALENVS_IN_PROJECT=true

RUN pip install --upgrade pip && pip install poetry==1.0.10

RUN ln -s /app/.cache /.cache

WORKDIR /app
