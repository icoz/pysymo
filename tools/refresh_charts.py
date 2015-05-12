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
    for i in list(res):
        # fill data for specified host
        # data for host will be sorted DESC because of db query sort
        # drilldown[<host>]['data'].append([MSG_PRIORITY_LIST[<priority>], <count>])
        drilldown[i['_id']['h']]['data'].append([MSG_PRIORITY_LIST[i['_id']['p']], i['count']])

    # create chart as a string - because event functions cannot be stored in dict() as an object
    chart = """{
        chart: {
            type: 'pie',
            height: 500,
            renderTo: 'hc_container',
            events: {
                drilldown: function(e) { chart.setTitle(null, {text: e.point.name + ' (all messages)'}); },
                drillup: function(e) { chart.setTitle(null, {text: 'All data'}); }
            }
        },
        title: {
            text : 'Top 10 hosts'
        },
        subtitle: {
            text: 'All data'
        },
        legend: {
            enabled: false
        },
        plotOptions: {
            series: {
                dataLabels: {
                    enabled: true,
                    format: '{point.name} - <b>{point.y}</b>'
                },
                point: {
                    events: {
                        click: function(e) {
                            // will work only for drilldown data
                            if (this.name) {
                                // redirect to search form. search with parameters from chart
                                psm_post_search({host: this.series.name, priority: MSG_PRIORITY_LIST.indexOf(this.name)});
                            }
                        }
                    }
                }
            }
        },
        series: [{
            name: 'All data',
            data: """ + main_series.__str__() + """
        }],
        drilldown: {
            series: """ + [drilldown[i] for i in drilldown].__str__() + """
        },
        tooltip: {
            headerFormat: '<span style="font-size:11px">{series.name}</span><br>',
            pointFormat: '<span style="color:{point.color}">{point.name}</span>: <b>{point.y}</b><br/>'
        }
    }"""

    db.charts.update_one({'name': 'tophosts'},
                         {'$set': {'title': 'Top 10 hosts (all data)',
                                   'created': datetime.now(),
                                   # save as str() to avoid unicode
                                   'chart': chart}},
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
            for i in list(res)]

    chart = """{
        chart: {
            type: 'spline',
            renderTo: 'hc_container'
        },
        title: {
            text: 'Messages per day'
        },
        legend: {
            enabled: false
        },
        plotOptions: {
            series: {
                dataLabels: {
                    enabled: false
                }
            }
        },
        yAxis: {
            title: {
                text: 'Number of messages'
            },
            min: 0
        },
        xAxis: {
            type: 'category',
            tickmarkPlacement: 'on'
        },
        series: [{
            name: 'messages',
            data: """ + data.__str__() + """
        }]
    }"""

    db.charts.update_one({'name': 'mesperday'},
                         {'$set': {'title': 'Messages per day',
                                   'created': datetime.now(),
                                   # save as str() to avoid unicode
                                   'chart': chart}},
                         upsert=True)


def main():
    top_hosts()
    messages_per_day()

if __name__ == '__main__':
    main()