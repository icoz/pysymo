#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ilya-il'

from flask import Flask

app = Flask(__name__)
app.config.from_object('config')
# add chart support
app.jinja_env.add_extension("chartkick.ext.charts")

from app import auth, db, debug, views, forms
