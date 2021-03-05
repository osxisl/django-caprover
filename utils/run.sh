#!/bin/sh

python manage.py collectstatic --noinput
python manage.py migrate
django-admin compilemessages
gunicorn djangosite.wsgi --bind=0.0.0.0:8001