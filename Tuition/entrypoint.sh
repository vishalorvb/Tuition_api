#!/bin/bash
set -e

# Run migrations
python manage.py makemigrations
python manage.py makemigrations Home
python manage.py makemigrations payment
python manage.py makemigrations Teacher
python manage.py makemigrations Tuitionmanager
python manage.py makemigrations usermanager
python manage.py migrate

# Start Gunicorn server
exec gunicorn --bind 0.0.0.0:8000 Tuition.wsgi:application
