#!/usr/bin/python
# -*- coding: utf-8 -*-
# Date: 2018/11/5
# Autor :  zlw dwk zly


from netmiko import ConnectHandler
import csv
import yaml
import os
import sys
sys.path.append('plugins')
import store
import parse
from log import log_instance

'''
连接设备
device_info: list csv中的设备信息
commonds: list yml中的commonds
return :  list 返回设备输出的结果
'''

def connect(device_info, commands):
    ip = device_info[0]
    protocol = device_info[1]
    device_type = device_info[2]
    username = device_info[3]
    password = device_info[4]
    secret = device_info[5]
    name = device_info[6]
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

    log_instance.info("'{0}'-'{1}' start connecting.".format(ip, name))
    net_connect = ConnectHandler(**cisco_device)
    net_connect.enable()

    result = []
    for cmd in commands:
        result.append(net_connect.send_command(cmd))
    net_connect.disconnect()
    return result

'''
读取CSV设备信息文件，对比yml中的ip
ip: string yml中的ip
commonds: list yml中的commonds
return :  list 返回设备输出的结果
'''
def read_csv(ip, commands):
    result = []
    with open('config.csv', mode='r') as f:
        # 逐行读入csv
        f_csv = csv.reader(f)
        for row in f_csv:
            if ip == row[0]:
                result = connect(row, commands)
            else:
                pass
    return result

'''
读取yml文件，并执行解析，存储
tables: string 配置文件的目录名
'''
def run(tables):
    path = "commands/" + tables
    files = os.listdir(path)
    for file in files:
        if not os.path.isdir(file):
            f = open(path + "/" + file)
            y = yaml.load(f)
            tmp = read_csv(y['ip'], y['commands'])
            if tables == 'ping':
                # print(y['device_name'])
                try:
                    store.ping(y['device_name'], parse.ping(tmp))
                except Exception as e:
                    log_instance.error(e)
            elif tables == 'cpu_memory':
                # print(y['device_name'], tmp)
                try:
                    store.cpu_mem(y['device_name'], parse.cpu_mem(tmp))
                except Exception as e:
                    log_instance.error(e)
            elif tables == 'flow':
                # print(y['device_name'], tmp)
                try:
                    store.flow(y['device_name'], parse.flow(tmp))
                except Exception as e:
                    log_instance.error(e)
            elif tables == 'interface':
                # print(y['device_name'], tmp)
                try:
                    store.interface(y['device_name'], parse.interface(tmp))
                except Exception as e:
                    log_instance.error(e)
            else:
                log_instance.error("不存在配置文件，请检查输入的目录名")
        else:
            log_instance.error("不存在配置文件，请检查目录结构")
            pass
            