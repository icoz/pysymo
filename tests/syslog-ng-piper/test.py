#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'ilya-il'

import sys
import json
import traceback
from datetime import datetime

line = sys.stdin.readline()
if line:
    print(type(line),line)
    print('')

    # TEST - 1.txt - remove escape characters \'
    # 1) # replace \' to '
    line = line.replace(r"\'", "'")

    # TEST
    # 2) replace \\ to empty string
    line = line.replace(r"\\", "")

#    print(line)
    print('')

    # TEST - non unicode symbols - strip out
    # 3) non unicode symbols - strip out
    # https://docs.python.org/2/howto/unicode.html#the-unicode-type
    # decode() takes no keyword arguments - on python 2.6.9
#    if sys.version_info >= (2, 7):
#        line = line.decode('utf-8', errors='ignore')
#    else:
#        line = line.decode('utf-8', 'ignore')

    print(type(line), line)
    print('')

    # JSON LOAD
    try:
        data = json.loads(line)
        print(data)
    except Exception, e:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        print('==============================')
        print('EXCEPTION: {0}'.format(exc_value))
        print('DATETIME: {0}\n'.format(datetime.now().strftime('%d.%m.%Y %H:%M:%S')))
        print('ERROR LINE: {0}'.format(line))
        traceback.print_exception(exc_type, exc_value, exc_traceback, limit=1)
        print('==============================')

#    print data
