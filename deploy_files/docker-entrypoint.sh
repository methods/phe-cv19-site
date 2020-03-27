#!/bin/bash
set -e

until python3 manage.py migrate
do
  echo "Waiting for database to be migrated"
  sleep 5
done

# start cron
exec cron service start

#Run Gunicorn
exec gunicorn CMS.wsgi:application \
  --name methods-cms \
  --bind 0.0.0.0:80 \
  --workers 3 \
  --log-level=info \
  --log-file=- \
  --access-logfile=- \
  --error-logfile=- \
  --timeout 60 \
  --max-requests 1000


# EXECUTE DOCKER COMMAND NOW
exec "$@"
