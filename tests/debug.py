# -*- coding: utf-8 -*-

__author__ = 'icoz'

from datetime import datetime, timedelta
from random import random


from app import app
from app.db import db
from app.auth import login_required

# if DEBUG:


def date_convert(d):
    if type(d) is datetime:
        return 'd{}_{}_{}'.format(d.year, d.month, d.day)
    else:
        return None


def random_record():
    host = 'serv {0}'.format(int(random() * 5))
    facilities = ['kern', 'auth', 'cron', 'daemon', 'user', 'mail']
    facility = facilities[int(random() * len(facilities))]
    priority = int(random() * 7)
    apps = ['samba', 'exim', 'postfix', 'httpd', 'ftpd']
    ap = apps[int(random() * len(apps))]
    dt = datetime.utcnow()
    words = ['hello', 'world', 'how', 'are', 'you']
    message = ' '.join([words[int(random() * len(words))] for i in range(5)])
    # h = host
    # f = facility(???)
    # p = priority(0 - 7)
    # dt = date-time.timestamp
    # a = app | program
    # m = msg
    return host, facility, priority, ap, dt, message


@app.route('/gen_info/<int:num>')
@login_required
def gen_info(num=1):
    # print(type(datetime.today()))
    while num > 0:
        # d = date_convert(datetime.today())
        # out = d
        # print(d)
        h, f, p, a, d, m = random_record()
        d = d + timedelta(days=int(random() * 10) - 5)
        # print(h, f, p, a, d, m)
        db['messages'].insert({'h': h, 'f': f, 'p': p, 'a': a, 'd': d, 'm': m})
        db['messages'].ensure_index('h')
        db['messages'].ensure_index('p')
        # db['messages'].ensure_index({'p': 1})
        # db['messages'].ensure_index({'a': 1})
        # db['messages'].ensure_index({'d': 1})
        # db['messages'].ensure_index({'m': 0})
        # db.test.insert({'some': 12})
        # db['d12_12_12'].insert({'cool':1})
        # try:
        #     if db.dates.find_one({'date': str(datetime.today().date()), 'servers': s}) is None:
        #         db.dates.update({'date': str(datetime.today().date()), 'coll_name': d}, {'$push': {'servers': s}},
        #                         upsert=True)
        # except Exception as e:
        #     print('except', str(e))
        # db[d].insert({'h': s, 'a': a, 'p': l, 'd': t, 'm': m})
        num -= 1
    return 'Done\n'
