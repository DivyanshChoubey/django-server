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
        user, token = Authentication.authenticate(request=request)

        serializer = DailyReportUpdateSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                {
                    "success": False,
                    "errors": serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        return self._update_daily_report_data(
            user=user,
            validated_data=serializer.validated_data,
        )

    def _update_daily_report_data(self, user, validated_data):
        try:
            with transaction.atomic():
                daily_report = self._get_daily_report(
                    report_id=validated_data.get("id"),
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

                self._update_instance_fields(
                    instance=daily_report,
                    data=validated_data,
                    allowed_fields=["report_date", "description", "status"],
                )

                error_response = self._process_tasks(
                    daily_report=daily_report,
                    tasks=validated_data.get("tasks", []),
                )

                if error_response:
                    return error_response

        except Exception:
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

    def _process_tasks(self, daily_report, tasks):
        for task in tasks:
            daily_task = self._update_or_create_task(
                daily_report=daily_report,
                task=task,
            )

            if daily_task is None:
                return Response(
                    {
                        "success": False,
                        "message": ResponseMessages.TASK_NOT_FOUND,
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            self._handle_pr_link(
                daily_task=daily_task,
                task=task,
            )

        return None

    def _update_or_create_task(self, daily_report, task):
        task_id = task.get("id")

        if task_id:
            daily_task = DailyTask.objects.filter(
                id=task_id,
                report=daily_report,
            ).first()

            if daily_task is None:
                return None

            self._update_instance_fields(
                instance=daily_task,
                data=task,
                allowed_fields=[
                    "title",
                    "description",
                    "is_development_task",
                    "status",
                    "hours",
                    "minutes",
                ],
            )

            return daily_task

        return DailyTask.objects.create(
            report=daily_report,
            title=task.get("title"),
            description=task.get("description"),
            is_development_task=task.get("is_development_task", False),
            status=task.get("status"),
            hours=task.get("hours", 0),
            minutes=task.get("minutes", 0),
        )

    def _update_instance_fields(self, instance, data, allowed_fields):
        updated_fields = []

        for field in allowed_fields:
            if field in data and data.get(field) is not None:
                setattr(instance, field, data.get(field))
                updated_fields.append(field)

        if updated_fields:
            instance.save(update_fields=updated_fields)

    def _handle_pr_link(self, daily_task, task):
        pr_link = task.get("pr_link")

        if daily_task.is_development_task is False:
            daily_task.pr_links.all().delete()
            return

        if not pr_link:
            return

        pr_url = pr_link.get("url")

        if not pr_url:
            return

        TaskPRLink.objects.update_or_create(
            task=daily_task,
            defaults={"pr_url": pr_url},
        )
