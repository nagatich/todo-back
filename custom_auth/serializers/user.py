from django.contrib.auth.models import User

from rest_framework import serializers
from rest_framework.authtoken.models import Token

class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    token = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
            'token',
        ]

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

    def get_token(self, user):
        token, created = Token.objects.get_or_create(user=user)
        return token.key
