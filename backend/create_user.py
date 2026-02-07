#!/usr/bin/env python
"""
Simple script to create user 'anas' with proper password
"""

import os
import sys
import django

# Setup Django environment
sys.path.append('/media/apknation/APKnation/PROJECT/VUE/agriculture/backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from market.models import User

def main():
    print("👤 Creating user 'anas'...")
    
    # Delete existing user if exists
    if User.objects.filter(username='anas').exists():
        print("🗑️  Deleting existing user 'anas'...")
        User.objects.filter(username='anas').delete()
    
    # Create new user
    try:
        user = User.objects.create_user(
            username='anas',
            password='1212',
            role='farmer',
            region='North',
            email='anas@example.com'
        )
        print(f"✅ User created successfully!")
        print(f"   Username: {user.username}")
        print(f"   Role: {user.role}")
        print(f"   Region: {user.region}")
        print(f"   ID: {user.id}")
        
        # Test password immediately
        if user.check_password('1212'):
            print("✅ Password verification: SUCCESS")
        else:
            print("❌ Password verification: FAILED")
            
    except Exception as e:
        print(f"❌ Error creating user: {e}")

if __name__ == '__main__':
    main()
