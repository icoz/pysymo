#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'icoz'

from flask import Flask, render_template, session, request

from app.db import db


# DEBUG = True
SECRET_KEY = 'sifdj ncs dcq odicn pdscn[os ncpasvaidcjn sajc acbqisbc csbabcdsac valsdcb alsjd bafd ba'

app = Flask(__name__)
app.config.from_object(__name__)

from app.auth import login_required, login, logout, register
from app.useful import get_apps, get_hosts
from app.debug import random_record, gen_info
from app.json import json_apps, json_servers
from app.forms import get_info


@app.route('/')
def home():
    print(session)
    return render_template('home.html')


if __name__ == '__main__':
    app.run()
