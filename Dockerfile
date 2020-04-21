FROM ubuntu:16.04

WORKDIR /opt/super-devops

COPY . /opt/super-devops

RUN set -ex \
    && apt-get update \
    && apt-get install -y python3.5 python3-pip libffi-dev libssl-dev \
    && mkdir -p /opt/super-devops \
    && pip3 install -r requirements.txt
    && python3 setup.py install
    && rm -rf /var/lib/apt/lists/*

