# -*- coding: utf-8 -*-

__author__ = 'icoz'

from pymongo import MongoClient

MONGO_HOST = '127.0.0.1'
MONGO_PORT = 27017
MONGO_DATABASE = 'syslog'

db = MongoClient(host=MONGO_HOST, port=MONGO_PORT)[MONGO_DATABASE]


def get_hosts():
    print('get_hosts called')
    res = db.cache.find_one({'type': 'h'})['value']
    return sorted([(i, i) for i in res])


def get_applications():
    res = db.cache.find_one({'type': 'a'})['value']
    return sorted([(i, i) for i in res])


def get_facility():
    res = db.cache.find_one({'type': 'f'})['value']
    return sorted([(i, i) for i in res])


# top hosts and messages count, desc order
def get_top_hosts():
    res = db.messages.aggregate([{"$group": {"_id": "$h", "count": {"$sum": 1}}},
                                 {"$sort": {"count": -1}},
                                 {"$limit": 5}
                                 ])
    # return list [['Label', value], }] for chartkick
    # BUG: chartkick can't use unicode string like u'test'
    # add count to hostname - create label for chart
    return [[i['_id'].encode('utf8') + ' - ' + str(i['count']), i['count']] for i in res['result']]


# messages count per day
def get_daily_stat():
    res = db.messages.aggregate([{"$project": {"host": "$h",
                                               "y": {"$year": "$d"},
                                               "m": {"$month": "$d"},
                                               "d": {"$dayOfMonth": "$d"}}
                                  },
                                 {"$group": {"_id": {"y": "$y", "m": "$m", "d": "$d"},
                                             "count": {"$sum": 1}}
                                  }
                                 ])
    #return res['result']
    return [['{0}-{1:02d}-{2:02d}'.format(i["_id"]["y"], i["_id"]["m"], i["_id"]["d"]), i['count']]
            for i in res['result']]
