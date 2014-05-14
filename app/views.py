__author__ = 'icoz'

from app import app
from app.db import db, get_apps, get_hosts
from app.auth import login_required

from flask import request, render_template, session


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
    # app = None
    # host = None
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
        if prio != '':
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


@app.route('/json/servers/', methods=['GET', 'POST'])
def json_servers():
    if request.method == 'GET':
        return str(get_hosts())
        # info = db.messages.aggregate({'$distinct': {'d': 0}})
        # info = db['dates'].aggregate({'$match': {'d': {'$and': [{'$gte':1}, {'$lte': 1}]}}},
        #                              {'$group': {"_id": 'servers', 'servers': {'$addToSet': '$servers'}}})
    else:
        return str([])
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
        return str([])