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

COPY . /code/

# RUN useradd wagtail
# RUN chown -R wagtail /code
# USER wagtail
