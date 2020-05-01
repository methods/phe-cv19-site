"""
Schedule wagtail managment tasks and other admin with cron.
"""

import difflib
import getpass
import logging
import os
import shutil
import subprocess
import sys
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
    if period_units == "second":
        job.second.every(period)
    elif period_units == "minute":
        job.minute.every(period)
    elif period_units == "hour":
        job.hour.every(period)
    elif period_units == "day":
        job.day.every(period)
    elif period_units == "daily":
        job.hour.on(period)


def write_mgmt_task_runner(
    mgmt_command: str,
    working_dir: str,
    runner_dir: str,
    logging: bool = False,
    logfile: str = "",
) -> str:
    """
    Write executable shell script to run management task with cron, and return
    bash statement to run it. The task runner will be written to the runner_dir,
    but the returned bash statement will execute it from the working_dir
    (presumed to be the project root).

    The task runner bash script does this:
        - exports all env vars found in the env this script was executed from.
        - cds to working_dir and calls manage.py to run the mgmt_task, using
        the python interpreter that was used to execute this script.
    """
    runner_file_lines = ["#!/bin/bash"]

    # append export statements for complete env to runner file
    runner_file_lines += [f"export {k}={v}" for k, v in os.environ.items()]

    # get path to python intepreter in use by the script caller
    python_interpreter = sys.executable

    # add the execution command
    log_start_str = (
        f'(echo "=== $(date) ===> Executing {mgmt_command}" &&' if logging else ""
    )
    log_stop_str = f") >> {logfile} 2>&1" if logging else ""
    execute_str = f"{log_start_str} cd {working_dir} && {python_interpreter} manage.py {mgmt_command} {log_stop_str} "
    runner_file_lines.append(execute_str)

    # add empty line for luck
    runner_file_lines.append("")

    # write file to runner_dir
    runner_filename = f"run_{mgmt_command}.sh"
    runner_filepath = os.path.join(runner_dir, runner_filename)

    with open(runner_filepath, "w") as f:
        f.write("\n".join(runner_file_lines))

    # make file x-able
    subprocess.call(f"chmod +x {runner_filepath}", shell=True)

    _log_and_print(f"Job runner added to {runner_filepath}")

    # output cron command string
    return f"cd {working_dir} && {runner_filepath}"


def schedule_cron_jobs():
    """
    Load config and add jobs to cron tab. If config["clean_old_jobs"]=True, clear out old jobs first.
    """

    # dir setup
    working_dir = os.getcwd()
    runner_dir = os.path.join(working_dir, "cron_jobs")
    os.makedirs(runner_dir, exist_ok=True)

    # get config
    config = read_config()
    cron_user = (
        config["cron_user"]
        if config["cron_user"] != "current_user"
        else getpass.getuser()
    )
    logfile = config["logfile"]

    if config["clean_old_jobs"]:

        _log_and_print(f"Clearing crontab for user {cron_user}")
        with CronTab(user=cron_user) as cron:
            cron.remove_all()

        _log_and_print(f"Clearing job runners from {runner_dir}")
        shutil.rmtree(runner_dir)
        os.makedirs(runner_dir, exist_ok=True)

    for cron_job in config["cron_jobs"]:

        job_name = cron_job["name"]

        try:
            period_units = difflib.get_close_matches(
                cron_job["period_units"], ("second", "minute", "hour", "day"), n=1
            )[0]
        except IndexError:
            _log_and_print(
                f"Unrecognised period_units ({cron_job['period_units']}) for cron job {job_name} - job could not be added. Skipped."
            )
            continue

        period = cron_job["period"]
        cron_command = write_mgmt_task_runner(
            mgmt_command=cron_job["mgmt_command"],
            working_dir=working_dir,
            runner_dir=runner_dir,
            logging=cron_job["logging"],
            logfile=logfile,
        )

        with CronTab(user=cron_user) as cron:

            job = cron.new(command=cron_command, comment=job_name)
            _set_job_schedule(job, period_units, period)
            _log_and_print(f"Cron job {job_name} added to crontab for user {cron_user}")


if __name__ == "__main__":
    SCHEDULE_CRON_JOBS = os.environ.get("SCHEDULE_CRON_JOBS")
    if SCHEDULE_CRON_JOBS and SCHEDULE_CRON_JOBS.lower() == "true":
        schedule_cron_jobs()
    else:
        _log_and_print(
            "SCHEDULE_CRON_JOBS env var is unset or false, skipping scheduling of management tasks with cron."
        )
