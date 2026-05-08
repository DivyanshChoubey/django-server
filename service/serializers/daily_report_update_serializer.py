from rest_framework import serializers
from service.constants import TaskConstants, DailyReportConstants


class TaskPRLinkUpdateSerializer(serializers.Serializer):
    url = serializers.URLField(required=False, allow_blank=True)


class DailyTaskUpdateSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False, allow_null=True)
    title = serializers.CharField(max_length=255, required = False)
    description = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    is_development_task = serializers.BooleanField(required=False)
    pr_link = TaskPRLinkUpdateSerializer(required=False)
    status = serializers.ChoiceField(
        choices=TaskConstants.STATUS_CHOICES,
        required=False
    )
    hours = serializers.IntegerField(required=False)
    minutes = serializers.IntegerField(required=False)


class DailyReportUpdateSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    report_date = serializers.DateField(required=False)
    description = serializers.CharField(required=False, allow_blank=True, allow_null =True)
    status = serializers.ChoiceField(
        choices=DailyReportConstants.STATUS_CHOICES,
        required=False 
    )
    tasks = DailyTaskUpdateSerializer(many=True, required=False)
