#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Fill database script.

Fill database with number of random records.

"""

from pymongo import MongoClient
from config import MONGO_HOST, MONGO_PORT, MONGO_DATABASE
from datetime import datetime, timedelta
from random import random, randrange
import argparse
import sys

__author__ = 'ilya-il'

def random_record():
    """Generate random record."""
    host = 'serv {0}'.format(int(random() * 20))
    facilities = ['kern', 'auth', 'cron', 'daemon', 'user', 'mail', 'local0', 'local1',
                  'local2', 'local3', 'local4', 'local5', 'local6', 'local7', ]
    facility = facilities[int(random() * len(facilities))]
    priority = int(random() * 7)
    apps = ['samba', 'exim', 'postfix', 'httpd', 'vsftpd', 'kernel', 'smbd', 'sshd', 'xinetd', 'auditd', 'logger']
    app = apps[int(random() * len(apps))]

    # month range in seconds
    dt = datetime.utcnow() - timedelta(seconds=randrange(0, 2592000))

    words = ['hello', 'world', 'how', 'are', 'you']
    message = ' '.join([words[int(random() * len(words))] for i in range(5)])

    return host, facility, priority, app, dt, message


def fill_db(count):
    """Fill database with [count] of random records."""
    if sys.version_info >= (3, 0):
        r = range(count)
    else:
        r = range(count)

    db = MongoClient(host=MONGO_HOST, port=int(MONGO_PORT))[MONGO_DATABASE]
    start_time = datetime.now()

    for i in r:
        h, f, p, a, d, m = random_record()
        db['messages'].insert({'h': h, 'f': f, 'p': p, 'a': a, 'd': d, 'm': m})

    end_time = datetime.now()

    print('Time elapsed  - {time}'.format(time=end_time-start_time))


def main():
    parser = argparse.ArgumentParser(description='Fill database with random records.')
    parser.add_argument('count', type=int, help='Records count')

    args = parser.parse_args()

    if args.count:
        fill_db(args.count)


if __name__ == '__main__':
    main()