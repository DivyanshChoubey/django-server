from rest_framework.views import APIView
from service.utils import Authentication
from service.serializers import DailyReportUpdateSerializer
from rest_framework.response import Response
from rest_framework import status
from service.models import DailyReport, DailyTask, TaskPRLink
from service.constants import ResponseMessages


class DailyReportUpdateView(APIView):
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
        
        daily_report = self._get_daily_report(
            report_id=serializer.validated_data.get("id"),
            user=user
        )

        if daily_report is None : 
            return Response(
                {
                    "success": False,
                    "message": ResponseMessages.REPORT_NOT_FOUND
                },
                status = status.HTTP_400_BAD_REQUEST
            )
        
        self._update_daily_report(
            daily_report=daily_report,
            data=serializer.validated_data
        )
        
        error_response = self._process_tasks(
            daily_report=daily_report,
            tasks=serializer.validated_data.get("tasks", [])
        )

        if error_response:
            return error_response
        
        return Response(
            {
                "success": True,
                "message": ResponseMessages.REPORT_UPDATE_SUCCESS
            },
            status = status.HTTP_200_OK
        )


    def _get_daily_report(self, report_id, user):
        return DailyReport.objects.filter(id=report_id, user=user).first()

    def _update_daily_report(self, daily_report, data):
        if data.get("report_date") is not None:
            daily_report.report_date = data.get("report_date")

        if data.get("description") is not None:
            daily_report.description = data.get("description")

        if data.get("status") is not None:
            daily_report.status = data.get("status")

        daily_report.save()

    def _process_tasks(self, daily_report, tasks):
        for task in tasks:
            error_response = self._validate_pr_link(task)

            if error_response:
                return error_response

            daily_task = self._update_or_create_task(
                daily_report=daily_report,
                task=task
            )

            if daily_task is None:
                return Response(
                    {
                        "success": False,
                        "message": ResponseMessages.TASK_NOT_FOUND
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            self._handle_pr_link(
                daily_task=daily_task,
                task=task
            )

        return None

    def _validate_pr_link(self, task):
        pr_link = task.get("pr_link")
        is_development_task = task.get("is_development_task")

        if is_development_task is False and pr_link:
            return Response(
                {
                    "success": False,
                    "message": ResponseMessages.INVALID_PR_LINK
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        return None

    def _update_or_create_task(self, daily_report, task):
        task_id = task.get("id")

        if task_id:
            daily_task = DailyTask.objects.filter(
                id=task_id,
                report=daily_report
            ).first()

            if daily_task is None:
                return None

            self._update_task_fields(
                daily_task=daily_task,
                task=task
            )

            return daily_task

        return DailyTask.objects.create(
            report=daily_report,
            title=task.get("title"),
            description=task.get("description"),
            is_development_task=task.get("is_development_task", False),
            status=task.get("status"),
            hours=task.get("hours", 0),
            minutes=task.get("minutes", 0)
        )

    def _update_task_fields(self, daily_task, task):
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
            daily_task.minutes = task.get("minutes")

        daily_task.save()

    def _handle_pr_link(self, daily_task, task):
        pr_link = task.get("pr_link")
        is_development_task = task.get("is_development_task")

        if is_development_task is False:
            daily_task.pr_links.all().delete()
            return

        if pr_link and pr_link.get("url"):
            existing_pr_link = daily_task.pr_links.first()

            if existing_pr_link:
                existing_pr_link.pr_url = pr_link.get("url")
                existing_pr_link.save()
                return

            TaskPRLink.objects.create(
                task=daily_task,
                pr_url=pr_link.get("url")
            )
