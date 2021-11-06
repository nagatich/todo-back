from rest_framework import serializers

from utils.serializers import DynamicFieldsModelSerializer
from custom_auth.serializers.get_user import GetUserSerializer

from ..models import TodoItem

class TodoItemSerializer(DynamicFieldsModelSerializer):
    user = GetUserSerializer()
    parents = serializers.SerializerMethodField()

    class Meta:
        model = TodoItem
        fields = '__all__'

    def get_parents(self, instance):
        return instance.parents
