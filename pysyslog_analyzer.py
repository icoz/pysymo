#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'icoz'

from datetime import datetime, timedelta
from functools import wraps
from random import random

from flask import Flask, request, render_template, flash, session, redirect, url_for

from db import db


DEBUG = True
SECRET_KEY = 'sifdj ncs dcq odicn pdscn[os ncpasvaidcjn sajc acbqisbc csbabcdsac valsdcb alsjd bafd ba'

app = Flask(__name__)
app.config.from_object(__name__)


def login_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if session.get('logged_in'):
            return func(*args, **kwargs)
        else:
            print('url=', request.url)
            session['next'] = request.url
            return redirect(url_for('login'), code=302)

    return decorated_view


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == 'GET':
        session['next'] = None
        return render_template('login.html')
    if request.method == 'POST':
        r = db['users'].find_one({'user': request.form['username']})
        # user, passwd = ("user", "pass")
        print(r)
        print()
        if r is None:
            flash('Invalid username')
        elif request.form['password'] != r['password']:
            flash('Invalid password')
        else:
            print('login ok, setting session')
            session['logged_in'] = True
            print('process 1', session)
            session['username'] = request.form['username']
            print('process 2', session)
            # TODO store user_id
            session['user_id'] = str(r['_id'])
            print('before flash')
            flash("Logged in successfully.")
            print('after flash')
            if session.get('next'):
                url = session['next']
                session['next'] = None
                return redirect(url)
            else:
                return redirect(url_for('home'))
                # return redirect(request.args.get("next") or url_for("home"))
    return redirect(url_for('home'))


@app.route('/logout')
@login_required
def logout():
    session.clear()
    return redirect(url_for('home'))


@app.route('/register', methods=['GET', "POST"])
def register():
    if request.method == "GET":
        return render_template('register.html')
    if request.method == 'POST':
        user = request.form['username']
        password = request.form['password']
        mail = request.form['email']
        dbu = db['users']
        # TODO: check on exists
        rec = dbu.find_one({"user": user})
        if rec is None:
            # TODO: make it safe to save to mongodb
            dbu.insert({'user': user, 'password': password, 'mail': mail})
            flash('Registered. Sending to login page.')
            session['next'] = None
            return redirect(url_for('login'))
        else:
            flash('Error! Login is not unique!')
    pass


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


@app.route('/')
def home():
    print(session)
    return render_template('home.html')


@app.route('/get_info', methods=['GET', 'POST'])
@login_required
def get_info():
    hosts = get_hosts()
    apps = get_apps()
    data = None
    app = None
    host = None
    act = dict()
    if request.method == 'GET':
        print('get-info: get')
    else:
        if request.args.get('skip'):
            sk = request.args.get('skip')
        else:
            sk = 0
        print('get-info: post', request.form)
        host = request.form.get('host')
        app = request.form.get('app')
        prio = request.form.get('prio')
        regex = request.form.get('msg_regex')
        req = dict()
        if host:
            act['host'] = host
            req['h'] = host
        if app:
            act['app'] = app
            req['a'] = app
        if prio is not None:
            prio = int(prio)
            act['prio'] = prio
            req['p'] = prio
        if regex:
            act['regex'] = regex
            req['m'] = {'$regex': regex}
        print(req)
        # if regex:
        #     info = db.messages.find({'h': host, 'a': app, 'm':{'$regex': regex}}).limit(100+sk).skip(sk)
        # else:
        #     info = db.messages.find({'h': host, 'a': app}).limit(100+sk).skip(sk)
        info = db.messages.find(req).limit(100 + sk).skip(sk)
        data = [i for i in info]
    return render_template('request_form.html', hosts=hosts, apps=apps, data=data, active=act)


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


@app.route('/date/', methods=['GET', 'POST'])
def test_date():
    if request.method == 'GET':
        info = db.messages.find({'d': {'$gte': datetime(2014, 5, 11, 10, 38, 10)}})
        # info = db['dates'].aggregate({'$match': {'d': 0}})
        # info = db['dates'].aggregate({'$match': {'d': {'$and': [{'$gte':1}, {'$lte': 1}]}}},
        #                              {'$group': {"_id": 'servers', 'servers': {'$addToSet': '$servers'}}})
        print(info.count())
        ii = []
        for i in info:
            # print(i)
            ii.append(str(i) + '<br>')
        # if info['ok']:
        #     out = ""
        #     servers = info['result']
        #     print(servers)
        #     for s in servers:
        #         out += str(s) + "\n"
        # else:
        #     print('not found')
        #     out = 'not found'
        return str(ii)
    else:
        date_from = request.json['date_from']
        date_to = request.json['date_to']
        collections = db.dates.find({'date': {'$ge': date_from, '$le': date_to}}, {'coll_name': 1})
        return 'post'
    return 'error'


def get_hosts():
    return db.messages.distinct('h')


def get_apps():
    return db.messages.distinct('a')


@app.route('/json/servers/', methods=['GET', 'POST'])
def json_servers():
    if request.method == 'GET':
        return str(get_hosts())
        # info = db.messages.aggregate({'$distinct': {'d': 0}})
        # info = db['dates'].aggregate({'$match': {'d': {'$and': [{'$gte':1}, {'$lte': 1}]}}},
        #                              {'$group': {"_id": 'servers', 'servers': {'$addToSet': '$servers'}}})
    else:
        return (str([]))
        # date_from = request.json['date_from']
        # date_to = request.json['date_to']
        # collections = db.dates.find({'date': {'$ge': date_from, '$le': date_to}}, {'coll_name': 1})


@app.route('/json/apps/', methods=['GET', 'POST'])
def json_apps():
    if request.method == 'GET':
        return str(get_apps())
        # info = db.messages.aggregate({'$distinct': {'d': 0}})
        # info = db['dates'].aggregate({'$match': {'d': {'$and': [{'$gte':1}, {'$lte': 1}]}}},
        #                              {'$group': {"_id": 'servers', 'servers': {'$addToSet': '$servers'}}})
    else:
        return (str([]))


if __name__ == '__main__':
    app.run()
