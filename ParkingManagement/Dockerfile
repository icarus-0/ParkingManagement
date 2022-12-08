FROM python:3

ENV PYTHONUNBUFFERED 1

WORKDIR /parking_management

ADD . /parking_management

COPY ./requirements.txt /parking_management/requirements.txt

RUN pip install --upgrade pip

RUN pip install -r requirements.txt



