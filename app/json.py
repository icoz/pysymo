__author__ = 'icoz'

from app import app,request,get_hosts,get_apps

@app.route('/json/servers/', methods=['GET', 'POST'])
def json_servers():
    if request.method == 'GET':
        return str(get_hosts())
        # info = db.messages.aggregate({'$distinct': {'d': 0}})
        # info = db['dates'].aggregate({'$match': {'d': {'$and': [{'$gte':1}, {'$lte': 1}]}}},
        #                              {'$group': {"_id": 'servers', 'servers': {'$addToSet': '$servers'}}})
    else:
        return (str([]))
        # date_from = request.json['date_from']
        # date_to = request.json['date_to']
        # collections = db.dates.find({'date': {'$ge': date_from, '$le': date_to}}, {'coll_name': 1})


@app.route('/json/apps/', methods=['GET', 'POST'])
def json_apps():
    if request.method == 'GET':
        return str(get_apps())
        # info = db.messages.aggregate({'$distinct': {'d': 0}})
        # info = db['dates'].aggregate({'$match': {'d': {'$and': [{'$gte':1}, {'$lte': 1}]}}},
        #                              {'$group': {"_id": 'servers', 'servers': {'$addToSet': '$servers'}}})
    else:
        return (str([]))
