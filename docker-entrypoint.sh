#!/bin/sh

flask db upgrade

exec gunicorn --capture-output --enable-stdio-inheritance --bind 0.0.0.0:80 "app:create_app()"