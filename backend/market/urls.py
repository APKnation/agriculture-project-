from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Create a router and register ViewSets
router = DefaultRouter()
router.register(r'users', views.UserViewSet, basename='user')
router.register(r'crops', views.CropViewSet, basename='crop')
router.register(r'price-records', views.PriceRecordViewSet, basename='pricerecord')
router.register(r'notifications', views.NotificationViewSet, basename='notification')
router.register(r'market-posts', views.MarketPostViewSet, basename='marketpost')
router.register(r'price-alerts', views.PriceAlertViewSet, basename='pricealert')

# Define URL patterns
urlpatterns = [
    # Router URLs (includes all ViewSet endpoints)
    path('', include(router.urls)),
    
    # APIView endpoints
    path('demand/', views.DemandView.as_view(), name='demand'),
    path('price-trend/<int:crop_id>/', views.PriceTrendView.as_view(), name='price-trend'),
    path('market-average/', views.MarketAverageView.as_view(), name='market-average'),
    path('crop-recommendation/', views.CropRecommendationView.as_view(), name='crop-recommendation'),
]
