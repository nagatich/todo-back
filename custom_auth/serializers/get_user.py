from django.contrib.auth.models import User

from rest_framework import serializers
from rest_framework.authtoken.models import Token

class GetUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
        ]
