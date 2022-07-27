FROM python:3.9-slim

RUN apt update \
    && apt install -y make python3-lxml python3-yaml \
    && apt clean

WORKDIR /whispers

COPY dist/*.tar.gz .

RUN pip3 install *.tar.gz \
    && rm -rf *.tar.gz

ENTRYPOINT [ "whispers" ]
