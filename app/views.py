# -*- coding: utf-8 -*-

import time

from app import app, babel
from app.forms import RequestForm, flash_form_errors
from app.db import db, db_get_charts_list, db_get_chart, db_get_messages_stat, db_get_db_stat
from app.functions import medb_parse_msg

from flask_paginate import Pagination
from flask_login import login_required, current_user
from flask_babel import gettext

from flask import request, render_template, redirect, url_for, flash

__author__ = 'icoz'


@app.route('/')
def home():
    if current_user.is_authenticated:
        return redirect(url_for('search'))
    else:
        return redirect(url_for('login'))


# route for charts
# /charts - charts list
# /charts?chart=<chart_name> - show specified chart
@app.route('/charts', methods=['GET'])
@login_required
def charts():
    chart_name = request.args.get('chart')
    if chart_name:
        chart = db_get_chart(chart_name)
    else:
        chart = None
    charts_list = db_get_charts_list()
    return render_template('charts.html', charts_list=charts_list, chart=chart)


# test get info on flask-wtf forms
@app.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    data = None

    form = RequestForm.new()
    if form.validate_on_submit():
        req = dict()
        req_stat = dict()

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

        # pagination skip records
        skip_records = (int(form.current_page.data) - 1) * form.records_per_page.data

        # statistics
        begin = time.time()
        total_records = db.messages.find(req).count()

        info = db.messages.find(filter=req,
                                skip=skip_records,
                                limit=form.records_per_page.data,
                                sort=[('d', form.sort_direction.data)])

        data = [i for i in info]

        # if MEDB enabled, process messages
        if app.config['MEDB_ENABLED']:
            for i in range(len(data)):
                t = medb_parse_msg(data[i]['m'])
                if t:
                    data[i]['m'] = t + ' ' + data[i]['m']

        end = time.time()

        req_stat['total_records'] = total_records
        req_stat['time_elapsed'] = end - begin

        pagination = Pagination(page=int(form.current_page.data),
                                per_page=form.records_per_page.data,
                                total=total_records,
                                bs_version=3,
                                href='javascript:change_page({0})')
    else:
        req_stat = None
        pagination = None
        flash_form_errors(form)

    return render_template('search.html',
                           form=form,
                           data=data,
                           req_stat=req_stat,
                           pagination=pagination)


@app.route('/stat')
@login_required
def stat():
    return render_template('stat.html',
                           mes_stat=db_get_messages_stat(),
                           db_stat=db_get_db_stat())


@app.route('/about')
@login_required
def about():
    return render_template('about.html')


@babel.localeselector
def get_locale():
    return request.accept_languages.best_match(app.config['LANGUAGES'].keys())


@app.errorhandler(401)
def page_not_found(e):
    flash(gettext('401 - Unauthorized'), 'danger')
    return redirect(url_for('login'))


@app.errorhandler(404)
def page_not_found(e):
    flash(gettext('404 - Page not found'), 'danger')
    return redirect(url_for('home'))


@app.errorhandler(500)
def internal_error(e):
    app.logger.error("""    ErrorHandler 500
    Request:   {method} {path}
    IP:        {ip}
    Agent:     {agent_platform} | {agent_browser} {agent_browser_version}
    Raw Agent: {agent}""".format(
        method=request.method,
        path=request.path,
        ip=request.remote_addr,
        agent_platform=request.user_agent.platform,
        agent_browser=request.user_agent.browser,
        agent_browser_version=request.user_agent.version,
        agent=request.user_agent.string
    ))
    return render_template('500.html'), 500
