import json

from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_403_FORBIDDEN,
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT
)
from core.models import todo_list
from notifications import tasks

from utils.permissions import IsOwner
from notifications.tasks import notificate_by_ws

from ..models import (
    TodoItem,
    TodoList,
)
from ..serializers import (
    TodoItemSerializer,
)
from ..consumers import events

class TodoItemRUDView(RetrieveUpdateDestroyAPIView):
    model = TodoItem
    serializer_class = TodoItemSerializer
    permission_classes = [IsOwner]

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)

    def update(self, request, *args, **kwargs):
        super().update(request, *args, **kwargs)
        instance = self.get_object()
        serializer = self.serializer_class(instance=instance)
        todo_lists = TodoList.objects.filter(tasks__id=instance.id)

        room = events.TODO_LIST if len(instance.parents) != 0 else events.TODO_ITEM
        message = serializer.data
        message['todo_lists'] = [todo_list.id for todo_list in todo_lists]
        if (instance.is_private):
            room = f'{instance.user.username}_{room}'
        notificate_by_ws(room, message, events.UPDATE_TODO_ITEM)
        return Response(serializer.data, status=HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        todo_lists = TodoList.objects.filter(tasks__id=instance.id)
        message = {
            'id': instance.id,
            'todo_lists': [todo_list.id for todo_list in todo_lists],
        }
        room = events.TODO_LIST if len(instance.parents) != 0 else events.TODO_ITEM
        if (instance.is_private):
            room = f'{instance.user.username}_{room}'
        super().delete(self, request, *args, **kwargs)
        notificate_by_ws(room, message, events.DELETE_TODO_ITEM)
        return Response(status=HTTP_204_NO_CONTENT)
