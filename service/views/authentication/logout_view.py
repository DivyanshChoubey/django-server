from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from service.constants import ResponseMessages
from service.models import UserActiveToken
from service.utils import ResponseHandler


class LogoutView(APIView):
    def post(self, request):
        token = request.auth
        user = request.user

        if not token:
            return ResponseHandler(
                success=False,
                message=ResponseMessages.UNAUTHORIZED,
                status=status.HTTP_401_UNAUTHORIZED
            )

        updated_count = UserActiveToken.objects.filter(
            user=user,
            token=token,
            is_active=True
        ).update(is_active=False)

        if updated_count == 0:
            return ResponseHandler(
                success=False,
                message=ResponseMessages.NO_ACTIVE_SESSION_FOUND,
                status=status.HTTP_400_BAD_REQUEST
            )

        return ResponseHandler(
            success=True,
            message=ResponseMessages.LOGOUT_SUCCESS,
            status=status.HTTP_200_OK
        )
