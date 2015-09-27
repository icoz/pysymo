# -*- coding: utf-8 -*-

__author__ = 'icoz'

from pymongo import MongoClient

from app.utils import get_formatted_bytes, get_formatted_thousand_sep
from os import environ as env

MONGO_HOST = env.get('PYSYMO_MONGO_HOST') or env.get('DB_PORT_27017_TCP_ADDR') or '127.0.0.1'
MONGO_PORT = env.get('PYSYMO_MONGO_PORT') or env.get('DB_PORT_27017_TCP_PORT') or 27017
MONGO_DATABASE = env.get('PYSYMO_MONGO_DATABASE') or 'syslog'

db = MongoClient(host=MONGO_HOST, port=int(MONGO_PORT))[MONGO_DATABASE]


# MESSAGES


def db_get_hosts():
    res = db.cache.find_one({'type': 'h'})
    if res:
        return res['value']
    else:
        return []


def db_get_applications():
    res = db.cache.find_one({'type': 'a'})
    if res:
        return res['value']
    else:
        return []


def db_get_facility():
    res = db.cache.find_one({'type': 'f'})
    if res:
        return res['value']
    else:
        return []


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
    print(res)

    stat = list()
    stat.append(['db', res.get('db')])
    stat.append(['fileSize', get_formatted_bytes(res.get('fileSize'))])
    stat.append(['storageSize', get_formatted_bytes(res.get('storageSize'))])
    stat.append(['dataSize', get_formatted_bytes(res.get('dataSize'))])
    stat.append(['indexSize', get_formatted_bytes(res.get('indexSize'))])
    stat.append(['objects', get_formatted_thousand_sep(res.get('objects'))])
    stat.append(['avgObjSize', get_formatted_thousand_sep(res.get('avgObjSize'))])
    stat.append(['collections', res.get('collections')])

    return stat


def db_get_messages_stat():
    res = db.command('collstats', 'messages')

    stat = list()
    stat.append(['ns', res.get('ns')])
    stat.append(['count', get_formatted_thousand_sep(res.get('count'))])
    stat.append(['size', get_formatted_bytes(res.get('size'))])
    stat.append(['storageSize', get_formatted_bytes(res.get('storageSize'))])
    stat.append(['totalIndexSize', get_formatted_bytes(res.get('totalIndexSize'))])
    stat.append(['lastExtentSize', get_formatted_bytes(res.get('lastExtentSize'))])
    stat.append(['avgObjSize', res.get('avgObjSize')])
    stat.append(['indexSizes', res.get('indexSizes')])

    return stat


# MEDB

def db_get_medb_entry(medb_id):
    res = db.medb.find_one({'id': medb_id})
    return res
