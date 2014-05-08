from functools import wraps

from flask import session, request, redirect, url_for

__author__ = 'icoz'


def login_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if session['logged_in']:
            return func(*args, **kwargs)
        else:
            session['next'] = request.url
            return redirect(url_for('login'), code=302)

    return decorated_view
