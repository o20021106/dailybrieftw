FROM ubuntu:18.04
RUN apt-get update \
  && apt install -y software-properties-common \
  && add-apt-repository --yes ppa:deadsnakes/ppa \
  && apt install -y python3.7 \
  && apt install -y python3-pip \
  && apt-get -y install python3.7-dev

COPY . /app
WORKDIR /app
RUN python3.7 -m pip install --upgrade pip
RUN python3.7 -m pip install -r requirements.txt
RUN python3.7 -m pip install .
RUN python3.7 -m pip freeze
WORKDIR /app/server
ENV DB_USER=DB_USER_PLACEHOLDER,DB_PWD=DB_PWD_PLACEHOLDER,DB_NAME=DB_NAME_PLACEHOLDER
CMD python3.7 app.py