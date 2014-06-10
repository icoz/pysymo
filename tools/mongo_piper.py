#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'ilya-il'

import sys
import json
from datetime import datetime

from pymongo import MongoClient

from save_to_db import save_to_db
from config import MONGO_HOST, MONGO_PORT, MONGO_DATABASE

db = MongoClient(host=MONGO_HOST, port=MONGO_PORT)[MONGO_DATABASE]

try:
    # pre_allocate_in_db()
    while 1:
        line = sys.stdin.readline()
        if not line:
            break

        # 1) # replace \' to '
        line = line.replace(r"\'", "'")
        # 2) replace \\ to empty string
        line = line.replace(r"\\", "")
        # 3) non unicode symbols - strip out
        # https://docs.python.org/2/howto/unicode.html#the-unicode-type
        line = line.decode('utf-8', errors='ignore')

        data = json.loads(line)

        # 4) convert UNIXTIME to Python datetime
        data['d'] = datetime.fromtimestamp(data['d'])

        save_to_db(db, data)

except Exception, e:
    f = open('/var/log/pysymo/piper_error.log', 'ab')
    f.write(e.message)
    f.write('\n')
    f.write(line)
    f.close()
    exit(0)
