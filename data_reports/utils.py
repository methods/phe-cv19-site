from datetime import date, timedelta

from django.contrib.auth.models import User
from django.core.mail import EmailMessage

from data_reports.models import PageViewReport

def create_daily_usage_report():
  page_views_report_file = UsageReport.generate_report('page_views')
  downloads_report_file = UsageReport.generate_report('downloads')
