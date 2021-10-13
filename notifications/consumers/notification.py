import json

from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async

from asgiref.sync import async_to_sync, sync_to_async

from ..models import Notification
from ..serializers import NotificationSerializer
from ..events import NOTIFICATIONS

class NotificationConsumer(AsyncJsonWebsocketConsumer):
    room = None

    async def connect(self):
        try:
            self.user = self.scope.get('user')
            if self.user.is_anonymous:
                await self.close()

            self.room = f'{self.user.username}_room_notifications'
            if self.room:
                await self.accept()
                await self.channel_layer.group_add(self.room, self.channel_name)
                await self.send_unseen_notifications()
            else:
                await self.close()
        except:
            await self.close()

    async def disconnect(self, code):
        if self.room is not None:
            await self.channel_layer.group_discard(self.room, self.channel_name)

    async def receive(self, text_data):
        await self.channel_layer.group_send(
            self.room,
            {
                'type': 'notificate',
                'event': NOTIFICATIONS,
                'message': json.loads(text_data)
            }
        )

    async def send_unseen_notifications(self):
        notifications = await self.get_notifications()
        await self.channel_layer.group_send(
            self.room,
            {
                'type': 'notificate',
                'event': NOTIFICATIONS,
                'message': notifications,
            }
        )

    @database_sync_to_async
    def get_notifications(self):
        notifications = Notification.objects.filter(to_user=self.user, seen=False)
        serializer = NotificationSerializer(instance=notifications, many=True)
        return serializer.data

    async def notificate(self, event):
        await self.send_json(event)
