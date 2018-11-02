#!/usr/bin/python
# -*- coding: utf-8 -*-
# Date: 2018/10/31

from netmiko import ConnectHandler
import datetime
import os
import csv
import logging
import yaml
import re
from log import logmode
from apscheduler.schedulers.blocking import BlockingScheduler

#创建一个log实例
logger = logmode('daily-work').getlog()
log_ap = logmode('apscheduler').getlog()


#login and resolve result
def connect_devices(device_info, commands):
    ip = device_info[0]
    protocol = device_info[1]
    device_type = device_info[2]
    username = device_info[3]
    password = device_info[4]
    secret = device_info[5]
    port = 22 if protocol == 'ssh' else 23

    device_type = device_type + '_telnet' if protocol == 'telnet' else device_type

    cisco_device = {
        'device_type': device_type,
        'ip': ip,
        'username': username,
        'password': password,
        'port': port,  # optional, defaults to 22
        'secret': secret,  # optional, defaults to ''
        'verbose': False,  # optional, defaults to False
    }

    net_connect = ConnectHandler(**cisco_device)
    net_connect.enable()

    result = []
    # print(commands)
    for cmd in commands:
        result.append(net_connect.send_command(cmd))
    # print(result)

    net_connect.disconnect()
    return result


def parsing_ping(result, device_name):
    ping_result_write = []
    for row in result:
        if row == '':
            pass
        else:
            matchObj = re.search(
                r'.* rate is (.*?) .*max = (.*?)/(.*?)/(.*?) (.*)', row,
                re.M | re.I)
            percent = 100 - int(matchObj.group(1))
            avg = matchObj.group(3)
            unit = matchObj.group(5)

            ping_result = {
                'percent': percent,
                'avg': avg,
                'unit': unit,
            }
            ping_result_write.append(ping_result)
            #to do save
    print(device_name,ping_result_write)


#read the csv
def read_csv(ip, commands):
    result = []
    with open('config.csv', mode='r') as f:
        # 逐行读入csv
        f_csv = csv.reader(f)
        for row in f_csv:
            if ip == row[0]:
                result = connect_devices(row, commands)
            else:
                pass
    return result


# main
def read_yml(tables):
    path = "commands/" + tables
    files = os.listdir(path)
    for file in files:
        if not os.path.isdir(file):
            f = open(path + "/" + file)
            y = yaml.load(f)
            tmp = read_csv(y['ip'], y['commands'])
            parsing_ping(tmp, y['device_name'])
        else:
            pass


def job():
    read_yml('ping')


def main():
    # logger.info('start daily network ')
    scheduler = BlockingScheduler()
    # scheduler.add_job(job, 'cron', day_of_week='1-5', hour=8, minute=00)
    scheduler.add_job(job, 'interval', seconds=60)
    scheduler.start()
    job.remove()
    # logger.info('end')
    


if __name__ == '__main__':
    main()
