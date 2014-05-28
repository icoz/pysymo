README for pysymo
=================

Version 0.1

Syslog-ng mongodb analyzer

https://github.com/icoz/pysymo

Requirements
------------

- Python 2/3
- Python packages: Flask, Flask-WTF, Jinja2, WTForms, pymongo, chartkick, flup
- MongoDB
- Web-server

Summary
-------

Pysymo is a web-interface for view and analyze syslog data, stored in MongoDB.
Storing is provided by Syslog-ng.

Installing
----------

1. Config MongoDB database. Change MONGO_DATABASE in app/db.py if necessary
2. Config Syslog-ng. See example in examples/syslog-ng.conf
2.1. Config AppArmor (if exists). See example in examples/sbin.syslog-ng
3. Config web-server to run pysymo.fcgi
3.1 Set permissions for logging directory (see config['PYSYMO_LOG']) to web-server