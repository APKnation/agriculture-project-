#!/bin/bash
# Agriculture Management System Deployment Script

echo "🚀 Starting Agriculture Management System Deployment..."

# Backend Setup
echo "📦 Setting up backend..."
cd backend

# Install dependencies
pip install django djangorestframework djangorestframework-simplejwt django-cors-headers django-filter pillow

# Database migrations
python manage.py migrate

# Create superuser if needed
python manage.py shell -c "
from market.models import User
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print('Admin user created')
"

# Start backend server
echo "🖥️ Starting backend server..."
python manage.py runserver 8003 &
BACKEND_PID=$!

# Frontend Setup
echo "📦 Setting up frontend..."
cd ../frontend

# Install dependencies
npm install

# Start frontend server
echo "🌐 Starting frontend server..."
npm run dev &
FRONTEND_PID=$!

echo "✅ Deployment complete!"
echo "🔗 Frontend: http://localhost:5173"
echo "🔗 Backend: http://127.0.0.1:8003"
echo "👤 Admin login: admin / admin123"
echo "👤 Test user: apk / password123"

# Wait for user input to stop
echo "Press Ctrl+C to stop servers"
wait $BACKEND_PID $FRONTEND_PID
