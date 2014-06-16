#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'ilya-il'

from pymongo import MongoClient
from config import MONGO_HOST, MONGO_PORT, MONGO_DATABASE

db = MongoClient(host=MONGO_HOST, port=MONGO_PORT)[MONGO_DATABASE]

if 'messages' not in db.collection_names():
    # TODO: create TTL or capped collection
    db.create_collection('messages')
    db.messages.ensure_index('h', 1)
    db.messages.ensure_index('d', -1)
    db.messages.ensure_index('f', 1)
    db.messages.ensure_index('a', 1)
    db.messages.ensure_index('p', 1)
    print("OK: Colleciton 'messages' and indexes were created in '{0}' database").format(MONGO_DATABASE)
else:
    print("ERROR: Collection 'messages' already exists")