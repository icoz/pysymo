#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Init database script

Creates collections and indexes.

"""

from pymongo import MongoClient, DESCENDING
from config import MONGO_HOST, MONGO_PORT, MONGO_DATABASE

__author__ = 'ilya-il'


def main():
    db = MongoClient(host=MONGO_HOST, port=int(MONGO_PORT))[MONGO_DATABASE]

    if 'messages' not in db.collection_names():
        db.create_collection('messages')
        db.messages.ensure_index('h')
        # TTL-collection for 31 days
        db.messages.ensure_index([('d', DESCENDING)], expireAfterSeconds=60*60*24*31)
        db.messages.ensure_index('f')
        db.messages.ensure_index('a')
        db.messages.ensure_index('p')

        db.users.ensure_index('username', unique=True)
        db.charts.ensure_index('name', unique=True)
        db.cache.ensure_index('type', unique=True)
        print("OK: Collections and indexes were created in '{0}' database".format(MONGO_DATABASE))
    else:
        print("ERROR: Collection 'messages' already exists")

if __name__ == '__main__':
    main()
