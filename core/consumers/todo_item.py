from channels.db import database_sync_to_async

from utils.consumers import Consumer

from ..models import TodoItem
from ..serializers import TodoItemSerializer

from .events import (
    TODO_ITEM,
    GET_TODO_ITEM,
    GET_ALL_TODO_ITEM,
)

class TodoItemConsumer(Consumer):
    model = TodoItem
    serializer_class = TodoItemSerializer

    def __init__(self, *args, **kwargs):
        super().__init__(room=TODO_ITEM, *args, **kwargs)

    async def send_on_connect(self):
        if self.scope.get('query_string_params').get('get_all') == 'true':
            todo_items = await self.get_all_todo_items()
            event = GET_ALL_TODO_ITEM
        else:
            todo_items = await self.get_todo_items()
            event = GET_TODO_ITEM
        await self.channel_layer.group_send(
            self.room,
            {
                'type': 'notificate',
                'event': event,
                'message': todo_items,
            }
        )

    @database_sync_to_async
    def get_todo_items(self):
        todo_items = self.model.objects.filter(user=self.scope['user'])
        serializer = self.serializer_class(instance=todo_items, many=True)
        return serializer.data

    @database_sync_to_async
    def get_all_todo_items(self):
        todo_items = self.model.objects.filter(is_private=False)
        serializer = self.serializer_class(instance=todo_items, many=True)
        return serializer.data

    def get_private_room(self):
        if not self.scope.get('query_string_params').get('get_all') == 'true':
            return True
        return False
