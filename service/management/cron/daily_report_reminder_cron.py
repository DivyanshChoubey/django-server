from django.core.mail import send_mail

from service.constants import DailyReportConstants
from service.models import Users
from service.utils import DateUtils


class DailyReportReminderCron:
    def __init__(self):
        pass
 
    def initiate(self):
        users = self.get_users_to_remind()
        self.send_reminder_email(users)
    
    def get_users_to_remind(self):
        return Users.objects.filter(
            is_active=True
        ).exclude(
            dailyreport__report_date=DateUtils.get_today_date(),
            dailyreport__status=DailyReportConstants.SUBMITTED
        ).distinct().values_list("first_name", "email")
    
    def send_reminder_email(self, users):
        for first_name, email in users:
            print(first_name)
            print(email)

            send_mail(
                subject="Daily Report Reminder",
                message=(
                    f"Hello {first_name},\n\n"
                    "This is a reminder to submit your daily report for today.\n\n"
                    "Thanks."
                ),
                from_email=None,
                recipient_list=[email],
                fail_silently=False,
            )

            print(f"Reminder mail sent to {email}")
