from django.utils import timezone


class DateUtils:
    def __init__(self):
        pass

    @classmethod
    def get_today_date(cls):
        return timezone.now().date()
