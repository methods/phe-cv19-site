from data_reports.models import PageViewReport

def create_daily_usage_report():
  page_views_report_file = UsageReport.generate_report('page_views')
  downloads_report_file = UsageReport.generate_report('downloads')
  # attach the files to an email and send to the users in the 'Data team' user group.
