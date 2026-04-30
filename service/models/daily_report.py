from django.db import models
from service.constants import DailyReportConstants
from service.models import Users


class DailyReport(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    report_date = models.DateField()
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20,choices=DailyReportConstants.STATUS_CHOICES,default=DailyReportConstants.DRAFT)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "daily_report"
        constraints = [
            models.UniqueConstraint(
                fields=["user", "report_date"],
                name="unique_user_report_per_day"
            )
        ]
        indexes = [
            models.Index(fields=["user", "report_date"]),
            models.Index(fields=["status"]),
        ]
