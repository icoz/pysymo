FROM python:2.7
MAINTAINER icoz

RUN pip install flask
RUN pip install flask_wtf
RUN pip install flask_babel
RUN pip install flask_login
RUN pip install flask_paginate
RUN pip install pymongo
RUN pip install pycrypto

RUN mkdir -p /data/log
WORKDIR /data
RUN git clone git://github.com/icoz/pysymo.git

WORKDIR /data/pysymo
ENV PYSYMO_LOG=/data/log/pysymo.log 
#ENV PYSYMO_MONGO_HOST=
#ENV PYSYMO_MONGO_PORT=27017
ENV PYSYMO_MONGO_DATABASE=syslog_test
#ENV PYSYMO_PRODUCTION=True
ENV PYSYMO_PRODUCTION=False

CMD python run.py
EXPOSE 5000
