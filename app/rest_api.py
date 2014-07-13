# -*- coding: utf-8 -*-
from datetime import datetime

__author__ = 'icoz'

from app import app
from app.db import db

from flask import request, render_template


@app.route('/test')
def rest_test():
    render_template('rest_search.html')

@app.route('/api/v1/get')
def rest_get():
    req = dict()
    # format request
    args = request.args
    records_skip = 0
    records_limit = 0
    # sort_direction = 1
    for arg_name in args:
        # HOST
        if isinstance(args[arg_name], (list, tuple)):
            arg_iter_val = args[arg_name]
        else:
            arg_iter_val = [args[arg_name]]
        if str(arg_name).lower() == 'host_in':
            req['h'] = {'$in': arg_iter_val}
        elif str(arg_name).lower() == 'host_not_in':
            req['h'] = {'$nin': arg_iter_val}
        # APP
        elif str(arg_name).lower() == 'app_in':
            req['a'] = {'$in': arg_iter_val}
        elif str(arg_name).lower() == 'app_not_in':
            req['a'] = {'$nin': arg_iter_val}
        # FACILITY
        elif str(arg_name).lower() == 'facility_in':
            req['f'] = {'$in': arg_iter_val}
        elif str(arg_name).lower() == 'facility_not_in':
            req['f'] = {'$nin': arg_iter_val}
        # PRIORITY
        elif str(arg_name).lower() == 'priority_in':
            req['p'] = {'$in': arg_iter_val}
        elif str(arg_name).lower() == 'priority_not_in':
            req['p'] = {'$nin': arg_iter_val}
        # DATE
        elif str(arg_name).lower() == 'date_from':
            req['d'] = {'$gte': datetime(args[arg_name])}
        elif str(arg_name).lower() == 'date_to':
            req['p'] = {'$lte': datetime(args[arg_name])}
        # MSG REGEX
        elif str(arg_name).lower() == 'msg_regex':
            req['m'] = {'$regex': args[arg_name]}
        elif str(arg_name).lower() == 'limit':
            records_limit = int(args[arg_name])
        elif str(arg_name).lower() == 'offset':
            records_skip = int(args[arg_name])
    print(req)
    if records_limit < records_skip:
        records_limit += records_skip
    # get info
    # TODO: add sorting
    info = db.messages.find(spec=req,
                            skip=records_skip,
                            limit=records_limit)
    # sort=[('d', sort_direction)])
    print(info.count())
    out = str(list(info))
    return out