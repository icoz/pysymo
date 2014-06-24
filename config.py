# -*- coding: utf-8 -*-

__author__ = 'ilya-il'

import sys
import os

# WTF forms
CSRF_ENABLED = True
SECRET_KEY = 'sifdj ncs dcq odicn pdscn[os ncpasvaidcjn sajc acbqisbc csbabcdsac valsdcb alsjd bafd ba'

# priority list
# WARNING! do not change item position in list
MSG_PRIORITY_LIST = ('emerg', 'alert', 'crit', 'err', 'warn', 'notice', 'info', 'debug')

# datetime format for search form
DATETIME_FORMAT = '%d.%m.%Y %H:%M:%S'

# log file
if sys.platform == 'win32':
    basedir = os.path.abspath(os.path.dirname(__file__))
    PYSYMO_LOG = os.path.join(basedir, 'python.log')
else:
    PYSYMO_LOG = '/var/log/pysymo/python.log'
