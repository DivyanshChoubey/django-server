import time
from datetime import datetime, timezone, timedelta

from django.core.management.base import BaseCommand

from service.management.cron import DailyReportReminderCron
from service.utils import logger
from service.constants import ResponseMessages, ReportReminderConstants


class Command(BaseCommand):
    def handle(self, *args, **options):
        if not ReportReminderConstants.REPORT_REMINDER_CRON_EXECUTION:
            self.stdout.write(
                self.style.ERROR(
                    ResponseMessages.REPORT_REMINDER_CRON_OFF
                )
            )
            return
        else:
            self.stdout.write(
                self.style.SUCCESS(
                    ResponseMessages.REPORT_REMINDER_CRON_ON
                )
            )
        run_mode = ReportReminderConstants.REPORT_REMINDER_CRON_RUN_MODE

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
        cron_run_time = ReportReminderConstants.REPORT_REMINDER_CRON_SPECIFIC_TIME
        target_time = datetime.strptime(cron_run_time, "%H:%M:%S").time()
        logger.info(f"Cron configured to run at: {cron_run_time} UTC")
        while True:
            try:
                current_datetime = datetime.now(timezone.utc)
                current_date = current_datetime.date()
                next_run_datetime = datetime.combine(
                    current_date,
                    target_time,
                    tzinfo=timezone.utc
                )
                if current_datetime >= next_run_datetime:
                    next_run_datetime += timedelta(days=1)
                sleep_seconds = int((next_run_datetime - current_datetime).total_seconds())
                logger.info(
                    f"Next cron scheduled for: {next_run_datetime.strftime('%Y-%m-%d %H:%M:%S')} UTC"
                )
                time.sleep(sleep_seconds)
                logger.info(
                    f"Cron execution started at: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')} UTC"
                )
                self._execution()
                logger.info(ResponseMessages.REMINDER_EMAIL_SENT_SUCCESSFULLY)
            except Exception as error:
                logger.exception(f"Error while running reminder cron: {str(error)}")
                time.sleep(ReportReminderConstants.REPORT_REMINDER_CRON_SLEEP_SECONDS)

    def _run_interval_time(self):
        while True:
            self._execution()
            time.sleep(ReportReminderConstants.REPORT_REMINDER_CRON_TIME_INTERVAL)
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
