FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/

RUN python manage.py compilescss
RUN python manage.py  collectstatic --ignore=*.scss

RUN chmod +x ./deploy_files/docker-entrypoint.sh

RUN apt-get update
RUN apt-get install cron vim -y
RUN touch /var/log/cron.log
