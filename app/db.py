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
    return res


# STAT


def get_messages_stat():
    res = db.command('collstats', 'messages')
    # FIXME (IL): ',d' - only for python >= 2.7
    #stat = list()
    #stat.append(['ns', res['ns']])
    #stat.append(['count', format(res['count'], ',d')])
    #stat.append(['size', format(res['size'], ',d')])
    #stat.append(['storageSize', format(res['storageSize'], ',d')])
    #stat.append(['totalIndexSize', format(res['totalIndexSize'], ',d')])
    #stat.append(['lastExtentSize', format(res['lastExtentSize'], ',d')])
    #stat.append(['avgObjSize', format(res['avgObjSize'], ',d')])
    #stat.append(['indexSizes', res['indexSizes']])

    return res


def get_db_stat():
    res = db.command('dbstats')
    # FIXME (IL): ',d' - only for python >= 2.7
    #stat = list()
    #stat.append(['db', res['db']])
    #stat.append(['fileSize', format(res['fileSize'], ',d')])
    #stat.append(['storageSize', format(res['storageSize'], ',d')])
    #stat.append(['dataSize', format(res['dataSize'], ',d')])
    #stat.append(['indexSize', format(res['indexSize'], ',d')])
    #stat.append(['objects', format(res['objects'], ',d')])
    #stat.append(['avgObjSize', format(res['avgObjSize'], ',f')])
    #stat.append(['collections', res['collections']])

    return res
