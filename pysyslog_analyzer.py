# -*- coding: utf-8 -*-
from datetime import datetime
from random import random

from flask import Flask, request

from db import db


app = Flask(__name__)


def date_convert(d):
    if type(d) is datetime:
        return 'd{}_{}_{}'.format(d.year, d.month, d.day)
    else:
        return None


def random_record():
    server = 'serv {0}'.format(int(random() * 5))
    # print(server)
    apps = ['samba', 'exim', 'postfix', 'httpd', 'ftpd']
    app = apps[int(random() * 5)]
    # print(app)
    """ level:
    1 - debug
    2 - info
    3 - warning
    4 - error
    5 - critical
    """
    level = int(random() * 5)
    # print(level)
    time = str(datetime.today().time())
    words = ['hello', 'world', 'how', 'are', 'you']
    message = ' '.join([words[int(random() * 5)] for i in range(3)])
    return server, app, level, time, message


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/gen_info')
def gen_info():
    # print(type(datetime.today()))
    d = date_convert(datetime.today())
    # out = d
    # print(d)
    s, a, l, t, m = random_record()
    print(s, a, l, t, m)
    # db.test.insert({'some': 12})
    # db['d12_12_12'].insert({'cool':1})
    try:
        if db.dates.find_one({'date': str(datetime.today().date()), 'servers': s}) is None:
            db.dates.update({'date': str(datetime.today().date()), 'coll_name': d}, {'$push': {'servers': s}},
                            upsert=True)
    except Exception as e:
        print('except', str(e))
    db[d].insert({'server': s, 'app': a, 'level': l, 'time': t, 'message': m})
    return 'Done\n'


@app.route('/servers/', methods=['GET', 'POST'])
def servers():
    print('servers')
    if request.method == 'GET':
        # collections = db.dates.find({}, {'coll_name': 1})
        print('get')
        info = db['dates'].aggregate({'$group': {"_id": 'servers', 'servers': {'$addToSet': '$servers'}}})
        if info['ok']:
            out = ""
            servers = info['result'][0]['servers'][0]
            print(servers)
            for s in servers:
                out += str(s) + "\n"
        else:
            print('not found')
            out = 'not found'
        return out
    else:
        date_from = request.json['date_from']
        date_to = request.json['date_to']
        collections = db.dates.find({'date': {'$ge': date_from, '$le': date_to}}, {'coll_name': 1})
    for c in collections:
        cn = c['coll_name']
        print(cn)
        map = ''
        red = ''
        db[cn].map_reduce(map=map, reduce=red)
        db[cn].find({})


if __name__ == '__main__':
    app.run()
