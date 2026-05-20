from rest_framework import status
from rest_framework.views import APIView

from service.constants import Constants, ResponseMessages
from service.models import DepartmentMaster, Users
from service.serializers import (DepartmentCreateSerializer,
                                 DepartmentSerializer,
                                 DepartmentUpdateSerializer)
from service.utils import ResponseHandler


class DepartmentView(APIView):
    def get(self, request):
        departments = DepartmentMaster.objects.all().order_by("-id")
        serializer = DepartmentSerializer(departments, many =True)

        return ResponseHandler(
            success=True,
            message=ResponseMessages.DEPARTMENT_FETCH,
            data=serializer.data,
            status= status.HTTP_200_OK
        )
    
    def post(self,request):
        serializer = DepartmentCreateSerializer(data=request.data)

        if not serializer.is_valid():
            return ResponseHandler(
                success=False,
                message=ResponseMessages.INVALID_DATA,
                errors=serializer.errors,
                status = status.HTTP_400_BAD_REQUEST
            )

        name = serializer.validated_data.get("name")
        created_by = serializer.validated_data.get("created_by")

        user = None
        if created_by is not None:
            try:
                user = Users.objects.get(id = created_by, user_type__in=[Constants.ADMIN, Constants.SUPER_ADMIN])
            except Users.DoesNotExist:
                return ResponseHandler(
                    success=False,
                    message=ResponseMessages.INVALID_CREATED_BY,
                    status = status.HTTP_400_BAD_REQUEST
                )
            
        department = DepartmentMaster.objects.create(
            name = name,
            created_by = user
        )

        return ResponseHandler(
            success=True,
            message=ResponseMessages.DEPARTMENT_CREATED,
            data={
                "id": department.id,
                "name": department.name
            },
            status = status.HTTP_201_CREATED
        )

    def patch(self, request):
        serializer = DepartmentUpdateSerializer(data=request.data)

        if not serializer.is_valid():
            return ResponseHandler(
                success=False,
                message=ResponseMessages.INVALID_DATA,
                errors=serializer.errors,
                status = status.HTTP_400_BAD_REQUEST
            )

        department_id = serializer.validated_data.get("id")
        name = serializer.validated_data.get("name")

        try:
            department = DepartmentMaster.objects.get(id=department_id)
        except DepartmentMaster.DoesNotExist:
            return ResponseHandler(
                success=False,
                message=ResponseMessages.DEPARTMENT_NOT_FOUND,
                status = status.HTTP_400_BAD_REQUEST
            )

        department.name = name
        department.save()

        return ResponseHandler(
            success=True,
            message=ResponseMessages.DEPARTMENT_UPDATED,
            status = status.HTTP_200_OK
        )
