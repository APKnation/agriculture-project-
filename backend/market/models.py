from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('farmer', 'Farmer'),
        ('officer', 'Market Officer'),
        ('admin', 'Admin'),
    )
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='farmer')
    region = models.CharField(max_length=100, blank=True, null=True)
    preferred_markets = models.CharField(max_length=200, blank=True, null=True)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']

    def __str__(self):
        return self.username


# -----------------------------
# Proxy Models for Analytics
# -----------------------------
class DemandReport(models.Model):
    class Meta:
        managed = False   # no database table
        verbose_name = "Demand Report"
        verbose_name_plural = "Demand Reports"

class RecommendationReport(models.Model):
    class Meta:
        managed = False
        verbose_name = "Recommendation Report"
        verbose_name_plural = "Recommendation Reports"


# -----------------------------
# Crop Model
# -----------------------------
class Crop(models.Model):
    CROP_TYPES = (
        ('vegetables', 'Vegetables'),
        ('fruits', 'Fruits'),
        ('grains', 'Grains'),
        ('legumes', 'Legumes'),
    )
    
    STATUS_CHOICES = (
        ('planted', 'Planted'),
        ('growing', 'Growing'),
        ('harvested', 'Harvested'),
    )
    
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=20, choices=CROP_TYPES, default='vegetables')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='planted')
    description = models.TextField(blank=True, null=True)
    planting_date = models.DateField(null=True, blank=True)
    expected_harvest_date = models.DateField(null=True, blank=True)
    yield_estimate = models.FloatField(null=True, blank=True)
    farmer = models.ForeignKey(User, related_name="owned_crops", on_delete=models.CASCADE, null=True, blank=True)
    image = models.ImageField(upload_to='crop_images/', blank=True, null=True)
    
    def __str__(self):
        return self.name


class CropDocument(models.Model):
    crop = models.ForeignKey(Crop, related_name="documents", on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to='crop_documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    file_type = models.CharField(max_length=50, blank=True, null=True)
    file_size = models.IntegerField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.crop.name} - {self.title}"
    
    def save(self, *args, **kwargs):
        if self.file:
            self.file_type = self.file.name.split('.')[-1].upper()
            self.file_size = self.file.size
        super().save(*args, **kwargs)


class PriceRecord(models.Model):
    crop = models.ForeignKey(Crop, related_name="prices", on_delete=models.CASCADE)
    market = models.CharField(max_length=100)
    region = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(auto_now_add=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f"{self.crop.name} - {self.region} - {self.price}"


class PriceAlert(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    crop = models.ForeignKey(Crop, on_delete=models.CASCADE)
    target_price = models.DecimalField(max_digits=10, decimal_places=2)
    active = models.BooleanField(default=True)


class Notification(models.Model):
    user = models.ForeignKey(User, related_name="notifications", on_delete=models.CASCADE)
    crop = models.ForeignKey(Crop, null=True, blank=True, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    read = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification for {self.user.username}"


class MarketPost(models.Model):
    farmer = models.ForeignKey(User, on_delete=models.CASCADE)
    crop = models.ForeignKey(Crop, on_delete=models.CASCADE)
    quantity = models.FloatField()
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    contact = models.CharField(max_length=100)


# -----------------------------
# Weather Integration Models
# -----------------------------
class WeatherData(models.Model):
    region = models.CharField(max_length=100)
    date = models.DateField()
    temperature = models.FloatField(help_text="Temperature in Celsius")
    humidity = models.FloatField(help_text="Humidity percentage")
    rainfall = models.FloatField(help_text="Rainfall in mm", null=True, blank=True)
    wind_speed = models.FloatField(help_text="Wind speed in km/h", null=True, blank=True)
    weather_condition = models.CharField(max_length=50, help_text="e.g., Sunny, Cloudy, Rainy")
    data_source = models.CharField(max_length=50, default="OpenWeatherMap")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['region', 'date']
        ordering = ['-date']
    
    def __str__(self):
        return f"{self.region} - {self.date} - {self.weather_condition}"


# Severity choices used by multiple models
SEVERITY_CHOICES = (
    ('low', 'Low'),
    ('medium', 'Medium'),
    ('high', 'High'),
    ('critical', 'Critical'),
)


class WeatherAlert(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    region = models.CharField(max_length=100)
    alert_type = models.CharField(max_length=50, help_text="e.g., Frost, Heatwave, Heavy Rain")
    severity = models.CharField(max_length=20, choices=SEVERITY_CHOICES)
    message = models.TextField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.alert_type} - {self.severity}"


class CropWeatherRecommendation(models.Model):
    crop = models.ForeignKey(Crop, on_delete=models.CASCADE)
    region = models.CharField(max_length=100)
    weather_condition = models.CharField(max_length=50)
    recommendation = models.TextField(help_text="Farming recommendation based on weather")
    priority = models.CharField(max_length=20, choices=SEVERITY_CHOICES, default='medium')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['crop', 'region', 'weather_condition']
        ordering = ['-priority', 'created_at']
    
    def __str__(self):
        return f"{self.crop.name} - {self.region} - {self.weather_condition}"
