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
* m - $MSG       - Text contents of the log message without the program name and pid.
                   Note that this has changed in syslog-ng version 3.0; in earlier versions this macro included the
                   program name and the pid. In syslog-ng 3.0, the MSG macro became equivalent with the MSGONLY macro.
                   The program name and the pid together are available in the MSGHDR macro.

## Collection 'cache'

* type: h/f/a - host, facility, application - UNIQUE
* value: list of distinct values - ["value1", "value2", ]

## Collection 'charts'

* name: - chart name - UNIQUE
* type: - chart type - pie, column, bar, area, line
* title: - chart title
* created: - creation datetime
* data: - chart data - [['label', value], ['label', value], ]

## Collection 'users'

* username - UNIQUE
* password
* salt
* email
