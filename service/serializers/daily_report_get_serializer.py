from rest_framework import serializers

from service.models import DailyReport, DailyTask, TaskPRLink

class TaskPRLinkSerializer(serializers.ModelSerializer):
    url = serializers.CharField(source="pr_url")

    class Meta:
        model = TaskPRLink
        fields = [
            "id",
            "url"
        ]


class DailyTaskSerializer(serializers.ModelSerializer):
    pr_link = serializers.SerializerMethodField()

    class Meta:
        model = DailyTask
        fields = [
            "id",
            "title",
            "description",
            "is_development_task",
            "pr_link",
            "status",
            "hours",
            "minutes"
        ]


    def get_pr_link(self, obj):
        pr_link = obj.pr_links.first()

        if not pr_link:
            return None

        return TaskPRLinkSerializer(pr_link).data

class DailyReportGetSerializer(serializers.ModelSerializer):
    tasks = DailyTaskSerializer(many=True)

    class Meta:
        model = DailyReport
        fields = [
            "id",
            "report_date",
            "description",
            "status",
            "tasks"
        ]
