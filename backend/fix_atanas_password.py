#!/usr/bin/env python
"""
Script to fix password for user 'atanas'
"""

import os
import sys
import django

# Setup Django environment
sys.path.append('/media/apknation/APKnation/PROJECT/VUE/agriculture/backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from market.models import User

def fix_password():
    """Fix password for user 'atanas'"""
    print("🔧 Fixing password for user 'atanas'...")
    print("=" * 50)
    
    try:
        user = User.objects.get(username='atanas')
        print(f"✅ User found: {user.username} ({user.role})")
        
        # Set password properly
        user.set_password('1212')
        user.save()
        
        print("✅ Password updated successfully!")
        
        # Test the new password
        print(f"\n🔐 Testing new password '1212'...")
        if user.check_password('1212'):
            print("✅ Password verification: SUCCESS!")
        else:
            print("❌ Password verification: FAILED!")
            
        print(f"\n🎯 User 'atanas' can now login with:")
        print(f"   Username: atanas")
        print(f"   Password: 1212")
        print(f"   Role: {user.role}")
        print(f"   Expected redirect: /officer-dashboard")
            
    except User.DoesNotExist:
        print("❌ User 'atanas' does NOT exist!")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n" + "=" * 50)

if __name__ == '__main__':
    fix_password()
