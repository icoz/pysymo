#!/usr/bin/python

import sys
import json
from datetime import datetime

line = sys.stdin.readline()
if line:
    # TEST - 1.txt - remove escape characters \'
    line = line.decode('string_escape') 
    print line

    # TEST - 2.txt - UnicodeDecodeError: 'utf8' codec can't decode byte 0xc8 in position 237: invalid continuation byte
    line = line.decode('latin-1')
    print line

    # JSON LOAD
    data = json.loads(line)

