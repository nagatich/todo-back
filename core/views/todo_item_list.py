from rest_framework import generics
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST

from core.consumers import events
from core.models import todo_list
from notifications.tasks import notificate_by_ws

from ..models import (
    TodoItem,
    TodoList,
)
from ..serializers import (
    TodoItemSerializer,
)

class TodoItemListView(generics.ListCreateAPIView):
    model = TodoItem
    serializer_class = TodoItemSerializer

    def get_queryset(self):
        if self.request.GET.get('get_all', None) == 'true':
            return self.model.objects.filter(is_private=False)
        return self.model.objects.filter(user=self.request.user)

    def post(self, request, *args, **kwargs):
        request.data['user'] = request.user.id
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
        item = serializer.save()
        todo_list_id = request.data.get('todolist', None)
        message = serializer.data
        room = events.TODO_ITEM
        if todo_list_id:
            todo_list = TodoList.objects.filter(id=todo_list_id).first()
            if todo_list:
                room = events.TODO_LIST
                todo_list.tasks.add(item.id)
                message['todolist'] = todo_list.id
        if item.is_private:
            room = f'{item.user.username}_{room}'
        notificate_by_ws(room, message, events.CREATE_TODO_ITEM)
        return Response(serializer.data, status=HTTP_201_CREATED)
