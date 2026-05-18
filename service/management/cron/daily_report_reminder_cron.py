from service.constants import DailyReportConstants
from service.models import Users
from service.utils import BulkMailHandler, DateUtils


class DailyReportReminderCron:
    def __init__(self):
        pass

    def initiate(self):
        users = self.get_users_to_remind()
        bulk_mail_handler = BulkMailHandler()
        bulk_mail_handler.send_bulk_email(users)

    def get_users_to_remind(self):
        return Users.objects.filter(
            is_active=True
        ).exclude(
            dailyreport__report_date=DateUtils.get_today_date(),
            dailyreport__status=DailyReportConstants.SUBMITTED
        ).distinct().values_list("first_name", "email")
