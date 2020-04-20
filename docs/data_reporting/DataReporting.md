Data Reporting
=======================

<!-- vim-markdown-toc GitLab -->

* [Accessing the data](#accessing-the-data)
* [Producing daily reports](#producing-daily-reports)
  * [Page views report](#page-views-report)
  * [Resource downloads report](#resource-downloads-report)

<!-- vim-markdown-toc -->

-----
The usage data for this project is being gathered using CloudFronts access log capability, the logs for page views and resource downloads are being stored in S3 buckets (named `<environment>-logs-<distribution>-coronavirusresources.phe.gov.uk`).

## Accessing the data

The data files produced by CloudFront are .txt files for each request received. To access them in a useful format you will need to import them in to an AWS Athena database.

The script to load the logs in to a database can be found [here](logs_import_script.sql).

## Producing daily reports

There are 2 daily reports required by PHE; page views and resource downloads.

### Page views report

The page views report needs to contain a list of all pages requested on a specfied date with aggregate counts of success and error responses.
The script to produce this data set can be found [here](page_views_export_script.sql)

### Resource downloads report

The page views report needs to contain a list of all downloadable resources requested on a specfied date with aggregate counts of success and error responses.
The script to produce this data set can be found [here](downloads_export_script.sql)

(The `[` at the start of the dates in the above scripts is meant to be there, it is to account for a remnant of the import process)
