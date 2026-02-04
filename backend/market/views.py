from rest_framework import viewsets, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db.models import Avg, Count
from datetime import timedelta, date

from .models import User, Crop, PriceRecord, Notification, MarketPost, PriceAlert
from .serializers import (
    UserSerializer, CropSerializer, PriceRecordSerializer,
    NotificationSerializer, MarketPostSerializer, PriceAlertSerializer
)


# =========================
# User / Crop / Price / Notification
# =========================
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    @action(detail=False, methods=['get'])
    def me(self, request):
        user = User.objects.first()
        serializer = self.get_serializer(user)
        return Response(serializer.data)


class CropViewSet(viewsets.ModelViewSet):
    queryset = Crop.objects.all()
    serializer_class = CropSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        queryset = Crop.objects.all()
        farmer_id = self.request.query_params.get('farmer')
        if farmer_id:
            queryset = queryset.filter(farmer_id=farmer_id)
        return queryset


class PriceRecordViewSet(viewsets.ModelViewSet):
    queryset = PriceRecord.objects.all().order_by('-timestamp')
    serializer_class = PriceRecordSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        queryset = PriceRecord.objects.all().order_by('-timestamp')
        crop_id = self.request.query_params.get('crop')
        region = self.request.query_params.get('region')
        if crop_id:
            queryset = queryset.filter(crop_id=crop_id)
        if region:
            queryset = queryset.filter(region=region)
        return queryset

    @action(detail=False, methods=['get'])
    def trends(self, request):
        crop_id = request.query_params.get('crop')
        if not crop_id:
            return Response({"error": "crop parameter required"}, status=400)
        data = PriceRecord.objects.filter(crop_id=crop_id)\
            .values('region')\
            .annotate(avg_price=Avg('price'))
        return Response(data)


class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all().order_by('-created_at')
    serializer_class = NotificationSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        queryset = Notification.objects.all().order_by('-created_at')
        user_id = self.request.query_params.get('user')
        if user_id:
            queryset = queryset.filter(user_id=user_id)
        return queryset


# =========================
# Marketplace / Alerts / Demand
# =========================
class MarketPostViewSet(viewsets.ModelViewSet):
    queryset = MarketPost.objects.all()
    serializer_class = MarketPostSerializer
    permission_classes = [permissions.AllowAny]


class PriceAlertViewSet(viewsets.ModelViewSet):
    queryset = PriceAlert.objects.all()
    serializer_class = PriceAlertSerializer
    permission_classes = [permissions.AllowAny]


class DemandView(APIView):
    def get(self, request):
        data = (
            PriceRecord.objects
            .values('crop__name', 'market')
            .annotate(records=Count('id'))
            .order_by('-records')
        )
        return Response(data)


# =========================
# APIViews for analytics
# =========================
class PriceTrendView(APIView):
    def get(self, request, crop_id):
        period = request.query_params.get('period', 'monthly')
        today = date.today()
        if period == 'weekly':
            start = today - timedelta(days=7)
        elif period == 'yearly':
            start = today - timedelta(days=365)
        else:
            start = today - timedelta(days=30)

        data = (
            PriceRecord.objects
            .filter(crop_id=crop_id, date__gte=start)
            .values('date')
            .annotate(avg_price=Avg('price'))
            .order_by('date')
        )
        return Response(data)


class MarketAverageView(APIView):
    def get(self, request):
        data = (
            PriceRecord.objects
            .values('region')
            .annotate(avg_price=Avg('price'))
        )
        return Response(data)


class CropRecommendationView(APIView):
    def get(self, request):
        # fallback if no user auth
        region = getattr(request.user, 'region', 'DefaultRegion')
        crops = (
            PriceRecord.objects
            .filter(region=region)
            .values('crop__name')
            .annotate(avg_price=Avg('price'))
            .order_by('-avg_price')[:5]
        )
        return Response(crops)
