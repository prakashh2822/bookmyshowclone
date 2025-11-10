#!/usr/bin/env bash
set -e

# Run database migrations
python manage.py migrate --noinput

# Collect static files
python manage.py collectstatic --noinput

# Start server using gunicorn
gunicorn bms.wsgi:application --bind 0.0.0.0:$PORT
