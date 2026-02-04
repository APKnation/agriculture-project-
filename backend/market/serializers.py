from rest_framework import serializers
from .models import User, Crop, PriceRecord, Notification, PriceAlert, MarketPost


# =========================
# Crop Serializer
# =========================
class CropSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crop
        fields = [
            'id',
            'name',
            'description',
            'planting_date',
            'expected_harvest_date',
            'yield_estimate',
            'farmer'
        ]


# =========================
# User Serializer
# =========================
class UserSerializer(serializers.ModelSerializer):
    # Include crops owned by this user
    owned_crops = CropSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'password',
            'role',
            'region',
            'preferred_markets',
            'owned_crops'
        ]
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)  # hash password
        user.save()
        return user


# =========================
# Price Record Serializer
# =========================
class PriceRecordSerializer(serializers.ModelSerializer):
    crop = CropSerializer(read_only=True)

    class Meta:
        model = PriceRecord
        fields = ['id', 'crop', 'market', 'region', 'price', 'date']


# =========================
# Price Alert Serializer
# =========================
class PriceAlertSerializer(serializers.ModelSerializer):
    class Meta:
        model = PriceAlert
        fields = ['id', 'user', 'crop', 'target_price', 'active']


# =========================
# Notification Serializer
# =========================
class NotificationSerializer(serializers.ModelSerializer):
    crop = CropSerializer(read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = Notification
        fields = ['id', 'user', 'crop', 'message', 'created_at', 'read']


# =========================
# Farmer Marketplace Post Serializer
# =========================
class MarketPostSerializer(serializers.ModelSerializer):
    farmer_username = serializers.CharField(source='farmer.username', read_only=True)
    crop_name = serializers.CharField(source='crop.name', read_only=True)

    class Meta:
        model = MarketPost
        fields = ['id', 'farmer', 'farmer_username', 'crop', 'crop_name', 'quantity', 'price', 'contact']
