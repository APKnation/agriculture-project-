# Quick CSRF Fix for Cross-Origin Requests
# Add this to your settings_production.py if CSRF issues persist

# TEMPORARY CSRF DISABLE (FOR TESTING ONLY)
# WARNING: This reduces security - use only for debugging

# Option 1: Disable CSRF middleware temporarily
# MIDDLEWARE = [
#     'django.middleware.security.SecurityMiddleware',
#     'django.contrib.sessions.middleware.SessionMiddleware',
#     'corsheaders.middleware.CorsMiddleware',
#     'django.middleware.common.CommonMiddleware',
#     'django.contrib.auth.middleware.AuthenticationMiddleware',
#     'django.contrib.messages.middleware.MessageMiddleware',
#     'django.middleware.clickjacking.XFrameOptionsMiddleware',
#     'whitenoise.middleware.WhiteNoiseMiddleware',
# ]

# Option 2: Custom CSRF decorator that bypasses CSRF for API
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

# Apply to your API views:
# @method_decorator(csrf_exempt, name='dispatch')
# class YourAPIView(APIView):
#     pass

# Option 3: Add CSRF exempt to specific URLs in urls.py
# from django.views.decorators.csrf import csrf_exempt
# from django.urls import path
# from . import views

# urlpatterns = [
#     path('api/login/', csrf_exempt(views.login_view), name='login'),
# ]
