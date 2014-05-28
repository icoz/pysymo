#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = 'icoz'

from datetime import datetime, time
from random import random
import sys

from pymongo import MongoClient

MONGO_HOST = '127.0.0.1'
MONGO_PORT = 27017
MONGO_DATABASE = 'syslog'


def random_record():
    host = 'serv {0}'.format(int(random() * 5))
    facilities = ['kern', 'auth', 'cron', 'daemon', 'user', 'mail']
    facility = facilities[int(random() * len(facilities))]
    priority = int(random() * 7)
    apps = ['samba', 'exim', 'postfix', 'httpd', 'ftpd']
    app = apps[int(random() * len(apps))]
    dt = datetime.utcnow()
    words = ['hello', 'world', 'how', 'are', 'you']
    message = ' '.join([words[int(random() * len(words))] for i in range(5)])
    # h = host
    # f = facility(???)
    # p = priority(0 - 7)
    # dt = date-time.timestamp
    # a = app | program
    # m = msg
    return host, facility, priority, app, dt, message


def save_to_db(db, data):
    # just save data
    db['messages'].insert(data)
    # update hourly stat
    d = datetime.combine(data['d'].date(), time.min)
    hour = data['d'].hour
    minute = data['d'].minute
    query = {
        'metadata': {'d': d, 'h': data['h'], 'a': data['a']}}
    update = {'$inc': {
        'total': 1,
        'hourly.%d' % (hour,): 1,
        'minute.%d.%d' % (hour, minute): 1}}
    db.stats.daily.update(query, update, upsert=True)
    #update monthly stat
    day_of_month = data['d'].day
    query = {
        'metadata': {
            'date': d.replace(day=1),
            'h': data['h'],
            'a': data['a']}}
    update = {'$inc': {
        'total': 1,
        'daily.%d' % day_of_month: 1}}
    db.stats.monthly.update(query, update, upsert=True)


def pre_allocate_in_db(db):
    pass
    # if db.stat.findOne():
    #     return


def main():
    if len(sys.argv) != 2:
        print('usage: ', sys.argv[0], ' count_of_records')
        exit(0)
    db = MongoClient(host=MONGO_HOST, port=MONGO_PORT)[MONGO_DATABASE]
    start = datetime.utcnow()
    print('Start writing 1e5: ', start)
    for i in range(int(sys.argv[1])):
        h, f, p, a, d, m = random_record()
        data = {'h': h, 'f': f, 'p': p, 'a': a, 'd': d, 'm': m}
        save_to_db(db, data)
    stop = datetime.utcnow()
    print('Stop writing 1e5: ', stop)
    print('It took ', (stop - start).seconds, 's ', (stop - start).microseconds, 'microsec')


if __name__ == '__main__':
    main()