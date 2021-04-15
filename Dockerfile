FROM python:3.6

ENV PYTHONUNBUFFERED 1

WORKDIR /code
COPY ./requirements.txt /code/
RUN cat /etc/os-release && pip install --upgrade pip
RUN pip install -r requirements.txt
RUN apt-get update && apt-get upgrade -y
RUN apt-get install cron vim -y
RUN touch /var/log/cron.log
ENV TZ=Europe/London

COPY . /code/

RUN python manage.py compilescss
RUN python manage.py  collectstatic --ignore=*.scss --no-input
RUN chmod +x ./deploy_files/docker-entrypoint.sh

# ENTRYPOINT ["./deploy_files/docker-entrypoint.sh"]

