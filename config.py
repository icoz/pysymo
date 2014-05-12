# -*- coding: utf-8 -*-
__author__ = 'ilya-il'

'''
    http://www.balabit.com/sites/default/files/documents/syslog-ng-ose-3.3-guides/en/syslog-ng-ose-v3.3-guide-admin-en/html/reference_macros.html
    DB Format
        id       - ModgoDB ID
        host     - $HOST     - The name of the source host where the message originates from.
        facility - $FACILITY - The name of the facility (for example, kern) that sent the message.
        priority - $PRIORITY - The priority (also called severity) of the message, for example, error.
        datetime - $UNIXTIME - message time (eg. $UNIXTIME)
        program  - $PROGRAM  - The name of the program sending the message.
                   Note that the content of the $PROGRAM variable may not be completely trusted as it is provided
                   by the client program that constructed the message.
        msg      - $MSG      -  Text contents of the log message without the program name and pid.
                   Note that this has changed in syslog-ng version 3.0; in earlier versions this macro included the
                   program name and the pid. In syslog-ng 3.0, the MSG macro became equivalent with the MSGONLY macro.
                   The program name and the pid together are available in the MSGHDR macro.
'''
# priority list, constant
MSG_PRIORITY_LIST = ('alert', 'crit', 'debug', 'err', 'info', 'notice', 'warning', 'emerg')
# ('emerg', 'alert', 'crit', 'err', 'warn', 'notice', 'info', 'debug')
