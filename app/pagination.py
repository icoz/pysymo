# -*- coding: utf-8 -*-

__author__ = 'ilya-il'

PREV_LABEL = '&laquo;'
NEXT_LABEL = '&raquo;'

# 0 - function
# 1 - page_num
LINK = '<li><a href="javascript:{0}({1})">{1}</a></li>'
LINKS_BEGIN = '<ul class="pagination">'
LINKS_END = '</ul>'


class Pagination(object):
    """
        Pagination class for post-method form
        Creates bootstrap pagination with <a>-links
        to javascript function 'function'
    """
    def __init__(self, **kwargs):
        self.page_num = kwargs.get('page_num', 1)
        self.total_records = kwargs.get('total_records', 0)
        self.records_per_page = kwargs.get('records_per_page', 10)
        self.function = kwargs.get('function', '')

    @property
    def links(self):
        l = list()
        l.append(LINKS_BEGIN)
        for i in range(1, 6):
            l.append(LINK.format(self.function, i))
        l.append(LINKS_END)
        return ''.join(l)