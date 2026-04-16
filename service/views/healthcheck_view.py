from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from service.constants import ResponseMessages


class HealthCheckView(APIView):
    def get(self, request, *args, **kwargs):
        """
        Health check endpoint to verify if the service is up and running.
        """
        return Response({
            "success": True,
            "message" : ResponseMessages.SERVICE_UP,
        }, status=status.HTTP_200_OK)
