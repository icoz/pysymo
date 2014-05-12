__author__ = 'icoz'

from app import db

def get_hosts():
    return db.messages.distinct('h')


def get_apps():
    return db.messages.distinct('a')

