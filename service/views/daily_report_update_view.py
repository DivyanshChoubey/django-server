from rest_framework.views import APIView
from service.utils import Authentication
from service.serializers import DailyReportUpdateSerializer
from rest_framework.response import Response
from rest_framework import status
from service.models import DailyReport, DailyTask, TaskPRLink
from service.constants import ResponseMessages


class DailyResportUpdateview(APIView):
    def patch(self, request):
        user, token = Authentication.authenticate(request=request)
        serializer = DailyReportUpdateSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                {
                    "success": False,
                    "errors": serializer.errors
                },
                status = status.HTTP_400_BAD_REQUEST
            )
        
        report_id = serializer.validated_data.get("id")
        report_date = serializer.validated_data.get("report_date")
        description = serializer.validated_data.get("description")
        report_status = serializer.validated_data.get("status")
        tasks = serializer.validated_data.get("tasks", [])

        try:
            daily_report = DailyReport.objects.get(id=report_id, user=user)
        except DailyReport.DoesNotExist:
            return Response(
                {
                    "success": False,
                    "message": ResponseMessages.Report_NOT_Found
                },
                status = status.HTTP_400_BAD_REQUEST
            )
        
        if report_date is not None:
            daily_report.report_date = report_date
        if description is not None:
            daily_report.description = description
        if report_status is not None:
            daily_report.status = report_status
        
        daily_report.save()

        for task in tasks:
            pr_link =  task.get("pr_link")
            is_development_task = task.get("is_development_task")

            if is_development_task is False and  pr_link:
                return Response(
                    {
                        "success": False,
                        "messages": ResponseMessages.INVALID_PR_LINK
                    },
                    status = status.HTTP_400_BAD_REQUEST
                )
            
            task_id = task.get("id")

            if task_id:
                try:
                    daily_task = DailyTask.objects.get(id=task_id, report = daily_report)
                except DailyTask.DoesNotExist:
                    return Response(
                        {
                            "success": False,
                            "message": ResponseMessages.TASK_NOT_Found
                        },
                        status = status.HTTP_400_BAD_REQUEST
                    )
                
                if task.get("title") is not None:
                    daily_task.title = task.get("title")
                if task.get("description") is not None:
                    daily_task.description = task.get("description")
                if task.get("is_development_task") is not None:
                    daily_task.is_development_task = task.get("is_development_task")
                if task.get("status") is not None:
                    daily_task.status = task.get("status")
                if task.get("hours") is not None:
                    daily_task.hours = task.get("hours")
                if task.get("minutes") is not None:
                    daily_task.minutes  = task.get("minutes")
                
                daily_task.save()

            else:
                daily_task = DailyTask.objects.create(
                    report=daily_report,
                    title=task.get("title"),
                    description=task.get("description"),
                    is_development_task=task.get("is_development_task", False),
                    status = task.get("status"),
                    hours=task.get("hours",0),
                    minutes=task.get("minutes",0) 
                )
            
            if is_development_task is False:
                daily_task.pr_links.all().delete()
            
            if pr_link and pr_link.get("url"):
                existing_pr_link = daily_task.pr_links.first()
            
                if existing_pr_link:
                    existing_pr_link.pr_url = pr_link.get("url")
                    existing_pr_link.save()
                else:
                    TaskPRLink.objects.create(
                        task=daily_task,
                        pr_url=pr_link.get("url")
                    )
        
        return Response(
            {
                "success": True,
                "message": ResponseMessages.REPORT_UPDATE_SUCCESS
            },
            status = status.HTTP_200_OK
        )
