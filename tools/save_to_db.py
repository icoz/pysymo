#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from db import db

__author__ = 'icoz'
__DEBUG__ = True

from argparse import ArgumentParser
import json


def check_data(data):
    flag = True
    for key in data:
        if key not in ['h', 'a', 'f', 'p', 'd', 'm']:
            flag = False
    return flag


def get_and_parse(pipefile):
    with open(pipefile, 'rt') as f:
        for line in iter(f.readline, ""):
            if __DEBUG__:
                print('got line: {}'.format(line))
            data = json.loads(line)
            if check_data(data):
                db.messages.insert(data)


def main():
    pa = ArgumentParser()
    pa.add_argument('pipefile', help='filename of pipe')
    args = pa.parse_args()
    if args.pipefile:
        get_and_parse(args.pipefile)


if __name__ == '__main__':
    main()