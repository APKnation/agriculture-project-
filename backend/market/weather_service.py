import requests
import logging
from datetime import datetime, timedelta
from django.conf import settings
from .models import WeatherData, WeatherAlert, CropWeatherRecommendation

logger = logging.getLogger(__name__)

class WeatherService:
    def __init__(self):
        self.api_key = getattr(settings, 'OPENWEATHER_API_KEY', None)
        self.base_url = 'https://api.openweathermap.org/data/2.5'
        
    def get_current_weather(self, region):
        """
        Fetch current weather data for a region
        """
        if not self.api_key:
            logger.error("OpenWeather API key not configured")
            return None
            
        try:
            # Get coordinates for the region (simplified - in production, use geocoding API)
            coords = self.get_region_coordinates(region)
            if not coords:
                logger.error(f"Could not find coordinates for region: {region}")
                return None
            
            url = f"{self.base_url}/weather"
            params = {
                'lat': coords['lat'],
                'lon': coords['lon'],
                'appid': self.api_key,
                'units': 'metric'  # Celsius
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            # Parse and save weather data
            weather_data = {
                'region': region,
                'date': datetime.now().date(),
                'temperature': data['main']['temp'],
                'humidity': data['main']['humidity'],
                'rainfall': data.get('rain', {}).get('1h', 0) * 24,  # Convert hourly to daily estimate
                'wind_speed': data.get('wind', {}).get('speed', 0) * 3.6,  # Convert m/s to km/h
                'weather_condition': data['weather'][0]['main'],
                'data_source': 'OpenWeatherMap'
            }
            
            # Save to database
            weather_record, created = WeatherData.objects.update_or_create(
                region=region,
                date=weather_data['date'],
                defaults=weather_data
            )
            
            return weather_record
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching weather data: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error processing weather data: {e}")
            return None
    
    def get_forecast(self, region, days=5):
        """
        Fetch weather forecast for a region
        """
        if not self.api_key:
            logger.error("OpenWeather API key not configured")
            return []
            
        try:
            coords = self.get_region_coordinates(region)
            if not coords:
                return []
            
            url = f"{self.base_url}/forecast"
            params = {
                'lat': coords['lat'],
                'lon': coords['lon'],
                'appid': self.api_key,
                'units': 'metric'
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            # Process forecast data (group by day)
            forecast_data = []
            daily_data = {}
            
            for item in data['list']:
                date = datetime.fromtimestamp(item['dt']).date()
                
                if date not in daily_data:
                    daily_data[date] = {
                        'date': date,
                        'temperatures': [],
                        'humidity': [],
                        'rainfall': 0,
                        'wind_speed': [],
                        'conditions': []
                    }
                
                daily_data[date]['temperatures'].append(item['main']['temp'])
                daily_data[date]['humidity'].append(item['main']['humidity'])
                daily_data[date]['rainfall'] += item.get('rain', {}).get('3h', 0)
                daily_data[date]['wind_speed'].append(item.get('wind', {}).get('speed', 0))
                daily_data[date]['conditions'].append(item['weather'][0]['main'])
            
            # Calculate daily averages
            for date_data in daily_data.values():
                forecast_data.append({
                    'region': region,
                    'date': date_data['date'],
                    'temperature': sum(date_data['temperatures']) / len(date_data['temperatures']),
                    'humidity': sum(date_data['humidity']) / len(date_data['humidity']),
                    'rainfall': date_data['rainfall'],
                    'wind_speed': (sum(date_data['wind_speed']) / len(date_data['wind_speed'])) * 3.6,
                    'weather_condition': max(set(date_data['conditions']), key=date_data['conditions'].count)
                })
            
            return forecast_data[:days]
            
        except Exception as e:
            logger.error(f"Error fetching forecast data: {e}")
            return []
    
    def get_region_coordinates(self, region):
        """
        Get coordinates for a region (simplified implementation)
        In production, use a proper geocoding service
        """
        # This is a simplified mapping - in production, use Google Geocoding API or similar
        region_coords = {
            'North': {'lat': 40.7128, 'lon': -74.0060},  # New York
            'South': {'lat': 34.0522, 'lon': -118.2437},  # Los Angeles
            'East': {'lat': 42.3601, 'lon': -71.0589},   # Boston
            'West': {'lat': 37.7749, 'lon': -122.4194},  # San Francisco
            'Central': {'lat': 41.8781, 'lon': -87.6298}, # Chicago
            'DefaultRegion': {'lat': 40.7128, 'lon': -74.0060}
        }
        
        return region_coords.get(region, region_coords.get('DefaultRegion'))
    
    def check_weather_alerts(self, region):
        """
        Check for weather alerts and create notifications
        """
        try:
            current_weather = WeatherData.objects.filter(
                region=region,
                date=datetime.now().date()
            ).first()
            
            if not current_weather:
                return []
            
            alerts = []
            
            # Temperature alerts
            if current_weather.temperature < 5:
                alerts.append({
                    'alert_type': 'Frost Warning',
                    'severity': 'high',
                    'message': f'Low temperature of {current_weather.temperature}°C detected. Risk of frost damage to crops.'
                })
            elif current_weather.temperature > 35:
                alerts.append({
                    'alert_type': 'Heatwave Warning',
                    'severity': 'high',
                    'message': f'High temperature of {current_weather.temperature}°C detected. Ensure adequate irrigation for crops.'
                })
            
            # Rainfall alerts
            if current_weather.rainfall > 50:
                alerts.append({
                    'alert_type': 'Heavy Rain Warning',
                    'severity': 'medium',
                    'message': f'Heavy rainfall of {current_weather.rainfall}mm expected. Risk of flooding and waterlogging.'
                })
            elif current_weather.rainfall < 1 and current_weather.weather_condition == 'Clear':
                alerts.append({
                    'alert_type': 'Drought Warning',
                    'severity': 'medium',
                    'message': 'No rainfall expected. Consider irrigation for water-sensitive crops.'
                })
            
            # Wind alerts
            if current_weather.wind_speed > 50:
                alerts.append({
                    'alert_type': 'Strong Wind Warning',
                    'severity': 'medium',
                    'message': f'Strong winds of {current_weather.wind_speed}km/h expected. Secure loose equipment and protect young plants.'
                })
            
            return alerts
            
        except Exception as e:
            logger.error(f"Error checking weather alerts: {e}")
            return []
    
    def generate_crop_recommendations(self, region, weather_condition):
        """
        Generate farming recommendations based on weather conditions
        """
        recommendations = []
        
        # Predefined recommendations based on weather conditions
        weather_recommendations = {
            'Clear': [
                'Good conditions for harvesting and field operations',
                'Monitor soil moisture levels and irrigate if needed',
                'Apply pesticides during cooler parts of the day'
            ],
            'Clouds': [
                'Suitable conditions for transplanting seedlings',
                'Reduced stress on plants compared to direct sunlight',
                'Good time for fertilizer application'
            ],
            'Rain': [
                'Avoid field operations during heavy rainfall',
                'Check drainage systems to prevent waterlogging',
                'Postpone fertilizer application to prevent runoff'
            ],
            'Snow': [
                'Protect sensitive crops with covers or mulch',
                'Ensure livestock have adequate shelter',
                'Check greenhouse structures for snow load'
            ],
            'Thunderstorm': [
                'Seek shelter and avoid outdoor field work',
                'Secure equipment and structures',
                'Check for lightning damage to irrigation systems'
            ]
        }
        
        condition_recommendations = weather_recommendations.get(weather_condition, [
            'Monitor weather conditions closely',
            'Adjust farming activities as needed'
        ])
        
        return condition_recommendations

# Weather data update task (can be called by celery or cron)
def update_weather_data():
    """
    Update weather data for all regions
    """
    from .models import User
    
    weather_service = WeatherService()
    regions = User.objects.values_list('region', flat=True).distinct()
    
    for region in regions:
        if region:  # Skip null/empty regions
            weather_service.get_current_weather(region)
            alerts = weather_service.check_weather_alerts(region)
            
            # Create weather alerts for users in the region
            for alert_data in alerts:
                users_in_region = User.objects.filter(region=region)
                for user in users_in_region:
                    WeatherAlert.objects.get_or_create(
                        user=user,
                        region=region,
                        alert_type=alert_data['alert_type'],
                        severity=alert_data['severity'],
                        message=alert_data['message'],
                        start_date=datetime.now(),
                        end_date=datetime.now() + timedelta(hours=24),
                        defaults={'is_active': True}
                    )
