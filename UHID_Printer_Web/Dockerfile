# Build stage
FROM python:3.11-alpine as builder


WORKDIR /uhid_label_printer

COPY ./requirements.txt /uhid_label_printer/requirements.txt

RUN apk update \
    && apk upgrade \
    && apk add --no-cache  build-base linux-headers \
    && python3 -m venv /py \
    && /py/bin/pip install --upgrade pip \
    && /py/bin/pip install --no-cache --no-cache-dir -r /uhid_label_printer/requirements.txt  \
    && apk del  build-base linux-headers \
    && rm -rf /var/cache/apk/* 



# Runtime stage
FROM python:3.11-alpine

WORKDIR /uhid_label_printer

COPY --from=builder /py /py

COPY . /uhid_label_printer

LABEL maintainer='ahmed'

ENV PYTHONUNBUFFERED 1

RUN apk update && apk add --no-cache \
    curl unzip libaio gcompat \
    && mkdir -p /cx_oracle \
    && cd /cx_oracle \
    && curl -o instantclient-basiclite-linux.x64-21.9.0.0.0dbru.zip https://download.oracle.com/otn_software/linux/instantclient/219000/instantclient-basiclite-linux.x64-21.9.0.0.0dbru.zip \
    && unzip -d . instantclient-basiclite-linux.x64-21.9.0.0.0dbru.zip \
    && rm -f instantclient-basiclite-linux.x64-21.9.0.0.0dbru.zip \
    && ln -snf /usr/share/zoneinfo/Asia/Kolkata /etc/localtime && echo "Asia/Kolkata" > /etc/timezone \
    && mkdir /var/log/uwsgi \
    && touch /var/log/uwsgi/uhid_label_printer.log \
    && apk del curl unzip \
    && rm -rf /var/cache/apk/* \
    && apk fix --no-cache \
    && rm -rf /var/lib/apk/lists/*

ENV LD_LIBRARY_PATH=/cx_oracle/instantclient_21_9



ENV PATH="/cx_oracle/instantclient_21_9:/uhid_label_printer/scripts:/py/bin:$PATH"


CMD ["./scripts/py_run.sh"]
