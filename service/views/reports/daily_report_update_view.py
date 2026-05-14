from django.db import transaction
from rest_framework import status
from rest_framework.views import APIView

from service.constants import ResponseMessages
from service.models import DailyReport, DailyTask, TaskPRLink
from service.serializers import DailyReportUpdateSerializer
from service.utils import Authentication , ResponseHandler


class DailyReportUpdateView(APIView):
    serializer_class = DailyReportUpdateSerializer

    def patch(self, request):
        # Auth
        user, token = Authentication.authenticate(request=request)

        # Serialize Payload
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return ResponseHandler(
                success=False,
                errors=serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        data = serializer.validated_data

        try:
            with transaction.atomic():
                daily_report = self._get_daily_report(
                    report_id=data.get("id"),
                    user=user,
                )

                if daily_report is None:
                    return ResponseHandler(
                        success=False,
                        message=ResponseMessages.REPORT_NOT_FOUND,
                        status=status.HTTP_400_BAD_REQUEST
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
                
                return ResponseHandler(
                    success=True,
                    message=ResponseMessages.REPORT_UPDATE_SUCCESS,
                    status=status.HTTP_201_CREATED
                )

        except Exception as e:
            print(e)
            return ResponseHandler(
                success=False,
                message=ResponseMessages.SOMETHING_WENT_WRONG,
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
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
            task_id = task_data.get("id")

            if task_id:
                daily_task = self._get_daily_task(
                    task_id=task_id,
                    daily_report=daily_report,
                )

                if daily_task is None:
                    return ResponseHandler(
                        success=False,
                        message=ResponseMessages.TASK_NOT_FOUND,
                        status=status.HTTP_400_BAD_REQUEST
                    )

                self._update_daily_task(
                    daily_task=daily_task,
                    task_data=task_data,
                )

            else:
                daily_task = self._create_daily_task(
                    daily_report=daily_report,
                    task_data=task_data,
                )

            pr_link_list = task_data.get("pr_link", [])

            if pr_link_list and daily_task.is_development_task:
                error_response = self._process_pr_links(
                    daily_task=daily_task,
                    pr_link_list=pr_link_list,
                )

                if error_response:
                    return error_response

        return None

    def _get_daily_task(self, task_id, daily_report):
        return DailyTask.objects.filter(
            id=task_id,
            report=daily_report,
        ).first()

    def _update_daily_task(self, daily_task, task_data):
        if task_data.get("title") is not None:
            daily_task.title = task_data.get("title")

        if task_data.get("description") is not None:
            daily_task.description = task_data.get("description")

        if task_data.get("is_development_task") is not None:
            is_development = daily_task.is_development_task
            if is_development and task_data.get("is_development_task") is False:
                self._remove_pr_links(task=daily_task)
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

    def _remove_pr_links(self, task):
        TaskPRLink.objects.filter(task=task).delete()

    def _create_daily_task(self, daily_report, task_data):
        return DailyTask.objects.create(
            report=daily_report,
            title=task_data.get("title"),
            description=task_data.get("description"),
            is_development_task=task_data.get("is_development_task", False),
            status=task_data.get("status"),
            hours=task_data.get("hours", 0),
            minutes=task_data.get("minutes", 0),
        )


    def _create_task_pr_link(self, daily_task, pr_link_data):
        if pr_link_data.get("url"):
            return TaskPRLink.objects.create(
                task=daily_task,
                pr_url=pr_link_data.get("url"),
            )

        return None

    def _process_pr_links(self, daily_task, pr_link_list):
        for pr_link_data in pr_link_list:
            pr_link_id = pr_link_data.get("id")

            if pr_link_id:
                task_pr_link = self._get_task_pr_link(
                    pr_link_id=pr_link_id,
                    daily_task=daily_task,
                )

                if task_pr_link is None:
                    return ResponseHandler(
                        success=False,
                        message=ResponseMessages.PR_LINK_NOT_FOUND,
                        status=status.HTTP_400_BAD_REQUEST
                    )

                self._update_task_pr_link(
                    task_pr_link=task_pr_link,
                    pr_link_data=pr_link_data,
                )

            else:
                self._create_task_pr_link(
                    daily_task=daily_task,
                    pr_link_data=pr_link_data,
                )

        return None
