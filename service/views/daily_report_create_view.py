from rest_framework.views import APIView
from service.serializers import DailyReportCreateSerializer
from rest_framework.response import Response
from service.constants import ResponseMessages
from rest_framework import status
from service.models import Users, DailyReport, DailyTask, TaskPRLink


class DailyReportCreateView(APIView):
    def post(self, request):
        serializer = DailyReportCreateSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                {
                    "success": False,
                    "errors": serializer.errors
                },
                status = status.HTTP_400_BAD_REQUEST
            )
        
        user_id = serializer.validated_data.get("user_id")
        report_date = serializer.validated_data.get("report_date")
        description = serializer.validated_data.get("description")
        report_status = serializer.validated_data.get("status")
        tasks = serializer.validated_data.get("tasks",[])

        try:
            user = Users.objects.get(id=user_id)
        except Users.DoesNotExist:
            return Response(
                {
                    "success": False,
                    "message": ResponseMessages.INVALID_USER
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
        daily_report = DailyReport.objects.create(
            user = user,
            report_date = report_date,
            description = description,
            status = report_status 
        )

        for task in tasks:
            pr_link = task.get("pr_link")
            daily_task = DailyTask.objects.create(
                report=daily_report,
                title=task.get("title"),
                description=task.get("description"),
                is_development_task=task.get("is_development_task"),
                status=task.get("status"),
                hours=task.get("hours"),
                minutes=task.get("minutes")
            )

            if pr_link:
                TaskPRLink.objects.create(
                    task=daily_task,
                    pr_url=pr_link.get("url")
                )

        return Response(
            {
                "success": True,
                "message": "Daily report created successfully",
                "data": {
                    "id": daily_report.id,
                    "report_date": daily_report.report_date,
                    "status": daily_report.status
                }
            },
            status=status.HTTP_201_CREATED
        ) 
