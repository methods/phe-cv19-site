"""
Schedule wagtail managment tasks and other admin with cron.
"""

import difflib
import logging
import yaml

from crontab import CronTab

logger = logging.getLogger(__name__)


def read_config(config_path: str = "management_cron_jobs.yml") -> dict:
    """
    Read config from yaml file found at config_path and return as dict.
    """
    with open(config_path, "r") as f:
        return yaml.safe_load(f)


def _log_and_print(msg: str):
    print(msg)
    logger.info(msg)


def _set_job_schedule(job, period_units, period):
    period_units = difflib.get_close_matches(
        period_units, ("second", "minute", "hour", "day"), n=1
    )[0]
    if period_units == "second":
        job.second.every(period)
    if period_units == "minute":
        job.minute.every(period)
    if period_units == "hour":
        job.hour.every(period)
    if period_units == "day":
        job.day.every(period)


def schedule_cron_jobs():
    """
    Load config and add jobs to cron tab. If config["clean_old_jobs"]=True, clear out old jobs first.
    """
    config = read_config()
    cron_user = config["cron_user"]

    if config["clean_old_jobs"]:
        with CronTab(user=cron_user) as cron:
            _log_and_print(f"Clearing crontab for user {cron_user}")
            cron.remove_all()

    for cron_job in config["cron_jobs"]:
        with CronTab(user=cron_user) as cron:
            job_name = cron_job["name"]
            job_command = cron_job["command"]
            period_units = cron_job["period_units"]
            period = cron_job["period"]
            job = cron.new(command=job_command, comment=job_name)
            _set_job_schedule(job, cron_job["period_units"], cron_job["period"])
            _log_and_print(f"Cron job {job_name} added to crontab for user {cron_user}")


if __name__ == "__main__":
    schedule_cron_jobs()
