#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = 'ilya-il'

import sys
import json
import traceback
from datetime import datetime
from pymongo import MongoClient

from config import MONGO_HOST, MONGO_PORT, MONGO_DATABASE, PIPER_ERROR_LOG

db = MongoClient(host=MONGO_HOST, port=MONGO_PORT)[MONGO_DATABASE]

while 1:
    line = sys.stdin.readline()
    if not line:
        break

    try:
        # 1) # replace \' to '
        line = line.replace(r"\'", "'")
        # 2) replace \\ to empty string
        line = line.replace(r"\\", "")
        # 3) non unicode symbols - strip out
        # https://docs.python.org/2/howto/unicode.html#the-unicode-type
        # FIXME (IL): error - decode() takes no keyword arguments - on SLES 11 x64, python 2.6.9
        line = line.decode('utf-8', errors='ignore')

        data = json.loads(line)

        # 4) convert UNIXTIME to Python datetime
        data['d'] = datetime.fromtimestamp(data['d'])

        db.messages.insert(data)

    except Exception as e:
        exc_type, exc_value, exc_traceback = sys.exc_info()

        f = open(PIPER_ERROR_LOG, 'at')
        f.write('==============================\n')
        f.write('EXCEPTION: {0}\n'.format(exc_value))
        f.write('DATETIME: {0}\n'.format(datetime.now().strftime('%d.%m.%Y %H:%M:%S')))
        f.write('ERROR LINE: {0}\n'.format(line))
        traceback.print_exception(exc_type, exc_value, exc_traceback, limit=1, file=f)
        f.close()
        exit(1)