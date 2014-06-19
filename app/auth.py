# -*- coding: utf-8 -*-

__author__ = 'icoz'

from app import app, login_manager
from app.db import db
from app.forms import RegistrationForm, flash_form_errors, LoginForm

from flask import redirect, url_for, render_template, flash
from flask.ext.login import UserMixin, login_user, logout_user, login_required

from bson.objectid import ObjectId

from Crypto import Random
from Crypto.Hash import SHA256


class User(UserMixin):
    def __init__(self, username=None, password=None, salt=None, email=None):
        self.username = username
        self.password = password
        self.salt = salt
        self.email = email
        self.id = None

    def save(self):
        user_exist = db.users.find_one({'username': self.username})
        if not user_exist:
            res = db.users.insert({'username': self.username,
                                   'password': self.password,
                                   'salt': self.salt,
                                   'email': self.email})
            # insert() returns document id
            self.id = res
            return self.id, 'No error'
        else:
            return None, 'Cannot register - user already exists'

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
            self.salt = res['salt']
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
            self.salt = res['salt']
            self.email = res['email']
            return self
        else:
            return None

    def check_password(self, pwd):
        pwd_hash = SHA256.new(pwd + self.salt)
        return pwd_hash.hexdigest() == self.password

    @staticmethod
    def hash_password(pwd):
        salt = SHA256.new(Random.get_random_bytes(30))
        pwd_hash = SHA256.new(pwd + salt.hexdigest())
        return pwd_hash.hexdigest(), salt.hexdigest()


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
        elif not user.check_password(form.password.data):
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
        pwd_hash, salt = User.hash_password(form.password.data)
        user = User(username=form.username.data,
                    password=pwd_hash,
                    salt=salt,
                    email=form.email.data)
        # save user to db
        user_id, save_error = user.save()
        if user_id:
            # try to login
            if login_user(user):
                flash("Logged in successfully.", 'success')
                return redirect(url_for('search'))
            else:
                flash("Unable to log you in.", 'warning')
                return redirect(url_for('home'))
        else:
            flash(save_error, 'warning')
            return redirect(url_for('register'))
    else:
        flash_form_errors(form)
        return render_template('register.html', form=form)
