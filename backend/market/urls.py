from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views_file_upload import CropDocumentViewSet, CropImageViewSet, UserProfileImageViewSet
from .views_weather import WeatherDataViewSet, WeatherRecommendationView, WeatherAnalyticsView

router = DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'crops', views.CropViewSet)
router.register(r'price-records', views.PriceRecordViewSet)
router.register(r'notifications', views.NotificationViewSet)
router.register(r'market-posts', views.MarketPostViewSet)
router.register(r'price-alerts', views.PriceAlertViewSet)
router.register(r'crop-documents', CropDocumentViewSet, basename='crop-document')
router.register(r'weather', WeatherDataViewSet, basename='weather')

urlpatterns = [
    # Authentication endpoints
    path('login/', views.login_view, name='login'),
    path('auth/login/', views.login_view, name='auth_login'),
    path('logout/', views.logout_view, name='logout'),
    path('auth/logout/', views.logout_view, name='auth_logout'),
    path('register/', views.register_view, name='register'),
    path('auth/register/', views.register_view, name='auth_register'),
    path('change-password/', views.change_password_view, name='change_password'),
    path('auth/change-password/', views.change_password_view, name='auth_change_password'),
    
    # Router URLs (includes all ViewSet endpoints)
    path('', include(router.urls)),
    
    # File upload endpoints
    path('crops/<int:pk>/upload-image/', CropImageViewSet.as_view({'post': 'upload_image'})),
    path('crops/<int:pk>/delete-image/', CropImageViewSet.as_view({'delete': 'delete_image'})),
    path('crops/<int:pk>/upload-image/', views.CropViewSet.as_view({'post': 'upload_image'})),
    path('crops/<int:pk>/delete-image/', views.CropViewSet.as_view({'delete': 'delete_image'})),
    path('user/upload-profile-image/', UserProfileImageViewSet.as_view({'post': 'upload_profile_image'})),
    path('user/delete-profile-image/', UserProfileImageViewSet.as_view({'delete': 'delete_profile_image'})),
    
    # Weather endpoints
    path('weather/recommendations/', WeatherRecommendationView.as_view()),
    path('weather/analytics/', WeatherAnalyticsView.as_view()),
    
    # APIView endpoints
    path('demand/', views.DemandView.as_view()),
    path('regions/', views.RegionsView.as_view()),
    path('price-trends/<int:crop_id>/', views.PriceTrendView.as_view()),
    path('market-averages/', views.MarketAverageView.as_view()),
    path('crop-recommendations/', views.CropRecommendationView.as_view()),
    
    # Advanced Analytics endpoints
    path('analytics/advanced/', views.AdvancedAnalyticsView.as_view()),
    path('analytics/market-reports/', views.MarketReportView.as_view()),
    path('analytics/yield/', views.YieldAnalyticsView.as_view()),
    path('analytics/demand/', views.DemandAnalyticsView.as_view()),
]
