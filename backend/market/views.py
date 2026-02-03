from rest_framework import viewsets, permissions
from .models import User, Crop, PriceRecord, Notification
from .serializers import UserSerializer, CropSerializer, PriceRecordSerializer, NotificationSerializer
from django.db.models import Avg
from rest_framework.decorators import action
from rest_framework.response import Response


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]  # ✅ public

    # Custom endpoint to get current user info (no auth, just returns first user for demo)
    @action(detail=False, methods=['get'])
    def me(self, request):
        # Without authentication, you can either return nothing or a default user
        user = User.objects.first()
        serializer = self.get_serializer(user)
        return Response(serializer.data)


class CropViewSet(viewsets.ModelViewSet):
    queryset = Crop.objects.all()
    serializer_class = CropSerializer
    permission_classes = [permissions.AllowAny]  # ✅ public

    def get_queryset(self):
        queryset = Crop.objects.all()
        farmer_id = self.request.query_params.get('farmer')
        if farmer_id:
            queryset = queryset.filter(farmer_id=farmer_id)
        # Removed request.user logic since no auth
        return queryset


class PriceRecordViewSet(viewsets.ModelViewSet):
    queryset = PriceRecord.objects.all().order_by('-timestamp')
    serializer_class = PriceRecordSerializer
    permission_classes = [permissions.AllowAny]  # ✅ public

    def get_queryset(self):
        queryset = PriceRecord.objects.all().order_by('-timestamp')
        crop_id = self.request.query_params.get('crop')
        region = self.request.query_params.get('region')
        if crop_id:
            queryset = queryset.filter(crop_id=crop_id)
        if region:
            queryset = queryset.filter(region=region)
        return queryset

    # Custom endpoint for trends
    @action(detail=False, methods=['get'])
    def trends(self, request):
        crop_id = request.query_params.get('crop')
        period = request.query_params.get('period', 'monthly')
        if not crop_id:
            return Response({"error": "crop parameter required"}, status=400)

        qs = PriceRecord.objects.filter(crop_id=crop_id)
        # For now, just average by region
        data = qs.values('region').annotate(avg_price=Avg('price'))
        return Response(data)


class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all().order_by('-created_at')
    serializer_class = NotificationSerializer
    permission_classes = [permissions.AllowAny]  # ✅ public

    def get_queryset(self):
        queryset = Notification.objects.all().order_by('-created_at')
        user_id = self.request.query_params.get('user')
        if user_id:
            queryset = queryset.filter(user_id=user_id)
        # Removed request.user fallback
        return queryset
