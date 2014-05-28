#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'ilya-il'

import sys
import json

line = sys.stdin.readline()
if line:
    print(line)
    print('')

    # TEST - 1.txt - remove escape characters \'
    # replace \' to '
    line = line.replace(r"\'", "'")
    # replace \\ to empty string
    line = line.replace(r"\\", "")

    # TEST - non unicode symbols - strip out
    # https://docs.python.org/2/howto/unicode.html#the-unicode-type
    line = line.decode('utf-8', 'ignore')

    print(line)
    print('')

#    print str2.decode('string_escape')
    # TEST - 2.txt - UnicodeDecodeError: 'utf8' codec can't decode byte 0xc8 in position 237: invalid continuation byte
    #line = line.decode('latin-1')
    #print(line)

    # JSON LOAD
    data = json.loads(line)

    print data
