#!/usr/bin/python
# -*- coding: utf-8 -*-

""" Config file ONLY for tools scripts."""


__author__ = 'ilya-il'

from os import environ as env
import os
import sys

MONGO_HOST = env.get('PYSYMO_MONGO_HOST') or env.get('DB_PORT_27017_TCP_ADDR') or '127.0.0.1'
MONGO_PORT = env.get('PYSYMO_MONGO_PORT') or env.get('DB_PORT_27017_TCP_PORT') or 27017
MONGO_DATABASE = env.get('PYSYMO_MONGO_DATABASE') or 'syslog'

# log file
if sys.platform == 'win32':
    basedir = os.path.abspath(os.path.dirname(__file__))
    PIPER_ERROR_LOG = os.path.join(basedir, 'piper_error.log')
else:
    PIPER_ERROR_LOG = os.environ.get('PIPER_ERROR_LOG') or '/var/log/pysymo/piper_error.log'


# priority list
# WARNING! do not change item position in list
MSG_PRIORITY_LIST = ('emerg', 'alert', 'crit', 'err', 'warn', 'notice', 'info', 'debug')

