FROM ubuntu:18.04
RUN apt-get update \
  && apt-get install -y python3-pip python3-dev \
  && cd /usr/local/bin \
  && ln -s /usr/bin/python3 python \
  && pip3 install --upgrade pip

COPY . /app
WORKDIR /app
RUN pip3 install -r requirements.txt
WORKDIR /app/server
ENV DB_USER=DB_USER_PLACEHOLDER,DB_PWD=DB_PWD_PLACEHOLDER,DB_NAME=DB_NAME_PLACEHOLDER
CMD python3 app.py