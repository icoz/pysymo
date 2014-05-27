#!/usr/bin/python

__author__ = 'ilya-il'

from pymongo import MongoClient

MONGO_HOST = '127.0.0.1'
MONGO_PORT = 27017
MONGO_DATABASE = 'syslog'

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