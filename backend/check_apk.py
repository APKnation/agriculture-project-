#!/usr/bin/env python
"""
Script to check if user 'apk' exists and test credentials
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
    """Check if user 'apk' exists and test password"""
    print("🔍 Checking user 'apk'...")
    print("=" * 50)
    
    try:
        user = User.objects.get(username='apk')
        print(f"✅ User found: {user.username}")
        print(f"📧 Email: {user.email}")
        print(f"👤 Role: {user.role}")
        print(f"🌍 Region: {user.region}")
        print(f"📅 Created: {user.date_joined}")
        
        # Test password (assuming password is '1212')
        print(f"\n🔐 Testing password '1212'...")
        if user.check_password('1212'):
            print("✅ Password matches!")
        else:
            print("❌ Password does NOT match!")
            print("💡 This is likely the login issue!")
            
    except User.DoesNotExist:
        print("❌ User 'apk' does NOT exist in database!")
        print("💡 Need to create this user first")
    
    # Show all users for comparison
    print(f"\n📋 All users in database:")
    all_users = User.objects.all()
    for u in all_users:
        print(f"   - {u.username} ({u.role})")
    
    print("\n" + "=" * 50)

if __name__ == '__main__':
    check_user()
