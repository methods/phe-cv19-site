from data_reports.models import UsageReport

def create_daily_usage_report():
  page_views_report_file = UsageReport.generate_report('page_views')
  downloads_report_file = UsageReport.generate_report('downloads')
