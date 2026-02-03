from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from market.views import UserViewSet, CropViewSet, PriceRecordViewSet, NotificationViewSet

router.register(r'users', UserViewSet, basename='user')
router.register(r'crops', CropViewSet, basename='crop')
router.register(r'price-records', PriceRecordViewSet, basename='price-record')
router.register(r'notifications', NotificationViewSet, basename='notification')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
]
