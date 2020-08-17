# File for building Model and API environment inside a container
# The Python environment will be based off the requirements.txt that can be found in the same folder
# BUILD: docker build -t model_api:latest . 
# RUN: docker run -it -v /path/to/model_api/:/external_lib/ -p 5000:5000 -p 5432:5432 --network="host" brain_api sh -c 'cd external_lib && make api-start'

FROM python:3.7.6-alpine

ARG external_lib_path

RUN apk add --no-cache cmake gcc libxml2 \
       automake g++ subversion python3-dev \
       libxml2-dev libxslt-dev lapack-dev gfortran \
       postgresql-dev musl-dev freetype-dev \
       libpng-dev libffi-dev make

RUN python -m pip install --upgrade pip

# copy python packages to container
COPY ./requirements.txt .

RUN pip install -r requirements.txt

RUN mkdir external_lib