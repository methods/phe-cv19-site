from django.core.management.base import BaseCommand
from data_reports.utils import create_daily_usage_report


class Command(BaseCommand):
    """
    Produce daily usage reports
    """
    help = 'Export usage reports CSV to the data team'

    def handle(self, *args, **kwargs):
        """
        Actual command procesing goes here
        """
        create_daily_usage_report()
