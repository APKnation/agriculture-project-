from django.contrib import admin
from .models import User, Crop, PriceRecord, Notification, PriceAlert, MarketPost

# -----------------------------
# User Admin
# -----------------------------
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'role', 'region', 'preferred_markets')
    search_fields = ('username', 'role', 'region', 'preferred_markets')
    list_filter = ('role', 'region')


# -----------------------------
# Crop Admin
# -----------------------------
@admin.register(Crop)
class CropAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'description',
        'planting_date',
        'expected_harvest_date',
        'yield_estimate',
        'farmer',
    )
    search_fields = ('name', 'farmer__username')
    list_filter = ('planting_date', 'expected_harvest_date', 'farmer')


# -----------------------------
# Price Record Admin
# -----------------------------
@admin.register(PriceRecord)
class PriceRecordAdmin(admin.ModelAdmin):
    list_display = ('crop', 'market', 'region', 'price', 'date')
    search_fields = ('crop__name', 'region', 'market')
    list_filter = ('region', 'crop', 'market')


# -----------------------------
# Notification Admin
# -----------------------------
@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'crop', 'message', 'created_at', 'read')
    search_fields = ('user__username', 'crop__name', 'message')
    list_filter = ('read', 'created_at')


# -----------------------------
# Price Alert Admin
# -----------------------------
@admin.register(PriceAlert)
class PriceAlertAdmin(admin.ModelAdmin):
    list_display = ('user', 'crop', 'target_price', 'active')
    search_fields = ('user__username', 'crop__name')
    list_filter = ('active',)


# -----------------------------
# Farmer Marketplace Post Admin
# -----------------------------
@admin.register(MarketPost)
class MarketPostAdmin(admin.ModelAdmin):
    list_display = ('farmer', 'crop', 'quantity', 'price', 'contact')
    search_fields = ('farmer__username', 'crop__name', 'contact')
    list_filter = ('crop',)
