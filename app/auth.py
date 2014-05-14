from functools import wraps
from app import app
from app.db import db
from flask import session, request, redirect, url_for, render_template, flash

__author__ = 'icoz'


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
        return render_template('login.html')
    if request.method == 'POST':
        r = db['users'].find_one({'user': request.form['username']})
        # user, passwd = ("user", "pass")
        print(r)
        print()
        if r is None:
            flash('Invalid username')
        elif request.form['password'] != r['password']:
            flash('Invalid password')
        else:
            print('login ok, setting session')
            session['logged_in'] = True
            print('process 1', session)
            session['username'] = request.form['username']
            print('process 2', session)
            # TODO store user_id
            session['user_id'] = str(r['_id'])
            print('before flash')
            flash("Logged in successfully.")
            print('after flash')
            if session.get('next'):
                url = session['next']
                session['next'] = None
                return redirect(url)
            else:
                return redirect(url_for('home'))
                # return redirect(request.args.get("next") or url_for("home"))
    return redirect(url_for('home'))


@app.route('/logout')
@login_required
def logout():
    session.clear()
    return redirect(url_for('home'))


@app.route('/register', methods=['GET', "POST"])
def register():
    if request.method == "GET":
        return render_template('register.html')
    if request.method == 'POST':
        user = request.form['username']
        password = request.form['password']
        mail = request.form['email']
        dbu = db['users']
        # TODO: check on exists
        rec = dbu.find_one({"user": user})
        if rec is None:
            # TODO: make it safe to save to mongodb
            dbu.insert({'user': user, 'password': password, 'mail': mail})
            flash('Registered. Sending to login page.')
            session['next'] = None
            return redirect(url_for('login'))
        else:
            flash('Error! Login is not unique!')
    pass
