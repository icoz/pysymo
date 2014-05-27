#!/usr/bin/python

import sys
import json
from datetime import datetime

from pymongo import MongoClient

from save_to_db import save_to_db

MONGO_HOST = '127.0.0.1'
MONGO_PORT = 27017
MONGO_DATABASE = 'syslog'

db = MongoClient(host=MONGO_HOST, port=MONGO_PORT)[MONGO_DATABASE]

try:
    # pre_allocate_in_db()
    while 1:
        line = sys.stdin.readline()
        if not line:
            break
        # 1) fix \' strings
        data = json.loads(line.decode('string_escape'))
        # 2) convert UNIXTIME to Python datetime
        data['d'] = datetime.fromtimestamp(data['d'])

        save_to_db(db, data)

except Exception, e:
    f = open('/var/log/pysymo/piper_error.log', 'ab')
    f.write(e.message)
    f.write('\n')
    f.write(line)
    f.close()
    exit(0)
