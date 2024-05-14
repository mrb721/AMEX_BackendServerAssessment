# FROM alpine:3
FROM python:3.11-slim
# FROM debian:12
WORKDIR /backendify
 
ENV STATSD_SERVER="STATSD_SERVER"

COPY ./requirements.txt /backendify/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /backendify/requirements.txt


COPY . /backendify/

# This Dockerfile is provided for empty as you will need to have a different
# kind of file depending on the language you use to solve this challenge.
# 
# Feel free to change it as much as needed so it is your solution the one that
# launches.

EXPOSE  9000

ENTRYPOINT ["python", "./backendify-app/main.py"]
# ENTRYPOINT ["gunicorn", "main:app", "--host", "0.0.0.0", "--port", "9000", "--reload", "us=http://provider:8001", "ru=http://provider:8002"]

#  us=http://api.github.com ru=http://api.github.com