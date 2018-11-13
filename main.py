#!/usr/bin/python
# -*- coding: utf-8 -*-
# Date: 2018/11/5
# Autor :  zlw dwk zly

from apscheduler.schedulers.blocking import BlockingScheduler
import sys
sys.path.append('plugins')
import task
from log import log_instance
# from log import logmode

# log_ap = logmode('daily-network').getlog()


def job_ping():
    task.run('ping')


def job_flow():
    task.run('flow')


def job_cup_memory():
    task.run('cpu_memory')


def job_interface():
    task.run('interface')

'''
实例化BlockingScheduler
添加定时计划
'''
scheduler = BlockingScheduler()
scheduler.add_job(job_interface, 'cron', day_of_week='0-6', hour=10, minute=10)
scheduler.add_job(
    job_cup_memory, 'cron', day_of_week='0-6', hour=10, minute=30)
scheduler.add_job(job_flow, 'cron', day_of_week='0-6', hour=10, minute=30)
scheduler.add_job(job_flow, 'cron', day_of_week='0-6', hour=22, minute=20)
scheduler.add_job(job_ping, 'cron', day_of_week='0-6', hour=8, minute=00)

'''
主函数
开启scheduler
'''
def main():
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
    except Exception as e:
        log_instance.error(e)
    
    # task.run('flow')
    # task.run('ping')
    # task.run('cpu_memory')
    # task.run('interface')
    


    
if __name__ == '__main__':
    main()