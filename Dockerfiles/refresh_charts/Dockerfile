FROM python:2.7
MAINTAINER icoz

RUN mkdir -p /data/log

RUN groupadd -r swuser -g 1234 && \
useradd -u 1234 -r -g swuser -d /data -s /sbin/nologin -c "Docker image user" swuser && \
chown -R swuser:swuser /data
USER root

RUN apt-get update && apt-get -y install unzip
RUN pip install pymongo
ENV PIPER_ERROR_LOG=/data/log/piper_error.log 

WORKDIR /data
RUN git clone git://github.com/icoz/pysymo.git

WORKDIR /data/pysymo/tools
#ENV PYSYMO_MONGO_HOST=
#ENV PYSYMO_MONGO_PORT=27017
ENV PYSYMO_MONGO_DATABASE=syslog_test

RUN chown -R swuser:swuser /data
USER swuser

CMD python refresh_charts.py
