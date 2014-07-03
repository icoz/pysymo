#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'ilya-il'

import sys
import json
import traceback
from datetime import datetime

line = sys.stdin.readline()
if line:
#    print(line)
#    print('')

    # TEST - 1.txt - remove escape characters \'
    # replace \' to '
#    line = line.replace(r"\'", "'")
    # replace \\ to empty string
#    line = line.replace(r"\\", "")

    # TEST - non unicode symbols - strip out
    # https://docs.python.org/2/howto/unicode.html#the-unicode-type
#    line = line.decode('utf-8', 'ignore')

#    print(line)
#    print('')

#    print str2.decode('string_escape')
    # TEST - 2.txt - UnicodeDecodeError: 'utf8' codec can't decode byte 0xc8 in position 237: invalid continuation byte
    #line = line.decode('latin-1')
    #print(line)

    # JSON LOAD
    try:
        data = json.loads(line)
    except Exception, e:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        print('==============================')
        print('EXCEPTION: {0}'.format(exc_value))
        print('DATETIME: {0}\n'.format(datetime.now().strftime('%d.%m.%Y %H:%M:%S')))
        print('ERROR LINE: {0}'.format(line))
        traceback.print_exception(exc_type, exc_value, exc_traceback, limit=1)
        print('==============================')

#    print data
