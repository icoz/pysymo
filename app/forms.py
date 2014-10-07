# -*- coding: utf-8 -*-

__author__ = 'ilya-il'

from app.db import db_get_hosts, db_get_applications, db_get_facility
from flask import flash
from flask_wtf import Form
from flask.ext.babel import lazy_gettext
from wtforms import validators, SelectMultipleField, DateTimeField, RadioField, SelectField, \
    StringField, HiddenField, PasswordField, BooleanField
from config import MSG_PRIORITY_LIST, DATETIME_FORMAT

priority_list = [(i, MSG_PRIORITY_LIST[i]) for i in range(len(MSG_PRIORITY_LIST))]
ie_list = [(0, lazy_gettext('Include')), (1, lazy_gettext('Exclude'))]
sort_list = [(1, 'ASC'), (-1, 'DESC')]


def flash_form_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(lazy_gettext("Field '%(field)s' - %(errtext)s",
                               field=getattr(form, field).label.text, errtext=error), 'warning')


class RequestForm(Form):
    # HOST
    host_ie = RadioField('HostIE', choices=ie_list, default=0, coerce=int)
    host = SelectMultipleField(lazy_gettext('Host'))
    # PROGRAM
    application_ie = RadioField('ApplicationIE', choices=ie_list, default=0, coerce=int)
    application = SelectMultipleField(lazy_gettext('Application'))
    # FACILITY
    facility_ie = RadioField('FacilityIE', choices=ie_list, default=0, coerce=int)
    facility = SelectMultipleField(lazy_gettext('Facility'))
    # PRIORITY
    priority_ie = RadioField('PriorityIE', choices=ie_list, default=0, coerce=int)
    priority = SelectMultipleField(lazy_gettext('Priority'), choices=priority_list, coerce=int)
    # DATETIME (%Y-%m-%d %H:%M:%S)
    date_from = DateTimeField(lazy_gettext('From'), [validators.optional()], format=DATETIME_FORMAT)
    date_to = DateTimeField(lazy_gettext('To'), [validators.optional()], format=DATETIME_FORMAT)

    # RECORDS PER PAGE
    records_per_page = SelectField(lazy_gettext('Records'),
                                   choices=[(i, i) for i in (10, 25, 50, 100, 500)],
                                   coerce=int,
                                   default=25)

    # SORT DIRECTION - index - MongoDB sort style
    sort_direction = SelectField(lazy_gettext('Sort'), choices=sort_list, coerce=int, default=-1)

    # SEARCH STRING (regexp)
    search_str = StringField(lazy_gettext('Msg'))

    # PAGE NUMBER
    # hidden field has coerce=string - this cannot be changed
    # use int() in views to work with
    current_page = HiddenField('CurrentPage', default=1)

    # WATCH (auto refresh page)
    watch = HiddenField('Watch', default=0)

    # select fields with dynamic lists
    @classmethod
    def new(cls):
        form = cls()
        form.host.choices = sorted([(j, j) for j in db_get_hosts()])
        form.application.choices = sorted([(j, j) for j in db_get_applications()])
        form.facility.choices = sorted([(j, j) for j in db_get_facility()])
        return form


class RegistrationForm(Form):
    # FIXME (IL) - 'username' - same field as in LoginForm. If registration fails username restored in both forms
    username = StringField(lazy_gettext('Username'), [validators.DataRequired(),
                           validators.Length(min=3)])
    password = PasswordField(lazy_gettext('Password'), [validators.DataRequired(),
                             validators.equal_to('confirm', message=lazy_gettext('Passwords must match.')),
                             validators.Length(min=6, max=20)])
    confirm = PasswordField(lazy_gettext('Confirm password'), [validators.DataRequired()])
    email = StringField(lazy_gettext('Email'), [validators.DataRequired(),
                        validators.Length(min=4)])


class LoginForm(Form):
    username = StringField(lazy_gettext('Login'), [validators.DataRequired()])
    password = PasswordField(lazy_gettext('Password'), [validators.DataRequired()])
    remember_me = BooleanField(lazy_gettext('Remember me'), default=False)
