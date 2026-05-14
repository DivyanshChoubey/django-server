from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from service.utils import ResponseHandler


from service.constants import ResponseMessages


class HealthCheckView(APIView):
    permission_classes = [AllowAny]
    def get(self, request, *args, **kwargs):
        """
        Health check endpoint to verify if the service is up and running.
        """
        return ResponseHandler(
            success=True,
            message=ResponseMessages.SERVICE_UP,
            status=status.HTTP_200_OK
        )
