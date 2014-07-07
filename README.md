# README for pysymo

PySyMo is a web-interface for view and analyze syslog data, stored in MongoDB.

https://github.com/icoz/pysymo

## Requirements

- Python => 2.6
- Python packages: 
    - Flask, Flask-WTF, Jinja2, WTForms - flask base 
    - pymongo                           - work with MongoDB 
    - flup                              - run pysymo via fcgi
    - flask-paginate (> 0.2)            - output data pagination
    - flask-login                       - user login
    - pycrypto                          - password protection
    - python-ldap                       - LDAP authentication
- MongoDB
- Web-server
- Linux logging system (syslog-ng, ...)

## Summary

Pysymo is a web-interface for view and analyze syslog data, stored in MongoDB. There are two main things:
 
- Store syslog data in MongoDB. Different distributions use different logging system (SUSE - syslog-ng, 
  Arch - journald, Ubuntu - rsyslog). So you need a way to write to MongoDB from your syslog system 
  by piper script or by MongoDB driver built-in in you syslog system.
- View stored data by web-interface based on Flask. You can use any web-server you like. 
   

## Installation

1. Install requirements.
2. Config MongoDB database.
    - Change MONGO_DATABASE in *app/db.py*, *tools/config.py* if necessary.
    - Init database using *tools/initdb.py*.
3. Config LDAP in *config.py* if necessary.
4. Config AppArmor (if exists). See example in *examples/sbin.syslog-ng*.
5. Config logging system to store in MongoDB. See example for syslog-ng 2.x in *examples/syslog-ng.conf*.
6. Config web-server to run pysymo.fcgi. See example for lighttpd in *examples/fastcgi.conf* .
7. Set permissions for logging directory (see config['PYSYMO_LOG']) to web-server.
8. Config crontab to run periodic tasks: *refresh_cache.py*, *refresh_charts.py*.

## Authentication types

- plain - user and password stored in MongoDB. Registration needed and must be enabled.
- ldap - user and password stored in LDAP. No registration needed.

## LDAP

If you want to use LDAP to authenticate users, you need to config some parameters in *config.py*.
 
- LDAP_SERVER = 'ldap://[ldap_server]' (ex: 'ldap://ldap.office.mycompany.com')
- LDAP_SEARCH_BASE = '[organisation]' (ex: 'o=myorganisation')
- LDAP_SERVICE_USER = '[service_user_dn]' (ex: 'cn=pysymoauth,ou=myunit,o=myorganisation')
- LDAP_SERVICE_PASSWORD = '[password]'

## Directories and files

- /app/ - flask app
- /examples/ - configuration examples
- /tools/ - tools scripts
    - config.py - config for scripts
    - initdb.py - db init script, creates collections and indexes. Use once during installation.
    - refresh_cache.py - caching script, creates lists of hosts, facilities displayed in web-interface. Use in crontab.
    - refresh_charts.py - chart script, aggregates data to create charts. Use in crontab.
    - syslog-ng_piper.py - script to store syslog-ng data to MongoDB. Use with syslog-ng 2.x.
- config.py - main config
- pysymo.fcgi - run pysymo with web-server
- run.py - run pysymo standalone on localhost

## Links

Syslog protocol RFC - http://tools.ietf.org/html/rfc5424

Sylog-ng OSE - http://www.balabit.com/sites/default/files/documents/syslog-ng-ose-3.3-guides/en/syslog-ng-ose-v3.3-guide-admin-en/html/index.html

Bootstrap theme - http://bootswatch.com/spacelab/