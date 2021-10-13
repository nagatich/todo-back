from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_200_OK,
)

from ..serializers import UserSerializer

class LoginAPIView(ObtainAuthToken):
    user_serializer = UserSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            data = self.user_serializer(user)
            return Response(data.data, status=HTTP_200_OK)
        return Response({'error': 'Неверный логин или пароль'}, status=HTTP_400_BAD_REQUEST)
