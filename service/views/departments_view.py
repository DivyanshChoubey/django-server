from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from service.constants import ResponseMessages
from service.models import DepartmentMaster
from service.serializers import DepartmentSerializer


class DepartmentsView(APIView):
    def get(self, request):
        departments = DepartmentMaster.objects.all().order_by("-id")
        serializer = DepartmentSerializer(departments, many =True)

        return Response(
            {
                "success": True,
                "message": ResponseMessages.DEPARTMENT_FETCH,
                "data": serializer.data
            },
            status= status.HTTP_200_OK
        )
