# -*- coding: utf-8 -*-

__author__ = 'ilya-il'

import re

from app.db import db_get_medb_entry

# regular expressions to search
MSG_REGEXP = (
    "(%.*?) ",  # cisco
)


def medb_parse_msg(msg):
    """Search for message explanation and return HTML-link with medb data."""
    for r in MSG_REGEXP:
        rc = re.compile(r)

        res = rc.search(msg)
        if res:
            mes_id = res.group(1)
            medb_entry = db_get_medb_entry(mes_id)
            if medb_entry:
                # exit on first medb entry
                content = '<b>Message:</b> {m}<br>' \
                          '<b>Explanation:</b> {e}<br>' \
                          '<b>Action:</b> {a}'.format(m=medb_entry['m'],
                                                      e=medb_entry['e'],
                                                      a=medb_entry['a'])
                medb_tooltip = '<a href="#" class="medb" rel="popover" ' \
                               'data-title="{title}" data-content="{content}">[MEDB]' \
                               '</a>'.format(title=medb_entry['id'],
                                             content=content)
                return medb_tooltip
    return None