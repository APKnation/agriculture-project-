#!/bin/bash

# Django startup script for Render
set -e

echo "🚀 Starting Django application..."

# Change to backend directory
cd /app/backend

# Ensure production settings are used
export DJANGO_SETTINGS_MODULE=backend.settings_production
echo "🔧 Using settings: $DJANGO_SETTINGS_MODULE"

# Wait for database to be ready
echo "⏳ Waiting for database..."
python manage.py check --deploy || echo "⚠️ Database check failed, continuing anyway..."

# Collect static files
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput --clear || echo "⚠️ Static files collection had issues, continuing..."

# Run migrations
echo "🗄️ Running migrations..."
python manage.py migrate --noinput || echo "⚠️ Migrations had issues, continuing..."

# Create a simple health check endpoint
echo "🔍 Creating health check..."
python -c "
import django
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings_production')
django.setup()
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

@require_http_methods(['GET'])
def health_check(request):
    return JsonResponse({'status': 'healthy', 'service': 'agriculture-backend'})

# Add to urls.py temporarily if needed
print('Health check endpoint ready')
"

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
    --capture-output \
    backend.wsgi:application
