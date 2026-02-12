#!/usr/bin/env python3
"""
PythonAnywhere WSGI configuration for Django
Username: apknation
Project: agriculture-project-
"""

import os
import sys

# Add the project directory to the Python path
project_path = '/home/apknation/agriculture-project-/backend'
if project_path not in sys.path:
    sys.path.insert(0, project_path)

# Add the parent directory to the Python path (for imports)
parent_path = '/home/apknation/agriculture-project-'
if parent_path not in sys.path:
    sys.path.insert(0, parent_path)

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings_production')

# Import the Django WSGI application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

# Print debug information (remove in production)
print("WSGI application loaded successfully")
print(f"Project path: {project_path}")
print(f"Settings module: {os.environ.get('DJANGO_SETTINGS_MODULE')}")
