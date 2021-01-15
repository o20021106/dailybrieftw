FROM ubuntu:18.04
RUN apt-get update \
  && apt install software-properties-common \
  && add-apt-repository --yes ppa:deadsnakes/ppa \
  && apt install python3.7 \
  && apt-get install -y python3-pip python3-dev \
  && cd /usr/local/bin \
  && ln -s /usr/bin/python3 python \
  && pip3 install --upgrade pip

COPY . /app
WORKDIR /app
RUN python3.7 -m pip install --upgrade pip
RUN python3.7 -m pip install -r requirements.txt
RUN python3.7 -m pip install .
WORKDIR /app/server
ENV DB_USER=DB_USER_PLACEHOLDER,DB_PWD=DB_PWD_PLACEHOLDER,DB_NAME=DB_NAME_PLACEHOLDER
CMD python3.7 app.py