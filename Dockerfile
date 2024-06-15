FROM python:3.11-slim

WORKDIR /opt/whispers

ADD . .

RUN pip3 install -e .

RUN whispers --help

ENTRYPOINT [ "whispers" ]
