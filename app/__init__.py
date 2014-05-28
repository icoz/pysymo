#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'ilya-il'

from flask import Flask
import logging
from logging.handlers import RotatingFileHandler


app = Flask(__name__)
app.config.from_object('config')

# add chart support
app.jinja_env.add_extension("chartkick.ext.charts")

# add logging
# parent log level
app.logger.setLevel(logging.INFO)
formatter = logging.Formatter(u'%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s')
file_handler = RotatingFileHandler(app.config['PYSYMO_LOG'], maxBytes=1024 * 1024 * 10, backupCount=20)
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)
app.logger.addHandler(file_handler)

from app import auth, db, debug, views, forms
