#!/usr/bin/python
# -*- coding: utf-8 -*-

""" Refresh charts script.

Aggregates data for charts.
Puts chart data and properties in collection 'charts'

"""


__author__ = 'ilya-il'

from pymongo import MongoClient, DESCENDING
from datetime import datetime

from config import MONGO_HOST, MONGO_PORT, MONGO_DATABASE, MSG_PRIORITY_LIST


def top_hosts():
    """Top hosts by messages count."""
    db = MongoClient(host=MONGO_HOST, port=MONGO_PORT)[MONGO_DATABASE]

    # Top 10 hosts by message count
    res = db.messages.aggregate([{"$group": {"_id": "$h", "count": {"$sum": 1}}},
                                 {"$sort": {"count": -1}},
                                 {"$limit": 10}
                                 ])
    host_list = []
    main_series = []
    drilldown = dict()

    for i in res['result']:
        host_list.append(i['_id'])
        # use format() to avoid unicode strings
        # [{'name': <host>, 'drilldown': <host>, 'y': <count>}, ]
        main_series.append({'name': '{0}'.format(i['_id']), 'y': i['count'], 'drilldown': '{0}'.format(i['_id'])})
        # {<host>: {'id: <host>, 'data': [], 'name': <host>}, }
        drilldown[i['_id']] = {'id': '{0}'.format(i['_id']), 'data': [], 'name': '{0}'.format(i['_id'])}

    # Hosts and priority
    res = db.messages.aggregate([{"$match": {"h": {"$in": host_list}}
                                  },
                                 {"$group": {"_id": {"h": "$h", "p": "$p"}, "count": {"$sum": 1}}},
                                 {"$sort": {"count": DESCENDING}}
                                 ])
    for i in res['result']:
        # fill data for specified host
        # data for host will be sorted DESC because of db query sort
        # drilldown[<host>]['data'].append([MSG_PRIORITY_LIST[<priority>], <count>])
        drilldown[i['_id']['h']]['data'].append([MSG_PRIORITY_LIST[i['_id']['p']], i['count']])

    chart = dict()
    chart['chart'] = {
        'type': 'pie',
        'height': 500,
        'renderTo': 'hc_container'
    }
    chart['title'] = {'text': 'Top 10 hosts'}
    chart['legend'] = {'enabled': False}
    chart['plotOptions'] = {
        'series': {
            'dataLabels': {
                'enabled': True,
                'format': '{point.name} - <b>{point.y}</b>'
            }
        }
    }
    chart['series'] = [{
        'name': 'All messages',
        'data': main_series
    }]
    chart['drilldown'] = {
        'series': [drilldown[i] for i in drilldown]
    }
    chart['tooltip'] = {
        'headerFormat': '<span style="font-size:11px">{series.name}</span><br>',
        'pointFormat': '<span style="color:{point.color}">{point.name}</span>: <b>{point.y}</b><br/>'
    }

    db.charts.update({'name': 'tophosts'},
                     {'$set': {'title': 'Top 10 hosts',
                               'created': datetime.now(),
                               # save as str() to avoid unicode
                               'chart': chart.__str__()}},
                     upsert=True)


def messages_per_day():
    """Total number of messages per day"""
    db = MongoClient(host=MONGO_HOST, port=MONGO_PORT)[MONGO_DATABASE]

    res = db.messages.aggregate([{"$project": {"host": "$h",
                                               "y": {"$year": "$d"},
                                               "m": {"$month": "$d"},
                                               "d": {"$dayOfMonth": "$d"}}
                                  },
                                 {"$group": {"_id": {"y": "$y", "m": "$m", "d": "$d"},
                                             "count": {"$sum": 1}}
                                  },
                                 {"$sort": {"_id": 1}},
                                 ])
    # data list [['Label', value], ] - ['dd.mm', value]
    data = [['{0:02d}.{1:02d}'.format(i["_id"]["d"], i["_id"]["m"]),
             i['count']]
            for i in res['result']]

    chart = dict()

    chart['chart'] = {
        'type': 'spline',
        'renderTo': 'hc_container'
    }
    chart['title'] = {'text': 'Messages per day'}
    chart['legend'] = {'enabled': False}
    chart['yAxis'] = {
        'title': {
            'text': 'Number of messages'
        },
        'min': 0
    }
    chart['xAxis'] = {
        'type': 'category',
        'tickmarkPlacement': 'on'
    }
    chart['plotOptions'] = {
        'series': {
            'dataLabels': {
                'enabled': False
            }
        }
    }
    chart['series'] = [{
        'name': 'messages',
        'data': data
    }]

    db.charts.update({'name': 'mesperday'},
                     {'$set': {'title': 'Messages per day',
                               'created': datetime.now(),
                               # save as str() to avoid unicode
                               'chart': chart.__str__()
                               }
                      },
                     upsert=True)


def main():
    top_hosts()
    messages_per_day()

if __name__ == '__main__':
    main()