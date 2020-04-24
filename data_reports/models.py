import boto3
import csv

from datetime import date, timedelta

from django.conf import settings

class UsageReport():

  CONFIG = {
    "page_views": {
      "sql_file": "/data_reports/scripts/page_views_export_report.sql",
      "results_file": "Page views"

    },
    "downloads": {
      "sql_file": "/data_reports/scripts/downloads_export_report.sql",
      "results_file": "Downloads"
    }
  }
  
  @classmethod
  def generate_report(cls, report_type):
    report_config = cls.CONFIG[report_type]
    athena_client = boto3.client('athena', region_name=settings.AWS_REGION_DEPLOYMENT)

    sql_command = cls.get_sql_command(report_config['sql_file'])
    
    query_id = cls.run_query(athena_client, sql_command)

    query_results = cls.get_results(athena_client, query_id)

    filename = cls.generate_csv(query_results, report_config['results_file'])

    return filename


  @classmethod
  def get_sql_command(cls, sql_file):
    file = open(settings.BASE_DIR + sql_file, "r")
    return file.read()

  @classmethod
  def run_query(cls, client, sql_command):
    response = client.start_query_execution(
      QueryString=sql_command,
      ResultConfiguration={
        'OutputLocation': settings.ATHENA_OUTPUT_BUCKET,
      },
      WorkGroup=settings.ATHENA_WORKGROUP
    )

    return response['QueryExecutionId']

  @classmethod
  def get_results(cls, client, query_id):
    response = client.get_query_results(
      QueryExecutionId=query_id
    )
    return response['ResultSet']

  @classmethod
  def generate_csv(cls, results, results_file):
    headers = cls.get_headers(results['ResultSetMetadata']['ColumnInfo'])
    processed_results = cls.process_results(results['Rows'])
    
    yesterday = date.today() - timedelta(days=1).strftime('%d-%m-%y')
    filename = "{0} {1}.csv".format(results_file, yesterday)

    with open(filename, 'wb') as csvfile:
      filewriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
      filewriter.writerow(headers)
      for row in processed_results:
        filewriter.writerow(row)

    return filename

  @classmethod
  def get_headers(cls, column_info):
    headers = []
    for column in column_info:
      headers.push(column['Label'])
    return headers

  @classmethod
  def process_results(cls, rows):
    processed_results = []
    for row in rows:
      data = []
      for field in row['Data']:
        data.push(field['VarCharValue'])
      processed_results.push(data)
    return processed_results
