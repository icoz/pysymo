# -*- coding: utf-8 -*-

__author__ = 'ilya-il'

import sys
import os

# WTF forms
CSRF_ENABLED = True
SECRET_KEY = 'sifdjncs-dcqodicnpdscn[osncpas#vaidcjnsajcacbqisbccsbab-cdsacvalsdcb!alsjdbafdba'

# priority list
# WARNING! do not change item position in list
MSG_PRIORITY_LIST = ('emerg', 'alert', 'crit', 'err', 'warn', 'notice', 'info', 'debug')

# datetime format for search form
DATETIME_FORMAT = '%d.%m.%Y %H:%M:%S'

# log file
basedir = os.path.abspath(os.path.dirname(__file__))
if sys.platform == 'win32':
    PYSYMO_LOG = os.path.join(basedir, 'python.log')
else:
    PYSYMO_LOG = '/var/log/pysymo/python.log'
