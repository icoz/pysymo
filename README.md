# README for pysymo

Version 0.1

Syslog mongodb analyzer

https://github.com/icoz/pysymo

## Requirements

- Python 2/3
- Python packages: 
    Flask, Flask-WTF, Jinja2, WTForms - flask base 
    pymongo                           - work with MongoDB 
    chartkick                         - create charts
    flup                              - run pysymo via fcgi
    flask-paginate                    - output data pagination
    flask-login                       - user login
    pycrypto                          - password protection
- MongoDB
- Web-server
- Linux logging system (syslog-ng, ...)

## Summary

Pysymo is a web-interface for view and analyze syslog data, stored in MongoDB. There are two main things:
 
- Store syslog data in MongoDB. Different discributions use different logging system (SUSE - syslog-ng, 
  Arch - journald, Ubuntu - rsyslog). So you need a way to write to MongoDB from your syslog system 
  by piper script or by MongoDB driver built-in in you syslog system.
- View stored data by web-interface based on Flask. You can use any web-server you like. 
   

## Installation

1. Install requirements
2. Config MongoDB database
    - Change MONGO_DATABASE in *app/db.py*, *tools/config.py* if necessary
    - Init database using *tools/initdb.py*
3. Config AppArmor (if exists). See example in *examples/sbin.syslog-ng*
4. Config logging system to store in MongoDB. See example for syslog-ng 2.x in *examples/syslog-ng.conf*
5. Config web-server to run pysymo.fcgi. See example for lighttpd in *examples/fastcgi.conf* 
6. Set permissions for logging directory (see config['PYSYMO_LOG']) to web-server
7. Config crontab to run periodic tasks: *refresh_cache.py*, *refresh_charts.py*

## Directories and files

- /app/ - flask app
- /examples/ - configuration exaples
- /tools/ - tools scripts
    - config.py - config for scripts
    - initdb.py - db init script, creates collections and indexes. Use once during installation.
    - refresh_cache.py - caching script, creates lists of hosts, facilities displayed in web-interface. Use in crontab
    - refresh_charts.py - chart script, aggregates data to create charts. Use in crontab
    - syslog-ng_piper.py - sctipt to store syslog-ng data to MongoDB. Use with syslog-ng 2.x
- config.py - main config
- pysymo.fcgi - run pysymo with web-server
- run.py - run pysymo standalone on localhost

## Links

Syslog protocol RFC - http://tools.ietf.org/html/rfc5424

Sylog-ng OSE - http://www.balabit.com/sites/default/files/documents/syslog-ng-ose-3.3-guides/en/syslog-ng-ose-v3.3-guide-admin-en/html/index.html