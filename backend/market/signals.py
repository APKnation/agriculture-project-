from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import PriceRecord, PriceAlert, Notification

@receiver(post_save, sender=PriceRecord)
def check_price_alert(sender, instance, created, **kwargs):
    if not created:
        return

    alerts = PriceAlert.objects.filter(
        crop=instance.crop,
        target_price__lte=instance.price,
        active=True
    )

    for alert in alerts:
        Notification.objects.create(
            user=alert.user,
            crop=instance.crop,
            message=f"Best time to sell {instance.crop.name}!"
        )
        alert.active = False
        alert.save()
