from django.contrib import admin
from .models import User, Crop, PriceRecord, Notification

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'role', 'region', 'preferred_markets')
    search_fields = ('username', 'role', 'region', 'preferred_markets')
    list_filter = ('role', 'region')

@admin.register(Crop)
class CropAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'description',
        'planting_date',
        'expected_harvest_date',
        'yield_estimate',
        'farmer',   # ✅ show farmer here
    )
    search_fields = ('name', 'farmer__username')
    list_filter = ('planting_date', 'expected_harvest_date', 'farmer')

@admin.register(PriceRecord)
class PriceRecordAdmin(admin.ModelAdmin):
    list_display = ('crop', 'region', 'price', 'timestamp')
    search_fields = ('crop__name', 'region')
    list_filter = ('region', 'crop')

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'crop', 'message', 'created_at', 'read')
    search_fields = ('user__username', 'crop__name', 'message')
    list_filter = ('read', 'created_at')
