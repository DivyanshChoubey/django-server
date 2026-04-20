import bcrypt
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from service.constants import ResponseMessages
from service.models import Roles, Users
from service.serializers import RegisterSerializer


class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {
                    "success": False,
                    "message": ResponseMessages.INVALID_DATA,
                    "errors": serializer.errors
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        validated_data = serializer.validated_data
        email = validated_data.get("email")

        if Users.objects.filter(email=email).exists():
            return Response(
                {
                    "success": False,
                    "message": ResponseMessages.USER_ALREADY_EXISTS
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            role = Roles.objects.get(id=validated_data.get("role_id"))
        except Roles.DoesNotExist:
            return Response(
                {
                    "success": False,
                    "message": ResponseMessages.INVALID_ROLE
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        hashed_password = bcrypt.hashpw(
            validated_data.get("password").encode("utf-8"),
            bcrypt.gensalt()
        ).decode("utf-8")

        Users.objects.create(
            first_name=validated_data.get("first_name"),
            last_name=validated_data.get("last_name"),
            email=validated_data.get("email"),
            password=hashed_password,
            role=role,
            bio=validated_data.get("bio", ""),
            position_name=validated_data.get("position_name")
        )

        return Response(
            {
                "success": True,
                "message": ResponseMessages.USER_CREATED
            },
            status=status.HTTP_201_CREATED
        )
