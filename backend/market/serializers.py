from rest_framework import serializers
from .models import User, Crop, PriceRecord, Notification, PriceAlert, MarketPost, CropDocument


# =========================
# Crop Document Serializer
# =========================
class CropDocumentSerializer(serializers.ModelSerializer):
    file_size_display = serializers.SerializerMethodField()
    
    class Meta:
        model = CropDocument
        fields = [
            'id', 'crop', 'title', 'file', 'uploaded_at', 
            'file_type', 'file_size', 'file_size_display'
        ]
        read_only_fields = ['uploaded_at', 'file_type', 'file_size']
    
    def get_file_size_display(self, obj):
        if obj.file_size:
            # Convert bytes to human readable format
            size = obj.file_size
            for unit in ['B', 'KB', 'MB', 'GB']:
                if size < 1024.0:
                    return f"{size:.1f} {unit}"
                size /= 1024.0
            return f"{size:.1f} TB"
        return "Unknown"


# =========================
# Crop Serializer
# =========================
class CropSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    documents = CropDocumentSerializer(many=True, read_only=True)
    farmer_username = serializers.CharField(source='farmer.username', read_only=True)
    
    class Meta:
        model = Crop
        fields = [
            'id',
            'name',
            'type',
            'status',
            'description',
            'planting_date',
            'expected_harvest_date',
            'yield_estimate',
            'farmer',
            'farmer_id',
            'farmer_username',
            'image',
            'image_url',
            'documents'
        ]
        extra_kwargs = {
            'farmer': {'required': False},
            'planting_date': {'required': False},
            'expected_harvest_date': {'required': False},
            'yield_estimate': {'required': False},
            'description': {'required': False},
            'image': {'required': False}
        }
    
    def get_image_url(self, obj):
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return None


# =========================
# User Serializer
# =========================
class UserSerializer(serializers.ModelSerializer):
    # Include crops owned by this user
    owned_crops = CropSerializer(many=True, read_only=True)
    profile_image_url = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'password',
            'role',
            'region',
            'preferred_markets',
            'profile_image',
            'profile_image_url',
            'owned_crops'
        ]
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': True},
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    def get_profile_image_url(self, obj):
        if obj.profile_image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.profile_image.url)
            return obj.profile_image.url
        return None

    def create(self, validated_data):
        # Hash the password before creating the user
        password = validated_data.pop('password', None)
        user = User.objects.create_user(**validated_data)
        if password:
            user.set_password(password)
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
