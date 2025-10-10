#!/bin/sh
set -e

echo "🟢 Running migrations..."
python manage.py migrate --noinput

echo "🟢 Collecting static files..."
python manage.py collectstatic --noinput

echo "🟢 Starting Django..."
# For production, replace with Gunicorn:
exec gunicorn config.wsgi:application \
    --bind 0.0.0.0:8112 \
    --workers 4 \
    --access-logfile - \
    --error-logfile - \
    --log-level debug \
    --capture-output

#exec python3 manage.py runserver 0.0.0.0:8112