#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'ilya-il'

from flask import Flask
from flask_login import LoginManager
from flask.ext.babel import Babel
from flask_wtf.csrf import CsrfProtect
import logging
from logging.handlers import RotatingFileHandler

app = Flask(__name__)
app.config.from_object('config')

# extended CSRF protection for JS
csrf = CsrfProtect()
csrf.init_app(app)

# add login support
login_manager = LoginManager()
login_manager.init_app(app)

# L10n
babel = Babel(app)

# add logging
formatter = logging.Formatter('''--------------------------------------------------
Message type:       %(levelname)s
Location:           %(pathname)s:%(lineno)d
Module:             %(module)s
Function:           %(funcName)s
Time:               %(asctime)s

Message:

%(message)s
''')
file_handler = RotatingFileHandler(app.config['PYSYMO_LOG'], maxBytes=1024 * 1024 * 10, backupCount=20)
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)
app.logger.setLevel(logging.INFO)
app.logger.addHandler(file_handler)

from app import auth, db, views, forms
