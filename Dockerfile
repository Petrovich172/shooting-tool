FROM golang:latest as pandora
RUN git clone https://github.com/yandex/pandora.git \
 && cd pandora \
 && make deps \
 && go install \
 && go build main.go
RUN echo "pandora ls" \
 && ls \
 && cd pandora \
 && ls

FROM ubuntu:latest

MAINTAINER pete172194177@gmail.com

COPY --from=pandora ./go/pandora .
COPY ./requirements/ /requirements
COPY ./start.sh /start.sh
COPY ./load.yaml /load.yaml
COPY ./pandora_config.yaml /pandora_config.yaml
COPY ./token.txt /token.txt
COPY ./flow/ /flow
WORKDIR /.

RUN apt-get update \
 && apt-get install -y software-properties-common \
 && add-apt-repository ppa:yandex-load/main \
 && apt-get update \
 && apt-get install -y python-pip \
 && apt-get install -y wget \
 && wget https://bootstrap.pypa.io/get-pip.py \
 && python get-pip.py \
 && pip install --upgrade pip \
 && pip install -U pip \
 && python -m pip install --upgrade six \
 && pip install redis \
 && apt install -y libpq-dev python-dev \
# && apt-get install -y build-dep python-psycopg2 \
 && pip install psycopg2 \
 && pip install -r /requirements/production.txt \
 && pip install https://api.github.com/repos/yandex/yandex-tank/tarball/master \
 && apt-get install -y git \
 && apt-get update \
 && apt-get -y install tesseract-ocr \
 && apt-get -y install nano \
 && apt-get clean \
 && apt-get install build-essential


RUN sed -i 's/\r//' /start.sh \
 && chmod +x /start.sh \
 && rm -rf /var/lib/apt/lists/*

CMD ["/start.sh"]