FROM ubuntu:20.04

RUN apt-get update && \
    apt-get install -y sudo \
    build-essential \
    curl \
    libcurl4-openssl-dev \
    libssl-dev \
    wget \
    python3-dev \
    python3-pip \
    libxrender-dev \
    libxext6 \
    libsm6 \
    openssl

RUN mkdir -p /opt/service
COPY requirements.txt /opt/service

RUN pip3 install --upgrade pip
RUN pip3 install -r /opt/service/requirements.txt


COPY langdata/torch/ /root/.cache/torch/
COPY docker/entry-point-cli.sh /opt/service/entry-point-cli.sh
COPY summarizer /opt/service/summarizer
COPY *.py /opt/service/

COPY tests /opt/service/tests
COPY evaluation /opt/service/evaluation


WORKDIR  /opt/service
ENTRYPOINT /opt/service/entry-point-cli.sh
