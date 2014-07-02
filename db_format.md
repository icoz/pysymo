# DB Format

## Collection 'messages'

* h = host     (string)
* f = facility (string)
* p = priority (integer, 0-7)
* d = datetime (unix timestamp)
* a = program  (string)
* m = msg      (string)

## Collection 'messages' fields to syslog macro

Reference - http://www.balabit.com/sites/default/files/documents/syslog-ng-ose-3.3-guides/en/syslog-ng-ose-v3.3-guide-admin-en/html/reference_macros.html

* h - $HOST      - The name of the source host where the message originates from.
* f - $FACILITY  - The name of the facility (for example, kern) that sent the message.
* p - $LEVEL_NUM - The priority (also called severity) of the message, for example, error.
* d - $UNIXTIME  - message time
* a - $PROGRAM   - The name of the program sending the message.
                   Note that the content of the $PROGRAM variable may not be completely trusted as it is provided
                   by the client program that constructed the message.
* m - $MSGONLY   - Text contents of the log message without the program name and pid.

## Collection 'cache'

* type: h/f/a - host, facility, application - UNIQUE
* value: list of distinct values - ["value1", "value2", ]

## Collection 'charts'

* name: - chart name - UNIQUE
* title: - chart title
* created: - creation datetime
* chart: - chart string (as it should be in Highcharts.Chart(<chart>))

## Collection 'users'

* username - UNIQUE
* password
* salt
* email
