#!/bin/bash

echo "start migrations"
python manage.py makemigrations
echo "start migrate"
python manage.py migrate
echo "run server"
WORKERS_COUNT=50
gunicorn dano.wsgi:application -b 0.0.0.0:8000 --workers ${WORKERS_COUNT} -k gevent --log-level debug
