from django.core.mail import send_mail


class EmailHandler:
    def __init__(self):
        pass

    def send_email(self, subject, message, recipient_list, from_email=None, fail_silently=False):
        send_mail(
            subject=subject,
            message=message,
            recipient_list=recipient_list,
            from_email=from_email,
            fail_silently=fail_silently,
        )

    def send_bulk_email(self, users):
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
