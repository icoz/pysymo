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
    """Plain authenticated user stored in MongoDB."""
    def __init__(self, username=None, password=None, email=None):
        self.username = username
        self.password = password
        self.salt = None
        self.email = email
        self.id = None

    def save(self):
        """Save user in MongoDB."""
        user_exist = db.users.find_one({'username': self.username})
        if not user_exist:
            # hash and salt password
            self.__hash_password()
            res = db.users.insert({'username': self.username,
                                   'password': self.password,
                                   'salt': self.salt,
                                   'email': self.email})
            # insert() returns document id
            self.id = res
            return self.id, 'No error'
        else:
            return None, 'Cannot save - user already exists'

    def get_by_username_w_password(self, username, pwd):
        """Find user by name and check password."""
        res = db.users.find_one({'username': username})
        if res:
            self.id = res['_id']
            self.username = username
            # hashed and salted password
            self.password = res['password']
            self.salt = res['salt']
            self.email = res['email']

            # check user password
            # pwd - plain text password from user input
            if self.__check_password(pwd):
                return self
            else:
                return None
        else:
            return None

    def get_by_id(self, userid):
        """Get user by userid. For user_loader callback."""
        # !!! must use ObjectId() to search by _id
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

    def __check_password(self, pwd):
        """Check password."""
        return SHA256.new(pwd + self.salt).hexdigest() == self.password

    def __hash_password(self):
        """Generate salt and hash password."""
        self.salt = SHA256.new(Random.get_random_bytes(30)).hexdigest()
        self.password = SHA256.new(self.password + self.salt).hexdigest()


@login_manager.user_loader
def load_user(user_id):
    user = User()
    return user.get_by_id(user_id)

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user_obj = User()
        # find user and check password
        user = user_obj.get_by_username_w_password(form.username.data, form.password.data)
        if user is None:
            flash('Invalid username or password', 'warning')
        else:
            if login_user(user, remember=form.remember_me.data):
                flash("Logged in successfully.", 'success')
                return redirect(url_for('search'))
            else:
                flash("Unable to log you in.", 'warning')
                return redirect(url_for('home'))
    else:
        flash_form_errors(form)

    return render_template('home.html', login_form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/register', methods=['GET', "POST"])
def register():
    if app.config['REGISTRATION_ENABLED']:
        reg_form = RegistrationForm()
        login_form = LoginForm()

        if reg_form.validate_on_submit():
            user = User(username=reg_form.username.data,
                        password=reg_form.password.data,
                        email=reg_form.email.data)
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
            flash_form_errors(reg_form)
            return render_template('register.html', reg_form=reg_form, login_form=login_form)
    else:
        return redirect(url_for('home'))
