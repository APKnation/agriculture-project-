from rest_framework import viewsets, permissions, status, parsers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.db.models import Avg, Count, Sum, Max, Min, StdDev, Variance
from django.db.models.functions import TruncDate, TruncWeek, TruncMonth, TruncYear
from datetime import timedelta, date
from django.utils import timezone
from itertools import count
from decimal import Decimal

from .models import User, Crop, PriceRecord, Notification, MarketPost, PriceAlert
from .serializers import (
    UserSerializer, CropSerializer, PriceRecordSerializer,
    NotificationSerializer, MarketPostSerializer, PriceAlertSerializer
)
from .permissions import (
    IsOwnerOrReadOnly, IsFarmer, IsOfficer, IsAdmin, 
    IsFarmerOrOfficer, IsOfficerOrAdmin, CanAccessAnalytics, CanManageUsers
)


# =========================
# Authentication Views
# =========================
@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')
    
    if not username or not password:
        return Response({
            'error': 'Username and password are required'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        user = User.objects.get(username=username)
        if user.check_password(password):
            refresh = RefreshToken.for_user(user)
            return Response({
                'token': str(refresh.access_token),
                'refresh': str(refresh),
                'user': UserSerializer(user).data,
                'role': user.role
            })
        else:
            return Response({
                'error': 'Invalid credentials'
            }, status=status.HTTP_401_UNAUTHORIZED)
    except User.DoesNotExist:
        return Response({
            'error': 'User not found'
        }, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def logout_view(request):
    try:
        refresh_token = request.data.get('refresh')
        if refresh_token:
            token = RefreshToken(refresh_token)
            token.blacklist()
        return Response({'message': 'Successfully logged out'})
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def register_view(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            'token': str(refresh.access_token),
            'refresh': str(refresh),
            'user': UserSerializer(user).data,
            'role': user.role
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def change_password_view(request):
    current_password = request.data.get('current_password')
    new_password = request.data.get('new_password')
    
    if not current_password or not new_password:
        return Response({
            'error': 'Current password and new password are required'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        user = request.user
        if not user.check_password(current_password):
            return Response({
                'error': 'Current password is incorrect'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        user.set_password(new_password)
        user.save()
        return Response({'message': 'Password changed successfully'})
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def user_stats(request):
    user = request.user
    
    # Get user's crops count
    total_crops = Crop.objects.filter(farmer=user).count()
    
    # Get user's price records count
    total_price_records = PriceRecord.objects.filter(crop__farmer=user).count()
    
    # Get unread notifications count
    unread_notifications = Notification.objects.filter(user=user, read=False).count()
    
    # Calculate days active (since registration)
    days_active = (timezone.now() - user.date_joined).days
    
    return Response({
        'totalCrops': total_crops,
        'totalPriceRecords': total_price_records,
        'notifications': unread_notifications,
        'daysActive': days_active
    })

# =========================
# User / Crop / Price / Notification
# =========================
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.IsAuthenticated()]
        return [CanManageUsers()]

    @action(detail=False, methods=['get'], permission_classes=[permissions.AllowAny])
    def me(self, request):
        if request.user.is_authenticated:
            serializer = self.get_serializer(request.user)
            return Response(serializer.data)
        else:
            return Response({'detail': 'Authentication required'}, status=401)


class CropViewSet(viewsets.ModelViewSet):
    queryset = Crop.objects.all()
    serializer_class = CropSerializer
    parser_classes = [parsers.JSONParser, parsers.MultiPartParser, parsers.FormParser]

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [permissions.IsAuthenticated]
        else:
            self.permission_classes = [permissions.AllowAny]
        return super().get_permissions()

    def get_queryset(self):
        return Crop.objects.all()

    def perform_create(self, serializer):
        # Set farmer to current user
        try:
            print("Creating crop with data:", serializer.validated_data)
            crop = serializer.save(farmer=self.request.user)
            print("Crop created successfully:", crop)
            return crop
        except Exception as e:
            print("Error creating crop:", str(e))
            print("Error details:", e.__class__.__name__)
            raise e

    def perform_update(self, serializer):
        # Ensure farmer is set to current user
        try:
            print("Updating crop with data:", serializer.validated_data)
            # Remove farmer from validated_data if it exists
            validated_data = serializer.validated_data.copy()
            if 'farmer' in validated_data:
                del validated_data['farmer']
            crop = serializer.save(farmer=self.request.user, **validated_data)
            print("Crop updated successfully:", crop)
            return crop
        except Exception as e:
            print("Error updating crop:", str(e))
            print("Error details:", e.__class__.__name__)
            print("Serializer errors:", getattr(serializer, 'errors', 'No errors'))
            raise e
        return serializer

    @action(detail=True, methods=['post'])
    def upload_image(self, request, pk=None):
        crop = self.get_object()
        if 'image' in request.FILES:
            crop.image = request.FILES['image']
            crop.save()
            return Response({'message': 'Image uploaded successfully', 'image_url': crop.image.url if crop.image else None})
        return Response({'error': 'No image provided'}, status=status.HTTP_400_BAD_REQUEST)


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
        data = (
            PriceRecord.objects
            .filter(crop_id=crop_id)
            .values('region')
            .annotate(avg_price=Avg('price'))
        )
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


class RegionsView(APIView):
    permission_classes = [permissions.AllowAny]
    
    def get(self, request):
        """Get all regions with their associated crops"""
        try:
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
                    'latest_price': float(latest_record.price) if latest_record else None,
                    'latest_crop': latest_record.crop.name if latest_record else None
                })
            
            return Response(regions_data)
            
        except Exception as e:
            return Response({'error': str(e)}, status=500)


class DemandView(APIView):
    permission_classes = [permissions.AllowAny]  # Make accessible without authentication
    def get(self, request):
        # Get comprehensive demand data from multiple sources
        demand_data = []
        
        # 1. Get market posts (supply indicators)
        market_posts = MarketPost.objects.all()
        post_crops = {}
        for post in market_posts:
            crop_name = post.crop.name
            if crop_name not in post_crops:
                post_crops[crop_name] = {
                    'supply_count': 0,
                    'demand_count': 0,
                    'inquiries': 0
                }
            post_crops[crop_name]['supply_count'] += 1
        
        # 2. Get price alerts (demand indicators)
        price_alerts = PriceAlert.objects.filter(active=True)
        for alert in price_alerts:
            crop_name = alert.crop.name
            if crop_name not in post_crops:
                post_crops[crop_name] = {
                    'supply_count': 0,
                    'demand_count': 0,
                    'inquiries': 0
                }
            post_crops[crop_name]['demand_count'] += 1
        
        # 3. Get recent price records (market activity indicator)
        recent_prices = PriceRecord.objects.filter(
            date__gte=timezone.now() - timedelta(days=30)
        ).values('crop__name').annotate(record_count=Count('id'))
        
        for price in recent_prices:
            crop_name = price['crop__name']
            if crop_name not in post_crops:
                post_crops[crop_name] = {
                    'supply_count': 0,
                    'demand_count': 0,
                    'inquiries': 0
                }
            post_crops[crop_name]['inquiries'] += price['record_count']
        
        # 4. Calculate demand levels based on comprehensive metrics
        for crop_name, data in post_crops.items():
            supply = data['supply_count']
            demand_indicators = data['demand_count']
            market_activity = data['inquiries']
            
            # Calculate demand score (0-100)
            demand_score = 0
            
            # High demand if many price alerts + high market activity
            if demand_indicators >= 5 or market_activity >= 20:
                demand_score = min(85, demand_score * 20 + market_activity * 2)
            
            # Moderate demand with some activity
            elif demand_indicators >= 2 or market_activity >= 10:
                demand_score = min(60, demand_score * 15 + market_activity * 1.5)
            
            # Low demand with minimal activity
            elif demand_indicators >= 1 or market_activity >= 5:
                demand_score = min(40, demand_score * 10 + market_activity)
            
            # Very low demand with little to no activity
            else:
                demand_score = max(10, market_activity * 0.5)
            
            # Determine demand level
            if demand_score >= 70:
                demand_level = 'High'
            elif demand_score >= 50:
                demand_level = 'Moderate'
            elif demand_score >= 25:
                demand_level = 'Low'
            else:
                demand_level = 'Very Low'
            
            demand_data.append({
                'id': len(demand_data) + 1,
                'crop__name': crop_name,
                'market': self.get_primary_market(crop_name),
                'records': demand_score,
                'demand_level': demand_level,
                'supply_count': supply,
                'demand_indicators': demand_indicators,
                'market_activity': market_activity
            })
        
        return Response(demand_data)
    
    def get_primary_market(self, crop_name):
        """Get the primary market for a crop based on recent price records"""
        markets = PriceRecord.objects.filter(crop__name=crop_name).values('market').annotate(count=Count('id'))
        if markets.exists():
            return markets.order_by('-count').first()['market']
        return 'Unknown'


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


# =========================
# Advanced Analytics Views
# =========================
class AdvancedAnalyticsView(APIView):
    def get(self, request):
        period = request.query_params.get('period', 'monthly')
        region = request.query_params.get('region')
        crop_id = request.query_params.get('crop')
        
        # Date filtering
        today = date.today()
        if period == 'weekly':
            start = today - timedelta(days=7)
            trunc_func = TruncDate
        elif period == 'yearly':
            start = today - timedelta(days=365)
            trunc_func = TruncYear
        else:
            start = today - timedelta(days=30)
            trunc_func = TruncMonth
        
        # Base queryset
        queryset = PriceRecord.objects.filter(date__gte=start)
        if region:
            queryset = queryset.filter(region=region)
        if crop_id:
            queryset = queryset.filter(crop_id=crop_id)
        
        # Time series data
        time_series = (
            queryset
            .annotate(period=trunc_func('date'))
            .values('period')
            .annotate(
                avg_price=Avg('price'),
                max_price=Max('price'),
                min_price=Min('price'),
                volume=Count('id')
            )
            .order_by('period')
        )
        
        # Overall statistics
        stats = queryset.aggregate(
            avg_price=Avg('price'),
            max_price=Max('price'),
            min_price=Min('price'),
            price_stddev=StdDev('price'),
            total_records=Count('id'),
            price_variance=Variance('price')
        )
        
        # Regional comparison
        regional_data = (
            queryset
            .values('region')
            .annotate(
                avg_price=Avg('price'),
                volume=Count('id'),
                max_price=Max('price'),
                min_price=Min('price')
            )
            .order_by('-avg_price')
        )
        
        return Response({
            'time_series': list(time_series),
            'statistics': stats,
            'regional_comparison': list(regional_data),
            'period': period,
            'filters': {
                'region': region,
                'crop_id': crop_id
            }
        })


class MarketReportView(APIView):
    def get(self, request):
        report_type = request.query_params.get('type', 'summary')
        region = request.query_params.get('region')
        
        if report_type == 'summary':
            return self.generate_summary_report(region)
        elif report_type == 'detailed':
            return self.generate_detailed_report(region)
        elif report_type == 'forecast':
            return self.generate_forecast_report(region)
        else:
            return Response({'error': 'Invalid report type'}, status=400)
    
    def generate_summary_report(self, region=None):
        queryset = PriceRecord.objects.all()
        if region:
            queryset = queryset.filter(region=region)
        
        # Top performing crops
        top_crops = (
            queryset
            .values('crop__name')
            .annotate(
                avg_price=Avg('price'),
                total_volume=Count('id'),
                regions=Count('region', distinct=True)
            )
            .order_by('-avg_price')[:10]
        )
        
        # Market overview
        overview = queryset.aggregate(
            total_crops=Count('crop', distinct=True),
            total_regions=Count('region', distinct=True),
            avg_price=Avg('price'),
            total_transactions=Count('id')
        )
        
        # Price volatility analysis
        volatility = (
            queryset
            .values('crop__name')
            .annotate(
                price_stddev=StdDev('price'),
                avg_price=Avg('price'),
                volatility=StdDev('price') / Avg('price')
            )
            .order_by('-volatility')[:5]
        )
        
        return Response({
            'report_type': 'summary',
            'overview': overview,
            'top_crops': list(top_crops),
            'price_volatility': list(volatility),
            'generated_at': date.today().isoformat()
        })
    
    def generate_detailed_report(self, region=None):
        queryset = PriceRecord.objects.all()
        if region:
            queryset = queryset.filter(region=region)
        
        # Monthly trends
        monthly_trends = (
            queryset
            .annotate(month=TruncMonth('date'))
            .values('month')
            .annotate(
                avg_price=Avg('price'),
                transaction_count=Count('id'),
                unique_crops=Count('crop', distinct=True)
            )
            .order_by('month')
        )
        
        # Crop performance matrix
        crop_performance = (
            queryset
            .values('crop__name', 'region')
            .annotate(
                avg_price=Avg('price'),
                max_price=Max('price'),
                min_price=Min('price'),
                transaction_count=Count('id')
            )
            .order_by('crop__name', '-avg_price')
        )
        
        return Response({
            'report_type': 'detailed',
            'monthly_trends': list(monthly_trends),
            'crop_performance_matrix': list(crop_performance),
            'generated_at': date.today().isoformat()
        })
    
    def generate_forecast_report(self, region=None):
        # Simple forecast based on historical trends
        queryset = PriceRecord.objects.filter(
            date__gte=date.today() - timedelta(days=90)
        )
        if region:
            queryset = queryset.filter(region=region)
        
        # Calculate trend for each crop
        forecasts = []
        for crop in Crop.objects.all():
            crop_data = queryset.filter(crop=crop)
            if crop_data.count() > 1:
                # Simple linear trend calculation
                recent_prices = list(
                    crop_data
                    .order_by('date')
                    .values_list('price', flat=True)
                )
                if len(recent_prices) >= 2:
                    trend = (recent_prices[-1] - recent_prices[0]) / len(recent_prices)
                    forecast_price = float(recent_prices[-1]) + float(trend)
                    
                    forecasts.append({
                        'crop': crop.name,
                        'current_price': float(recent_prices[-1]),
                        'forecast_price': forecast_price,
                        'trend': 'upward' if trend > 0 else 'downward' if trend < 0 else 'stable',
                        'confidence': 'medium'  # Simplified confidence level
                    })
        
        return Response({
            'report_type': 'forecast',
            'forecasts': forecasts,
            'generated_at': date.today().isoformat(),
            'methodology': 'Linear trend based on last 90 days'
        })


class YieldAnalyticsView(APIView):
    def get(self, request):
        farmer_id = request.query_params.get('farmer_id')
        
        queryset = Crop.objects.all()
        if farmer_id:
            queryset = queryset.filter(farmer_id=farmer_id)
        
        # Yield statistics
        yield_stats = queryset.aggregate(
            avg_yield=Avg('yield_estimate'),
            max_yield=Max('yield_estimate'),
            min_yield=Min('yield_estimate'),
            total_crops=Count('id'),
            yield_stddev=StdDev('yield_estimate')
        )
        
        # Crop performance by type
        crop_performance = (
            queryset
            .values('name')
            .annotate(
                avg_yield=Avg('yield_estimate'),
                total_count=Count('id'),
                avg_price=Avg('prices__price')
            )
            .order_by('-avg_yield')
        )
        
        # Seasonal analysis
        seasonal_data = (
            queryset
            .exclude(planting_date__isnull=True)
            .annotate(
                planting_month=TruncMonth('planting_date'),
                harvest_month=TruncMonth('expected_harvest_date')
            )
            .values('planting_month', 'harvest_month')
            .annotate(
                avg_yield=Avg('yield_estimate'),
                crop_count=Count('id')
            )
            .order_by('planting_month')
        )
        
        return Response({
            'yield_statistics': yield_stats,
            'crop_performance': list(crop_performance),
            'seasonal_analysis': list(seasonal_data)
        })


class DemandAnalyticsView(APIView):
    def get(self, request):
        region = request.query_params.get('region')
        time_period = request.query_params.get('period', '30')
        
        # Filter by time period
        days = int(time_period)
        start_date = date.today() - timedelta(days=days)
        
        queryset = PriceRecord.objects.filter(date__gte=start_date)
        if region:
            queryset = queryset.filter(region=region)
        
        # Demand indicators (based on transaction volume)
        demand_indicators = (
            queryset
            .values('crop__name')
            .annotate(
                transaction_volume=Count('id'),
                avg_price=Avg('price'),
                price_volatility=StdDev('price') / Avg('price'),
                market_penetration=Count('region', distinct=True)
            )
            .order_by('-transaction_volume')
        )
        
        # Regional demand distribution
        regional_demand = (
            queryset
            .values('region')
            .annotate(
                total_transactions=Count('id'),
                unique_crops=Count('crop', distinct=True),
                avg_price=Avg('price')
            )
            .order_by('-total_transactions')
        )
        
        # Price-demand correlation (simplified)
        price_demand_correlation = []
        for crop in queryset.values_list('crop__name', flat=True).distinct():
            crop_data = queryset.filter(crop__name=crop)
            if crop_data.count() > 1:
                avg_price = crop_data.aggregate(avg_price=Avg('price'))['avg_price']
                volume = crop_data.count()
                price_demand_correlation.append({
                    'crop': crop,
                    'avg_price': float(avg_price),
                    'demand_volume': volume,
                    'price_elasticity': 'high' if volume > 10 else 'medium' if volume > 5 else 'low'
                })
        
        return Response({
            'demand_indicators': list(demand_indicators),
            'regional_demand': list(regional_demand),
            'price_demand_correlation': price_demand_correlation,
            'analysis_period': f'{days} days'
        })
