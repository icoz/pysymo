# -*- coding: utf-8 -*-

__author__ = 'ilya-il'

from math import log, pow
import sys

SIZES = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")


def get_formatted_bytes(value):
    """Format value of bytes to KB/MB/etc."""
    if value > 0:
        i = int(log(value, 2)//10)
        res = round(value/pow(1024, i), 2)
        return '{0:g} {1}'.format(res, SIZES[i])
    else:
        return 'Value error!'


def get_formatted_thousand_sep(value):
    """Format number to string with thousands separator."""
    if sys.version_info >= (2, 7):
        return '{0:,}'.format(value)
    else:
        # FIXME (IL): Python <= 2.6 doesn't support ',' format
        return '{0}'.format(value)
