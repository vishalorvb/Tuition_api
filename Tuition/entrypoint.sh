#!/bin/bash
set -e

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Start Gunicorn server
exec gunicorn --bind 0.0.0.0:8000 Tuition.wsgi:application
