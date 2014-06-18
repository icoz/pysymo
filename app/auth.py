# -*- coding: utf-8 -*-

__author__ = 'icoz'

from app import app, login_manager
from app.db import db
from app.forms import RegistrationForm, flash_form_errors, LoginForm
from flask import redirect, url_for, render_template, flash
from flask.ext.login import UserMixin, login_user, logout_user, login_required
from bson.objectid import ObjectId


class User(UserMixin):
    def __init__(self, username=None, password=None, email=None):
        self.username = username
        self.password = password
        self.email = email
        self.id = None

    def save(self):
        res = db.users.insert({'username': self.username,
                               'password': self.password,
                               'email': self.email})
        # insert() returns document id
        self.id = res
        return self.id

    def get_by_username(self, username):
        res = db.users.find_one({'username': username})
        if res:
            self.id = res['_id']
            self.username = username
            self.email = res['email']
            return self
        else:
            return None

    def get_by_username_w_password(self, username):
        res = db.users.find_one({'username': username})
        if res:
            self.id = res['_id']
            self.username = username
            self.password = res['password']
            self.email = res['email']
            return self
        else:
            return None

    def get_by_id(self, userid):
        # !!!
        # !!! must use ObjectId() to search by _id
        # !!!
        res = db.users.find_one({'_id': ObjectId(userid)})
        if res:
            self.id = res['_id']
            self.username = res['username']
            self.password = res['password']
            self.email = res['email']
            return self
        else:
            return None


@login_manager.user_loader
def load_user(userid):
    user = User()
    return user.get_by_id(userid)

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user_obj = User()
        user = user_obj.get_by_username_w_password(form.username.data)
        if user is None:
            flash('Invalid username or password', 'warning')
        # TODO check password!!!
        elif form.password.data != user.password:
            flash('Invalid username or password', 'warning')
        else:
            if login_user(user):
                flash("Logged in successfully.", 'success')
                return redirect(url_for('search'))
            else:
                flash("Unable to log you in.", 'warning')
                return redirect(url_for('home'))
    else:
        flash_form_errors(form)

    return render_template('home.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/register', methods=['GET', "POST"])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(username=form.username.data,
                    password=form.password.data,
                    email=form.email.data)
        # save user to db
        # TODO try/except - duplicate users
        user.save()
        # try to login
        if login_user(user):
            flash("Logged in successfully.", 'success')
            return redirect(url_for('search'))
        else:
            flash("Unable to log you in.", 'warning')
            return redirect(url_for('home'))
    else:
        flash_form_errors(form)
        return render_template('register.html', form=form)
