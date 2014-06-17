# -*- coding: utf-8 -*-

__author__ = 'icoz'

from functools import wraps
from app import app
from app.db import db
from app.forms import RegistrationForm, flash_form_errors
from flask import session, request, redirect, url_for, render_template, flash


def login_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if session.get('logged_in'):
            return func(*args, **kwargs)
        else:
            print('url=', request.url)
            session['next'] = request.url
            return redirect(url_for('login'), code=302)

    return decorated_view


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == 'GET':
        session['next'] = None
        return redirect(url_for('home'))
    if request.method == 'POST':
        r = db['users'].find_one({'user': request.form['username']})
        # user, passwd = ("user", "pass")
        if r is None:
            flash('Invalid username or password', 'warning')
        elif request.form['password'] != r['password']:
            flash('Invalid username or password', 'warning')
        else:
            #print('login ok, setting session')
            session['logged_in'] = True
            #print('process 1', session)
            session['username'] = request.form['username']
            #print('process 2', session)
            # TODO store user_id
            session['user_id'] = str(r['_id'])
            #print('before flash')
            flash("Logged in successfully.", 'success')
            #print('after flash')
            if session.get('next'):
                url = session['next']
                session['next'] = None
                return redirect(url)
            else:
                return redirect(url_for('search'))
    return redirect(url_for('home'))


@app.route('/logout')
@login_required
def logout():
    session.clear()
    return redirect(url_for('home'))


@app.route('/register', methods=['GET', "POST"])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        user = form.username.data
        password = form.password.data
        email = form.email.data
        dbu = db['users']
        # TODO: check on exists
        rec = dbu.find_one({"user": user})
        if rec is None:
            # TODO: make it safe to save to mongodb
            dbu.insert({'user': user, 'password': password, 'mail': email})
            flash('User registered. You can login now.', 'success')
            session['next'] = None
            return redirect(url_for('home'))
        else:
            flash('Error! Login is not unique!', 'warning')
            return redirect(url_for('register'))
    else:
        flash_form_errors(form)
        return render_template('register.html', form=form)
