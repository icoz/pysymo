#!/usr/bin/python
# -*- coding: utf-8 -*-

from pymongo import MongoClient
from config import MONGO_HOST, MONGO_PORT, MONGO_DATABASE
import re

__author__ = 'ilya-il'

db = MongoClient(host=MONGO_HOST, port=int(MONGO_PORT))[MONGO_DATABASE]
cur = db.messages.find({'h': {'$not': re.compile('.*\..*')}}).distinct('h')

for doc in cur:
    db.messages.update({"h": doc},
                       {"$set": {"h": doc + ".mycompany,com"}}, False)
