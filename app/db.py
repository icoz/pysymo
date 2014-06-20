# -*- coding: utf-8 -*-

__author__ = 'icoz'

from pymongo import MongoClient

MONGO_HOST = '127.0.0.1'
MONGO_PORT = 27017
MONGO_DATABASE = 'syslog'

db = MongoClient(host=MONGO_HOST, port=MONGO_PORT)[MONGO_DATABASE]


# MESSAGES


def get_hosts():
    return db.cache.find_one({'type': 'h'})['value']


def get_applications():
    return db.cache.find_one({'type': 'a'})['value']


def get_facility():
    return db.cache.find_one({'type': 'f'})['value']


# CHARTS


# list of available charts from chart cache
def get_charts_list():
    res = db.charts.find({}, {'name': 1, 'title': 1, 'created': 1, '_id': 0}).sort('title', 1)
    return [i for i in res]


# get specified chart from chart cache
def get_chart(chart_name):
    res = db.charts.find_one({'name': chart_name})
    # FIXME chartkick doesn't support Unicode strings (!!!)
    # http://api.mongodb.org/python/current/tutorial.html#a-note-on-unicode-strings
    if res:
        # FIXME - dirty trick only for data with one series - [['name1', value1], ['name2', value2], ]
        res['data'] = [[i[0].encode('utf8'), i[1]] for i in res['data']]
    return res


# STAT


def get_messages_stat():
    res = db.command('collstats', 'messages')
    return res


def get_db_stat():
    res = db.command('dbstats')
    return res
