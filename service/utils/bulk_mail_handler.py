from django.core.mail import send_mail


class BulkMailHandler:
    def __init__(self):
        pass

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
