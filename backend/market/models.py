from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Count
from rest_framework.views import APIView
from rest_framework.response import Response

# =========================
# Custom User Model
# =========================
class User(AbstractUser):
    ROLE_CHOICES = (
        ('farmer', 'Farmer'),
        ('officer', 'Market Officer'),
        ('admin', 'Admin'),
    )

    # default='farmer' prevents prompt for existing users
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='farmer')
    region = models.CharField(max_length=100, blank=True, null=True)
    preferred_markets = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.username


# =========================
# Crop Model
# =========================
class Crop(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    planting_date = models.DateField(null=True, blank=True)
    expected_harvest_date = models.DateField(null=True, blank=True)
    yield_estimate = models.FloatField(null=True, blank=True)

    farmer = models.ForeignKey(
        User,
        related_name="owned_crops",
        on_delete=models.CASCADE,
        null=True,   
        blank=True
    )

    def __str__(self):
        return self.name


# =========================
# Price Record Model
# =========================
class PriceRecord(models.Model):
    crop = models.ForeignKey(
        Crop,
        related_name="prices",
        on_delete=models.CASCADE
    )
    market = models.CharField(max_length=100)
    region = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Adding null=True bypasses the migration requirement for a one-off default
    date = models.DateField(auto_now_add=True, null=True)          
    timestamp = models.DateTimeField(auto_now_add=True, null=True) 

    def __str__(self):
        return f"{self.crop.name} - {self.region} - {self.price}"


# =========================
# Price Alert Model
# =========================
class PriceAlert(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    crop = models.ForeignKey(Crop, on_delete=models.CASCADE)
    target_price = models.DecimalField(max_digits=10, decimal_places=2)
    active = models.BooleanField(default=True)


# =========================
# Notification Model
# =========================
class Notification(models.Model):
    user = models.ForeignKey(User, related_name="notifications", on_delete=models.CASCADE)
    crop = models.ForeignKey(Crop, null=True, blank=True, on_delete=models.CASCADE)
    message = models.TextField()
    
    # Adding null=True here as well
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    read = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification for {self.user.username}"


# =========================
# Farmer Marketplace Post
# =========================
class MarketPost(models.Model):
    farmer = models.ForeignKey(User, on_delete=models.CASCADE)
    crop = models.ForeignKey(Crop, on_delete=models.CASCADE)
    quantity = models.FloatField()
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    contact = models.CharField(max_length=100)


# =========================
# Demand View (for DRF API)
# =========================
class DemandView(APIView):
    def get(self, request):
        data = (
            PriceRecord.objects
            .values('crop__name', 'market')
            .annotate(records=Count('id'))
            .order_by('-records')
        )
        return Response(data)