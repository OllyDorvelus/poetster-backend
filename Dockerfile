FROM python:3.7-slim
MAINTAINER Slader

# create project directory
RUN mkdir /usr/src/poetster
WORKDIR /usr/src/poetster

# install dependencies
COPY requirements.txt /usr/src/poetster
RUN pip install -r requirements.txt

# copy project to env
COPY . /usr/src/poetster





