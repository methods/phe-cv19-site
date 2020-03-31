#!/bin/bash
set -e

until python3 manage.py migrate
do
  echo "Waiting for database to be migrated"
  sleep 5
done

# start redis
service redis-server start

# start celery worker pool for 'core' app, logging INFO to /var/log/celery.log
celery multi start worker -A core -l INFO -f /var/log/celery.log

#Run Gunicorn
exec gunicorn CMS.wsgi:application \
  --name methods-cms \
  --bind 0.0.0.0:8000 \
  --workers 3 \
  --log-level=info \
  --log-file=- \
  --access-logfile=- \
  --error-logfile=- \
  --timeout 300 \
  --max-requests 1000


# EXECUTE DOCKER COMMAND NOW
exec "$@"
