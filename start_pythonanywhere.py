#!/usr/bin/env python3
"""
PythonAnywhere startup script
This script handles Django startup on PythonAnywhere
"""

import os
import sys
import django
from django.conf import settings

# Add project to Python path
sys.path.insert(0, '/home/apknation/agriculture-project-/backend')

# Set environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings_production')

# Setup Django
django.setup()

# Print startup info
print("🚀 Django application starting...")
print(f"📁 Project path: /home/apknation/agriculture-project-/backend")
print(f"⚙️ Settings: {os.environ.get('DJANGO_SETTINGS_MODULE')}")
print(f"🌐 Debug mode: {getattr(settings, 'DEBUG', 'Unknown')}")
print(f"🔗 Allowed hosts: {getattr(settings, 'ALLOWED_HOSTS', [])}")
print(f"🌍 CORS origins: {getattr(settings, 'CORS_ALLOWED_ORIGINS', [])}")
print("✅ Django application ready!")
