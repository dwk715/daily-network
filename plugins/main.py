#!/usr/bin/python
# -*- coding: utf-8 -*-
# Date: 2018/10/31
# Autor : dwk zlw zly 



from apscheduler.schedulers.blocking import BlockingScheduler


def job_ping():
    read_yml('ping')


def job_flow():
    read_yml('flow')
  

def job_cup_memory():
    read_yml('cpu_memory')


def job_interface():
    read_yml('interface')
  

def main():
    scheduler = BlockingScheduler()
    scheduler.add_job(job_interface, 'cron', day_of_week='0-6', hour=8, minute=00)
    scheduler.add_job(job_cup_memory, 'cron', day_of_week='0-6', hour=10, minute=30)
    scheduler.add_job(job_flow, 'cron', day_of_week='0-6', hour=10, minute=30)
    scheduler.add_job(job_flow, 'cron', day_of_week='0-6', hour=22, minute=20)
    scheduler.add_job(job_ping, 'cron', day_of_week='0-6', hour=8, minute=00)
    # read_yml('interface')
    scheduler.start()

if __name__ == '__main__':
    main()