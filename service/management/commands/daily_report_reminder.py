import time
from datetime import datetime, timezone

from django.core.management.base import BaseCommand
from django_server import settings

from service.management.cron import DailyReportReminderCron
from service.utils import logger
from service.constants import ResponseMessages


class Command(BaseCommand):
    def handle(self, *args, **options):
        run_mode = settings.RUN_MODE

        if run_mode == "specific_time":
            self._run_specific_time()
        elif run_mode == "interval":
            self._run_interval_time()
        else :
            self.stdout.write(
                self.style.ERROR(
                    ResponseMessages.INVALID_RUN_MODE
                )
            )

    def _run_specific_time(self):
        last_execution_time = None
        while True:
            current_datetime = datetime.now(timezone.utc)
            current_date = current_datetime.date()
            current_time  = current_datetime.strftime("%H:%M:%S")
            if (current_time == settings.SPECIFIC_TIME) and (last_execution_time != current_date):
                self._execution()
                last_execution_time = current_date 
                logger.info(ResponseMessages.REMINDER_EMAIL_SENT_SUCCESSFULLY)
            time.sleep(settings.SLEEP_SECONDS)

    def _run_interval_time(self):
        while True:
            self._execution()
            time.sleep(settings.TIME_INTERVAL)
            logger.info(ResponseMessages.INTERVAL_REMINDER_EMAIL_SENT_SUCCESSFULLY)

    def _execution(self): 
        try:
            cron = DailyReportReminderCron()
            cron.initiate()
            self.stdout.write(
                self.style.SUCCESS(
                    ResponseMessages.CRON_EXECUTE_SUCCESS
                )
            )
        except Exception as error:
            self.stdout.write(
                self.style.ERROR(f"Cron failed: {str(error)}")
                )
