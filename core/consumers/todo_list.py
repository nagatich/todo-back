from channels.db import database_sync_to_async

from utils.consumers import Consumer

from ..models import (
    TodoList,
)
from ..serializers import TodoListSerializer

from .events import (
    TODO_LIST,
    GET_TODO_LIST,
    GET_ALL_TODO_LIST,
)

class TodoListConsumer(Consumer):
    model = TodoList
    serializer_class = TodoListSerializer

    def __init__(self, *args, **kwargs):
        super().__init__(room=TODO_LIST, *args, **kwargs)

    async def send_on_connect(self):
        if self.scope.get('query_string_params').get('get_all') == 'true':
            todo_list = await self.get_all_todo_list()
            event = GET_ALL_TODO_LIST
        else:
            todo_list = await self.get_todo_list()
            event = GET_TODO_LIST
        await self.channel_layer.group_send(
            self.room,
            {
                'type': 'notificate',
                'event': event,
                'message': todo_list,
            }
        )

    @database_sync_to_async
    def get_todo_list(self):
        todo_list = self.model.objects.filter(user=self.scope['user'])
        serializer = self.serializer_class(instance=todo_list, many=True)
        return serializer.data

    @database_sync_to_async
    def get_all_todo_list(self):
        todo_list = self.model.objects.filter(is_private=False)
        serializer = self.serializer_class(instance=todo_list, many=True)
        return serializer.data

    def get_private_room(self):
        if not self.scope.get('query_string_params').get('get_all') == 'true':
            return True
        return False
