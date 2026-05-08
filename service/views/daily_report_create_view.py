from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from service.models import DailyReport, DailyTask, TaskPRLink, Users
from service.serializers import DailyReportCreateSerializer
from service.utils import Authentication

class DailyReportCreateView(APIView):
    def post(self, request):
        user, token = Authentication.authenticate(request=request)
        serializer = DailyReportCreateSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                {
                    "success": False,
                    "errors": serializer.errors
                },
                status = status.HTTP_400_BAD_REQUEST
            )
        
        report_date = serializer.validated_data.get("report_date")
        description = serializer.validated_data.get("description")
        report_status = serializer.validated_data.get("status")
        tasks = serializer.validated_data.get("tasks",[])

        existing_report = self._check_existing_report(report_date)
        if existing_report:
            return Response(
                {
                    "success": False,
                    "errors": f"Report already exists for {report_date}"
                },
                status = status.HTTP_400_BAD_REQUEST
            )
        
        for task in tasks:
            pr_link = task.get("pr_link")
            is_development_task = task.get("is_development_task")
        
            if not is_development_task and pr_link:
                return Response(
                    {
                        "success": False,
                        "errors": "PR link is allowed only for development task"
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

        daily_report = DailyReport.objects.create(
            user=user,
            report_date=report_date,
            description=description,
            status=report_status 
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
            },
            status=status.HTTP_201_CREATED
        ) 

    def _check_existing_report(self, report_date):
        return DailyReport.objects.filter(report_date=report_date).first()
