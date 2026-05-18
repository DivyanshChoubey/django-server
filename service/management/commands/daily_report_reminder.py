import time

from django.core.management.base import BaseCommand

from service.management.cron import DailyReportReminderCron
from service.utils import logger


class Command(BaseCommand):
    help = "Run daily report reminder cron"

    def add_arguments(self, parser):
        parser.add_argument(
            "--interval",
            type=int,
            default=5,
            help="Cron execution interval in seconds",
        )

    def handle(self, *args, **options):
        interval = options.get("interval")
        self.stdout.write(
            self.style.SUCCESS(
                f"Daily report reminder cron started. Interval: {interval} seconds"
            )
        )
        while True:
            try:
                cron = DailyReportReminderCron()
                cron.initiate()

                self.stdout.write(
                    self.style.SUCCESS(
                        "Daily report reminder cron executed successfully"
                    )
                )
            except Exception as error:
                self.stdout.write(
                    self.style.ERROR(f"Cron failed: {str(error)}")
                )
            time.sleep(interval)
