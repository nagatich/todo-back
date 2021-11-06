import json
from rest_framework import status

from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_403_FORBIDDEN,
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT
)

from utils.permissions import IsOwner
from notifications.tasks import notificate_by_ws

from ..models import TodoList
from ..serializers import (
    TodoListSerializer,
    GetTodoListSerializer,
)
from ..consumers import events

class TodoListRUDView(RetrieveUpdateDestroyAPIView):
    model = TodoList
    serializer_class = TodoListSerializer
    permission_classes = [IsOwner]

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)

    def get(self, request, *args, **kwargs):
        self.serializer_class = GetTodoListSerializer
        return super().get(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        super().update(request, *args, **kwargs)
        instance = self.get_object()
        serializer = GetTodoListSerializer(instance=instance)
        room = events.TODO_LIST
        if (instance.is_private):
            room = f'{instance.user.username}_{room}'
        notificate_by_ws(room, serializer.data, events.UPDATE_TODO_LIST)
        return Response(serializer.data, status=HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        message = {
            'id': instance.id
        }
        room = events.TODO_LIST
        if (instance.is_private):
            room = f'{instance.user.username}_{room}'
        super().delete(self, request, *args, **kwargs)
        notificate_by_ws(room, message, events.DELETE_TODO_LIST)
        return Response(status=HTTP_204_NO_CONTENT)
