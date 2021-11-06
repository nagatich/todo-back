from utils.serializers import DynamicFieldsModelSerializer
from custom_auth.serializers import GetUserSerializer

from ..models import (
    TodoList,
)

class TodoListSerializer(DynamicFieldsModelSerializer):
    user = GetUserSerializer()

    class Meta:
        model = TodoList
        fields = '__all__'
