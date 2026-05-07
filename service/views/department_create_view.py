from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from service.constants import Constants, ResponseMessages
from service.models import DepartmentMaster, Users
from service.serializers import DepartmentCreateSerializer


class DepartmentCreateView(APIView):
    def post(self,request):
        serializer = DepartmentCreateSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                {
                    "success": False,
                    "message": ResponseMessages.INVALID_DATA,
                    "errors": serializer.errors
                },
                status = status.HTTP_400_BAD_REQUEST
            )

        name = serializer.validated_data.get("name")
        created_by = serializer.validated_data.get("created_by")

        user = None
        if created_by is not None:
            try:
                user = Users.objects.get(id = created_by, user_type__in=[Constants.ADMIN, Constants.SUPER_ADMIN])
            except Users.DoesNotExist:
                return Response(
                    {
                        "success": False,
                        "message": ResponseMessages.INVALID_CREATED_BY
                    },
                    status = status.HTTP_400_BAD_REQUEST
                )
            
        department = DepartmentMaster.objects.create(
            name = name,
            created_by = user
        )

        return Response(
            {
                "success": True,
                "message": ResponseMessages.DEPARTMENT_CREATED,
                "data": {
                    "id": department.id,
                    "name": department.name
                }
            },
            status = status.HTTP_201_CREATED
        )
