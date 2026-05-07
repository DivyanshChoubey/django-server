from rest_framework.views import APIView
from rest_framework import status

from service.constants import ResponseMessages
from service.models import DailyReport
from service.serializers import DailyReportGetSerializer
from rest_framework.response import Response

class DailyReportView(APIView):
    def get(self,request):
        daily_report = DailyReport.objects.all().order_by("-id")
        serializer = DailyReportGetSerializer(daily_report, many=True)

        return Response(
            {
                "success": True,
                "message": ResponseMessages.DAILY_REPORT_FETCH,
                "data": serializer.data
            },
            status = status.HTTP_200_OK
        )
