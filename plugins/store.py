#!/usr/bin/python
# -*- coding: utf-8 -*-
# Date: 2018/11/9
# Autor :  zlw dwk zly

import datetime
from pymongo import MongoClient
import copy
Client = MongoClient('mongodb://localhost:27017/')
try:
    db = Client['daily_network']
except Exception as e:
    print(e)
collection_line = db['line']
collection_device = db['device']
current_date = datetime.datetime.now().strftime("%Y-%m-%d")
hour = datetime.datetime.now().strftime("%H")
print(current_date)
print(hour)

line = {
    "name": None,  # name --> string 线路名称
    "type": "line",  # type --> [] 数据类型
    "loss": [],  # loss --> [] 丢包率
    "delay": [],  # delay --> [] 线路延迟
    "flow_in_am": [],  # flow_in_am --> [] 上午的下行流量
    "flow_out_am": [],  # flow_out_am --> [] 上午的上行流量
    "flow_in_pm": [],  # flow_in_pm_ --> [] 下午的上行流量
    "flow_out_pm": []  # flow_out_pm --> []下午的下行流量
}

device = {
    "name": None,  # name --> string 设备名称
    "type": "device",  # type --> [] 数据类型
    "interface": [],  # interface --> [] 包含每天的接口总数，剩余数
    "cpu": [],  # cpu --> [] cpu百分比
    "memory": [],  # memory --> [] 内存百分比
}

# aviable_line = []
# line_name_mongo = collection_line.find({"type": "line"})
# for document in line_name_mongo:
#     aviable_line.append(document["name"])
# print(aviable_line)


def ping(line_name, result):
    loss = result['loss']
    delay = result['delay_avg']
    ping_line = copy.deepcopy(line)
    ping_line.update(
        {
    "name": line_name,  
    "type": "line",  
    "loss": [],  
    "delay": [],  
    "flow_in_am": [],  
    "flow_out_am": [],  
    "flow_in_pm": [],  
    "flow_out_pm": []  
       }
    )
    collection_line.find_one_and_update({
        'name': line_name
    }, {'$push': {
        'loss': [{
            'date': current_date,
            'loss': loss
        }]
    },'$push': {
        'delay': [{
            'date': current_date,
            'delay': delay
        }]
    }},
    
    upsert=True)

    # collection_line.update({'name'= line_name},{"$push":{"loss":}} upsert=True)




def flow(line_name, result):
    flow_in_am = flow_result['in'] if hour < 12 else flow_in_pm = result['in']
    flow_out_am = flow_result['out'] if hour < 12 else flow_out_pm = result[
        'out']
    name = line


def interface(device_name, result):
    total = result['total']
    aviable = result['aviable']


def cpu_men(device_name, result):
    cpu = result['cpu']
    mem = result['mem']
