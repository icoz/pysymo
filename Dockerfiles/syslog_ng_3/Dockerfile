FROM ubuntu
MAINTAINER icoz

RUN apt-get update && apt-get install -y syslog-ng-core syslog-ng-mod-mongodb && apt-get clean


ADD ./syslog_docker.conf /etc/syslog.conf
RUN sed 's/module(load="imklog")/#module(load="imklog")/' -i /etc/rsyslog.conf
RUN sed 's/#$ModLoad imudp/$ModLoad imudp/' -i /etc/rsyslog.conf
RUN sed 's/#$UDPServerRun 514/$UDPServerRun 514/' -i /etc/rsyslog.conf


CMD [ "/usr/sbin/syslog-ng",  "-f", "/etc/syslog.conf" ]

