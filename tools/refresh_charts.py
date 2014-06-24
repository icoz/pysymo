#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = 'ilya-il'

from pymongo import MongoClient
from datetime import datetime

from config import MONGO_HOST, MONGO_PORT, MONGO_DATABASE

db = MongoClient(host=MONGO_HOST, port=MONGO_PORT)[MONGO_DATABASE]


# TOP HOSTS by messages count
def top_hosts():
    library = {
        'chart': {
            'height': 500
        },
        'title': {
            'text': 'Top10 hosts'
        },
        'plotOptions': {
            'pie': {
                'dataLabels': {
                    'enabled': 'true',
                    'format': '<b>{point.name}</b> - {point.y}'
                }
            }
        },
#        'legend': {
#            'layout': 'vertical',
#            'align': 'right',
#            'verticalAlign': 'middle'
#        }
    }

    res = db.messages.aggregate([{"$group": {"_id": "$h", "count": {"$sum": 1}}},
                                 {"$sort": {"count": -1}},
                                 {"$limit": 10}
                                 ])
    # data list [['Label', value], ] for chartkick
    data = [[i['_id'].encode('utf-8'), i['count']] for i in res['result']]

    db.charts.update({'name': 'tophosts'},
                     {'$set': {'type': 'pie',
                               'title': 'Top 10 hosts',
                               'library': library,
                               'created': datetime.now(),
                               # FIXME - dirty trick - store data as a string to avoid unicode. See encode() above
                               'data': data.__str__()}},
                     upsert=True)


# Messages count per day
def messages_per_day():
    library = {
        'title': {
            'text': 'Messages per day'
        }
    }
    res = db.messages.aggregate([{"$project": {"host": "$h",
                                               "y": {"$year": "$d"},
                                               "m": {"$month": "$d"},
                                               "d": {"$dayOfMonth": "$d"}}
                                  },
                                 {"$group": {"_id": {"y": "$y", "m": "$m", "d": "$d"},
                                             "count": {"$sum": 1}}
                                  }
                                 ])
    # data list [['Label', value], ] for chartkick
    data = [['{0}-{1:02d}-{2:02d}'.format(i["_id"]["y"], i["_id"]["m"], i["_id"]["d"]),
             i['count']]
            for i in res['result']]

    db.charts.update({'name': 'mesperday'},
                     {'$set': {'type': 'line',
                               'title': 'Messages per day',
                               'library': library,
                               'created': datetime.now(),
                               # FIXME - dirty trick - store data as a string to avoid unicode
                               'data': data.__str__()}},
                     upsert=True)


# Warning messages per host
# Warning messages only - ['emerg', 'alert', 'crit', 'err', 'warn'] - [0-4]
def warning_messages_per_host():
    library = {
        'chart': {
            'height': 800
        },
        'title': {
            'text': 'Warning messages per host (Top 10)'
        },
        'legend': {
            'layout': 'vertical',
            'align': 'right',
            'verticalAlign': 'middle',
            'reversed': 'true'
        },
        'plotOptions': {
            'bar': {
                'showInLegend': 'true',
                'dataLabels': {
                    "enabled": 'true'
                }
            }
        }
    }
    res = db.messages.aggregate([{"$match": {"p": {"$in": [0, 1, 2, 3, 4]}}
                                  },
                                 {"$group": {"_id": {"host": "$h", "type": "$p"},
                                             "count": {"$sum": 1}}
                                  },
                                 {"$sort": {"count": -1}},
                                 {"$limit": 10}
                                 ])
    emerg_serie = []
    alert_serie = []
    crit_serie = []
    err_serie = []
    warn_serie = []

    for r in res['result']:
        if r["_id"]["type"] == 0:
            emerg_serie.append([r["_id"]["host"].encode('utf-8'), r["count"]])
        elif r["_id"]["type"] == 1:
            alert_serie.append([r["_id"]["host"].encode('utf-8'), r["count"]])
        elif r["_id"]["type"] == 2:
            crit_serie.append([r["_id"]["host"].encode('utf-8'), r["count"]])
        elif r["_id"]["type"] == 3:
            err_serie.append([r["_id"]["host"].encode('utf-8'), r["count"]])
        elif r["_id"]["type"] == 4:
            warn_serie.append([r["_id"]["host"].encode('utf-8'), r["count"]])

    data = []

    # each serie sorted by host ASC
    # series in data[] sorted DESC by type value (4-0)
    # series on charts display in reverse order (legend too)
    if warn_serie:
        data.append({r"data": sorted(warn_serie), "name": "warn"})
    if err_serie:
        data.append({"data": sorted(err_serie), "name": "err"})
    if crit_serie:
        data.append({"data": sorted(crit_serie), "name": "crit"})
    if alert_serie:
        data.append({"data": sorted(alert_serie), "name": "alert"})
    if emerg_serie:
        data.append({"data": sorted(emerg_serie), "name": "emerg"})

    db.charts.update({'name': 'warnmesperhost'},
                     {'$set': {'type': 'bar',
                               'title': 'Warning messages per host (Top 10)',
                               'library': library,
                               'created': datetime.now(),
                               # FIXME - dirty trick - store data as a string to avoid unicode. See encode() above
                               'data': data.__str__()}},
                     upsert=True)


def main():
    top_hosts()
    messages_per_day()
    warning_messages_per_host()

if __name__ == '__main__':
    main()