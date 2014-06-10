# -*- coding: utf-8 -*-

__author__ = 'icoz'

import time

from app import app
from app.forms import RequestForm
from app.db import db, get_charts_list, get_chart_data
from app.auth import login_required
from flask_paginate import Pagination

from flask import request, render_template, session

@app.route('/')
def home():
    print(session)
    return render_template('home.html')


# route for charts
# /charts - charts list
# /charts?chart=<chart_name> - show specified chart
@app.route('/charts', methods=['GET'])
@login_required
def charts():
    chart_name = request.args.get('chart')
    if chart_name:
        chart_data = get_chart_data(chart_name)
    else:
        chart_data = None
    charts_list = get_charts_list()
    return render_template('charts.html', charts_list=charts_list, chart_data=chart_data)


# test get info on flask-wtf forms
@app.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    data = None

    form = RequestForm.new()
    if form.validate_on_submit():
        stat = dict()
        req = dict()

        # HOST
        if form.host.data:
            if form.host_ie.data == 0:
                req['h'] = {'$in': form.host.data}
            else:
                req['h'] = {'$nin': form.host.data}

        # APPLICATION
        if form.application.data:
            if form.application_ie.data == 0:
                req['a'] = {'$in': form.application.data}
            else:
                req['a'] = {'$nin': form.application.data}

        # FACILITY
        if form.facility.data:
            if form.facility_ie.data == 0:
                req['f'] = {'$in': form.facility.data}
            else:
                req['f'] = {'$nin': form.facility.data}

        # PRIORITY
        if form.priority.data:
            if form.priority_ie.data == 0:
                req['p'] = {'$in': [i for i in form.priority.data]}
            else:
                req['p'] = {'$nin': [i for i in form.priority.data]}

        # DATEFROM
        if form.date_from.data:
            req['d'] = {'$gte': form.date_from.data}

        # DATETO
        if form.date_to.data:
            if 'd' in req:
                req['d']['$lte'] = form.date_to.data
            else:
                req['d'] = {'$lte': form.date_to.data}

        # RECORD PER PAGE - in find()

        # SORT - in find()

        # SEARCH STR
        if form.search_str.data:
            req['m'] = {'$regex': form.search_str.data}

        print('db-request', req)

        # pagination skip records
        skip_records = (int(form.current_page.data) - 1)*form.records_per_page.data

        # statistics
        begin = time.time()
        total_records = db.messages.find(req).count()

        info = db.messages.find(spec=req,
                                skip=skip_records,
                                limit=form.records_per_page.data,
                                sort=[('d', form.sort_direction.data)])

        data = [i for i in info]

        end = time.time()

        stat['total_records'] = total_records
        stat['time_elapsed'] = end-begin

        pagination = Pagination(page=int(form.current_page.data),
                                per_page=form.records_per_page.data,
                                total=total_records,
                                bs_version=3,
                                href='javascript:change_page({0})')
    else:
        stat = None
        pagination = None

    return render_template('search.html',
                           form=form,
                           data=data,
                           stat=stat,
                           pagination=pagination)


@app.errorhandler(500)
def internal_error(exception):
    app.logger.error('EXCEPTION!')
    return render_template('500.html')
