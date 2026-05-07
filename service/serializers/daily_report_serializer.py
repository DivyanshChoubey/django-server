from rest_framework import serializers
from service.constants import DailyReportConstants, TaskConstants


class TaskPRLinkSerializer(serializers.Serializer):
    url = serializers.URLField(required=False, allow_blank=True)


class DailyTaskSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False, allow_null=True)
    title = serializers.CharField(max_length=255)
    description = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    is_development_task = serializers.BooleanField(default=False)
    pr_link = TaskPRLinkSerializer(required=False)
    status = serializers.ChoiceField(choices=TaskConstants.STATUS_CHOICES)
    hours = serializers.IntegerField(default=0)
    minutes = serializers.IntegerField(default=0)


class DailyReportCreateSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    report_date = serializers.DateField()
    description = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    status = serializers.ChoiceField(choices=DailyReportConstants.STATUS_CHOICES)
    tasks = DailyTaskSerializer(many=True)
