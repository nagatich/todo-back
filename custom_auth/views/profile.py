from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_200_OK,
)

from ..serializers import UserSerializer

class ProfileAPIView(APIView):
    serializer_class = UserSerializer

    def get(self, request):
        serializer = self.serializer_class(instance=request.user)
        return Response(serializer.data, status=HTTP_200_OK)
