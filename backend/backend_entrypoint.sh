#!/bin/sh
python manage.py makemigrations

python manage.py migrate

python manage.py collectstatic --noinput

cp -r collected_static/. /backend_static/static/

DJANGO_SUPERUSER_PHONE="admin" \
DJANGO_SUPERUSER_PASSWORD="admin" \
python manage.py createsuperuser --noinput

gunicorn --reload -b 0.0.0.0:8000 referral_project.wsgi
