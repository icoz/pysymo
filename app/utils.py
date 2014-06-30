# -*- coding: utf-8 -*-

__author__ = 'ilya-il'

from math import log, pow
import sys

SIZES = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")


def get_formatted_bytes(bytes):
    """Format value of bytes to KB/MB/etc."""
    if bytes > 0:
        i = int(log(bytes, 2)//10)
        value = round(bytes/pow(1024, i), 2)
        return '{0:g} {1}'.format(value, SIZES[i])
    else:
        return 'Value error!'


def get_formatted_thousand_sep(value):
    """Format number to string with thousands separator."""
    if sys.version_info >= (2, 7):
        return '{0:,}'.format(value)
    else:
        # FIXME (IL): Python <= 2.6 doesn't support ',' format
        return '{0}'.format(value)
