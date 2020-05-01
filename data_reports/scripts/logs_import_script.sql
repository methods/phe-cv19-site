CREATE EXTERNAL TABLE IF NOT EXISTS cloudfront_logs.{{table name}} (
  instance STRING,
  host STRING,
  datetime STRING,
  timezone STRING,
  ip STRING,
  `role` STRING,
  ref STRING,
  action_type STRING,
  object STRING,
  method STRING,
  path STRING,
  protocol STRING,
  response_code STRING,
  error STRING,
  file_size BIGINT,
  bytes_sent BIGINT
)
ROW FORMAT DELIMITED 
FIELDS TERMINATED BY ' '
LOCATION 's3://{{log bucket name}}'