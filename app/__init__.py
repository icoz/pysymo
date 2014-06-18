#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'ilya-il'

from flask import Flask, Blueprint
from flask_login import LoginManager
import chartkick
import logging
from logging.handlers import RotatingFileHandler

app = Flask(__name__)
app.config.from_object('config')

# Blueprint magic
ck = Blueprint('ck', __name__, static_folder=chartkick.js(), static_url_path='/ck/static')
app.register_blueprint(ck)

# add chart support
app.jinja_env.add_extension("chartkick.ext.charts")

# add login support
login_manager = LoginManager()
login_manager.init_app(app)
# TODO login view - https://flask-login.readthedocs.org/en/latest/#flask.ext.login.LoginManager.login_view
#login_manager.login_view = 'login'

# add logging
# parent log level
app.logger.setLevel(logging.INFO)
formatter = logging.Formatter(u'%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s')
file_handler = RotatingFileHandler(app.config['PYSYMO_LOG'], maxBytes=1024 * 1024 * 10, backupCount=20)
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)
app.logger.addHandler(file_handler)

from app import auth, db, views, forms
