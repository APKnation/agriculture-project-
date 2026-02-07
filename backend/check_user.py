#!/usr/bin/env python
"""
Script to check if user 'anas' exists and debug login issues
"""

import os
import sys
import django

# Setup Django environment
sys.path.append('/media/apknation/APKnation/PROJECT/VUE/agriculture/backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from market.models import User

def check_user():
    """Check if user 'anas' exists and show details"""
    print("🔍 Checking user 'anas'...")
    print("=" * 50)
    
    try:
        user = User.objects.get(username='anas')
        print(f"✅ User found: {user.username}")
        print(f"📧 Email: {user.email}")
        print(f"👤 Role: {user.role}")
        print(f"🌍 Region: {user.region}")
        print(f"📅 Created: {user.date_joined}")
        
        # Test password
        print(f"\n🔐 Testing password '1212'...")
        if user.check_password('1212'):
            print("✅ Password matches!")
        else:
            print("❌ Password does NOT match!")
            print("💡 This is likely the login issue!")
        
        # Show all users for comparison
        print(f"\n📋 All users in database:")
        all_users = User.objects.all()
        for u in all_users:
            print(f"   - {u.username} ({u.role})")
            
    except User.DoesNotExist:
        print("❌ User 'anas' does NOT exist in database!")
        print("💡 Need to create this user first")
    
    print("\n" + "=" * 50)

if __name__ == '__main__':
    check_user()
