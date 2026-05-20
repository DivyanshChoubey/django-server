from django.utils import timezone


class DateTimeUtils:
    def __init__(self):
        pass

    @classmethod
    def get_today_date(cls):
        return timezone.now().date()
