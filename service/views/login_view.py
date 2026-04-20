import jwt
import bcrypt
from datetime import datetime, timedelta
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from service.models import Users, UserActiveToken
from service.serializers import LoginSerializer
from service.constants.response_messages import ResponseMessages
from django.conf import settings


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

        email = serializer.validated_data["email"]
        password = serializer.validated_data["password"]

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

        if not bcrypt.checkpw(password.encode("utf-8"), user.password.encode("utf-8")):
            return Response(
                {
                    "success": False,
                    "message": ResponseMessages.INCORRECT_PASSWORD
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        expiry_time = datetime.utcnow() + timedelta(days=1)
        payload = {
            "user_id": user.id,
            "email": user.email,
            "exp": expiry_time
        }
        token = jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
        UserActiveToken.objects.create(
            user_id=user,
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
