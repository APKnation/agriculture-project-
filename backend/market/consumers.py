import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Notification, PriceAlert, User

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user_id = self.scope['url_route']['kwargs']['user_id']
        self.user_group_name = f'user_{self.user_id}'
        
        # Join user group
        await self.channel_layer.group_add(
            self.user_group_name,
            self.channel_name
        )
        
        await self.accept()
    
    async def disconnect(self, close_code):
        # Leave user group
        await self.channel_layer.group_discard(
            self.user_group_name,
            self.channel_name
        )
    
    async def send_notification(self, event):
        notification = event['notification']
        
        # Send notification to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'notification',
            'notification': notification
        }))
    
    async def send_price_alert(self, event):
        alert = event['alert']
        
        # Send price alert to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'price_alert',
            'alert': alert
        }))

@database_sync_to_async
def create_notification(user_id, message, crop_id=None):
    try:
        user = User.objects.get(id=user_id)
        notification = Notification.objects.create(
            user=user,
            message=message,
            crop_id=crop_id
        )
        return {
            'id': notification.id,
            'message': notification.message,
            'created_at': notification.created_at.isoformat(),
            'read': notification.read,
            'crop': notification.crop.name if notification.crop else None
        }
    except User.DoesNotExist:
        return None

@database_sync_to_async
def get_user_price_alerts(user_id):
    try:
        user = User.objects.get(id=user_id)
        alerts = PriceAlert.objects.filter(user=user, active=True)
        return [
            {
                'id': alert.id,
                'crop': alert.crop.name,
                'target_price': str(alert.target_price),
                'active': alert.active
            }
            for alert in alerts
        ]
    except User.DoesNotExist:
        return []
