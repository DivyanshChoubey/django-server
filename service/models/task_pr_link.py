from django.db import models
from service.models import DailyTask


class TaskPRLink(models.Model):
    task = models.ForeignKey(DailyTask,on_delete=models.CASCADE,related_name="pr_links")
    pr_url = models.URLField()

    class Meta:
        db_table = "task_pr_link"
        indexes = [
            models.Index(fields=["task"]),
        ]
