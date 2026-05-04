from datetime import timedelta
import bcrypt
import jwt
from django.conf import settings
from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from service.constants import ResponseMessages
from service.models import UserActiveToken, Users
from service.serializers import LoginSerializer


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                {
                    "success": False,
                    "message": ResponseMessages.INVALID_DATA,
                    "errors": serializer.errors
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        email = serializer.validated_data.get("email")
        password = serializer.validated_data.get("password")

        try:
            user = Users.objects.get(email=email)
        except Users.DoesNotExist:
            return Response(
                {
                    "success": False,
                    "message": ResponseMessages.EMAIL_NOT_EXISTS
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        if not self.check_password(password, user.password):
            return Response(
                {
                    "success": False,
                    "message": ResponseMessages.INCORRECT_PASSWORD
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        payload = {
            "user_id": user.id,
            "user_type": user.user_type,
            "iat": timezone.now().timestamp()
        }

        token = jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)

        UserActiveToken.objects.filter(
            user=user,
            is_active=True
        ).update(is_active=False)

        UserActiveToken.objects.create(
            user=user,
            token=token,
            is_active=True,
            expire_at=timezone.now() + timedelta(days=1)
        )

        return Response(
            {
                "success": True,
                "message": ResponseMessages.LOGIN_SUCCESS,
                "data": {
                    "token": token,
                    "user_id": user.id
                }
            },
            status=status.HTTP_200_OK
        )
    
    def check_password(self, input_password, actual_password):
        return bcrypt.checkpw(
        input_password.encode("utf-8"),
        actual_password.encode("utf-8")
    )
