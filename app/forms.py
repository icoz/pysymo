# -*- coding: utf-8 -*-
__author__ = 'ilya-il'
from app.db import get_hosts
from flask_wtf import Form
from wtforms import SelectMultipleField, DateTimeField, validators, RadioField
from config import MSG_PRIORITY_LIST

host_list = [(i, i) for i in get_hosts()]
# use str() because int value doesn't submit form
prio_list = [(str(i), MSG_PRIORITY_LIST[i]) for i in xrange(len(MSG_PRIORITY_LIST))]


class RequestForm(Form):
    hostie = RadioField('HostIE', choices=[('0', 'Include'), ('1', 'Exclude')], default='0')
    host = SelectMultipleField('Host', choices=host_list)
    prio = SelectMultipleField('Priority', choices=prio_list)
    datef = DateTimeField('Datetime from<br>%Y-%m-%d %H:%M:%S', [validators.optional()])