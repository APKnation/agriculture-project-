#!/usr/bin/env python
import os
import sys
import django

# Setup Django
sys.path.append('/media/apknation/APKnation/PROJECT/VUE/agriculture/backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from market.models import Crop, User
from market.serializers import CropSerializer

def test_crop_creation():
    """Test crop creation without API"""
    print("🧪 Testing crop creation...")
    
    try:
        # Get or create a test user
        user, created = User.objects.get_or_create(
            username='testuser',
            defaults={
                'email': 'test@example.com',
                'role': 'farmer'
            }
        )
        print(f"✅ User: {user}")
        
        # Test crop creation
        crop_data = {
            'name': 'Test Crop',
            'type': 'vegetables',
            'status': 'planted',
            'description': 'Test description',
            'planting_date': '2024-01-15',
            'expected_harvest_date': '2024-04-15',
            'yield_estimate': 5.5,
            'farmer_id': user.id  # Fixed: Use farmer_id instead of farmer
        }
        
        serializer = CropSerializer(data=crop_data)
        if serializer.is_valid():
            crop = serializer.save()
            print(f"✅ Crop created: {crop}")
            print(f"✅ Crop ID: {crop.id}")
            print(f"✅ Crop type: {crop.type}")
            print(f"✅ Crop status: {crop.status}")
        else:
            print(f"❌ Serializer errors: {serializer.errors}")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        print(f"❌ Error type: {type(e)}")

if __name__ == '__main__':
    test_crop_creation()
