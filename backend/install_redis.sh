#!/bin/bash

echo "Installing Redis for Smart Agri-Market..."
echo "====================================="

# Update package list
echo "Updating package list..."
sudo apt update

# Install Redis server
echo "Installing Redis server..."
sudo apt install -y redis-server

# Start Redis server
echo "Starting Redis server..."
sudo systemctl start redis-server

# Enable Redis to start on boot
echo "Enabling Redis to start on boot..."
sudo systemctl enable redis-server

# Check Redis status
echo "Checking Redis status..."
sudo systemctl status redis-server

# Test Redis connection
echo "Testing Redis connection..."
redis-cli ping

echo ""
echo "Redis installation completed!"
echo "Now you can enable the full features by:"
echo "1. Uncomment 'channels' in INSTALLED_APPS in backend/settings.py"
echo "2. Uncomment ASGI_APPLICATION and CHANNEL_LAYERS in backend/settings.py"
echo "3. Restart the Django server"
echo ""
echo "Your Smart Agri-Market will then have:"
echo "- Real-time WebSocket notifications"
echo "- Advanced caching with Redis"
echo "- Better performance"
