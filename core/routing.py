from django.urls import path

from channels.routing import URLRouter

from .consumers import (
    TodoListConsumer,
    TodoItemConsumer,
)


websocket_urlpatterns = URLRouter([
    path('todo_list/', TodoListConsumer.as_asgi()),
    path('todo_items/', TodoItemConsumer.as_asgi()),
])
