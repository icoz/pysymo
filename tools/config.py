#!/usr/bin/python
# -*- coding: utf-8 -*-

""" Config file ONLY for tools scripts."""


__author__ = 'ilya-il'

MONGO_HOST = '127.0.0.1'
MONGO_PORT = 27017
MONGO_DATABASE = 'syslog'

PIPER_ERROR_LOG = '/var/log/pysymo/piper_error.log'

# priority list
# WARNING! do not change item position in list
MSG_PRIORITY_LIST = ('emerg', 'alert', 'crit', 'err', 'warn', 'notice', 'info', 'debug')