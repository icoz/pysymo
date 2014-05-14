#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ilya-il'

from flask import Flask

app = Flask(__name__)
app.config.from_object('config')

from app import auth, db, debug, views
