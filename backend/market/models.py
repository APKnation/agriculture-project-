from django.contrib.auth.models import AbstractUser
from django.db import models

# =========================
# Custom User Model
# =========================
class User(AbstractUser):
    ROLE_CHOICES = (
        ('farmer', 'Farmer'),
        ('officer', 'Market Officer'),
        ('admin', 'Admin'),
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES
    )
    region = models.CharField(max_length=100, blank=True, null=True)
    preferred_markets = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.username


# =========================
# Crop Model
# =========================
class Crop(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)   # ✅ allow nulls to avoid migration errors
    planting_date = models.DateField(null=True, blank=True)
    expected_harvest_date = models.DateField(null=True, blank=True)
    yield_estimate = models.FloatField(null=True, blank=True)

    farmer = models.ForeignKey(
        User,
        related_name="owned_crops",
        on_delete=models.CASCADE,
        null=True,   # ✅ allow nulls so existing rows don’t break
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
    region = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.crop.name} - {self.region} - {self.price}"


# =========================
# Notification Model
# =========================
class Notification(models.Model):
    user = models.ForeignKey(
        User,
        related_name="notifications",
        on_delete=models.CASCADE
    )
    crop = models.ForeignKey(Crop, on_delete=models.CASCADE, null=True, blank=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification for {self.user.username}"
