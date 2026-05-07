from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from service.constants import ResponseMessages
from service.models import DepartmentMaster
from service.serializers import DepartmentUpdateSerializer


class DepartmentUpdateView(APIView):
    def patch(self, request):
        serializer = DepartmentUpdateSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                {
                    "success": False,
                    "message": ResponseMessages.INVALID_DATA,
                    "errors": serializer.errors
                },
                status = status.HTTP_400_BAD_REQUEST
            )

        department_id = serializer.validated_data.get("id")
        name = serializer.validated_data.get("name")

        try:
            department = DepartmentMaster.objects.get(id=department_id)
        except DepartmentMaster.DoesNotExist:
            return Response(
                {
                    "success": False,
                    "message": ResponseMessages.DEPARTMENT_NOT_FOUND
                },
                status = status.HTTP_400_BAD_REQUEST
            )

        department.name = name
        department.save()

        return Response(
            {
                "success": True,
                "message": ResponseMessages.DEPARTMENT_UPDATED
            },
            status = status.HTTP_200_OK
        )
