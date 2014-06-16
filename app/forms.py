# -*- coding: utf-8 -*-

__author__ = 'ilya-il'

from app.db import get_hosts, get_applications, get_facility
from flask_wtf import Form
from wtforms import validators, SelectMultipleField, DateTimeField, RadioField, SelectField, StringField, HiddenField
from config import MSG_PRIORITY_LIST, DATETIME_FORMAT

priority_list = [(i, MSG_PRIORITY_LIST[i]) for i in range(len(MSG_PRIORITY_LIST))]
ie_list = [(0, 'Include'), (1, 'Exclude')]
sort_list = [(1, 'ASC'), (-1, 'DESC')]


class RequestForm(Form):
    # HOST
    host_ie = RadioField('HostIE', choices=ie_list, default=0, coerce=int)
    host = SelectMultipleField('Host')
    # PROGRAM
    application_ie = RadioField('ApplicationIE', choices=ie_list, default=0, coerce=int)
    application = SelectMultipleField('Application')
    # FACILITY
    facility_ie = RadioField('FacilityIE', choices=ie_list, default=0, coerce=int)
    facility = SelectMultipleField('Facility')
    # PRIORITY
    priority_ie = RadioField('PriorityIE', choices=ie_list, default=0, coerce=int)
    priority = SelectMultipleField('Priority', choices=priority_list, coerce=int)
    # DATETIME (%Y-%m-%d %H:%M:%S)
    date_from = DateTimeField('From', [validators.optional()], format=DATETIME_FORMAT)
    date_to = DateTimeField('To', [validators.optional()], format=DATETIME_FORMAT)

    # RECORDS PER PAGE
    records_per_page = SelectField('Records p/p',
                                   choices=[(i, i) for i in (10, 25, 50, 100, 500)],
                                   coerce=int,
                                   default=25)
    # SORT DIRECTION - index - MongoDB sort style
    sort_direction = SelectField('Sort', choices=sort_list, coerce=int, default=-1)

    # SEARCH STRING (regexp)
    search_str = StringField('Search')

    # PAGE NUMBER
    # hidden field has coerce=string - this cannot be changed
    # use int() in views to work with
    current_page = HiddenField('CurrentPage', default=1)

    # select fields with dynamic lists
    @classmethod
    def new(cls):
        form = cls()
        form.host.choices = sorted([(j, j) for j in get_hosts()])
        form.application.choices = sorted([(j, j) for j in get_applications()])
        form.facility.choices = sorted([(j, j) for j in get_facility()])
        return form

