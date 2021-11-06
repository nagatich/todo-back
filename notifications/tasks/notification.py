from django.contrib.auth.models import User

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from todo.celery import app

@app.task
def notificate_user_by_ws(user_id, message, event=None, data=None):
    user = User.objects.get(id=user_id)
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f'{user.username}_room_notifications',
        {
            'type': 'notificate',
            'event': event or 'notifications',
            'message': message,
            'data': data,
        }
    )

@app.task
def notificate_by_ws(room, message, event=None):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        room,
        {
            'type': 'notificate',
            'event': event or 'notifications',
            'message': message,
        }
    )
