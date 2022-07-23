FROM python:3.7-slim

WORKDIR /project

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt