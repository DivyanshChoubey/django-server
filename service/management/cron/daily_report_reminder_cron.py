from service.constants import DailyReportConstants
from service.models import Users
from service.utils import EmailHandler, DateTimeUtils,logger
from service.constants import ResponseMessages


class DailyReportReminderCron:
    def __init__(self):
        pass

    def initiate(self):
        try:
            users = self.get_users_to_remind()
            if not users:
                logger.info(ResponseMessages.NO_USER_REQUIRE_REMINDER)
                return
            email_handler = EmailHandler()
            email_handler.send_bulk_email(users)
            logger.info(ResponseMessages.REMINDER_EMAILS_SENT_SUCCESS)
        except Exception as error:
            logger.exception(
                f"errors while executing DailyReportReminderCron: {str(error)}"
            )

    def get_users_to_remind(self):
        return Users.objects.filter(
            is_active=True
        ).exclude(
            dailyreport__report_date=DateTimeUtils.get_today_date(),
            dailyreport__status=DailyReportConstants.SUBMITTED
        ).distinct().values_list("first_name", "email")
