# -*- coding: utf-8 -*-

__author__ = 'icoz'

from pymongo import MongoClient

from app.utils import get_formatted_bytes, get_formatted_thousand_sep

MONGO_HOST = '127.0.0.1'
MONGO_PORT = 27017
MONGO_DATABASE = 'syslog'

db = MongoClient(host=MONGO_HOST, port=MONGO_PORT)[MONGO_DATABASE]


# MESSAGES


def db_get_hosts():
    return db.cache.find_one({'type': 'h'})['value']


def db_get_applications():
    return db.cache.find_one({'type': 'a'})['value']


def db_get_facility():
    return db.cache.find_one({'type': 'f'})['value']


# CHARTS


# list of available charts from chart cache
def db_get_charts_list():
    res = db.charts.find({}, {'name': 1, 'title': 1, 'created': 1, '_id': 0}).sort('title', 1)
    return [i for i in res]


# get specified chart from chart cache
def db_get_chart(chart_name):
    res = db.charts.find_one({'name': chart_name})
    return res


# STAT

def db_get_db_stat():
    res = db.command('dbstats')

    stat = list()
    stat.append(['db', res['db']])
    # fileSize is float on SLES 11 x64, python 2.6.9 - convert to long
    stat.append(['fileSize', get_formatted_bytes(long(res['fileSize']))])
    stat.append(['storageSize', get_formatted_bytes(res['storageSize'])])
    stat.append(['dataSize', get_formatted_bytes(res['dataSize'])])
    stat.append(['indexSize', get_formatted_bytes(res['indexSize'])])
    stat.append(['objects', get_formatted_thousand_sep(res['objects'])])
    stat.append(['avgObjSize', get_formatted_thousand_sep(res['avgObjSize'])])
    stat.append(['collections', res['collections']])

    return stat


def db_get_messages_stat():
    res = db.command('collstats', 'messages')

    stat = list()
    stat.append(['ns', res['ns']])
    stat.append(['count', get_formatted_thousand_sep(res['count'])])
    stat.append(['size', get_formatted_bytes(res['size'])])
    stat.append(['storageSize', get_formatted_bytes(res['storageSize'])])
    stat.append(['totalIndexSize', get_formatted_bytes(res['totalIndexSize'])])
    stat.append(['lastExtentSize', get_formatted_bytes(res['lastExtentSize'])])
    stat.append(['avgObjSize', res['avgObjSize']])
    stat.append(['indexSizes', res['indexSizes']])

    return stat
