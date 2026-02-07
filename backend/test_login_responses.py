#!/usr/bin/env python
"""
Script to test login responses for both users
"""

import os
import sys
import django
import json

# Setup Django environment
sys.path.append('/media/apknation/APKnation/PROJECT/VUE/agriculture/backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from market.views import login_view
from rest_framework.test import APIRequestFactory
from django.contrib.auth import get_user_model

User = get_user_model()

def test_login_response():
    """Test login response for both users"""
    factory = APIRequestFactory()
    
    print("🔍 Testing login responses...")
    print("=" * 60)
    
    # Test apk (farmer)
    print("\n📋 Testing 'apk' (farmer):")
    request = factory.post('/api/auth/login/', {
        'username': 'apk',
        'password': '1212'
    })
    
    try:
        response = login_view(request)
        response_data = response.data
        print(f"✅ Status: {response.status_code}")
        print(f"🔑 Token: {response_data.get('token', 'NOT FOUND')[:50]}...")
        print(f"👤 Role: {response_data.get('role', 'NOT FOUND')}")
        print(f"📊 User data keys: {list(response_data.get('user', {}).keys())}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test atanas (officer)
    print("\n📋 Testing 'atanas' (officer):")
    request = factory.post('/api/auth/login/', {
        'username': 'atanas',
        'password': '1212'
    })
    
    try:
        response = login_view(request)
        response_data = response.data
        print(f"✅ Status: {response.status_code}")
        print(f"🔑 Token: {response_data.get('token', 'NOT FOUND')[:50]}...")
        print(f"👤 Role: {response_data.get('role', 'NOT FOUND')}")
        print(f"📊 User data keys: {list(response_data.get('user', {}).keys())}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n" + "=" * 60)

if __name__ == '__main__':
    test_login_response()
