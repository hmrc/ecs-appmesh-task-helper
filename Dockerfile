ARG DOCKERHUB=dockerhub.tax.service.gov.uk
FROM ${DOCKERHUB}/python:3.10.11-alpine3.18

RUN addgroup -g 1001 runner && adduser -D -u 1001 -G runner -h /app runner

ADD requirements.txt /
RUN pip install -r /requirements.txt
RUN rm /requirements.txt

ADD task_helper/main.py /app
ADD task_helper/envoy_manager.py /app
ADD task_helper/environment_variables.py /app

RUN chmod 0664 /app/*.py

USER runner

WORKDIR /app

ENV ENABLE_JSON_LOGGING 1

CMD [ "python", "-u", "main.py" ]
