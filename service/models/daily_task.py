from django.db import models
from service.constants import TaskConstants
from service.models import DailyReport


class DailyTask(models.Model):
    report = models.ForeignKey(DailyReport,on_delete=models.CASCADE,related_name="tasks")
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    is_development_task = models.BooleanField(default=False)
    status = models.CharField(max_length=20,choices=TaskConstants.STATUS_CHOICES,default=TaskConstants.NOT_STARTED)
    hours = models.IntegerField(default=0)
    minutes = models.IntegerField(default=0)

    class Meta:
        db_table = "daily_task"
        indexes = [
            models.Index(fields=["report"]),
            models.Index(fields=["status"]),
        ]
