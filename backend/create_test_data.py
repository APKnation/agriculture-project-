#!/usr/bin/env python
import os
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from market.models import User, Crop, PriceRecord
from django.utils import timezone
from datetime import date, timedelta

# Create test users
farmer = User.objects.create_user('farmer1', 'farmer@example.com', 'farmer123', role='farmer', region='North')
officer = User.objects.create_user('officer1', 'officer@example.com', 'officer123', role='officer', region='South')

# Create test crops
crop1 = Crop.objects.create(name='Wheat', description='High quality wheat', farmer=farmer, planting_date=date.today() - timedelta(days=30), expected_harvest_date=date.today() + timedelta(days=60), yield_estimate=5.5)
crop2 = Crop.objects.create(name='Corn', description='Sweet corn variety', farmer=farmer, planting_date=date.today() - timedelta(days=15), expected_harvest_date=date.today() + timedelta(days=45), yield_estimate=8.2)

# Create test price records
PriceRecord.objects.create(crop=crop1, market='Central Market', region='North', price=250.50)
PriceRecord.objects.create(crop=crop2, market='South Market', region='South', price=180.75)
PriceRecord.objects.create(crop=crop1, market='East Market', region='East', price=265.25)

print("Test data created successfully!")
print(f"Users: {User.objects.count()}")
print(f"Crops: {Crop.objects.count()}")
print(f"Price records: {PriceRecord.objects.count()}")
