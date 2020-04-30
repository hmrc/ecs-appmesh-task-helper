FROM python:3.8.2-alpine3.11

RUN addgroup -g 1001 runner && adduser -D -u 1001 -G runner -h /app runner

ADD requirements.txt /
RUN pip install -r /requirements.txt
RUN rm /requirements.txt

ADD task_helper/main.py /app
ADD task_helper/envoy_manager.py /app

RUN chmod 0664 /app/*.py

USER runner

WORKDIR /app

CMD [ "python", "-u", "main.py" ]