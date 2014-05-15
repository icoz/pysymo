# -*- coding: utf-8 -*-
__author__ = 'ilya-il'
from app.db import get_hosts, get_applications, get_facility
from flask_wtf import Form
from wtforms import validators, SelectMultipleField, DateTimeField, RadioField, SelectField, TextField
from config import MSG_PRIORITY_LIST, DATETIME_FORMAT

host_list = [(i, i) for i in get_hosts()]
application_list = [(i, i) for i in get_applications()]
facility_list = [(i, i) for i in get_facility()]
priority_list = [(i, MSG_PRIORITY_LIST[i]) for i in range(len(MSG_PRIORITY_LIST))]
ie_list = [(0, 'Include'), (1, 'Exclude')]

datetime_mask = '%d.%m.%Y %H:%M:%S'

class RequestForm(Form):
    # HOST
    host_ie = RadioField('HostIE', choices=ie_list, default=0, coerce=int)
    host = SelectMultipleField('Host', choices=host_list)
    # PROGRAM
    application_ie = RadioField('ApplicationIE', choices=ie_list, default=0, coerce=int)
    application = SelectMultipleField('Application', choices=application_list)
    # FACILITY
    facility_ie = RadioField('FacilityIE', choices=ie_list, default=0, coerce=int)
    facility = SelectMultipleField('Facility', choices=facility_list)
    # PRIORITY
    priority_ie = RadioField('PriorityIE', choices=ie_list, default=0, coerce=int)
    priority = SelectMultipleField('Priority', choices=priority_list, coerce=int)

    # DATETIME (%Y-%m-%d %H:%M:%S)
    date_from = DateTimeField('From', [validators.optional()], format=DATETIME_FORMAT)
    date_to = DateTimeField('To', [validators.optional()], format=DATETIME_FORMAT)

    # RECORDS PER PAGE
    records_per_page = SelectField('Records p/p',
                                   choices=[(i, i) for i in (10, 25, 50, 100, 200, 500, 1000)],
                                   coerce=int,
                                   default=25)
    # SORT DIRECTION - index - MongoDB sort style
    sort_direction = SelectField('Sort', choices=[(1, 'ASC'), (-1, 'DESC')], coerce=int, default=-1)

    # SEARCH STRING (regexp)
    search_str = TextField('Search')