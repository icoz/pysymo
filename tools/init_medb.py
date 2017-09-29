#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Init MEDB

Creates collection and indexes. Puts data/medb.txt into collection.

"""

from pymongo import MongoClient
from config import MONGO_HOST, MONGO_PORT, MONGO_DATABASE
from ast import literal_eval
from subprocess import call
from os import remove

__author__ = 'ilya-il'


def main():
    db = MongoClient(host=MONGO_HOST, port=int(MONGO_PORT))[MONGO_DATABASE]

    if 'medb' not in db.collection_names():
        db.create_collection('medb')
        db.messages.ensure_index('id')

        print("OK: Collection 'medb' and indexes were created in '{0}' database".format(MONGO_DATABASE))
        print("OK: Now load medb into '{0}' database".format(MONGO_DATABASE))

        # unzip
        call(['unzip', '../data/medb.zip'])

        f = open('medb.txt', 'r')
        for line in f:
            # convert string into tuple
            t = literal_eval(line)
            db.medb.insert({'id': t[0], 'm': t[1], 'e': t[2], 'a': t[3]})
        f.close()

        remove('medb.txt')
        print('OK: MEDB loaded.')
    else:
        print("ERROR: Collection 'medb' already exists")

if __name__ == '__main__':
    main()
