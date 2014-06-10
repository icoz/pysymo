#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = 'ilya-il'

from pymongo import MongoClient

from config import MONGO_HOST, MONGO_PORT, MONGO_DATABASE


db = MongoClient(host=MONGO_HOST, port=MONGO_PORT)[MONGO_DATABASE]

# refresh host list
hosts = db.messages.distinct('h')
db.cache.update({'type': 'h'}, {'$set': {'value': hosts}}, upsert=True)

# refresh program list
# remove digital programs, marks, empty strings
query = {'a': {'$nin': ['--', ''], '$regex': '\D'}}
apps = db.messages.find(query).distinct('a')
db.cache.update({'type': 'a'}, {'$set': {'value': apps}}, upsert=True)

# refresh facility list
fac = db.messages.distinct('f')
db.cache.update({'type': 'f'}, {'$set': {'value': fac}}, upsert=True)