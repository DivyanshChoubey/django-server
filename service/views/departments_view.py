from rest_framework.views import APIView
from service.models import DepartmentMaster
from service.serializers import DepartmentSerializer
from rest_framework.response import Response
from service.constants import ResponseMessages
from rest_framework import status


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