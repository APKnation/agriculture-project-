#!/usr/bin/env python
"""
Script to get all regions from the database with their associated crops
"""

import os
import sys
import django

# Setup Django environment
sys.path.append('/media/apknation/APKnation/PROJECT/VUE/agriculture/backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from market.models import Crop, PriceRecord, User

def get_regions_with_crops():
    """Get all regions that have crops and their associated crop data"""
    
    # Get unique regions from PriceRecords
    regions_with_data = PriceRecord.objects.values('region').distinct()
    
    regions_data = []
    for region_record in regions_with_data:
        region_name = region_record['region']
        
        # Get crops for this region
        crops_in_region = PriceRecord.objects.filter(region=region_name).values('crop__name').distinct()
        crop_list = [crop['crop__name'] for crop in crops_in_region]
        
        # Get latest price record for this region
        latest_record = PriceRecord.objects.filter(region=region_name).order_by('-timestamp').first()
        
        regions_data.append({
            'name': region_name,
            'crops': crop_list,
            'crop_count': len(crop_list),
            'latest_price': latest_record.price if latest_record else None,
            'latest_crop': latest_record.crop.name if latest_record else None
        })
    
    return regions_data

def main():
    """Main function to display regions data"""
    print("🌍 Fetching regions with crops from database...")
    print("=" * 50)
    
    regions = get_regions_with_crops()
    
    if not regions:
        print("❌ No regions found with crop data")
        return
    
    print(f"✅ Found {len(regions)} regions with crop data:")
    print()
    
    for i, region in enumerate(regions, 1):
        print(f"{i}. {region['name']}")
        print(f"   🌾 Crops: {', '.join(region['crops'])}")
        print(f"   📊 Crop Count: {region['crop_count']}")
        if region['latest_price']:
            print(f"   💰 Latest Price: {region['latest_price']} ({region['latest_crop']})")
        print()
    
    print("=" * 50)
    print("🎯 Regions data ready for WeatherDashboard!")
    print(f"   Total regions: {len(regions)}")
    print(f"   Total crops across all regions: {sum(r['crop_count'] for r in regions)}")
    
    # Export as JSON for frontend
    import json
    with open('/media/apknation/APKnation/PROJECT/VUE/agriculture/backend/regions_data.json', 'w') as f:
        json.dump(regions, f, indent=2)
    
    print("📁 Regions data exported to regions_data.json")

if __name__ == '__main__':
    main()
