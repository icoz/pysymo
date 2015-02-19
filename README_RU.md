# README for pysymo

PySyMo (Python+Syslog+Mongodb) - это простой и приятный веб-интерфейс для просмотра и анализа журналов, аналогичный проекту [php-syslog-ng](https://code.google.com/p/php-syslog-ng/), но использующий mongodb в качестве базы данных и python в качестве языка программирования.
Главная цель проекта - возможность быстро (значительно быстрее, чем в php-syslog-ng) получать необходимые данные из централизованного журнала (syslog-ng), куда сохраняются данные с большого количества машин.

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
    - Babel, Flask-Babel                - i18n
- MongoDB
- Web-server
- Linux logging system (syslog-ng, ...)

## Краткое описание

Pysymo - веб-интерфейс для просмотра записей журналов, хранящихся в mongodb, с возможностью настройки фильтров по дате, времени, хосту, приложению, приоритету сообщения, тексту сообщения

Данные журналов сохраняются в mongodb. После чего по cron проводится их предварительная обработка. В дальнейшем эти данные можно быстро и просто просматривать и анализировать, применяя различные фильтры.
На текущий момент реализован сбор информации из syslog-ng, хранение и обработка данных в mongodb (вопросы настройки отказоустойчивой mongodb - за рамками данного проекта), серверная и клиентская части для просмотра журналов. Присутствует аутентификация пользователей: plain и ldap.
Pysymo использует Flask, так что в качестве веб-сервера вы можете использовать всё, на чем Flask может запуститься.

## Установка

1. Установите требуемый софт и пакеты python.
2. Настройте базу данных MongoDB.
    - Измените MONGO_DATABASE в *app/db.py*, *tools/config.py* если необходимо.
    - Инициализируейте базу данных используя *tools/initdb.py*.
    - Инициализируйте MEDB (базу данных с описанием сообщений) используя *tools/init_medb.py*.
3. Настройте LDAP в *config.py* если необходимо.
4. Настройте AppArmor (если он есть). Смотрите пример в *examples/apparmor/sbin.syslog-ng*.
5. Настройте систему логирования (syslog-ng, rsyslog и т.п.) на сохранение данных в MongoDB. 
    - пример для syslog-ng 2.x в *examples/syslog-ng-2.x/syslog-ng.conf*.
    - пример для syslog-ng 3.x в *examples/syslog-ng-3.x/syslog-ng.conf*.
    - пример для rsyslog в *examples/rsyslog/syslog-ng.conf*.
        - процесс syslog должен иметь права на выполнение piper-скрипта!
6. Настройте веб-сервер для запуска pysymo.fcgi. Смотрите пример для lighttpd in *examples/lighttps/fastcgi.conf* .
7. Настройте директорию для логов (config['PYSYMO_LOG'], tools/config['PYSYMO_ERROR_LOG']) и права на запись в нее для веб-сервера и процесса syslog.
8. Настройте crontab для выполнения периодических задач: *tools/refresh_cache.py*, *tools/refresh_charts.py*.

## Типы аутентификации

- plain - логин и пароль хранятся в MongoDB. Регистрация необходима и должна быть включена.
- ldap - логин и пароль хранятся в LDAP. Регистрация не требуется.

## LDAP

Для использования LDAP настройте параметры в *config.py*.
 
- LDAP_SERVER = 'ldap://[ldap_server]' (ex: 'ldap://ldap.office.mycompany.com')
- LDAP_SEARCH_BASE = '[organisation]' (ex: 'o=myorganisation')
- LDAP_SERVICE_USER = '[service_user_dn]' (ex: 'cn=pysymoauth,ou=myunit,o=myorganisation')
- LDAP_SERVICE_PASSWORD = '[password]'

## Описание структуры файлов и папок проекта

- /app/ - приложение flask
- /data/ - файлы с данными
- /examples/ - примеры настройки
- /tools/ - вспомогательные скрипты
    - config.py - настройки для скриптов
    - initdb.py - инициализация БД, создание коллекций и индексов. Используется однократно при установке.
    - init_medb.py - инициализация MEDB (база данных с описанием сообщений), создание коллекции 'medb' и заполнение данными из *data/medb.zip* file. Используется однократно при установке.
    - refresh_cache.py - скрипт создания кешей, списков хостов и т.п., используемых в веб-интерфейсе. Рекомендуется включить в crontab.
    - refresh_charts.py - скрипт, выполняющий предобработку данных, для последующего использования в отрисовке графиков. Рекомендуется включить в crontab.
    - syslog-ng_piper.py - скрипт сохранения данных syslog-ng в MongoDB. Требуется syslog-ng 2.x.
    - syslog-ng_piper2.py - скрипт сохранения данных syslog-ng в MongoDB. Требуется syslog-ng 2.x.
    - rsyslog_piper.py - скрипт сохранения данных rsyslog в MongoDB. Требуется rsyslog
- config.py - основной конфиг
- pysymo.fcgi - запуск pysymo средствами веб-сервера
- run.py - запуск pysymo в одиночном режиме на localhost

## Ссылки

Syslog protocol RFC - http://tools.ietf.org/html/rfc5424

Sylog-ng OSE - http://www.balabit.com/sites/default/files/documents/syslog-ng-ose-3.3-guides/en/syslog-ng-ose-v3.3-guide-admin-en/html/index.html

Bootstrap theme - http://bootswatch.com/spacelab/