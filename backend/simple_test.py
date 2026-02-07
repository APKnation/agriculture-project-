#!/usr/bin/env python

import os
import sys
import django

# Setup Django environment
sys.path.append('/media/apknation/APKnation/PROJECT/VUE/agriculture/backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from market.models import User, Crop, MarketPost, PriceRecord, PriceAlert
from django.contrib.auth import get_user_model

User = get_user_model()

def main():
    """Simple test data creation"""
    print("Creating basic test data...")
    
    # Create test users
    if not User.objects.filter(username='farmer1').exists():
        user = User.objects.create_user(
            username='farmer1',
            password='farmer123',
            role='farmer',
            region='North'
        )
        print(f"✅ Created user: {user.username}")
    
    # Create test crops
    crop = None
    if not Crop.objects.filter(name='Wheat').exists():
        crop = Crop.objects.create(
            name='Wheat',
            description='Premium wheat variety',
            planting_date='2024-01-15'
        )
        print(f"✅ Created crop: {crop.name}")
    
    # Create market post
    if crop and not MarketPost.objects.filter(farmer__username='farmer1', crop__name='Wheat').exists():
        MarketPost.objects.create(
            farmer=user,
            crop=crop,
            quantity=500,
            price=2.50,
            contact='farmer1@market.com'
        )
        print("✅ Created market post for Wheat")
    
    # Create price alert
    if crop and not PriceAlert.objects.filter(user__username='farmer1', crop__name='Wheat').exists():
        PriceAlert.objects.create(
            user=user,
            crop=crop,
            target_price=3.00,
            active=True
        )
        print("✅ Created price alert for Wheat")
    
    # Create some price records
    if crop:
        for i in range(10):
            PriceRecord.objects.create(
                crop=crop,
                user=user,
                market='N',
                price=2.20 + (i * 0.1),
                date='2024-01-01'
            )
        
        print(f"✅ Created 10 price records for Wheat")
    
    print("\n🎯 Basic test data created successfully!")
    print("Now you can test the Demand Insights page")

if __name__ == '__main__':
    main()
