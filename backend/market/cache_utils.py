from django.core.cache import cache
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
import json
import hashlib

class CacheManager:
    """
    Centralized cache management for the agriculture market application
    """
    
    # Cache key prefixes
    WEATHER_PREFIX = 'weather:'
    PRICE_PREFIX = 'price:'
    CROP_PREFIX = 'crop:'
    USER_PREFIX = 'user:'
    ANALYTICS_PREFIX = 'analytics:'
    NOTIFICATION_PREFIX = 'notification:'
    
    # Cache durations (in seconds)
    CACHE_DURATIONS = {
        'weather_current': 300,      # 5 minutes
        'weather_forecast': 1800,    # 30 minutes
        'price_data': 600,           # 10 minutes
        'crop_data': 3600,           # 1 hour
        'user_data': 1800,           # 30 minutes
        'analytics_data': 900,       # 15 minutes
        'notifications': 300,        # 5 minutes
        'market_data': 300,           # 5 minutes
        'recommendations': 1800,      # 30 minutes
    }
    
    @classmethod
    def get_cache_key(cls, prefix, *args):
        """Generate a consistent cache key"""
        key_string = ':'.join(str(arg) for arg in args)
        return f"{prefix}{key_string}"
    
    @classmethod
    def get(cls, prefix, key, default=None):
        """Get cached data"""
        cache_key = cls.get_cache_key(prefix, key)
        return cache.get(cache_key, default)
    
    @classmethod
    def set(cls, prefix, key, value, duration=None):
        """Set cache data with optional duration"""
        cache_key = cls.get_cache_key(prefix, key)
        
        if duration is None:
            # Determine default duration based on prefix
            if prefix == cls.WEATHER_PREFIX:
                duration = cls.CACHE_DURATIONS['weather_current']
            elif prefix == cls.PRICE_PREFIX:
                duration = cls.CACHE_DURATIONS['price_data']
            elif prefix == cls.CROP_PREFIX:
                duration = cls.CACHE_DURATIONS['crop_data']
            elif prefix == cls.USER_PREFIX:
                duration = cls.CACHE_DURATIONS['user_data']
            elif prefix == cls.ANALYTICS_PREFIX:
                duration = cls.CACHE_DURATIONS['analytics_data']
            elif prefix == cls.NOTIFICATION_PREFIX:
                duration = cls.CACHE_DURATIONS['notifications']
            else:
                duration = 300  # Default 5 minutes
        
        return cache.set(cache_key, value, duration)
    
    @classmethod
    def delete(cls, prefix, key):
        """Delete cached data"""
        cache_key = cls.get_cache_key(prefix, key)
        return cache.delete(cache_key)
    
    @classmethod
    def clear_pattern(cls, pattern):
        """Clear cache keys matching a pattern"""
        # This is a simplified implementation
        # In production, you might want to use redis-py's scan functionality
        keys = cache.keys(pattern)
        if keys:
            return cache.delete_many(keys)
        return 0
    
    @classmethod
    def get_or_set(cls, prefix, key, callback, duration=None):
        """Get cached data or set it using callback if not exists"""
        cached_data = cls.get(prefix, key)
        if cached_data is not None:
            return cached_data
        
        # Generate data using callback
        data = callback()
        cls.set(prefix, key, data, duration)
        return data
    
    @classmethod
    def cache_weather_data(cls, region, weather_data, forecast=False):
        """Cache weather data"""
        prefix = cls.WEATHER_PREFIX
        key_suffix = 'forecast' if forecast else 'current'
        cache_key = f"{region}:{key_suffix}"
        
        duration = cls.CACHE_DURATIONS['weather_forecast'] if forecast else cls.CACHE_DURATIONS['weather_current']
        return cls.set(prefix, cache_key, weather_data, duration)
    
    @classmethod
    def get_weather_data(cls, region, forecast=False):
        """Get cached weather data"""
        prefix = cls.WEATHER_PREFIX
        key_suffix = 'forecast' if forecast else 'current'
        cache_key = f"{region}:{key_suffix}"
        
        return cls.get(prefix, cache_key)
    
    @classmethod
    def cache_price_data(cls, crop_id=None, region=None, price_data=None):
        """Cache price data"""
        prefix = cls.PRICE_PREFIX
        cache_key_parts = []
        
        if crop_id:
            cache_key_parts.append(f"crop:{crop_id}")
        if region:
            cache_key_parts.append(f"region:{region}")
        
        if not cache_key_parts:
            cache_key_parts.append("all")
        
        cache_key = ':'.join(cache_key_parts)
        return cls.set(prefix, cache_key, price_data)
    
    @classmethod
    def get_price_data(cls, crop_id=None, region=None):
        """Get cached price data"""
        prefix = cls.PRICE_PREFIX
        cache_key_parts = []
        
        if crop_id:
            cache_key_parts.append(f"crop:{crop_id}")
        if region:
            cache_key_parts.append(f"region:{region}")
        
        if not cache_key_parts:
            cache_key_parts.append("all")
        
        cache_key = ':'.join(cache_key_parts)
        return cls.get(prefix, cache_key)
    
    @classmethod
    def cache_user_data(cls, user_id, user_data):
        """Cache user data"""
        prefix = cls.USER_PREFIX
        return cls.set(prefix, user_id, user_data)
    
    @classmethod
    def get_user_data(cls, user_id):
        """Get cached user data"""
        prefix = cls.USER_PREFIX
        return cls.get(prefix, user_id)
    
    @classmethod
    def cache_analytics_data(cls, analytics_type, params, data):
        """Cache analytics data"""
        prefix = cls.ANALYTICS_PREFIX
        
        # Create a hash of parameters for consistent key
        params_str = json.dumps(params, sort_keys=True)
        params_hash = hashlib.md5(params_str.encode()).hexdigest()
        
        cache_key = f"{analytics_type}:{params_hash}"
        return cls.set(prefix, cache_key, data)
    
    @classmethod
    def get_analytics_data(cls, analytics_type, params):
        """Get cached analytics data"""
        prefix = cls.ANALYTICS_PREFIX
        
        # Create a hash of parameters for consistent key
        params_str = json.dumps(params, sort_keys=True)
        params_hash = hashlib.md5(params_str.encode()).hexdigest()
        
        cache_key = f"{analytics_type}:{params_hash}"
        return cls.get(prefix, cache_key)
    
    @classmethod
    def invalidate_user_cache(cls, user_id):
        """Invalidate all cache entries for a specific user"""
        patterns = [
            f"{cls.USER_PREFIX}{user_id}",
            f"{cls.NOTIFICATION_PREFIX}user:{user_id}",
        ]
        
        deleted_count = 0
        for pattern in patterns:
            deleted_count += cls.clear_pattern(pattern)
        
        return deleted_count
    
    @classmethod
    def invalidate_price_cache(cls, crop_id=None, region=None):
        """Invalidate price cache entries"""
        patterns = [f"{cls.PRICE_PREFIX}*"]
        
        if crop_id:
            patterns.append(f"{cls.PRICE_PREFIX}crop:{crop_id}:*")
        if region:
            patterns.append(f"{cls.PRICE_PREFIX}*:region:{region}:*")
        
        deleted_count = 0
        for pattern in patterns:
            deleted_count += cls.clear_pattern(pattern)
        
        return deleted_count
    
    @classmethod
    def invalidate_weather_cache(cls, region):
        """Invalidate weather cache for a region"""
        patterns = [
            f"{cls.WEATHER_PREFIX}{region}:current",
            f"{cls.WEATHER_PREFIX}{region}:forecast",
        ]
        
        deleted_count = 0
        for pattern in patterns:
            deleted_count += cls.clear_pattern(pattern)
        
        return deleted_count
    
    @classmethod
    def get_cache_stats(cls):
        """Get cache statistics (Redis specific)"""
        try:
            if hasattr(cache, 'client'):  # Redis cache
                info = cache.client.info()
                return {
                    'type': 'redis',
                    'used_memory': info.get('used_memory_human', 'Unknown'),
                    'connected_clients': info.get('connected_clients', 0),
                    'total_commands_processed': info.get('total_commands_processed', 0),
                    'keyspace_hits': info.get('keyspace_hits', 0),
                    'keyspace_misses': info.get('keyspace_misses', 0),
                }
            else:
                return {'type': 'local', 'message': 'Local cache - no detailed stats available'}
        except Exception as e:
            return {'type': 'error', 'message': str(e)}
    
    @classmethod
    def warm_up_cache(cls):
        """Warm up frequently accessed cache data"""
        from .models import Crop, PriceRecord, User
        
        # Cache all crops
        crops = Crop.objects.all()
        for crop in crops:
            crop_data = {
                'id': crop.id,
                'name': crop.name,
                'description': crop.description,
            }
            cls.cache_crop_data(crop.id, crop_data)
        
        # Cache latest price records for each crop
        for crop in crops:
            latest_price = PriceRecord.objects.filter(crop=crop).order_by('-timestamp').first()
            if latest_price:
                cls.cache_price_data(crop.id, None, {
                    'price': float(latest_price.price),
                    'date': latest_price.date.isoformat(),
                    'region': latest_price.region,
                })
        
        return True
    
    @classmethod
    def cache_crop_data(cls, crop_id, crop_data):
        """Cache crop data"""
        prefix = cls.CROP_PREFIX
        return cls.set(prefix, crop_id, crop_data)
    
    @classmethod
    def get_crop_data(cls, crop_id):
        """Get cached crop data"""
        prefix = cls.CROP_PREFIX
        return cls.get(prefix, crop_id)


# Decorator for caching function results
def cache_result(prefix, duration=None, key_func=None):
    """
    Decorator to cache function results
    
    Usage:
    @cache_result(CacheManager.PRICE_PREFIX, duration=600)
    def get_expensive_calculation(param1, param2):
        # Expensive operation
        return result
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            # Generate cache key
            if key_func:
                cache_key = key_func(*args, **kwargs)
            else:
                # Default key generation
                key_parts = [func.__name__] + [str(arg) for arg in args]
                key_parts.extend([f"{k}:{v}" for k, v in sorted(kwargs.items())])
                cache_key = ':'.join(key_parts)
            
            # Try to get from cache
            cached_result = CacheManager.get(prefix, cache_key)
            if cached_result is not None:
                return cached_result
            
            # Execute function and cache result
            result = func(*args, **kwargs)
            CacheManager.set(prefix, cache_key, result, duration)
            return result
        
        return wrapper
    return decorator


# Cache warming task
def schedule_cache_warming():
    """
    Schedule periodic cache warming
    This should be called from a management command or celery task
    """
    from django.utils import timezone
    import threading
    
    def warm_cache():
        try:
            CacheManager.warm_up_cache()
            print(f"Cache warmed at {timezone.now()}")
        except Exception as e:
            print(f"Cache warming failed: {e}")
    
    # Run in background thread (in production, use Celery)
    thread = threading.Thread(target=warm_cache)
    thread.daemon = True
    thread.start()
    
    return True
