FROM python:3.6

ENV PYTHONUNBUFFERED 1
ENV DJANGO_ENV dev

WORKDIR /code
COPY ./requirements.txt /code/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN apt-get update
RUN apt-get install cron vim -y
RUN touch /var/log/cron.log

RUN apt-get update && apt-get install redis-server -y

COPY . /code/

RUN python manage.py compilescss
RUN python manage.py  collectstatic --ignore=*.scss --no-input
RUN chmod +x ./deploy_files/docker-entrypoint.sh

ENTRYPOINT ["./deploy_files/docker-entrypoint.sh"]

