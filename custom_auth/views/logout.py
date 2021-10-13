from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.status import (
    HTTP_200_OK,
)

class LogoutAPIView(APIView):

    def get(self, request):
        request.user.auth_token.delete()
        return Response({}, status=HTTP_200_OK)
