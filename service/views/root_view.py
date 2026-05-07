import os

from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from service.constants import ResponseMessages


class RootView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        return Response({
            "data" : {
                "environment": os.getenv("APP_ENVIRONMENT"),
                "is_debug_mode": os.getenv("DJANGO_DEBUG")
            },
            "message" : ResponseMessages.ROOT_MESSAGE
        })
