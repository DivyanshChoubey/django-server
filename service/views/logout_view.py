from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from service.constants import ResponseMessages
from service.models import UserActiveToken
from service.serializers import LogoutSerializer


class LogoutView(APIView):
    def post(self, request):
        serializer = LogoutSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                {
                    "success": False,
                    "message": ResponseMessages.INVALID_DATA,
                    "errors": serializer.errors
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        user_id = serializer.validated_data.get("user_id")
        updated_count = UserActiveToken.objects.filter(
            user_id=user_id,
            is_active=True
        ).update(is_active=False)

        if updated_count == 0:
            return Response(
                {
                    "success": False,
                    "message": ResponseMessages.NO_ACTIVE_SESSION_FOUND
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {
                "success": True,
                "message": ResponseMessages.LOGOUT_SUCCESS
            },
            status=status.HTTP_200_OK
        )
