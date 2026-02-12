#!/bin/bash

# PythonAnywhere Deployment Script
# Username: apknation
# Project: agriculture-project-

echo "🚀 Starting PythonAnywhere deployment for apknation..."

# Navigate to project directory
cd /home/apknation/agriculture-project-

# Pull latest changes from GitHub
echo "📥 Pulling latest changes from GitHub..."
git pull origin main

# Navigate to backend
cd backend

# Set correct working directory for PythonAnywhere
echo "📁 Setting working directory..."
export PYTHONPATH=/home/apknation/agriculture-project-:$PYTHONPATH

# Install/Update dependencies
echo "📦 Installing Python dependencies..."
pip install -r requirements_pythonanywhere.txt

# Collect static files
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput

# Run migrations
echo "🗄️ Running database migrations..."
python manage.py migrate

# Create superuser if doesn't exist
echo "👤 Creating superuser (if needed)..."
python manage.py shell -c "
from django.contrib.auth.models import User
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print('Superuser created: admin/admin123')
else:
    print('Superuser already exists')
"

# Restart PythonAnywhere web app
echo "🔄 Restarting web application..."
touch /var/www/apknation_pythonanywhere_com_wsgi.py

echo "✅ Deployment completed successfully!"
echo "🌐 Your app is available at: https://apknation.pythonanywhere.com"
echo "🔧 Admin panel: https://apknation.pythonanywhere.com/admin/"
