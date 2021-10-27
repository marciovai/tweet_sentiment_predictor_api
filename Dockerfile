# File for building Model and API environment inside a container
# Python environment will be based on requirements.txt
# BUILD: docker build -t model_api:latest . 
# RUN: docker run -it -v /path/to/model_api/:/external_lib/ -p 5000:5000 model_api sh -c 'cd external_lib && make api-start'

FROM ubuntu:xenial

# update dependencies
RUN apt-get update && apt-get upgrade -y
RUN apt-get install software-properties-common -y 

# install pip
RUN apt-get install -y python3-pip
RUN pip3 install --upgrade pip

# copy python packages list to container and install
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# create folder where API root path will be attached to during RUN
RUN mkdir external_lib
