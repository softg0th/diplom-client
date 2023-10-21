FROM python:3
ENV PYTHONUNBUFFERED 1
WORKDIR /code
RUN apt-get update && apt-get upgrade -y
ADD requirements.txt /code/
RUN pip install --upgrade pip && pip install -r requirements.txt
ADD . /code/