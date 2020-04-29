FROM python:3.8.2-alpine3.11

WORKDIR /app

ADD requirements.txt /
RUN pip install -r /requirements.txt
RUN rm /requirements.txt

ADD task_helper/main.py /app
ADD task_helper/envoy_manager.py /app

CMD [ "python", "-u", "main.py" ]