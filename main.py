#!/usr/bin/python
# -*- coding: utf-8 -*-
# Date: 2018/11/5
# Autor :  zlw dwk zly



from apscheduler.schedulers.blocking import BlockingScheduler
import sys
sys.path.append('plugins')
import task
from log import logmode

log_ap = logmode('apscheduler').getlog()

def job_ping():
    task.run('ping')


def job_flow():
    task.run('flow')
  

def job_cup_memory():
    task.run('cpu_memory')


def job_interface():
    task.run('interface')
  
scheduler = BlockingScheduler()
scheduler.add_job(job_interface, 'cron', day_of_week='0-6', hour=8, minute=00)
scheduler.add_job(job_cup_memory, 'cron', day_of_week='0-6', hour=10, minute=30)
scheduler.add_job(job_flow, 'cron', day_of_week='0-6', hour=10, minute=30)
scheduler.add_job(job_flow, 'cron', day_of_week='0-6', hour=22, minute=20)
scheduler.add_job(job_ping, 'cron', day_of_week='0-6', hour=8, minute=00)
def main():
    try:
        # task.run('ping')
        task.run('flow')
        scheduler.start()
    except (KeyboardInterrupt, SystemExit): 
        scheduler.shutdown()
if __name__ == '__main__':
    main()