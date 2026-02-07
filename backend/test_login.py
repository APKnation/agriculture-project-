#!/usr/bin/env python
"""
Script to create user 'anas' and test login functionality
"""

import os
import sys
import django

# Setup Django environment
sys.path.append('/media/apknation/APKnation/PROJECT/VUE/agriculture/backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from market.models import User
from django.contrib.auth import authenticate

def create_test_user():
    """Create user 'anas' if doesn't exist"""
    print("👤 Creating test user 'anas'...")
    
    if User.objects.filter(username='anas').exists():
        print("⚠️  User 'anas' already exists")
        user = User.objects.get(username='anas')
    else:
        print("✅ Creating new user 'anas'")
        user = User.objects.create_user(
            username='anas',
            password='1212',
            role='farmer',
            region='North',
            email='anas@example.com'
        )
        print(f"✅ User created: {user.username} (role: {user.role})")
    
    return user

def test_password_check():
    """Test password checking"""
    print("\n🔐 Testing password checking...")
    
    try:
        user = User.objects.get(username='anas')
        
        # Test 1: Direct password check
        print(f"📋 User found: {user.username}")
        print(f"🔐 Testing password '1212' directly...")
        
        if user.check_password('1212'):
            print("✅ Direct password check: SUCCESS")
        else:
            print("❌ Direct password check: FAILED")
            print("💡 This indicates password hashing issue!")
        
        # Test 2: Django authenticate
        print(f"\n🔐 Testing Django authenticate()...")
        auth_user = authenticate(username='anas', password='1212')
        
        if auth_user:
            print(f"✅ Django authenticate: SUCCESS ({auth_user.username})")
        else:
            print("❌ Django authenticate: FAILED")
            print("💡 This indicates authentication backend issue!")
            
        # Test 3: Wrong password
        print(f"\n🔐 Testing wrong password...")
        if user.check_password('wrongpassword'):
            print("❌ Wrong password check: UNEXPECTED SUCCESS")
        else:
            print("✅ Wrong password check: CORRECTLY FAILED")
            
    except User.DoesNotExist:
        print("❌ User 'anas' not found!")
    except Exception as e:
        print(f"❌ Error: {e}")

def main():
    """Main function"""
    print("🧪 Testing User Creation and Login")
    print("=" * 50)
    
    # Create user
    user = create_test_user()
    
    # Test password checking
    test_password_check()
    
    print("\n" + "=" * 50)
    print("🎯 Test completed!")
    print("If password check works but login fails, check:")
    print("1. Frontend request format")
    print("2. API endpoint configuration")
    print("3. Network/CORS issues")

if __name__ == '__main__':
    main()
