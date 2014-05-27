DB Format
=========

Collection 'messages'
---------------------

* h = host
* f = facility
* p = priority (0-7)
* d = datetime (unix timestamp)
* a = program
* m = msg

Collection 'messages' fields to syslog macro
--------------------------------------------

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

Collection 'cache'
-----------------

* type: h/f/a - host, facility, application
* value: [] - list of distinct values


#For caching

##Collection date

##Collection servers

# Just for info
#define LOG_EMERG       0       /* system is unusable */
#define LOG_ALERT       1       /* action must be taken immediately */
#define LOG_CRIT        2       /* critical conditions */
#define LOG_ERR         3       /* error conditions */
#define LOG_WARNING     4       /* warning conditions */
#define LOG_NOTICE      5       /* normal but significant condition */
#define LOG_INFO        6       /* informational */
#define LOG_DEBUG       7       /* debug-level messages */

['emerg', 'alert', 'crit', 'err', 'warn', 'notice', 'info', 'debug']

CODE facilitynames[] = {
	"auth",		LOG_AUTH,
	"authpriv",	LOG_AUTHPRIV,
	"cron", 	LOG_CRON,
	"daemon",	LOG_DAEMON,
	"kern",		LOG_KERN,
	"lpr",		LOG_LPR,
	"mail",		LOG_MAIL,
	"mark", 	INTERNAL_MARK,		/* INTERNAL */
	"news",		LOG_NEWS,
	"security",	LOG_AUTH,		/* DEPRECATED */
	"syslog",	LOG_SYSLOG,
	"user",		LOG_USER,
	"uucp",		LOG_UUCP,
	"local0",	LOG_LOCAL0,
	"local1",	LOG_LOCAL1,
	"local2",	LOG_LOCAL2,
	"local3",	LOG_LOCAL3,
	"local4",	LOG_LOCAL4,
	"local5",	LOG_LOCAL5,
	"local6",	LOG_LOCAL6,
	"local7",	LOG_LOCAL7,
	NULL,		-1,
};