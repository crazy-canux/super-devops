FROM ubuntu:16.04

RUN apt-get update && apt-get install -y python3.5 python3-pip libffi-dev libssl-dev && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /opt/super-devops

COPY . /opt/super-devops

RUN ls -l /opt/super-devops

WORKDIR /opt/super-devops

RUN pip3 install -r requirements.txt

RUN python3 setup.py install

