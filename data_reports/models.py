import boto3
import csv

from datetime import date, timedelta

from django.conf import settings

class UsageReport():

  CONFIG = {
    "page_views": {
      "sql_file": "/data_reports/scripts/page_views_export_script.sql",
      "directory_name": "page_views_reports"

    },
    "downloads": {
      "sql_file": "/data_reports/scripts/downloads_export_script.sql",
      "directory_name": "downloads_reports"
    }
  }
  
  @classmethod
  def generate_report(cls, report_type):
    report_config = cls.CONFIG[report_type]
    athena_client = boto3.client('athena', region_name=settings.AWS_REGION_DEPLOYMENT, aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)

    sql_command = cls.get_sql_command(report_config['sql_file'])
    
    cls.run_query(athena_client, sql_command, report_config['directory_name'])


  @classmethod
  def get_sql_command(cls, sql_file):
    file = open(settings.BASE_DIR + sql_file, "r")
    return file.read()

  @classmethod
  def run_query(cls, client, sql_command, report_type):
    yesterday = (date.today() - timedelta(days=1)).strftime('%d-%m-%y')
    output_location = "s3://{0}/{1}/{2}/".format(settings.ATHENA_OUTPUT_BUCKET, report_type, yesterday)
    request_token = "{0}_{1}".format(yesterday, report_type)

    response = client.start_query_execution(
      QueryString=sql_command,
      ClientRequestToken=request_token,
      ResultConfiguration={
        'OutputLocation': output_location,
      },
      WorkGroup=settings.ATHENA_WORKGROUP
    )
