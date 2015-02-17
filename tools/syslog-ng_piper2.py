#!/usr/bin/python
# -*- coding: utf-8 -*-

""" Syslog-ng to MongoDB piper script.

Reads line from stdin. Line should be a python dict.
Puts it in MongoDB collection 'messages'.

"""


__author__ = 'ilya-il'

import sys
import ast
import traceback
from datetime import datetime
from pymongo import MongoClient

from config import MONGO_HOST, MONGO_PORT, MONGO_DATABASE, PIPER_ERROR_LOG


def main():
    db = MongoClient(host=MONGO_HOST, port=MONGO_PORT)[MONGO_DATABASE]

    while 1:
        try:
            line = sys.stdin.readline()
            if not line:
                break

            data = ast.literal_eval(line)
            # convert UNIXTIME to Python datetime
            data['d'] = datetime.fromtimestamp(data['d'])

            db.messages.insert(data)

        # yeah, it's too broad, I know.
        except:
            exc_type, exc_value, exc_traceback = sys.exc_info()

            f = open(PIPER_ERROR_LOG, 'at')
            f.write('==============================\n')
            f.write('EXCEPTION: {0}\n'.format(exc_value))
            f.write('DATETIME: {0}\n'.format(datetime.now().strftime('%d.%m.%Y %H:%M:%S')))
            f.write('ERROR LINE: {0}\n'.format(line))
            traceback.print_exception(exc_type, exc_value, exc_traceback, limit=1, file=f)
            f.close()
            exit(1)


if __name__ == '__main__':
    main()
