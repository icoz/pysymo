#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'ilya-il'

from app import app
from os import environ as env
if env.get('PYSYMO_PRODUCTION'):
    app.run(host='0.0.0.0', port=80)
else:
    app.run(debug=True, host='0.0.0.0', port=5000)

