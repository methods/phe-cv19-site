#!/bin/bash
set -e

until python manage.py makemigrations && python3 manage.py migrate
do
  echo "Waiting for database to be migrated"
  sleep 5
done

# start redis
echo "Starting Redis message broker for celery..."
service redis-server start

# start single, non-concurrent celery worker for 'core' app, logging INFO to /var/log/celery.log
echo "Starting celery..."
celery worker -A core -l INFO -f /var/log/celery.log -c 1 --detach

# start cron & schedule cron jobs
echo "Starting cron..."
cron service start
echo "Scheduling management cron jobs..."
python3 CMS/settings/management_cron_jobs.py

#Run Gunicorn
exec gunicorn CMS.wsgi:application \
  --name methods-cms \
  --bind 0.0.0.0:8000 \
  --workers 3 \
  --log-level=info \
  --log-file=- \
  --access-logfile=- \
  --error-logfile=- \
  --timeout 600 \
  --max-requests 1000


# EXECUTE DOCKER COMMAND NOW
exec "$@"
