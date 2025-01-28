#!/usr/bin/env python3
import os
import subprocess
import time
from datetime import datetime, timedelta

# Function to parse and check missed cron jobs
def check_missed_cron_jobs():
    # Get the current user's crontab entries
    result = subprocess.run(['crontab', '-l'], stdout=subprocess.PIPE)
    cron_jobs = result.stdout.decode('utf-8').splitlines()

    gitCron = ""

    for cron in cron_jobs:
        if "update_number.py" in cron:
            gitCron = cron
            break

    # Example cron job format: '*/5 * * * * /path/to/script.sh'
    time_parts, command = gitCron.split(maxsplit=5)[:5], gitCron.split(maxsplit=5)[5]

    # Parse schedule
    schedule = f'{time_parts[0]} {time_parts[1]} {time_parts[2]} {time_parts[3]} {time_parts[4]}'
    
    # Get the next scheduled run time
    next_run = get_next_run_time(schedule)

    # Check if the job was missed
    if next_run < datetime.now():
        print(f"Missed job: {command}")
        print(f"Running missed job: {command}")
        subprocess.run(command, shell=True)

# Function to calculate the next scheduled run time
def get_next_run_time(schedule):
    # This is a simplified version for illustrative purposes
    now = datetime.now()
    next_run = now

    # Parse crontab fields (this part would need more comprehensive parsing)
    minute, hour, day, month, weekday = schedule.split()
    
    if minute == '*':
        next_run = next_run.replace(second=0, microsecond=0) + timedelta(minutes=1)
    else:
        next_run = next_run.replace(minute=int(minute), second=0, microsecond=0)
    
    if hour != '*':
        next_run = next_run.replace(hour=int(hour))

    # Add more logic to handle day, month, and weekday

    return next_run

if __name__ == "__main__":
    check_missed_cron_jobs()
