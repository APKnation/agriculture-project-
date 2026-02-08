#!/bin/bash

# Django startup script for Render
set -e

echo "🚀 Starting Django application..."

# Wait for database to be ready
echo "⏳ Waiting for database..."
python manage.py check --deploy

# Collect static files
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput --clear

# Run migrations
echo "🗄️ Running migrations..."
python manage.py migrate --noinput

# Start Gunicorn with error handling
echo "🌐 Starting Gunicorn..."
exec gunicorn \
    --bind :$PORT \
    --workers 1 \
    --threads 1 \
    --timeout 120 \
    --keep-alive 2 \
    --max-requests 1000 \
    --max-requests-jitter 50 \
    --preload \
    --access-logfile - \
    --error-logfile - \
    backend.wsgi:application
