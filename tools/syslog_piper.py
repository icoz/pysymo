#!/usr/bin/python
# -*- coding: utf-8 -*-

""" Common syslog to MongoDB piper script.

Reads line from stdin. Line should be a python dict.
Puts it in MongoDB collection 'messages'.

Use for rsyslog, syslog-ng 2.x.

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
            # convert datetime string to Python datetime
            # rsyslog   - RFC 3339 - %timestamp:::date-rfc3339%
            # syslog-ng - ISO 8601 - $ISODATE
            # cut 19 chars to match mask, fractions of a second and timezone are ignored
            data['d'] = datetime.strptime(data['d'][0:19], '%Y-%m-%dT%H:%M:%S')

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
