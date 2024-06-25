# python_django_2024

[![](https://img.shields.io/badge/Python-3.12.3-yellow.svg)](https://www.python.org/downloads/) [![](https://img.shields.io/badge/Docker-blue.svg)](https://www.docker.com/) [![](https://img.shields.io/badge/Bitnami-MySQL-red.svg)](https://hub.docker.com/r/bitnami/mysql) [![](https://img.shields.io/badge/Django-5.0.6-green.svg)](https://www.djangoproject.com/) 

Revisiting Django in 2024.

Primarily looking at configuration.

> Forewarning: obviously don't use this in Production!

## Use

```bash
docker-compose up
```

> When's all done you should see the default Django view: http://127.0.0.1:8000/

## Discussion

Initialization:

```bash
python3 --version
python3 -m pip install Django
django-admin startproject djangoexample
```

Most people seem to move **Application Configuration** into it's own **Module** [like so](./django/djangoexample/config/).

A lot of examples use PyMySQL but [this article](https://adamj.eu/tech/2020/02/04/how-to-use-pymysql-with-django/) gives great reasons why one should avoid that and just use the out of the box connector and drivers (e.g. - `mysqlclient`).

The above works using fairly paradigmatic config:

```python
DATABASES = {
    'default': {
        "ENGINE": "django.db.backends.mysql",
        'NAME': 'example',
        'USER': 'example',
        'PASSWORD': 'example',
        'HOST': 'mysql',
        'PORT': '3306',
    }
}
```

A lot of folks encounter timing issues especially when dealing with Dockerized Containers:

```bash
#!/usr/bin/env bash

sleep 60

echo "Migrating DB and running server"

sleep 15 && python3 manage.py makemigrations && python3 manage.py migrate && python3 manage.py runserver 0.0.0.0:8000 &

wait
```

Django will spin up immediately and attempt to `migrate` - the success of those `migrations` determines whether the app will actually serve. 

> The easiest and least janky way I've seen to address that is to fork the Bash process and impose timer within the script that way the Container can spin up and initialization before it executes any `migration`. That has many advantages over using like Docker `health_checks` (awkward command-based `test` field, timing, and so on).

Without the `sleep` command you'd see:

```bash
MySQLdb.OperationalError: (2002, "Can't connect to server on 'mysql' (115)")
```
```bash
 MySQLdb.OperationalError: (2002, "Can't connect to local server through socket '/run/mysqld/mysqld.sock' (2)")
django-1  |
django-1  | The above exception was the direct cause of the following exception:
django-1  |
django-1  | Traceback (most recent call last):
django-1  |   File "/app/manage.py", line 22, in <module>
django-1  |     main()
django-1  |   File "/app/manage.py", line 18, in main
django-1  |     execute_from_command_line(sys.argv)
django-1  |   File "/usr/local/lib/python3.12/site-packages/django/core/management/__init__.py", line 442, in execute_from_command_line
django-1  |     utility.execute()
django-1  |   File "/usr/local/lib/python3.12/site-packages/django/core/management/__init__.py", line 436, in execute
django-1  |     self.fetch_command(subcommand).run_from_argv(self.argv)
django-1  |   File "/usr/local/lib/python3.12/site-packages/django/core/management/base.py", line 413, in run_from_argv
django-1  |     self.execute(*args, **cmd_options)
django-1  |   File "/usr/local/lib/python3.12/site-packages/django/core/management/base.py", line 459, in execute
django-1  |     output = self.handle(*args, **options)
django-1  |              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
django-1  |   File "/usr/local/lib/python3.12/site-packages/django/core/management/base.py", line 107, in wrapper
django-1  |     res = handle_func(*args, **kwargs)
django-1  |           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
django-1  |   File "/usr/local/lib/python3.12/site-packages/django/core/management/commands/migrate.py", line 100, in handle
django-1  |     self.check(databases=[database])
django-1  |   File "/usr/local/lib/python3.12/site-packages/django/core/management/base.py", line 486, in check
django-1  |     all_issues = checks.run_checks(
django-1  |                  ^^^^^^^^^^^^^^^^^^
django-1  |   File "/usr/local/lib/python3.12/site-packages/django/core/checks/registry.py", line 88, in run_checks
django-1  |     new_errors = check(app_configs=app_configs, databases=databases)
django-1  |                  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
```
Again the `sleep` command prevents connection issues and `migration` timing effects.

Also, make sure to bind the Database and server correctly:

* [Here - `settings.py`](django/djangoexample/config/settings.py)
* [Here - `run.sh`](django/run.sh)

## Resources and Links

1. https://docs.djangoproject.com/en/5.0/intro/tutorial01/
2. https://docs.djangoproject.com/en/5.0/ref/django-admin/#runserver
3. https://medium.com/@omaraamir19966/connect-django-with-mysql-database-f946d0f6f9e3
