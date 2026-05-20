from django.core.mail import send_mass_mail, send_mail
from django_server import settings


class EmailHandler:
    def send_email(self, subject, message, recipient_list, from_email=None, fail_silently=False):
        send_mail(
            subject=subject,
            message=message,
            recipient_list=recipient_list,
            from_email=from_email,
            fail_silently=fail_silently,
        )

    def send_bulk_email(self, data):
        messages = []
        for first_name, email in data:
            message = (
                f"Hello {first_name},\n\n"
                "This is a reminder to submit your daily report for today.\n\n"
                "Thanks."
            )
            messages.append(
                (
                    "Daily Report Reminder",  
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    [email],
                )
            )

        send_mass_mail(
            messages,
            fail_silently=False
        )
