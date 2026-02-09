
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse
import os

def health_check(request):
    """Simple health check endpoint for Render"""
    return JsonResponse({
        'status': 'healthy',
        'service': 'agriculture-backend',
        'version': '1.0.0',
        'settings_module': os.environ.get('DJANGO_SETTINGS_MODULE', 'unknown'),
        'debug_mode': getattr(settings, 'DEBUG', 'unknown'),
        'cors_origins': getattr(settings, 'CORS_ALLOWED_ORIGINS', 'not_set'),
        'cors_allow_all': getattr(settings, 'CORS_ALLOW_ALL_ORIGINS', 'not_set')
    })

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('market.urls')),
    path('health/', health_check, name='health_check'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
