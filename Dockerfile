# File for building Model and API environment inside a container
# The Python environment will be based off the requirements.txt that can be found in the same folder
# BUILD: docker build -t model_api:latest . 
# RUN: docker run -it -v /path/to/model_api/:/external_lib/ -p 5000:5000 -p 5432:5432 --network="host" model_api sh -c 'cd external_lib && make api-start'
# 
FROM ubuntu:xenial

# argument passed when RUN is called to append the host directory inside the container
ARG external_lib_path

# update environment packages
RUN apt-get update && apt-get upgrade -y
RUN apt-get install software-properties-common -y 

# install pip
RUN apt-get install -y python3-pip
RUN pip3 install --upgrade pip

# copy python packages list to container and install
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# create folder where project folder will be attached to during RUN
RUN mkdir external_lib