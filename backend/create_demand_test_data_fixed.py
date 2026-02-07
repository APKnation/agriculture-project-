#!/usr/bin/env python
"""
Script to create test demand data for the Supply & Demand Insights page
This creates realistic market activity to demonstrate the demand calculation system.
"""

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

def create_test_users():
    """Create test users if they don't exist"""
    users_data = [
        {'username': 'farmer1', 'password': 'farmer123', 'role': 'farmer', 'region': 'North'},
        {'username': 'farmer2', 'password': 'farmer123', 'role': 'farmer', 'region': 'South'},
        {'username': 'farmer3', 'password': 'farmer123', 'role': 'farmer', 'region': 'East'},
        {'username': 'officer1', 'password': 'officer123', 'role': 'officer', 'region': 'West'},
    ]
    
    for user_data in users_data:
        if not User.objects.filter(username=user_data['username']).exists():
            user = User.objects.create_user(
                username=user_data['username'],
                password=user_data['password'],
                role=user_data['role'],
                region=user_data['region']
            )
            print(f"✅ Created user: {user.username} ({user.role})")

def create_test_crops():
    """Create test crops"""
    crops_data = [
        {'name': 'Wheat', 'description': 'Premium wheat variety', 'planting_date': '2024-01-15'},
        {'name': 'Corn', 'description': 'Sweet corn variety', 'planting_date': '2024-02-20'},
        {'name': 'Tomatoes', 'description': 'Fresh tomatoes', 'planting_date': '2024-03-10'},
        {'name': 'Potatoes', 'description': 'Organic potatoes', 'planting_date': '2024-01-25'},
        {'name': 'Rice', 'description': 'Long grain rice', 'planting_date': '2024-02-05'},
        {'name': 'Onions', 'description': 'Yellow onions', 'planting_date': '2024-03-15'},
    ]
    
    for crop_data in crops_data:
        if not Crop.objects.filter(name=crop_data['name']).exists():
            crop = Crop.objects.create(
                name=crop_data['name'],
                description=crop_data['description'],
                planting_date=crop_data['planting_date']
            )
            print(f"✅ Created crop: {crop.name}")

def create_test_market_posts():
    """Create test market posts (supply indicators)"""
    farmers = User.objects.filter(role='farmer')
    crops = Crop.objects.all()
    
    market_posts_data = [
        {'farmer': 'farmer1', 'crop': 'Wheat', 'quantity': 500, 'price': 2.50, 'contact': 'farmer1@market.com'},
        {'farmer': 'farmer2', 'crop': 'Corn', 'quantity': 300, 'price': 3.20, 'contact': 'farmer2@market.com'},
        {'farmer': 'farmer3', 'crop': 'Tomatoes', 'quantity': 200, 'price': 1.80, 'contact': 'farmer3@market.com'},
        {'farmer': 'farmer1', 'crop': 'Potatoes', 'quantity': 150, 'price': 1.20, 'contact': 'farmer1@market.com'},
        {'farmer': 'farmer2', 'crop': 'Rice', 'quantity': 400, 'price': 2.80, 'contact': 'farmer2@market.com'},
        {'farmer': 'farmer3', 'crop': 'Onions', 'quantity': 100, 'price': 1.50, 'contact': 'farmer3@market.com'},
    ]
    
    for post_data in market_posts_data:
        farmer = farmers.get(username=post_data['farmer'])
        crop = crops.get(name=post_data['crop'])
        
        if farmer and crop:
            MarketPost.objects.create(
                farmer=farmer,
                crop=crop,
                quantity=post_data['quantity'],
                price=post_data['price'],
                contact=post_data['contact']
            )
            print(f"✅ Created market post: {farmer.username} selling {crop.name}")

def create_test_price_alerts():
    """Create test price alerts (demand indicators)"""
    users = User.objects.filter(role='farmer')
    crops = Crop.objects.all()
    
    price_alerts_data = [
        {'user': 'farmer1', 'crop': 'Wheat', 'target_price': 3.00},  # High demand for wheat
        {'user': 'farmer2', 'crop': 'Corn', 'target_price': 3.50},  # High demand for corn
        {'user': 'farmer3', 'crop': 'Tomatoes', 'target_price': 2.00},  # Moderate demand for tomatoes
        {'user': 'farmer1', 'crop': 'Potatoes', 'target_price': 1.50},  # Low demand for potatoes
        {'user': 'farmer2', 'crop': 'Rice', 'target_price': 2.50},  # Moderate demand for rice
        {'user': 'farmer3', 'crop': 'Onions', 'target_price': 1.80},  # Low demand for onions
    ]
    
    for alert_data in price_alerts_data:
        user = users.get(username=alert_data['user'])
        crop = crops.get(name=alert_data['crop'])
        
        if user and crop:
            PriceAlert.objects.create(
                user=user,
                crop=crop,
                target_price=alert_data['target_price'],
                active=True
            )
            print(f"✅ Created price alert: {user.username} for {crop.name} at ${alert_data['target_price']}")

def create_test_price_records():
    """Create test price records (market activity indicators)"""
    users = User.objects.filter(role='farmer')
    crops = Crop.objects.all()
    
    # Create price records to show market activity
    import random
    from datetime import datetime, timedelta
    
    for crop in crops:
        user = random.choice(users.filter(region__in=['North', 'South', 'East', 'West']))
        
        # Create multiple price records per crop to show activity
        for i in range(random.randint(5, 15)):  # 5-15 records per crop
            days_ago = random.randint(1, 30)
            record_date = datetime.now() - timedelta(days=days_ago)
            
            markets = ['N', 'S', 'E', 'W', 'C']  # North, South, East, West, Central
            market = random.choice(markets)
            
            # Vary prices by market
            base_price = {
                'Wheat': 2.20 + random.uniform(-0.30, 0.30),
                'Corn': 3.00 + random.uniform(-0.40, 0.40),
                'Tomatoes': 1.60 + random.uniform(-0.20, 0.20),
                'Potatoes': 1.10 + random.uniform(-0.15, 0.15),
                'Rice': 2.40 + random.uniform(-0.30, 0.30),
                'Onions': 1.30 + random.uniform(-0.20, 0.20),
            }
            
            price = round(base_price[crop.name] + random.uniform(-0.20, 0.20), 2)
            
            PriceRecord.objects.create(
                crop=crop,
                user=user,
                market=market,
                price=price,
                date=record_date
            )
        
        print(f"✅ Created {PriceRecord.objects.filter(crop=crop).count()} price records for {crop.name}")

def main():
    """Main function to create all test data"""
    print("🌱 Creating test demand data...")
    print("=" * 50)
    
    print("1️⃣ Creating test users...")
    create_test_users()
    
    print("\n2️⃣ Creating test crops...")
    create_test_crops()
    
    print("\n3️⃣ Creating market posts (supply indicators)...")
    create_test_market_posts()
    
    print("\n4️⃣ Creating price alerts (demand indicators)...")
    create_test_price_alerts()
    
    print("\n5️⃣ Creating price records (market activity indicators)...")
    create_test_price_records()
    
    print("\n" + "=" * 50)
    print("🎯 Test data creation complete!")
    print("\n📊 Demand Data Summary:")
    print("   • Market Posts: Supply indicators (farmers selling crops)")
    print("   • Price Alerts: Demand indicators (farmers setting target prices)")
    print("   • Price Records: Market activity indicators (historical pricing data)")
    print("\n🚀 Now you can test the Demand Insights page!")
    print("   The demand levels are calculated based on:")
    print("   - Market posts (supply count)")
    print("   - Price alerts (demand indicators)")
    print("   - Price records (market activity)")

if __name__ == '__main__':
    main()
