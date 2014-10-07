# -*- coding: utf-8 -*-

__author__ = 'icoz'

from app import app, login_manager
from app.db import db
from app.forms import RegistrationForm, flash_form_errors, LoginForm

from flask import redirect, url_for, render_template, flash
from flask.ext.login import UserMixin, login_user, logout_user, login_required
from flask.ext.babel import gettext

from bson.objectid import ObjectId

from Crypto import Random
from Crypto.Hash import SHA256

if app.config['AUTH_TYPE'] == 'ldap':
    import ldap


class UserLDAP(UserMixin):
    """LDAP authenticated user."""
    def __init__(self, username=None, email=None):
        self.id = None
        self.username = username
        self.username1 = username
        self.email = email

    def get_by_username_w_password(self, username, pwd):
        """Check user exists in LDAP and auth him."""
        try:
            conn = ldap.initialize(app.config['LDAP_SERVER'])
            conn.protocol_version = 3
            conn.simple_bind_s(app.config['LDAP_SERVICE_USER'], app.config['LDAP_SERVICE_PASSWORD'])
            # search for user, username is 'cn' - unique for LDAP
            res = conn.search_s(app.config['LDAP_SEARCH_BASE'],
                                ldap.SCOPE_SUBTREE,
                                'cn={0}'.format(username),
                                ['cn', 'mail'])

            if not res:
                # user not found
                return None, 'Invalid username or password.'

            # res format - [(<user_dn>, {<properties>})]
            user_dn = res[0][0]

            # try to auth with user password
            conn.simple_bind_s(user_dn, pwd)

            # auth ok
            self.id = res[0][1].get('cn')[0]
            self.username = res[0][1].get('cn')[0]
            if res[0][1].get('mail'):
                self.email = res[0][1].get('mail')[0]
            else:
                self.email = None
            conn.unbind_s()

            return self, 'No error'
        except ldap.LDAPError as e:
            return None, e.message

    def get_by_id(self, user_id):
        """Get user by userid. For user_loader callback."""
        try:
            conn = ldap.initialize(app.config['LDAP_SERVER'])
            conn.protocol_version = 3
            conn.simple_bind_s(app.config['LDAP_SERVICE_USER'], app.config['LDAP_SERVICE_PASSWORD'])
            # search for user, username is 'cn' - unique for LDAP
            res = conn.search_s(app.config['LDAP_SEARCH_BASE'],
                                ldap.SCOPE_SUBTREE,
                                'cn={0}'.format(user_id),
                                ['cn', 'mail'])

            if not res:
                # user not found
                return None

            # res format - [(<user_dn>, {<properties>})]
            self.id = res[0][1].get('cn')[0]
            self.username = res[0][1].get('cn')[0]
            if res[0][1].get('mail'):
                self.email = res[0][1].get('mail')[0]
            else:
                self.email = None

            conn.unbind_s()

            return self
        except ldap.LDAPError:
            return None


class UserPlain(UserMixin):
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
                return self, 'No error'
            else:
                return None, 'Invalid username or password.'
        else:
            return None, 'Invalid username or password.'

    def get_by_id(self, user_id):
        """Get user by userid. For user_loader callback."""
        # !!! must use ObjectId() to search by _id
        res = db.users.find_one({'_id': ObjectId(user_id)})
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
        return SHA256.new((pwd + self.salt).encode()).hexdigest() == self.password

    def __hash_password(self):
        """Generate salt and hash password."""
        self.salt = SHA256.new(Random.get_random_bytes(30)).hexdigest()
        self.password = SHA256.new((self.password + self.salt).encode()).hexdigest()


@login_manager.user_loader
def load_user(user_id):
    if app.config['AUTH_TYPE'] == 'ldap':
        user = UserLDAP()
    elif app.config['AUTH_TYPE'] == 'plain':
        user = UserPlain()
    else:
        return None
    return user.get_by_id(user_id)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        if app.config['AUTH_TYPE'] == 'ldap':
            user_obj = UserLDAP()
        elif app.config['AUTH_TYPE'] == 'plain':
            user_obj = UserPlain()
        else:
            flash(gettext('Unknown authentication type.'), 'warning')
            return render_template('home.html', login_form=form)

        # find user and check password
        user, error = user_obj.get_by_username_w_password(form.username.data, form.password.data)
        if user is None:
            flash(error, 'warning')
        else:
            if login_user(user, remember=form.remember_me.data):
                flash('Logged in successfully.', 'success')
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
    if app.config['REGISTRATION_ENABLED'] and app.config['AUTH_TYPE'] == 'plain':
        reg_form = RegistrationForm()
        login_form = LoginForm()

        if reg_form.validate_on_submit():
            user = UserPlain(username=reg_form.username.data,
                             password=reg_form.password.data,
                             email=reg_form.email.data)
            # save user to db
            user_id, save_error = user.save()
            if user_id:
                # try to login
                if login_user(user):
                    flash('Logged in successfully.', 'success')
                    return redirect(url_for('search'))
                else:
                    flash('Unable to log you in.', 'warning')
                    return redirect(url_for('home'))
            else:
                flash(save_error, 'warning')
                return redirect(url_for('register'))
        else:
            flash_form_errors(reg_form)
            return render_template('register.html', reg_form=reg_form, login_form=login_form)
    else:
        return redirect(url_for('home'))
