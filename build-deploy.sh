#!/bin/bash

# Build script for Render deployment
echo "🚀 Starting deployment preparation..."

# Backend setup
echo "📦 Setting up backend..."
cd backend

# Install dependencies
echo "📥 Installing Python dependencies..."
pip install -r requirements.txt

# Collect static files
echo "🗂️  Collecting static files..."
python manage.py collectstatic --noinput --settings backend.settings_production

# Run migrations
echo "🔄 Running database migrations..."
python manage.py migrate --settings backend.settings_production

# Create superuser (optional - uncomment if needed)
# echo "👤 Creating superuser..."
# echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'admin@example.com', 'admin123')" | python manage.py shell --settings backend.settings_production

cd ..

# Frontend setup
echo "🎨 Setting up frontend..."
cd frontend

# Install dependencies
echo "📥 Installing Node.js dependencies..."
npm install

# Build for production
echo "🏗️  Building frontend for production..."
npm run build

cd ..

echo "✅ Deployment preparation complete!"
echo "📋 Summary:"
echo "   - Backend dependencies installed"
echo "   - Static files collected"
echo "   - Database migrations applied"
echo "   - Frontend built for production"
echo ""
echo "🎯 Ready for deployment to Render!"
