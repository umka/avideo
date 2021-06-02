
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.6-alpine3.8

WORKDIR /opt/app

# Install application dependencies
RUN echo "http://mirror.leaseweb.com/alpine/edge/community" >> /etc/apk/repositories
RUN echo "http://dl-cdn.alpinelinux.org/alpine/edge/community" >> /etc/apk/repositories
RUN apk add --virtual .build-deps \
        --repository http://dl-cdn.alpinelinux.org/alpine/edge/community \
        --repository http://dl-cdn.alpinelinux.org/alpine/edge/main \
        gcc libc-dev geos-dev geos libffi-dev git openssl-dev libcap && \
    runDeps="$(scanelf --needed --nobanner --recursive /usr/local \
    | awk '{ gsub(/,/, "\nso:", $2); print "so:" $2 }' \
    | xargs -r apk info --installed \
    | sort -u)" && \
    apk add --virtual .rundeps $runDeps

# Install Python dependencies
COPY requirements.txt /opt/app/requirements.txt
RUN pip install -U pip && pip install -r requirements.txt

# Copy application files
COPY server /opt/app/server

# Allow image to use reserved ports
RUN setcap 'cap_net_bind_service=+ep' /opt/app/server/app.py

# Set deployment parameters
WORKDIR /opt/app/server
ENV PYTHONPATH /opt/app

ENTRYPOINT python3 app.py
