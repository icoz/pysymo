# -*- coding: utf-8 -*-

from math import log, pow, trunc
import sys
import re

__author__ = 'ilya-il'

SIZES = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")


def get_formatted_bytes(value):
    """Format value of bytes to KB-YB."""
    # some values from mongostat are float
    if isinstance(value, float):
        value = trunc(value)

    if value == 0:
        return '0 B'
    elif (value >= 1) and (isinstance(value, int) or isinstance(value, long)):
        i = int(log(value, 2)//10)
        if i <= 8:
            res = round(value/pow(1024, i), 2)
            return '{0:g} {1}'.format(res, SIZES[i])
        else:
            return 'Value error!'
    else:
        return 'Value error!'


def get_formatted_thousand_sep(value):
    """Format number to string with thousands separator."""
    if sys.version_info >= (2, 7):
        return '{0:,}'.format(value)
    else:
        # FIXME (IL): Python <= 2.6 doesn't support ',' format
        return '{0}'.format(value)


def get_formatted_host(value):
    """Format host to support FQDN and IP address"""
    # IP address
    if re.match('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', value):
        return value
    # FQDN ('.' find) - leave only short name
    elif value.find('.') > 0:
        return value[:value.find('.')]
    # any other value (short hostname)
    else:
        return value
