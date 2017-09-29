# -*- coding: utf-8 -*-

import sys
import os

__author__ = 'ilya-il'

# ==================================================
#       PROGRAM CONFIG SECTION. DO NOT EDIT!
# ==================================================

# WTF forms
CSRF_ENABLED = True
SECRET_KEY = 'sifdjncs-dcqodicnpdscn[osncpas#vaidcjnsajcacbqisbccsbab-cdsacvalsdcb!alsjdbafdba'

# priority list
# WARNING! do not change item position in list
# and do not change list type 'list' :)
MSG_PRIORITY_LIST = ['emerg', 'alert', 'crit', 'err', 'warn', 'notice', 'info', 'debug']

# datetime format for search form
DATETIME_FORMAT = '%d.%m.%Y %H:%M:%S'

# pysymo version
PYSYMO_VERSION = 0.2

# log file
if sys.platform == 'win32':
    basedir = os.path.abspath(os.path.dirname(__file__))
    PYSYMO_LOG = os.path.join(basedir, 'python.log')
else:
    PYSYMO_LOG = os.environ.get('PYSYMO_LOG') or '/var/log/pysymo/python.log'

# L10n
LANGUAGES = {
    'en': 'English',
    'ru': 'Russian'
}

# ==================================================
#               USER EDITABLE SECTION
# ==================================================

# watch mode interval in seconds
WATCH_MODE_REFRESH_INTERVAL = 30

# allow registration (only for plain auth)
REGISTRATION_ENABLED = True

# Auth type - plain, ldap
AUTH_TYPE = 'plain'

# LDAP
LDAP_SERVER = os.environ.get('PYSYMO_LDAP_SERVER') or 'ldap://[ldap_server]'
LDAP_SEARCH_BASE = os.environ.get('PYSYMO_LDAP_BASE') or '[organisation]'
LDAP_SERVICE_USER = os.environ.get('PYSYMO_LDAP_USER') or '[service_user_dn]'
LDAP_SERVICE_PASSWORD = os.environ.get('PYSYMO_LDAP_PASSWORD') or '[password]'

# MEDB - message explanation database
MEDB_ENABLED = True

# Use
USE_FQDN = True
