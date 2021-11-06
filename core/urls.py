from django.urls import path

from .views import (
    TodoListRUDView,
    TodoListView,
    TodoItemListView,
    TodoItemRUDView,
)

urlpatterns = [
    path('list/', TodoListView.as_view()),
    path('list/<int:pk>', TodoListRUDView.as_view()),
    path('items/', TodoItemListView.as_view()),
    path('items/<int:pk>', TodoItemRUDView.as_view()),
]
