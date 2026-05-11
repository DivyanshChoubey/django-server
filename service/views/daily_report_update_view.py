from django.db import transaction
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from service.constants import ResponseMessages
from service.models import DailyReport, DailyTask, TaskPRLink
from service.serializers import DailyReportUpdateSerializer
from service.utils import Authentication


class DailyReportUpdateView(APIView):
    def patch(self, request):
        # Auth
        user, token = Authentication.authenticate(request=request)

        # Serialize Payload
        serializer = DailyReportUpdateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {
                    "success": False,
                    "errors": serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        data = serializer.validated_data

        try:
            with transaction.atomic():
                daily_report = self._get_daily_report(
                    report_id=data.get("id"),
                    user=user,
                )

                if daily_report is None:
                    return Response(
                        {
                            "success": False,
                            "message": ResponseMessages.REPORT_NOT_FOUND,
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                self._update_daily_report(
                    daily_report=daily_report,
                    data=data,
                )

                error_response = self._process_tasks(
                    daily_report=daily_report,
                    tasks=data.get("tasks", []),
                )

                if error_response:
                    return error_response

        except Exception as e:
            print(e)
            return Response(
                {
                    "success": False,
                    "message": ResponseMessages.SOMETHING_WENT_WRONG,
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return Response(
            {
                "success": True,
                "message": ResponseMessages.REPORT_UPDATE_SUCCESS,
            },
            status=status.HTTP_200_OK,
        )

    def _get_daily_report(self, report_id, user):
        return DailyReport.objects.filter(
            id=report_id,
            user=user,
        ).first()

    def _update_daily_report(self, daily_report, data):
        if data.get("description") is not None:
            daily_report.description = data.get("description")

        if data.get("status") is not None:
            daily_report.status = data.get("status")

        daily_report.save()

    def _process_tasks(self, daily_report, tasks):
        for task_data in tasks:
            daily_task = self._get_daily_task(
                task_id=task_data.get("id"),
                daily_report=daily_report,
            )

            if daily_task is None:
                return Response(
                    {
                        "success": False,
                        "message": ResponseMessages.TASK_NOT_FOUND,
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            self._update_daily_task(
                daily_task=daily_task,
                task_data=task_data,
            )

            pr_link_data = task_data.get("pr_link")

            if pr_link_data:
                task_pr_link = self._get_task_pr_link(
                    pr_link_id=pr_link_data.get("id"),
                    daily_task=daily_task,
                )

                if task_pr_link is None:
                    return Response(
                        {
                            "success": False,
                            "message": ResponseMessages.PR_LINK_NOT_FOUND,
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                self._update_task_pr_link(
                    task_pr_link=task_pr_link,
                    pr_link_data=pr_link_data,
                )

        return None

    def _get_daily_task(self, task_id, daily_report):
        return DailyTask.objects.filter(
            id=task_id,
            report=daily_report,
        ).first()

    def _update_daily_task(self, daily_task, task_data):
        if daily_task.is_development_task is False:
            daily_task.pr_links.all().delete()
        
        if task_data.get("title") is not None:
            daily_task.title = task_data.get("title")

        if task_data.get("description") is not None:
            daily_task.description = task_data.get("description")

        if task_data.get("is_development_task") is not None:
            daily_task.is_development_task = task_data.get("is_development_task")

        if task_data.get("status") is not None:
            daily_task.status = task_data.get("status")

        if task_data.get("hours") is not None:
            daily_task.hours = task_data.get("hours")

        if task_data.get("minutes") is not None:
            daily_task.minutes = task_data.get("minutes")

        daily_task.save()

    def _get_task_pr_link(self, pr_link_id, daily_task):
        return TaskPRLink.objects.filter(
            id=pr_link_id,
            task=daily_task,
        ).first()

    def _update_task_pr_link(self, task_pr_link, pr_link_data):
        if pr_link_data.get("url") is not None:
            task_pr_link.pr_url = pr_link_data.get("url")

        task_pr_link.save()
