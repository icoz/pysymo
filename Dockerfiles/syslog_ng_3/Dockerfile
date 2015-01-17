FROM ubuntu
MAINTAINER icoz

RUN apt-get update && apt-get install -y syslog-ng-core syslog-ng-mod-mongodb && apt-get clean


ADD ./syslog_docker_test.conf /etc/syslog.conf

CMD [ "/usr/sbin/syslog-ng",  "-f", "/etc/syslog.conf", "--no-caps", "-e", "-F" ]

