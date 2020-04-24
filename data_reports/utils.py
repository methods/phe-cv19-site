from datetime import date, timedelta

from django.contrib.auth.models import User
from django.core.mail import EmailMessage

from data_reports.models import PageViewReport

def create_daily_usage_report():
  page_views_report_file = UsageReport.generate_report('page_views')
  downloads_report_file = UsageReport.generate_report('downloads')
  data_team_emails = User.objects.filter(groups__name='Data team').values_list('email', flat=True)

  report_date = date.today() - timedelta(days=1).strftime('%d-%m-%y')

  message = EmailMessage('Usage reports {0}'.format(report_date), 'Attached are the daily usage report', settings.DEFAULT_FROM_EMAIL, data_team_emails)
  
  attachment = open(page_views_report_file, 'r')
  message.attach(page_views_report_file, attachment.read(), 'text/csv')

  attachment = open(downloads_report_file, 'r')
  message.attach(downloads_report_file, attachment.read(), 'text/csv')

  message.send()
