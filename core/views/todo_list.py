from os import stat
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST

from notifications.tasks import notificate_by_ws

from ..consumers import events
from ..models import TodoList
from ..serializers import (
    TodoListSerializer,
    GetTodoListSerializer,
)

class TodoListView(generics.ListCreateAPIView):
    model = TodoList
    serializer_class = TodoListSerializer

    def get_queryset(self):
        if self.request.GET.get('get_all', None) == 'true':
            return self.model.objects.filter(is_private=False)
        return self.model.objects.filter(user=self.request.user)

    def get(self, request, *args, **kwargs):
        self.serializer_class = GetTodoListSerializer
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        request.data['user'] = request.user.id
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
        todo_list = serializer.save()
        room = events.TODO_LIST
        if todo_list.is_private:
            room = f'{todo_list.user.username}_{room}'
        notificate_by_ws(room, serializer.data, events.CREATE_TODO_LIST)
        return Response(serializer.data, status=HTTP_201_CREATED)
