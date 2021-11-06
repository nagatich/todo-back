from utils.serializers import DynamicFieldsModelSerializer
from custom_auth.serializers.get_user import GetUserSerializer

from ..models import (
    TodoList,
)

from .todo_item import TodoItemSerializer

class GetTodoListSerializer(DynamicFieldsModelSerializer):
    tasks = TodoItemSerializer(many=True, exclude=['user'])
    user = GetUserSerializer()

    class Meta:
        model = TodoList
        fields = '__all__'
