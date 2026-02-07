from rest_framework import viewsets, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from django.utils import timezone
from datetime import datetime, timedelta
from django.db.models import Avg, Max, Min, Sum, Count
from .models import WeatherData, WeatherAlert, CropWeatherRecommendation
from .weather_service import WeatherService
from .permissions import IsFarmer, IsOfficer, IsAdmin, IsOfficerOrAdmin

class WeatherDataViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = None  # We'll create this if needed
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = WeatherData.objects.all()
        region = self.request.query_params.get('region')
        if region:
            queryset = queryset.filter(region=region)
        
        # Filter by date range
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        if start_date:
            queryset = queryset.filter(date__gte=start_date)
        if end_date:
            queryset = queryset.filter(date__lte=end_date)
            
        return queryset.order_by('-date')

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        data = []
        
        for weather in queryset:
            data.append({
                'id': weather.id,
                'region': weather.region,
                'date': weather.date,
                'temperature': weather.temperature,
                'humidity': weather.humidity,
                'rainfall': weather.rainfall,
                'wind_speed': weather.wind_speed,
                'weather_condition': weather.weather_condition,
                'data_source': weather.data_source,
                'created_at': weather.created_at
            })
        
        return Response(data)

    @action(detail=False, methods=['get'])
    def current(self, request):
        """Get current weather for user's region"""
        region = request.query_params.get('region') or getattr(request.user, 'region', None)
        
        if not region:
            return Response(
                {'error': 'Region parameter is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        weather_service = WeatherService()
        weather_data = weather_service.get_current_weather(region)
        
        if weather_data:
            return Response({
                'id': weather_data.id,
                'region': weather_data.region,
                'date': weather_data.date,
                'temperature': weather_data.temperature,
                'humidity': weather_data.humidity,
                'rainfall': weather_data.rainfall,
                'wind_speed': weather_data.wind_speed,
                'weather_condition': weather_data.weather_condition,
                'data_source': weather_data.data_source,
                'created_at': weather_data.created_at
            })
        else:
            return Response(
                {'error': 'Could not fetch weather data'}, 
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )

    @action(detail=False, methods=['get'])
    def forecast(self, request):
        """Get weather forecast for a region"""
        region = request.query_params.get('region') or getattr(request.user, 'region', None)
        days = int(request.query_params.get('days', 5))
        
        if not region:
            return Response(
                {'error': 'Region parameter is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        weather_service = WeatherService()
        forecast_data = weather_service.get_forecast(region, days)
        
        return Response(forecast_data)

    @action(detail=False, methods=['get'])
    def alerts(self, request):
        """Get weather alerts for user"""
        region = request.query_params.get('region') or getattr(request.user, 'region', None)
        
        if not region:
            return Response(
                {'error': 'Region parameter is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        alerts = WeatherAlert.objects.filter(
            user=request.user,
            region=region,
            is_active=True,
            end_date__gte=timezone.now()
        ).order_by('-created_at')
        
        data = []
        for alert in alerts:
            data.append({
                'id': alert.id,
                'alert_type': alert.alert_type,
                'severity': alert.severity,
                'message': alert.message,
                'start_date': alert.start_date,
                'end_date': alert.end_date,
                'is_active': alert.is_active,
                'created_at': alert.created_at
            })
        
        return Response(data)

    @action(detail=False, methods=['post'])
    def check_alerts(self, request):
        """Check and create weather alerts for user's region"""
        region = request.data.get('region') or getattr(request.user, 'region', None)
        
        if not region:
            return Response(
                {'error': 'Region parameter is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        weather_service = WeatherService()
        alerts = weather_service.check_weather_alerts(region)
        
        created_alerts = []
        for alert_data in alerts:
            alert, created = WeatherAlert.objects.get_or_create(
                user=request.user,
                region=region,
                alert_type=alert_data['alert_type'],
                severity=alert_data['severity'],
                message=alert_data['message'],
                start_date=timezone.now(),
                end_date=timezone.now() + timedelta(hours=24),
                defaults={'is_active': True}
            )
            
            if created:
                created_alerts.append({
                    'id': alert.id,
                    'alert_type': alert.alert_type,
                    'severity': alert.severity,
                    'message': alert.message
                })
        
        return Response({
            'message': f'Checked weather alerts for {region}',
            'new_alerts': created_alerts,
            'total_alerts': len(alerts)
        })


class WeatherRecommendationView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        """Get farming recommendations based on current weather"""
        region = request.query_params.get('region') or getattr(request.user, 'region', None)
        
        if not region:
            return Response(
                {'error': 'Region parameter is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Get current weather
        current_weather = WeatherData.objects.filter(
            region=region,
            date=timezone.now().date()
        ).first()
        
        if not current_weather:
            return Response(
                {'error': 'No weather data available for this region'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        weather_service = WeatherService()
        recommendations = weather_service.generate_crop_recommendations(
            region, 
            current_weather.weather_condition
        )
        
        # Get crop-specific recommendations
        crop_recommendations = CropWeatherRecommendation.objects.filter(
            region=region,
            weather_condition=current_weather.weather_condition
        ).order_by('-priority')
        
        crop_data = []
        for crop_rec in crop_recommendations:
            crop_data.append({
                'crop': crop_rec.crop.name,
                'recommendation': crop_rec.recommendation,
                'priority': crop_rec.priority
            })
        
        return Response({
            'region': region,
            'current_weather': {
                'temperature': current_weather.temperature,
                'humidity': current_weather.humidity,
                'rainfall': current_weather.rainfall,
                'wind_speed': current_weather.wind_speed,
                'weather_condition': current_weather.weather_condition
            },
            'general_recommendations': recommendations,
            'crop_specific_recommendations': crop_data,
            'generated_at': timezone.now()
        })


class WeatherAnalyticsView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsOfficerOrAdmin]

    def get(self, request):
        """Get weather analytics and trends"""
        region = request.query_params.get('region')
        days = int(request.query_params.get('days', 30))
        
        # Calculate date range
        end_date = timezone.now().date()
        start_date = end_date - timedelta(days=days)
        
        queryset = WeatherData.objects.filter(
            date__gte=start_date,
            date__lte=end_date
        )
        
        if region:
            queryset = queryset.filter(region=region)
        
        # Calculate statistics
        total_records = queryset.count()
        if total_records == 0:
            return Response({
                'error': 'No weather data available for the specified period',
                'period': f'{days} days',
                'region': region or 'All regions'
            }, status=status.HTTP_404_NOT_FOUND)
        
        # Weather statistics
        from django.db.models import Avg, Max, Min, Count
        
        stats = queryset.aggregate(
            avg_temperature=Avg('temperature'),
            max_temperature=Max('temperature'),
            min_temperature=Min('temperature'),
            avg_humidity=Avg('humidity'),
            total_rainfall=Sum('rainfall'),
            avg_wind_speed=Avg('wind_speed')
        )
        
        # Weather condition distribution
        condition_distribution = queryset.values('weather_condition').annotate(
            count=Count('id')
        ).order_by('-count')
        
        # Regional comparison (if no specific region)
        regional_data = []
        if not region:
            regional_stats = queryset.values('region').annotate(
                avg_temperature=Avg('temperature'),
                total_rainfall=Sum('rainfall'),
                record_count=Count('id')
            ).order_by('-avg_temperature')
            
            for stat in regional_stats:
                regional_data.append({
                    'region': stat['region'],
                    'avg_temperature': round(stat['avg_temperature'], 2),
                    'total_rainfall': round(stat['total_rainfall'], 2),
                    'record_count': stat['record_count']
                })
        
        # Daily trends
        daily_trends = []
        for weather in queryset.order_by('date'):
            daily_trends.append({
                'date': weather.date,
                'temperature': weather.temperature,
                'humidity': weather.humidity,
                'rainfall': weather.rainfall,
                'wind_speed': weather.wind_speed,
                'weather_condition': weather.weather_condition
            })
        
        return Response({
            'period': f'{days} days',
            'region': region or 'All regions',
            'total_records': total_records,
            'statistics': {
                'avg_temperature': round(stats['avg_temperature'], 2),
                'max_temperature': stats['max_temperature'],
                'min_temperature': stats['min_temperature'],
                'avg_humidity': round(stats['avg_humidity'], 2),
                'total_rainfall': round(stats['total_rainfall'], 2),
                'avg_wind_speed': round(stats['avg_wind_speed'], 2)
            },
            'condition_distribution': list(condition_distribution),
            'regional_comparison': regional_data,
            'daily_trends': daily_trends,
            'generated_at': timezone.now()
        })
