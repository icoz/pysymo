# README for pysymo

PySyMo (Python+Syslog+Mongodb) - это простой и приятный веб-интерфейс для просмотра и анализа журналов, аналогичный проекту [phpsyslog-ng](https://code.google.com/p/php-syslog-ng/), только использующий mongodb в качестве базы данных и python в качестве языка программирования.
Главная цель проекта - возможность быстро (значительно быстрее, чем в phpsyslog-ng) получать необходимые данные из централизованного журнала (syslog-ng), куда сохраняются данные с большого количества машин.

https://github.com/icoz/pysymo

## Требования

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

## Краткое описание

Pysymo - веб-интерфейс для просмотра записей журналов, хранящихся в mongodb, с возможностью настройки фильтров по дате, времени, хосту, приложению, приоритету сообщения, тексту сообщения

Данные журналов сохраняются в mongodb. После чего по cron проводится их предварительная обработка. В дальнейшем эти данные можно быстро и просто просматривать и анализировать, применяя различные фильтры.
На текущий момент реализован сбор информации из syslog-ng, хранение и обработка данных в mongodb (вопросы настройки отказоустойчивой монги - за рамками данного проекта), серверная и клиентская части для просмотра журналов. Присутствует аутентификация пользователей: plain и ldap.
Pysymo использует Flask, так что в качестве веб-сервера вы можете использовать всё, на чем Flask может запуститься.

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

## Описание структуры файлов и папок проекта

- /app/ - приложение flask
- /examples/ - примеры настройки
- /tools/ - вспомогательные скрипты
    - config.py - настройки для скриптов
    - initdb.py - инициализация БД, создание коллекций и индексов. Используется однократно при установке.
    - refresh_cache.py - скрипт создания кешей, списков хостов и т.п., используемых в веб-интерфейсе. Рекомендуется включить в crontab.
    - refresh_charts.py - скрипт, выполняющий предобработку данных, для последующего использования в отрисовке диаграмм. Рекомендуется включить в crontab.
    - syslog-ng_piper.py - скрипт сохранения данных с центрального syslog-ng в MongoDB. Требуется syslog-ng 2.x.
- config.py - основной конфиг
- pysymo.fcgi - запуск pysymo средствами веб-сервера
- run.py - запуск pysymo в одиночном режиме на localhost

## Ссылки

Syslog protocol RFC - http://tools.ietf.org/html/rfc5424

Sylog-ng OSE - http://www.balabit.com/sites/default/files/documents/syslog-ng-ose-3.3-guides/en/syslog-ng-ose-v3.3-guide-admin-en/html/index.html

Bootstrap theme - http://bootswatch.com/spacelab/